"""
Spirologic Schema Package
========================

Schema definitions, constants, and validation for Spirologic rituals.
Provides the canonical contract for AI-generated rituals.
"""

from .constants import (
    StepType, ConsentScope, VoiceTag, RitualPhase, MemoryType, CrisisLevel,
    VOICE_FAMILIES, STANDARD_RITUALS, CRISIS_KEYWORDS,
    get_step_types, get_consent_scopes, get_voice_tags,
    validate_step_type, validate_consent_scope, get_voice_family
)

from .ritual import (
    RitualSchema, RitualStep, StepParameters, ConsentRequest, 
    VoiceReference, RitualTemplate, ExecutionResult,
    validate_ritual_json, ritual_to_dict, step_to_dict,
    migrate_v1_to_v2
)

__all__ = [
    # Constants and enums
    'StepType', 'ConsentScope', 'VoiceTag', 'RitualPhase', 
    'MemoryType', 'CrisisLevel',
    'VOICE_FAMILIES', 'STANDARD_RITUALS', 'CRISIS_KEYWORDS',
    
    # Schema models
    'RitualSchema', 'RitualStep', 'StepParameters', 'ConsentRequest',
    'VoiceReference', 'RitualTemplate', 'ExecutionResult',
    
    # Utility functions
    'get_step_types', 'get_consent_scopes', 'get_voice_tags',
    'validate_step_type', 'validate_consent_scope', 'get_voice_family',
    'validate_ritual_json', 'ritual_to_dict', 'step_to_dict',
    'migrate_v1_to_v2'
]