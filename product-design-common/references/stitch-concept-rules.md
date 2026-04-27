# Stitch Concept Rules

Stitch is allowed here as a quick visual backend for concept illustration.

## Minimum viable input

Before Stitch, have at least:
- product goal
- target user / use moment
- core page or flow
- hierarchy / key sections
- primary action
- style direction or constraints

## Prompt contract

```markdown
Product:
User / use moment:
Goal:
Screen(s):
Hierarchy:
Primary action:
Data/content:
States:
Style direction:
Constraints:
```

## Rules

- use only after a brief/spec exists or the user explicitly asks for rough exploration
- prompts must include product goal, audience, hierarchy, constraints, and style direction
- generated output is concept evidence, not source truth
- do not run the full design repo lifecycle or production repair loop
- ask before actions that create/edit external Stitch state when policy requires it
- if Stitch is unavailable, return the prompt and mark `degraded: no Stitch execution`
- hand concept screens to review before treating them as useful
