"""Scientific regression checks: invalid data, unbalanced FE and stale outputs."""
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from analysis import TERMS, fit_panel
from data_quality import evaluate_checks
from research_io import load_results


@pytest.fixture
def snapshot():
    return pd.read_csv(ROOT/'data/processed/maternal_mortality_analytical_master.csv')


def test_invalid_uncertainty_cannot_pass(snapshot):
    snapshot.loc[0,'mmr_low']=snapshot.loc[0,'mmr_high']+1
    checks=evaluate_checks(snapshot)
    assert any(c['status']=='FAIL' and 'uncertainty' in c['check'] for c in checks)


def test_infinite_complete_case_cannot_pass(snapshot):
    i=snapshot.index[snapshot.has_all_core_vars.eq(1)][0]
    snapshot.loc[i,'log_gdp_pcap_ppp']=np.inf
    checks=evaluate_checks(snapshot)
    assert any(c['status']=='FAIL' and 'flag' in c['check'] for c in checks)


def test_unbalanced_fe_recovers_known_slopes():
    rng=np.random.default_rng(20261015)
    beta=np.array([-.4,.1,.2,-.05,.03])
    rows=[]
    for country in range(12):
        for year in range(2000,2008):
            if (country+year)%5==0:
                continue
            x=rng.normal(size=5)
            rows.append(dict(country_iso3=str(country),year=year,
                             log_mmr_pt=country*.2+(year-2000)**2*.1+x@beta,
                             **dict(zip(TERMS,x))))
    _,_,result=fit_panel(pd.DataFrame(rows))
    np.testing.assert_allclose([r['coefficient'] for r in result['coefficients']],beta,atol=1e-10)


def test_stale_data_cannot_publish(tmp_path):
    (tmp_path/'reports').mkdir()
    (tmp_path/'data/processed').mkdir(parents=True)
    (tmp_path/'data/processed/maternal_mortality_analytical_master.csv').write_text('changed')
    (tmp_path/'reports/results.json').write_text(json.dumps({'data_sha256':'outdated'}))
    with pytest.raises(ValueError,match='changed'):
        load_results(tmp_path)


def test_generated_outputs_share_current_audited_input(snapshot):
    results,audit=load_results(ROOT)
    assert results['sample']['balanced_rows']==int(snapshot.is_balanced_sample.sum())
    assert audit['raw_cache_complete'] or not any(p['status']=='MISMATCH' for p in audit['provenance'])
    coefficients=pd.read_csv(ROOT/'reports/tables/model_coefficients.csv')
    assert set(coefficients.model)==set(results['models'])
    assert all(coefficients.ci_low.le(coefficients.coefficient) & coefficients.coefficient.le(coefficients.ci_high))
    html=(ROOT/'dashboard/index.html').read_text(encoding='utf-8')
    assert results['data_sha256'] in html
    assert 'Doctor\'s Defense Guide' not in html
