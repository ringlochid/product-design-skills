---
name: product-design-workflow
description: Conduct promotion-style concept packages with evidence, story, rich images, UI concept, critique, and verdict.
---

# Product Design Workflow

Use for full, real, industry-level, or promotion-ready concept packages. This is a thin conductor: router, context sharer, file manager, and phase gate. Leaf skills do the thinking.

Read first:
- `../product-design-common/references/product-design-contract.md`
- `../product-design-common/references/industry-quality-bar.md`
- `../product-design-common/references/e2e-artifact-contract.md`
- `../product-design-common/references/phase-orchestration.md`
- `../product-design-common/references/karpathy-product-design-rules.md`
- `../product-design-common/references/standards-and-sources.md`
- `../product-design-common/references/stitch-concept-rules.md`
- `../product-design-common/references/safety-boundaries.md`

Workflow:
1. Create `product-design-<product-slug>-<timestamp>/`; run `python3 product-design-common/scripts/create_product_design_skeleton.py <folder> --slug <product-slug> --request "<request summary>"` before any thinking work.
2. Run `python3 product-design-common/scripts/check_phase_status.py <folder>` at the start of every turn/resume and after each leaf output; continue only from the reported phase.
3. Treat the conductor as file manager only: write context packets, call/route one leaf lane, copy its bounded output into the contract files, then gate. Do not personally research, design, critique, and render everything in one pass.
4. Keep skeleton defaults until a gate proves otherwise: `run_status: degraded`, `promotion_eligible: false`, `ui_concept_artifact_present`, and `ui_concept_verdict`.
5. Evidence phase: route market/source/opportunity work to leaves; assemble sources, standards, market wedge, story, journey, and screen spec with stable `story_moment_id`/`screen_id` values.
6. Previsual gate: run `check_source_readiness.py <folder>`. If it fails or time is tight, update critique/report/handoff/verdict as degraded and stop cleanly.
7. Degraded finalize phase: before slow media, update critique, concept report, handoff, and promotion verdict files from current evidence so the package is complete even without visuals/UI.
8. Visual phase: generate exactly the required `gpt-image-2` hero, storyboard, and key-screen assets plus manifest/critique; no extra variants before gate pass.
9. UI phase: route to `stitch-concept-generator`; record real HTML/screenshots or exact blocker in `09-ui-concept`.
10. Final audit: route critique/handoff to leaves if needed, run source-link check only when promoting, then run `check_product_design_run.py <folder>`; stop after pass/degraded/blocked status.

Output:
- run folder path
- artifact inventory and pass/fail/degraded/blocked status
- evidence, standards, assumptions, and risks
- beachhead, strongest opponent, novelty delta, pain signals, customer-pull verdict
- rich concept image/storyboard/key-screen paths and critique
- UI concept artifact/screenshots or exact blocker
- promotion verdict, missing evidence, downstream lane, and next validation
