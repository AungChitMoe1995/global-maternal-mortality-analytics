"""Calculate integrity checks and fail the pipeline when a check fails."""
from pathlib import Path
import hashlib
import json
import sqlite3
import numpy as np
import pandas as pd

CORE = ['log_mmr_pt', 'log_gdp_pcap_ppp', 'chex_gdp_pct', 'tfr', 'ado_fert_rate', 'urban_pct']


def evaluate_checks(df):
    checks = []
    def add(name, violations):
        n = int(violations)
        checks.append(dict(check=name, violations=n, status='PASS' if n == 0 else 'FAIL'))
    add('Unique country-year keys', df.duplicated(['country_iso3', 'year']).sum())
    years = set(range(2000, 2024))
    add('One complete 2000–2023 outcome grid per country', sum(set(g.year) != years or len(g) != len(years) for _,g in df.groupby('country_iso3')))
    add('Finite positive MMR and ordered uncertainty limits',
        (~(np.isfinite(df[['mmr_low','mmr_pt','mmr_high']]).all(axis=1) & df.mmr_low.gt(0) & df.mmr_low.le(df.mmr_pt) & df.mmr_pt.le(df.mmr_high))).sum())
    for col in ['gdp_pcap_ppp','chex_gdp_pct','tfr','live_births']:
        add(col + ': finite positive observed values', (df[col].notna() & (~np.isfinite(df[col]) | df[col].le(0))).sum())
    add('Finite nonnegative observed adolescent fertility', (df.ado_fert_rate.notna() & (~np.isfinite(df.ado_fert_rate) | df.ado_fert_rate.lt(0))).sum())
    add('Observed urban percentages in [0,100]', (df.urban_pct.notna() & (~np.isfinite(df.urban_pct) | ~df.urban_pct.between(0,100))).sum())
    for value, log in [('mmr_pt','log_mmr_pt'),('mmr_low','log_mmr_low'),('mmr_high','log_mmr_high'),('gdp_pcap_ppp','log_gdp_pcap_ppp')]:
        valid=df[value].notna()
        add(log + ': consistent with natural logarithm', (~np.isclose(df.loc[valid,log], np.log(df.loc[valid,value]), equal_nan=False)).sum())
    complete = np.isfinite(df[CORE]).all(axis=1)
    add('Complete-case flag matches finite core values', df.has_all_core_vars.ne(complete.astype(int)).sum())
    counts=df.loc[complete].groupby('country_iso3').year.nunique()
    ids=counts[counts.eq(24)].index
    add('Balanced-panel flag matches 24 complete years', df.is_balanced_sample.ne(df.country_iso3.isin(ids).astype(int)).sum())
    return checks


def run_data_quality_audit(base_dir):
    root=Path(base_dir)
    df=pd.read_csv(root/'data/processed/maternal_mortality_analytical_master.csv')
    checks=evaluate_checks(df)
    with sqlite3.connect(root/'data/processed/maternal_mortality.db') as con:
        con.execute('PRAGMA foreign_keys=ON')
        sql=pd.read_sql_query('SELECT * FROM analytical_master ORDER BY country_iso3, year',con)
        csv=df.sort_values(['country_iso3','year']).reset_index(drop=True)
        equal=sql.shape==csv.shape and set(sql.columns)==set(csv.columns)
        if equal:
            for col in csv:
                a,b=csv[col],sql[col]
                if pd.api.types.is_numeric_dtype(a): equal = equal and np.allclose(a,b,equal_nan=True)
                else: equal = equal and a.fillna('').equals(b.fillna(''))
        checks.append(dict(check='CSV and SQLite values agree',violations=int(not equal),status='PASS' if equal else 'FAIL'))
        violations=len(con.execute('PRAGMA foreign_key_check').fetchall())
        constraints=len(con.execute('PRAGMA foreign_key_list(analytical_master)').fetchall())
        n=violations+int(constraints==0)
        checks.append(dict(check='Enforced schema foreign keys have no orphan rows', violations=n,status='PASS' if n==0 else 'FAIL'))
    parquet=pd.read_parquet(root/'data/processed/maternal_mortality_analytical_master.parquet')
    equal=parquet.equals(df) if parquet.shape==df.shape else False
    if not equal:
        try:
            pd.testing.assert_frame_equal(parquet,df,check_exact=False,rtol=1e-10,check_dtype=False)
            equal=True
        except AssertionError:
            pass
    checks.append(dict(check='CSV and Parquet values agree',violations=int(not equal),status='PASS' if equal else 'FAIL'))
    provenance=[]
    manifest=json.loads((root/'data/metadata/download_manifest.json').read_text())
    for entry in manifest:
        p=root/entry['local_path']
        actual=hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
        status='MATCH' if actual==entry['sha256'] else ('MISMATCH' if actual else 'NOT_CACHED')
        provenance.append(dict(resource_id=entry['resource_id'],status=status))
    mismatches=sum(x['status']=='MISMATCH' for x in provenance)
    checks.append(dict(check='Cached raw-file SHA-256 agrees with manifest',violations=mismatches,status='PASS' if mismatches==0 else 'FAIL'))
    passed=all(x['status']=='PASS' for x in checks)
    input_hash=hashlib.sha256((root/'data/processed/maternal_mortality_analytical_master.csv').read_bytes()).hexdigest()
    result=dict(status='PASS' if passed else 'FAIL',data_sha256=input_hash,checks=checks,provenance=provenance,
                raw_cache_complete=all(x['status']=='MATCH' for x in provenance),
                rows=len(df),countries=int(df.country_iso3.nunique()))
    (root/'reports').mkdir(exist_ok=True)
    (root/'reports/quality_audit.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    report=['# Data quality audit',f"Overall result: **{result['status']}**. {len(checks)} calculated checks.",
            pd.DataFrame(checks).to_markdown(index=False),
            'Missingness is reported separately. Allowed missing explanatory data do not make a row suitable for regression. '
            'These checks assess data integrity, not scientific validity, absence of bias, or correctness of upstream national estimates.',
            '## Missing values',df.isna().sum().rename('missing_rows').to_frame().to_markdown(),
            '## Raw-file provenance',pd.DataFrame(provenance).to_markdown(index=False),
            'NOT_CACHED means that raw provenance was not rechecked locally. A missing raw cache is allowed in the lightweight clone. '
            'A mismatching cached hash fails the audit. Re-downloading current WDI data is a new data version and may change findings. '
            'The project performs no additional interpolation; upstream MMEIG and WDI series may themselves be modeled or interpolated.']
    (root/'docs/data_quality_report.md').write_text('\n\n'.join(report)+'\n',encoding='utf-8')
    print('Quality audit:',result['status'],len(checks),'checks')
    if not passed:
        raise ValueError('Data audit failed; inspect reports/quality_audit.json')
    return result


if __name__=='__main__':
    run_data_quality_audit(Path(__file__).resolve().parents[1])
