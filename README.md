# Product Design Skills

Standalone promotion-style product-design concept bundle.

This bundle turns product/market/customer intent into evidence-backed concept packages with rich presentation images and a Stitch/HTML UI concept artifact. It is upstream of the full `design-skills` bundle.

## Flow

Leaf flow:

```text
market/context → concept brief → opportunity framing → journey/flow → concept page spec → optional UI concept → review → handoff
```

Promotion concept flow:

```text
product-design-workflow → evidence pack → market wedge → story → rich images → UI concept → critique → promotion verdict → handoff
```

## Public skills

- `product-design-workflow` — conduct promotion-ready concept packages with sources, standards, rich images, UI concept evidence, critique, and handoff.
- `product-design-router` — route product-design concept and UI concept requests.
- `market-context-reader` — read market/customer/competitor context enough to frame the concept.
- `product-concept-brief` — write user/problem/value/constraints/success concept brief.
- `opportunity-framing` — outcome → opportunity → solution hypotheses.
- `journey-flow-mapper` — journey, decisions, states, edge cases.
- `concept-page-spec-writer` — lightweight page/screen specs for concepts.
- `stitch-concept-generator` — use Stitch/HTML for quick UI concept screens only.
- `concept-review-gate` — review UX, positioning, marketing risk, accessibility basics, and feasibility.
- `product-design-handoff` — package handoff for design-skills, frontend, stakeholders, or GTM.

`product-design-common/` is shared support only and intentionally has no `SKILL.md`.

## Two lanes

- **Leaf lane:** one narrow artifact or review stage.
- **Workflow lane:** promotion concept run with sources, standards, market wedge, rich images, UI concept artifact, critique, promotion verdict, and handoff.

## Boundary

Product-design owns concept source truth, market wedge, visual story pack, and UI concept evidence.

Full `design-skills` owns serious design repo lifecycle, production generation packs, responsive repair, artifact governance, and implementation handoff.

Coding skills own implementation. Future marketing/GTM skills own campaigns, channels, launch calendars, ads, and growth experiments.

## Validate

```bash
python3 product-design-common/scripts/validate_product_design_bundle.py
python3 product-design-common/scripts/test_product_design_checker.py
```

## Synthetic test artifact chain

Expected leaf-level concept chain:

```text
market-context notes → concept brief → opportunity frame → journey/flow → concept page spec → UI concept prompt/screen → concept review → product-design handoff
```

Tests should use only the 10 top-level product-design skills. Community GitHub snapshots live outside this bundle root and are reference-only.

## Industry-level quality bar

A promotion concept package cannot pass unless claims trace to evidence, standards, or explicit assumptions; UI concept evidence has real artifacts; critique references standards such as WCAG 2.2, NN/g heuristics, GOV.UK/AU service standards, Apple/HIG-level clarity, and platform/design-system conventions; and handoff lists artifacts, status, risks, gaps, and downstream lane.

## Source-use rule

Use GOV.UK, AU/NSW/Queensland, USWDS, Canada GC, 18F, WCAG, Apple, Material, Atlassian, Carbon, and NN/g as standards/reference material. Do not copy layouts, wording, or component source; extract reusable checks, cite the source in `01-sources.md`, and map decisions in `02-standards.md`.
