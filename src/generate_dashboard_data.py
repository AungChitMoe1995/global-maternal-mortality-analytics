"""Build an offline dashboard from the current audited research outputs."""
from pathlib import Path
import json
import pandas as pd
from research_io import load_results


def build_dashboard(base_dir):
    root=Path(base_dir)
    results,audit=load_results(root)
    df=pd.read_csv(root/'data/processed/maternal_mortality_analytical_master.csv')
    fields=['country_iso3','country_name','income_level_name','year','mmr_pt','mmr_low','mmr_high',
            'gdp_pcap_ppp','chex_gdp_pct','tfr','ado_fert_rate','is_balanced_sample']
    payload=dict(results=results,audit=audit,rows=json.loads(df[fields].to_json(orient='records',double_precision=8)))
    content=(root/'src/dashboard_template.html').read_text(encoding='utf-8')
    content=content.replace('__RESEARCH_DATA__',json.dumps(payload,allow_nan=False).replace('</','<\\/'))
    (root/'dashboard/index.html').write_text(content,encoding='utf-8')
    print('Built dashboard/index.html from audited results')


if __name__=='__main__':
    build_dashboard(Path(__file__).resolve().parents[1])
