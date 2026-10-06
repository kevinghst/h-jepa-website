# H-JEPA project website

A static paper website for [h-jepa.com](https://h-jepa.com), inspired by the article layout of [Lifting Embodied World Models](https://www.alexn.wang/lwm/). No build step or JavaScript dependencies are required.

## Preview

```sh
python3 -m http.server 8000
```

Open `http://localhost:8000`. The existing `CNAME` and `.nojekyll` support serving the repository root with GitHub Pages.

## Content and assets

- `index.html`: paper content, authors, resource links, figure captions, and BibTeX.
- `styles.css`: layout, typography, desktop contents sidebar, and responsive styling.
- `script.js`: reading progress, active section tracking, and citation copying. The article remains readable without JavaScript.
- `assets/figures/`: paper figures exported from the release source.
- Paper links point directly to https://arxiv.org/pdf/2610.06805; no PDF is hosted in this repository.

Content follows `/Users/kevin/Desktop/hjepa_paper/main_release.tex` as of October 2, 2026. Figures 2 and 3 are cropped from the matching `main_release.pdf`; the other figures come from the corresponding files in the paper's `figures/` directory. Website figure numbering follows the order on this page.

The paper's repository link is used as supplied in the source. The BibTeX section is temporarily hidden, along with its navigation and resource links. Google Fonts supplies Crimson Pro and Inter, with system-font fallbacks.

To refresh the paper assets after compiling `main_release.tex`, run:

```sh
python3 scripts/export_paper_assets.py /Users/kevin/Desktop/hjepa_paper
```

The export utility needs PyMuPDF; the website does not. Check the cropped method diagrams after any paper layout changes. Website prose is edited separately so it remains a readable summary of the paper.
