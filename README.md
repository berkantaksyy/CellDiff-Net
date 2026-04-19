# ML-Based Identification of Stem Cell Differentiation States from Microscopy Images

Project hub for a literature review and (future) implementation around **microscopy + deep learning** for identifying stem cell differentiation states.

## Quick links
- Website: https://berkantaksyy.github.io/CellDiff-Net/
- Slides: `slides/StemCell_DL_LiteratureReview.pptx`
- References page: `docs/references.md` (published on the website)
- BibTeX: `references/references.bib`

## Problem & goal
Given microscopy images (ideally longitudinal time series), the goal is to **predict/quantify stem cell differentiation state** (early vs late, or a continuous score) in a way that is reproducible and biologically meaningful.

This repository currently focuses on the **literature review + reference management + slides + project website**. Model training/inference code will be added as the project matures.

## Proposed approach (high level)
1. **Data**: curate microscopy images with labels (time since induction, marker-based ground truth, expert labels, etc.).
2. **Preprocessing**: illumination correction, normalization, train/val/test split with leakage controls (plate/batch/time).
3. **Segmentation (optional)**: use a generalist model (e.g., Cellpose / SAM variants) to extract cell-level crops or masks.
4. **Representation learning**: self-supervised or supervised feature extraction (CNN/ViT) on full frames or cell crops.
5. **Prediction**: classification (state bins) and/or regression (differentiation score), with calibration + uncertainty.
6. **Evaluation**: per-batch generalization, time-to-detection, ablations; link predictions to biology.

## Usage (current)
### Update references (no PDFs published)
Paper PDFs are kept locally under `private/papers/` and are **ignored by git**.

Generate/update the public references list:
```bash
# optional (recommended): identify yourself to Crossref politely
export CROSSREF_MAILTO="berkantaksyy@gmail.com"

python3 tools/update_references.py --refresh
```
If a PDF has missing metadata, fill its title in:
- `references/title_overrides.json`

Then re-run the updater.

## Roadmap
- **Scope definition**: define target labels (discrete states vs continuous), microscopy modality, and evaluation protocol.
- **Dataset plan**: decide on data source (public datasets vs in-house), storage strategy, and annotation format.
- **Baselines**: simple CNN baseline on whole frames; report metrics + calibration.
- **Segmentation-assisted pipeline**: compare whole-frame vs cell-crop vs mask-based representations.
- **Explainability**: saliency/attribution, feature clustering over time, and biological validation checks.
- **Reproducibility**: fixed splits, seeded runs, experiment tracking, and a minimal training CLI.

## How to cite
If you reuse this repo’s reference list or structure, cite the original papers (see the References page) and link back to this repository.

## Website (GitHub Pages)
Live site: https://berkantaksyy.github.io/CellDiff-Net/

This repo publishes a simple project website from the **`/docs`** folder.

GitHub setup:
1. Go to **Settings → Pages**
2. **Source**: “Deploy from a branch”
3. **Branch**: `main`  /  **Folder**: `/docs`

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