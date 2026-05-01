#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_READY = ROOT / "product-design-common" / "scripts" / "check_source_readiness.py"
FINAL_CHECK = ROOT / "product-design-common" / "scripts" / "check_product_design_run.py"
REQUIRED = [
    "00-run-manifest.md", "01-sources.md", "02-standards.md", "03-golden-workflow.md",
    "04-research-synthesis.md", "05-concept-brief.md", "06-market-wedge.md",
    "06-presentation-story.md", "07-journey-map.md", "08-screen-spec.md",
    "09-concept-images/manifest.md", "09-concept-images/critique.md",
    "09-ui-concept/README.md", "09-ui-concept/stitch-attempt.md", "10-critique.md",
    "11-concept-report.md", "12-handoff.md", "15-promotion-verdict.md",
]


def read(path: Path) -> str:
    return path.read_text(errors="ignore") if path.exists() else ""


def run(cmd: list[str], folder: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd + [str(folder)], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def image_roles(folder: Path) -> set[str]:
    roles: set[str] = set()
    for p in (folder / "09-concept-images").glob("*"):
        if p.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            continue
        name = p.name.lower()
        if "hero" in name or "concept" in name:
            roles.add("hero")
        if "storyboard" in name:
            roles.add("storyboard")
        if "key" in name or "screen" in name:
            roles.add("key-screen")
    return roles


def ui_present(folder: Path) -> bool:
    ui = folder / "09-ui-concept"
    has_html = any(p.suffix.lower() == ".html" for p in ui.glob("*"))
    has_shot = any(p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"} for p in ui.glob("*"))
    manifest = read(folder / "00-run-manifest.md").lower()
    declared = re.search(r"(?m)^\s*ui_concept_artifact_present\s*:\s*true\s*$", manifest) is not None
    return declared and has_html and has_shot


def emit(phase: str, status: str, next_leaf: str, reason: str) -> int:
    print(f"PHASE={phase}")
    print(f"STATUS={status}")
    print(f"NEXT_LEAF={next_leaf}")
    print(f"REASON={reason}")
    return 0 if status in {"ready", "complete", "degraded"} else 1


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_phase_status.py <product-design-run-folder>")
        return 2
    folder = Path(sys.argv[1]).resolve()
    if not folder.exists():
        return emit("bootstrap", "blocked", "product-design-workflow", "run folder does not exist")

    missing = [rel for rel in REQUIRED if not (folder / rel).exists()]
    if missing:
        return emit("bootstrap", "blocked", "product-design-workflow", "missing skeleton files: " + ", ".join(missing[:6]))

    source = run([sys.executable, str(SOURCE_READY)], folder)
    if source.returncode != 0:
        first = next((line[2:] for line in source.stdout.splitlines() if line.startswith("- ")), "source/previsual gate failed")
        return emit("evidence", "blocked", "market-context-reader|opportunity-framing|concept-page-spec-writer", first)

    roles = image_roles(folder)
    if roles != {"hero", "storyboard", "key-screen"}:
        missing_roles = sorted({"hero", "storyboard", "key-screen"} - roles)
        return emit("visuals", "ready", "rich-concept-image-generation", "missing image roles: " + ", ".join(missing_roles))

    if not ui_present(folder):
        return emit("ui_concept", "ready", "stitch-concept-generator", "UI concept HTML+screenshot not present/declared")

    final = run([sys.executable, str(FINAL_CHECK)], folder)
    if final.returncode == 0:
        return emit("complete", "complete", "none", "final checker passed")
    first = next((line[2:] for line in final.stdout.splitlines() if line.startswith("- ")), "final checker failed")
    return emit("final_audit", "blocked", "concept-review-gate|product-design-handoff", first)


if __name__ == "__main__":
    raise SystemExit(main())
