# Output Shapes

Default compact shape:
- result / verdict
- evidence used
- risks and assumptions
- next action

Promotion concept run shape follows `e2e-artifact-contract.md` exactly. Do not invent alternate numbered chains for full runs.

Status values:
- `pass`
- `fail`
- `degraded`
- `blocked`

Use `degraded` when the concept is useful but not promotion-ready because evidence, source verification, image quality, UI concept proof, or user/integration validation is missing. Use `blocked` when a requested external/tool step could not run. Use `fail` when an artifact exists but is fake, contradictory, or unsafe to promote.

Keep proof fields separate:
- `ui_concept_artifact_present`: rendered/exported file exists
- `ui_concept_core_flow_demonstrated`: rendered output shows the promised job
- `ui_concept_quality_verdict`: visual/source-truth/a11y status
- `promotion_eligible`: independent readiness verdict from `15-promotion-verdict.md`

Concept image output:
- image/storyboard/key-screen prompt
- provider/model, explicitly `gpt-image-2`
- output path and actual image artifact path
- `story_moment_id` and `screen_id` mapping when relevant
- dimensions, critique verdict, and `not_ui_proof: true`
- blocker reason only when generation fails; this is not completion

Presentation/report output:
- deck storyline and slide intent
- written report with research basis, rationale, standards, feasibility, risks, assumptions, validation plan
- judge communication clarity and idea quality before visual polish

Review output:
- standard
- status
- evidence
- severity
- action item
- next validation step
