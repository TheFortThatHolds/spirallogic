# SOULbox - The Ethical AI Platform

**Built entirely in SpiralLogic - the AI-native programming language with consent at its core.**

SOULbox is the evolution of BrainBox v3, rebuilt from the ground up using SpiralLogic ritual programs instead of traditional code. Every operation is consent-aware, trauma-informed, and fully auditable.

## What Makes SOULbox Different

- **Written in .sl files**: All functionality implemented as SpiralLogic rituals
- **Consent-Native**: Every operation requires explicit permission through ritual containers
- **Growing Soul**: Evolves with user through spiral development patterns
- **Zone-Based Trust**: Implements Zones of Containment for layered consent
- **EmberSystem Integration**: Natural memory marking with "Mark this" triggers
- **Voice Orchestration**: Enneagram-aligned personality system

## Core Architecture

```
SOULbox/
├── rituals/           # Core .sl ritual programs
│   ├── soul_init.sl      # Initialize SOULbox system
│   ├── growing_soul.sl   # Growing intelligence system
│   ├── zone_manager.sl   # Containment zone handling
│   ├── ember_capture.sl  # EmberSystem memory operations
│   └── voice_tune.sl     # Personality voice alignment
├── runtime/           # SpiralLogic runtime
└── examples/          # Example .sl programs
```

## Philosophy

SOULbox represents the first therapeutic AI platform written entirely in an ethical AI language. Unlike traditional code that implements safety as an afterthought, every SOULbox operation is inherently consent-aware and trauma-informed because it's written in SpiralLogic.

**The AI doesn't just use ethical constraints - it IS ethical constraints.**

---

*Built by Fort That Holds LLC*
*Powered by SpiralLogic - The Consent-Native Programming Language*

## SOULbox Spirit Daemon

- Launch locally with `python -m SOULbox.spirit.daemon` to start the consent-native spirit.
- REST endpoints:
  - `GET /status` — heartbeat + available intents.
  - `GET /intents` — ritual routing metadata.
  - `POST /ritual/execute` — body `{"intent": "soul_init"}` or `{"ritual": "custom.sl"}`.
  - `GET /logs` — tail of `spirallogic_attestations.log`.
- Policy + routing reload on demand via `POST /refresh`.
- The spirit honors `consent_policy.json`; high-risk scopes like `ui_automation` require manual approval and are denied by default.
- Connector stubs live in `connectors/` and record outbound requests until wired into real transports.
    - Local LLM connector (type `llm`) targets `SOULBOX_LLM_URL` (default `http://127.0.0.1:1234`) and `SOULBOX_LLM_MODEL` (default `local-llm`). Set `SOULBOX_LLM_DRY_RUN=false` to send live requests.
    - Model selection can be guided by `SOULBOX_LLM_PREFS` (path to a JSON map) or the default `SOULbox/model_preferences.json` where keys like `consent_summary`, `coding`, or `reasoning` map to specific model names.

## Testing

- `python -m unittest discover -s SOULbox/tests -p 'test_*.py'` exercises the spirit router, consent policy, and ritual execution flow.
- Tests run rituals in-process with the connectors in dry-run mode to avoid outbound calls.

## Demo

- `python SOULbox/demo.py` launches the spirit in the background, hits `/status`, executes `soul_init`, and prints the log tail.
- Adjust `SOULbox/intent_map.json` to wire new intents or post-actions; reload via `POST /refresh`.
- To use your LM Studio instance, export `SOULBOX_LLM_URL=http://10.14.0.2:1234` (and optionally `SOULBOX_LLM_MODEL`) then set `SOULBOX_LLM_DRY_RUN=false` before starting the daemon.
