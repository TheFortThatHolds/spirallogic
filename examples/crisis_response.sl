{
    "intent": "crisis_response",
    "voice": "@witness",
    "phase": "crisis",
    "steps": [
        {
            "type": "crisis.detect",
            "text": "I can't handle this anymore, I want to give up"
        },
        {
            "type": "voice.speak",
            "message": "I notice you might be feeling overwhelmed right now. You're safe here with me. Let's take this one breath at a time."
        },
        {
            "type": "memory.store",
            "data": "Crisis episode detected and responded to - user expressing overwhelm",
            "type_": "artifact"
        }
    ]
}