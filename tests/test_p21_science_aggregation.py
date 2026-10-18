"""Synthetic-only aggregation QA; not real measured results."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from p21_science_aggregate import describe, summarize, markdown_report
from p21_science_acceptance import ARM_IDS,SEEDS


def fabricated():
    seen={}
    for seed in SEEDS:
        seen[seed]={"worker":{
            "fit_row_ids_sha256":str(seed),
            "selector":{"feature_names":["f"+str(i) for i in range(17)],
                        "feature_names_sha256":"a"*64},
            "arms":[{"arm":arm,"fit_seconds":8.0+j,
                     "metrics":{"macro_f1":0.7+j*0.01+seed/1e7,
                                "mcc":0.5+j*0.01,
                                "attack_precision":0.8+j*0.005,
                                "attack_recall":0.75+j*0.005,
                                "fpr":0.1+j*.005,
                                "fnr":0.25-j*.005}}
                    for j,arm in enumerate(ARM_IDS)]
        }}
    return seen


class TestAggregate(unittest.TestCase):
    def test_describe_rejects_partial(self):
        with self.assertRaises(ValueError):
            describe([1,2,3,4])

    def test_complete_matrix_differences(self):
        p,a,c=summarize(fabricated())
        self.assertEqual(len(p),5)
        self.assertEqual(len(a),5)
        self.assertEqual(len(c),4)
        self.assertAlmostEqual(c["RQ2_RF17_MINUS_RF42"]["macro_f1"]["mean"],.01)
        self.assertAlmostEqual(c["RQ5_OVERSAMPLE_MINUS_NONE"]["fnr"]["mean"],-.015)

    def test_report_warns_shared_holdout(self):
        p,a,c=summarize(fabricated())
        text=markdown_report({"arm_summary":a,"contrasts":c})
        self.assertIn("POST-HOC",text)
        self.assertIn("same",text.lower() if "same" in text.lower() else text.lower())
        self.assertIn("RQ1_STACK42_MINUS_RF42",text)

if __name__=="__main__":
    unittest.main()
