# Product Design Skills

Standalone product-design concept/prototype bundle.

This bundle turns product/market/customer intent into lightweight UX concepts and optional Stitch concept prototypes. It is upstream of the full `design-skills` bundle.

## Flow

```text
market/context → concept brief → opportunity framing → journey/flow → concept page spec → optional Stitch concept → review → handoff
```

## Public skills

- `product-design-router` — route product-design concept/prototype requests.
- `market-context-reader` — read market/customer/competitor context enough to frame the concept.
- `product-concept-brief` — write user/problem/value/constraints/success concept brief.
- `opportunity-framing` — outcome → opportunity → solution hypotheses.
- `journey-flow-mapper` — journey, decisions, states, edge cases.
- `concept-page-spec-writer` — lightweight page/screen specs for concepts.
- `stitch-concept-generator` — use Stitch for quick concept screens only.
- `concept-review-gate` — review UX, positioning, marketing risk, accessibility basics, and feasibility.
- `product-design-handoff` — package handoff for design-skills, frontend, stakeholders, or GTM.

`product-design-common/` is shared support only and intentionally has no `SKILL.md`.

## Boundary

Product-design owns concept source truth and lightweight prototypes.

Full `design-skills` owns serious design repo lifecycle, production generation packs, responsive repair, artifact governance, and implementation handoff.

Coding skills own implementation. Future marketing/GTM skills own campaigns, channels, launch calendars, ads, and growth experiments.

## Validate

```bash
python3 product-design-common/scripts/validate_product_design_bundle.py
```

## Synthetic test artifact chain

Expected end-to-end concept-prototype chain:

```text
market-context notes → concept brief → opportunity frame → journey/flow → concept page spec → Stitch concept prompt/screen → concept review → product-design handoff
```

Tests should use only the 9 top-level product-design skills. Community GitHub snapshots live outside this bundle root and are reference-only.
