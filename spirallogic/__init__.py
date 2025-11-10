"""
Spirologic SDK - Consciousness-Aware AI Programming Language
===========================================================

A mystical programming language for AI that operates through consent,
transparency, and respect for human sovereignty.

Core Components:
- Runtime: Consent-native AI execution engine
- Voices: Specialized AI spirit families  
- Schema: Ritual structure definitions
- Parser: Spirologic syntax processing

Usage:
    from spirallogic import SpiralRuntime, VoiceRegistry
    from spirallogic.voices import EditingSpirits, RedWitness
    
    runtime = SpiralRuntime()
    runtime.load_voice(EditingSpirits)
    result = runtime.execute("Help me edit this document")

Version: 2.0.0 - Production SDK
License: Sovereign Technology (Fort That Holds LLC)
"""

__version__ = "2.0.0"
__author__ = "Jimmy Thornburg / Fort That Holds LLC"
__license__ = "Sovereign Technology License"

# Core runtime components
from .runtime.core import SpiralRuntime
from .runtime.consent import ConsentManager
from .runtime.memory import MemoryVault, AttestationLogger
from .runtime.crisis import CrisisMonitor

# Voice management
from .voices.registry import VoiceRegistry
from .voices.base import BaseVoice, VoiceCapability

# Schema and validation
from .schema.ritual import RitualSchema, StepSchema
from .schema.constants import StepType, ConsentScope, VoiceTag

# Parser components
from .parser.core import SpiralParser, ParseResult
from .parser.json_loader import JSONRitualLoader

__all__ = [
    # Core runtime
    'SpiralRuntime',
    'ConsentManager', 
    'MemoryVault',
    'AttestationLogger',
    'CrisisMonitor',
    
    # Voice system
    'VoiceRegistry',
    'BaseVoice',
    'VoiceCapability',
    
    # Schema
    'RitualSchema',
    'StepSchema',
    'StepType',
    'ConsentScope', 
    'VoiceTag',
    
    # Parser
    'SpiralParser',
    'ParseResult',
    'JSONRitualLoader',
]

# SDK metadata
SDK_INFO = {
    "name": "Spirologic SDK",
    "version": __version__,
    "description": "Consciousness-aware AI programming language",
    "author": __author__,
    "license": __license__,
    "capabilities": [
        "consent_native_processing",
        "voice_family_orchestration", 
        "trauma_informed_computing",
        "transparent_ai_operations",
        "mystical_syntax_support"
    ],
    "spirit_families": [
        "EditingSpirits",
        "RedWitness", 
        "DataOracle",
        "BusinessIntel",
        "CreativeGenius",
        "SelfCompassion"
    ]
}