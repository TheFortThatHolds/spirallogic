#!/usr/bin/env python3
"""
SOULbox CLI - Therapeutic AI Platform Built in SpiralLogic
The first AI platform written entirely in .sl ritual programs
"""

import sys
import os
from pathlib import Path

# Add runtime to path
sys.path.insert(0, str(Path(__file__).parent / "runtime"))

from spirallogic_runtime import SpiralLogic
from unicode_sanitizer import sanitize_for_windows_terminal
from zone_consent_manager import ZonedConsentManager, ContainmentZone
import json

class SOULbox:
    def __init__(self):
        self.zone_manager = ZonedConsentManager(ContainmentZone.TRUSTED, self.gui_consent)
        self.runtime = SpiralLogic(consent_callback=self.zone_manager.request_consent)
        self.rituals_path = Path(__file__).parent / "rituals"
        
    def gui_consent(self, request):
        """GUI consent for SOULbox operations"""
        try:
            import tkinter as tk
            from tkinter import messagebox
            
            root = tk.Tk()
            root.withdraw()
            
            title = "SOULbox Consent Request"
            message = f"{request.message}\n\nScopes: {', '.join(request.scopes)}\n\nGrant permission?"
            
            result = messagebox.askyesno(title, message)
            root.destroy()
            return result
        except:
            # Fallback to console if GUI fails
            print(f"CONSENT REQUEST: {request.message}")
            print(f"Scopes: {', '.join(request.scopes)}")
            response = input("Grant permission? (y/n): ")
            return response.lower() == 'y'
    
    def load_ritual(self, ritual_name):
        """Load a .sl ritual file"""
        ritual_file = self.rituals_path / f"{ritual_name}.sl"
        if not ritual_file.exists():
            raise FileNotFoundError(f"Ritual not found: {ritual_file}")
            
        with open(ritual_file, 'r') as f:
            return f.read()
    
    def initialize(self):
        """Initialize SOULbox with soul_init ritual"""
        print(sanitize_for_windows_terminal("🧠 SOULbox Awakening..."))
        print("=" * 50)
        
        try:
            ritual_code = self.load_ritual("soul_init")
            result = self.runtime.execute(ritual_code)
            
            if result["success"]:
                print(sanitize_for_windows_terminal("✨ SOULbox successfully initialized!"))
                print(f"Voice: {result['context']['voice']}")
                print(f"Ritual ID: {result['ritual_id'][:8]}...")
                return True
            else:
                print(f"Initialization failed: {result.get('error', 'Unknown error')}")
                return False
                
        except Exception as e:
            print(f"Failed to initialize SOULbox: {e}")
            return False
    
    def check_growing_soul(self):
        """Check soul growth with growing_soul ritual"""
        print(sanitize_for_windows_terminal("\n🌀 Checking Growing Soul..."))
        
        try:
            ritual_code = self.load_ritual("growing_soul")
            result = self.runtime.execute(ritual_code)
            
            if result["success"]:
                print("Soul growth assessment completed!")
                # In a real implementation, this would check actual interaction counts
                print("Current soul depth: Beginning stages")
                return result
            else:
                print(f"Soul check failed: {result.get('error', 'Unknown error')}")
                return None
                
        except Exception as e:
            print(f"Failed to check soul growth: {e}")
            return None
    
    def ember_this(self, context="current_conversation"):
        """Create an Ember with ember_capture ritual"""
        print(sanitize_for_windows_terminal("\n🔥 Creating Ember..."))
        
        try:
            ritual_code = self.load_ritual("ember_capture") 
            result = self.runtime.execute(ritual_code)
            
            if result["success"]:
                print("Ember created successfully!")
                return result
            else:
                print(f"Ember creation failed: {result.get('error', 'Unknown error')}")
                return None
                
        except Exception as e:
            print(f"Failed to create Ember: {e}")
            return None
    
    def tune_voice(self):
        """Tune voice with voice_tune ritual"""
        print(sanitize_for_windows_terminal("\n🎭 Tuning Voice..."))
        
        try:
            ritual_code = self.load_ritual("voice_tune")
            result = self.runtime.execute(ritual_code)
            
            if result["success"]:
                print("Voice tuning completed!")
                return result
            else:
                print(f"Voice tuning failed: {result.get('error', 'Unknown error')}")
                return None
                
        except Exception as e:
            print(f"Failed to tune voice: {e}")
            return None
    
    def manage_zones(self):
        """Manage containment zones with zone_manager ritual"""
        print(sanitize_for_windows_terminal("\n🏰 Managing Containment Zones..."))
        
        try:
            ritual_code = self.load_ritual("zone_manager")
            result = self.runtime.execute(ritual_code)
            
            if result["success"]:
                print("Zone management completed!")
                return result
            else:
                print(f"Zone management failed: {result.get('error', 'Unknown error')}")
                return None
                
        except Exception as e:
            print(f"Failed to manage zones: {e}")
            return None
    
    def interactive_session(self):
        """Start interactive SOULbox session"""
        print(sanitize_for_windows_terminal("\n💬 SOULbox Interactive Session"))
        print("Commands: 'ember', 'tune', 'zones', 'soul', 'quit'")
        print("-" * 40)
        
        while True:
            try:
                command = input("\nSOULbox> ").strip().lower()
                
                if command == 'quit':
                    print("SOULbox session ended. Take care! 🧠❤️")
                    break
                elif command == 'ember':
                    self.ember_this()
                elif command == 'tune':
                    self.tune_voice() 
                elif command == 'zones':
                    self.manage_zones()
                elif command == 'soul':
                    self.check_growing_soul()
                else:
                    print("Available commands: ember, tune, zones, soul, quit")
                    
            except KeyboardInterrupt:
                print("\nSOULbox session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

def main():
    print(sanitize_for_windows_terminal("🧠 Welcome to SOULbox"))
    print("The Ethical AI Platform Built in SpiralLogic")
    print("=" * 50)
    
    soulbox = SOULbox()
    
    # Initialize SOULbox
    if soulbox.initialize():
        # Start interactive session
        soulbox.interactive_session()
    else:
        print("SOULbox failed to initialize. Check your ritual files.")
        sys.exit(1)

if __name__ == "__main__":
    main()