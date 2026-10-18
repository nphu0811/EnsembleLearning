"""Strict metadata-only acceptance for P21 TRAIN-derived scientific seed results.

No raw data or ML modules; checks derived metrics against actual confusion counts.
This cannot prove data provenance by itself: supervisor also verifies source bytes.
"""
from __future__ import annotations
import math

ARM_IDS = ("A0_RF42_NONE","A1_RF17_NONE","A2_RF42_BALANCED",
           "A3_RF42_OVERSAMPLE","A4_STACK42_NONE")
SEEDS = (1103,2207,3301,4409,5501)
SCOPE = "P21_TRAIN_REUSED_POST_HOC_SCIENCE_INTERNAL_VALIDATION_ONLY"


def _metric_check(m: dict, support: tuple[int,int] | None = None) -> bool:
    if not isinstance(m,dict):
        return False
    try:
        tn,fp,fn,tp = [m[x] for x in ("tn","fp","fn","tp")]
        if any(not isinstance(x,int) or isinstance(x,bool) or x<0 for x in (tn,fp,fn,tp)):
            return False
        if tn+fp == 0 or tp+fn == 0:
            return False
        if support is not None and (tn+fp,tp+fn)!=support:
            return False
        total=tn+fp+fn+tp
        if m.get("validation_rows")!=total or m.get("threshold")!=0.5:
            return False
        def div(n,d): return n/d if d else 0.0
        f1_1=div(2*tp,2*tp+fp+fn)
        f1_0=div(2*tn,2*tn+fp+fn)
        denominator=math.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))
        derived={
            "macro_f1":(f1_1+f1_0)/2,
            "mcc":div(tp*tn-fp*fn,denominator),
            "attack_precision":div(tp,tp+fp),
            "attack_recall":div(tp,tp+fn),
            "fpr":div(fp,fp+tn),"fnr":div(fn,fn+tp)
        }
        return all(isinstance(m.get(key),(int,float)) and
                   math.isfinite(m[key]) and
                   math.isclose(m[key],value,rel_tol=0,abs_tol=1e-10)
                   for key,value in derived.items())
    except (KeyError,ValueError,TypeError,OverflowError,ZeroDivisionError):
        return False


def acceptable_science_worker(d: dict, seed: int, source_sha: str,
                              protocol_sha: str) -> bool:
    if not isinstance(d,dict):
        return False
    s=d.get("split",{})
    selector=d.get("selector",{})
    inner=d.get("stack_inner_cv",{})
    if not (
        d.get("passed") is True and d.get("scope")==SCOPE
        and seed in SEEDS and d.get("seed")==seed
        and d.get("source_sha256")==source_sha
        and d.get("protocol_sha256")==protocol_sha
        and d.get("train_rows")==175341 and d.get("fit_subset_rows")==60000
        and d.get("fit_pool_rows")==140272 and d.get("validation_rows")==35069
        and isinstance(d.get("fit_row_ids_sha256"),str)
        and len(d["fit_row_ids_sha256"])==64
        and s.get("group_disjoint") is True
        and s.get("row_disjoint") is True
        and s.get("validation_evaluation_performed") is False
        and s.get("validation_rows")==35069
        and selector.get("validation_used") is False
        and len(selector.get("feature_names",[]))==17
        and len(set(selector.get("feature_names",[])))==17
        and len(selector.get("feature_names_sha256",""))==64
        and selector.get("selector_fit_calls")==15
        and selector.get("sample_rows_per_selection_seed")==35000
        and inner.get("type")=="StratifiedGroupKFold"
        and inner.get("n_splits")==3 and inner.get("seed")==137
        and inner.get("exact_vector_group_disjoint") is True
        and inner.get("amendment")=="P21_PRE_FULL_SCIENCE_INNER_GROUP_SPLIT_2026-10-18"
        and d.get("arm_ids")==list(ARM_IDS)
        and d.get("official_test_opened") is False
        and d.get("validation_used_for_tuning") is False
        and d.get("historical_p9_modified") is False
        and d.get("model_artifacts_saved") is False
    ):
        return False
    entries=d.get("arms")
    if not isinstance(entries,list) or len(entries)!=5:
        return False
    support=None
    for i,(arm,info) in enumerate(zip(ARM_IDS,entries)):
        if not isinstance(info,dict):
            return False
        if not (info.get("arm")==arm and
            info.get("fit_row_ids_sha256")==d["fit_row_ids_sha256"] and
            info.get("fit_source_rows")==60000 and
            info.get("original_feature_count")==(17 if i==1 else 42) and
            isinstance(info.get("fit_seconds"),(int,float)) and info["fit_seconds"]>0
            and isinstance(info.get("predict_seconds"),(int,float)) and info["predict_seconds"]>=0
            and info.get("class_weight")==("balanced" if i==2 else None)):
            return False
        n=info.get("actual_model_fit_rows")
        if i!=3 and n!=60000:
            return False
        if i==3 and (not isinstance(n,int) or not 60000<n<=120000):
            return False
        m=info.get("metrics")
        if not _metric_check(m,support):
            return False
        if support is None:
            support=(m["tn"]+m["fp"],m["tp"]+m["fn"])
        if sum(support)!=35069:
            return False
    return True
