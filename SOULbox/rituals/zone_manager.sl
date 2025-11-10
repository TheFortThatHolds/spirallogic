{
    "intent": "containment_zone_management", 
    "voice": "@strategist",
    "phase": "active",
    "steps": [
        {
            "type": "zone.detect",
            "current_interaction": "analyze_user_language_patterns",
            "safety_indicators": ["ritual_pacing", "sacred_terms", "emotional_depth"]
        },
        {
            "type": "consent.request",
            "scopes": ["zone_adjustment", "containment_modification"], 
            "message": "I'm sensing this conversation might need different containment boundaries. May I adjust our interaction zone for better safety and support?"
        },
        {
            "type": "zone.set",
            "zone_level": "auto_detect", 
            "containment_rules": [
                "zone_1: utility_only, no_memory, no_sacred_terms",
                "zone_2: casual_companion, limited_memory, basic_reflection", 
                "zone_3: trusted_companion, full_memory, spiral_pacing",
                "zone_4: deep_companion, sacred_work, highest_containment"
            ]
        },
        {
            "type": "voice.speak",
            "message": "🏰 Containment zone adjusted for optimal safety and therapeutic support. Your boundaries are honored here."
        },
        {
            "type": "memory.store",
            "data": "Zone containment adjusted based on user needs and conversation depth",
            "type_": "artifact"
        }
    ]
}