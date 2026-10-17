"""No real training: RQ5 worker-report acceptance regression."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from p21_rq5_pilot_supervisor import acceptable_worker

def sample():
    rows=8000
    before={"0":2555,"1":5445}
    arms=[]
    for name in ("NONE","BALANCED","FIT_ONLY_RANDOM_OVERSAMPLE"):
        after=before.copy() if name!="FIT_ONLY_RANDOM_OVERSAMPLE" else {"0":5445,"1":5445}
        arms.append({"arm":name,"fit_rows":rows,"fitted_rows":sum(after.values()),
                     "before":before.copy(),"after":after,
                     "class_weight":"balanced" if name=="BALANCED" else None,
                     "scientific_metrics_calculated":False})
    return {"passed":True,"scope":"P21_RQ5_FIT_ONLY_RESOURCE_PILOT; no RQ result",
            "source_sha256":"a"*64,"pilot_fit_rows":rows,"feature_count":42,
            "arm_names":["NONE","BALANCED","FIT_ONLY_RANDOM_OVERSAMPLE"],
            "split":{"group_disjoint":True,"validation_evaluation_performed":False},
            "validation_predicted":False,"official_test_opened":False,
            "scientific_metrics_calculated":False,"model_artifact_saved":False,"arms":arms}

class TestAcceptance(unittest.TestCase):
    def test_accept(self):
        self.assertTrue(acceptable_worker(sample(),8000,"a"*64))
    def test_disallow_validation(self):
        x=sample(); x["validation_predicted"]=True
        self.assertFalse(acceptable_worker(x,8000,"a"*64))
    def test_disallow_test(self):
        x=sample(); x["official_test_opened"]=True
        self.assertFalse(acceptable_worker(x,8000,"a"*64))
    def test_oversample_count(self):
        x=sample(); x["arms"][2]["after"]["0"]=5000
        self.assertFalse(acceptable_worker(x,8000,"a"*64))
    def test_unmatched_balanced(self):
        x=sample(); x["arms"][1]["after"]["0"]=5000
        self.assertFalse(acceptable_worker(x,8000,"a"*64))
    def test_missing_arm(self):
        x=sample(); x["arms"].pop()
        self.assertFalse(acceptable_worker(x,8000,"a"*64))

if __name__=="__main__":
    unittest.main()
