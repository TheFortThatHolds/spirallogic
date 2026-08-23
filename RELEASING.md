# Releasing SpiralLogic

The repo publishes itself. `.github/workflows/publish-spirallogic.yml` (here since
Nov 2025) builds and uploads to PyPI via trusted publishing (OIDC) **on every push
to `main`** — the PyPI-side trusted publisher is already configured for this repo.
`skip-existing: true` means pushes that don't bump the version are a no-op.

To ship a release:

1. Bump the version in `pyproject.toml` AND `src/spirallogic/__init__.py` (keep them in sync).
2. Merge to `main`.
3. That's it. CI builds and publishes automatically. Verify at
   https://pypi.org/project/spirallogic/ (upload lands within ~a minute of the merge).

No tokens, no twine, no manual upload. Do not add a second publish workflow —
one already exists (learned 2026-08-23, when a duplicate rail and a Cloudflare
relay were built before anyone ran `ls -a` and found this one).
