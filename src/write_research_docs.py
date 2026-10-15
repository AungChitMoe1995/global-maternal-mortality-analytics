"""Generate the research narrative and coverage documents from audited results."""
from pathlib import Path
import json
import pandas as pd
from research_io import load_results

WHO='https://www.who.int/publications/i/item/9789240108462'
METHODS='https://pmnch.who.int/docs/librariesprovider9/meeting-reports/9789240108462-web-final.pdf?sfvrsn=db2a572e_3'
FINANCE='https://www.who.int/data/gho/data/themes/topics/indicator-groups/indicator-group-details/GHO/health-expenditure'


def write_docs(base_dir):
    root=Path(base_dir)
    r,audit=load_results(root)
    df=pd.read_csv(root/'data/processed/maternal_mortality_analytical_master.csv')
    s=r['sample']; models=r['models']; coefficient=models['balanced']['coefficients'][0]
    methods=f'''# Methods

## Research question and design

How did estimated national maternal mortality change from 2000 to 2023, how did inequalities differ by fixed income classification, and what exploratory associations appear with economic and demographic indicators?

This is a secondary analysis of public country-year aggregates. Descriptive analyses retain all {s['all_countries']} countries and territories. Regression analyses use {s['balanced_countries']} countries with complete data for all 24 years ({s['balanced_rows']:,} rows) and compare the result with {s['complete_rows']:,} complete country-years in an unbalanced panel. Equal country-year weighting describes the average country association rather than the average pregnancy.

## Outcome and provenance

MMR is estimated maternal deaths per 100,000 live births. The 2025 MMEIG estimation round supplies posterior medians and marginal 80% uncertainty limits, not complete annual censuses of maternal deaths. GDP uses constant 2021 international PPP dollars. SHA-256 records establish file identity, not scientific validity. See the [source register](source_register.md) and [calculated audit](data_quality_report.md).

## Dependence on the upstream model

The [WHO report]({METHODS}), sections 3.2.4 and 3.4.2, identifies GDP per capita, general fertility rate and skilled birth attendance as BMat predictors. In data-sparse settings these predictors can strongly inform the estimated mortality trajectory. Regressing MMEIG MMR on GDP is therefore partly dependent on the construction of the outcome. Total fertility rate is distinct from general fertility rate, but related demographic inputs also limit independence. Omitting skilled birth attendance does not remove circularity. The models describe associations in this snapshot and do not independently estimate effects of GDP or fertility.

## Descriptive estimands

- Country mean and country median MMR give every country equal weight.
- Derived aggregate MMR is 100,000 × sum(country posterior median maternal deaths) / sum(live births). It is a snapshot calculation and need not equal the posterior median of the official aggregate. Marginal uncertainty limits are not summed to construct aggregate uncertainty.
- Income classifications come from the WDI country metadata acquired with this dataset and remain fixed throughout 2000–2023. They are not historical income classifications. Cook Islands lacks a WDI classification and is labeled Unclassified.
- Expenditure quartile boundaries come from the observed 2023 balanced sample. Both counts and boundaries are exported.

## Exploratory model specification

`log(MMR_it) = country_FE_i + year_FE_t + b1*log(GDP_PPP_it) + b2*CHE_GDP_it + b3*TFR_it + b4*adolescent_fertility_it + b5*urban_pct_it + error_it`.

Explicit country/year dummy variables correctly handle both balanced and unbalanced samples. The full design parameter count enters the cluster covariance finite-sample correction. Panel standard errors cluster by country, with t inference on G−1 degrees of freedom. Cross-sectional fits in 2000, 2010 and 2023 use HC1 standard errors with t inference. Fixed effects account for fixed national differences and common year shocks, not time-varying confounding or reverse causality. Log transformation does not guarantee normal or homoskedastic residuals.

GDP is a log-log coefficient. Other slopes are semi-elasticities per displayed indicator unit. Report estimates with 95% confidence intervals. These intervals are conditional regression intervals, not intervals for an intervention effect and not a full propagation of MMEIG estimation uncertainty. No predictive validation is claimed.

## Sensitivity analyses actually implemented

1. All complete country-years, with country and year effects.
2. Balanced countries restricted to 2000–2019.
3. Separate lower and upper marginal MMR uncertainty-limit outcomes.
4. Consecutive annual first differences of outcome and predictors, with year effects and country-clustered inference.
5. Separate models within the fixed income tiers. These exploratory subgroup analyses have fewer country clusters and do not establish differences between subgroup coefficients.

Outcome-bound replacements are not joint posterior draws. They neither supply posterior coefficient uncertainty nor prove robustness to measurement error. A source-quality-restricted analysis is not implemented because defensible country-period CRVS quality classifications have not been constructed. Presence of any CRVS record alone would not justify such a classification.

## Diagnostics and sample selection

Export within-transformed predictor VIF, country-model residuals, pooled within-country lag-1 residual correlation and GDP slopes after omitting one country at a time. The omission exercise re-demeans the remaining rectangular panel and uses least squares; it is a descriptive influence diagnostic without new inferential claims. Compare baseline and endpoint characteristics and missingness for included and excluded countries. Complete-case analysis can exclude countries systematically and does not eliminate selection bias.

## Interpretation of financing and fertility

Current health expenditure as a share of GDP includes public, private and external financing. It does not isolate government priority, maternal health budgets or efficient service delivery. The GDP denominator can change independently of spending. [WHO publishes distinct financing indicators]({FINANCE}) for government expenditure, private expenditure and out-of-pocket payments.

National total fertility does not measure a woman's parity or spacing. Adolescent fertility is a national birth rate, not an individual risk estimate. The dataset cannot identify hemorrhage, eclampsia, referral delays, roads or blood-bank mechanisms. Such mechanisms require appropriate clinical or health-system data and separate literature evidence.
'''
    limitations=f'''# Limitations

1. **Modeled-outcome dependence:** GDP and general fertility help generate MMEIG estimates. GDP associations are not independent confirmation of economic effects. See [WHO methods]({METHODS}), printed pages 20 and 24.
2. **Ecological inference:** National rates do not measure individual exposures, parity, spacing or clinical risk. National averages conceal subnational inequalities.
3. **Uncertainty:** Country posterior medians and marginal 80% limits do not provide joint posterior draws. Conditional regression CIs and endpoint sensitivity fits do not propagate all upstream uncertainty.
4. **Selection:** The balanced sample excludes {len(r['excluded'])} countries, including several conflict-affected settings. The unbalanced complete-case fit still excludes missing rows. No claim of representativeness follows from a high fraction of countries alone.
5. **Changing confounding and dependence:** Fixed effects do not remove changing conflict, service access, institutions or reverse causation. Cluster SE assume suitable independence between country clusters, which upstream shared modeling may weaken. Smooth modeled annual series contain less independent information than their row count suggests.
6. **Financing measurement:** CHE/GDP combines financing sources and is sensitive to its denominator. It cannot identify government commitment or maternal-care efficiency.
7. **Classification:** Income groups use the snapshot metadata for every historical year. Changing composition and historic income mobility are not studied.
8. **Diagnostics:** VIF, residual plots and country-omission checks reveal instability without curing confounding. Subgroup models have fewer clusters. No pre-registered causal design or out-of-sample prediction study is claimed.
9. **Data vintage:** WDI revisions can change values. The checked-in processed snapshot supports reproduction of this release; re-downloading is a new data version. Hashes verify identity, not correctness.
10. **Further work:** A defensible CRVS-quality sensitivity analysis needs country-period metadata. Full MMEIG uncertainty propagation requires appropriate joint posterior draws. These remain open methodological tasks rather than completed analyses.
'''
    protocol=f'''# Analysis plan and amendment record

**Author:** Dr. Aung Chit Moe (MBBS). **Revision date:** 15 October 2026.

This is a documented analysis plan for a portfolio secondary-data study. It was revised after inspecting data and results and is **not a preregistered protocol**. Hypotheses and specification choices should not be described as prospectively registered.

## Objectives

1. Describe 2000–2023 maternal mortality trends across all {s['all_countries']} countries and territories.
2. Compare country-level inequality by fixed income classification and distinguish country averages from a birth-based aggregate ratio.
3. Explore associations of estimated MMR with economic and demographic indicators while explicitly acknowledging upstream model dependence.

## Population and samples

Full outcome grid: {s['all_rows']:,} country-years. Balanced regression sample: {s['balanced_countries']} countries and {s['balanced_rows']:,} rows. All-complete-row comparison: {s['complete_rows']:,} observations in {s['complete_countries']} countries. Inclusion requires finite outcome and five finite core predictors. The project adds no interpolation or carry-forward values.

## Implemented analyses

The [methods](methodology.md) define units, models, inference, sensitivity analyses and diagnostics. The [statistical report](statistical_analysis.md) contains calculated tables for each fit, including income subsets and unbalanced comparison. Excluded countries and selection summaries are exported. No significance threshold determines which fitted coefficients appear in outputs.

## Changes from the earlier repository release

- Primary contribution changed from claims about macroeconomic effects to descriptive trends and inequalities with exploratory regressions.
- Corrected the claim that excluding SBA removes circularity. GDP and related demographic inputs remain relevant to MMEIG outcome construction.
- Added previously described but absent unbalanced and income-stratified fits, consecutive first differences, VIF, residual diagnostics and country omissions.
- Replaced manual two-way demeaning for panel inference with explicit FE dummy fits that handle unbalanced samples and include FE parameters in covariance correction.
- Corrected outdated 183/12 sample counts to the computed sample. Removed claims that a balanced panel eliminates selection bias.
- Renamed lower/upper uncertainty-bound fits as sensitivity exercises rather than complete measurement-error robustness.
- Removed unmeasured clinical mechanisms and policy effects from the study's findings.
- Rebuilt reports and presentation artifacts from machine-readable results, with input hashes and calculated audit outcomes.

## Remaining analyses not claimed

CRVS-quality-restricted models, full joint-posterior uncertainty propagation, causal identification, and prospective prediction require additional inputs or study design. No ethics approval or journal publication is claimed. This repository uses public national aggregates and contains no patient records.
'''
    tables=root/'reports/tables'
    selection=pd.read_csv(tables/'sample_selection.csv')
    coverage=df.groupby('country_iso3').has_all_core_vars.sum()
    inventory=pd.DataFrame({'variable':df.columns,'observed_rows':df.notna().sum().values,
                            'missing_pct':df.isna().mean().values*100})
    inventory_text=inventory.round(2).to_markdown(index=False)
    selection_text=selection[['year','group','n_countries','median_mmr','mean_mmr']].round(2).to_markdown(index=False)
    manifest=json.loads((root/'data/metadata/download_manifest.json').read_text())
    register=pd.DataFrame([{k:x.get(k,'') for k in ['resource_id','source','retrieval_timestamp','local_path','sha256']} for x in manifest])
    source=f'''# Source register

- [WHO/UN MMEIG, Trends in maternal mortality 2000 to 2023]({WHO}), published 7 April 2025. Outcome estimates, live births, maternal death estimates and uncertainty limits come from its linked distribution archive.
- [WHO full methodological report]({METHODS}), sections 3.2.4 and 3.4.2, describes the GDP, general-fertility and skilled-attendance predictors and their role in data-sparse settings.
- [World Bank WDI](https://databank.worldbank.org/source/world-development-indicators) supplies economic and demographic indicators through the API. Indicator metadata and original responses are cached by acquisition scripts.
- [WHO financing definitions]({FINANCE}) distinguish current expenditure from government expenditure and out-of-pocket financing.

The MMEIG and WDI series are not independent confirmations of mortality. GDP and demographic information can inform the MMEIG model. WDI also republishes indicators produced by other agencies. File hashes provide provenance, not validation of epidemiological truth.

Country metadata use World Bank regional groupings, not WHO regions. Income labels remain fixed to this acquisition snapshot. Cook Islands is Unclassified in WDI here.

## Acquired resources

The original retrieval timestamps are retained below. Cached raw files are rehashed by the audit when available. Re-downloading mutable WDI endpoints constitutes a new version.

{register.to_markdown(index=False)}
'''
    def slope(key):
        c=models[key]['coefficients'][0]
        return f"{c['coefficient']:.3f} (95% CI {c['ci_low']:.3f} to {c['ci_high']:.3f})"
    report=f'''# Global Maternal Mortality, 2000–2023
## Trends, inequalities and exploratory associations

**Author:** Dr. Aung Chit Moe, MBBS. Secondary analysis of public country aggregates.

## Question

How did estimated national maternal mortality change, how unequal were those trends, and what associations appeared with economic and demographic indicators?

## Data and approach

The study integrates the MMEIG 2025 estimation round with WDI. Descriptive analyses retain {s['all_countries']} countries and territories ({s['all_rows']:,} country-years). The balanced regression uses {s['balanced_countries']} countries ({s['balanced_rows']:,} rows). An unbalanced model includes {s['complete_rows']:,} complete rows. [Methods](methodology.md) explain estimands, source dependence and conditional inference.

## Descriptive results

{pd.DataFrame(r['global_trends']).query('year in [2000, 2010, 2015, 2023]')[['year','median_mmr','mean_mmr','aggregate_mmr']].round(2).to_markdown(index=False)}

Mean and median weight countries equally. The derived aggregate uses country median death estimates and births and may differ from the official global posterior result. Income trajectories use one fixed classification. They do not describe historical income mobility.

## Selection

{selection_text}

Included and excluded countries differ. Several excluded settings have substantial conflict or data gaps. Neither sample provides an unbiased representation merely because many countries remain.

## Exploratory regressions

The balanced-panel GDP slope is {slope('balanced')}. Corresponding slopes are {slope('unbalanced')} for all complete rows, {slope('pre_pandemic')} before 2020, and {slope('first_difference')} for consecutive first differences. These are model coefficients, not estimated intervention effects. All predictors, uncertainty intervals, income subset fits and diagnostics appear in the [statistical report](statistical_analysis.md).

The apparent GDP relationship requires special caution: the MMEIG model already uses GDP, general fertility and skilled birth attendance. These regressions do not independently discover an economic effect on maternal mortality. Replacing modeled outcomes by their marginal lower/upper limits does not fully propagate posterior uncertainty.

## Interpretation

The project demonstrates persistent country-level differences and explores specification sensitivity. It cannot identify clinical pathways, individual pregnancy risk or the effects of government spending. National fertility does not establish individual parity or spacing. CHE/GDP does not isolate government priority. The research can inform better questions and further data collection without supplying an intervention recommendation.

## Contribution and next work

The portfolio contribution is the reproducible integration of public data, explicit handling of coverage and estimands, and consistent communication of methodological limits. Additional work should prioritize source-quality metadata and uncertainty propagation before stronger etiological claims. See [limitations](limitations.md) and the retrospective [analysis-plan amendment](research_protocol.md).

Sources: [WHO/UN MMEIG]({WHO}), [World Bank WDI](https://databank.worldbank.org/source/world-development-indicators), and the [source register](source_register.md). AI tools assisted implementation and review. The author directed the project questions and reviewed outputs within his current technical understanding.
'''
    readme=f'''# Global Maternal Mortality, 2000–2023
### Trends, inequalities and exploratory associations

**Author:** Dr. Aung Chit Moe, MBBS. Healthcare data analytics portfolio.

This project asks how estimated maternal mortality changed across countries, how inequalities differed by fixed income group, and what exploratory associations appeared with economic and demographic indicators. It combines WHO/UN MMEIG 2025 estimates with World Bank WDI, retaining all {s['all_countries']} countries and territories for descriptive work.

**Interpretation:** MMEIG estimates already use GDP, general fertility and skilled birth attendance. Regressions on these modeled outcomes are exploratory and cannot independently establish causal effects. See [WHO methods]({METHODS}), sections 3.2.4 and 3.4.2.

## Explore the project

- [Live dashboard](https://aungchitmoe1995.github.io/global-maternal-mortality-analytics/dashboard/) (GitHub Pages deployment status is visible in the repository Actions tab).
- [Offline dashboard](dashboard/index.html): download the repository and open this file beside its bundled Chart.js runtime.
- [PowerPoint briefing](docs/presentation/maternal_mortality_research_briefing.pptx).
- [Executed analysis notebook](notebooks/maternal_mortality_analysis.ipynb).
- [Research report](docs/research_report.md), [methods](docs/methodology.md), [statistical tables](docs/statistical_analysis.md), and [limitations](docs/limitations.md).

## Data and estimands

| Sample | Countries | Country-years |
|---|---:|---:|
| Full outcome grid | {s['all_countries']} | {s['all_rows']:,} |
| Complete balanced model | {s['balanced_countries']} | {s['balanced_rows']:,} |
| All complete rows | {s['complete_countries']} | {s['complete_rows']:,} |

The descriptive outputs distinguish country means, country medians, and a derived aggregate ratio based on estimated maternal deaths and live births. Country averages do not equal the global MMR. Income classifications remain fixed to the acquisition metadata. Excluded countries are reported rather than silently dropped from descriptive conclusions.

## What the analysis demonstrates

- Acquisition, country/year integration, CSV/Parquet/SQLite outputs with enforced database keys, and source manifests.
- Computed integrity checks that fail on invalid data, plus [sample selection comparisons](reports/tables/sample_selection.csv).
- Exploratory cross-sectional and country/year fixed-effect fits, including an unbalanced panel, pre-pandemic restriction, income subsets, consecutive first differences and marginal outcome-bound sensitivity.
- Conditional 95% confidence intervals, within-predictor VIF, residual diagnostics, and leave-one-country-out GDP slopes.
- Reports, figures, notebook, dashboard and slides generated from [machine-readable results](reports/results.json), tied to the analytical input by SHA-256.

No model identifies individual clinical risk or the effects of an intervention. CHE/GDP includes multiple financing sources, and national total fertility does not measure individual parity or birth spacing. Outcome-bound sensitivity does not propagate the full MMEIG posterior uncertainty. CRVS-quality-restricted analysis and predictive validation are not claimed.

## Reproduce the checked-in snapshot

Use Python 3.12 and the versions in [requirements-lock.txt](requirements-lock.txt) for this release, preferably in a virtual environment.

```bash
python -m venv .venv
# Windows PowerShell: .\\.venv\\Scripts\\Activate.ps1
# Linux/macOS: source .venv/bin/activate
pip install -r requirements-lock.txt
python src/run_pipeline.py
python -m pytest -q
```

The default pipeline uses the checked-in processed snapshot, rechecks CSV/Parquet/SQLite consistency, and rebuilds the statistical results and all presentation outputs. It does not require a raw-data download or network access. Raw-file hashes are checked when the files are cached; missing raw files are reported as NOT_CACHED, not verified.

To rebuild integration from the cached raw files:

```bash
python src/run_pipeline.py --integrate
```

To acquire upstream data, run `src/download_mmeig.py` and `src/download_world_bank.py`, then integrate. WDI is mutable: a fresh acquisition is a new data version and may change sample counts and estimates. Retain original responses and the manifest when archiving a release. The [amendment record](docs/research_protocol.md) explains changes from the earlier study design; this was not a preregistered study.

## Repository guide

`src/` contains acquisition, integration, audit, models and output generators. `data/processed/` contains the compact analytical snapshot. `reports/tables/` contains model coefficients, sample comparisons, diagnostics and descriptive summaries. `docs/` contains source and research documentation, figures and slides. `dashboard/` includes a local Chart.js runtime for offline use. `tests/` checks acquisition artifacts, data integrity, unbalanced FE behavior and stale-output protection.

## Sources, licensing and AI assistance

[WHO/UN MMEIG 2025]({WHO}) and [World Bank WDI](https://databank.worldbank.org/source/world-development-indicators). Full resource URLs, hashes and retrieval timestamps are in the [source register](docs/source_register.md) and `data/metadata/download_manifest.json`. Project code is MIT licensed; upstream data retain their providers' terms, and the vendored Chart.js runtime retains its license notice.

AI coding tools (including Antigravity/Gemini and Codex) assisted implementation and review. I directed the research questions and healthcare context and reviewed the outputs within my current technical understanding. I do not claim that every line of code was independently written.
'''
    dictionary='''# Data dictionary

One row is one country/territory and calendar year. Missing values remain missing.

| Field | Definition |
|---|---|
| country_iso3 / iso2_code | Country identifiers used in integration |
| country_name | Country/territory name |
| year | Calendar year, 2000–2023 |
| region_name | Acquisition-time World Bank region, not WHO region |
| income_level_name | Acquisition-time WDI income label, held fixed across years |
| mmr_pt / mmr_low / mmr_high | MMEIG posterior median MMR and marginal 10th/90th percentiles, maternal deaths per 100,000 live births |
| maternal_deaths | Country posterior median estimate of maternal deaths |
| live_births | Annual live births supplied by the MMEIG/WPP distribution |
| lifetime_risk_1_in | Estimated lifetime maternal mortality risk as 1 in N |
| gdp_pcap_ppp | GDP per capita, constant 2021 international PPP dollars |
| gdp_pcap_curr | GDP per capita, current US dollars, not used as the longitudinal economic predictor |
| chex_gdp_pct | Current health expenditure as % GDP, including multiple financing sources |
| chex_pcap_curr | Current health expenditure per capita, current US dollars |
| tfr | Total fertility rate, births per woman under current age-specific rates, not individual parity |
| ado_fert_rate | Annual births per 1,000 women aged 15–19 |
| urban_pct | Urban population as % total population, not a direct measure of referral access |
| sab_modeled_pct | MMEIG internally modeled skilled birth attendance %, retained as supplementary context |
| wdi_sba_pct | WDI skilled birth attendance %, intermittently observed |
| female_sec_enroll_pct | Gross female secondary enrollment %, may exceed 100 |
| physicians_per_1k / nurses_midwives_per_1k | National workforce density, potentially incomplete |
| log_* | Natural logarithm of the named positive measure |
| has_all_core_vars | Finite log MMR and all five regression predictors in this row |
| is_balanced_sample | All 24 country-years have finite core variables |
| is_mdg_era / is_sdg_era / is_covid_era | Descriptive period flags: through 2015, from 2016, and from 2020 |

Source measures may themselves be estimated. The project adds no interpolation. GDP and demographic series are not independent of MMEIG's estimation inputs.
'''
    docs={'methodology.md':methods,'limitations.md':limitations,'research_protocol.md':protocol,
          'research_report.md':report,'source_register.md':source,'data_dictionary.md':dictionary,
          'data_inventory.md':'# Analytical data inventory\n\n'+inventory_text,
          'data_coverage_report.md':f'# Coverage and sample selection\n\nFull grid: {s["all_rows"]:,} rows in {s["all_countries"]} countries and territories.\n\n'+inventory_text+'\n\n## Included versus excluded\n\n'+selection_text+'\n\n'+pd.DataFrame(r['excluded']).to_markdown(index=False)+'\n\nSelection follows completeness, not random sampling. See reports/tables/sample_selection.csv for predictor missingness. No missingness mechanism (MAR/MNAR) is established from these patterns alone.'}
    for name,text in docs.items():
        (root/'docs'/name).write_text(text.strip()+'\n',encoding='utf-8')
    (root/'README.md').write_text(readme.strip()+'\n',encoding='utf-8')
    (root/'reports/README.md').write_text('# Calculated research outputs\n\n`results.json` is the shared input for reports, dashboard and slides. `quality_audit.json` records calculated checks. Each records the analytical CSV hash. `tables/` contains full coefficient CIs and diagnostics, rather than selected significant findings. No coefficient is an identified causal effect.\n',encoding='utf-8')
    log=root/'docs/data_acquisition_log.md'
    original=log.read_text(encoding='utf-8')
    if not original.startswith('> Historical acquisition record'):
        log.write_text('> Historical acquisition record: the current methods and sample counts are maintained in methodology.md and research_protocol.md. Original retrieval records below are retained for provenance.\n\n'+original,encoding='utf-8')
    print('Generated research documents from audited results')


if __name__=='__main__':
    write_docs(Path(__file__).resolve().parents[1])
