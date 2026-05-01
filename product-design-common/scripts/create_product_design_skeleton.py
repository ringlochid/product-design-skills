#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from datetime import datetime, timezone
from pathlib import Path


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "product-concept"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(errors="ignore").strip():
        return
    path.write_text(text.strip() + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a timeout-safe product-design promotion concept skeleton.")
    parser.add_argument("folder", help="Target run folder")
    parser.add_argument("--slug", default="product-concept")
    parser.add_argument("--request", default="Promotion-style product design concept package")
    parser.add_argument("--timestamp", default="")
    args = parser.parse_args()

    root = Path(args.folder).resolve()
    slug = slugify(args.slug)
    timestamp = args.timestamp or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    root.mkdir(parents=True, exist_ok=True)
    (root / "09-concept-images").mkdir(parents=True, exist_ok=True)
    (root / "09-ui-concept").mkdir(parents=True, exist_ok=True)

    write(root / "00-run-manifest.md", f"""
request_summary: {args.request}
product_slug: {slug}
timestamp: {timestamp}
workflow_kind: promotion_concept
requested_outputs: evidence pack, standards map, market wedge, concept brief, presentation story, rich concept images, UI concept artifact, critique, report, handoff, promotion verdict
ui_concept_requested: true
run_status: degraded
ui_concept_artifact_present: false
ui_concept_verdict: blocked
sources: skeleton pending source research
standards: Double Diamond, d.school, NN/g, WCAG 2.2, privacy, data feasibility pending mapping
assumptions_gaps: skeleton created before evidence; all claims require validation
 downstream_target: design-skills or frontend after validation
""")
    write(root / "01-sources.md", """
| url | source_role | quality_tier | claim | opponent/pain signal | decision impact | supports_promotion | retrieval_date | verification_status |
|---|---|---|---|---|---|---|---|---|
| TBD | feasibility constraint source pending | A | pending | constraint pending | do not promote until replaced | no | TBD | unverified |
| TBD | direct opponent pending | B | pending | direct opponent pending | do not promote until replaced | no | TBD | unverified |
| TBD | workaround pending | B | pending | workaround pending | do not promote until replaced | no | TBD | unverified |
| TBD | pain signal pending | C | pending | pain signal not proof | do not promote until replaced | no | TBD | unverified |
| TBD | pain signal pending | C | pending | pain signal not proof | do not promote until replaced | no | TBD | unverified |
""")
    write(root / "02-standards.md", """
| Standard or source | Smallest relevant rule | Product decision |
|---|---|---|
| Double Diamond | Discover/Define before Develop/Deliver. | Evidence and market wedge precede screens. |
| d.school | Empathize, Define, Ideate, Prototype, Test. | Treat UI as concept only until tested. |
| NN/g | Match to real world, error prevention, visibility of status. | Show evidence status and unsupported assumptions. |
| WCAG 2.2 | Perceivable, operable, understandable, robust. | Use accessible labels and contrast. |
| Privacy | Minimise personal data and state handling assumptions. | Do not store private data in artifacts. |
| Data feasibility | Input quality and source traceability shape automation. | Mark uncertain extraction as human review. |
""")
    write(root / "03-golden-workflow.md", """
# Golden workflow

happy path: user enters the use moment, captures evidence, reviews source-truth, resolves gaps, exports a follow-up package.

edge state: missing source, uncertain rule, conflicting evidence, private data, unsupported claim.

failure state: source unavailable, artifact generation blocked, UI concept unavailable, legal/professional advice risk.

```mermaid
graph TD
  A[Evidence intake] --> B[Source-truth review]
  B --> C[Concept decision]
  C --> D[Follow-up package]
  B --> E[Human review needed]
```
""")
    write(root / "04-research-synthesis.md", """
# Research synthesis

| type | content | confidence | implication |
|---|---|---|---|
| fact | pending authoritative source review | low | do not promote yet |
| source claim | pending | low | replace skeleton rows |
| signal | pain signals are pending and must be treated as signal, not proof | low | validate before promotion |
| inference | concept may reduce follow-up friction | assumption | needs interviews |
| assumption | user will trust a guided package | unvalidated | test with target users |
| gap | no primary research or expert review yet | high | promotion blocked |
""")
    write(root / "05-concept-brief.md", """
# Concept brief

User/problem: bounded beachhead user has a high-stakes decision moment with scattered evidence and uncertainty.

Job: help the user organise evidence, understand gaps, and prepare a clean follow-up without overclaiming authority.

Value proposition: a guided evidence-to-follow-up package that is source-traced, cautious, and reviewable.

Constraints: no legal/professional advice claims, privacy minimisation, source uncertainty, accessibility, data feasibility.

Non-goals: production implementation, validated prototype, legal/professional determination, broad everyone-product.

Success criteria: target users understand the next step, can export a cleaner package, and trust uncertainty labels.

Evidence assumptions risks: all pending until source review, user interviews, and expert review land.
""")
    write(root / "06-market-wedge.md", """
beachhead_segment: Bounded target users in one launch region with a specific high-stakes use moment
launch_region: launch region pending source lock
use_moment: preparing a source-traced follow-up package before a consequential handoff
excluded_users: generic consumers, enterprise teams, users needing professional/legal advice, all-purpose dashboard users
local_constraints: local rules, privacy, source quality, professional advice boundary, data feasibility
opponent_map: direct: incumbent specialist tools pending; workaround: spreadsheets, email, notes, generic AI/chat, manual consultant/professional help
strongest_direct_opponent: pending opponent scan
why_users_choose_opponent_today: existing tools/workarounds are familiar, trusted, or bundled into current workflow
opponent_coverage_gap: hypothesis pending; likely source-traced preparation for one narrow handoff moment
pain_evidence_status: skeleton only; Tier C/community pain signals are signal, not proof
novelty_evidence_status: assumption
customer_pull_signal: none yet; requires interviews or usage evidence
market_gate_verdict: degraded
kill_or_pivot_condition: kill if target users do not report the specific handoff pain or already trust existing workflows
novelty_delta_hypothesis: a narrow source-traced preparation pack for one high-stakes handoff
 delta_against_opponent: narrower and more evidence-explicit than broad dashboards or generic AI notes
not_the_novelty: not AI, not better UI, not a generic dashboard, not no competitors
""")
    write(root / "06-presentation-story.md", """
# Presentation story

story_moment_id: M1
slide: problem
problem: high-stakes handoff evidence is scattered and uncertain.

story_moment_id: M2
slide: insight
insight: users need source-truth and gap labels before a polished follow-up.

story_moment_id: M3
slide: idea
idea: guided evidence capture, source comparison, and follow-up pack.

key moments: prepare, capture, compare, review, export.
proof: pending sources, artifacts, and user validation.
""")
    write(root / "07-journey-map.md", """
# Journey map

Persona/scenario: bounded target user in one launch region preparing for a consequential handoff.

1. Trigger: user faces deadline or handoff moment.
2. Gather: user captures documents/photos/notes.
3. Compare: product maps evidence against sources and assumptions.
4. Review: user resolves missing evidence and uncertainty.
5. Export: user sends a clear follow-up package.

Edge/failure states: uncertain evidence, unsupported claim, privacy-sensitive data, missing source, professional advice boundary.
""")
    write(root / "08-screen-spec.md", """
# Screen spec

Stitch/local HTML concept request. Build responsive screens with accessibility, privacy, data-state clarity, and key screens.

screen_id: intake-evidence
- `Evidence Intake`
- state: empty, captured, missing required context

screen_id: source-trace
- `Source Trace`
- state: matched source, assumption, human review needed

screen_id: follow-up-pack
- `Follow-up Pack`
- state: draft, ready to review, blocked by missing evidence

Required visible labels:
- `Evidence Intake`
- `Source Trace`
- `Follow-up Pack`
- `Human Review Needed`
""")
    write(root / "09-concept-images" / "manifest.md", """
status: blocked skeleton
prompt: pending rich image generation
provider: pending
model: gpt-image-2 required for final package
output path: 09-concept-images
actual image artifact: pending hero, storyboard, key-screen
 dimensions: pending
story_moment_id: M1, M2, M3
screen_id: intake-evidence, source-trace, follow-up-pack
source_truth_refs: 01-sources.md, 06-market-wedge.md, 08-screen-spec.md
launch_region: pending
beachhead: pending
not_ui_proof: true
""")
    write(root / "09-concept-images" / "critique.md", """
concept clarity: blocked until generated
 audience: pending
storyboard: pending
key screens: pending
readability: pending
misleading: must not imply legal/professional certainty
presentation quality: pending
region consistency: pending
geography drift: pending
verdict: blocked; concept image only, not UI proof
""")
    write(root / "09-ui-concept" / "README.md", """
# UI concept

Status: blocked skeleton. Local HTML/export and screenshots are pending.

This folder must eventually include rendered UI concept evidence or exact blocker notes.
""")
    write(root / "09-ui-concept" / "stitch-attempt.md", """
stitch adapter command: pending or local HTML fallback
confirmation: not run yet
status: blocked
artifact: pending
blocker: skeleton created before UI concept generation
""")
    write(root / "10-critique.md", """
| standard | status | evidence | severity | action item | next validation step |
|---|---|---|---|---|---|
| visual | blocked | no final visuals yet | high | generate and critique images | image audit |
| WCAG | degraded | spec requires accessibility | medium | render HTML and screenshot | accessibility pass |
| idea quality | degraded | concept hypothesis only | high | source and user validation | interviews |
| presentation | blocked | storyboard pending | high | generate images | deck review |
| region specificity | degraded | region pending | high | lock sources and launch region | source review |
| strongest direct opponent | degraded | opponent pending | high | scan opponents | market wedge update |
| novelty delta | degraded | assumption only | high | compare against opponent | validation |
| customer pull | blocked | no primary evidence | high | interview target users | research sprint |
| UI concept | blocked | no rendered artifact yet | high | build local HTML/screenshot | UI audit |
""")
    write(root / "11-concept-report.md", """
# Concept report

Research basis: skeleton only; sources and primary research pending.

Market wedge: degraded until launch region, strongest direct opponent, and pain signals are validated.

Design rationale: organise evidence, expose uncertainty, and generate a clean follow-up package.

Standards compliance: WCAG/NN/g/privacy/data feasibility mapped in draft only.

Feasibility: depends on source quality, extraction reliability, and professional advice boundaries.

Risks: legal/professional advice overclaim, privacy, false confidence, weak customer pull, source drift.

Assumptions: target users trust a cautious evidence organiser; current workarounds are painful enough.

Validation plan: source scan, 8-12 target interviews, expert review, concept test, UI usability test.
""")
    write(root / "12-handoff.md", """
# Handoff

Artifact inventory: skeleton contract files created; images/UI evidence pending unless later updated.

Source-truth: 01-sources.md is placeholder until replaced with real links.

Decisions: start degraded; do not promote until checker/source links/artifacts pass.

Risks: privacy, professional advice, unsupported claims, missing user evidence.

Open questions: launch region, strongest direct opponent, actual user pain, willingness to use/pay.

Missing evidence: authoritative sources, opponent scan, pain signals, rendered UI concept, image audit.

Assumptions: evidence organisation has value before professional review.

Downstream lane: design-skills/front-end only after validation.

Promotion verdict: false until final checks pass.
""")
    write(root / "15-promotion-verdict.md", """
promotion_eligible: false
promotion_scope: not promotion-ready; skeleton/degraded package only
source links: not checked
concept images: blocked until generated and audited
UI concept: blocked until rendered artifact and screenshot exist
visual/a11y: not complete
independent audit: pending
verdict: degraded skeleton; do not promote
""")

    print(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
