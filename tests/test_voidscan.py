import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from voidscan.main import main
from voidscan.report import write_report
from voidscan.system import collect_system


class VoidscanTests(unittest.TestCase):
    def test_report_structure_is_json(self):
        data = {"system": {}, "hardware": {}, "performance": {}, "network": {}}
        with tempfile.TemporaryDirectory() as folder:
            path = write_report(data, Path(folder) / "report.json")
            self.assertEqual(json.loads(path.read_text()), data)

    def test_missing_os_release_is_handled(self):
        with patch("voidscan.system.Path.read_text", side_effect=OSError):
            result = collect_system()
        self.assertEqual(result["distribution"], "N/A")
        self.assertNotEqual(result["kernel"], "N/A")

    def test_version_command(self):
        with self.assertRaises(SystemExit) as exit_info:
            main(["--version"])
        self.assertEqual(exit_info.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
