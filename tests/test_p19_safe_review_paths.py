"""Negative release-path checks, without creating archives or touching artifacts."""
import unittest

from tools.p19_safe_review_draft import forbidden


class ReleasePathTests(unittest.TestCase):
    def test_archive_traversal_and_absolute_paths_are_rejected(self):
        for name in ('../escape.md','report/../../escape.md','/etc/passwd',
                     'C:/Users/secret.txt','report\\file.md'):
            with self.subTest(name=name):self.assertTrue(forbidden(name))

    def test_restricted_artifacts_are_rejected(self):
        for name in ('a/model.joblib','a/MODEL.PKL','data/raw/test.csv',
                     'templates/original/form.docx','x/local_sources/paper.pdf',
                     '.venv/pyvenv.cfg','x/__pycache__/a.pyc','x/predictions.csv',
                     'x/.env','x/id_rsa','x/archive.zip'):
            with self.subTest(name=name):self.assertTrue(forbidden(name))

    def test_review_summary_and_approved_pdf_paths_are_allowed(self):
        for name in ('results/final_metrics.csv','docs/limits.md',
                     'report/main.tex','approved_report/Bao_cao_37p_UNCHANGED.pdf'):
            with self.subTest(name=name):self.assertFalse(forbidden(name))


if __name__=='__main__':unittest.main()
