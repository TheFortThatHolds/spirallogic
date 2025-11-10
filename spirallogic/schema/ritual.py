"""
Spirologic Ritual Schema Definitions
===================================

Pydantic models for ritual structure validation and type safety.
The canonical contract that all parsers and runtimes must follow.
"""

from __future__ import annotations
from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field, validator
from enum import Enum
import uuid
from datetime import datetime

from .constants import StepType, ConsentScope, VoiceTag, RitualPhase, MemoryType, CrisisLevel

class RitualMetadata(BaseModel):
    """Ritual execution metadata"""
    ritual_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    version: str = "2.0.0"

class ConsentRequest(BaseModel):
    """Consent request structure"""
    scopes: List[ConsentScope]
    message: str
    timeout_ms: int = 30000
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    @validator('timeout_ms')
    def validate_timeout(cls, v):
        if v <= 0 or v > 600000:  # Max 10 minutes
            raise ValueError('Timeout must be between 1ms and 10 minutes')
        return v

class VoiceReference(BaseModel):
    """Reference to a voice family"""
    name: str  # e.g. "@EditingSpirits"
    capabilities: Optional[List[str]] = None
    context: Optional[Dict[str, Any]] = None
    
    @validator('name')
    def validate_voice_name(cls, v):
        if not v.startswith('@'):
            raise ValueError('Voice name must start with @')
        return v

class StepParameters(BaseModel):
    """Generic step parameters with validation"""
    # Common parameters
    voice: Optional[VoiceReference] = None
    spirit: Optional[VoiceReference] = None
    context: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    
    # Consent parameters
    scopes: Optional[List[ConsentScope]] = None
    message: Optional[str] = None
    timeout_ms: Optional[int] = None
    
    # Memory parameters
    data: Optional[str] = None
    memory_type: Optional[MemoryType] = None
    query: Optional[str] = None
    max_results: Optional[int] = None
    
    # Voice parameters
    wait_for_response: Optional[bool] = None
    format: Optional[str] = None
    confidence: Optional[str] = None
    
    # Conditional parameters
    condition: Optional[Dict[str, Any]] = None
    then_step: Optional[Dict[str, Any]] = None
    else_step: Optional[Dict[str, Any]] = None
    
    # Generic parameters for extensibility
    custom_params: Optional[Dict[str, Any]] = None

class RitualStep(BaseModel):
    """Single step in a ritual"""
    type: StepType
    parameters: StepParameters = Field(default_factory=StepParameters)
    
    # Execution metadata
    step_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    line: Optional[int] = None
    column: Optional[int] = None
    
    # Results (populated during execution)
    success: Optional[bool] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time_ms: Optional[float] = None

class ConditionalStep(RitualStep):
    """Conditional step with branching logic"""
    type: StepType = StepType.CONDITIONAL
    condition: Dict[str, Any]
    then_step: RitualStep
    else_step: Optional[RitualStep] = None

class RitualSchema(BaseModel):
    """Complete ritual definition and execution context"""
    # Core ritual definition
    intent: str
    voice: Optional[VoiceReference] = None
    spirit: Optional[VoiceReference] = None
    phase: RitualPhase = RitualPhase.ACTIVE
    steps: List[RitualStep]
    
    # Metadata
    metadata: RitualMetadata = Field(default_factory=RitualMetadata)
    
    # Execution context
    consent_granted: Dict[str, bool] = Field(default_factory=dict)
    memory_store: Dict[str, Any] = Field(default_factory=dict)
    artifacts: Dict[str, Any] = Field(default_factory=dict)
    crisis_active: bool = False
    crisis_level: CrisisLevel = CrisisLevel.NONE
    
    # Results
    execution_results: List[Dict[str, Any]] = Field(default_factory=list)
    overall_success: Optional[bool] = None
    completion_time: Optional[datetime] = None
    
    @validator('intent')
    def validate_intent(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Intent cannot be empty')
        return v.strip()
    
    @validator('steps')
    def validate_steps(cls, v):
        if not v:
            raise ValueError('Ritual must have at least one step')
        return v
    
    def add_step(self, step: RitualStep) -> None:
        """Add a step to the ritual"""
        self.steps.append(step)
    
    def get_required_consents(self) -> List[ConsentScope]:
        """Extract all consent scopes required by this ritual"""
        required = set()
        
        for step in self.steps:
            if step.parameters.scopes:
                required.update(step.parameters.scopes)
        
        return list(required)
    
    def get_voice_families(self) -> List[str]:
        """Get all voice families referenced in this ritual"""
        voices = set()
        
        if self.voice:
            voices.add(self.voice.name)
        if self.spirit:
            voices.add(self.spirit.name)
            
        for step in self.steps:
            if step.parameters.voice:
                voices.add(step.parameters.voice.name)
            if step.parameters.spirit:
                voices.add(step.parameters.spirit.name)
        
        return list(voices)
    
    def is_crisis_sensitive(self) -> bool:
        """Check if ritual involves crisis-sensitive operations"""
        crisis_steps = [
            StepType.CRISIS_DETECT,
            StepType.CRISIS_RESPOND,
            StepType.VOICE_SPEAK  # Voice operations can trigger crisis detection
        ]
        
        return any(step.type in crisis_steps for step in self.steps)

class RitualTemplate(BaseModel):
    """Reusable ritual template"""
    name: str
    description: str
    category: str
    default_voice: Optional[VoiceReference] = None
    required_scopes: List[ConsentScope]
    template_steps: List[Dict[str, Any]]
    variables: Optional[Dict[str, Any]] = None
    
    def instantiate(self, variables: Optional[Dict[str, Any]] = None) -> RitualSchema:
        """Create a ritual instance from this template"""
        # Template instantiation logic would go here
        # For now, return a basic ritual
        steps = [RitualStep(type=StepType.VOICE_SPEAK, parameters=StepParameters(
            message=f"Executing {self.name} ritual"
        ))]
        
        return RitualSchema(
            intent=self.name,
            voice=self.default_voice,
            steps=steps
        )

class ExecutionResult(BaseModel):
    """Result of ritual execution"""
    ritual_id: str
    success: bool
    results: List[Dict[str, Any]]
    context: Dict[str, Any]
    artifacts: Dict[str, Any] = Field(default_factory=dict)
    errors: List[str] = Field(default_factory=list)
    execution_time_ms: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Schema validation utilities
def validate_ritual_json(ritual_data: Dict[str, Any]) -> RitualSchema:
    """Validate and convert JSON ritual data to schema"""
    return RitualSchema(**ritual_data)

def ritual_to_dict(ritual: RitualSchema) -> Dict[str, Any]:
    """Convert ritual schema to dictionary"""
    return ritual.dict()

def step_to_dict(step: RitualStep) -> Dict[str, Any]:
    """Convert step to dictionary"""
    return step.dict()

# Schema migration utilities
def migrate_v1_to_v2(v1_ritual: Dict[str, Any]) -> RitualSchema:
    """Migrate old JSON format to new schema"""
    # Convert old format to new schema
    steps = []
    
    for old_step in v1_ritual.get('steps', []):
        step_type = StepType(old_step['type'])
        parameters = StepParameters()
        
        # Map old parameters to new structure
        if 'scopes' in old_step:
            parameters.scopes = [ConsentScope(scope) for scope in old_step['scopes']]
        if 'message' in old_step:
            parameters.message = old_step['message']
        if 'data' in old_step:
            parameters.data = old_step['data']
        if 'voice' in old_step:
            parameters.voice = VoiceReference(name=old_step['voice'])
        
        steps.append(RitualStep(type=step_type, parameters=parameters))
    
    return RitualSchema(
        intent=v1_ritual.get('intent', 'migrated_ritual'),
        voice=VoiceReference(name=v1_ritual['voice']) if v1_ritual.get('voice') else None,
        phase=RitualPhase(v1_ritual.get('phase', 'active')),
        steps=steps
    )