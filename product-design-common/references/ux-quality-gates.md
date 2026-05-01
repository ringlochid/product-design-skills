# UX Quality Gates

Review against a named persona/scenario/goal and concrete artifacts.

Core gates:
- value proposition and primary task are clear
- presentation story has problem, insight, idea, key moments, proof, and next validation
- report traces research basis, design rationale, standards, feasibility, risks, and assumptions
- hierarchy supports the happy path before secondary paths
- workflow handles edge/failure states
- copy is plain, truthful, and audience-fit
- source, freshness, uncertainty, and user control are visible when trust matters
- no misleading marketing promise or legal/official advice overreach
- WCAG 2.2 basics: contrast intent, labels, focus, target size, status messages, non-color-only state
- privacy/security/data feasibility risks are explicit when personal data or integrations appear

Visual gates:
- actual concept images, storyboards, and selected key-screen artifacts communicate the idea and fit audience/context
- UI quality is judged for concept clarity and interaction usefulness from rendered evidence: Stitch/export screenshot plus local viewport/full-page screenshots where possible
- production-quality frontend polish is outside the default concept bar unless explicitly requested, but real Stitch evidence is still required

Scorecard rows must include: standard, status, evidence, severity, action items, next validation step.


Visual failure classes: `nav-overlap`, `safe-area`, `density`, `contrast`, `small-text`, `screenshot-evidence-poor`, `visual-hierarchy`, `responsive-overflow`.

When any class blocks promotion, write `18-repair-plan.md` with blocker, target artifact, repair lane, expected proof, and rerun/audit criteria.

After `18-repair-plan.md`, run or record the repair in `19-repair-attempt.md`; then recapture screenshots and rerun visual/a11y audit.
