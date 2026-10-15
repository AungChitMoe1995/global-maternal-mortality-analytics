# Global Maternal Mortality, 2000–2023
### Trends, inequalities and exploratory associations

**Author:** Dr. Aung Chit Moe, MBBS. Healthcare data analytics portfolio.

This project asks how estimated maternal mortality changed across countries, how inequalities differed by fixed income group, and what exploratory associations appeared with economic and demographic indicators. It combines WHO/UN MMEIG 2025 estimates with World Bank WDI, retaining all 195 countries and territories for descriptive work.

**Interpretation:** MMEIG estimates already use GDP, general fertility and skilled birth attendance. Regressions on these modeled outcomes are exploratory and cannot independently establish causal effects. See [WHO methods](https://pmnch.who.int/docs/librariesprovider9/meeting-reports/9789240108462-web-final.pdf?sfvrsn=db2a572e_3), sections 3.2.4 and 3.4.2.

## Explore the project

- [Live dashboard](https://aungchitmoe1995.github.io/global-maternal-mortality-analytics/dashboard/) (GitHub Pages deployment status is visible in the repository Actions tab).
- [Offline dashboard](dashboard/index.html): download the repository and open this file beside its bundled Chart.js runtime.
- [PowerPoint briefing](docs/presentation/maternal_mortality_research_briefing.pptx).
- [Executed analysis notebook](notebooks/maternal_mortality_analysis.ipynb).
- [Research report](docs/research_report.md), [methods](docs/methodology.md), [statistical tables](docs/statistical_analysis.md), and [limitations](docs/limitations.md).

## Data and estimands

| Sample | Countries | Country-years |
|---|---:|---:|
| Full outcome grid | 195 | 4,680 |
| Complete balanced model | 177 | 4,248 |
| All complete rows | 186 | 4,406 |

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
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
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

[WHO/UN MMEIG 2025](https://www.who.int/publications/i/item/9789240108462) and [World Bank WDI](https://databank.worldbank.org/source/world-development-indicators). Full resource URLs, hashes and retrieval timestamps are in the [source register](docs/source_register.md) and `data/metadata/download_manifest.json`. Project code is MIT licensed; upstream data retain their providers' terms, and the vendored Chart.js runtime retains its license notice.

AI coding tools (including Antigravity/Gemini and Codex) assisted implementation and review. I directed the research questions and healthcare context and reviewed the outputs within my current technical understanding. I do not claim that every line of code was independently written.
