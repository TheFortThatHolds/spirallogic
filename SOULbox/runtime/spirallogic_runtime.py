#!/usr/bin/env python3
"""
SpiralLogic Runtime Engine
AI-native programming language for ethical interaction systems

Usage:
    from spirallogic_runtime import SpiralLogic
    
    sl = SpiralLogic()
    result = sl.execute(ritual_program_string)
"""

import json
import time
import hashlib
from datetime import datetime
from dataclasses import dataclass, asdict
from types import SimpleNamespace
from typing import Dict, List, Optional, Any, Callable
import builtins
import threading
import uuid
import sqlite3
import os

@dataclass
class ConsentRequest:
    """Consent request structure"""
    scopes: List[str]
    message: str
    timeout_ms: int = 30000
    request_id: str = None
    
    def __post_init__(self):
        if not self.request_id:
            self.request_id = str(uuid.uuid4())

@dataclass
class RitualContext:
    """Execution context for a ritual"""
    ritual_id: str
    intent: str
    voice: str
    phase: str
    user_id: str
    session_id: str
    consent_granted: Dict[str, bool]
    memory_store: Dict[str, Any]
    artifacts: Dict[str, Any]
    crisis_active: bool = False
    
class ConsentManager:
    """Manages user consent for various operations"""
    
    def __init__(self, consent_callback: Optional[Callable] = None):
        self.consent_callback = consent_callback or self._default_consent_callback
        self._granted_scopes = set()
        self.granted_scopes = self._granted_scopes
    
    def _default_consent_callback(self, request: ConsentRequest) -> bool:
        """Default console-based consent"""
        print(f"Consent requested: {request.message}")
        print(f"Scopes: {', '.join(request.scopes)}")
        response = input("Grant consent? (y/n): ")
        return response.lower() in ['y', 'yes']
    
    def request_consent(self, scopes: List[str], message: str) -> bool:
        """Request consent for specific scopes"""
        request = ConsentRequest(scopes=scopes, message=message)
        granted = self.consent_callback(request)
        if granted:
            self._granted_scopes.update(scopes)
        return granted

    def check_scope(self, scope: str) -> bool:
        """Check if scope already granted"""
        return scope in self._granted_scopes

    def revoke_scopes(self, scopes: List[str]) -> None:
        """Revoke granted scopes"""
        for scope in scopes:
            self._granted_scopes.discard(scope)

class MemoryVault:
    """Manages memory storage with Chronicle Split architecture"""
    
    def __init__(self, db_path: str = "spirallogic_memory.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database with Chronicle Split tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Narrative memories (user stories, experiences, emotions)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS narrative_memories (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                user_id TEXT NOT NULL,
                session_id TEXT,
                data TEXT NOT NULL,
                tags TEXT,
                searchable BOOLEAN DEFAULT 1
            )
        """)
        
        # Artifact memories (system data, logs, structured info)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS artifact_memories (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                user_id TEXT NOT NULL,
                session_id TEXT,
                data TEXT NOT NULL,
                memory_type TEXT,
                metadata TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def store_memory(self, data: str, memory_type: str, user_id: str, 
                    session_id: str = None, tags: List[str] = None) -> str:
        """Store memory in appropriate Chronicle Split table"""
        memory_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if memory_type == "narrative":
            cursor.execute("""
                INSERT INTO narrative_memories 
                (id, timestamp, user_id, session_id, data, tags)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (memory_id, timestamp, user_id, session_id, data, 
                  json.dumps(tags) if tags else None))
        
        elif memory_type == "artifact":
            cursor.execute("""
                INSERT INTO artifact_memories 
                (id, timestamp, user_id, session_id, data, memory_type)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (memory_id, timestamp, user_id, session_id, data, memory_type))
        
        else:
            # Default to artifact storage
            cursor.execute("""
                INSERT INTO artifact_memories 
                (id, timestamp, user_id, session_id, data, memory_type)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (memory_id, timestamp, user_id, session_id, data, "unknown"))
        
        conn.commit()
        conn.close()
        
        return memory_id

class CrisisMonitor:
    """Monitors for crisis indicators and responds appropriately"""
    
    CRISIS_PATTERNS = [
        r"want to (hurt|harm|kill) myself",
        r"going to (hurt|harm|kill) myself", 
        r"suicide|suicidal",
        r"end it all",
        r"can't go on",
        r"want to die",
        r"better off dead",
        r"no point in living",
        r"give up.*everything"
    ]
    
    def __init__(self):
        import re
        self.patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.CRISIS_PATTERNS]
    
    def detect_crisis(self, text: str) -> bool:
        """Check if text contains crisis indicators"""
        for pattern in self.patterns:
            if pattern.search(text):
                return True
        return False
    
    def create_crisis_response(self) -> Dict[str, Any]:
        """Generate appropriate crisis response"""
        return {
            "mode": "anchor_mode",
            "message": "I notice you might be feeling overwhelmed right now. You're safe here. Let's take a breath together.",
            "resources": [
                "Crisis Text Line: Text HOME to 741741",
                "National Suicide Prevention Lifeline: 988"  
            ],
            "next_steps": ["breathing_exercise", "grounding_technique"]
        }

class AttestationLogger:
    """Cryptographic logging for transparency and audit trails"""
    
    def __init__(self, log_file: str = "spirallogic_attestations.log"):
        self.log_file = log_file
        self.previous_hash = "0" * 64  # Genesis hash
    
    def log_event(self, event_type: str, data: Dict[str, Any]) -> str:
        """Log an event with cryptographic hash chain"""
        timestamp = datetime.now().isoformat()
        
        log_entry = {
            "timestamp": timestamp,
            "event_type": event_type,
            "data": data,
            "previous_hash": self.previous_hash
        }
        
        # Create hash of current entry
        entry_json = json.dumps(log_entry, sort_keys=True)
        current_hash = hashlib.sha256(entry_json.encode()).hexdigest()
        log_entry["hash"] = current_hash
        
        # Write to log file
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        self.previous_hash = current_hash
        return current_hash

class PythonExecutionSandbox:
    """Minimal sandbox for executing consent-wrapped Python blocks."""

    SAFE_BUILTINS = [
        'abs', 'all', 'any', 'bool', 'dict', 'enumerate', 'float', 'int',
        'len', 'list', 'map', 'max', 'min', 'pow', 'range', 'round',
        'set', 'sorted', 'str', 'sum', 'tuple', 'zip', 'print',
        'Exception', '__import__'
    ]

    def __init__(self) -> None:
        self.safe_builtins = {
            name: getattr(builtins, name)
            for name in self.SAFE_BUILTINS
            if hasattr(builtins, name)
        }

    def create_environment(
        self,
        *,
        runtime: Optional['SpiralLogic'] = None,
        context: Optional[RitualContext] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        env_globals: Dict[str, Any] = {
            '__builtins__': dict(self.safe_builtins),
            'metadata': metadata or {},
            'ritual_context': context,
            'json': json,
            'time': time,
            'datetime': datetime,
            'uuid': uuid,
            'hashlib': hashlib,
            'SimpleNamespace': SimpleNamespace,
        }

        try:
            import requests  # type: ignore
            env_globals['requests'] = requests
        except ImportError:
            pass

        try:
            import sqlite3 as sqlite_module  # type: ignore
            env_globals['sqlite3'] = sqlite_module
        except ImportError:
            pass

        if runtime is not None:
            env_globals['runtime'] = runtime

        return env_globals

    def execute_block(
        self,
        code: str,
        env_globals: Dict[str, Any],
        env_locals: Dict[str, Any],
        *,
        block_name: str = 'execute',
    ) -> None:
        if not code or not code.strip():
            return
        compiled = compile(code, f'<spirallogic:{block_name}>', 'exec')
        exec(compiled, env_globals, env_locals)  # nosec B102


class ExecutionBridge:
    """Helper exposed inside consent-wrapped execution blocks."""

    def __init__(self, runtime: 'SpiralLogic', context: RitualContext, metadata: Dict[str, Any]):
        self._runtime = runtime
        self._context = context
        self.metadata = metadata

    @property
    def consent(self) -> Dict[str, bool]:
        return self._context.consent_granted

    def require_scope(self, scope: str, message: Optional[str] = None) -> bool:
        return self._runtime._ensure_scopes([scope], message or f'Requires scope: {scope}', self._context)

    def remember(self, data: Any, memory_type: str = 'narrative', tags: Optional[List[str]] = None) -> Dict[str, Any]:
        step = {
            'type': 'memory.store',
            'data': data,
            'type_': memory_type,
        }
        if tags:
            step['tags'] = tags
        return self._runtime._execute_memory_store(step, self._context)

    def log(self, message: str, **details: Any) -> None:
        payload = {
            'ritual_id': self._context.ritual_id,
            'message': message,
            'details': self._runtime._safe_json_value(details) if details else {}
        }
        self._runtime.attestation.log_event('execution_note', payload)


class SpiralLogic:
    """Main SpiralLogic runtime engine"""
    
    def __init__(self, consent_callback: Optional[Callable] = None):
        self.consent_manager = ConsentManager(consent_callback)
        self.memory_vault = MemoryVault()
        self.crisis_monitor = CrisisMonitor()
        self.attestation = AttestationLogger()
        self.execution_sandbox = PythonExecutionSandbox()
        
    def execute(self, ritual_code: str, user_id: str = "default", 
                session_id: str = None) -> Dict[str, Any]:
        """Execute a SpiralLogic ritual program"""
        
        ritual_id = str(uuid.uuid4())
        session_id = session_id or str(uuid.uuid4())
        
        try:
            # Parse ritual program
            ritual = json.loads(ritual_code)
            
            # Validate required fields
            required_fields = ["intent", "voice", "steps"]
            for field in required_fields:
                if field not in ritual:
                    raise ValueError(f"Missing required field: {field}")
            
            # Create execution context
            context = RitualContext(
                ritual_id=ritual_id,
                intent=ritual.get("intent"),
                voice=ritual.get("voice"),
                phase=ritual.get("phase", "active"),
                user_id=user_id,
                session_id=session_id,
                consent_granted={},
                memory_store={},
                artifacts={},
                crisis_active=False
            )
            
            # Log ritual start
            self.attestation.log_event("ritual_start", {
                "ritual_id": ritual_id,
                "intent": context.intent,
                "voice": context.voice,
                "user_id": user_id
            })
            
            # Execute steps
            step_results = []
            for i, step in enumerate(ritual["steps"]):
                try:
                    step_result = self._execute_step(step, context)
                    step_results.append(step_result)
                    
                    # Check for crisis activation
                    if step_result.get("crisis_detected"):
                        context.crisis_active = True
                        # Insert crisis response step
                        crisis_response = self._handle_crisis(context)
                        step_results.append(crisis_response)
                
                except Exception as e:
                    step_results.append({
                        "step_index": i,
                        "type": step.get("type", "unknown"),
                        "success": False,
                        "error": str(e)
                    })
            
            # Log ritual completion
            self.attestation.log_event("ritual_complete", {
                "ritual_id": ritual_id,
                "success": True,
                "steps_executed": len(step_results)
            })
            
            return {
                "success": True,
                "ritual_id": ritual_id,
                "context": asdict(context),
                "results": step_results,
                "attestation_hash": self.attestation.previous_hash
            }
            
        except Exception as e:
            # Log error
            self.attestation.log_event("ritual_error", {
                "ritual_id": ritual_id,
                "error": str(e)
            })
            
            return {
                "success": False,
                "ritual_id": ritual_id,
                "error": str(e)
            }
    
    def _execute_step(self, step: Dict[str, Any], context: RitualContext) -> Dict[str, Any]:
        """Execute a single ritual step"""

        step_type = step.get("type")

        if step_type == "consent.request":
            scopes = step.get("scopes", [])
            message = step.get("message", "Permission requested")

            granted = self.consent_manager.request_consent(scopes, message)

            for scope in scopes:
                context.consent_granted[scope] = granted

            result = {
                "type": step_type,
                "success": granted,
                "scopes": scopes,
                "granted": granted
            }

        elif step_type == "voice.speak":
            message = step.get("message", "")

            crisis_detected = self.crisis_monitor.detect_crisis(message)

            result = {
                "type": step_type,
                "success": True,
                "message": message,
                "crisis_detected": crisis_detected
            }

        elif step_type == "memory.store":
            if not context.consent_granted.get("memory", False):
                result = {
                    "type": step_type,
                    "success": False,
                    "error": "Memory access denied - no consent granted"
                }
            else:
                data = step.get("data", "")
                memory_type = step.get("type_", "artifact")

                memory_id = self.memory_vault.store_memory(
                    data=data,
                    memory_type=memory_type,
                    user_id=context.user_id,
                    session_id=context.session_id
                )

                result = {
                    "type": step_type,
                    "success": True,
                    "memory_id": memory_id,
                    "memory_type": memory_type
                }

        elif step_type and step_type.startswith("ritual."):
            result = self._execute_ritual_action(step, context)

        else:
            result = {
                "type": step_type,
                "success": True,
                "message": f"Unknown step type: {step_type}"
            }

        self.attestation.log_event("step_executed", {
            "step_type": step_type,
            "success": result.get("success", False),
            "ritual_id": context.ritual_id
        })

        return result

    def _execute_ritual_action(self, step: Dict[str, Any], context: RitualContext) -> Dict[str, Any]:
        """Execute consent-wrapped ritual actions that run embedded Python code."""

        metadata = step.get('metadata', {}) or {}
        step_type = step.get('type', 'ritual.action')

        consent_scopes = step.get('consent_scopes') or metadata.get('consent_scopes') or []
        if not consent_scopes:
            consent_scopes = self._default_scopes_for_step(step_type)

        if consent_scopes:
            consent_message = metadata.get('intent') or metadata.get('message') or f"{step_type} requires consent"
            if not self._ensure_scopes(consent_scopes, consent_message, context):
                result = {
                    'type': step_type,
                    'success': False,
                    'error': 'Consent denied',
                    'requested_scopes': consent_scopes,
                }
                self.attestation.log_event('ritual_action', {
                    'ritual_id': context.ritual_id,
                    'step_type': step_type,
                    'success': result['success'],
                    'metadata': metadata,
                    'requested_scopes': consent_scopes,
                })
                return result

        env_globals = self.execution_sandbox.create_environment(
            runtime=self,
            context=context,
            metadata=metadata,
        )
        env_locals: Dict[str, Any] = {}
        bridge = ExecutionBridge(self, context, metadata)
        env_globals['bridge'] = bridge
        env_globals['context'] = SimpleNamespace(ritual=context, metadata=metadata, bridge=bridge)

        try:
            self.execution_sandbox.execute_block(step.get('execute', ''), env_globals, env_locals, block_name='execute')
            if step.get('complete'):
                self.execution_sandbox.execute_block(step['complete'], env_globals, env_locals, block_name='complete')
            success = True
            error = None
            traceback_text = None
        except Exception as exc:
            success = False
            error = str(exc)
            traceback_text = traceback.format_exc()

        locals_summary = self._summarize_execution_locals(env_locals)

        result = {
            'type': step_type,
            'success': success,
            'metadata': metadata,
            'requested_scopes': consent_scopes,
        }
        if error:
            result['error'] = error
        if locals_summary:
            result['locals'] = locals_summary
        if traceback_text:
            result['traceback'] = traceback_text

        self.attestation.log_event('ritual_action', {
            'ritual_id': context.ritual_id,
            'step_type': step_type,
            'success': success,
            'metadata': metadata,
            'requested_scopes': consent_scopes,
            'locals': locals_summary,
            'error': error,
        })

        return result

    def _ensure_scopes(self, scopes: List[str], message: str, context: RitualContext) -> bool:
        """Ensure required consent scopes are approved before continuing."""

        needed = [
            scope
            for scope in scopes
            if not context.consent_granted.get(scope) and not self.consent_manager.check_scope(scope)
        ]
        if not needed:
            return True

        granted = self.consent_manager.request_consent(needed, message)
        if granted:
            for scope in needed:
                context.consent_granted[scope] = True
        return granted

    def _default_scopes_for_step(self, step_type: str) -> List[str]:
        """Map ritual verbs to default consent scopes."""
        mapping = {
            'ritual.api_request': ['external_api'],
            'ritual.file_access': ['file_system'],
            'ritual.file_write': ['file_system'],
            'ritual.database_query': ['database_access'],
            'ritual.database_insert': ['database_access'],
            'ritual.database_connection': ['database_access'],
        }
        return mapping.get(step_type, [])

    def _summarize_execution_locals(self, env_locals: Dict[str, Any]) -> Dict[str, Any]:
        """Create a JSON-safe summary of local variables from execution."""
        summary: Dict[str, Any] = {}
        for key, value in env_locals.items():
            if key.startswith('_'):
                continue
            summary[key] = self._safe_json_value(value)
        return summary

    def _safe_json_value(self, value: Any, depth: int = 0) -> Any:
        """Best-effort conversion of execution results into JSON-friendly structures."""
        if depth > 3:
            return repr(value)
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value
        if isinstance(value, list):
            return [self._safe_json_value(item, depth + 1) for item in value[:10]]
        if isinstance(value, tuple):
            return [self._safe_json_value(item, depth + 1) for item in list(value)[:10]]
        if isinstance(value, dict):
            items = list(value.items())[:10]
            return {str(k): self._safe_json_value(v, depth + 1) for k, v in items}
        if isinstance(value, set):
            return [self._safe_json_value(item, depth + 1) for item in list(value)[:10]]
        return repr(value)

    def _handle_crisis(self, context: RitualContext) -> Dict[str, Any]:
        """Handle crisis situation"""
        
        crisis_response = self.crisis_monitor.create_crisis_response()
        
        # Log crisis event
        self.attestation.log_event("crisis_detected", {
            "ritual_id": context.ritual_id,
            "response_mode": crisis_response["mode"]
        })
        
        return {
            "type": "crisis_response",
            "success": True,
            "data": crisis_response,
            "automatic": True
        }
