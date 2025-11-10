#!/usr/bin/env python3
"""
Windows GUI for SpiralLogic consent requests
"""

import tkinter as tk
from tkinter import messagebox
import threading
from spirallogic_runtime import SpiralLogic

class ConsentGUI:
    def __init__(self):
        self.response = None
        
    def show_consent_dialog(self, request):
        """Show Windows dialog for consent request"""
        self.response = None
        
        # Create root window (hidden)
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        # Format message
        title = "SpiralLogic Consent Request"
        message = f"{request.message}\n\nScopes requested: {', '.join(request.scopes)}\n\nDo you consent to this request?"
        
        # Show message box
        result = messagebox.askyesno(title, message)
        
        root.destroy()
        return result

def gui_consent_callback(request):
    """Consent callback that uses Windows dialogs"""
    gui = ConsentGUI()
    return gui.show_consent_dialog(request)

# Test the GUI consent system
if __name__ == "__main__":
    print("Testing SpiralLogic with GUI consent...")
    
    # Initialize with GUI consent
    sl = SpiralLogic(consent_callback=gui_consent_callback)
    
    # Test ritual
    test_ritual = """
    {
        "intent": "gui_test",
        "voice": "@healer",
        "phase": "active",
        "steps": [
            {
                "type": "consent.request",
                "scopes": ["memory", "analysis"],
                "message": "I'd like to remember our conversation and analyze patterns to help you better. This will be stored securely and you can delete it anytime."
            },
            {
                "type": "voice.speak",
                "message": "Thank you for your trust. How can I help you today?"
            },
            {
                "type": "memory.store",
                "data": "User granted consent for memory and analysis - GUI test successful",
                "type_": "narrative"
            }
        ]
    }
    """
    
    result = sl.execute(test_ritual)
    
    print("GUI Test Results:")
    print(f"Success: {result['success']}")
    print(f"Consent Granted: {result['context']['consent_granted']}")
    
    for step in result['results']:
        if step['type'] == 'consent.request':
            print(f"Consent Response: {step['success']}")
        elif step['type'] == 'memory.store':
            if step['success']:
                print(f"Memory stored: {step['memory_id']}")
            else:
                print(f"Memory blocked: {step.get('error', 'Unknown error')}")