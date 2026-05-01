---
name: concept-review-gate
description: Review product concepts, rich images, and UI concept evidence for UX clarity, risk, and promotion readiness.
---

# Concept Review Gate

Use to critique product-design concepts, concept images, sketches, or Stitch/HTML UI concept screens before handoff or deeper design work.

Read first:
- `../product-design-common/references/product-design-contract.md`
- `../product-design-common/references/ux-quality-gates.md`
- `../product-design-common/references/positioning-marketing-risk.md`
- `../product-design-common/references/output-shapes.md`
- `../product-design-common/references/industry-quality-bar.md`
- `../product-design-common/references/standards-and-sources.md`
- `../product-design-common/references/safety-boundaries.md`

Workflow:
1. Identify target beachhead, user moment, product promise, artifacts, and evidence quality.
2. Review clarity, hierarchy, task flow, trust, WCAG basics, feasibility, and source/standard traceability.
3. Critique `gpt-image-2` images: richness, audience/context fit, story/screen mapping, presentation quality, no misleading claims, not UI proof.
4. Review UI concept quality only from rendered evidence: HTML/export plus viewport/full-page screenshots when available.
5. Check NN/g, Apple/HIG-level clarity, GOV.UK/AU service clarity, WCAG 2.2, privacy/data feasibility, and positioning risk.
6. Return promotion-ready only when required evidence exists; otherwise return degraded/fail/blocked with missing evidence and next action.

Output:
- artifact/concept reviewed
- evidence and standards used
- UX/visual findings and severity
- concept-image verdict or skip evidence
- UI concept verdict or blocker
- positioning/marketing risks
- verdict, missing evidence, assumptions, risks, and next action
