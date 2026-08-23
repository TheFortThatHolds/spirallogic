# Releasing SpiralLogic

1. Bump the version in `pyproject.toml` and `src/spirallogic/__init__.py` (keep them in sync).
2. Build and check: `python -m build && twine check dist/*` (both must PASS).
3. Smoke-test the wheel from a clean directory: install it, run `spirallogic --help`, and confirm `spirallogic.__version__`.
4. Publish. Two rails exist:
   - **Fort Card (wallet-brokered):** the PyPI token lives in the Fort Card wallet as secret `pypi`. An agent requests a card scoped to `upload.pypi.org` and spends it — the raw token is never held by the agent or stored in this repo.
   - **GitHub Actions (`.github/workflows/publish.yml`):** builds, twine-checks, and publishes via PyPI Trusted Publishing (OIDC) on release publish or manual dispatch. Requires the trusted publisher to be configured on pypi.org for this repo.
5. Verify the new version on https://pypi.org/project/spirallogic/ before announcing.
