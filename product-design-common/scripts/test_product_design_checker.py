#!/usr/bin/env python3
from __future__ import annotations

import shutil
import struct
import subprocess
import sys
import tempfile
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "product-design-common" / "scripts" / "check_product_design_run.py"
SKELETON = ROOT / "product-design-common" / "scripts" / "create_product_design_skeleton.py"
SOURCE_READY = ROOT / "product-design-common" / "scripts" / "check_source_readiness.py"


def png(path: Path, w: int = 2048, h: int = 1152) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = b"".join(b"\x00" + b"\xff\xff\xff" * w for _ in range(h))
    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)
    data = b"\x89PNG\r\n\x1a\n"
    data += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    data += chunk(b"IDAT", zlib.compress(raw, 1))
    data += chunk(b"IEND", b"")
    path.write_bytes(data)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n")


def base_fixture(path: Path, *, run_status: str, ui_present: bool, ui_verdict: str, promotion: bool) -> None:
    write(path / "00-run-manifest.md", f"""
request_summary: Promotion concept package for a bounded beachhead.
product_slug: fixture
timestamp: 20260501T000000Z
workflow_kind: promotion_concept
requested_outputs: research, market wedge, rich images, UI concept, review, promotion verdict
ui_concept_requested: true
run_status: {run_status}
ui_concept_artifact_present: {str(ui_present).lower()}
ui_concept_verdict: {ui_verdict}
sources: default evidence pack
standards: Double Diamond, d.school, NN/g, WCAG 2.2, privacy/data feasibility
assumptions_gaps: missing-user-research remains
 downstream_target: design-skills
""")
    write(path / "01-sources.md", """
| url | source_role | quality_tier | claim | opponent/pain signal | decision impact | supports_promotion | retrieval_date | verification_status |
|---|---|---|---|---|---|---|---|---|
| https://example.com/api | feasibility | A | official API/constraint exists | constraint | scope data feasibility | yes | 2026-05-01 | ok |
| https://example.com/direct | opponent | B | direct opponent has broad workflow | strongest direct opponent | compare gap | yes | 2026-05-01 | ok |
| https://example.com/workaround | workaround | B | users use spreadsheet/chat workaround | workaround | compare manual alternative | yes | 2026-05-01 | ok |
| https://example.com/pain-1 | pain | C | public complaint about exact moment | pain signal not proof | supports validation need | yes | 2026-05-01 | ok |
| https://example.com/pain-2 | pain | C | review mentions repeated friction | pain signal not proof | supports validation need | yes | 2026-05-01 | ok |
""")
    write(path / "02-standards.md", "Double Diamond and d.school frame discover/define before ideation. NN/g and WCAG 2.2 guide clarity and accessibility. Privacy and data feasibility constrain decisions.")
    write(path / "03-golden-workflow.md", """
happy path: A to B. edge state: empty data. failure state: blocked source.
```mermaid
graph TD; A-->B
```
""")
    write(path / "04-research-synthesis.md", "fact source claim signal inference assumption gap")
    write(path / "05-concept-brief.md", "concept brief with user problem job value proposition constraints non-goals success criteria evidence assumptions risks")
    write(path / "06-market-wedge.md", """
beachhead_segment: Inner Sydney independent cafe managers with 8-35 staff
launch_region: Glebe / Newtown / Surry Hills, Sydney
use_moment: reviewing a weekly roster before publishing it
excluded_users: enterprise workforce teams, generic productivity users, all restaurants
local_constraints: Australian hospitality award patterns and small-team skill coverage
opponent_map: direct: Deputy; workaround: spreadsheets and WhatsApp shift chats
strongest_direct_opponent: Deputy
why_users_choose_opponent_today: it already covers rostering, breaks, mobile workforce workflows, and payroll adjacency
opponent_coverage_gap: it does not give one narrow pre-publish risk narrative for understaffing, fatigue, and fragile swaps
pain_evidence_status: signal
novelty_evidence_status: signal
customer_pull_signal: weak but repeated Tier C pain signals, not proof
market_gate_verdict: continue_with_validation
kill_or_pivot_condition: kill if five target managers do not report this exact pre-publish review pain
novelty_delta_hypothesis: a publish-risk cockpit for one cafe roster decision moment
delta_against_opponent: narrower than Deputy; ranks fixable risks before publishing rather than replacing workforce management
not_the_novelty: not AI, not better UI, not a prettier dashboard
Tier C/community pain signals are signal, not proof.
""")
    write(path / "06-presentation-story.md", """
story_moment_id: M1 problem: roster risk is invisible before publish.
story_moment_id: M2 insight: managers need one ranked fix list.
story_moment_id: M3 idea: UI concept shows key moments and proof.
slide outline with problem insight idea key moments proof and next validation.
""")
    write(path / "07-journey-map.md", "journey map with persona/scenario/goal states edge failure privacy trust risks evidence assumptions")
    write(path / "08-screen-spec.md", """
Stitch responsive accessibility privacy data state key screens.
screen_id: home-risk-review
screen_id: source-trace
Required visible labels:
- `Local Answer`
- `Source Trace`
""")
    c = path / "09-concept-images"
    png(c / "hero-concept.png")
    png(c / "storyboard.png")
    png(c / "key-screen-01-home-risk-review.png")
    write(c / "manifest.md", """
role: hero concept, storyboard, key screens
story_moment_id: M1, M2, M3
screen_id: home-risk-review, source-trace
source_truth_refs: 01-sources.md, 06-market-wedge.md, 08-screen-spec.md
prompt: rich presentation visual for launch_region and beachhead
provider: openai
model: gpt-image-2
output path: 09-concept-images
actual image artifact: hero-concept.png storyboard.png key-screen-01-home-risk-review.png
dimensions: 2048x1152
launch_region: Glebe / Newtown / Surry Hills
beachhead: inner Sydney independent cafe managers
not_ui_proof: true
""")
    write(c / "critique.md", "concept clarity audience storyboard key screens readability misleading presentation quality region consistency geography drift verdict pass; concept image only, not UI proof")
    write(path / "10-critique.md", """
| standard | status | evidence | severity | action item | next validation step |
|---|---|---|---|---|---|
| visual WCAG idea quality presentation region specificity strongest direct opponent novelty delta customer pull UI concept | pass | evidence | low | test | interview |
""")
    write(path / "11-concept-report.md", "research basis market wedge design rationale standards compliance feasibility risks assumptions validation plan")
    write(path / "12-handoff.md", "artifact inventory source-truth decisions risks open questions missing evidence assumptions downstream lane promotion verdict")
    extra = "ui_concept_core_flow_demonstrated ui_concept_quality_verdict" if ui_present or ui_verdict == "pass" else ""
    write(path / "13-artifact-check.txt", f"required files manifest fields market wedge beachhead strongest direct opponent novelty delta opponents pain signals concept images storyboard key screens UI concept stitch attempt presentation report sources standards verdict {extra}")
    write(path / "15-promotion-verdict.md", f"""
promotion_eligible: {str(promotion).lower()}
promotion_scope: promotion_concept
source links: {'pass' if promotion else 'not promotion-ready'}
concept images: pass
UI concept: {ui_verdict}
visual/a11y: checked
independent audit: checked
verdict: {'pass' if promotion else 'not eligible'}
""")
    if promotion:
        write(path / "14-source-link-check.txt", "VERDICT=PASS")


def add_ui(path: Path, *, rendered: bool = True, blocked: bool = False) -> None:
    p = path / "09-ui-concept"
    status = "blocked" if blocked else "pass"
    write(p / "README.md", "Stitch screenshot artifact path local viewport full-page UI concept")
    write(p / "stitch-attempt.md", f"stitch adapter command confirmation status: {status} artifact path blocker recorded")
    if not blocked:
        if rendered:
            write(p / "mobile.html", """
<html><body><main><header>Local Answer</header><nav>Source Trace</nav><section><button>Act</button><a href='#'>Source Trace</a></section></main></body></html>
""")
        else:
            write(p / "mobile.html", "# Markdown spec, not rendered UI")
        png(p / "local-viewport.png", 390, 844)


def run_case(name: str, expect_ok: bool, setup) -> None:
    tmp = Path(tempfile.mkdtemp(prefix=f"pd-checker-{name}-"))
    try:
        setup(tmp)
        result = subprocess.run([sys.executable, str(CHECKER), str(tmp)], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        ok = result.returncode == 0
        if ok != expect_ok:
            print(f"FAIL {name}: expected ok={expect_ok}, got exit={result.returncode}")
            print(result.stdout)
            raise SystemExit(1)
        print(f"PASS {name}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> None:
    def skeleton_bootstrap(d: Path) -> None:
        result = subprocess.run([sys.executable, str(SKELETON), str(d), "--slug", "Fixture", "--request", "Fixture request"], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if result.returncode != 0:
            print(result.stdout)
            raise SystemExit(result.returncode)
        required = ["00-run-manifest.md", "01-sources.md", "10-critique.md", "11-concept-report.md", "12-handoff.md", "15-promotion-verdict.md", "09-concept-images/manifest.md", "09-ui-concept/stitch-attempt.md"]
        missing = [rel for rel in required if not (d / rel).exists()]
        if missing:
            print(f"FAIL skeleton_bootstrap: missing {missing}")
            raise SystemExit(1)
        checker = subprocess.run([sys.executable, str(CHECKER), str(d)], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if "missing required file" in checker.stdout:
            print(checker.stdout)
            raise SystemExit(1)
        print("PASS skeleton_bootstrap_creates_contract_shape")
    tmp = Path(tempfile.mkdtemp(prefix="pd-checker-skeleton-bootstrap-"))
    try:
        skeleton_bootstrap(tmp)
        readiness = subprocess.run([sys.executable, str(SOURCE_READY), str(tmp)], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if readiness.returncode == 0 or "requires at least 5 real http(s) source rows" not in readiness.stdout:
            print("FAIL source_readiness_blocks_skeleton")
            print(readiness.stdout)
            raise SystemExit(1)
        print("PASS source_readiness_blocks_skeleton")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    def promotion_pass(d: Path) -> None:
        base_fixture(d, run_status="pass", ui_present=True, ui_verdict="pass", promotion=True)
        add_ui(d)
    run_case("promotion_pass_minimal", True, promotion_pass)

    def missing_images(d: Path) -> None:
        base_fixture(d, run_status="pass", ui_present=True, ui_verdict="pass", promotion=True)
        shutil.rmtree(d / "09-concept-images")
        add_ui(d)
    run_case("missing_rich_images_blocks_promotion", False, missing_images)

    def fake_ui(d: Path) -> None:
        base_fixture(d, run_status="pass", ui_present=True, ui_verdict="pass", promotion=True)
        add_ui(d, rendered=False)
    run_case("ui_concept_not_rendered_blocks_promotion", False, fake_ui)

    def source_fail(d: Path) -> None:
        base_fixture(d, run_status="pass", ui_present=True, ui_verdict="pass", promotion=True)
        add_ui(d)
        write(d / "14-source-link-check.txt", "VERDICT=FAIL")
    run_case("source_link_fail_blocks_promotion", False, source_fail)

    def missing_artifact_check_is_generated(d: Path) -> None:
        base_fixture(d, run_status="pass", ui_present=True, ui_verdict="pass", promotion=True)
        (d / "13-artifact-check.txt").unlink()
        add_ui(d)
    run_case("missing_artifact_check_is_generated", True, missing_artifact_check_is_generated)

    def suspicious_large_tiny_ui_screenshot(d: Path) -> None:
        base_fixture(d, run_status="pass", ui_present=True, ui_verdict="pass", promotion=True)
        add_ui(d)
        (d / "09-ui-concept" / "local-viewport.png").unlink()
        png(d / "09-ui-concept" / "local-viewport.png", 1440, 2000)
    run_case("suspicious_large_tiny_ui_screenshot_blocks_promotion", False, suspicious_large_tiny_ui_screenshot)

    def honest_not_ready(d: Path) -> None:
        base_fixture(d, run_status="blocked", ui_present=False, ui_verdict="blocked", promotion=False)
        add_ui(d, blocked=True)
    run_case("honest_not_promotion_eligible_passes_contract", True, honest_not_ready)


if __name__ == "__main__":
    main()
