"""TDD tests: tiny synthetic CSVs, no real dataset needed."""
from pathlib import Path
from tempfile import TemporaryDirectory
import csv
import hashlib
import importlib.util
import sys
import unittest

MODULE_PATH = Path(__file__).parents[1] / 'tools' / 'p15_03_check_dataset_provenance.py'
spec = importlib.util.spec_from_file_location('p15_03_check_dataset_provenance', MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)

class DataProvenanceTests(unittest.TestCase):
    def fixtures(self, root):
        data = root / 'data/raw/unsw-nb15'
        data.mkdir(parents=True)
        train = data / 'UNSW_NB15_training-set.csv'
        test = data / 'UNSW_NB15_testing-set.csv'
        features = data / 'NUSW-NB15_features.csv'
        header = 'id,proto,service,state,attack_cat,label\n'
        train.write_text(header+'1,tcp,http,FIN,Normal,0\n2,udp,dns,INT,Fuzzers,1\n',encoding='utf-8')
        test.write_text(header+'1,tcp,http,FIN,Normal,0\n',encoding='utf-8')
        features.write_text('Name,Type\nid,numeric\n', encoding='utf-8')
        rows = []
        for p, expected_rows, expected_class in [(train,2,{'0':1,'1':1}),(test,1,{'0':1,'1':0}),(features,None,None)]:
            rows.append({'file':p.name,'size_bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(), 'rows':expected_rows, 'label_counts':expected_class, 'columns':6 if expected_rows is not None else None})
        return rows

    def test_identical_data_passes_and_reports_only_aggregates(self):
        with TemporaryDirectory() as t:
            root=Path(t)
            refs=self.fixtures(root)
            result=mod.audit(root,refs)
            self.assertEqual(result['status'],'PASS')
            self.assertTrue(all(item['status']=='PASS' for item in result['files']))
            self.assertFalse('raw_rows' in str(result))

    def test_modified_test_csv_fails_checksum(self):
        with TemporaryDirectory() as t:
            root=Path(t)
            refs=self.fixtures(root)
            p=root/'data/raw/unsw-nb15/UNSW_NB15_testing-set.csv'
            p.write_text(p.read_text(encoding='utf-8').replace('Normal','Fuzzers'),encoding='utf-8')
            result=mod.audit(root,refs)
            self.assertEqual(result['status'],'FAIL')
            self.assertIn('hash', str(result).lower())

    def test_missing_source_does_not_claim_pass(self):
        with TemporaryDirectory() as t:
            root=Path(t)
            refs=self.fixtures(root)
            (root/'data/raw/unsw-nb15/NUSW-NB15_features.csv').unlink()
            result=mod.audit(root,refs)
            self.assertEqual(result['status'],'FAIL')

if __name__=='__main__':
    unittest.main()
