import json
import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from SOULbox.spirit.daemon import SpiritDaemon
from SOULbox.spirit.intent_router import IntentRouter
from SOULbox.spirit.consent_policy import ConsentPolicy

BASE_DIR = Path(__file__).resolve().parents[1]
RITUALS_DIR = BASE_DIR / "rituals"
INTENT_MAP = BASE_DIR / "intent_map.json"


class IntentRouterTests(unittest.TestCase):
    def test_intent_router_loads_map(self) -> None:
        router = IntentRouter(RITUALS_DIR, INTENT_MAP)
        route = router.get_route("soul_init")
        self.assertIsNotNone(route)
        self.assertEqual(route.ritual_name, "soul_init")
        self.assertTrue(route.post_actions)


class ConsentPolicyTests(unittest.TestCase):
    def test_manual_scope_requires_escalation(self) -> None:
        policy = ConsentPolicy(BASE_DIR / "spirallogic_attestations.log")
        decision = policy.evaluate(scopes=["ui_automation"], context={}, intent="test")
        self.assertFalse(decision.allowed)
        self.assertTrue(decision.escalation_required)


class SpiritDaemonTests(unittest.TestCase):
    def test_handle_execute_runs_ritual_and_post_action(self) -> None:
        with TemporaryDirectory() as tmp:
            log_path = Path(tmp) / "attestations.log"
            prefs_path = Path(tmp) / "prefs.json"
            prefs_path.write_text(json.dumps({"default": "local-llm", "consent_summary": "summary-model"}))
            os.environ["SOULBOX_LLM_PREFS"] = str(prefs_path)

            try:
                spirit = SpiritDaemon(rituals_dir=RITUALS_DIR, log_path=log_path)
                spirit.dispatcher.api.dry_run = True
                spirit.dispatcher.llm.dry_run = True

                response = spirit._handle_execute({"intent": "soul_init"})
                self.assertTrue(response["success"])
                self.assertIn("post_actions", response)

                actions = {entry["action"]["type"]: entry for entry in response["post_actions"]}
                self.assertEqual(actions["llm"]["response"]["status"], "dry_run")
                self.assertEqual(actions["llm"]["response"].get("model"), "summary-model")
                self.assertEqual(actions["api"]["response"]["status"], "dry_run")

                contents = log_path.read_text().strip().splitlines()
                self.assertTrue(contents)
                events = [json.loads(line)["event"] for line in contents]
                self.assertIn("ritual_execution", events)
                self.assertIn("post_action", events)
            finally:
                os.environ.pop("SOULBOX_LLM_PREFS", None)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
