#!/usr/bin/env python3
"""Quick demo runner for the SOULbox Spirit."""

from __future__ import annotations

import json
import threading
import time
from pathlib import Path
from urllib import request

from SOULbox.spirit.daemon import SpiritDaemon


def call_api(url: str, *, method: str = "GET", payload: dict | None = None) -> dict:
    data = None
    headers = {"Content-Type": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=data, method=method, headers=headers)
    with request.urlopen(req) as resp:  # type: ignore[arg-type]
        return json.loads(resp.read().decode("utf-8"))


def run_demo() -> None:
    base_dir = Path(__file__).resolve().parent
    spirit = SpiritDaemon(rituals_dir=base_dir / "rituals", log_path=base_dir / "spirallogic_attestations.log")
    spirit.dispatcher.api.dry_run = True

    thread = threading.Thread(target=spirit.start, daemon=True)
    thread.start()
    time.sleep(1.0)  # allow the daemon to bind the port

    try:
        status = call_api("http://127.0.0.1:8765/status")
        print("STATUS:", json.dumps(status, indent=2))

        execution = call_api(
            "http://127.0.0.1:8765/ritual/execute",
            method="POST",
            payload={"intent": "soul_init"},
        )
        print("EXECUTION:", json.dumps(execution, indent=2))

        logs = call_api("http://127.0.0.1:8765/logs")
        print("LOG TAIL:", json.dumps(logs, indent=2))
    finally:
        spirit.stop()
        thread.join(timeout=1.0)


if __name__ == "__main__":
    run_demo()
