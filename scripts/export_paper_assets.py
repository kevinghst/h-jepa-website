"""Refresh website assets from a compiled release paper without modifying its repo."""
import argparse
import shutil
from pathlib import Path

import fitz

FIGURES = {
    "overview": "planning_illustrations/teaser",
    "abstractions": "abstraction/depth_probes",
    "planning-results-pareto": "planning/depth_planning_pareto",
    "goal-costs": "heatmaps/composite_levels",
    "subgoal-tracking": "tmono/instance",
    "scene-diversity": "droid/scene_diversity_cube_droid",
    "droid-ablation": "droid/cls_ladder",
    "droid-compute": "compute/pareto_real_cls_droid",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paper_dir", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    figures = root / "assets/figures"
    paper = root / "assets/paper"
    figures.mkdir(parents=True, exist_ok=True)
    paper.mkdir(parents=True, exist_ok=True)
    with fitz.open(args.paper_dir / "main_release.pdf") as pdf:
        # These bounds match the release PDF dated October 2, 2026.
        diagrams = [("training", 2, 239), ("planning", 3, 254)]
        for name, page_number, bottom in diagrams:
            page = pdf[page_number]
            expected = "Figure 2:" if name == "training" else "Figure 3:"
            captions = page.search_for(expected)
            if not captions or abs(captions[0].y0 - (bottom + 9)) > 3:
                raise ValueError(f"Paper layout changed: check the {name} crop before exporting.")
        for name, page_number, bottom in diagrams:
            pdf[page_number].get_pixmap(
                matrix=fitz.Matrix(5, 5), clip=fitz.Rect(107, 80.5, 505, bottom), alpha=False
            ).save(figures / f"{name}.png")
    for name, source in FIGURES.items():
        shutil.copy2(args.paper_dir / "figures" / f"{source}.png", figures / f"{name}.png")
    shutil.copy2(args.paper_dir / "main_release.pdf", paper / "h-jepa.pdf")
    print("Exported 10 figures and the release PDF. Review the method crops before publishing.")


if __name__ == "__main__":
    main()
