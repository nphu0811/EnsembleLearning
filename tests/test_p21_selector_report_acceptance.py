"""Read-only selector pilot JSON acceptance tests; never touch raw TRAIN/TEST."""
from __future__ import annotations

from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "p21_selector_report_validator", ROOT / "tools/p21_verify_selector_pilot_reports.py"
)
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)
PILOT = ROOT / "results/controlled_extensions/p21_train_only_pilot_selector17_01"
START = json.loads((PILOT / "start.json").read_text(encoding="utf-8"))
RUN = json.loads((PILOT / "run_report.json").read_text(encoding="utf-8"))
WORKER = json.loads((PILOT / "worker/worker_result.json").read_text(encoding="utf-8"))
CONTRACT = json.loads((ROOT / "config/p21_train_only_protocol_2026_10_18.json").read_text(encoding="utf-8"))


def failed(s=START, r=RUN, w=WORKER, c=CONTRACT):
    return [x["check"] for x in VALIDATOR.verify_reports(s, r, w, c) if not x["passed"]]


class P21SelectorReportTests(unittest.TestCase):
    def test_original_three_committed_reports_consistent(self):
        self.assertEqual(failed(), [])

    def test_report_protocol_sha_resolves(self):
        self.assertTrue(VALIDATOR.protocol_sha_matches(
            ROOT / "config/p21_train_only_protocol_2026_10_18.json",
            RUN["protocol_sha256"]))

    def test_test_access_or_validation_score_falsified(self):
        for section, field in (("worker", "official_test_opened"),
                               ("worker", "scientific_metrics_calculated"),
                               ("worker", "validation_predicted"),
                               ("run", "official_test_opened")):
            r, w = deepcopy(RUN), deepcopy(WORKER)
            if section == "run":
                r[field] = True
            else:
                w[field] = True
            with self.subTest(section=section, field=field):
                self.assertIn("strict fit-only/validation/test/pilot outputs",
                              failed(r=r, w=w))

    def test_incorrect_selector_calls_or_changed_feature_count(self):
        for field, value in (("selector_fit_calls", 14),
                             ("selected_feature_count", 18),
                             ("no_validation_rows_used", False),
                             ("forced_top17_count", 2),
                             ("pilot_feature_names_saved", True)):
            w = deepcopy(WORKER)
            w["selection"][field] = value
            self.assertTrue(failed(w=w), field)

    def test_reject_forged_pass_with_timeout_or_ram_breach(self):
        for field, value in (("stop_reason", "TIMEOUT"),
                             ("exit_code", 2),
                             ("peak_tree_rss_bytes", 2 * VALIDATOR.GIB),
                             ("minimum_system_available_bytes", 1)):
            r = deepcopy(RUN)
            r[field] = value
            with self.subTest(field=field):
                self.assertTrue(failed(r=r))

    def test_start_and_worker_report_mutations_detected(self):
        s = deepcopy(START)
        s["train_sha256"] = "0" * 64
        self.assertIn("start JSON is immutable pre-run snapshot", failed(s=s))
        r = deepcopy(RUN)
        r["worker_checks"]["pilot_fit_rows"] = 1
        self.assertIn("separate worker JSON matches nested worker evidence", failed(r=r))

    def test_reject_unrelated_or_traversal_pilot_directories(self):
        for path in (
            "../", "/tmp", "results/controlled_extensions/p21_train_only_pilot_rf42_01"
        ):
            with self.subTest(path=path):
                with self.assertRaises((ValueError, OSError)):
                    VALIDATOR.safe_pilot_dir(path)


if __name__ == "__main__":
    unittest.main()
