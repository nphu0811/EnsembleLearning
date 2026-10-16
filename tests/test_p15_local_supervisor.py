"""Unit-only P15 local runner safety tests. No model training or real dataset reads."""
import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

SCRIPT = Path(__file__).resolve().parents[1] / 'tools' / 'p15_local_supervisor.py'
spec=importlib.util.spec_from_file_location('p15_supervisor_tests',SCRIPT)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
G=mod.GIB

class SafetyTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        (self.root/'results/reproducibility').mkdir(parents=True)

    def tearDown(self):self.temp.cleanup()

    def test_2gib_free_is_no_go(self):
        b=mod.resource_budget(int(2.01*G),25*G,2*G)
        self.assertFalse(b['passed'])
        self.assertFalse(b['checks']['memory_start'])

    def test_4gib_free_can_start_at_2gib_cap_only_if_gates_pass(self):
        b=mod.resource_budget(4*G,25*G,2*G)
        self.assertTrue(b['passed'])
        self.assertEqual(b['required_available_bytes'],4*G)

    def test_raising_process_cap_requires_higher_start_memory(self):
        b=mod.resource_budget(4*G,25*G,3*G)
        self.assertFalse(b['passed'])
        self.assertGreater(b['required_available_bytes'],4*G)

    def test_disk_is_a_hard_gate(self):
        b=mod.resource_budget(5*G,9*G,2*G)
        self.assertFalse(b['checks']['disk_start'])

    def test_floor_cannot_be_lowered_by_config(self):
        b=mod.resource_budget(5*G,20*G,2*G,1*G)
        self.assertFalse(b['checks']['floor_protected'])

    def test_output_under_unique_reproducibility_dir(self):
        p=mod.safe_new_output(self.root,Path('results/reproducibility/p15_local_trialA'))
        self.assertEqual(p.parent.resolve(),(self.root/'results/reproducibility').resolve())

    def test_output_refuses_existing_folder(self):
        p=self.root/'results/reproducibility/p15_local_trialA'
        p.mkdir()
        with self.assertRaises(ValueError):mod.safe_new_output(self.root,p)

    def test_output_refuses_escape_and_historical_directories(self):
        for path in ('results/reproducibility/../legacy', 'results/final_evaluation/overwrite',
                     'results/reproducibility/p15_local_good/nested'):
            with self.subTest(path=path), self.assertRaises((ValueError,FileNotFoundError)):
                mod.safe_new_output(self.root,Path(path))

    def test_pilot_evidence_match(self):
        p=self.root/'pilot.json'
        base={'mode':'pilot','candidate':'random_forest_17','result':'PASS','source_hashes':{'train':'abcd'},
              'python_executable':sys.executable,'budget':{'process_tree_rss_cap_bytes':2*G},
              'worker_checks':{'passed':True},'release_certified':False,'peak_tree_rss_bytes':int(1.1*G)}
        p.write_text(json.dumps(base))
        self.assertTrue(mod.check_pilot_evidence(p,'random_forest_17',{'train':'abcd'},sys.executable,2*G))

    def test_pilot_wrong_model_hash_or_no_headroom_is_rejected(self):
        p=self.root/'pilot.json'
        base={'mode':'pilot','candidate':'random_forest_17','result':'PASS','source_hashes':{'train':'abcd'},
              'python_executable':sys.executable,'budget':{'process_tree_rss_cap_bytes':2*G},
              'worker_checks':{'passed':True},'release_certified':False,'peak_tree_rss_bytes':int(1.8*G)}
        p.write_text(json.dumps(base))
        self.assertFalse(mod.check_pilot_evidence(p,'random_forest_17',{'train':'abcd'},sys.executable,2*G))
        base['peak_tree_rss_bytes']=int(1*G)
        p.write_text(json.dumps(base))
        self.assertFalse(mod.check_pilot_evidence(p,'stacking_42',{'train':'abcd'},sys.executable,2*G))
        self.assertFalse(mod.check_pilot_evidence(p,'random_forest_17',{'train':'changed'},sys.executable,2*G))

    def test_watchdog_rss_cap_stops(self):
        class FakeProc:
            def __init__(self,pid):pass
            def children(self,recursive):return []
            def memory_info(self):return SimpleNamespace(rss=int(2.1*G))
        ps=SimpleNamespace(Process=FakeProc,NoSuchProcess=RuntimeError,
                           virtual_memory=lambda:SimpleNamespace(available=4*G))
        original=mod.shutil.disk_usage
        mod.shutil.disk_usage=lambda _:SimpleNamespace(free=20*G)
        try:
            sample=mod.resource_sample(ps,123,self.root,2*G,mod.MIN_FREE_FLOOR)
            self.assertEqual(sample['stop_reason'],'PROCESS_TREE_RSS_CAP')
        finally:mod.shutil.disk_usage=original

    def test_watchdog_available_ram_floor_stops(self):
        class FakeProc:
            def __init__(self,pid):pass
            def children(self,recursive):return []
            def memory_info(self):return SimpleNamespace(rss=100_000)
        ps=SimpleNamespace(Process=FakeProc,NoSuchProcess=RuntimeError,
                           virtual_memory=lambda:SimpleNamespace(available=1*G))
        original=mod.shutil.disk_usage
        mod.shutil.disk_usage=lambda _:SimpleNamespace(free=20*G)
        try:self.assertEqual(mod.resource_sample(ps,123,self.root,2*G,mod.MIN_FREE_FLOOR)['stop_reason'],'AVAILABLE_RAM_FLOOR')
        finally:mod.shutil.disk_usage=original

    def test_worker_validation_fails_on_missing_artifact(self):
        import hashlib
        kwargs=dict(candidate='random_forest_17',mode='full',worker_dir=self.root,
                    input_hashes={'train':'abc'},package_versions={'sklearn':'1'})
        w={'passed':True,'candidate':'random_forest_17','mode':'full','train_rows':175341,
           'classes':[0,1],'threshold':0.5,'input_sha256':{'train':'abc'},
           'package_versions':{'sklearn':'1'},
           'artifact':{'filename':'random_forest_17_RECONSTRUCTED_FULL_TRAIN.joblib',
                       'bytes':2,'sha256':'0'}}
        self.assertFalse(mod.verify_worker_result(w,**kwargs))
        path=self.root/w['artifact']['filename']
        path.write_bytes(b'fake-model-bytes-fixture-only')
        w['artifact']['bytes']=len(path.read_bytes())
        w['artifact']['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertTrue(mod.verify_worker_result(w,**kwargs))
        path.write_bytes(b'tampered')
        self.assertFalse(mod.verify_worker_result(w,**kwargs))

    def test_pilot_cannot_claim_serialized_final_artifact(self):
        w={'passed':True,'candidate':'random_forest_17','mode':'pilot','train_rows':10000,
           'classes':[0,1],'threshold':0.5,'input_sha256':{},'package_versions':{},
           'artifact':{'filename':'bad.joblib'}}
        self.assertFalse(mod.verify_worker_result(w,'random_forest_17','pilot',self.root,{},{}))
        del w['artifact']
        self.assertTrue(mod.verify_worker_result(w,'random_forest_17','pilot',self.root,{},{}))

    def test_watchdog_kills_child_process_forced_stop(self):
        import subprocess
        import psutil
        child=subprocess.Popen([sys.executable,'-c','import time;time.sleep(30)'])
        try:
            mod.stop_tree(psutil,child.pid)
            child.wait(timeout=5)
            self.assertIsNotNone(child.returncode)
        finally:
            if child.poll() is None:child.kill();child.wait()

    def test_worker_forbids_official_test_csv_access(self):
        worker=SCRIPT.parent/'p15_local_worker.py'
        spec2=importlib.util.spec_from_file_location('p15_worker_guard_test',worker)
        w=importlib.util.module_from_spec(spec2)
        spec2.loader.exec_module(w)
        with self.assertRaises(PermissionError):
            w.audit_csv('open',(str(self.root/'UNSW_NB15_testing-set.csv'),'r',0))

    def test_worker_does_not_allow_interim_csv(self):
        worker=SCRIPT.parent/'p15_local_worker.py'
        spec2=importlib.util.spec_from_file_location('p15_worker_guard_test2',worker)
        w=importlib.util.module_from_spec(spec2)
        spec2.loader.exec_module(w)
        with self.assertRaises(PermissionError):
            w.audit_csv('open',(str(w.ROOT/'data/interim/unsw-nb15/test_unseen_vectors.csv'),'r',0))

    def test_no_training_imported_at_module_load(self):
        self.assertNotIn('src.models.run_unsw_phase9_final_holdout',sys.modules)

if __name__=='__main__':unittest.main()
