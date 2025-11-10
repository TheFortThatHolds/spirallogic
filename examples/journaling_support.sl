{
    "intent": "journaling_support",
    "voice": "@healer",
    "phase": "contemplative",
    "steps": [
        {
            "type": "consent.request",
            "scopes": ["memory"],
            "message": "I'd like to remember your journaling patterns to provide better support over time. Is that okay?"
        },
        {
            "type": "voice.speak",
            "message": "Let's create a safe space for your thoughts. What's been on your mind today?"
        },
        {
            "type": "memory.store",
            "data": "User initiated journaling session - seeking emotional processing space",
            "type_": "narrative"
        }
    ]
}