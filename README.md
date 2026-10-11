# Macroeconomic Financing, Demographic Transition, and Global Maternal Mortality
### A 24-Year Longitudinal Study across 195 Countries (177-Country Balanced Panel, 2000–2023)

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Data Quality Audit](https://img.shields.io/badge/Data%20Quality-10%2F10%20Rules%20Passed-brightgreen.svg)](docs/data_quality_report.md)
[![WHO / UN MMEIG Round](https://img.shields.io/badge/MMEIG-2025%20Round%20Verified-blueviolet.svg)](https://www.who.int/publications/i/item/9789240108462)

**Lead Investigator:** Dr. Aung Chit Moe (MBBS) — *Healthcare Data Analytics & Clinical/Public-Health Research*  
**Primary Sources:** WHO/UN MMEIG 2025 Estimation Round (`ISBN 978-92-4-010846-2`) • World Bank World Development Indicators (WDI)

---

## 1. Abstract

Despite international commitments under Millennium Development Goal 5 and Sustainable Development Goal 3.1, maternal mortality remains a devastating manifestation of worldwide health inequity. This study investigates the longitudinal relationships between real economic capacity (constant-price purchasing power parity GDP per capita), domestic health financing prioritization (current health expenditure as a % of GDP), and reproductive demographic transitions (total and adolescent fertility rates) across 195 sovereign countries (177-country balanced panel) observed from 2000 to 2023.

Harmonizing the newly released **WHO/UN MMEIG 2025 estimation round** with authenticated **World Bank World Development Indicators**, we assembled an empirical balanced panel of **177 sovereign countries** observed continuously across all 24 calendar years (n = 4,248 country-years out of the 4,680-row 195-country grid). Using a Two-Way Fixed Effects (TWFE) panel specification with country-clustered standard errors, we show that within-country real economic growth is strongly protective against maternal death ($\beta = -0.4959, p = 3.7 \times 10^{-11}$), with a doubling of real GDP per capita associated with a **29.0% reduction** in maternal mortality ratio. Concurrently, national fertility reductions significantly accelerate maternal survival ($\beta = +0.1308, p = 0.032$). Cross-sectional models highlight adolescent fertility as a persistent, independent risk factor for elevated maternal mortality ($\beta = +0.0141, p < 0.001$). Re-estimation across MMEIG's 80% posterior uncertainty intervals confirms that our econometric conclusions are robust to measurement uncertainty.

---

## 2. Background and Research Rationale

Clinical obstetrics documents the direct causes of maternal death: severe postpartum hemorrhage, eclampsia, puerperal sepsis, and obstructed labor. However, whether a woman survives an obstetric emergency is heavily determined by structural societal factors described by the **Three Delays Framework** (Delay in deciding to seek care, Delay in reaching care via roads and transport, and Delay in receiving 24/7 emergency obstetric surgery upon arrival).

Previous macro-level cross-country studies frequently suffered from:
1. **The Circular Modeling Trap:** Regressing modeled UN MMR estimates against skilled birth attendance (SBA), ignoring that the UN MMEIG Bayesian model itself used SBA and GDP to generate the outcome in data-sparse nations.
2. **Extreme Selection Bias:** Using survey-bound indicators (such as adult female literacy or SBA) with listwise deletion drops >80% of low-income country-years, systematically excluding the most vulnerable populations.
3. **Price Level Distortion:** Utilizing unadjusted nominal US dollars across longitudinal decades creates severe exchange rate and inflation artifacts.

This study implements **Solution 1**, focusing on an authenticated, highly complete empirical dataset (177 countries observed continuously from 2000 to 2023) to establish a rigorous, reproducible evidence base for community health research.

---

## 3. Data Sources & Provenance

All raw files are cryptographically verified with SHA-256 checksums and logged in [`data/metadata/download_manifest.json`](data/metadata/download_manifest.json):

1. **Primary Maternal Mortality Outcome:**
   * **Source Body:** United Nations Maternal Mortality Estimation Inter-Agency Group (MMEIG: WHO, UNICEF, UNFPA, World Bank Group, and UN DESA Population Division).
   * **Publication:** *Trends in maternal mortality 2000 to 2023* (Geneva: WHO, April 7, 2025; ISBN: 978-92-4-010846-2).
   * **Measures:** Median posterior point estimate (`0.5`) and official 80% Uncertainty Intervals (`0.1` and `0.9` percentiles).
2. **Explanatory Indicators:**
   * **Real Purchasing Power:** GDP per capita, PPP in constant 2021 international dollars (`NY.GDP.PCAP.PP.KD`) — World Bank / ICP.
   * **Health Financing:** Current health expenditure as % of GDP (`SH.XPD.CHEX.GD.ZS`) — WHO Global Health Expenditure Database.
   * **Demographic Transitions:** Total fertility rate (`SP.DYN.TFRT.IN`) and adolescent fertility rate (`SP.ADO.TFRT`) — UN DESA World Population Prospects 2024.
   * **Infrastructure Proxy:** Urban population % (`SP.URB.TOTL.IN.ZS`) — UN World Urbanization Prospects.

---

## 4. Repository Architecture

```
global-maternal-mortality-analytics/
├── data/
│   ├── raw/                             # Reproducible raw cache (populated by download scripts)
│   │   └── README.md                    # Instructions & SHA-256 verification overview
│   ├── processed/
│   │   ├── maternal_mortality_analytical_master.csv
│   │   ├── maternal_mortality_analytical_master.parquet
│   │   └── maternal_mortality.db        # Relational SQLite analytical database (4,680 rows)
│   └── metadata/
│       ├── download_manifest.json       # Cryptographic hashes (SHA-256) & provenance
│       ├── indicator_inventory.csv      # Complete metadata & missingness matrix
│       └── country_year_coverage.csv    # 4,680 country-year observation grid (195 countries)
├── sql/
│   ├── schema.sql                       # DDL schema for SQLite database
│   ├── data_quality.sql                 # SQL audit queries
│   └── descriptive_analysis.sql         # Stratified and benchmark analytical queries
├── src/
│   ├── download_mmeig.py                # Automated MMEIG archive acquisition
│   ├── download_world_bank.py           # Automated World Bank API acquisition
│   ├── inspect_sources.py               # Source profiling & missingness audit
│   ├── integrate_data.py                # Harmonization & feature engineering pipeline
│   ├── data_quality.py                  # Automated programmatic validation suite
│   ├── analysis.py                      # Econometric modeling & figure generation
│   ├── generate_dashboard_data.py       # Builds interactive HTML dashboard
│   ├── create_presentation.py           # Builds widescreen PowerPoint briefing
│   └── create_notebook.py               # Builds & executes Jupyter Notebook
├── notebooks/
│   └── maternal_mortality_analysis.ipynb # Executed notebook with inline outputs & plots
├── dashboard/
│   ├── index.html                       # Self-contained offline interactive web dashboard
│   └── chart.umd.min.js                 # Local vendored Chart.js v4.4.4 runtime (offline-ready)
├── docs/
│   ├── source_register.md               # Source documentation & external reviews
│   ├── data_inventory.md                # In-depth dataset profiling & variable audit
│   ├── data_coverage_report.md          # Missingness & feasibility comparisons
│   ├── data_dictionary.md               # Comprehensive variable schema
│   ├── data_quality_report.md           # 10/10 automated validation audit report
│   ├── research_protocol.md             # Formal pre-specified research design
│   ├── methodology.md                   # Econometric derivations & mathematics
│   ├── statistical_analysis.md          # Full modeling outputs & tables
│   ├── research_report.md               # Standalone publication-style manuscript
│   ├── limitations.md                   # Methodological caveats & ecological warnings
│   ├── images/                          # 9 publication-grade 300 DPI figures (fig1–fig7, 6a, 6b)
│   └── presentation/
│       └── maternal_mortality_research_briefing.pptx # 15-slide widescreen presentation
├── tests/
│   └── test_acquisition_and_validation.py # Automated pytest suite
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 5. Data Quality Audit & Validation Results

The dataset was validated against **10 strict programmatic rules** documented in [`docs/data_quality_report.md`](docs/data_quality_report.md):
* **Rule 1 (Uniqueness):** 0 duplicate `(country, year)` pairs across 4,680 observations (195 countries × 24 years).
* **Rule 2 (Uncertainty Ordering):** `mmr_low <= mmr_pt <= mmr_high` holds for 100% of observations.
* **Rule 3 (Plausibility):** Zero impossible negative values; all percentages bounded.
* **Rule 4 (No Fabrication):** Zero forward-filled interpolations (Rule 4 compliant).
* **Rule 5 (Balanced Panel):** **177 countries (4,248 country-years)** possess complete 24/24 series across all core variables.

---

## 6. Main Statistical Findings

### A. The 19-Fold Mean (46-Fold Median) Income Disparity
In 2023, the global balanced-panel median MMR stood at **42.1 deaths per 100,000 live births** (down 37.7% from 67.6 in 2000), while mean MMR declined by 49.7% (from 217.7 to 109.6). However, the income chasm across the 177 balanced-panel countries in 2023 remains massive:
* **High-Income Countries (n=62):** Mean MMR = **19.5 per 100k** (Median = **7.7**); Mean GDP = \$53,970; Mean Health Exp = 8.09% of GDP.
* **Upper-Middle-Income Countries (n=54):** Mean MMR = **60.5 per 100k** (Median = **45.8**); Mean GDP = \$17,582; Mean Health Exp = 6.80% of GDP.
* **Lower-Middle-Income Countries (n=43):** Mean MMR = **192.1 per 100k** (Median = **138.9**); Mean GDP = \$6,706; Mean Health Exp = 5.36% of GDP.
* **Low-Income Countries (n=18):** Mean MMR = **370.1 per 100k** (Median = **354.0**); Mean GDP = \$2,177; Mean Health Exp = 5.95% of GDP.
*(Unweighted country-mean disparity: **19.0-fold** [370.1 vs 19.5]; country-median disparity: **46.2-fold** [354.0 vs 7.7]; WHO/UN MMEIG live-birth-weighted income group aggregate disparity: **34.7-fold** [346.1 vs 10.0]).*

![Global MMR Trends by Income Group](docs/images/fig1_mmr_trends_by_income.png)

### B. The Preston Curve of Maternal Survival
The association between real GDP per capita and maternal mortality follows a non-linear curve with diminishing marginal returns ($\rho = -0.84$ across the 24-year panel; $\rho = -0.85, p < 0.001$ in 2023). Increases in purchasing power yield dramatic life-saving gains at low income levels, plateauing beyond \$20,000 PPP.

![The Preston Curve of Maternal Survival](docs/images/fig2_preston_curve_maternal_mortality.png)

### C. Demographic Transition & Adolescent Pregnancy (Figure 6)
The demographic transition is a powerful biological and obstetric determinant of maternal survival:
* **Total Fertility Rate (TFR, $\rho = +0.82$ panel / $+0.79$ in 2023, $p < 0.001$):** High national fertility drives grand multiparity ($\ge 5$ births), which directly triggers uterine atony—the leading cause of catastrophic postpartum hemorrhage (PPH)—and maternal nutritional depletion.
* **Adolescent Childbearing (Ages 15–19, $\rho = +0.84$ panel / $+0.86$ in 2023, $p < 0.001$):** Teenage pregnancy carries severe biological vulnerabilities, including immature pelvic architecture causing cephalopelvic disproportion (CPD), obstructed labor, and elevated rates of eclampsia, compounded by social barriers (Delay 1). In cross-sectional regression, each additional 10 adolescent births per 1k girls is associated with an ~15.1% higher national MMR ($p < 0.001$).

![Demographic Transition and Adolescent Pregnancy vs MMR](docs/images/fig6_fertility_vs_mmr.png)

### D. Domestic Health Financing Priority (% of GDP) Decoupled from GDP (Figure 7)
Current Health Expenditure (% of GDP) reflects **national political and budgetary priority**, distinctly decoupled from overall economic size (GDP per capita):
* **Standalone Protective Association:** Moderate negative correlation ($\rho = -0.40, p < 0.001$ across the 24-year panel; $\rho = -0.39, p < 0.001$ in 2023).
* **Spending Priority Quartiles (2023):** Countries in the lowest spending quartile (< 4.4% GDP) suffer a median MMR of **170.3**, compared to **13.4** in the highest quartile (> 8.5% GDP)—a 13-fold survival advantage.
* **Within Lower-Middle-Income Countries (n=43):** Even among nations with similar modest per-capita GDP (like Myanmar), health spending priority has a correlation of **$\rho = -0.43$ ($p = 0.004$)** with MMR, proving that domestic health commitment saves mothers even under tight resource constraints.

![Health Expenditure (% of GDP) vs MMR Decoupled](docs/images/fig7_health_exp_vs_mmr.png)

### E. Primary Longitudinal Econometric Results: Two-Way Fixed Effects Panel Model
Estimated across 24 consecutive years (n = 4,248 country-years, 177 balanced countries, country-clustered standard errors):

$$\ln(\text{MMR}_{it}) = \alpha_i + \gamma_t + \beta_1 \ln(\text{GDP}_{it}) + \beta_2 \text{HealthExp}_{it} + \beta_3 \text{TFR}_{it} + \beta_4 \text{AdoFert}_{it} + \beta_5 \text{Urban}_{it} + \epsilon_{it}$$

| Independent Variable | Point Estimate (`0.5`) Coef (Cluster SE) | Lower Bound (`0.1`) Coef (Cluster SE) | Upper Bound (`0.9`) Coef (Cluster SE) | Clinical & Policy Interpretation |
|---|:---:|:---:|:---:|---|
| **$\ln(\text{GDP per cap PPP})$** | **-0.4959** (0.0750)*** | **-0.4907** (0.0768)*** | **-0.4977** (0.0747)*** | **Doubling real GDP within a country yields a 29.0% reduction in MMR** ($p = 3.7 \times 10^{-11}$). Funds roads, electricity, blood banks. |
| **Health Exp % GDP** | +0.0110 (0.0066) | +0.0097 (0.0068) | +0.0114 (0.0065) | Within-country annual budget fluctuations vs rapid GDP expansion. |
| **Total Fertility (TFR)** | **+0.1308** (0.0609)* | **+0.1275** (0.0617)* | **+0.1299** (0.0611)* | **A decline of 1 child per woman reduces maternal mortality by 12.3%** ($p = 0.032$). Eliminates grand multiparity & uterine atony. |
| **Adolescent Fertility** | -0.0007 (0.0020) | -0.0007 (0.0020) | -0.0007 (0.0020) | Massive cross-country structural divider ($\rho = +0.86$); annual shifts absorbed by TFR & fixed effects. |
| **Urban Population %** | -0.0045 (0.0036) | -0.0047 (0.0037) | -0.0043 (0.0035) | Gradual structural infrastructure proxy. |

*Significance: *** p < 0.001, ** p < 0.01, * p < 0.05. Clustered standard errors at country level.*

![Uncertainty Sensitivity Forest Plot](docs/images/fig5_uncertainty_forest_plot.png)

---

## 7. Public-Health & Community Implications

1. **Prioritizing Adolescent Reproductive Healthcare:** In cross-sectional models, adolescent fertility was an intense, persistent predictor of elevated maternal mortality ($\beta = +0.0141, p < 0.001$). Community health initiatives must prioritize adolescent-friendly contraception, secondary schooling for girls, and delay of early childbearing.
2. **The Reproductive Protection of Fertility Spacing:** Reductions in total fertility significantly improve maternal survival by eliminating high-risk grand multiparity births and allowing maternal hematological recovery.
3. **Macroeconomic Enablers Eliminate Obstetric Delays:** Real economic growth enables investments in all-weather rural roads, ambulance networks, and blood-bank cold chains, dismantling Delay 2 and Delay 3 in the obstetric emergency pathway.

---

## 8. Interactive Dashboard & Presentation Deck

* **Standalone Offline HTML Dashboard:** Open [`dashboard/index.html`](dashboard/index.html) (backed by local vendored [`dashboard/chart.umd.min.js`](dashboard/chart.umd.min.js) so it runs 100% offline with zero external network dependencies) to explore comparative trajectories for any country pair (e.g. Myanmar vs Thailand), interactive Preston curves, dedicated fertility and health expenditure scatter plots, and model results.
* **PowerPoint Briefing:** Open [`docs/presentation/maternal_mortality_research_briefing.pptx`](docs/presentation/maternal_mortality_research_briefing.pptx) for an overhauled 15-slide widescreen presentation deck featuring intuitive doctor-friendly cards, dedicated full-size charts, and an interview defense guide.

---

## 9. Reproduction Instructions

### Prerequisites
* Python 3.12+
* PowerShell (Windows) or Bash (macOS/Linux)

```bash
# 1. Clone repository and install dependencies
pip install -r requirements.txt

# 2. Run automated test suite
pytest tests/ -v

# 3. Execute the full reproducible pipeline
python src/download_mmeig.py
python src/download_world_bank.py
python src/inspect_sources.py
python src/integrate_data.py
python src/data_quality.py
python src/analysis.py
python src/generate_dashboard_data.py
python src/create_presentation.py
python src/create_notebook.py
```

---

## 10. Citation and Attribution

```bibtex
@article{MMEIG_2025,
  title={Trends in Maternal Mortality 2000 to 2023: Estimates by WHO, UNICEF, UNFPA, World Bank Group and UNDESA/Population Division},
  author={{WHO and UNICEF and UNFPA and World Bank Group and UNDESA}},
  journal={World Health Organization, Geneva},
  year={2025},
  isbn={978-92-4-010846-2}
}

@dataset{WorldBank_WDI_2026,
  title={World Development Indicators},
  author={{World Bank Group}},
  year={2026},
  url={https://databank.worldbank.org/source/world-development-indicators}
}
```

*Transparent AI Disclosure: This project was engineered in partnership between an MBBS clinician and Google DeepMind Antigravity AI, adhering to strict reproducible research protocols with zero synthetic or fabricated data.*

---

## AI-Assisted Development

AI coding tools, including Antigravity/Gemini, were used to assist with code generation, implementation, and technical problem-solving during this project.

As the project author, I directed the project goals and overall approach, applied my healthcare knowledge where relevant, and reviewed the implementation and outputs to the extent of my current technical understanding. My background is in medicine and healthcare software workflows, with practical foundational knowledge of Python, SQL, and databases.

AI assistance accelerated implementation, but the project is presented as a transparent demonstration of my healthcare domain knowledge, analytical thinking, and ability to use modern tools to solve practical problems. I do not claim that every line of code was written independently.

