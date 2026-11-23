import json
import tempfile
import unittest
from pathlib import Path
from configforge import differences, get_path, load_config


class ConfigForgeTests(unittest.TestCase):
    def test_dotted_lookup(self):
        self.assertEqual(get_path({"app": {"port": 80}}, "app.port"), (True, 80))
        self.assertFalse(get_path({}, "app.port")[0])

    def test_nested_diff(self):
        result = differences({"app": {"port": 80}}, {"app": {"port": 90}, "debug": True})
        self.assertEqual({row[0] for row in result}, {"changed", "added"})

    def test_json_load(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "settings.json"
            path.write_text(json.dumps({"enabled": True}), encoding="utf-8")
            self.assertEqual(load_config(path), {"enabled": True})


if __name__ == "__main__":
    unittest.main()
