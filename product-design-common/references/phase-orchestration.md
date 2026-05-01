# Phase Orchestration Rules

The full workflow is an orchestrator/router, not the thinking layer. The conductor is the file manager for the package.

Conductor responsibilities:
- create and own the run folder, skeleton, phase status, and final assembly
- pass the smallest useful context packet to one leaf at a time
- copy leaf outputs into contract files, preserving source links and artifact paths
- run deterministic gates between phases and stop on blocked/degraded status
- resume from the last completed phase instead of restarting the package

Leaf responsibilities:
- do the stage thinking: market/context, opportunity, journey, screen spec, UI concept, review, or handoff
- return bounded artifacts, evidence, assumptions, risks, and blockers
- never decide promotion eligibility alone

Phases:
1. `bootstrap`: create skeleton and defaults.
2. `evidence`: source pack, standards, market wedge, story, journey, screen spec.
3. `previsual_gate`: run source/previsual readiness; do not generate visuals before pass.
4. `degraded_finalize`: update critique/report/handoff/verdict from current evidence before slow media.
5. `visuals`: generate exactly required hero/storyboard/key-screen assets and manifest.
6. `ui_concept`: create Stitch/HTML artifact or exact blocker.
7. `final_audit`: run source links if promoting, then final checker.

If time is tight, the conductor must finish the current phase and save the next phase, not start slow work.
