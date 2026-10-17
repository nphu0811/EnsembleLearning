"""Synthetic-only safety report acceptance for STACK-LITE pilot."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from p21_stack_lite_pilot_supervisor import acceptable_worker

def evidence():
    return {
        "passed":True,"scope":"P21_STACK_LITE_FIT_ONLY_RESOURCE_PILOT; no RQ result",
        "source_sha256":"x"*64,"pilot_fit_rows":8000,
        "feature_count":42,"pilot_component":"A4_STACK42_LITE",
        "inner_cv_folds":3,"inner_cv_seed":137,"fit_seconds":30.5,
        "split":{"group_disjoint":True,"validation_evaluation_performed":False},
        "official_test_opened":False,"validation_predicted":False,
        "scientific_metrics_calculated":False,"model_artifact_saved":False
    }
class StackAcceptance(unittest.TestCase):
    def test_accept_scoped(self):
        self.assertTrue(acceptable_worker(evidence(),8000,"x"*64))
    def test_reject_validation(self):
        d=evidence();d["validation_predicted"]=True
        self.assertFalse(acceptable_worker(d,8000,"x"*64))
    def test_reject_test(self):
        d=evidence();d["official_test_opened"]=True
        self.assertFalse(acceptable_worker(d,8000,"x"*64))
    def test_reject_cv_change(self):
        d=evidence();d["inner_cv_folds"]=2
        self.assertFalse(acceptable_worker(d,8000,"x"*64))
    def test_reject_source_change(self):
        self.assertFalse(acceptable_worker(evidence(),8000,"y"*64))
    def test_reject_performance_metrics(self):
        d=evidence();d["scientific_metrics_calculated"]=True
        self.assertFalse(acceptable_worker(d,8000,"x"*64))
if __name__=="__main__":
    unittest.main()
