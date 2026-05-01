# Safety Boundaries

Ask before:
- external writes, public posts, uploads, or messages
- logged-in browser sessions or account mutations
- reading credentials, secrets, tokens, or private ignored files
- paid generation/API calls when cost or quota matters
- destructive edits or repo publication
- external Stitch create/generate/edit if not already authorized by the current request

Do freely:
- local file reads/writes inside the requested bundle
- public source reading
- generated prompts/specs
- local validation scripts
- local screenshots of local artifacts

Never store credentials or private raw data in artifacts. Redact secrets in screenshots/logs.

Generated UI concept artifacts can illustrate ideas but must not be presented as validated user research, market proof, implementation proof, or production readiness.
