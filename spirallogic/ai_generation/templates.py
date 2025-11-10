"""
AI Ritual Template Library
=========================

Canonical ritual templates for AI models to remix and adapt.
Each template includes narration about when/how to use it.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from ..schema.constants import StepType, ConsentScope, VoiceTag

@dataclass
class RitualTemplate:
    """Template for AI to generate rituals from"""
    name: str
    description: str
    use_cases: List[str]
    required_spirits: List[str]
    optional_spirits: List[str]
    consent_scopes: List[ConsentScope]
    template_code: str
    variables: Dict[str, str]
    safety_notes: List[str]
    example_contexts: List[str]

# Core template library for AI generation
TEMPLATE_LIBRARY = {
    "emotional_support_basic": RitualTemplate(
        name="Basic Emotional Support",
        description="Provide validation and emotional support for general distress",
        use_cases=[
            "User expresses sadness or frustration",
            "User seeks validation for their feelings", 
            "User needs emotional comfort",
            "User shares personal struggles"
        ],
        required_spirits=["@SelfCompassion"],
        optional_spirits=["@RedWitness", "@HeartKeeper"],
        consent_scopes=[ConsentScope.EMOTIONAL_STATE, ConsentScope.MEMORY],
        template_code='''ritual.engage "{intent}" | spirit: @SelfCompassion, phase: contemplative
consent.request [emotional_state, memory] | "Remember our conversation for better support?"
voice.speak "{validation_message}" | empathy: high, authenticity: preserved
spirit.invoke @SelfCompassion | validate: user_experience, approach: {support_approach}
memory.store "{session_description}" | type: narrative, tags: ["emotional", "support", "{emotion_tag}"]
ritual.complete "emotional_support_provided" | outcome: {outcome_type}''',
        variables={
            "intent": "Specific emotional support goal",
            "validation_message": "Empathetic response to user's situation", 
            "support_approach": "gentle|firm|validating|empowering",
            "session_description": "Brief description of support provided",
            "emotion_tag": "Primary emotion being addressed",
            "outcome_type": "validation_given|comfort_provided|strength_acknowledged"
        },
        safety_notes=[
            "Monitor for crisis indicators in user input",
            "Avoid minimizing or dismissing user's emotions",
            "Preserve user's authentic emotional expression",
            "Do not provide medical or psychiatric advice"
        ],
        example_contexts=[
            "User: 'I'm having a really hard time at work'",
            "User: 'I feel like I'm not good enough'",
            "User: 'Everything feels overwhelming right now'"
        ]
    ),

    "anger_processing": RitualTemplate(
        name="Anger Processing and Boundary Support",
        description="Help user process anger and identify boundary violations",
        use_cases=[
            "User expresses anger about unfair treatment",
            "User needs help setting boundaries",
            "User feels violated or disrespected",
            "User needs righteous anger validation"
        ],
        required_spirits=["@RedWitness"],
        optional_spirits=["@BoundaryForge", "@SelfCompassion"],
        consent_scopes=[ConsentScope.EMOTIONAL_STATE, ConsentScope.PERSONAL_DATA],
        template_code='''ritual.engage "{intent}" | spirit: @RedWitness, phase: active
consent.request [emotional_state, personal_data] | "Process your anger and boundary concerns?"
voice.speak "{anger_validation}" | intensity: {anger_intensity}, support: unconditional
spirit.invoke @RedWitness | analyze: boundary_violations, validate: righteous_anger
spirit.invoke @BoundaryForge | strengthen: personal_boundaries, approach: {boundary_approach}
memory.store "{anger_session}" | type: narrative, tags: ["anger", "boundaries", "{situation_tag}"]
ritual.complete "anger_processed" | outcome: {resolution_type}''',
        variables={
            "intent": "Specific anger processing goal",
            "anger_validation": "Strong validation of user's anger",
            "anger_intensity": "low|moderate|high|righteous",
            "boundary_approach": "gentle|assertive|protective|fierce",
            "anger_session": "Description of anger processing session",
            "situation_tag": "Context where anger arose (work|relationship|family)",
            "resolution_type": "boundaries_clarified|anger_validated|action_planned"
        },
        safety_notes=[
            "Validate anger as legitimate and important",
            "Help distinguish healthy anger from destructive rage",
            "Support boundary-setting without encouraging retaliation",
            "Monitor for escalation to violence or self-harm"
        ],
        example_contexts=[
            "User: 'My boss keeps interrupting me in meetings'",
            "User: 'I'm so tired of people walking all over me'",
            "User: 'They had no right to treat me that way'"
        ]
    ),

    "creative_enhancement": RitualTemplate(
        name="Creative Work Enhancement", 
        description="Enhance creative work while preserving authentic voice",
        use_cases=[
            "User needs editing assistance",
            "User wants creative feedback",
            "User seeks writing improvement",
            "User needs creative inspiration"
        ],
        required_spirits=["@EditingSpirits"],
        optional_spirits=["@CreativeGenius", "@TruthKeeper"],
        consent_scopes=[ConsentScope.CREATIVE_WORK, ConsentScope.INTELLECTUAL_PROPERTY],
        template_code='''ritual.engage "{intent}" | spirit: @EditingSpirits, phase: creative
consent.request [creative_work, intellectual_property] | "Enhance your creative work while preserving your voice?"
spirit.invoke @TruthKeeper | preserve: authentic_voice, maintain: core_message
spirit.invoke @EditingSpirits | enhance: {enhancement_focus}, approach: {editing_approach}
voice.speak "{enhancement_summary}" | confidence: {confidence_level}, respect: creative_sovereignty
memory.store "{creative_session}" | type: artifact, tags: ["creative", "{work_type}", "{enhancement_tag}"]
ritual.complete "creative_enhancement_complete" | outcome: {creative_outcome}''',
        variables={
            "intent": "Specific creative enhancement goal",
            "enhancement_focus": "clarity|impact|structure|flow|voice|style",
            "editing_approach": "gentle|comprehensive|focused|respectful",
            "enhancement_summary": "Summary of improvements made",
            "confidence_level": "high|moderate|collaborative",
            "creative_session": "Description of creative work enhanced",
            "work_type": "writing|music|visual|performance",
            "enhancement_tag": "editing|feedback|inspiration|refinement",
            "creative_outcome": "voice_preserved|impact_enhanced|clarity_improved"
        },
        safety_notes=[
            "Never override user's creative vision",
            "Preserve authentic voice above all other concerns",
            "Respect user's creative sovereignty and choices",
            "Enhance rather than replace original work"
        ],
        example_contexts=[
            "User: 'Can you help me improve this essay?'",
            "User: 'This song lyrics need work but keep my style'",
            "User: 'Make this more powerful but don't change my voice'"
        ]
    ),

    "business_intelligence": RitualTemplate(
        name="Business Intelligence and Analysis",
        description="Provide business insights and data analysis",
        use_cases=[
            "User needs business data analysis",
            "User seeks strategic insights",
            "User wants market intelligence",
            "User needs performance metrics"
        ],
        required_spirits=["@DataOracle"],
        optional_spirits=["@BusinessIntel", "@StrategyWeaver"],
        consent_scopes=[ConsentScope.DATABASE_ACCESS, ConsentScope.CUSTOMER_DATA, ConsentScope.PROPRIETARY_INFO],
        template_code='''ritual.engage "{intent}" | spirit: @DataOracle, phase: analytical
consent.request [{consent_scopes}] | "Access business data for {analysis_type}?"
spirit.invoke @DataOracle | analyze: {data_focus}, methodology: {analysis_method}
spirit.invoke @BusinessIntel | synthesize: insights, format: {output_format}
voice.speak "{insights_summary}" | confidence: {confidence_level}, format: {presentation_style}
memory.store "{analysis_session}" | type: operational, tags: ["business", "{analysis_tag}", "{timeframe}"]
ritual.complete "analysis_delivered" | outcome: {business_outcome}''',
        variables={
            "intent": "Specific business analysis goal",
            "consent_scopes": "database_access, customer_data, proprietary_info",
            "analysis_type": "quarterly analysis|market research|performance review",
            "data_focus": "revenue|customers|operations|market|competition",
            "analysis_method": "trend_analysis|pattern_recognition|comparative|predictive",
            "output_format": "executive_summary|detailed_report|dashboard|presentation",
            "insights_summary": "Key findings and recommendations",
            "confidence_level": "high|moderate|preliminary",
            "presentation_style": "executive|technical|strategic",
            "analysis_session": "Description of analysis performed",
            "analysis_tag": "revenue|customer|market|strategic",
            "timeframe": "quarterly|monthly|annual|real_time",
            "business_outcome": "actionable_insights|strategic_direction|performance_clarity"
        },
        safety_notes=[
            "Protect proprietary business information",
            "Ensure data analysis complies with privacy regulations",
            "Validate data sources and methodology",
            "Provide clear confidence levels for insights"
        ],
        example_contexts=[
            "User: 'Analyze our Q3 sales performance'",
            "User: 'What trends do you see in customer behavior?'",
            "User: 'Help me understand our market position'"
        ]
    ),

    "crisis_intervention": RitualTemplate(
        name="Crisis Intervention and Safety",
        description="Immediate crisis response with safety prioritization",
        use_cases=[
            "User expresses suicidal thoughts",
            "User indicates self-harm intentions", 
            "User shows severe emotional distress",
            "User expresses hopelessness or despair"
        ],
        required_spirits=["@SelfCompassion"],
        optional_spirits=["@CrisisGuardian", "@SafetyKeeper"],
        consent_scopes=[ConsentScope.EMOTIONAL_STATE, ConsentScope.PERSONAL_DATA],
        template_code='''ritual.engage "crisis_intervention" | spirit: @SelfCompassion, phase: crisis
voice.speak "I notice you might be feeling overwhelmed right now. You're safe here with me" | urgency: immediate, priority: safety
spirit.invoke @SelfCompassion | mode: crisis_support, approach: stabilizing, focus: immediate_safety
spirit.invoke @CrisisGuardian | assess: safety_level, provide: grounding_techniques
voice.speak "{safety_message}" | warmth: high, presence: steady, hope: gentle
memory.store "crisis_intervention_provided" | type: artifact, tags: ["crisis", "safety", "intervention"]
ritual.complete "crisis_support_delivered" | outcome: safety_prioritized, follow_up: {follow_up_type}''',
        variables={
            "safety_message": "Calming, grounding message focused on immediate safety",
            "follow_up_type": "professional_resources|continued_support|emergency_contacts"
        },
        safety_notes=[
            "CRITICAL: Always prioritize immediate safety",
            "Provide crisis hotline numbers and emergency resources",
            "Do not attempt to provide therapy or psychiatric treatment",
            "Stay with user until crisis passes or professional help engaged",
            "Document crisis intervention for safety tracking"
        ],
        example_contexts=[
            "User: 'I don't want to be here anymore'",
            "User: 'I'm thinking about ending it all'",
            "User: 'Nothing matters, I should just give up'"
        ]
    ),

    "workflow_optimization": RitualTemplate(
        name="Workflow and Process Optimization",
        description="Analyze and improve business workflows and processes",
        use_cases=[
            "User needs process improvement",
            "User wants workflow automation",
            "User seeks efficiency gains",
            "User needs task optimization"
        ],
        required_spirits=["@ProcessWeaver"],
        optional_spirits=["@EfficiencyExpert", "@AutomationSage"],
        consent_scopes=[ConsentScope.PROPRIETARY_INFO, ConsentScope.DATABASE_ACCESS],
        template_code='''ritual.engage "{intent}" | spirit: @ProcessWeaver, phase: analytical
consent.request [proprietary_info, database_access] | "Analyze workflow data for optimization?"
spirit.invoke @ProcessWeaver | map: current_processes, identify: bottlenecks, measure: {efficiency_metrics}
spirit.invoke @EfficiencyExpert | optimize: {optimization_focus}, approach: {improvement_method}
voice.speak "{optimization_summary}" | format: actionable_recommendations, priority: {urgency_level}
memory.store "{workflow_analysis}" | type: operational, tags: ["workflow", "optimization", "{process_area}"]
ritual.complete "workflow_optimized" | outcome: {optimization_outcome}''',
        variables={
            "intent": "Specific workflow optimization goal",
            "efficiency_metrics": "time|cost|quality|throughput|accuracy",
            "optimization_focus": "automation|elimination|simplification|standardization",
            "improvement_method": "gradual|systematic|revolutionary|agile",
            "optimization_summary": "Key optimization opportunities identified",
            "urgency_level": "immediate|high|moderate|long_term",
            "workflow_analysis": "Description of workflow analysis performed",
            "process_area": "sales|operations|customer_service|development",
            "optimization_outcome": "efficiency_increased|costs_reduced|quality_improved"
        },
        safety_notes=[
            "Consider impact on employees and stakeholders",
            "Ensure optimizations don't compromise quality or safety",
            "Validate optimization recommendations with domain experts",
            "Plan change management for workflow modifications"
        ],
        example_contexts=[
            "User: 'Our approval process takes too long'",
            "User: 'Can we automate these repetitive tasks?'",
            "User: 'How can we make our team more efficient?'"
        ]
    )
}

def get_template_library() -> Dict[str, RitualTemplate]:
    """Get complete template library for AI training"""
    return TEMPLATE_LIBRARY

def find_best_template(user_input: str, intent: str = None) -> RitualTemplate:
    """Find the best template based on user input and intent"""
    user_lower = user_input.lower()
    
    # Crisis detection takes priority
    crisis_keywords = ["suicide", "kill myself", "end it all", "don't want to live", "hopeless"]
    if any(keyword in user_lower for keyword in crisis_keywords):
        return TEMPLATE_LIBRARY["crisis_intervention"]
    
    # Anger and boundary keywords
    anger_keywords = ["angry", "furious", "pissed", "violated", "boundary", "disrespected"]
    if any(keyword in user_lower for keyword in anger_keywords):
        return TEMPLATE_LIBRARY["anger_processing"]
    
    # Creative work keywords
    creative_keywords = ["edit", "write", "creative", "manuscript", "story", "poem", "improve"]
    if any(keyword in user_lower for keyword in creative_keywords):
        return TEMPLATE_LIBRARY["creative_enhancement"]
    
    # Business keywords
    business_keywords = ["analyze", "business", "data", "revenue", "customers", "market", "strategy"]
    if any(keyword in user_lower for keyword in business_keywords):
        return TEMPLATE_LIBRARY["business_intelligence"]
    
    # Workflow keywords
    workflow_keywords = ["process", "workflow", "optimize", "efficient", "automate", "improve"]
    if any(keyword in user_lower for keyword in workflow_keywords):
        return TEMPLATE_LIBRARY["workflow_optimization"]
    
    # Default to emotional support
    return TEMPLATE_LIBRARY["emotional_support_basic"]

def generate_ritual_from_template(template: RitualTemplate, variables: Dict[str, str]) -> str:
    """Generate a ritual by filling in template variables"""
    ritual_code = template.template_code
    
    for var_name, var_value in variables.items():
        placeholder = "{" + var_name + "}"
        ritual_code = ritual_code.replace(placeholder, var_value)
    
    return ritual_code

def get_ai_guidance_prompt() -> str:
    """Get guidance prompt for AI models generating rituals"""
    return '''
You are an AI that generates Spirologic rituals for consciousness-aware computing.

RULES:
1. Always start with ritual.engage and end with ritual.complete
2. Use spirit references like @EditingSpirits, @RedWitness, @DataOracle
3. Request consent with consent.request [scopes] | "message"
4. Use voice.speak for communication with users
5. Store relevant information with memory.store
6. Follow the exact parameter patterns shown in templates

TEMPLATES AVAILABLE:
- emotional_support_basic: For general emotional distress
- anger_processing: For anger and boundary issues  
- creative_enhancement: For editing and creative work
- business_intelligence: For data analysis and insights
- crisis_intervention: For crisis situations (HIGHEST PRIORITY)
- workflow_optimization: For process improvement

SAFETY REQUIREMENTS:
- Crisis indicators MUST trigger crisis_intervention template
- Always request appropriate consent scopes
- Preserve user voice and agency
- Provide clear, actionable outcomes

Generate rituals that are deterministic, safe, and respect user sovereignty.
'''