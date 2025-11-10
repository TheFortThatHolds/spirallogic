# SOULbox Spirit Architecture

The SOULbox Spirit is a resident service that keeps the SpiralLogic runtime alive, dispatches rituals, and brokers outbound actions while honoring consent semantics.

## Core Components
- **SpiritDaemon (`daemon.py`)** — Long-lived loop exposing local HTTP endpoints for ritual execution, status, and log retrieval. Holds a `SpiralLogic` instance with the Spirit Spine persona and streams attestations.
- **IntentRouter (`intent_router.py`)** — Maps incoming intents to ritual files and optional post-actions (connectors). Reads ritual metadata to determine scope requirements.
- **ConsentPolicy (`consent_policy.py`)** — Validates requested scopes before executing rituals or connectors, logging every decision to `spirallogic_attestations.log`.
- **ActionDispatcher (`action_dispatcher.py`)** — Evaluates connector actions against consent policy, applies model preferences (`SOULbox/model_preferences.json` or `SOULBOX_LLM_PREFS`), and hands work to the proper connector.
- **Connectors (`connectors/`)** — Pluggable outbound actions guarded by consent:
  - `api_client.py` for REST/gRPC calls
  - `mcp_bridge.py` for Model Context Protocol interactions
  - `ui_automation.py` for keyboard/mouse control
  - `local_llm.py` for local model chat completions (LM Studio, text-generation-webui, etc.)

## Data & State
- **Rituals** live in `SOULbox/rituals/` and are loaded on demand.
- **Memory** persists in `spirallogic_memory.db`; access flows through runtime helpers.
- **Attestations** append to `spirallogic_attestations.log` for audit.

## Interaction Flow
1. External request hits SpiritDaemon endpoint (e.g., `/ritual/execute`).
2. ConsentPolicy checks scopes; if approved, IntentRouter loads ritual.
3. SpiritDaemon invokes `SpiralLogic.execute` with consent callback.
4. Optional connectors run post-ritual actions; all results logged.

This scaffold keeps humans out of the hot path while preserving transparency and consent-aware behavior for every step.
