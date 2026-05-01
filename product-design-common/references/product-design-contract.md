# Product Design Contract

Product-design turns market/customer/product intent into an evidence-backed promotion concept package: research, market wedge, story, rich presentation visuals, UI concept evidence, critique, promotion verdict, and handoff.

## Lifecycle

For full promotion concept runs, create a complete timeout-safe skeleton before research or polishing, preferably with `create_product_design_skeleton.py`. Required end-state files should exist early with honest `degraded`/`blocked` status, then improve as evidence and artifacts land.

1. Clarify audience, problem, outcome, and use moment.
2. Lock launch region/beachhead, beachhead segment, excluded users, and local constraints before solution claims.
3. Gather the default evidence pack: Tier A feasibility/constraint, Tier B opponents, Tier C real-user pain signals, plus caveats for weak evidence.
4. Write a structured market wedge: strongest direct opponent, current workaround, opponent gap, pain evidence status, novelty delta hypothesis, not-the-novelty, market gate verdict, kill/pivot condition.
5. Synthesize facts, source claims, signals, inferences, assumptions, and gaps.
6. Frame one sharp concept and one core journey before screens.
7. Write presentation story with stable `story_moment_id` values.
8. Write screen spec with stable `screen_id` values.
9. Generate rich `gpt-image-2` presentation visuals: hero, storyboard, selected key-screen illustrations.
10. Use Stitch/HTML by default for a UI concept artifact, not a validated product prototype.
11. Review evidence, novelty delta, customer pull, Apple/HIG-level clarity, WCAG, positioning risk, image/UI coherence, and promotion readiness.
12. Hand off cleanly to design-skills, frontend handoff, or stakeholders.

## Boundaries

- Product-design owns concept source truth, opponent scans, market wedges, concept prompts, presentation visuals, UI concept artifacts, reports, and promotion verdicts.
- Full design-skills owns serious design repo lifecycle, responsive repair, generation packs, and production handoff.
- Coding skills own implementation.
- Marketing/GTM skills own campaigns, channels, launch calendars, and ad systems.

Stop when evidence is too thin, external writes/credentials are needed, or UI concept artifacts are claimed but unavailable. Full promotion concept packages use `product-design-workflow`.
