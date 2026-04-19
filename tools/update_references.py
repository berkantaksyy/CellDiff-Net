#!/usr/bin/env python3
"""Generate a public references list from local PDFs.

- Scans:   private/papers/*.pdf   (git-ignored)
- Extracts a best-effort title (macOS Spotlight `mdls` if available)
- Queries Crossref by title to find DOI/venue/year
- Writes:
    - references/papers.json
    - references/references.bib
    - docs/references.md

This is designed to keep the repo publishable without committing copyrighted PDFs.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

CROSSREF_API = "https://api.crossref.org/works"
DEFAULT_USER_AGENT = "stemcell-litreview/0.1 (mailto:unknown)"


@dataclass
class Paper:
    paper_id: str
    pdf_file: str
    title: str | None = None
    doi: str | None = None
    url: str | None = None
    year: int | None = None
    venue: str | None = None
    authors: list[str] | None = None


def _run_mdls(pdf_path: Path) -> dict[str, Any]:
    """macOS only: query Spotlight metadata."""
    try:
        proc = subprocess.run(
            [
                "mdls",
                "-name",
                "kMDItemTitle",
                "-name",
                "kMDItemAuthors",
                "-name",
                "kMDItemContentCreationDate",
                str(pdf_path),
            ],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except FileNotFoundError:
        return {}

    if proc.returncode != 0:
        return {}

    out: dict[str, Any] = {}
    for line in proc.stdout.splitlines():
        if "=" not in line:
            continue
        key, val = line.split("=", 1)
        out[key.strip()] = val.strip()
    return out


def extract_title_best_effort(pdf_path: Path) -> str | None:
    md = _run_mdls(pdf_path)
    raw = md.get("kMDItemTitle")
    if not raw:
        return None

    # raw examples: "\"Cellpose: ...\"" or "(null)"
    if raw == "(null)":
        return None
    if raw.startswith('"') and raw.endswith('"'):
        raw = raw[1:-1]
    raw = raw.strip()
    return raw or None


def _crossref_query_url(title: str) -> str:
    params = {"query.title": title, "rows": 1}
    return f"{CROSSREF_API}?{urllib.parse.urlencode(params)}"


def _crossref_lookup_via_urllib(url: str, *, user_agent: str, timeout_s: int) -> dict[str, Any] | None:
    req = urllib.request.Request(url, headers={"User-Agent": user_agent})
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            payload = json.loads(resp.read().decode("utf-8", errors="replace"))
    except Exception:
        return None

    items = payload.get("message", {}).get("items", [])
    if not items:
        return None
    return items[0]


def _crossref_lookup_via_curl(url: str, *, user_agent: str, timeout_s: int) -> dict[str, Any] | None:
    # curl often works on macOS even when python SSL certs are not configured.
    try:
        proc = subprocess.run(
            ["curl", "-s", "-L", "--max-time", str(int(timeout_s)), "-H", f"User-Agent: {user_agent}", url],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except FileNotFoundError:
        return None

    if proc.returncode != 0 or not proc.stdout.strip():
        return None

    try:
        payload = json.loads(proc.stdout)
    except Exception:
        return None

    items = payload.get("message", {}).get("items", [])
    if not items:
        return None
    return items[0]


def crossref_lookup(title: str, *, mailto: str | None, timeout_s: int = 20) -> dict[str, Any] | None:
    url = _crossref_query_url(title)

    user_agent = DEFAULT_USER_AGENT
    if mailto:
        user_agent = f"stemcell-litreview/0.1 (mailto:{mailto})"

    item = _crossref_lookup_via_urllib(url, user_agent=user_agent, timeout_s=timeout_s)
    if item is not None:
        return item

    return _crossref_lookup_via_curl(url, user_agent=user_agent, timeout_s=timeout_s)


def _get_year(item: dict[str, Any]) -> int | None:
    issued = item.get("issued", {}).get("date-parts")
    if isinstance(issued, list) and issued and isinstance(issued[0], list) and issued[0]:
        y = issued[0][0]
        return int(y) if isinstance(y, int) else None
    return None


def _get_venue(item: dict[str, Any]) -> str | None:
    ct = item.get("container-title")
    if isinstance(ct, list) and ct:
        return str(ct[0]).strip() or None
    if isinstance(ct, str):
        return ct.strip() or None
    return None


def _get_authors(item: dict[str, Any]) -> list[str] | None:
    authors = item.get("author")
    if not isinstance(authors, list) or not authors:
        return None
    out: list[str] = []
    for a in authors:
        given = (a.get("given") or "").strip()
        family = (a.get("family") or "").strip()
        name = (given + " " + family).strip()
        if name:
            out.append(name)
    return out or None


def _bibtex_key(p: Paper) -> str:
    base = re.sub(r"[^a-zA-Z0-9]+", "_", (p.title or p.paper_id)).strip("_")
    return (base[:50] or p.paper_id).lower()


def to_bibtex(p: Paper) -> str:
    key = _bibtex_key(p)
    fields: list[tuple[str, str]] = []

    if p.title:
        fields.append(("title", p.title))
    if p.authors:
        fields.append(("author", " and ".join(p.authors)))
    if p.venue:
        fields.append(("journal", p.venue))
    if p.year:
        fields.append(("year", str(p.year)))
    if p.doi:
        fields.append(("doi", p.doi))
    if p.url:
        fields.append(("url", p.url))

    body = ",\n".join([f"  {k} = {{{v}}}" for k, v in fields])
    return f"@article{{{key},\n{body}\n}}\n"


def write_docs_markdown(papers: list[Paper], out_path: Path) -> None:
    lines: list[str] = []
    lines.append("---")
    lines.append("title: References")
    lines.append("---")
    lines.append("")
    lines.append("# References")
    lines.append("")
    lines.append("This list is auto-generated from local PDFs under `private/papers/` (which are *not* committed).")
    lines.append("")

    for p in sorted(papers, key=lambda x: x.paper_id):
        title = p.title or p.paper_id
        parts: list[str] = []
        if p.year:
            parts.append(str(p.year))
        if p.venue:
            parts.append(p.venue)
        if not p.title:
            parts.append("missing title metadata — set in references/title_overrides.json")
        meta = " — ".join(parts)

        if p.url:
            lines.append(f"- **[{title}]({p.url})**{f' ({meta})' if meta else ''}")
        else:
            lines.append(f"- **{title}**{f' ({meta})' if meta else ''}")
        if p.doi:
            lines.append(f"  - DOI: `{p.doi}`")
    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf-dir", default="private/papers", help="Directory containing local paper PDFs")
    ap.add_argument("--cache", default="references/crossref_cache.json", help="Cache file for Crossref lookups")
    ap.add_argument(
        "--overrides",
        default="references/title_overrides.json",
        help="Optional JSON map of {paper_id: title} for PDFs with missing metadata",
    )
    ap.add_argument("--mailto", default=os.environ.get("CROSSREF_MAILTO"), help="Contact email for Crossref User-Agent")
    ap.add_argument("--sleep", type=float, default=0.2, help="Sleep between Crossref requests")
    ap.add_argument("--refresh", action="store_true", help="Ignore cache and re-query Crossref")
    args = ap.parse_args()

    pdf_dir = Path(args.pdf_dir)
    pdfs = sorted(pdf_dir.glob("*.pdf"))
    if not pdfs:
        print(f"No PDFs found under {pdf_dir}", file=sys.stderr)
        return 2

    cache_path = Path(args.cache)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        cache: dict[str, Any] = json.loads(cache_path.read_text(encoding="utf-8"))
    except Exception:
        cache = {}

    if not isinstance(cache, dict):
        cache = {}
    # Drop any old negative cache entries (e.g., null) so we can retry.
    cache = {k: v for k, v in cache.items() if isinstance(v, dict)}

    overrides_path = Path(args.overrides)
    try:
        overrides: dict[str, str] = json.loads(overrides_path.read_text(encoding="utf-8"))
    except Exception:
        overrides = {}
    if not isinstance(overrides, dict):
        overrides = {}

    papers: list[Paper] = []
    missing_title_ids: list[str] = []

    for pdf in pdfs:
        paper_id = pdf.stem
        override_title = str(overrides.get(paper_id, "")).strip()
        title = override_title or extract_title_best_effort(pdf)
        p = Paper(paper_id=paper_id, pdf_file=str(pdf))
        p.title = title

        if not title:
            missing_title_ids.append(paper_id)

        if title:
            item: dict[str, Any] | None = None

            if not args.refresh:
                cached = cache.get(title)
                if isinstance(cached, dict):
                    item = cached

            if item is None:
                item = crossref_lookup(title, mailto=args.mailto)
                if isinstance(item, dict):
                    cache[title] = item
                time.sleep(args.sleep)

            if isinstance(item, dict):
                p.doi = item.get("DOI")
                p.url = item.get("URL") or (f"https://doi.org/{p.doi}" if p.doi else None)
                p.year = _get_year(item)
                p.venue = _get_venue(item)
                p.authors = _get_authors(item)

        papers.append(p)

    if missing_title_ids:
        if not overrides_path.exists():
            overrides_path.parent.mkdir(parents=True, exist_ok=True)
            overrides_path.write_text(
                json.dumps({pid: "" for pid in sorted(set(missing_title_ids))}, indent=2),
                encoding="utf-8",
            )
            print(f"Created {overrides_path} — fill in missing titles and re-run for better DOI matching")
        else:
            missing = ", ".join(sorted(set(missing_title_ids)))
            print(f"Missing PDF title metadata for: {missing}. Add titles to {overrides_path} and re-run.")

    cache_path.write_text(json.dumps(cache, indent=2, sort_keys=True), encoding="utf-8")

    # Write structured artifacts
    out_json = Path("references/papers.json")
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps([asdict(p) for p in papers], indent=2), encoding="utf-8")

    out_bib = Path("references/references.bib")
    out_bib.write_text("\n".join([to_bibtex(p) for p in papers]), encoding="utf-8")

    out_docs = Path("docs/references.md")
    out_docs.parent.mkdir(parents=True, exist_ok=True)
    write_docs_markdown(papers, out_docs)

    print(f"Wrote {out_docs}")
    print(f"Wrote {out_bib}")
    print(f"Wrote {out_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
