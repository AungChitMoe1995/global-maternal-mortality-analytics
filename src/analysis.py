"""Descriptive research and exploratory models of estimated national MMR.

All published numbers originate in results.json / CSV exports. No causal
effects or clinical mechanisms are identified by these ecological models.
"""
from pathlib import Path
import hashlib
import json
import platform

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
import statsmodels
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor

TITLE = 'Global Maternal Mortality, 2000–2023'
TERMS = ['log_gdp_pcap_ppp', 'chex_gdp_pct', 'tfr', 'ado_fert_rate', 'urban_pct']
LABELS = ['Log GDP per capita (constant PPP)', 'Current health expenditure (% GDP)',
          'Total fertility (births/woman)', 'Adolescent fertility (births/1,000)', 'Urban population (%)']
INCOMES = ['Low income', 'Lower middle income', 'Upper middle income', 'High income']
COLORS = dict(zip(INCOMES, ['#bd5829', '#7c63a8', '#168b80', '#315d89']))
CAVEAT = ('MMEIG estimates already use GDP, general fertility and skilled birth attendance. '
          'Regressions on these modeled outcomes are exploratory associations, not independent '
          'estimates of causal effects. National fertility does not measure individual parity or spacing.')


def json_ready(value):
    if isinstance(value, dict):
        return {str(k): json_ready(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(v) for v in value]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (float, np.floating)):
        return float(value) if np.isfinite(value) else None
    return value


def fit_panel(data, outcome='log_mmr_pt', difference=False):
    """Explicit FE dummies work for both balanced and unbalanced samples.

    Keeping the FE columns in the design also includes their parameter count
    in the cluster covariance finite-sample adjustment. Inference uses G-1 t df.
    """
    data = data.copy().reset_index(drop=True)
    if difference:
        data = data.sort_values(['country_iso3', 'year'])
        for col in [outcome] + TERMS:
            data[col] = data.groupby('country_iso3')[col].diff()
        consecutive = data.groupby('country_iso3').year.diff().eq(1)
        data = data.loc[consecutive].dropna(subset=[outcome] + TERMS)
    formula = outcome + ' ~ ' + ' + '.join(TERMS) + ' + C(year)'
    if not difference:
        formula += ' + C(country_iso3)'
    model = smf.ols(formula, data=data).fit(
        cov_type='cluster', cov_kwds={'groups': data.country_iso3}, use_t=True)
    ci = model.conf_int()
    records = []
    for term, label in zip(TERMS, LABELS):
        records.append(dict(term=term, label=label, coefficient=float(model.params[term]),
                            se=float(model.bse[term]), ci_low=float(ci.loc[term, 0]),
                            ci_high=float(ci.loc[term, 1]), p_value=float(model.pvalues[term])))
    return model, data, dict(n_obs=len(data), n_countries=data.country_iso3.nunique(),
                            first_year=int(data.year.min()), last_year=int(data.year.max()),
                            rank=int(model.model.rank), r_squared_including_fe=float(model.rsquared),
                            country_fixed_effects=not difference, coefficients=records)


def run_analysis(base_dir):
    root = Path(base_dir)
    out = root / 'reports' / 'tables'
    images = root / 'docs' / 'images'
    out.mkdir(parents=True, exist_ok=True)
    images.mkdir(parents=True, exist_ok=True)
    master = root / 'data/processed/maternal_mortality_analytical_master.csv'
    df = pd.read_csv(master)
    core = ['log_mmr_pt'] + TERMS
    if df.duplicated(['country_iso3', 'year']).any():
        raise ValueError('Duplicate country-year rows')
    complete = df.loc[np.isfinite(df[core]).all(axis=1)].copy()
    counts = complete.groupby('country_iso3').year.nunique()
    balanced_ids = counts[counts.eq(df.year.nunique())].index
    bal = complete.loc[complete.country_iso3.isin(balanced_ids)].copy()
    if not df.is_balanced_sample.eq(df.country_iso3.isin(balanced_ids).astype(int)).all():
        raise ValueError('Stored balanced-sample flag disagrees with finite complete cases')

    # All-country descriptive results retain countries excluded from regression.
    trends = []
    for (year, income), group in df.groupby(['year', 'income_level_name']):
        trends.append(dict(year=int(year), income=income, n_countries=len(group),
                           median_mmr=group.mmr_pt.median(), mean_mmr=group.mmr_pt.mean(),
                           aggregate_mmr=1e5 * group.maternal_deaths.sum() / group.live_births.sum()))
    pd.DataFrame(trends).to_csv(out / 'income_trends.csv', index=False)
    global_trends = []
    for year, g in df.groupby('year'):
        global_trends.append(dict(year=int(year), n_countries=len(g), median_mmr=g.mmr_pt.median(),
                                  mean_mmr=g.mmr_pt.mean(), maternal_deaths=g.maternal_deaths.sum(),
                                  live_births=g.live_births.sum(),
                                  aggregate_mmr=1e5 * g.maternal_deaths.sum() / g.live_births.sum()))
    selection = []
    for year in [2000, 2023]:
        for included in [True, False]:
            g = df.loc[df.year.eq(year) & df.country_iso3.isin(balanced_ids).eq(included)]
            row = dict(year=year, group='Included' if included else 'Excluded',
                       n_countries=len(g), median_mmr=g.mmr_pt.median(), mean_mmr=g.mmr_pt.mean())
            for term in TERMS:
                row[term + '_median'] = g[term].median()
                row[term + '_missing_pct'] = g[term].isna().mean() * 100
            selection.append(row)
    pd.DataFrame(selection).to_csv(out / 'sample_selection.csv', index=False)
    excluded = df.loc[~df.country_iso3.isin(balanced_ids), ['country_iso3', 'country_name', 'income_level_name']].drop_duplicates()
    excluded.to_csv(out / 'excluded_countries.csv', index=False)
    for name, data in [('all_countries', df), ('balanced', bal)]:
        data.groupby('year')[['mmr_pt'] + TERMS].agg(['count', 'mean', 'median', 'std']).to_csv(out / (name + '_descriptives.csv'))

    # Same full covariate specification in every FE sensitivity fit.
    specifications = [
        ('balanced', 'Balanced panel', bal, 'log_mmr_pt', False),
        ('unbalanced', 'All complete country-years', complete, 'log_mmr_pt', False),
        ('pre_pandemic', 'Balanced panel, 2000–2019', bal.loc[bal.year.le(2019)], 'log_mmr_pt', False),
        ('lower_bound', 'Outcome: lower 80% UI limit', bal, 'log_mmr_low', False),
        ('upper_bound', 'Outcome: upper 80% UI limit', bal, 'log_mmr_high', False),
        ('first_difference', 'Consecutive annual first differences', bal, 'log_mmr_pt', True),
    ]
    for income in INCOMES:
        specifications.append(('income_' + income.lower().replace(' ', '_'), income + ' subset',
                               bal.loc[bal.income_level_name.eq(income)], 'log_mmr_pt', False))
    models = {}
    primary_fit = primary_data = None
    for key, label, data, outcome, difference in specifications:
        model, used, summary = fit_panel(data, outcome, difference)
        models[key] = dict(label=label, outcome=outcome, **summary)
        if key == 'balanced':
            primary_fit, primary_data = model, used
        print('Fitted', key, 'observations', len(used), flush=True)
    for year in [2000, 2010, 2023]:
        used = bal.loc[bal.year.eq(year)]
        m = smf.ols('log_mmr_pt ~ ' + ' + '.join(TERMS), data=used).fit(cov_type='HC1', use_t=True)
        ci = m.conf_int()
        models['cross_section_' + str(year)] = dict(
            label=str(year) + ' cross-section', outcome='log_mmr_pt', n_obs=len(used),
            n_countries=len(used), first_year=year, last_year=year, country_fixed_effects=False,
            coefficients=[dict(term=t, label=l, coefficient=float(m.params[t]), se=float(m.bse[t]),
                               ci_low=float(ci.loc[t, 0]), ci_high=float(ci.loc[t, 1]), p_value=float(m.pvalues[t]))
                          for t, l in zip(TERMS, LABELS)])
    pd.DataFrame([dict(model=k, model_label=v['label'], n_obs=v['n_obs'], n_countries=v['n_countries'], **r)
                  for k, v in models.items() for r in v['coefficients']]).to_csv(out / 'model_coefficients.csv', index=False)

    # Within-transformed diagnostics and exact leave-one-country-out slope fits
    # are valid here because this diagnostic sample is a rectangular panel.
    columns = ['log_mmr_pt'] + TERMS
    def within(data):
        values = data[columns]
        return values - data.groupby('country_iso3')[columns].transform('mean') - data.groupby('year')[columns].transform('mean') + values.mean()
    w = within(bal)
    xx = w[TERMS].to_numpy()
    vif = [dict(term=t, label=l, vif=float(variance_inflation_factor(xx, i))) for i, (t, l) in enumerate(zip(TERMS, LABELS))]
    pd.DataFrame(vif).to_csv(out / 'within_predictor_vif.csv', index=False)
    reference = models['balanced']['coefficients'][0]['coefficient']
    jackknife = []
    for iso in sorted(bal.country_iso3.unique()):
        sub = within(bal.loc[~bal.country_iso3.eq(iso)])
        coef = np.linalg.lstsq(sub[TERMS].to_numpy(), sub.log_mmr_pt.to_numpy(), rcond=None)[0][0]
        jackknife.append(dict(excluded_country=iso, log_gdp_coefficient=coef, change_from_full=coef-reference))
    jk = pd.DataFrame(jackknife)
    jk.to_csv(out / 'leave_one_country_out.csv', index=False)
    residuals = primary_data[['country_iso3', 'year']].copy()
    residuals['residual'] = primary_fit.resid.to_numpy()
    residuals['fitted'] = primary_fit.fittedvalues.to_numpy()
    residuals.to_csv(out / 'balanced_model_residuals.csv', index=False)
    lag = residuals.sort_values(['country_iso3', 'year']).groupby('country_iso3').residual.shift()
    residual_lag_correlation = residuals.residual.corr(lag)
    corr = bal[['mmr_pt'] + TERMS].corr(method='spearman')
    corr.to_csv(out / 'spearman_correlations.csv')
    # Quartile cut points are calculated, never embedded as fixed labels.
    y2023 = bal.loc[bal.year.eq(2023)].copy()
    y2023['quartile'], edges = pd.qcut(y2023.chex_gdp_pct, 4, labels=['Q1', 'Q2', 'Q3', 'Q4'], retbins=True)
    quartiles = y2023.groupby('quartile', observed=True).agg(n_countries=('mmr_pt', 'size'), median_mmr=('mmr_pt', 'median')).reset_index()
    quartiles['quartile'] = quartiles.quartile.astype(str)
    quartiles['lower_chex_pct'] = edges[:-1]
    quartiles['upper_chex_pct'] = edges[1:]
    quartiles.to_csv(out / 'spending_quartiles.csv', index=False)
    results = dict(title=TITLE, subtitle='Trends, inequalities and exploratory associations',
                   data_sha256=hashlib.sha256(master.read_bytes()).hexdigest(),
                   versions=dict(python=platform.python_version(), numpy=np.__version__, pandas=pd.__version__,
                                 scipy=scipy.__version__, statsmodels=statsmodels.__version__),
                   sample=dict(all_countries=df.country_iso3.nunique(), all_rows=len(df),
                               balanced_countries=bal.country_iso3.nunique(), balanced_rows=len(bal),
                               complete_rows=len(complete), complete_countries=complete.country_iso3.nunique()),
                   caveat=CAVEAT, global_trends=global_trends, income_trends=trends,
                   selection=selection, excluded=excluded.to_dict('records'),
                   models=models, spending_quartiles=quartiles.to_dict('records'), vif=vif,
                   diagnostics=dict(residual_lag1_correlation=residual_lag_correlation,
                                    leave_one_out_gdp_min=jk.log_gdp_coefficient.min(),
                                    leave_one_out_gdp_max=jk.log_gdp_coefficient.max()))
    (root/'reports/results.json').write_text(json.dumps(json_ready(results), indent=2, allow_nan=False), encoding='utf-8')

    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'axes.spines.top': False,
                         'axes.spines.right': False, 'savefig.dpi': 300, 'figure.facecolor': 'white'})
    def save(fig, name):
        fig.tight_layout()
        fig.savefig(images/name, bbox_inches='tight')
        plt.close(fig)
    trend = pd.DataFrame(trends)
    fig, ax = plt.subplots(figsize=(9, 5))
    for income in INCOMES:
        g=trend.loc[trend.income.eq(income)]
        ax.plot(g.year, g.median_mmr, color=COLORS[income], label=income, linewidth=2)
    ax.set(title='Country-median MMR by fixed income classification', ylabel='Deaths per 100,000 live births (log scale)', xlabel='Year', yscale='log')
    ax.legend(fontsize=9); save(fig, 'fig1_mmr_trends_by_income.png')
    def scatter(ax, var, label, logx=False):
        for income in INCOMES:
            g = y2023.loc[y2023.income_level_name.eq(income)]
            ax.scatter(g[var], g.mmr_pt, color=COLORS[income], label=income, alpha=.75, s=22)
        ax.set(xlabel=label, ylabel='Estimated MMR (log scale)', yscale='log')
        if logx: ax.set_xscale('log')
    fig, ax = plt.subplots(figsize=(9, 5))
    scatter(ax, 'gdp_pcap_ppp', 'GDP per capita, constant 2021 PPP dollars (log scale)', True)
    ax.set_title('GDP and estimated MMR, 2023 balanced sample')
    ax.legend(fontsize=9); save(fig,'fig2_preston_curve_maternal_mortality.png')
    fig, ax = plt.subplots(figsize=(9, 6))
    im=ax.imshow(corr, vmin=-1, vmax=1, cmap='RdBu_r')
    labels=['MMR', 'Log GDP', 'Health exp.', 'TFR', 'Adolescent fert.', 'Urban %']
    ax.set_xticks(range(6), labels, rotation=35, ha='right'); ax.set_yticks(range(6), labels)
    for i in range(6):
        for j in range(6): ax.text(j,i,f'{corr.iloc[i,j]:.2f}',ha='center',va='center',color='white' if abs(corr.iloc[i,j])>.6 else 'black')
    ax.set_title('Descriptive Spearman correlations, balanced country-years')
    fig.colorbar(im, ax=ax); save(fig,'fig3_spearman_correlation_matrix.png')
    fig, ax=plt.subplots(figsize=(9,5))
    select=pd.DataFrame(selection)
    for included, color in [('Included','#168b80'),('Excluded','#bd5829')]:
        g=select.loc[select.group.eq(included)]
        ax.plot(g.year,g.median_mmr,marker='o',label=included,color=color,linewidth=2)
    ax.set(title='Countries excluded from the balanced sample differ in MMR',xlabel='Year',ylabel='Country-median estimated MMR')
    ax.legend(); save(fig,'fig4_income_heterogeneity_effects.png')
    fig, ax=plt.subplots(figsize=(9,6))
    keys=['balanced','unbalanced','pre_pandemic','lower_bound','upper_bound','first_difference']
    for i,k in enumerate(keys):
        r=models[k]['coefficients'][0]
        ax.errorbar(r['coefficient'],i,xerr=[[r['coefficient']-r['ci_low']],[r['ci_high']-r['coefficient']]],fmt='o',color='#315d89',capsize=3)
    ax.axvline(0,color='gray',linewidth=.8)
    ax.set_yticks(range(len(keys)),[models[k]['label'] for k in keys]); ax.invert_yaxis()
    ax.set(title='Exploratory GDP coefficient across specifications',xlabel='Log-log coefficient with country-clustered 95% CI')
    save(fig,'fig5_uncertainty_forest_plot.png')
    fig, axes=plt.subplots(1,2,figsize=(12,5))
    scatter(axes[0],'tfr','Total fertility (births/woman)'); scatter(axes[1],'ado_fert_rate','Adolescent fertility (births/1,000)')
    fig.suptitle('National fertility indicators and estimated MMR, 2023')
    save(fig,'fig6_fertility_vs_mmr.png')
    for var,label,name in [('tfr','Total fertility (births/woman)','fig6a_tfr_vs_mmr.png'),('ado_fert_rate','Adolescent fertility (births/1,000)','fig6b_adolescent_fert_vs_mmr.png')]:
        fig,ax=plt.subplots(figsize=(9,5)); scatter(ax,var,label); ax.set_title('Ecological association, 2023 balanced sample'); ax.legend(fontsize=9); save(fig,name)
    fig, axes=plt.subplots(1,2,figsize=(12,5))
    scatter(axes[0],'chex_gdp_pct','Current health expenditure (% GDP)')
    axes[1].bar(quartiles.quartile,quartiles.median_mmr,color='#168b80')
    axes[1].set(xlabel='Calculated expenditure quartile',ylabel='Country-median estimated MMR')
    fig.suptitle('Health expenditure includes public, private and external financing')
    save(fig,'fig7_health_exp_vs_mmr.png')
    fig, axes=plt.subplots(1,2,figsize=(12,5))
    axes[0].scatter(residuals.fitted,residuals.residual,s=5,alpha=.2)
    axes[0].axhline(0,color='gray'); axes[0].set(xlabel='Fitted log MMR including FE',ylabel='Residual',title='Residual spread')
    axes[1].hist(jk.log_gdp_coefficient,bins=25,color='#315d89')
    axes[1].axvline(reference,color='#bd5829'); axes[1].set(xlabel='GDP slope after dropping one country',ylabel='Number of country omissions',title='Country influence diagnostic')
    save(fig,'fig8_model_diagnostics.png')
    write_report(root, results)
    return results


def write_report(root, results):
    tables = root/'reports/tables'
    parts = [f'# {TITLE}\n\n## Statistical analysis\n',
             results['caveat'],
             '\n## Samples\n', pd.DataFrame([results['sample']]).to_markdown(index=False),
             '\n## Full-sample trends\n', pd.DataFrame(results['global_trends']).query('year in [2000, 2010, 2015, 2023]').round(2).to_markdown(index=False),
             '\nAggregate MMR is 100,000 times the sum of country median death estimates divided by total live births. '
             'It is a derived snapshot aggregate, not the official posterior median or uncertainty interval of a global total. '
             'Country means and medians answer different questions and weight each country equally.\n',
             '\n## Selection into the balanced panel\n',
             pd.DataFrame(results['selection'])[['year','group','n_countries','median_mmr','mean_mmr']].round(2).to_markdown(index=False),
             '\nExcluded countries:\n', pd.DataFrame(results['excluded']).to_markdown(index=False),
             '\nSelection is associated with data availability. Neither balanced nor unbalanced complete-case analysis removes this bias.\n',
             '\n## Model specification and inference\n',
             'Log MMR is regressed on log constant-PPP GDP, current health expenditure (% GDP), total fertility, adolescent fertility and urban population (%). '
             'Panel fits include explicit country and year dummy columns. Cluster covariance includes the full design rank in its finite-sample adjustment, '
             'with t inference using the number of country clusters minus one degrees of freedom. Cross-sections use HC1 standard errors. '
             'First differences use consecutive annual changes and year effects. All fits give equal weight to country-years. '
             'Fixed effects do not remove changing confounding, reverse causality, or dependence introduced by the MMEIG model.\n']
    for key, model in results['models'].items():
        table = pd.DataFrame(model['coefficients'])[['label','coefficient','se','ci_low','ci_high','p_value']]
        parts += [f"\n### {model['label']}\n\n{model['n_countries']} countries, {model['n_obs']} observations.\n",
                  table.to_markdown(index=False, floatfmt='.5f')]
    parts += ['\n## Diagnostics\n', pd.DataFrame(results['vif']).round(3).to_markdown(index=False),
              '\nWithin-panel VIF measures collinearity after country/year effects are removed.\n',
              pd.DataFrame([results['diagnostics']]).round(5).to_markdown(index=False),
              '\nResidual serial dependence and influential-country slopes are diagnostics, not evidence of causal identification. '
              'Clustered SE account for within-country dependence under the cluster assumptions, but do not propagate upstream MMEIG uncertainty or all cross-country dependence.\n',
              '\n## Outcome-bound sensitivity\n',
              'The lower/upper 80% UI fits replace every outcome by its marginal lower/upper limit. These two vectors are not joint posterior draws. '
              'They do not yield a posterior interval for a coefficient, represent a worst-case bound, or establish robustness to measurement error. '
              'Full uncertainty propagation would require suitable joint posterior draws and an explicit analysis plan.\n',
              '\n## Expenditure quartiles\n', pd.DataFrame(results['spending_quartiles']).round(3).to_markdown(index=False),
              '\nCurrent expenditure is not government budget priority. Its ratio to GDP may change because either numerator or denominator changes.\n',
              '\n## Remaining limits\n',
              'The observational ecological design cannot identify individual risk, parity, birth spacing, health-system mechanisms or intervention effects. '
              'The current metadata classify countries using one acquisition-time income classification throughout 2000–2023. '
              'Income-stratified results are exploratory, with fewer country clusters in each subgroup. No CRVS-only analysis is claimed: '
              'a defensible source-quality classification has not been constructed. No model here establishes predictive performance on unseen countries or future years.\n',
              '\n## Reproducibility\n',
              f"Analytical input SHA-256: `{results['data_sha256']}`. Machine-readable coefficients, sample comparisons, VIF, country omissions and residuals are in `reports/tables/`.\n",
              '\nSources: [WHO 2025 report](https://www.who.int/publications/i/item/9789240108462), '
              '[WHO health financing metadata](https://www.who.int/data/gho/data/themes/topics/indicator-groups/indicator-group-details/GHO/health-expenditure).\n']
    (root/'docs/statistical_analysis.md').write_text('\n\n'.join(parts), encoding='utf-8')


if __name__ == '__main__':
    run_analysis(Path(__file__).resolve().parents[1])
