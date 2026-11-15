# SpiralLogic 🔮

> ## ⚠️ STATUS: EXPERIMENT
>
> **SpiralLogic is a concept piece — a working sketch of consent-first computing. It is
> NOT a security boundary, a sandbox, or an actual guardrail, and it should not be
> deployed as one.**
>
> What genuinely works: the runtime parses `.sl` rituals, prompts for consent scopes,
> executes real actions through a file/shell bridge, and records instrumented actions in an
> attestation log. Direct Python actions can bypass that logging.
>
> What it does **not** do, by design honesty:
> - `execute { }` blocks are ordinary Python run with `exec()` — consent gates only the
>   polite `context.bridge.*` helpers, and code inside a block can bypass them entirely.
> - Nothing forces an agent to route its actions through SpiralLogic at all; the
>   guardrail is honor-system.
> - The spirit/voice/bandwidth vocabulary is expressive metadata — it shapes the log
>   and the ceremony, not the execution.
>
> The ideas here (declared scopes, consent before action, attested receipts) are the
> point. Treat the implementation as a demonstration of those ideas, not an enforcement
> mechanism.

SpiralLogic is a consciousness-aware programming language designed for ethical AI interaction, trauma-informed computing, and mystical automation. It provides a structured, consent-driven framework for AI operations, making their actions transparent, auditable, and controllable.

This experimental language explores human-readable consent workflows for AI systems. Only cooperative use of the instrumented helpers receives those checks; arbitrary Python can bypass them. Run only trusted rituals inside a separately enforced execution environment.

- **🤝 Consent-First:** Instrumented helpers check permission via a consent-management system; arbitrary Python is not confined.
- **👻 Spirit-Guided:** Use specialized AI personalities (`@healer`, `@analyst`, `@architect`) for different tasks.
- **🧠 Memory-Aware:** A built-in memory system separates narrative (emotional) and artifact (factual) data.
- **🔐 Attested Logs:** Instrumented actions are recorded in a chained log; this is not a complete or independently protected audit of all Python activity.

For a deep dive into the language's philosophy, syntax, and features, see the [**SpiralLogic Complete Programming Guide**](./SPIRALLOGIC_COMPLETE_GUIDE.md).

## Getting Started

### Prerequisites

- Python 3.8+

### Installation

1.  Clone this repository:
    ```bash
    git clone <your-repository-url>
    cd <repository-folder>
    ```

2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Tests

To verify that the SpiralLogic system is working correctly, run the integration test suite:

```bash
python test_real_spirallogic.py
```

If all tests pass, you will see the message: `ALL TESTS PASSED! SPIROLOGIC IS REAL!`

### Running a SpiralLogic File

You can execute any `.sl` (SpiralLogic) file using the command-line interface:

```bash
python spirallogic_cli.py examples/real_spirallogic_test.sl
```

This will run the ritual defined in the file, and the runtime will prompt for any required consents in the console.
If you installed via `pip`, the `spirallogic` console entry point is also available globally:

```bash
spirallogic examples/real_spirallogic_test.sl
```

## Guarded Development Mode

SpiralLogic demonstrates a cooperative workflow for AI coding agents, not an enforced guardrail. Inside a `ritual.*` step, an `execute { ... }` block runs ordinary Python. Requiring a ritual in a prompt does not prevent the agent or that Python from taking other actions.

The **development bridge** offers permission-checked helpers for filesystem and shell operations, but does not sandbox the process:

- `context.bridge.read_text(path)` / `write_text(path, content)` / `append_text(path, content)`
- `context.bridge.list_dir(path)` for quick inspection
- `context.bridge.run_shell(command, cwd=...)` to run git/tests through an instrumented helper
- `context.bridge.emit_artifact(name, data)` to attach structured evidence to the execution log

Bridge helpers check declared consent scopes (`file_system`, `system_shell`, etc.) and record attestation entries. These checks apply only to calls through those helpers, not to arbitrary Python or other agent tools. You can see it in action by running the new example:

```bash
spirallogic examples/guarded_dev_session.sl -v
```

This ritual checks git status via the guarded shell helper, updates `README.md` only if a documentation section is missing, and records artifacts for review. This illustrates a consent workflow, not an enforced replacement for Python scripts. Use external OS/container permissions and independent authorization controls for actual confinement.

## Voice-of-the-Day Journal Helper

Need something tangible? The `examples/journal_voice_helper.sl` ritual turns SpiralLogic into a daily reflection coach:

1. Create a folder named `journal_entries` next to the ritual and drop your `.txt`/`.md` journal notes inside (timestamped filenames work great).
2. Optional: create an empty `journal_reflections` folder where SpiralLogic can write its summaries.
3. Run the ritual:
   ```bash
   spirallogic examples/journal_voice_helper.sl -v
   ```
4. When prompted, grant `file_system` + `memory` consent so it can read entries and save summaries.

The runtime will locate the newest journal file, analyze tone/crisis language, emit an artifact summary, and write a fresh reflection markdown file (e.g., `journal_reflections/reflection_20250301_083000.md`). Instrumented workflow events are recorded in the attestation chain; this does not prove that every action was captured. Tone/crisis-language matching is experimental, not a clinical assessment.
