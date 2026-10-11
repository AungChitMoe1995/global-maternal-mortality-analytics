# DATA INVENTORY
## Maternal Mortality Community Research Project (2000–2023)

**Author:** Collaborative Research Team  
**Investigator Profile:** MBBS Physician (Myanmar) transitioning into Health Data Analytics & Clinical Research  
**Phase:** Phase 1 Deliverable — Source Discovery, Data Acquisition, and Verification  
**Date of Audit:** October 2026  

---

### 1. Overview of Acquired Data Assets

All data files were retrieved directly from official WHO and World Bank endpoints, cryptographically verified using SHA-256 checksums, and stored in `data/raw/`. The raw directory structure preserves the original source files immutably.

```
data/
├── raw/
│   ├── mmeig/
│   │   ├── trends-in-maternal-mortality-2000-to-2023-estimates-data.zip (12.4 MB)
│   │   ├── 9789240108462-eng.pdf (4.55 MB, 132 pages)
│   │   └── extracted/
│   │       └── Estimate_data_v2/
│   │           ├── Estimates/
│   │           │   ├── estimates.csv (8.5 MB, 100,029 rows)
│   │           │   ├── estimates_arr.csv (1,170 rows)
│   │           │   └── aggregates/ (54 CSV files of regional/income aggregates)
│   │           ├── main_data.csv (4,578 empirical observations, 105 columns)
│   │           ├── main_data_adjusted.csv (4,578 adjusted observations)
│   │           └── Other inputs/
│   │               ├── estimates_base_0all_indicators_v2_sab_shared.xlsx (9,711 rows)
│   │               ├── WPP2024_Fertility_summary_MMEIG.xlsx
│   │               ├── GDP MMEIG_2024-07-04 (1).xlsx
│   │               ├── gdp_imputed_21092024.csv
│   │               └── hiv_2024.csv
│   └── world_bank/
│       ├── json/ (14 raw API response JSON files)
│       └── csv/ (14 structured CSV files)
└── metadata/
    ├── download_manifest.json
    ├── indicator_inventory.csv (16 indicators fully profiled)
    └── country_year_coverage.csv (4,680 country-year grid cells)
```

---

### 2. Primary Dataset Audit: WHO/UN MMEIG 2025 Estimation Round

#### A. Country-Level Estimates File: `estimates.csv`
* **File Location:** `data/raw/mmeig/extracted/Estimate_data_v2/Estimates/estimates.csv`
* **File Format:** CSV, UTF-8 encoded, 100,029 rows, 7 columns.
* **Schema Definition:**
  * `iso_alpha_3_code` (string): ISO 3166-1 alpha-3 country identifier (195 unique countries).
  * `year_mid` (integer): Calendar year of estimate (range: 1985–2023).
  * `parameter` (string): Maternal health outcome or epidemiological parameter (15 distinct parameters).
  * `0.1` (float): 10th percentile of posterior distribution (lower bound of 80% Uncertainty Interval).
  * `0.5` (float): 50th percentile of posterior distribution (median point estimate).
  * `0.9` (float): 90th percentile of posterior distribution (upper bound of 80% Uncertainty Interval).
  * `estimate_version` (string): Model run identifier (`test_approach2V2`).

#### B. Epidemiological Parameters in `estimates.csv`

| Parameter Code | Full Description | Unit / Metric | Interpretation & Clinical Relevance |
|---|---|---|---|
| `mmr` | Maternal Mortality Ratio | Deaths per 100,000 live births | Core global outcome; quantifies the obstetric risk of death per live birth. |
| `maternal_deaths` | Absolute Maternal Deaths | Integer count | Absolute public-health burden of maternal mortality in the population. |
| `pm` | Proportion Maternal | Proportion (0 to 1) | Proportion of all deaths among women of reproductive age (15–49) attributable to maternal causes. |
| `lifetime_risk` | Adult Lifetime Risk | Probability (0 to 1) | Cumulative probability that a 15-year-old girl will die of maternal causes before age 50, accounting for competing risks. |
| `lifetime_risk_1_in` | Adult Lifetime Risk (1-in-N) | 1 in N women | Reciprocal form of lifetime risk (e.g., 1 in 49 women vs 1 in 10,000 women). |
| `births` | Annual Live Births | Count | Denominator for MMR; sourced from UN World Population Prospects (WPP 2024). |
| `coviddeaths` | Excess COVID-19 Deaths | Count | Estimated total female deaths aged 15–49 attributable to COVID-19. |
| `matcoviddeaths` | Maternal COVID-19 Deaths | Count | Maternal deaths directly associated with SARS-CoV-2 infection during pregnancy or puerperium. |
| `covidmmr` | COVID-19 MMR Contribution | Deaths per 100,000 live births | Additional MMR points attributable specifically to the COVID-19 pandemic (available 2020–2022). |
| `hiv_related_indirect_mmr` | HIV-Indirect MMR | Deaths per 100,000 live births | Indirect maternal deaths aggravated by HIV infection. |
| `hiv_related_indirect_maternal_deaths` | HIV-Indirect Deaths | Count | Absolute count of HIV-related indirect maternal deaths. |
| `hiv_related_indirect_percentage` | HIV-Indirect % | Percentage (%) | Percentage of total maternal deaths that were HIV-related indirect deaths. |
| `mmr_rate` | Maternal Mortality Rate | Deaths per 1,000 women-years | Obstetric mortality divided by person-years lived by women aged 15–49 (captures both obstetric risk and fertility level). |
| `pm_mean`, `mmr_mean` | Mean Estimates | Ratio / Proportion | Mean values from posterior Markov chain Monte Carlo (MCMC) samples. |

#### C. Uncertainty Intervals: Rigorous Clinical & Statistical Definition
* **Report Standard:** Box 2.1 and Chapter 3 of the official report establish that all published MMEIG uncertainty intervals are **80% Uncertainty Intervals (UIs)**, bounded by the 10th percentile (`0.1`) and 90th percentile (`0.9`).
* **Interpretation:** There is an 80% posterior probability that the true maternal mortality ratio falls between the 10th and 90th percentiles.
* **Integrity Validation:** Across all 4,680 country-year records in the 2000–2023 study window, **zero order violations** were observed (`0.1 <= 0.5 <= 0.9` holds for 100% of observations).
* **Missingness in Study Window (2000–2023):** Exactly **0.0%** missing (all 195 countries have complete 24-year modeled series).

#### D. Annual Rate of Reduction: `estimates_arr.csv`
* **File Location:** `data/raw/mmeig/extracted/Estimate_data_v2/Estimates/estimates_arr.csv`
* **Records:** 1,170 rows covering 195 countries.
* **Periods Assessed:**
  1. `2000, 2023`: Entire MDG-to-SDG tracking period (24 years).
  2. `2000, 2015`: Millennium Development Goal era (MDG 5 target: 5.5% annual reduction).
  3. `2016, 2023`: Sustainable Development Goal era (SDG 3.1 target: MMR < 70 per 100,000).
* **Parameters:** `arr` (annual percentage rate of reduction) and `percent_change_in_mmr` (cumulative % change).

#### E. Empirical Input Data: `main_data.csv`
* **File Location:** `data/raw/mmeig/extracted/Estimate_data_v2/main_data.csv`
* **Observations:** 4,578 empirical data records across 105 attributes.
* **Sources Documented:**
  * Civil Registration and Vital Statistics (CRVS): 3,083 country-years (54% of global data inputs).
  * Specialized Mortality Studies (confidential enquiries, RAMOS): 838 country-years (15%).
  * Population-Based Household Surveys (DHS, MICS): 1,288 country-years (22%).
  * National Censuses: 52 country-years (1%).
  * Miscellaneous sources: 466 country-years (8%).
* **Significance:** In countries without functional CRVS (primarily sub-Saharan Africa and parts of South Asia), empirical data consist of periodic survey points; the annual estimates are generated by the BMat Bayesian regression model using SBA, GDP, and GFR as covariates.

---

### 3. World Bank Indicators Dataset Audit

The World Bank API was queried for the 195 MMEIG countries across 2000–2023 (4,680 expected country-year observations).

#### Master Indicator Inventory Table

| Indicator Code | Domain | Indicator Name | Data Generation Mechanism | Valid Obs (out of 4,680) | Missing % (2000–2023) | Missing % (2023) | Complete Series (24/24 yrs) | Min Value | Median Value | Max Value |
|---|---|---|---|---|---|---|---|---|---|---|
| `MMEIG.MMR` | Maternal Mortality | Maternal mortality ratio (per 100k) | Modeled Bayesian estimate (BMat) | 4,680 | **0.0%** | **0.0%** | 195 / 195 | 0.1 | 57.8 | 1,661.5 |
| `SP.DYN.TFRT.IN` | Fertility | Total fertility rate (births per woman) | UN Population Division demographic model | 4,656 | **0.5%** | **0.5%** | 194 / 195 | 0.72 | 2.38 | 7.83 |
| `SP.ADO.TFRT` | Adolescent Fertility | Adolescent fertility rate (per 1k ages 15-19) | UN Population Division demographic model | 4,656 | **0.5%** | **0.5%** | 194 / 195 | 0.51 | 42.67 | 206.36 |
| `SP.URB.TOTL.IN.ZS` | Urbanization | Urban population (% of total) | UN World Urbanization Prospects | 4,656 | **0.5%** | **0.5%** | 194 / 195 | 8.04% | 58.91% | 100.0% |
| `NY.GDP.PCAP.CD` | Economic Dev | GDP per capita (current US$) | National accounts / World Bank | 4,595 | **1.8%** | **3.6%** | 188 / 195 | \$109.6 | \$4,412.8 | \$256,800 |
| `NY.GDP.PCAP.PP.KD` | Economic Dev | GDP per capita, PPP (constant 2021 intl \$) | ICP / World Bank (inflation-adjusted) | 4,474 | **4.4%** | **4.6%** | 185 / 195 | \$702.8 | \$13,262 | \$149,025 |
| `SH.XPD.CHEX.GD.ZS` | Health Financing | Current health expenditure (% of GDP) | WHO Global Health Expenditure Database | 4,529 | **3.2%** | **2.0%** | 183 / 195 | 1.22% | 5.65% | 27.09% |
| `SH.XPD.CHEX.PC.CD` | Health Financing | Current health expenditure per capita (US\$) | WHO GHED | 4,526 | **3.3%** | **2.6%** | 182 / 195 | \$4.18 | \$264.9 | \$13,473 |
| `SE.SEC.ENRR.FE` | Education | Secondary enrollment, female (% gross) | UNESCO UIS administrative records | 3,250 | **30.6%** | **29.7%** | 16 / 195 | 0.0% | 90.44% | 174.8% |
| `SH.MED.PHYS.ZS` | Workforce | Physicians (per 1,000 population) | WHO GHO / National registries | 2,856 | **39.0%** | **70.3%** | 17 / 195 | 0.01 | 1.97 | 9.54 |
| `SH.MED.NUMW.P3` | Workforce | Nurses and midwives (per 1,000 people) | WHO GHO / National registries | 2,852 | **39.1%** | **61.5%** | 17 / 195 | 0.09 | 4.04 | 20.83 |
| `SH.STA.BRTC.ZS` | Clinical Access | Births attended by skilled health staff (%) | UNICEF/WHO Joint Database (Surveys) | 2,225 | **52.5%** | **100.0%** | 0 / 195 | 5.6% | 98.7% | 100.0% |
| `SE.ADT.LITR.FE.ZS` | Education | Adult female literacy rate (% ages 15+) | UNESCO UIS (Censuses/Surveys) | 897 | **80.8%** | **82.0%** | 0 / 195 | 9.4% | 90.23% | 100.0% |
| `SH.STA.ANVC.ZS` | Clinical Access | Prenatal care coverage (4+ visits, %) | UNICEF/WHO Joint Database (Surveys) | 739 | **84.2%** | **100.0%** | 0 / 195 | 16.1% | 92.8% | 100.0% |

---

### 4. Methodological Findings & Quality Appraisal

1. **The Survey-Reporting Divide:** Indicators directly collected via household surveys (SBA, antenatal care, female literacy) display severe missingness (>50% to >80% missing). In 2023, skilled birth attendance and prenatal care have **zero reported observations** in the World Bank WDI database because DHS/MICS survey data lag by 1–3 years and are not annual.
2. **The Constant-Dollar Necessity:** Current US\$ GDP (`NY.GDP.PCAP.CD`) and current health expenditure (`SH.XPD.CHEX.PC.CD`) are distorted over 24 years by domestic inflation and currency fluctuations. For longitudinal econometric models, constant 2021 PPP international dollars (`NY.GDP.PCAP.PP.KD`) must be used.
3. **The Endogeneity Risk in MMEIG Modeling:** As documented in Chapter 3 of the MMEIG 2025 report, MMEIG itself used constant 2021 PPP GDP, General Fertility Rate, and Skilled Birth Attendance as covariates to model MMR for countries lacking CRVS. Therefore, regressing MMEIG MMR on SBA or GDP in low-CRVS countries requires extreme care to avoid tautological findings.
