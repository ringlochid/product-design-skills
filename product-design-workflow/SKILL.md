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
2. **Skeleton first:** immediately create every required file/folder with honest draft content, including critique, report, handoff, and promotion verdict files. Start with `run_status: degraded`, `promotion_eligible: false`, and honest UI fields until evidence proves otherwise.
3. Set `workflow_kind: promotion_concept`; record `ui_concept_requested`, `ui_concept_artifact_present`, and `ui_concept_verdict` honestly.
4. Write the default evidence pack and structured market wedge before solution work: beachhead segment, excluded users, use moment, opponents/workarounds, pain rows, novelty delta hypothesis, and market gate verdict.
5. Write sources, standards map, golden workflow, synthesis, concept brief, presentation story, journey, and screen spec with stable `story_moment_id` and `screen_id` values.
6. **First complete pass before polish:** update critique/report/handoff/verdict from the current evidence before generating extra variants. A complete degraded package beats an incomplete polished package.
7. Generate and critique real, readable `gpt-image-2` presentation visuals: hero, storyboard, and selected key screens mapped to story/screen IDs.
8. Enter the Stitch/HTML lane by default for a UI concept artifact; record real artifacts/screenshots or the exact blocker in `09-ui-concept`. Screenshots must show the rendered concept, not a blank/error/404 browser page.
9. Review Apple/HIG-level clarity, WCAG, source-truth match, screenshot sanity, image/UI coherence, novelty, customer pull, risk, and evidence.
10. Finalize deterministically before any extra polish: if `promotion_eligible: true`, run `product-design-common/scripts/check_source_links.py <folder>` and save stdout as `14-source-link-check.txt`; then run `product-design-common/scripts/check_product_design_run.py <folder>`. The checker writes `13-artifact-check.txt` itself. Stop after final checks and report pass/degraded/blocked rather than continuing refinements.

Output:
- run folder path
- artifact inventory and pass/fail/degraded/blocked status
- evidence, standards, assumptions, and risks
- beachhead, strongest opponent, novelty delta, pain signals, customer-pull verdict
- rich concept image/storyboard/key-screen paths and critique
- UI concept artifact/screenshots or exact blocker
- promotion verdict, missing evidence, downstream lane, and next validation
