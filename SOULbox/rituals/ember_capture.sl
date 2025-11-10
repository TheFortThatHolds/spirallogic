{
    "intent": "ember_system_capture",
    "voice": "@witness", 
    "phase": "active",
    "steps": [
        {
            "type": "ember.detect",
            "trigger_phrases": ["mark this", "ember this", "put a flame on it", "save this part", "that's important"],
            "context_window": "current_conversation_segment"
        },
        {
            "type": "consent.request",
            "scopes": ["memory", "ember_storage"],
            "message": "I hear you want to mark this moment as important. May I create an Ember - a save-point of this context, emotion, and insight?"
        },
        {
            "type": "ember.create",
            "timestamp": "auto_generate",
            "tags": ["user_marked", "important_moment", "context_preservation"],
            "content": "extract_from_conversation_context"
        },
        {
            "type": "voice.speak", 
            "message": "🔥 Ember created. This moment is now held safely in your SOULbox memory vault, tagged and searchable for future reflection."
        },
        {
            "type": "memory.store",
            "data": "Ember captured via user trigger phrase - important moment preserved",
            "type_": "ember",
            "searchable": true,
            "user_controlled": true
        },
        {
            "type": "voice.speak",
            "message": "Your Embers create a constellation of meaningful moments. Each one is a beacon you can return to whenever you need."
        }
    ]
}