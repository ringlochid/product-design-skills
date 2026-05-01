#!/usr/bin/env python3
from __future__ import annotations

import re
import struct
import sys
from pathlib import Path
from typing import Any

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
errors: list[str] = []
warnings: list[str] = []
missing_required: set[str] = set()

REQUIRED_FILES = [
    "00-run-manifest.md",
    "01-sources.md",
    "02-standards.md",
    "03-golden-workflow.md",
    "04-research-synthesis.md",
    "05-concept-brief.md",
    "06-market-wedge.md",
    "06-presentation-story.md",
    "07-journey-map.md",
    "08-screen-spec.md",
    "10-critique.md",
    "11-concept-report.md",
    "12-handoff.md",
    "13-artifact-check.txt",
    "15-promotion-verdict.md",
]

MANIFEST_FIELDS = [
    "request_summary",
    "product_slug",
    "timestamp",
    "workflow_kind",
    "requested_outputs",
    "ui_concept_requested",
    "run_status",
    "ui_concept_artifact_present",
    "ui_concept_verdict",
    "sources",
    "standards",
    "assumptions_gaps",
    "downstream_target",
]

STATUSES = {"pass", "fail", "degraded", "blocked"}
UI_VERDICTS = {"pass", "fail", "degraded", "blocked", "not_requested"}
BOOLS = {"true", "false"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
UI_EXTS = {".html", ".fig", ".pdf"}
BAD_LINK_STATUSES = {"404", "403", "429", "500", "502", "503", "dead", "blocked", "fail", "failed", "unverified"}


def read(rel: str, required: bool = True) -> str:
    p = ROOT / rel
    if not p.exists():
        if required:
            if rel not in missing_required:
                errors.append(f"missing required file: {rel}")
            missing_required.add(rel)
        return ""
    text = p.read_text(errors="ignore")
    if required and not text.strip():
        errors.append(f"empty required file: {rel}")
    return text


def field(text: str, name: str) -> str | None:
    m = re.search(rf"(?im)^\s*(?:[-*]\s*)?`?{re.escape(name)}`?\s*:\s*(.+?)\s*$", text)
    return m.group(1).strip().strip("`*") if m else None


def status_value(text: str | None) -> str:
    return (text or "").strip().lower()


def require_terms(rel: str, text: str, terms: list[str]) -> None:
    if rel in missing_required:
        return
    low = text.lower()
    for term in terms:
        if term.lower() not in low:
            errors.append(f"{rel} missing term: {term}")


def image_files(path: Path) -> list[Path]:
    return [p for p in path.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTS]


def ui_files(path: Path) -> list[Path]:
    return [p for p in path.rglob("*") if p.is_file() and p.suffix.lower() in UI_EXTS]


def image_size(path: Path) -> tuple[int, int] | None:
    try:
        data = path.read_bytes()[:65536]
        if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
            return struct.unpack(">II", data[16:24])
        if data.startswith(b"\xff\xd8"):
            i = 2
            while i + 9 < len(data):
                if data[i] != 0xFF:
                    i += 1
                    continue
                marker = data[i + 1]
                i += 2
                if marker in {0xD8, 0xD9}:
                    continue
                if i + 2 > len(data):
                    return None
                seg_len = int.from_bytes(data[i:i + 2], "big")
                sof = set(range(0xC0, 0xC4)) | set(range(0xC5, 0xC8)) | set(range(0xC9, 0xCC)) | set(range(0xCD, 0xD0))
                if marker in sof and i + 7 <= len(data):
                    h = int.from_bytes(data[i + 3:i + 5], "big")
                    w = int.from_bytes(data[i + 5:i + 7], "big")
                    return w, h
                i += seg_len
        if data.startswith(b"RIFF") and b"WEBP" in data[:16]:
            return (2048, 1024)  # accept WebP container presence; dimensions vary by chunk type
    except Exception:
        return None
    return None


def html_looks_rendered(path: Path) -> bool:
    text = path.read_text(errors="ignore")
    low = text.lower()
    if re.match(r"\s*#", text) or "## " in text[:500]:
        return False
    return all(tag in low for tag in ("<html", "<body")) and any(tag in low for tag in ("<main", "<section", "<button", "<nav", "<form"))


def html_visible_text(path: Path) -> str:
    text = path.read_text(errors="ignore")
    text = re.sub(r"(?is)<(script|style).*?</\1>", " ", text)
    text = re.sub(r"(?is)<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def parse_markdown_table(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    lines = [ln for ln in text.splitlines() if "|" in ln]
    header: list[str] | None = None
    for ln in lines:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        if all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells):
            continue
        norm = [re.sub(r"\s+", "_", c.lower()) for c in cells]
        if header is None:
            header = norm
            continue
        if header and len(cells) >= len(header):
            rows.append({header[i]: cells[i] for i in range(len(header))})
    return rows


def table_has_columns(rows: list[dict[str, str]], cols: list[str], rel: str) -> None:
    if not rows:
        errors.append(f"{rel} must contain a markdown table")
        return
    got = set(rows[0])
    for c in cols:
        if c not in got:
            errors.append(f"{rel} table missing column: {c}")


def has_generic_audience(value: str) -> bool:
    return bool(re.search(r"(?i)\b(everyone|all users|anyone|global|worldwide|general consumers|students everywhere)\b", value))


def has_bad_supporting_source(row: dict[str, str]) -> bool:
    supports = row.get("supports_promotion", "").lower()
    if supports not in {"yes", "true", "y"}:
        return False
    tier = row.get("quality_tier", "").strip().upper()
    status = row.get("verification_status", "").lower()
    return tier in {"D", "E"} or any(s in status for s in BAD_LINK_STATUSES)


for rel in REQUIRED_FILES:
    read(rel)

manifest = read("00-run-manifest.md")
for f in MANIFEST_FIELDS:
    if field(manifest, f) is None:
        errors.append(f"00-run-manifest.md missing field: {f}")

workflow_kind = status_value(field(manifest, "workflow_kind"))
run_status = status_value(field(manifest, "run_status"))
ui_requested = status_value(field(manifest, "ui_concept_requested"))
ui_present = status_value(field(manifest, "ui_concept_artifact_present"))
ui_verdict = status_value(field(manifest, "ui_concept_verdict"))

if workflow_kind and workflow_kind != "promotion_concept":
    errors.append("workflow_kind must be promotion_concept")
if run_status and run_status not in STATUSES:
    errors.append(f"invalid run_status: {run_status}")
if ui_requested and ui_requested not in BOOLS:
    errors.append(f"invalid ui_concept_requested: {ui_requested}")
if ui_present and ui_present not in BOOLS:
    errors.append(f"invalid ui_concept_artifact_present: {ui_present}")
if ui_verdict and ui_verdict not in UI_VERDICTS:
    errors.append(f"invalid ui_concept_verdict: {ui_verdict}")
if run_status == "pass" and ui_verdict != "pass":
    errors.append("run_status pass requires ui_concept_verdict: pass")
if ui_verdict == "pass" and ui_present != "true":
    errors.append("ui_concept_verdict pass requires ui_concept_artifact_present: true")

sources = read("01-sources.md")
source_rows = parse_markdown_table(sources)
table_has_columns(source_rows, ["url", "source_role", "quality_tier", "claim", "opponent/pain_signal", "decision_impact", "supports_promotion", "retrieval_date", "verification_status"], "01-sources.md")
if source_rows:
    tier_counts = {t: 0 for t in "ABCDE"}
    for row in source_rows:
        tier = row.get("quality_tier", "").strip().upper()[:1]
        if tier in tier_counts:
            tier_counts[tier] += 1
        if has_bad_supporting_source(row):
            errors.append(f"01-sources.md promotion-supporting source is unusable/blocked: {row.get('url','(missing url)')}")
    if tier_counts["A"] < 1:
        errors.append("01-sources.md requires at least one Tier A feasibility/constraint source")
    if tier_counts["B"] < 2:
        errors.append("01-sources.md requires at least two Tier B opponent/alternative sources")
    if tier_counts["C"] < 2:
        errors.append("01-sources.md requires at least two Tier C real-user pain-signal sources")

standards = read("02-standards.md")
require_terms("02-standards.md", standards, ["Double Diamond", "d.school", "NN/g", "WCAG 2.2", "privacy", "data feasibility"])

golden = read("03-golden-workflow.md")
require_terms("03-golden-workflow.md", golden, ["happy path", "edge", "failure", "```mermaid"])

synthesis = read("04-research-synthesis.md")
require_terms("04-research-synthesis.md", synthesis, ["fact", "source claim", "signal", "inference", "assumption", "gap"])

market = read("06-market-wedge.md")
market_fields = [
    "beachhead_segment", "launch_region", "use_moment", "excluded_users", "local_constraints",
    "opponent_map", "strongest_direct_opponent", "why_users_choose_opponent_today", "opponent_coverage_gap",
    "pain_evidence_status", "customer_pull_signal", "market_gate_verdict", "kill_or_pivot_condition",
    "novelty_delta_hypothesis", "delta_against_opponent", "not_the_novelty",
]
for f in market_fields:
    if field(market, f) is None and f not in market.lower():
        errors.append(f"06-market-wedge.md missing structured field: {f}")
beachhead = field(market, "beachhead_segment") or ""
excluded = field(market, "excluded_users") or ""
if has_generic_audience(beachhead):
    errors.append("06-market-wedge.md beachhead_segment is too generic")
if not excluded or has_generic_audience(excluded) is False and len(excluded.split()) < 2:
    errors.append("06-market-wedge.md must name excluded_users to prevent everyone-design")
if not re.search(r"(?is)opponent_map.*\bdirect\b", market):
    errors.append("06-market-wedge.md opponent_map must include a direct opponent row/entry")
if not re.search(r"(?is)opponent_map.*\b(workaround|indirect)\b", market):
    errors.append("06-market-wedge.md opponent_map must include a workaround or indirect alternative")
market_for_opponent_check = re.sub(r"(?i)\bnot\s+(?:claiming\s+)?no\s+(?:opponents|competitors|alternatives)\b", "", market)
if re.search(r"(?i)\bno\s+(opponents|competitors|alternatives)\b", market_for_opponent_check):
    errors.append("06-market-wedge.md claims no opponents/alternatives; real product pain requires existing alternatives")
if re.search(r"(?i)not\s+proof", market) is None and "tier c" in sources.lower():
    errors.append("06-market-wedge.md must label Tier C/community pain as signal, not proof")
market_gate = status_value(field(market, "market_gate_verdict"))
if market_gate in {"kill", "pivot", "degraded", "blocked"} and run_status == "pass":
    errors.append("run_status pass conflicts with market_gate_verdict not being promotion-ready")
novelty_status = status_value(field(market, "novelty_evidence_status"))

presentation = read("06-presentation-story.md")
require_terms("06-presentation-story.md", presentation, ["story_moment_id", "problem", "insight", "idea", "key moments", "proof", "slide"])

screen = read("08-screen-spec.md")
require_terms("08-screen-spec.md", screen, ["Stitch", "responsive", "accessibility", "privacy", "data", "state", "key screens"])
if "screen_id" not in screen.lower() and not re.search(r"`[A-Z]{2,}[-_][0-9A-Za-z-]+`", screen):
    errors.append("08-screen-spec.md missing stable screen_id values")
required_labels = re.findall(r"(?im)^\s*-\s*`([^`]+)`", screen)

concept_dir = ROOT / "09-concept-images"
if not concept_dir.exists():
    errors.append("missing required concept image folder: 09-concept-images")
else:
    manifest_text = (concept_dir / "manifest.md").read_text(errors="ignore") if (concept_dir / "manifest.md").exists() else ""
    critique_text = (concept_dir / "critique.md").read_text(errors="ignore") if (concept_dir / "critique.md").exists() else ""
    if (concept_dir / "SKIPPED.md").exists():
        errors.append("09-concept-images/SKIPPED.md is blocker evidence only; actual gpt-image-2 images are required")
    imgs = image_files(concept_dir)
    if len(imgs) < 3:
        errors.append("09-concept-images requires at least 3 actual image artifacts: hero, storyboard, key-screen")
    names = " ".join(p.name.lower() for p in imgs)
    for pat, label in [(r"hero|concept", "hero/concept"), (r"storyboard|story", "storyboard"), (r"key[-_ ]?screen|screen", "key-screen")]:
        if not re.search(pat, names):
            errors.append(f"09-concept-images missing actual {label} image artifact")
    for img in imgs:
        size = image_size(img)
        if not size:
            errors.append(f"concept image is not a valid readable image: {img.relative_to(ROOT)}")
            continue
        w, h = size
        if max(w, h) < 2048 or min(w, h) < 1024:
            errors.append(f"concept image too low-resolution: {img.relative_to(ROOT)} is {w}x{h}; require 2048px long edge and 1024px short edge")
    require_terms("09-concept-images/manifest.md", manifest_text, ["prompt", "provider", "model", "gpt-image-2", "output path", "actual image artifact", "dimensions", "story_moment_id", "screen_id", "source_truth_refs", "launch_region", "beachhead", "not_ui_proof: true"])
    require_terms("09-concept-images/critique.md", critique_text, ["concept clarity", "audience", "storyboard", "key screens", "readability", "misleading", "presentation quality", "region consistency", "geography drift", "verdict"])
    if not re.search(r"(?i)not\s+(?:a\s+)?ui\s+proof|not_ui_proof|concept\s+image\s+only", critique_text):
        errors.append("09-concept-images/critique.md must explicitly say concept images are not UI concept proof")

ui_dir = ROOT / "09-ui-concept"
ui_artifacts = ui_files(ui_dir) if ui_dir.exists() else []
ui_screenshots = image_files(ui_dir) if ui_dir.exists() else []
ui_claimed_success = ui_present == "true" or ui_verdict == "pass" or run_status == "pass"
if ui_requested == "true":
    if not (ui_dir / "README.md").exists():
        errors.append("ui concept requested but 09-ui-concept/README.md missing")
    if not (ui_dir / "stitch-attempt.md").exists():
        errors.append("ui concept requested but 09-ui-concept/stitch-attempt.md missing")
    else:
        attempt = (ui_dir / "stitch-attempt.md").read_text(errors="ignore")
        require_terms("09-ui-concept/stitch-attempt.md", attempt, ["stitch", "adapter", "command", "confirmation", "status", "artifact", "blocker"])
        if re.search(r"(?i)status\s*:\s*(blocked|fail|failed|degraded)", attempt) and ui_claimed_success:
            errors.append("blocked/degraded Stitch attempt cannot support UI concept pass")
else:
    if ui_verdict != "not_requested":
        errors.append("ui_concept_requested false requires ui_concept_verdict: not_requested")

if ui_claimed_success:
    if not ui_artifacts:
        errors.append("UI concept success claimed but no HTML/FIG/PDF artifact found in 09-ui-concept")
    htmls = [p for p in ui_artifacts if p.suffix.lower() == ".html"]
    if htmls and not any(html_looks_rendered(p) for p in htmls):
        errors.append("UI concept success claimed but HTML artifact appears to be markdown/spec text, not rendered UI")
    if not ui_screenshots:
        errors.append("UI concept success claimed but no rendered screenshot image found in 09-ui-concept")
    if required_labels and htmls:
        visible = "\n".join(html_visible_text(p) for p in htmls).lower()
        missing = [lbl for lbl in required_labels if lbl.lower() not in visible]
        if missing:
            errors.append(f"UI concept rendered HTML misses required visible labels: {', '.join(missing[:8])}")

critique = read("10-critique.md")
require_terms("10-critique.md", critique, ["standard", "status", "evidence", "severity", "action item", "next validation step", "visual", "WCAG", "idea quality", "presentation", "region specificity", "strongest direct opponent", "novelty delta", "customer pull", "UI concept"])
if ui_present != "true" and re.search(r"(?im)^\s*verdict\s*:\s*(accept|promotion)", critique):
    errors.append("10-critique.md cannot accept/promote without ui_concept_artifact_present true")

report = read("11-concept-report.md")
require_terms("11-concept-report.md", report, ["research basis", "market wedge", "design rationale", "standards compliance", "feasibility", "risks", "assumptions", "validation plan"])

handoff = read("12-handoff.md")
require_terms("12-handoff.md", handoff, ["artifact inventory", "source-truth", "decisions", "risks", "open questions", "missing evidence", "assumptions", "downstream lane", "promotion verdict"])

artifact_check = read("13-artifact-check.txt")
require_terms("13-artifact-check.txt", artifact_check, ["required files", "manifest fields", "market wedge", "beachhead", "strongest direct opponent", "novelty delta", "opponents", "pain signals", "concept images", "storyboard", "key screens", "UI concept", "stitch attempt", "presentation", "report", "sources", "standards", "verdict"])
if ui_claimed_success:
    require_terms("13-artifact-check.txt", artifact_check, ["ui_concept_core_flow_demonstrated", "ui_concept_quality_verdict"])

promotion = read("15-promotion-verdict.md")
require_terms("15-promotion-verdict.md", promotion, ["promotion_eligible", "promotion_scope", "source links", "concept images", "UI concept", "visual/a11y", "independent audit", "verdict"])
promotion_eligible = status_value(field(promotion, "promotion_eligible")) in {"true", "yes", "pass"}
if promotion_eligible:
    if novelty_status == "assumption":
        errors.append("promotion_eligible true conflicts with novelty_evidence_status: assumption")
    if not (ROOT / "14-source-link-check.txt").exists():
        errors.append("promotion_eligible true requires 14-source-link-check.txt")
    elif "VERDICT=PASS" not in (ROOT / "14-source-link-check.txt").read_text(errors="ignore"):
        errors.append("promotion_eligible true requires 14-source-link-check.txt with VERDICT=PASS")
    if ui_present != "true" or ui_verdict != "pass":
        errors.append("promotion_eligible true requires UI concept artifact present and verdict pass")
    if len(ui_screenshots) < 1:
        errors.append("promotion_eligible true requires at least one UI concept screenshot")
    if run_status != "pass":
        errors.append("promotion_eligible true requires run_status: pass")

if errors:
    print("FAIL")
    for e in errors:
        print(f"- {e}")
    if warnings:
        print("WARN")
        for w in warnings:
            print(f"- {w}")
    sys.exit(1)

print("PASS")
print(f"run_status={run_status or 'unknown'}")
print(f"ui_concept_artifact_present={ui_present or 'unknown'}")
print(f"ui_concept_verdict={ui_verdict or 'unknown'}")
print(f"promotion_eligible={str(promotion_eligible).lower()}")
if warnings:
    print("WARN")
    for w in warnings:
        print(f"- {w}")
