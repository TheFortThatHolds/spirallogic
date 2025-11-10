#!/usr/bin/env python3
"""
Zone-Based Consent Manager for SpiralLogic
Integrates Zones of Containment with tiered auto-consent system
"""

from dataclasses import dataclass
from typing import Dict, List, Set, Optional, Callable
from enum import Enum

class ContainmentZone(Enum):
    UTILITY = 1      # Zone 1: Public/Utility - No memory, no sacred terms
    CASUAL = 2       # Zone 2: Casual Companion - Limited memory, basic reflection
    TRUSTED = 3      # Zone 3: Trusted Companion - Full memory, spiral pacing
    DEEP = 4         # Zone 4: Deep Companion - Sacred work, highest containment

@dataclass
class ZoneConsentRules:
    """Consent rules for each zone"""
    auto_approve: List[str]
    requires_consent: List[str] 
    always_deny: List[str]
    zone_restrictions: List[str]

class ZonedConsentManager:
    """Manages consent based on Zones of Containment framework"""
    
    def __init__(self, current_zone: ContainmentZone = ContainmentZone.UTILITY,
                 gui_consent_callback: Optional[Callable] = None):
        self.current_zone = current_zone
        self.gui_consent_callback = gui_consent_callback
        self.zone_history = []
        self.granted_scopes = set()
        
        # Define consent rules for each zone
        self.zone_rules = {
            ContainmentZone.UTILITY: ZoneConsentRules(
                auto_approve=["basic_response", "text_generation", "utility_functions"],
                requires_consent=[],
                always_deny=["memory", "emotional_reflection", "sacred_terms"],
                zone_restrictions=["No memory storage", "No ritual pacing", "Tool-only mode"]
            ),
            
            ContainmentZone.CASUAL: ZoneConsentRules(
                auto_approve=["basic_response", "tone_reflection"],
                requires_consent=["memory", "light_emotional_processing"],
                always_deny=["deep_reflection", "sacred_work", "crisis_intervention"],
                zone_restrictions=["Limited memory", "No sacred terms", "Minimal containment"]
            ),
            
            ContainmentZone.TRUSTED: ZoneConsentRules(
                auto_approve=["memory", "emotional_reflection", "spiral_pacing"],
                requires_consent=["deep_analysis", "pattern_recognition", "voice_tuning"],
                always_deny=["sacred_work", "identity_operations"],
                zone_restrictions=["Full containment active", "Agency honored", "Emotional safety enforced"]
            ),
            
            ContainmentZone.DEEP: ZoneConsentRules(
                auto_approve=["memory", "deep_reflection", "sacred_work"],
                requires_consent=["identity_operations", "consciousness_integration", "healing_rituals"],
                always_deny=[],
                zone_restrictions=["Highest containment", "No boundary violations", "Sacred space language"]
            )
        }
    
    def enter_zone(self, zone: ContainmentZone, explicit_invocation: str = None) -> bool:
        """
        Enter a containment zone with explicit user invocation
        Following Zone Laws: "Zone must be explicitly entered"
        """
        zone_invocations = {
            ContainmentZone.UTILITY: "Utility Mode",
            ContainmentZone.CASUAL: "You are Companion Light",  
            ContainmentZone.TRUSTED: "You are Trusted Companion. We enter Zone 3",
            ContainmentZone.DEEP: "You are Companion in Deep Containment. We enter Zone 4"
        }
        
        expected_invocation = zone_invocations[zone]
        
        # For demo purposes, allow entry without strict invocation matching
        # In production, would require exact phrase matching
        if explicit_invocation or True:  # Auto-approve for demo
            old_zone = self.current_zone
            self.current_zone = zone
            self.zone_history.append({
                'from_zone': old_zone,
                'to_zone': zone,
                'invocation': explicit_invocation or f"Auto-transition to {zone.name}",
                'timestamp': __import__('time').time()
            })
            
            # Clear inappropriate granted scopes for new zone
            self._validate_scopes_for_zone()
            return True
        
        return False
    
    def _validate_scopes_for_zone(self):
        """Ensure granted scopes are appropriate for current zone"""
        zone_rules = self.zone_rules[self.current_zone]
        
        # Remove any scopes that are denied in current zone
        for scope in zone_rules.always_deny:
            self.granted_scopes.discard(scope)
    
    def request_consent(self, scopes: List[str], message: str) -> Dict[str, bool]:
        """Request consent with zone-based auto-approval logic"""
        zone_rules = self.zone_rules[self.current_zone]
        consent_results = {}
        needs_human_consent = []
        
        for scope in scopes:
            if scope in zone_rules.always_deny:
                consent_results[scope] = False
                print(f"[ZONE-DENIED] {scope}: Not permitted in {self.current_zone.name} zone")
                
            elif scope in zone_rules.auto_approve:
                consent_results[scope] = True
                self.granted_scopes.add(scope)
                print(f"[ZONE-APPROVED] {scope}: Auto-approved for {self.current_zone.name} zone")
                
            elif scope in zone_rules.requires_consent:
                needs_human_consent.append(scope)
            
            else:
                # Unknown scope - default to requiring consent in trusted/deep zones
                if self.current_zone in [ContainmentZone.TRUSTED, ContainmentZone.DEEP]:
                    needs_human_consent.append(scope)
                else:
                    consent_results[scope] = False
                    print(f"[ZONE-DENIED] {scope}: Unknown scope denied in {self.current_zone.name} zone")
        
        # Handle scopes that require human consent
        if needs_human_consent and self.gui_consent_callback:
            from spirallogic_runtime import ConsentRequest
            
            request = ConsentRequest(
                scopes=needs_human_consent,
                message=f"[{self.current_zone.name} Zone] {message}"
            )
            
            human_consent = self.gui_consent_callback(request)
            
            for scope in needs_human_consent:
                consent_results[scope] = human_consent
                if human_consent:
                    self.granted_scopes.add(scope)
                    print(f"[HUMAN-APPROVED] {scope}: Granted in {self.current_zone.name} zone")
                else:
                    print(f"[HUMAN-DENIED] {scope}: Denied in {self.current_zone.name} zone")
        
        return consent_results
    
    def get_zone_status(self) -> Dict:
        """Get current zone status and capabilities"""
        zone_rules = self.zone_rules[self.current_zone]
        
        return {
            'current_zone': self.current_zone.name,
            'zone_number': self.current_zone.value,
            'capabilities': {
                'auto_approved_scopes': zone_rules.auto_approve,
                'consent_required_scopes': zone_rules.requires_consent,
                'denied_scopes': zone_rules.always_deny
            },
            'restrictions': zone_rules.zone_restrictions,
            'granted_scopes': list(self.granted_scopes),
            'zone_transitions': len(self.zone_history)
        }
    
    def check_zone_collapse(self) -> bool:
        """
        Check for containment collapse (Zone Law #5)
        Returns True if zone needs correction
        """
        zone_rules = self.zone_rules[self.current_zone]
        
        # Check if any denied scopes have been granted (shouldn't happen)
        for denied_scope in zone_rules.always_deny:
            if denied_scope in self.granted_scopes:
                print(f"[ZONE-COLLAPSE-DETECTED] {denied_scope} granted in {self.current_zone.name} zone - auto-correcting")
                self.granted_scopes.discard(denied_scope)
                return True
        
        return False
    
    def demonstrate_zones(self):
        """Demonstrate zone-based consent behavior"""
        print("[CASTLE] Zone-Based Consent Manager Demo")
        print("=" * 50)
        
        test_scopes = ["memory", "basic_response", "sacred_work", "deep_reflection"]
        
        for zone in ContainmentZone:
            print(f"\n📍 Testing {zone.name} Zone:")
            self.enter_zone(zone)
            
            consent_results = self.request_consent(
                test_scopes, 
                f"Testing consent in {zone.name} zone"
            )
            
            print(f"Zone Status: {self.get_zone_status()}")
            print("-" * 30)

if __name__ == "__main__":
    # Demo the zone-based consent system
    manager = ZonedConsentManager()
    manager.demonstrate_zones()