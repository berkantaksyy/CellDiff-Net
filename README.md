# 🔬 CellDiff-Net

**ML-Based Identification of Stem Cell Differentiation States from Microscopy Images**

[![Website](https://img.shields.io/badge/🌐%20Website-Live-brightgreen)](https://berkantaksyy.github.io/CellDiff-Net/)
[![Slides](https://img.shields.io/badge/📊%20Slides-View%20Online-blue)](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fraw.githubusercontent.com%2Fberkantaksyy%2FCellDiff-Net%2Fmain%2Fslides%2FStemCell_DL_LiteratureReview.pptx)
[![Paper](https://img.shields.io/badge/📄%20Paper-Coming%20Soon-lightgrey)]()
[![Status](https://img.shields.io/badge/Status-Literature%20Review-orange)]()

> A project at the intersection of **deep learning** and **cell biology** — using microscopy images to automatically identify and quantify stem cell differentiation states, enabling reproducible, label-free biological analysis.

---

## 📂 Resources

| | Resource | Description | Link |
|---|---|---|---|
| 🌐 | **Website** | Project overview, slides & references | [berkantaksyy.github.io/CellDiff-Net](https://berkantaksyy.github.io/CellDiff-Net/) |
| 📊 | **Slides** | Literature review presentation | [▶ View online](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fraw.githubusercontent.com%2Fberkantaksyy%2FCellDiff-Net%2Fmain%2Fslides%2FStemCell_DL_LiteratureReview.pptx) · [⬇ Download PPTX](https://raw.githubusercontent.com/berkantaksyy/CellDiff-Net/main/slides/StemCell_DL_LiteratureReview.pptx) |
| 📄 | **Paper** | Research article | 🚧 Coming soon |
| 📚 | **References** | Curated literature with DOIs | [View References](https://berkantaksyy.github.io/CellDiff-Net/references) |
| 📖 | **BibTeX** | Citation file | [references.bib](references/references.bib) |

---

## 🧬 Problem & Motivation

Stem cell differentiation is a complex, multi-stage biological process. Traditional methods rely on molecular markers or expert visual inspection — both slow and subjective. This project asks:

> **Can a deep learning model learn to identify differentiation states directly from microscopy images, without requiring expensive labels?**

---

## 🗺️ Proposed Pipeline

```
Raw Microscopy Images
        │
        ▼
 Preprocessing & QC          ← illumination correction, normalization
        │
        ▼
  Segmentation (optional)    ← Cellpose / SAM-based cell extraction
        │
        ▼
 Representation Learning      ← CNN / ViT (self-supervised or supervised)
        │
        ▼
  State Prediction            ← classification (early/late) or regression (score)
        │
        ▼
  Evaluation & Explainability ← calibration, saliency, biological validation
```

---

## 📋 Roadmap

- [x] Literature review & reference management
- [x] Slide deck (literature review)
- [x] Project website (GitHub Pages)
- [ ] Dataset curation plan
- [ ] CNN baseline on whole frames
- [ ] Segmentation-assisted pipeline
- [ ] Self-supervised representation learning
- [ ] Explainability & biological validation
- [ ] Research paper / preprint

---

## 🗂️ Repository Structure

```
CellDiff-Net/
├── docs/              # GitHub Pages site (auto-deployed)
│   ├── index.html     # Landing page
│   └── references.md  # Auto-generated references
├── slides/            # Presentation slides
│   └── StemCell_DL_LiteratureReview.pptx
├── references/        # Generated reference artifacts
│   ├── references.bib
│   └── papers.json
├── tools/             # Helper scripts
│   └── update_references.py
└── private/           # Local-only (git-ignored)
    └── papers/        # Personal PDF copies
```

---

## 🔧 Usage

### Update the reference list

Paper PDFs are kept locally under `private/papers/` (git-ignored). To regenerate the public reference list from your local PDFs:

```bash
# Recommended: identify yourself to Crossref
export CROSSREF_MAILTO="berkantaksyy@gmail.com"

python3 tools/update_references.py --refresh
```

If a PDF has missing metadata, add its title to `references/title_overrides.json` and re-run.

---

## 🌐 GitHub Pages Setup

The site is published from the `/docs` folder on `main`:

1. Go to **Settings → Pages**
2. **Source**: Deploy from a branch
3. **Branch**: `main` / **Folder**: `/docs`
4. Site will be live at `https://berkantaksyy.github.io/CellDiff-Net/`

---

## 📝 How to Cite

Once the paper is published, a BibTeX entry will be added here. In the meantime, you can link to this repository and cite the original papers on the [References page](https://berkantaksyy.github.io/CellDiff-Net/references).

---

## ⚖️ Ethics & Copyright

Paper PDFs are **not committed** to this repository to respect publisher copyright. The repository stores citations, DOIs, and links only. Personal PDF copies should be kept locally under `private/papers/` (git-ignored).

---

## 📜 License

TBD — will be added before any model code or data is published.
