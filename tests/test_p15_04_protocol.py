import json
import shutil
import tempfile
import unittest
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parents[1]
S = HERE / 'tools' / 'p15_04_protocol_integrity.py'
spec=importlib.util.spec_from_file_location('audit_p15_04', S)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class AuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        for name, content in mod.REFERENCE_SOURCES.items():
            p=self.root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            # Synthetic contents deliberately won't match snapshot reference hash.
            p.write_text('print("hello")\n', encoding='utf-8')
        for label, name in mod.METADATA_PATHS.items():
            p=self.root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            values={
                'stage2': {'stable_2plus_methods': [f'f{i}' for i in range(17)]},
                'phase8': {'dataset':'UNSW-NB15','official_test_loaded':False},
                'freeze': {k: {'decision_threshold':0.5} for k in mod.EXPECTED_MODELS},
                'phase9': {'dataset':'UNSW-NB15','official_test_opened':True, 'train_rows':175341, 'official_test_rows':82332,
                           'frozen_candidates':{k:{'decision_threshold':0.5} for k in mod.EXPECTED_MODELS}},
            }[label]
            p.write_text(json.dumps(values),encoding='utf-8')
    def tearDown(self): self.tmp.cleanup()
    def test_recognizes_manifests_without_false_pass_when_code_changed(self):
        r=mod.evaluate(self.root)
        self.assertEqual('REVIEW_NEEDED',r['status'])
        self.assertEqual('PASS',r['checks']['frozen_thresholds_0_5']['status'])
        self.assertEqual('REVIEW',r['checks']['source_matches_historical_audit']['status'])
        self.assertEqual([],r['code_evidence'])
    def test_mismatched_frozen_manifest_fails(self):
        p=self.root/mod.METADATA_PATHS['phase9']
        m=json.loads(p.read_text());m['frozen_candidates']['stacking_42']['decision_threshold']=0.6
        p.write_text(json.dumps(m))
        r=mod.evaluate(self.root)
        self.assertEqual('REVIEW',r['checks']['manifest_unchanged_in_phase9']['status'])
    def test_absent_metadata_fails(self):
        (self.root/mod.METADATA_PATHS['freeze']).unlink()
        r=mod.evaluate(self.root)
        self.assertEqual('REVIEW_NEEDED',r['status'])
        self.assertEqual('REVIEW',r['checks']['metadata_set']['status'])

if __name__ == '__main__': unittest.main()
