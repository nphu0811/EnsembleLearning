"""Completely fabricated dataset; verify P21 grouped stacking + locked metrics."""
import sys
from pathlib import Path
import unittest
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from p21_science_core import inner_group_folds, make_rf, make_stacking, binary_metrics, fit_ids_digest

CFG={
    "source":{"categorical_predictors":["proto","service","state"]},
    "model":{
        "common_rf":{"n_estimators":8,"min_samples_leaf":2,
                     "max_features":0.5,"bootstrap":True},
        "stacking_lite":{
            "inner_cv":3,"inner_cv_seed":137,
            "stack_method":"predict_proba","passthrough":False,
            "base_lr":{"C":1.0,"solver":"liblinear"},
            "base_dt":{"min_samples_leaf":2},
            "meta_lr":{"C":0.5,"solver":"liblinear","class_weight":None}
        }
    }
}

class TestScientificCore(unittest.TestCase):
    def data(self):
        rs=np.random.default_rng(404)
        # 72 distinct vectors x 2 identical copies, with both labels;
        # grouping must keep each duplicate pair in a common fold.
        a=pd.DataFrame({
            "duration":np.arange(72,dtype=float)+1.0,
            "size":rs.integers(1,120,72).astype(float),
            "proto":rs.choice(["tcp","udp"],72),
            "service":rs.choice(["http","dns"],72),
            "state":rs.choice(["FIN","CON"],72),
        })
        y=np.arange(72)%2
        X=pd.concat([a,a],ignore_index=True)
        return X,np.tile(y,2)

    def test_groups_never_overlap(self):
        X,y=self.data()
        folds=inner_group_folds(X,y)
        self.assertEqual(len(folds),3)
        seen=[]
        for train_idx,val_idx in folds:
            self.assertFalse(set(train_idx)&set(val_idx))
            self.assertEqual(set(np.unique(y[train_idx])),{0,1})
            self.assertEqual(set(np.unique(y[val_idx])),{0,1})
            # all exact copies belong on same side
            hashes=pd.util.hash_pandas_object(X,index=False).to_numpy()
            self.assertFalse(set(hashes[train_idx])&set(hashes[val_idx]))
            seen.extend(val_idx.tolist())
        self.assertEqual(sorted(seen),list(range(len(y))))

    def test_actual_synthetic_stack_fit(self):
        X,y=self.data()
        folds=inner_group_folds(X,y)
        features=list(X.columns)
        rf=make_rf(features,CFG,1103)
        stack=make_stacking(features,CFG,1103,folds)
        rf.fit(X,y)
        stack.fit(X,y)
        for m in (rf,stack):
            p=m.predict_proba(X)[:,1]
            out=binary_metrics(y,p)
            self.assertEqual(out["validation_rows"],len(y))
            self.assertEqual(out["threshold"],0.5)
            self.assertGreaterEqual(out["macro_f1"],0)
            self.assertLessEqual(out["macro_f1"],1)

    def test_invalid_probability_rejected(self):
        with self.assertRaises(ValueError):
            binary_metrics([0,1],[0.2,float("nan")])

    def test_fit_identity_order_independent(self):
        self.assertEqual(fit_ids_digest([4,8,2]),fit_ids_digest([8,2,4]))
        with self.assertRaises(ValueError):
            fit_ids_digest([4,4])

if __name__=="__main__":
    unittest.main()
