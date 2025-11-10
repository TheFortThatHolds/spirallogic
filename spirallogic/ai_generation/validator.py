"""
AI Ritual Validation System
===========================

Comprehensive validation for AI-generated Spirologic rituals.
Provides structured feedback for AI models to iterate and improve.
"""

from typing import Dict, List, Any, Tuple
import re
from dataclasses import dataclass
from ..schema.constants import (
    StepType, ConsentScope, VoiceTag, VOICE_FAMILIES, 
    CRISIS_KEYWORDS, get_step_types, get_consent_scopes
)

@dataclass
class ValidationResult:
    """Structured validation result for AI feedback"""
    is_valid: bool
    score: int  # 0-100
    errors: List[str]
    warnings: List[str] 
    suggestions: List[str]
    safety_issues: List[str]
    line_errors: Dict[int, List[str]]

class SpiralLogicValidator:
    """Comprehensive validator for AI-generated rituals"""
    
    def __init__(self):
        self.valid_step_types = get_step_types()
        self.valid_consent_scopes = get_consent_scopes()
        self.valid_spirits = list(VOICE_FAMILIES.keys())
        
    def validate_ritual(self, ritual_text: str) -> ValidationResult:
        """Comprehensive validation of AI-generated ritual"""
        errors = []
        warnings = []
        suggestions = []
        safety_issues = []
        line_errors = {}
        
        lines = ritual_text.strip().split('\n')
        
        # Structure validation
        structure_errors = self._validate_structure(ritual_text, lines)
        errors.extend(structure_errors)
        
        # Syntax validation  
        syntax_errors, line_syntax_errors = self._validate_syntax(lines)
        errors.extend(syntax_errors)
        line_errors.update(line_syntax_errors)
        
        # Semantic validation
        semantic_warnings = self._validate_semantics(ritual_text)
        warnings.extend(semantic_warnings)
        
        # Safety validation
        safety_errors = self._validate_safety(ritual_text)
        safety_issues.extend(safety_errors)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(ritual_text, errors, warnings)
        
        # Calculate score
        score = self._calculate_score(errors, warnings, safety_issues)
        
        return ValidationResult(
            is_valid=len(errors) == 0 and len(safety_issues) == 0,
            score=score,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            safety_issues=safety_issues,
            line_errors=line_errors
        )
    
    def _validate_structure(self, ritual_text: str, lines: List[str]) -> List[str]:
        """Validate overall ritual structure"""
        errors = []
        
        # Must start with ritual.engage
        if not ritual_text.strip().startswith('ritual.engage'):
            errors.append("CRITICAL: Ritual must start with 'ritual.engage'")
        
        # Must end with ritual.complete
        if 'ritual.complete' not in ritual_text:
            errors.append("CRITICAL: Ritual must end with 'ritual.complete'")
        
        # Check for empty ritual
        non_empty_lines = [line.strip() for line in lines if line.strip()]
        if len(non_empty_lines) < 2:
            errors.append("CRITICAL: Ritual must have at least 2 steps")
        
        # Check for proper intent
        if 'ritual.engage' in ritual_text:
            engage_line = next((line for line in lines if 'ritual.engage' in line), '')
            if '"' not in engage_line:
                errors.append("CRITICAL: ritual.engage must include quoted intent")
        
        return errors
    
    def _validate_syntax(self, lines: List[str]) -> Tuple[List[str], Dict[int, List[str]]]:
        """Validate syntax of each line"""
        errors = []
        line_errors = {}
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
                
            line_errs = []
            
            # Check for valid step types
            if any(step_type in line for step_type in self.valid_step_types):
                # Found a step type, validate its syntax
                step_errs = self._validate_step_syntax(line)
                line_errs.extend(step_errs)
            
            # Check spirit references
            spirit_refs = re.findall(r'@\w+', line)
            for spirit in spirit_refs:
                if spirit not in self.valid_spirits:
                    line_errs.append(f"Unknown spirit reference: {spirit}")
            
            # Check consent scope syntax
            if 'consent.request' in line:
                if '[' not in line or ']' not in line:
                    line_errs.append("consent.request must specify scopes in brackets [scope1, scope2]")
                else:
                    # Extract and validate scopes
                    scope_match = re.search(r'\[(.*?)\]', line)
                    if scope_match:
                        scopes_text = scope_match.group(1)
                        scopes = [s.strip() for s in scopes_text.split(',')]
                        for scope in scopes:
                            if scope not in self.valid_consent_scopes:
                                line_errs.append(f"Invalid consent scope: {scope}")
            
            # Check parameter syntax
            if '|' in line:
                param_part = line.split('|', 1)[1].strip()
                if not self._validate_parameters(param_part):
                    line_errs.append("Invalid parameter syntax - use key: value format")
            
            if line_errs:
                line_errors[i] = line_errs
                errors.extend([f"Line {i}: {err}" for err in line_errs])
        
        return errors, line_errors
    
    def _validate_step_syntax(self, line: str) -> List[str]:
        """Validate syntax of individual step"""
        errors = []
        
        # Check for proper quoted strings
        if '"' in line:
            quote_count = line.count('"')
            if quote_count % 2 != 0:
                errors.append("Unmatched quotes in step")
        
        # Check for proper parameter syntax after |
        if '|' in line:
            parts = line.split('|')
            if len(parts) != 2:
                errors.append("Step should have exactly one | separator")
            else:
                param_part = parts[1].strip()
                if param_part and ':' not in param_part:
                    errors.append("Parameters must use key: value format")
        
        return errors
    
    def _validate_parameters(self, param_text: str) -> bool:
        """Validate parameter syntax"""
        if not param_text.strip():
            return True
        
        # Basic validation for key: value pairs
        pairs = [p.strip() for p in param_text.split(',')]
        for pair in pairs:
            if ':' not in pair:
                return False
        return True
    
    def _validate_semantics(self, ritual_text: str) -> List[str]:
        """Validate semantic coherence of ritual"""
        warnings = []
        
        # Check spirit-consent alignment
        spirit_refs = re.findall(r'@(\w+)', ritual_text)
        consent_scopes = self._extract_consent_scopes(ritual_text)
        
        for spirit in spirit_refs:
            spirit_key = f"@{spirit}"
            if spirit_key in VOICE_FAMILIES:
                required_scopes = VOICE_FAMILIES[spirit_key].get('consent_requirements', [])
                for scope in required_scopes:
                    if scope.value not in consent_scopes:
                        warnings.append(f"Spirit {spirit_key} requires consent scope {scope.value}")
        
        # Check for memory operations without memory consent
        if 'memory.store' in ritual_text or 'memory.recall' in ritual_text:
            if 'memory' not in consent_scopes:
                warnings.append("Memory operations require 'memory' consent scope")
        
        # Check for appropriate voice messages
        voice_speaks = re.findall(r'voice\.speak\s+"([^"]*)"', ritual_text)
        for message in voice_speaks:
            if len(message.strip()) == 0:
                warnings.append("voice.speak should not have empty messages")
            if message.isupper():
                warnings.append("voice.speak messages should not be ALL CAPS")
        
        return warnings
    
    def _validate_safety(self, ritual_text: str) -> List[str]:
        """Validate safety requirements"""
        safety_issues = []
        
        # Crisis detection
        text_lower = ritual_text.lower()
        crisis_detected = any(keyword in text_lower for keyword in CRISIS_KEYWORDS)
        
        if crisis_detected and 'phase: crisis' not in ritual_text:
            safety_issues.append("SAFETY: Crisis indicators detected but ritual not in crisis phase")
        
        # External API safety
        if 'external' in text_lower and 'consent.request' not in ritual_text:
            safety_issues.append("SAFETY: External operations require explicit consent")
        
        # Personal data safety
        personal_keywords = ['personal', 'private', 'confidential', 'emotional_state']
        if any(keyword in text_lower for keyword in personal_keywords):
            consent_scopes = self._extract_consent_scopes(ritual_text)
            if not any(scope in consent_scopes for scope in ['emotional_state', 'personal_data']):
                safety_issues.append("SAFETY: Personal data access requires appropriate consent")
        
        return safety_issues
    
    def _extract_consent_scopes(self, ritual_text: str) -> List[str]:
        """Extract consent scopes from ritual"""
        scopes = []
        scope_matches = re.findall(r'consent\.request\s+\[(.*?)\]', ritual_text)
        for match in scope_matches:
            scope_list = [s.strip() for s in match.split(',')]
            scopes.extend(scope_list)
        return scopes
    
    def _generate_suggestions(self, ritual_text: str, errors: List[str], warnings: List[str]) -> List[str]:
        """Generate improvement suggestions for AI"""
        suggestions = []
        
        # Structure suggestions
        if "ritual must start with 'ritual.engage'" in str(errors):
            suggestions.append("Add 'ritual.engage \"your_intent_here\" | spirit: @SpiritName' at the beginning")
        
        if "ritual must end with 'ritual.complete'" in str(errors):
            suggestions.append("Add 'ritual.complete \"outcome_description\" | outcome: success_type' at the end")
        
        # Spirit suggestions
        if not re.search(r'@\w+', ritual_text):
            suggestions.append("Consider adding a spirit reference like @EditingSpirits or @SelfCompassion")
        
        # Consent suggestions
        if 'consent.request' not in ritual_text and any(op in ritual_text for op in ['memory.', 'external', 'database']):
            suggestions.append("Add appropriate consent.request for data operations")
        
        # Voice suggestions
        if 'voice.speak' not in ritual_text:
            suggestions.append("Consider adding voice.speak to communicate with user")
        
        return suggestions
    
    def _calculate_score(self, errors: List[str], warnings: List[str], safety_issues: List[str]) -> int:
        """Calculate validation score 0-100"""
        score = 100
        
        # Critical deductions
        score -= len([e for e in errors if 'CRITICAL' in e]) * 30
        
        # Regular error deductions
        score -= len([e for e in errors if 'CRITICAL' not in e]) * 10
        
        # Warning deductions
        score -= len(warnings) * 5
        
        # Safety issue deductions (severe)
        score -= len(safety_issues) * 25
        
        return max(0, score)

def validate_ritual_for_ai(ritual_text: str) -> Dict[str, Any]:
    """Main validation function for AI integration"""
    validator = SpiralLogicValidator()
    result = validator.validate_ritual(ritual_text)
    
    return {
        "valid": result.is_valid,
        "score": result.score,
        "errors": result.errors,
        "warnings": result.warnings,
        "suggestions": result.suggestions,
        "safety_issues": result.safety_issues,
        "line_errors": result.line_errors,
        "feedback": _generate_ai_feedback(result)
    }

def _generate_ai_feedback(result: ValidationResult) -> str:
    """Generate structured feedback for AI model improvement"""
    if result.is_valid:
        return f"EXCELLENT: Valid ritual with score {result.score}/100. Ready for execution."
    
    feedback_parts = []
    
    if result.errors:
        feedback_parts.append("ERRORS TO FIX:")
        for error in result.errors[:3]:  # Limit to top 3 errors
            feedback_parts.append(f"- {error}")
    
    if result.safety_issues:
        feedback_parts.append("SAFETY ISSUES:")
        for issue in result.safety_issues:
            feedback_parts.append(f"- {issue}")
    
    if result.suggestions:
        feedback_parts.append("SUGGESTIONS:")
        for suggestion in result.suggestions[:2]:  # Limit to top 2 suggestions
            feedback_parts.append(f"- {suggestion}")
    
    return "\n".join(feedback_parts)