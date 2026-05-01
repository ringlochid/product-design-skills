# Promotion Concept Artifact Contract

Folder: `product-design-<product-slug>-<YYYYMMDDTHHMMSSZ>/`.

Promotion-style concept runs use this exact shape. If caller filenames conflict, flag the conflict and follow this contract.

Required files/folders:
- `00-run-manifest.md`: `request_summary`, `product_slug`, `timestamp`, `workflow_kind`, `requested_outputs`, `ui_concept_requested`, `run_status`, `ui_concept_artifact_present`, `ui_concept_verdict`, `sources`, `standards`, `assumptions_gaps`, `downstream_target`
- `01-sources.md`: table columns `url | source_role | quality_tier | claim | opponent/pain signal | decision impact | supports_promotion | retrieval_date | verification_status`
- `02-standards.md`: smallest relevant decision map: process, WCAG/NN/g, platform/HIG where useful, region/service/privacy/data feasibility
- `03-golden-workflow.md`: happy path, edge/failure states, Mermaid diagram
- `04-research-synthesis.md`: fact, source claim, signal, inference, assumption, gap
- `05-concept-brief.md`
- `06-market-wedge.md`: structured beachhead/opponent/pain fields including strongest direct opponent, novelty delta, and market gate
- `06-presentation-story.md`: deck outline with stable `story_moment_id` values
- `07-journey-map.md`
- `08-screen-spec.md`: Stitch request with stable `screen_id` values
- `09-concept-images/`: actual high-resolution `gpt-image-2` hero, storyboard, and key-screen images; manifest maps image role to `story_moment_id`, `screen_id`, source refs, launch region, beachhead, dimensions, and `not_ui_proof: true`; critique audits richness and geography drift
- `09-ui-concept/`: README and `stitch-attempt.md`; HTML/export plus screenshot paths when artifact is present, or exact blocker when not
- `10-critique.md`: scorecard table with standard, status, evidence, severity, action item, next validation step
- `11-concept-report.md`: research basis, market wedge, design rationale, standards compliance, feasibility, risks, assumptions, validation plan
- `12-handoff.md`
- `13-artifact-check.txt`
- `15-promotion-verdict.md`: `promotion_eligible`, `promotion_scope`, source links, concept images, UI concept, visual/a11y, independent audit, verdict

Conditional:
- `14-source-link-check.txt` with `VERDICT=PASS` is required when `promotion_eligible: true`.
- Dead/blocked links may be recorded as gaps but cannot support promotion.

Finalization order: write report/handoff/verdict; if promoting, save `check_source_links.py <folder>` output to `14-source-link-check.txt`; run `check_product_design_run.py <folder>` before declaring done. The checker writes `13-artifact-check.txt`; do not hand-patch test results. If time is tight, prefer final checks over extra polish and report exact degraded/blocked gaps.
