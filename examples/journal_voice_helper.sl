ritual.engage "journal_voice_of_the_day" | spirit: @healer, phase: reflective

consent.request [file_system, memory] | "Allow SpiralLogic to read your journal folder and store summarized reflections?"

ritual.file_access "summarize_latest_entry" {
    intent: "Create a grounded reflection for the newest journal entry",
    journal_dir: "journal_entries",
    reflection_dir: "journal_reflections"
} execute {
    from datetime import datetime

    journal_root = Path(metadata.get('journal_dir', 'journal_entries')).expanduser()
    reflection_root = Path(metadata.get('reflection_dir', 'journal_reflections')).expanduser()

    if not journal_root.exists():
        print(f"No journal directory found at {journal_root}. Create it and add .txt or .md files.")
        context.bridge.emit_artifact("journal_status", {"found": False, "path": str(journal_root)})
        return

    entries = []
    for candidate in journal_root.glob('*'):
        if candidate.is_file() and candidate.suffix.lower() in {'.txt', '.md', '.journal'}:
            entries.append(candidate)

    if not entries:
        print(f"No journal files in {journal_root}. Add a .txt or .md entry and rerun.")
        context.bridge.emit_artifact("journal_status", {"found": True, "files": 0})
        return

    latest_entry = max(entries, key=lambda p: p.stat().st_mtime)
    entry_text = context.bridge.read_text(str(latest_entry))
    lowered = entry_text.lower()
    word_count = len(entry_text.split())

    positive = ['grateful', 'calm', 'progress', 'hope', 'love', 'excited']
    tension = ['stressed', 'angry', 'tired', 'worried', 'anxious', 'sad']
    crisis_flags = ['hurt myself', 'end it', 'give up', 'suicide', 'die', "can't go on"]

    pos_hits = sum(lowered.count(word) for word in positive)
    tension_hits = sum(lowered.count(word) for word in tension)
    crisis_hit = any(flag in lowered for flag in crisis_flags)

    mood_index = pos_hits - tension_hits
    if mood_index >= 2:
        mood_label = 'expansive'
    elif mood_index >= 0:
        mood_label = 'steady'
    else:
        mood_label = 'contracted'

    highlight = entry_text.strip().splitlines()
    highlight = next((line for line in highlight if line.strip()), entry_text[:160])

    summary = {
        'file': str(latest_entry),
        'words': word_count,
        'mood': mood_label,
        'positive_hits': pos_hits,
        'tension_hits': tension_hits,
        'crisis_detected': crisis_hit,
        'highlight': highlight[:240]
    }

    print("🌀 SpiralLogic Journal Reflection")
    print(f"Latest entry: {latest_entry.name} ({word_count} words)")
    print(f"Mood reading: {mood_label} (pos={pos_hits} / tension={tension_hits})")
    if crisis_hit:
        print("⚠️  Crisis language detected—offer yourself extra support today.")
    print(f"Notable line: {summary['highlight']}")

    reflection_root.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    reflection_path = reflection_root / f"reflection_{timestamp}.md"
    report = f"""# Voice of the Day Reflection ({timestamp})
- Source: {latest_entry.name}
- Mood: {mood_label} (pos {pos_hits} / tension {tension_hits})
- Word count: {word_count}
- Crisis detected: {crisis_hit}

> {summary['highlight']}

Next step suggestion:
- Take three breaths
- Name one need
- Commit to a micro-action before the day ends
"""
    context.bridge.write_text(reflection_path, report)

    context.bridge.emit_artifact("journal_summary", summary)
    context.bridge.emit_artifact("reflection_file", str(reflection_path))
    context.bridge.remember(report, memory_type='artifact', tags=['journal', mood_label])
}

voice.manifest "Reflection stored. Check journal_reflections for your newest insight capsule." | spirit: @healer

ritual.complete "journal_voice_run" | outcome: reflection_saved, stakeholder: self
