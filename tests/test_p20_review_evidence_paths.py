"""Meaningful guard cases for externally authored review evidence pointers."""
import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('p20qa', Path(__file__).resolve().parents[1] / 'tools/p20_validate_pre_review.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class EvidencePaths(unittest.TestCase):
    def test_rejects_escape_and_windows_absolute(self):
        for path in ['../reviewer_A/report.json', '/etc/passwd', 'C:/secret.txt', 'x/../../outside', '..\\outside', '']:
            self.assertIsNone(module.safe_evidence_path(path))

    def test_packet_relative_path_retains_containment(self):
        p = module.safe_evidence_path('results/frozen.csv')
        self.assertEqual(p, (module.CONTENT / 'results/frozen.csv').resolve())

    def test_whitespace_normalization_does_not_change_numbers(self):
        self.assertEqual(module.normalized('0.000497\n  0.5'), '0.000497 0.5')
        self.assertNotEqual(module.normalized('0.000497'), module.normalized('0.00497'))


if __name__ == '__main__':
    unittest.main()
