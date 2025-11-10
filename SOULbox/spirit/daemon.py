"""Resident SOULbox Spirit daemon."""

from __future__ import annotations

import json
import logging
import threading
from datetime import datetime, timezone
from dataclasses import asdict
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, Optional

import sys

# Ensure the runtime modules are on the path
RUNTIME_DIR = Path(__file__).resolve().parent.parent / "runtime"
sys.path.insert(0, str(RUNTIME_DIR))

from spirallogic_runtime import SpiralLogic  # type: ignore  # pylint: disable=wrong-import-position
from unicode_sanitizer import sanitize_for_windows_terminal  # type: ignore  # pylint: disable=wrong-import-position

from .intent_router import IntentRouter, IntentRoute
from .consent_policy import ConsentDecision, ConsentPolicy
from .action_dispatcher import ActionDispatcher

logging.basicConfig(level=logging.INFO)


class SpiritDaemon:
    """Long-lived process that executes SpiralLogic rituals on demand."""

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 8765,
        rituals_dir: Optional[Path] = None,
        log_path: Optional[Path] = None,
    ) -> None:
        self.host = host
        self.port = port
        self.rituals_dir = rituals_dir or Path(__file__).resolve().parent.parent / "rituals"
        self.log_path = log_path or Path(__file__).resolve().parent.parent / "spirallogic_attestations.log"
        self.intent_router = IntentRouter(self.rituals_dir)
        self.consent_policy = ConsentPolicy(self.log_path)
        self.dispatcher = ActionDispatcher(self.consent_policy)
        self.runtime = SpiralLogic(consent_callback=self._consent_callback)
        self._server: Optional[ThreadingHTTPServer] = None
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------
    def start(self) -> None:
        """Start the HTTP server and block until interrupted."""
        server_address = (self.host, self.port)

        daemon = self

        class SpiritRequestHandler(BaseHTTPRequestHandler):
            """Inline handler bound to the surrounding daemon instance."""

            def _send_json(self, payload: Dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
                body = json.dumps(payload).encode("utf-8")
                self.send_response(status.value)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            # GET endpoints -------------------------------------------------
            def do_GET(self) -> None:  # noqa: N802 - built-in interface
                try:
                    if self.path == "/status":
                        payload = {
                            "spirit": "SOULbox",
                            "status": "awake",
                            "intents": list(daemon.intent_router.available_intents().keys()),
                        }
                        self._send_json(payload)
                    elif self.path == "/intents":
                        payload = {
                            intent: asdict(route)
                            for intent, route in daemon.intent_router.available_intents().items()
                        }
                        self._send_json(payload)
                    elif self.path == "/logs":
                        log_excerpt = daemon._read_log_tail()  # pylint: disable=protected-access
                        self._send_json({"attestations": log_excerpt})
                    else:
                        self._send_json({"error": "Not Found"}, HTTPStatus.NOT_FOUND)
                except Exception as exc:  # pragma: no cover - defensive
                    logging.exception("GET handler error: %s", exc)
                    self._send_json({"error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)

            # POST endpoints ------------------------------------------------
            def do_POST(self) -> None:  # noqa: N802 - built-in interface
                length = int(self.headers.get("Content-Length", "0"))
                raw_body = self.rfile.read(length) if length else b"{}"
                try:
                    body = json.loads(raw_body.decode("utf-8"))
                except json.JSONDecodeError:
                    self._send_json({"error": "Invalid JSON payload"}, HTTPStatus.BAD_REQUEST)
                    return

                try:
                    if self.path == "/ritual/execute":
                        response = daemon._handle_execute(body)  # pylint: disable=protected-access
                        self._send_json(response, HTTPStatus.OK if response.get("success") else HTTPStatus.BAD_REQUEST)
                    elif self.path == "/refresh":
                        daemon.intent_router.refresh()
                        self._send_json({"status": "refreshed"})
                    else:
                        self._send_json({"error": "Not Found"}, HTTPStatus.NOT_FOUND)
                except Exception as exc:  # pragma: no cover - defensive
                    logging.exception("POST handler error: %s", exc)
                    self._send_json({"error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)

            def log_message(self, format: str, *args: Any) -> None:  # noqa: A003 - match BaseHTTPRequestHandler
                logging.info("SpiritDaemon: " + format, *args)

        self._server = ThreadingHTTPServer(server_address, SpiritRequestHandler)
        banner = sanitize_for_windows_terminal("🌀 SOULbox Spirit listening on http://%s:%s" % server_address)
        logging.info(banner)
        try:
            self._server.serve_forever()
        except KeyboardInterrupt:  # pragma: no cover
            logging.info("SOULbox Spirit shutting down")
        finally:
            self.stop()

    def stop(self) -> None:
        """Stop the HTTP server if running."""
        if self._server:
            self._server.shutdown()
            self._server.server_close()
            self._server = None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _handle_execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        intent = payload.get("intent")
        ritual_override = payload.get("ritual")
        user_id = payload.get("user_id", "soulbox_spirit")
        context = payload.get("context") or {}
        post_actions = payload.get("post_actions") or []

        if ritual_override:
            ritual_path = self.rituals_dir / ritual_override
            ritual_name = Path(ritual_override).stem
            route = IntentRoute(ritual_name=ritual_name)
        elif intent:
            route = self.intent_router.get_route(intent)
            if not route:
                return {"success": False, "error": f"Unknown intent '{intent}'"}
            ritual_path = self.rituals_dir / f"{route.ritual_name}.sl"
        else:
            return {"success": False, "error": "Must provide 'intent' or 'ritual'"}

        if not ritual_path.exists():
            return {"success": False, "error": f"Ritual file not found: {ritual_path}"}

        ritual_code = ritual_path.read_text(encoding="utf-8")

        # Validate consent scopes before executing
        scopes = payload.get("scopes") or getattr(route, "scopes", [])
        decision = self.consent_policy.evaluate(scopes=scopes, context=context, intent=intent or route.ritual_name)
        if not decision.allowed:
            return {
                "success": False,
                "error": "Consent denied",
                "decision": decision.to_dict(),
            }

        with self._lock:
            result = self.runtime.execute(ritual_code, user_id=user_id)

        response: Dict[str, Any] = {
            "success": result.get("success", False),
            "ritual_id": result.get("ritual_id"),
            "context": result.get("context"),
            "results": result.get("results"),
            "decision": decision.to_dict(),
        }

        if response["success"]:
            actions = post_actions or getattr(route, "post_actions", [])
            if actions:
                dispatch_results = self.dispatcher.dispatch(actions, intent=intent or route.ritual_name, context=context)
                response["post_actions"] = [result.to_dict() for result in dispatch_results]
                for action_result in dispatch_results:
                    self._append_attestation({
                        "event": "post_action",
                        "intent": intent or route.ritual_name,
                        "action": action_result.action,
                        "success": action_result.success,
                        "decision": action_result.decision.to_dict(),
                    })

        self._append_attestation({
            "event": "ritual_execution",
            "intent": intent or route.ritual_name,
            "ritual": str(ritual_path.name),
            "success": response["success"],
            "decision": response["decision"],
        })

        return response

    def _consent_callback(self, request: Any) -> bool:
        """Called by SpiralLogic when a ritual requests consent mid-execution."""
        decision = self.consent_policy.evaluate(
            scopes=getattr(request, "scopes", []),
            context={},
            intent="runtime_request",
            message=getattr(request, "message", ""),
        )
        self._append_attestation(
            {
                "event": "runtime_consent",
                "scopes": getattr(request, "scopes", []),
                "message": getattr(request, "message", ""),
                "allowed": decision.allowed,
                "decision": decision.to_dict(),
            }
        )
        return decision.allowed

    def _append_attestation(self, entry: Dict[str, Any]) -> None:
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        entry_with_ts = {"timestamp": datetime.now(timezone.utc).isoformat(), **entry}
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry_with_ts) + "\n")

    def _read_log_tail(self, limit: int = 100) -> Any:
        if not self.log_path.exists():
            return []
        with self.log_path.open("r", encoding="utf-8") as handle:
            lines = handle.readlines()[-limit:]
        return [json.loads(line) for line in lines if line.strip()]


def main() -> None:  # pragma: no cover - manual entry point
    spirit = SpiritDaemon()
    spirit.start()


if __name__ == "__main__":  # pragma: no cover
    main()
