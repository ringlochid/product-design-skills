---
name: stitch-concept-generator
description: Use Stitch/HTML as the lightweight UI concept backend, recording artifacts or exact blockers.
---

# Stitch Concept Generator

Use Stitch/HTML to illustrate product ideas and quick UI concept screens. This is not the full design-skills production lifecycle.

Read first:
- `../product-design-common/references/product-design-contract.md`
- `../product-design-common/references/stitch-concept-rules.md`
- `../product-design-common/references/concept-page-spec-rules.md`
- `../product-design-common/references/safety-boundaries.md`
- `../product-design-common/references/output-shapes.md`
- `../product-design-common/references/industry-quality-bar.md`

Workflow:
1. Confirm concept brief/page spec is good enough.
2. Build a concise Stitch prompt from product intent, hierarchy, style direction, and `screen_id` values.
3. Enter the Stitch/HTML lane by default; create the UI concept stitch-attempt record before or during the attempt.
4. If the current request authorizes external Stitch generation, invoke the adapter with confirmation; otherwise record the approval blocker.
5. Treat generated screens as UI concept evidence, not source truth or validated prototype proof.
6. If HTML/export and screenshots are missing, label blocked/fail and not promotion-ready.
7. Return artifacts or exact blocker to concept review.

Output:
- concept prompt / generation brief
- Stitch action attempted or performed
- adapter command / confirmation state
- UI concept artifact links/paths if any, or exact blocker
- caveats and degraded evidence
- review handoff
- risks / blocked conditions
- assumptions
