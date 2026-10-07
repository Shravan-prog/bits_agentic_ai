import importlib.util
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch


ROOT = Path(__file__).resolve().parents[1]


def load_exercise(relative_path, module_name):
    """Load one exercise while keeping its week-specific utils package isolated."""
    path = ROOT / relative_path
    for name in list(sys.modules):
        if name == "utils" or name.startswith("utils."):
            del sys.modules[name]
    sys.path.insert(0, str(path.parent))
    try:
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path.pop(0)


class Week1Tests(unittest.TestCase):
    def test_assistant_calculator(self):
        module = load_exercise(
            "Week 1/skeleton/01_assistant_vs_agent.py", "week1_assistant"
        )
        self.assertEqual(module.calculator("0.185 * 2480 + 365"), 823.8)

    def test_safe_calculator_and_dispatch(self):
        module = load_exercise(
            "Week 1/skeleton/06_multi_tool_agent.py", "week1_multi_tool"
        )
        self.assertEqual(module.safe_calc("3 * 25 + 2 * 40"), 155)
        self.assertEqual(module.dispatch("price_lookup", "widget"), 25)
        self.assertEqual(module.dispatch("calc", "10 / 2"), 5)
        self.assertTrue(module.safe_calc("__import__('os')").startswith("error:"))
        self.assertTrue(module.dispatch("missing", "x").startswith("error:"))

    def test_advanced_schema_and_calculator(self):
        module = load_exercise(
            "Week 1/skeleton/07_advanced_agent.py", "week1_advanced"
        )
        self.assertEqual(module.calculator("23 * 7 + 19"), 180)
        self.assertEqual(module.TOOLS[0]["function"]["name"], "calculator")
        required = module.TOOLS[0]["function"]["parameters"]["required"]
        self.assertEqual(required, ["expression"])


class Week2Tests(unittest.TestCase):
    def test_weather_tool_schema(self):
        module = load_exercise(
            "Week 2/skeleton/01_first_tool_call.py", "week2_first_tool"
        )
        self.assertEqual(module.get_weather(" Dubai "), "38C and sunny")
        self.assertEqual(module.TOOLS[0]["function"]["name"], "get_weather")
        self.assertEqual(
            module.TOOLS[0]["function"]["parameters"]["required"], ["city"]
        )

    def test_function_schema_dispatch(self):
        module = load_exercise(
            "Week 2/skeleton/02_function_schemas.py", "week2_schemas"
        )
        call = SimpleNamespace(
            name="convert_currency",
            arguments={"amount": 10, "to_currency": "AED"},
        )
        self.assertEqual(module.run_tool(call), 36.7)
        bad_call = SimpleNamespace(name="convert_currency", arguments={})
        self.assertTrue(module.run_tool(bad_call).startswith("error:"))

    def test_reusable_agent_loop(self):
        module = load_exercise(
            "Week 2/skeleton/03_tool_calling_agent.py", "week2_agent"
        )
        tool_call = SimpleNamespace(name="add", arguments={"a": 2, "b": 3}, id="1")
        tool_result = SimpleNamespace(
            wants_tools=True,
            tool_calls=[tool_call],
            raw_message={"role": "assistant", "tool_calls": ["placeholder"]},
        )
        final_result = SimpleNamespace(wants_tools=False, text="5")
        fake_client = Mock()
        fake_client.chat.side_effect = [tool_result, final_result]

        agent = module.ToolAgent()
        agent.client = fake_client
        agent.register(module.add, module.ADD_SCHEMA)
        self.assertEqual(agent.run("Add two and three"), "5")
        self.assertEqual(fake_client.chat.call_count, 2)

    def test_temperature_validation_and_success(self):
        module = load_exercise(
            "Week 2/skeleton/04_api_tool.py", "week2_api"
        )
        self.assertTrue(module.get_current_temperature("").startswith("error:"))

        geo_response = Mock()
        geo_response.json.return_value = {
            "results": [{"latitude": 25.2, "longitude": 55.3, "name": "Dubai"}]
        }
        weather_response = Mock()
        weather_response.json.return_value = {"current": {"temperature_2m": 35.5}}
        with patch.object(
            module.requests, "get", side_effect=[geo_response, weather_response]
        ):
            self.assertEqual(module.get_current_temperature("Dubai"), "Dubai: 35.5°C")

    def test_elevation_success_and_validation(self):
        module = load_exercise(
            "Week 2/skeleton/05_multi_api_agent.py", "week2_multi_api"
        )
        module._geocode = lambda city: ((25.2, 55.3, "Dubai"), None)
        response = Mock()
        response.json.return_value = {"elevation": [12.0]}
        with patch.object(module.requests, "get", return_value=response):
            self.assertEqual(
                module.get_elevation("Dubai"), "Dubai: 12.0 m above sea level"
            )

        response.json.return_value = {"elevation": []}
        with patch.object(module.requests, "get", return_value=response):
            self.assertTrue(module.get_elevation("Dubai").startswith("error:"))

    def test_webhook_validation_and_mock(self):
        module = load_exercise(
            "Week 2/skeleton/06_webhook_tool.py", "week2_webhook"
        )
        module.WEBHOOK_URL = None
        self.assertTrue(module.trigger_workflow("").startswith("error:"))
        self.assertTrue(module.trigger_workflow("event", []).startswith("error:"))
        result = module.trigger_workflow(" email_summary ", {"text": "Passed"})
        self.assertEqual(result["status"], "accepted")
        self.assertEqual(result["event"], "email_summary")


if __name__ == "__main__":
    unittest.main()
