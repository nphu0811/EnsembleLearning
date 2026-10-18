"""Synthetic-only scientific metadata reconciliation (no TRAIN or TEST)."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from p21_science_acceptance import acceptable_science_worker, ARM_IDS

def make():
    metric={
        "tn":70,"fp":10,"fn":5,"tp":15,
        "validation_rows":100,"threshold":0.5,
        "macro_f1":((140/155)+(30/45))/2,
        "mcc":(15*70-10*5)/((25*20*80*75)**.5),
        "attack_precision":15/25,"attack_recall":15/20,
        "fpr":10/80,"fnr":5/20
    }
    names=["f"+str(i) for i in range(17)]
    return {
        "passed":True,
        "scope":"P21_TRAIN_REUSED_POST_HOC_SCIENCE_INTERNAL_VALIDATION_ONLY",
        "source_sha256":"a"*64,"protocol_sha256":"b"*64,
        "seed":1103,"train_rows":175341,"fit_subset_rows":60000,
        "fit_pool_rows":140272,"validation_rows":35069,
        "fit_row_ids_sha256":"c"*64,
        "split":{"group_disjoint":True,"row_disjoint":True,
                 "validation_evaluation_performed":False,"validation_rows":35069},
        "selector":{"validation_used":False,"feature_names":names,
                    "feature_names_sha256":"d"*64,"selector_fit_calls":15,
                    "sample_rows_per_selection_seed":35000},
        "stack_inner_cv":{"type":"StratifiedGroupKFold","n_splits":3,"seed":137,
                          "exact_vector_group_disjoint":True,
                          "amendment":"P21_PRE_FULL_SCIENCE_INNER_GROUP_SPLIT_2026-10-18"},
        "arm_ids":list(ARM_IDS),
        "arms":[
            {"arm":a,"fit_row_ids_sha256":"c"*64,
             "fit_source_rows":60000,
             "actual_model_fit_rows":(81670 if i==3 else 60000),
             "original_feature_count":17 if i==1 else 42,
             "class_weight":"balanced" if i==2 else None,
             "fit_seconds":12.5,"predict_seconds":1.0,
             "metrics":{**metric,
                        "tn":24500,"fp":1000,"fn":1500,"tp":8069,
                        "validation_rows":35069,
                        "macro_f1":((2*24500/(2*24500+1000+1500))+
                                    (2*8069/(2*8069+1000+1500)))/2,
                        "mcc":(8069*24500-1000*1500)/
                            (((8069+1000)*(8069+1500)*(24500+1000)*(24500+1500))**.5),
                        "attack_precision":8069/(8069+1000),
                        "attack_recall":8069/(8069+1500),
                        "fpr":1000/(1000+24500),
                        "fnr":1500/(1500+8069)}} for i,a in enumerate(ARM_IDS)
        ],
        "official_test_opened":False,"historical_p9_modified":False,
        "validation_used_for_tuning":False,"model_artifacts_saved":False,
    }

class TestAcceptance(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(acceptable_science_worker(make(),1103,"a"*64,"b"*64))
    def test_reject_changed_fit_hash(self):
        d=make();d["arms"][2]["fit_row_ids_sha256"]="z"*64
        self.assertFalse(acceptable_science_worker(d,1103,"a"*64,"b"*64))
    def test_reject_mcc_tamper(self):
        d=make();d["arms"][3]["metrics"]["mcc"]=0.9
        self.assertFalse(acceptable_science_worker(d,1103,"a"*64,"b"*64))
    def test_reject_missing_arm(self):
        d=make();d["arms"].pop()
        self.assertFalse(acceptable_science_worker(d,1103,"a"*64,"b"*64))
    def test_reject_test_or_tuning(self):
        for field in ("official_test_opened","validation_used_for_tuning"):
            d=make();d[field]=True
            self.assertFalse(acceptable_science_worker(d,1103,"a"*64,"b"*64))
    def test_reject_wrong_seed_and_unbalanced_oversample(self):
        d=make()
        self.assertFalse(acceptable_science_worker(d,2207,"a"*64,"b"*64))
        d["arms"][3]["actual_model_fit_rows"]=59999
        self.assertFalse(acceptable_science_worker(d,1103,"a"*64,"b"*64))
    def test_reject_non_group_cv(self):
        d=make();d["stack_inner_cv"]["type"]="StratifiedKFold"
        self.assertFalse(acceptable_science_worker(d,1103,"a"*64,"b"*64))

if __name__=="__main__":
    unittest.main()
