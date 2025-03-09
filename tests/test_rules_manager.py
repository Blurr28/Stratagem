import unittest
import pandas as pd
from core import RulesManager
from core.rules import MovingAverageCrossoverRule

class TestRulesManager(unittest.TestCase):

    def setUp(self):
        # Create a sample DataFrame for testing
        self.data = pd.DataFrame({
            "DATETIME": pd.date_range("2023-01-01", periods=10, freq="D"),
            "price": [100, 101, 102, 103, 104, 105, 106, 107, 108, 109]
        })

        # Sample configuration for a Moving Average Crossover rule
        self.config = {
            "rules": [
                {
                    "name": "MovingAverageCrossover",
                    "params": {"short_window": 3, "long_window": 5}
                }
            ]
        }

    def test_load_rules_from_config(self):
        # Instantiate RulesManager with the configuration
        manager = RulesManager(self.config)
        # Check that one rule is loaded
        self.assertEqual(len(manager.rules), 1)
        # Check that the loaded rule is an instance of MovingAverageCrossoverRule
        self.assertIsInstance(manager.rules[0], MovingAverageCrossoverRule)
        # Verify the rule parameters are set correctly
        rule_params = manager.rules[0].get_parameters()
        self.assertEqual(rule_params["short_window"], 3)
        self.assertEqual(rule_params["long_window"], 5)

    def test_apply_rules(self):
        manager = RulesManager(self.config)
        results = manager.apply_rules(self.data)
        # The results should be a dictionary with a key corresponding to the rule class name.
        self.assertIn("MovingAverageCrossoverRule", results)
        result_df = results["MovingAverageCrossoverRule"]
        # Verify that the output DataFrame has the new columns added by the rule
        self.assertIn("short_mavg", result_df.columns)
        self.assertIn("long_mavg", result_df.columns)
        self.assertIn("signal", result_df.columns)
        # Optionally, you can check that signal values are set (either 1, -1, or 0)
        self.assertTrue(result_df["signal"].isin([1, -1, 0]).all())

    def test_unknown_rule_raises_error(self):
        # Create a configuration with an unknown rule name.
        bad_config = {
            "rules": [
                {
                    "name": "UnknownRule",
                    "parameters": {}
                }
            ]
        }
        with self.assertRaises(ValueError):
            RulesManager(bad_config)

    def test_default_rules(self):
        # Test that when no rules are provided in the config, default rules are used.
        default_rule = [MovingAverageCrossoverRule(2, 4)]
        manager = RulesManager({}, default_rules=default_rule)
        self.assertEqual(len(manager.rules), 1)
        self.assertIsInstance(manager.rules[0], MovingAverageCrossoverRule)

if __name__ == "__main__":
    unittest.main()
