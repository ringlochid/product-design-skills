---
name: product-design-workflow
description: Conduct promotion-style concept packages with evidence, story, rich images, UI concept, critique, and verdict.
---

# Product Design Workflow

Use for full, real, industry-level, or promotion-ready concept packages. This is the conductor; leaf skills handle individual stages.

Read first:
- `../product-design-common/references/product-design-contract.md`
- `../product-design-common/references/industry-quality-bar.md`
- `../product-design-common/references/e2e-artifact-contract.md`
- `../product-design-common/references/karpathy-product-design-rules.md`
- `../product-design-common/references/standards-and-sources.md`
- `../product-design-common/references/stitch-concept-rules.md`
- `../product-design-common/references/safety-boundaries.md`

Workflow:
1. Create `product-design-<product-slug>-<timestamp>/` and follow the promotion concept artifact contract exactly.
2. Set `workflow_kind: promotion_concept`; record `ui_concept_requested`, `ui_concept_artifact_present`, and `ui_concept_verdict` honestly.
3. Write the default evidence pack and structured market wedge before solution work: beachhead segment, excluded users, use moment, opponents/workarounds, pain rows, novelty delta hypothesis, and market gate verdict.
4. Write sources, standards map, golden workflow, synthesis, concept brief, presentation story, journey, and screen spec with stable `story_moment_id` and `screen_id` values.
5. Generate and critique real, readable `gpt-image-2` presentation visuals: hero, storyboard, and selected key screens mapped to story/screen IDs.
6. Enter the Stitch/HTML lane by default for a UI concept artifact; record real artifacts/screenshots or the exact blocker in `09-ui-concept`.
7. Review Apple/HIG-level clarity, WCAG, source-truth match, screenshot sanity, image/UI coherence, novelty, customer pull, risk, and evidence.
8. Write report, handoff, and promotion verdict.
9. Finalize deterministically before any extra polish: run `product-design-common/scripts/check_source_links.py <folder>` when `promotion_eligible: true`, save that output as `14-source-link-check.txt`, then run `product-design-common/scripts/check_product_design_run.py <folder>`. The artifact checker writes `13-artifact-check.txt` itself. If time is tight, stop after these checks and report pass/degraded/blocked rather than continuing refinements.

Output:
- run folder path
- artifact inventory and pass/fail/degraded/blocked status
- evidence, standards, assumptions, and risks
- beachhead, strongest opponent, novelty delta, pain signals, customer-pull verdict
- rich concept image/storyboard/key-screen paths and critique
- UI concept artifact/screenshots or exact blocker
- promotion verdict, missing evidence, downstream lane, and next validation
