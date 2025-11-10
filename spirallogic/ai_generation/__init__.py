"""
AI Generation Package for Spirologic
====================================

Tools and systems designed for AI models to autonomously generate
Spirologic rituals with proper validation and guidance.
"""

from .grammar import (
    SPIROLOGIC_GRAMMAR, PARAMETER_PATTERNS, AI_TEMPLATES, VALIDATION_RULES,
    get_grammar_for_ai, get_template_by_intent, validate_ai_generated_ritual
)

from .templates import (
    RitualTemplate, TEMPLATE_LIBRARY, 
    get_template_library, find_best_template, generate_ritual_from_template,
    get_ai_guidance_prompt
)

from .validator import (
    ValidationResult, SpiralLogicValidator,
    validate_ritual_for_ai
)

__all__ = [
    # Grammar and patterns
    'SPIROLOGIC_GRAMMAR', 'PARAMETER_PATTERNS', 'AI_TEMPLATES', 'VALIDATION_RULES',
    'get_grammar_for_ai', 'get_template_by_intent', 'validate_ai_generated_ritual',
    
    # Templates
    'RitualTemplate', 'TEMPLATE_LIBRARY',
    'get_template_library', 'find_best_template', 'generate_ritual_from_template',
    'get_ai_guidance_prompt',
    
    # Validation
    'ValidationResult', 'SpiralLogicValidator', 'validate_ritual_for_ai'
]

# Quick AI integration function
def generate_and_validate_ritual(user_input: str, intent: str = None) -> dict:
    """
    Complete AI workflow: find template, generate ritual, validate
    
    This is the main function AI systems should use for end-to-end
    ritual generation with built-in validation.
    """
    from .templates import find_best_template, generate_ritual_from_template
    from .validator import validate_ritual_for_ai
    
    # Find best template
    template = find_best_template(user_input, intent)
    
    # TODO: Extract variables from user input (would be ML-powered)
    # For now, use placeholder variables
    variables = {
        "intent": intent or "user_assistance",
        "validation_message": "I understand you need support",
        "support_approach": "empathetic",
        "session_description": "User assistance session",
        "emotion_tag": "general",
        "outcome_type": "support_provided"
    }
    
    # Generate ritual
    ritual_text = generate_ritual_from_template(template, variables)
    
    # Validate
    validation_result = validate_ritual_for_ai(ritual_text)
    
    return {
        "template_used": template.name,
        "generated_ritual": ritual_text,
        "validation": validation_result,
        "ready_for_execution": validation_result["valid"]
    }