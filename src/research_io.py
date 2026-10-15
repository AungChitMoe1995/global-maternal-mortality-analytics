"""Reject stale statistical inputs before publishing an artifact."""
from pathlib import Path
import hashlib
import json


def load_results(base_dir):
    root=Path(base_dir)
    results=json.loads((root/'reports/results.json').read_text(encoding='utf-8'))
    actual=hashlib.sha256((root/'data/processed/maternal_mortality_analytical_master.csv').read_bytes()).hexdigest()
    if actual != results['data_sha256']:
        raise ValueError('Analytical data changed: rerun the audit and analysis before publishing')
    audit=json.loads((root/'reports/quality_audit.json').read_text(encoding='utf-8'))
    if audit['status'] != 'PASS':
        raise ValueError('Cannot publish with a failed data audit')
    if audit['data_sha256'] != actual:
        raise ValueError('Audit is stale: rerun data_quality.py')
    return results,audit
