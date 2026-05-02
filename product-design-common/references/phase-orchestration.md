# Phase Orchestration Rules

The full workflow is a WBS orchestrator/router, not the thinking layer. It maps one deliverable into phases, work packages, and gates. The conductor is file manager for files/state; leaves do stage thinking.

Conductor responsibilities:
- own run folder, skeleton, phase status, final assembly
- pass smallest useful context packet to one leaf/package at a time
- copy leaf outputs into contract files with source links/artifact paths
- run deterministic gates and stop on blocked/degraded status
- resume from last completed phase

Leaf responsibilities:
- do bounded market/context, opportunity, journey, screen spec, UI, review, or handoff work
- return artifacts, evidence, assumptions, risks, blockers
- never decide promotion eligibility alone

WBS phases:
1. `bootstrap`: skeleton/defaults; package `pd-bootstrap`; gate contract-shaped folder.
2. `evidence`: sources, standards, wedge, story, journey, screen spec; packages `pd-market`, `pd-opportunity`, `pd-screen`; gate stable source/story/screen IDs.
3. `previsual_gate`: source/readiness check; package `pd-previsual`; gate pass or degraded stop.
4. `degraded_finalize`: critique/report/handoff/verdict before slow media; gate complete text package.
5. `visuals`: required hero/storyboard/key-screen assets; package `pd-visuals`; gate manifest/review.
6. `ui_concept`: Stitch/HTML artifact or blocker; package `pd-ui`; gate real artifact/screenshot or blocker.
7. `final_audit`: source links if promoting, checker, verdict; package `pd-final-audit`.

Parallelism: evidence packages may run in parallel only with separate ownership and shared IDs. Visuals, UI, and final audit are serial. If time is tight, finish the current phase and save the next package; do not start slow work.


Gate proof rule: each phase gate must name the script/check/artifact inspected, pass/degraded/blocked result, and blocker if proof could not run.
Before spawning, name the smallest useful slice that can satisfy the user if later phases block.
