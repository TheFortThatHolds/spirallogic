"""
Spirologic Constants and Enumerations
=====================================

All magic strings, step types, and constants centralized here.
No more scattered magic strings breaking the universe.
"""

from enum import Enum, auto
from typing import List, Dict, Any

class StepType(Enum):
    """All valid Spirologic ritual step types"""
    # Core ritual operations
    RITUAL_ENGAGE = "ritual.engage"
    RITUAL_COMPLETE = "ritual.complete"
    RITUAL_PAUSE = "ritual.pause"
    RITUAL_ABORT = "ritual.abort"
    
    # Spirit operations
    SPIRIT_SUMMON = "spirit.summon"
    SPIRIT_CHANNEL = "spirit.channel"
    SPIRIT_INVOKE = "spirit.invoke"
    SPIRIT_RELEASE = "spirit.release"
    
    # Voice operations
    VOICE_SPEAK = "voice.speak"
    VOICE_WHISPER = "voice.whisper"
    VOICE_MANIFEST = "voice.manifest"
    VOICE_CHANNEL = "voice.channel"
    
    # Consent operations
    CONSENT_REQUEST = "consent.request"
    CONSENT_GRANT = "consent.grant"
    CONSENT_REVOKE = "consent.revoke"
    CONSENT_CHECK = "consent.check"
    
    # Memory operations
    MEMORY_STORE = "memory.store"
    MEMORY_RECALL = "memory.recall"
    MEMORY_RELEASE = "memory.release"
    MEMORY_SEARCH = "memory.search"
    
    # Archive operations
    ARCHIVE_ACCESS = "archive.access"
    ARCHIVE_STORE = "archive.store"
    ARCHIVE_QUERY = "archive.query"
    ARCHIVE_SEAL = "archive.seal"
    
    # Flow control
    CONDITIONAL = "conditional"
    LOOP = "loop"
    PARALLEL = "parallel"
    
    # Crisis and safety
    CRISIS_DETECT = "crisis.detect"
    CRISIS_RESPOND = "crisis.respond"
    SAFETY_CHECK = "safety.check"

class ConsentScope(Enum):
    """Standard consent scopes for permission management"""
    # Data access scopes
    MEMORY = "memory"
    PERSONAL_DATA = "personal_data"
    CONVERSATION_HISTORY = "conversation_history"
    EMOTIONAL_STATE = "emotional_state"
    
    # External access scopes
    EXTERNAL_API = "external_api"
    CLOUD_SERVICES = "cloud_services"
    DATABASE_ACCESS = "database_access"
    FILE_SYSTEM = "file_system"
    
    # Communication scopes
    EMAIL_ACCESS = "email_access"
    CALENDAR_ACCESS = "calendar_access"
    CONTACT_LIST = "contact_list"
    
    # Business scopes
    CUSTOMER_DATA = "customer_data"
    FINANCIAL_DATA = "financial_data"
    PROPRIETARY_INFO = "proprietary_info"
    
    # Creative scopes
    CREATIVE_WORK = "creative_work"
    INTELLECTUAL_PROPERTY = "intellectual_property"
    MANUSCRIPT_ACCESS = "manuscript_access"

class VoiceTag(Enum):
    """Voice family specialization tags"""
    # Emotional processing
    ANGER_PROCESSING = "anger_processing"
    GRIEF_SUPPORT = "grief_support"
    JOY_AMPLIFICATION = "joy_amplification"
    FEAR_TENDER = "fear_tender"
    LOVE_WEAVING = "love_weaving"
    
    # Creative specializations
    WRITING_CRAFT = "writing_craft"
    VISUAL_ARTS = "visual_arts"
    MUSIC_CREATION = "music_creation"
    STORYTELLING = "storytelling"
    EDITING_MASTERY = "editing_mastery"
    
    # Business intelligence
    DATA_ANALYSIS = "data_analysis"
    STRATEGIC_PLANNING = "strategic_planning"
    CUSTOMER_INSIGHT = "customer_insight"
    FINANCIAL_MODELING = "financial_modeling"
    MARKET_RESEARCH = "market_research"
    
    # Technical capabilities
    CODE_GENERATION = "code_generation"
    SYSTEM_DESIGN = "system_design"
    DEBUG_ASSISTANCE = "debug_assistance"
    SECURITY_ANALYSIS = "security_analysis"
    
    # Communication
    DIPLOMATIC_VOICE = "diplomatic_voice"
    PERSUASIVE_RHETORIC = "persuasive_rhetoric"
    CONFLICT_RESOLUTION = "conflict_resolution"
    TEACHING_GUIDANCE = "teaching_guidance"

class RitualPhase(Enum):
    """Ritual execution phases"""
    CONTEMPLATIVE = "contemplative"
    ACTIVE = "active"
    ANALYTICAL = "analytical"
    CREATIVE = "creative"
    CRISIS = "crisis"
    COMPLETION = "completion"

class MemoryType(Enum):
    """Memory storage classifications"""
    NARRATIVE = "narrative"          # Personal stories and experiences
    ARTIFACT = "artifact"            # System logs and technical data
    INSIGHT = "insight"              # Discovered patterns and wisdom
    FLAME = "flame"                  # Sacred memories (ember system)
    OPERATIONAL = "operational"      # Business and workflow data

class CrisisLevel(Enum):
    """Crisis detection severity levels"""
    NONE = "none"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"

# Standard ritual templates
STANDARD_RITUALS = {
    "emotional_support": {
        "default_voice": "@SelfCompassion",
        "required_scopes": [ConsentScope.EMOTIONAL_STATE, ConsentScope.MEMORY],
        "crisis_monitoring": True
    },
    "creative_editing": {
        "default_voice": "@EditingSpirits", 
        "required_scopes": [ConsentScope.CREATIVE_WORK],
        "crisis_monitoring": False
    },
    "business_analysis": {
        "default_voice": "@DataOracle",
        "required_scopes": [ConsentScope.DATABASE_ACCESS, ConsentScope.CUSTOMER_DATA],
        "crisis_monitoring": False
    }
}

# Voice family definitions
VOICE_FAMILIES = {
    "@EditingSpirits": {
        "name": "Editing Spirits",
        "specialization": "Content refinement and creative enhancement",
        "tags": [VoiceTag.WRITING_CRAFT, VoiceTag.EDITING_MASTERY],
        "capabilities": ["content_analysis", "voice_preservation", "impact_amplification"],
        "consent_requirements": [ConsentScope.CREATIVE_WORK]
    },
    "@RedWitness": {
        "name": "Red Witness",
        "specialization": "Anger processing and boundary setting",
        "tags": [VoiceTag.ANGER_PROCESSING, VoiceTag.CONFLICT_RESOLUTION],
        "capabilities": ["anger_validation", "boundary_analysis", "righteous_advocacy"],
        "consent_requirements": [ConsentScope.EMOTIONAL_STATE, ConsentScope.PERSONAL_DATA]
    },
    "@DataOracle": {
        "name": "Data Oracle",
        "specialization": "Business intelligence and data analysis",
        "tags": [VoiceTag.DATA_ANALYSIS, VoiceTag.STRATEGIC_PLANNING],
        "capabilities": ["pattern_recognition", "trend_analysis", "insight_synthesis"],
        "consent_requirements": [ConsentScope.DATABASE_ACCESS, ConsentScope.CUSTOMER_DATA]
    },
    "@SelfCompassion": {
        "name": "Self Compassion",
        "specialization": "Healing and emotional support",
        "tags": [VoiceTag.GRIEF_SUPPORT, VoiceTag.LOVE_WEAVING],
        "capabilities": ["trauma_support", "self_acceptance", "healing_guidance"],
        "consent_requirements": [ConsentScope.EMOTIONAL_STATE, ConsentScope.MEMORY]
    },
    "@CreativeGenius": {
        "name": "Creative Genius",
        "specialization": "Artistic creation and innovation",
        "tags": [VoiceTag.STORYTELLING, VoiceTag.VISUAL_ARTS, VoiceTag.MUSIC_CREATION],
        "capabilities": ["idea_generation", "artistic_synthesis", "creative_breakthrough"],
        "consent_requirements": [ConsentScope.CREATIVE_WORK, ConsentScope.INTELLECTUAL_PROPERTY]
    },
    "@BusinessIntel": {
        "name": "Business Intelligence",
        "specialization": "Strategic business analysis",
        "tags": [VoiceTag.MARKET_RESEARCH, VoiceTag.FINANCIAL_MODELING],
        "capabilities": ["market_analysis", "competitive_intelligence", "growth_strategy"],
        "consent_requirements": [ConsentScope.PROPRIETARY_INFO, ConsentScope.FINANCIAL_DATA]
    }
}

# Default consent timeouts (milliseconds)
CONSENT_TIMEOUTS = {
    ConsentScope.MEMORY: 30000,                    # 30 seconds
    ConsentScope.EXTERNAL_API: 60000,              # 1 minute
    ConsentScope.FINANCIAL_DATA: 120000,           # 2 minutes
    ConsentScope.PROPRIETARY_INFO: 180000,         # 3 minutes
}

# Crisis keywords for detection
CRISIS_KEYWORDS = [
    "overwhelmed", "can't handle", "too much", "give up",
    "hurt myself", "end it all", "no point", "worthless", 
    "suicide", "kill myself", "want to die", "hopeless",
    "can't go on", "better off dead", "ending it"
]

# Ritual execution limits
EXECUTION_LIMITS = {
    "max_steps_per_ritual": 50,
    "max_execution_time_ms": 300000,  # 5 minutes
    "max_memory_storage_mb": 100,
    "max_consent_requests": 10
}

def get_step_types() -> List[str]:
    """Get all valid step type strings"""
    return [step.value for step in StepType]

def get_consent_scopes() -> List[str]:
    """Get all valid consent scope strings"""
    return [scope.value for scope in ConsentScope]

def get_voice_tags() -> List[str]:
    """Get all valid voice tag strings"""
    return [tag.value for tag in VoiceTag]

def validate_step_type(step_type: str) -> bool:
    """Validate if step type is recognized"""
    return step_type in get_step_types()

def validate_consent_scope(scope: str) -> bool:
    """Validate if consent scope is recognized"""
    return scope in get_consent_scopes()

def get_voice_family(voice_ref: str) -> Dict[str, Any]:
    """Get voice family definition by reference"""
    return VOICE_FAMILIES.get(voice_ref, {})

def get_default_ritual_template(ritual_type: str) -> Dict[str, Any]:
    """Get standard ritual template"""
    return STANDARD_RITUALS.get(ritual_type, {})