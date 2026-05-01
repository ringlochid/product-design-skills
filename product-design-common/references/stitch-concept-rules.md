# Stitch Concept Rules

Use Stitch/HTML as the default lightweight visual backend for a UI concept artifact. It illustrates a concept; it is not a validated product prototype or implementation proof.

For promotion-style concept work:
- write `08-screen-spec.md` with stable `screen_id` values, hierarchy, states, data, copy intent, and risky claims
- create `09-ui-concept/stitch-attempt.md`
- record adapter command, confirmation state, status, artifact paths, screenshots, metadata, and exact blocker
- if external Stitch generation is authorized, invoke the adapter with confirmation; otherwise record the approval/preflight blocker
- if artifacts exist, include HTML/export plus local viewport and full-page screenshots where possible
- if unavailable, set `ui_concept_artifact_present: false` and `ui_concept_verdict: fail` or `blocked`; do not call it complete

UI concept acceptance requires rendered evidence in `09-ui-concept/`: Stitch/export HTML/FIG/PDF or local HTML, screenshots, readable labels matching `08-screen-spec.md`, no screenshot sanity failure, no fixed-nav overlap, no lock/copy failures, and no risky unsupported claims.

A markdown/spec dump saved as `.html` is not UI evidence. Judge concept clarity, hierarchy, key-state coverage, and interaction usefulness; production polish is optional.

Concept images are separate: actual `gpt-image-2` hero visuals, storyboards, and selected key-screen illustrations live in `09-concept-images/`. They enrich the presentation and may reference `screen_id`, but must never substitute for UI concept evidence.

External Stitch create/generate/edit is an external mutation. Do not mutate external tools without approval.

Generated UI concept output is not source truth.
