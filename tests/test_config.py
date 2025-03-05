import unittest
import yaml
import os
from core import Config

class TestConfig(unittest.TestCase):

    def setUp(self):
        self.sample_dict = {"name": "Cryptomancer", "version": 1.0, "enabled": True}
        self.config = Config(self.sample_dict)
        self.yaml_file = "test_config.yaml"

    def tearDown(self):
        if os.path.exists(self.yaml_file):
            os.remove(self.yaml_file)

    def test_init_dict(self):
        self.assertEqual(self.config.name, "Cryptomancer")
        self.assertEqual(self.config.version, 1.0)
        self.assertTrue(self.config.enabled)

    def test_add(self):
        self.config.add("new_key", 123)
        self.assertEqual(self.config.new_key, 123)
        with self.assertRaises(ValueError):
            self.config.add("name", "Duplicate")

    def test_fetch(self):
        self.assertEqual(self.config.fetch("name"), "Cryptomancer")
        with self.assertRaises(ValueError):
            self.config.fetch("unknown_key")

    def test_remove(self):
        self.config.remove("enabled")
        self.assertFalse(hasattr(self.config, "enabled"))
        with self.assertRaises(ValueError):
            self.config.remove("unknown_key")

    def test_save_and_load(self):
        self.config.save(self.yaml_file)
        loaded_config = Config(self.yaml_file)
        self.assertEqual(loaded_config.name, "Cryptomancer")
        self.assertEqual(loaded_config.version, 1.0)
        self.assertTrue(loaded_config.enabled)

    def test_repr(self):
        repr_str = repr(self.config)
        self.assertIn("Cryptomancer", repr_str)
        self.assertIn("1.0", repr_str)

    def test_iteration(self):
        keys = [key for key, _ in self.config]
        self.assertListEqual(keys, list(self.sample_dict.keys()))

if __name__ == "__main__":
    unittest.main()
