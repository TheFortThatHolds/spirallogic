# Repository Guidelines

## Project Structure & Module Organization
- `spirallogic/`: core language modules; `runtime/` handles orchestration, `parser/` builds AST, `ai_generation/` hosts prompt templates, `voices/` defines persona metadata.
- `examples/`: canonical `.sl` ritual scripts used in docs and smoke tests.
- `docs/`: author background references; update when runtime behavior changes.
- Root utilities: `spirallogic_cli.py` CLI runner, `unicode_sanitizer.py`, and scenario-specific test drivers (`test_suite.py`, `test_crisis.py`).

## Build, Test, and Development Commands
- `python spirallogic_cli.py examples/journaling_support.sl --verbose` — Run end-to-end ritual; inspect `spirallogic_attestations.log` afterward.
- `python test_suite.py` — Execute baseline runtime regression tests with auto-consent hooks.
- `python -m pytest` — Optional; discovers `test_*.py` for targeted cases.
- `run_test.bat` (Windows) — Convenience wrapper for core ritual smoke tests.

## Coding Style & Naming Conventions
- Python 3.10+, 4-space indentation, limit lines to 100 characters.
- Modules follow `snake_case.py`; classes are `PascalCase`; exported rituals and voices use `@voice` naming aligned with examples.
- Keep functions pure where possible; prefer dataclasses (`ConsentRequest`, `RitualContext`) for state.
- Add docstrings describing intent and consent implications; log user-facing output through sanitizers.

## Testing Guidelines
- Add deterministic tests alongside new modules; place scenario scripts under `examples/` and callable tests in `test_<feature>.py`.
- Use descriptive test names (`test_consent_timeout`); assert both success flags and context fields.
- Maintain coverage for consent flows, voice selection, and logging side effects.
- Update fixtures so tests pass on Windows terminals (use `sanitize_for_windows_terminal`).

## Commit & Pull Request Guidelines
- Use Conventional Commit prefixes (`feat:`, `fix:`, `docs:`, etc.); scope modules when helpful (`feat(runtime): ...`).
- Commit messages should mention ritual or module touched and notable consent changes.
- PRs must include summary bullets, test evidence (`python test_suite.py` output or run log), and link to relevant spec references (e.g., `spirallogic_spec.pdf`).
- Request review from another agent before merging runtime or parser changes.

## Security & Configuration Tips
- Never check in actual user transcripts; redact samples under `examples/`.
- Regenerate SQLite artifacts with `spirallogic_runtime.py` helpers; avoid committing personalized `.db` files.
- Keep secrets and API keys out of `.sl` rituals; use environment variables read inside runtime hooks.
