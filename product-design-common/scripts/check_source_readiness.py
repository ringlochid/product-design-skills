#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
errors: list[str] = []

SOURCES = ROOT / "01-sources.md"
MARKET = ROOT / "06-market-wedge.md"
SKELETON_WORDS = {"tbd", "pending", "skeleton"}


def read(path: Path) -> str:
    if not path.exists():
        errors.append(f"missing {path.name}")
        return ""
    return path.read_text(errors="ignore")


def rows(text: str) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    header: list[str] | None = None
    for line in text.splitlines():
        if "|" not in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        if all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells):
            continue
        if header is None:
            header = [re.sub(r"\s+", "_", c.lower()) for c in cells]
            continue
        if len(cells) >= len(header):
            out.append({header[i]: cells[i] for i in range(len(header))})
    return out


def has_placeholder(value: str) -> bool:
    low = value.lower()
    return any(word in low for word in SKELETON_WORDS)


source_text = read(SOURCES)
market_text = read(MARKET)
source_rows = rows(source_text)
real_url_rows = [r for r in source_rows if re.match(r"https?://", r.get("url", ""))]

if len(real_url_rows) < 5:
    errors.append(f"01-sources.md requires at least 5 real http(s) source rows before images/UI; found {len(real_url_rows)}")

counts = {"A": 0, "B": 0, "C": 0}
for row in real_url_rows:
    tier = row.get("quality_tier", "").strip().upper()[:1]
    if tier in counts:
        counts[tier] += 1
    if has_placeholder(" ".join(row.values())):
        errors.append(f"01-sources.md row still contains placeholder text: {row.get('url', '(missing url)')}")
    status = row.get("verification_status", "").lower()
    supports = row.get("supports_promotion", "").lower() in {"yes", "true", "y"}
    if supports and any(bad in status for bad in ("unverified", "tbd", "pending", "blocked", "dead", "404", "403", "500", "fail")):
        errors.append(f"promotion-supporting source is not verified: {row.get('url', '(missing url)')}")

if counts["A"] < 1:
    errors.append("requires at least one real Tier A feasibility/constraint source before images/UI")
if counts["B"] < 2:
    errors.append("requires at least two real Tier B opponent/workaround sources before images/UI")
if counts["C"] < 2:
    errors.append("requires at least two real Tier C pain-signal sources before images/UI")

required_market_fields = [
    "beachhead_segment", "launch_region", "use_moment", "excluded_users", "local_constraints",
    "opponent_map", "strongest_direct_opponent", "why_users_choose_opponent_today", "opponent_coverage_gap",
    "pain_evidence_status", "customer_pull_signal", "market_gate_verdict", "kill_or_pivot_condition",
    "novelty_delta_hypothesis", "delta_against_opponent", "not_the_novelty",
]
for field in required_market_fields:
    match = re.search(rf"(?im)^\s*`?{re.escape(field)}`?\s*:\s*(.+?)\s*$", market_text)
    if not match:
        errors.append(f"06-market-wedge.md missing field before images/UI: {field}")
        continue
    if has_placeholder(match.group(1)):
        errors.append(f"06-market-wedge.md field still placeholder before images/UI: {field}")

if re.search(r"(?i)skeleton only|pending source|pending opponent|pending;|launch region pending", market_text):
    errors.append("06-market-wedge.md still contains skeleton/pending language before images/UI")
if not re.search(r"(?is)opponent_map.*\bdirect\b", market_text):
    errors.append("06-market-wedge.md opponent_map must include direct opponent before images/UI")
if not re.search(r"(?is)opponent_map.*\b(workaround|indirect)\b", market_text):
    errors.append("06-market-wedge.md opponent_map must include workaround/indirect alternative before images/UI")

supporting_docs = {
    "02-standards.md": ["Double Diamond", "d.school", "NN/g", "WCAG 2.2", "privacy", "data feasibility"],
    "06-presentation-story.md": ["story_moment_id", "problem", "insight", "idea", "key moments", "proof", "slide"],
    "08-screen-spec.md": ["Stitch", "responsive", "accessibility", "privacy", "data", "state", "key screens"],
}
for rel, terms in supporting_docs.items():
    text = read(ROOT / rel)
    low = text.lower()
    for term in terms:
        if term.lower() not in low:
            errors.append(f"{rel} missing pre-visual term: {term}")

if errors:
    print("FAIL")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("PASS")
print(f"real_source_rows={len(real_url_rows)} tier_a={counts['A']} tier_b={counts['B']} tier_c={counts['C']}")
