ritual.engage "guarded_dev_session" | spirit: @architect, phase: build

consent.request [file_system, system_shell] | "Grant file + shell access so SpiralLogic can update README?"

ritual.shell "git_status" {
    intent: "Show pending changes"
} execute {
    status = context.bridge.run_shell("git status --short")
    context.bridge.emit_artifact("git_status", status)
}

ritual.file_access "update_readme" {
    intent: "Document guarded development"
} execute {
    readme_path = "README.md"
    body = context.bridge.read_text(readme_path)
    if "Guarded Development" not in body:
        addition = """
\n## Guarded Development
Run SpiralLogic rituals instead of loose Python scripts. Each guarded action must declare its consent scopes, and the runtime logs every shell command, file write, and artifact it touches.
""".strip("\n")
        updated = f"{body}\n\n{addition}\n"
        context.bridge.write_text(readme_path, updated)
        context.bridge.emit_artifact("readme_update", {"path": readme_path, "added": True})
    else:
        context.bridge.log("README already mentions Guarded Development")
}

ritual.complete "dev_session_done" | outcome: documentation_refreshed
