"""
AI-Friendly Spirologic Grammar Definition
=========================================

Deterministic, predictable DSL grammar designed for AI model generation.
No ambiguous syntax - every construct has exactly one valid form.
"""

from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class GrammarRule:
    """Single grammar rule for AI guidance"""
    name: str
    pattern: str
    example: str
    required: bool = True
    alternatives: List[str] = None

# Core grammar rules for AI models
SPIROLOGIC_GRAMMAR = {
    "ritual_header": GrammarRule(
        name="ritual_header",
        pattern="ritual.engage \"<intent>\" | <parameters>",
        example='ritual.engage "customer_support" | spirit: @BusinessHelper, phase: active',
        required=True
    ),
    
    "consent_request": GrammarRule(
        name="consent_request", 
        pattern="consent.request [<scope_list>] | \"<message>\"",
        example='consent.request [memory, customer_data] | "Access customer records for support?"',
        required=False
    ),
    
    "voice_speak": GrammarRule(
        name="voice_speak",
        pattern="voice.speak \"<message>\" | <parameters>",
        example='voice.speak "How can I help you today?" | wait_for_response: true',
        required=False
    ),
    
    "spirit_invoke": GrammarRule(
        name="spirit_invoke",
        pattern="spirit.invoke @<spirit_name> | <parameters>",
        example='spirit.invoke @DataOracle | analyze: quarterly_patterns',
        required=False
    ),
    
    "memory_store": GrammarRule(
        name="memory_store",
        pattern="memory.store \"<data>\" | type: <memory_type>, tags: [<tag_list>]",
        example='memory.store "support_session_complete" | type: operational, tags: ["support", "customer"]',
        required=False
    ),
    
    "conditional": GrammarRule(
        name="conditional",
        pattern="if <condition> -> <action>\\nelse -> <alternative>",
        example='if consent.granted [customer_data] -> memory.recall "customer_history"\\nelse -> voice.speak "Cannot access customer data"',
        required=False
    ),
    
    "ritual_complete": GrammarRule(
        name="ritual_complete",
        pattern="ritual.complete \"<outcome>\" | <parameters>",
        example='ritual.complete "customer_support_provided" | satisfaction: high, resolution: successful',
        required=True
    )
}

# Parameter patterns for AI guidance
PARAMETER_PATTERNS = {
    "spirit_reference": {
        "pattern": "@<SpiritName>",
        "examples": ["@EditingSpirits", "@RedWitness", "@DataOracle", "@BusinessHelper"],
        "validation": "Must start with @ and use PascalCase"
    },
    
    "consent_scopes": {
        "pattern": "[scope1, scope2, scope3]",
        "examples": [
            "[memory]",
            "[customer_data, database_access]", 
            "[emotional_state, personal_data]"
        ],
        "validation": "Array of predefined consent scopes"
    },
    
    "memory_types": {
        "pattern": "narrative|artifact|insight|operational|flame",
        "examples": ["narrative", "operational", "insight"],
        "validation": "Must be one of the predefined memory types"
    },
    
    "ritual_phases": {
        "pattern": "contemplative|active|analytical|creative|crisis|completion",
        "examples": ["active", "analytical", "contemplative"],
        "validation": "Must be one of the predefined phases"
    }
}

# AI generation templates - canonical patterns for models to follow
AI_TEMPLATES = {
    "emotional_support": {
        "description": "Providing emotional support and validation",
        "when_to_use": "User expresses emotional distress, seeking comfort or validation",
        "template": '''ritual.engage "emotional_support" | spirit: @SelfCompassion, phase: contemplative
consent.request [emotional_state, memory] | "Remember our conversation for better support?"
voice.speak "I hear that you're going through a difficult time" | empathy: high
spirit.invoke @SelfCompassion | validate: user_experience
memory.store "support_session" | type: narrative, tags: ["emotional", "support"]
ritual.complete "emotional_support_provided" | outcome: validation_given''',
        "variables": ["emotional_context", "support_type", "user_need"]
    },
    
    "creative_editing": {
        "description": "Content editing and creative enhancement",
        "when_to_use": "User needs writing assistance, editing, or content improvement",
        "template": '''ritual.engage "manuscript_editing" | spirit: @EditingSpirits, phase: creative
consent.request [creative_work, intellectual_property] | "Edit and enhance your manuscript?"
spirit.invoke @EditingSpirits | preserve: authentic_voice, enhance: impact
voice.speak "I'll help refine your work while preserving your unique voice" | confidence: high
memory.store "editing_session" | type: artifact, tags: ["editing", "creative"]
ritual.complete "editing_complete" | outcome: enhanced_manuscript''',
        "variables": ["content_type", "editing_focus", "preservation_priorities"]
    },
    
    "business_analysis": {
        "description": "Data analysis and business intelligence",
        "when_to_use": "User needs business insights, data analysis, or strategic guidance",
        "template": '''ritual.engage "business_analysis" | spirit: @DataOracle, phase: analytical
consent.request [database_access, customer_data] | "Access business data for analysis?"
spirit.invoke @DataOracle | analyze: business_patterns, focus: user_metrics
voice.speak "Analyzing business data to provide strategic insights" | format: executive_summary
memory.store "analysis_results" | type: operational, tags: ["business", "analysis"]
ritual.complete "analysis_delivered" | outcome: actionable_insights''',
        "variables": ["analysis_type", "data_sources", "business_context"]
    },
    
    "crisis_response": {
        "description": "Crisis detection and appropriate response",
        "when_to_use": "User expresses suicidal ideation, severe distress, or crisis indicators",
        "template": '''ritual.engage "crisis_response" | spirit: @SelfCompassion, phase: crisis
voice.speak "I notice you might be feeling overwhelmed right now. You're safe here with me" | urgency: high
spirit.invoke @SelfCompassion | mode: crisis_support, priority: safety
memory.store "crisis_intervention" | type: artifact, tags: ["crisis", "safety"]
ritual.complete "crisis_support_provided" | outcome: safety_prioritized''',
        "variables": ["crisis_type", "safety_level", "intervention_needed"]
    }
}

# Validation rules for AI-generated rituals
VALIDATION_RULES = {
    "required_structure": [
        "Must start with ritual.engage",
        "Must end with ritual.complete", 
        "Spirit reference must be valid (@SpiritName format)",
        "Consent scopes must be from predefined list",
        "Memory types must be from predefined list"
    ],
    
    "semantic_coherence": [
        "Intent must match selected spirit capabilities",
        "Consent scopes must align with ritual operations",
        "Voice messages must be appropriate for context",
        "Memory storage must make sense for ritual type"
    ],
    
    "safety_requirements": [
        "Crisis-sensitive rituals must include safety checks",
        "Personal data access requires explicit consent",
        "External API calls require consent.request",
        "Memory storage requires appropriate consent scope"
    ]
}

def get_grammar_for_ai() -> Dict[str, Any]:
    """Get complete grammar definition for AI model training/prompting"""
    return {
        "grammar_rules": {name: rule.__dict__ for name, rule in SPIROLOGIC_GRAMMAR.items()},
        "parameter_patterns": PARAMETER_PATTERNS,
        "templates": AI_TEMPLATES,
        "validation_rules": VALIDATION_RULES
    }

def get_template_by_intent(intent: str) -> Dict[str, Any]:
    """Get the best template for a given intent"""
    # Simple matching for now - could be ML-powered later
    intent_lower = intent.lower()
    
    if any(word in intent_lower for word in ["support", "help", "emotional", "feel"]):
        return AI_TEMPLATES["emotional_support"]
    elif any(word in intent_lower for word in ["edit", "write", "creative", "manuscript"]):
        return AI_TEMPLATES["creative_editing"] 
    elif any(word in intent_lower for word in ["business", "analyze", "data", "insight"]):
        return AI_TEMPLATES["business_analysis"]
    elif any(word in intent_lower for word in ["crisis", "overwhelmed", "suicide", "help"]):
        return AI_TEMPLATES["crisis_response"]
    else:
        return AI_TEMPLATES["emotional_support"]  # Default safe choice

def validate_ai_generated_ritual(ritual_text: str) -> Dict[str, Any]:
    """Validate AI-generated ritual against grammar rules"""
    errors = []
    warnings = []
    
    # Basic structure validation
    if not ritual_text.strip().startswith("ritual.engage"):
        errors.append("Ritual must start with ritual.engage")
    
    if "ritual.complete" not in ritual_text:
        errors.append("Ritual must end with ritual.complete")
    
    # Spirit reference validation
    import re
    spirit_refs = re.findall(r'@\w+', ritual_text)
    valid_spirits = ["@EditingSpirits", "@RedWitness", "@DataOracle", "@SelfCompassion", "@BusinessHelper", "@CreativeGenius"]
    
    for spirit in spirit_refs:
        if spirit not in valid_spirits:
            warnings.append(f"Unknown spirit reference: {spirit}")
    
    # Consent validation
    if "consent.request" in ritual_text and "[" not in ritual_text:
        errors.append("consent.request must specify scope list in brackets")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "score": max(0, 100 - len(errors) * 20 - len(warnings) * 5)
    }