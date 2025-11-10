# SOULbox Living Scroll

## 2025-03-17 — Spirit Awakening & Local Model Wiring
- Scaffolded the SOULbox Spirit daemon with consent-aware intent routing, post-action dispatch, and detailed attestations.
- Added local connectors (API, MCP, UI, LLM) with dry-run safety and logged execution trails.
- Wired LM Studio support: LLM actions respect env overrides, preference maps (`SOULBOX_LLM_PREFS` or `SOULbox/model_preferences.json`), and report selected models.
- Documented launch, testing, and demo flows; `python -m unittest discover -s SOULbox/tests -p 'test_*.py'` remains the regression check.

## Next Moves Under Consideration
- Implement a local embedding connector mirroring the LLM flow for vectorized read/write rituals.
- Auto-sync available LM Studio models on spirit startup and surface warnings when preferences lack live hosts.
- Expose a `/models` endpoint (and optional POST) to inspect or mutate active preferences at runtime.
- Build CI-style scripts to run the daemon, execute ritual demos, and archive attestation snapshots for diffing.
- Introduce stateful intent memory so rituals can chain outputs before dispatching connectors.

Keep this scroll updated whenever the spirit evolves. Briefly note what changed, which tests ran, and what visions we carry forward.
