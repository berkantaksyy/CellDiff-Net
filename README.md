# ML-Based Identification of Stem Cell Differentiation States from Microscopy Images

Project hub for a literature review and (future) implementation around **microscopy + deep learning** for identifying stem cell differentiation states.

## Website (GitHub Pages)
This repo is set up to publish a simple project website from the **`/docs`** folder.

After you push to GitHub:
1. Go to **Settings → Pages**
2. **Source**: “Deploy from a branch”
3. **Branch**: `main`  /  **Folder**: `/docs`
4. Save — your site will be available at `https://<username>.github.io/<repo>/`

## Slides
- `slides/StemCell_DL_LiteratureReview.pptx`

Tip: If you export a PDF version of the slides, you can put it in `docs/assets/` and link it from the website.

## References (automatic, without publishing PDFs)
This repo intentionally **does not commit academic paper PDFs**. Keep your personal copies under:
- `private/papers/` (git-ignored)

Then generate/update the public references list:
```bash
python3 tools/update_references.py
```
Outputs:
- `docs/references.md` (used by the website)
- `references/references.bib`
- `references/papers.json`

## Repository structure
- `docs/` — GitHub Pages site
- `slides/` — presentation slides
- `tools/` — helper scripts (e.g., reference generation)
- `references/` — generated reference artifacts (BibTeX/JSON)
- `private/` — local-only files (ignored)

## Ethics / copyright note
Sharing publisher PDFs publicly is often not allowed. The safe approach is: **publish citations + DOI links**, not the PDFs.

## License
TBD (pick one before publishing code/data).