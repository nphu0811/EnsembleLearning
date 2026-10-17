"""Read-only P21 reported-smoke audit fixtures (no raw dataset, no ML fit)."""
from __future__ import annotations
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("p21_pilot_acceptance",ROOT/"tools/p21_verify_pilot_reports.py")
MOD=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)
BASE=ROOT/"results/controlled_extensions/p21_train_only_pilot_rf42_01"
START=json.loads((BASE/"start.json").read_text(encoding="utf-8"))
RUN=json.loads((BASE/"run_report.json").read_text(encoding="utf-8"))
WORKER=json.loads((BASE/"worker/worker_result.json").read_text(encoding="utf-8"))
CONTRACT=json.loads((ROOT/"config/p21_train_only_protocol_2026_10_18.json").read_text(encoding="utf-8"))


def fail_ids(st,ru,wo,co):
    return [x["check"] for x in MOD.checks_for_reports(st,ru,wo,co) if not x["passed"]]


class P21PilotReportQA(unittest.TestCase):
    def test_real_report_consistency_metadata(self):
        self.assertEqual([],fail_ids(START,RUN,WORKER,CONTRACT))

    def test_reject_forged_test_or_model_score(self):
        r=deepcopy(RUN);w=deepcopy(WORKER)
        w["validation_predicted"]=True
        self.assertIn("NO official TEST, validation prediction or scientific metrics",fail_ids(START,r,w,CONTRACT))
        r=deepcopy(RUN);w=deepcopy(WORKER)
        r["official_test_opened"]=True
        self.assertIn("NO official TEST, validation prediction or scientific metrics",fail_ids(START,r,w,CONTRACT))

    def test_reject_resource_cap_or_missing_stop(self):
        r=deepcopy(RUN)
        r["peak_tree_rss_bytes"]=2*MOD.GIB
        self.assertIn("observed watchdog headroom",fail_ids(START,r,WORKER,CONTRACT))
        r=deepcopy(RUN);r["stop_reason"]="TIMEOUT"
        self.assertIn("completed without watchdog failure",fail_ids(START,r,WORKER,CONTRACT))

    def test_reject_drift_in_model_config_and_split(self):
        w=deepcopy(WORKER)
        w["model_config"]["n_estimators"]=300
        self.assertIn("fixed 42-feature RF configuration",fail_ids(START,RUN,w,CONTRACT))
        w=deepcopy(WORKER)
        w["split"]["group_disjoint"]=False
        self.assertIn("TRAIN-only group-disjoint single split",fail_ids(START,RUN,w,CONTRACT))

    def test_detect_start_worker_report_mismatch(self):
        s=deepcopy(START);s["train_sha256"]="bad"
        self.assertIn("start/run provenance and state consistent",fail_ids(s,RUN,WORKER,CONTRACT))
        r=deepcopy(RUN);r["worker_checks"]["pilot_fit_rows"]=100
        self.assertIn("worker nested report equals separate result",fail_ids(START,r,WORKER,CONTRACT))


if __name__=="__main__":
    unittest.main()
