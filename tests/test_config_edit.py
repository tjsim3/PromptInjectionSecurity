import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import editconfig


class ConfigEditTests(unittest.TestCase):
    def test_edit_config_updates_a_setting_and_saves_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "config.py"
            with patch("builtins.input", side_effect=["learning_rate", "0.05", "done"]):
                updated = editconfig.edit_config(config=editconfig.CONFIG.copy(), path=path)

            self.assertEqual(updated["learning_rate"], 0.05)
            saved = path.read_text(encoding="utf-8")
            self.assertIn("learning_rate", saved)
            self.assertIn("0.05", saved)


if __name__ == "__main__":
    unittest.main()
