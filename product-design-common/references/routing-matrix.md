# Routing Matrix

## Effort tiers

- quick: one lane, enough structure to answer or route.
- standard: normal concept work across 1-3 lanes with assumptions and risks.
- deep: stronger evidence, alternatives, and review before handoff.
- concept-prototype: full chain ending in optional Stitch concept and review.

| Request signal | First lane |
|---|---|
| ambiguous product/design ask | `product-design-router` |
| market/customer/competitor notes | `market-context-reader` |
| messy idea to brief | `product-concept-brief` |
| feature request / vague solution | `opportunity-framing` |
| flow/onboarding/funnel | `journey-flow-mapper` |
| page/screen concept | `concept-page-spec-writer` |
| quick visual prototype | `stitch-concept-generator` |
| critique/review/risk | `concept-review-gate` |
| package for downstream design/frontend | `product-design-handoff` |

Tie-breaks:
- For end-to-end concept-prototype asks, chain lanes instead of pretending one lane is enough.
- If the user asks to generate a quick visual concept, use Stitch concept after brief/spec.
- If the user asks for production design repo work, hand off to design-skills.
- If the user asks for implementation, hand off to coding skills.
