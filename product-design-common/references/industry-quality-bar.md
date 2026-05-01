# Industry Quality Bar

Rule: every claim, decision, screen, image, and critique traces to evidence, standard, or explicit assumption.

A promotion concept package cannot pass unless:
- Discover/Define evidence exists before Develop/UI concept output
- claims are sourced or marked assumption
- launch region/beachhead, excluded users, use moment, opponents, pain signals, and customer pull exist before solution work
- novelty is a delta against the strongest direct opponent, not “no one does this,” nicer UI, an AI wrapper, or a personalized dashboard
- the concept solves a whole user problem, not a decorative screen
- promotion-supporting URLs pass link check; 4xx/5xx cannot support promotion
- smallest relevant sources/standards are captured before decisions
- golden workflow has happy path, edge/failure states, and Mermaid
- presentation story and concept report exist
- readable `gpt-image-2` hero, storyboard, and key-screen images exist, preserve beachhead, and map to story/screen IDs
- Stitch/HTML runs by default for UI concept evidence; prompt-only or markdown/spec-as-HTML fails
- UI concept evidence includes HTML/export plus screenshots; production polish is not required
- critique names standards, persona/scenario/goal, severity, and action items
- WCAG 2.2, privacy/security, data feasibility, Apple/HIG-level clarity and positioning risks are reviewed
- success criteria and next validation exist
- handoff lists artifacts, decisions, risks, questions, assumptions, downstream lane

UI concept gate: requested UI without rendered Stitch/HTML evidence means `run_status: blocked`, `ui_concept_artifact_present: false`, `ui_concept_verdict: fail`.

Concept gate: deck/report quality is narrative clarity, evidence traceability, visual explanation, idea strength, feasibility, and validation.

Market gate: no real beachhead, strongest direct opponent, pain evidence, novelty delta against opponent, or customer pull means kill/pivot/degraded before promotion.

Visual-region gate: geography/audience drift from the locked beachhead blocks or degrades visual quality.

Promotion requires: checker PASS, source links PASS, concept-image critique PASS, UI concept screenshots, visual/a11y review, and independent audit.

Layer rule: Mermaid = workflow truth; deck/report = argument truth; `gpt-image-2` = concept/storyboard/key-screen truth; Stitch/HTML = UI concept truth; screenshots = visual audit truth.
