# RESEARCH PROTOCOL
## Macroeconomic Financing, Demographic Transition, and Global Maternal Mortality: A 24-Year Longitudinal Study across 195 Countries (177-Country Balanced Panel, 2000–2023)

**Principal Investigator:** Dr. Aung Chit Moe (MBBS)  
**Investigator Background:** MBBS Physician (Myanmar) transitioning into Healthcare Data Analytics  
**Date of Adoption:** October 2026  
**Document Type:** Formal Study Design & Research Protocol (Phase 2 Deliverable)  
**Status:** Approved Protocol — Solution 1  

---

### 1. Public Health Background and Rationale

Maternal mortality remains one of the most stark reflections of global health inequity. Despite substantial progress during the Millennium Development Goal (MDG 5) and Sustainable Development Goal (SDG 3.1) periods, approximately 248,000 to 260,000 women continue to die annually from preventable causes related to pregnancy and childbirth.

While clinical causes of maternal death (hemorrhage, hypertensive disorders, sepsis, obstructed labor, unsafe abortion) are well documented, population-level disparities are heavily driven by macro-structural determinants: national economic capacity, health system financing priority, and reproductive demographic patterns.

Previous macro-level studies have frequently suffered from three critical flaws:
1. **The Circular Modeling Trap:** Using modeled maternal mortality estimates as outcomes while naively regressing them against covariates (such as skilled birth attendance or basic GDP) that the estimation agency itself used to build the outcome in data-poor countries.
2. **Extreme Selection Bias via Listwise Deletion:** Attempting to force survey-dependent clinical variables (e.g., skilled birth attendance or adult female literacy) into annual panel models, resulting in the exclusion of over 80% of low-income country-years where censuses and DHS surveys are infrequent.
3. **Price Level Distortion:** Employing current US dollar metrics over longitudinal decades without adjusting for inflation, exchange rate volatility, or purchasing power parity (PPP).

This study implements **Solution 1**, capitalizing on an authenticated, highly complete empirical dataset (195 sovereign countries in the MMEIG grid; 177 balanced-panel countries observed continuously across all core covariates from 2000 to 2023) to rigorously assess how domestic health financing priority and fertility dynamics relate to maternal survival across the globe.

---

### 2. Research Questions and Pre-Specified Hypotheses

#### Primary Research Question:
* **Question 1 (Health Financing):** After controlling for national economic development level (constant-price purchasing power parity GDP per capita), is the domestic prioritization of healthcare—measured as current health expenditure as a percentage of GDP—independently associated with lower maternal mortality ratios across countries and within countries over time?
* **Hypothesis 1:** Greater health expenditure as a share of GDP is independently associated with lower MMR, reflecting systemic investments in emergency obstetric infrastructure, referral networks, and blood banking.

#### Secondary Research Questions:
* **Question 2 (Demographic Transition & Adolescent Pregnancy):** How do national fertility patterns (total fertility rate and adolescent fertility rate) correlate with maternal mortality, and does elevated adolescent fertility confer excess population-level maternal risk after accounting for overall fertility and economic status?
* **Hypothesis 2:** Elevated adolescent fertility rates (births per 1,000 girls aged 15–19) are independently associated with elevated MMR, reflecting both biological obstetric vulnerability (e.g., cephalopelvic disproportion, preeclampsia) and socioeconomic exclusion.
* **Question 3 (Equity & Income Tier Heterogeneity):** Do maternal mortality trajectories and the marginal protective association of health expenditure differ across World Bank income classifications (Low, Lower-Middle, Upper-Middle, High)?
* **Hypothesis 3:** Domestic health expenditure increases exhibit non-linear diminishing returns, yielding the steepest absolute reductions in maternal deaths within low- and lower-middle-income countries.

---

### 3. Study Population and Unit of Analysis

* **Unit of Analysis:** Country-year grid cell.
* **Geographic Coverage:** 195 sovereign countries and territories evaluated in the WHO/UN MMEIG 2025 estimation round (`4,680` country-years).
* **Study Period:** 2000 to 2023 (24 consecutive calendar years), spanning:
  * MDG Baseline Era: 2000–2005
  * MDG Acceleration Era: 2006–2015
  * SDG Era: 2016–2019
  * COVID-19 Era: 2020–2023
* **Analytical Sample:**
  * **Primary Balanced Panel:** Countries with 100% complete time series across all study variables from 2000 to 2023 (**177 countries**, providing **4,248 continuous country-year observations**; pre-integration single-indicator estimates ranged from 183 to 185 countries).
  * **Unbalanced Sensitivity Panel:** All available country-years with non-missing core variables (**4,406 country-years**).

---

### 4. Variables and Operational Definitions

```
                     STUDY VARIABLE ARCHITECTURE
┌────────────────────────────────────────────────────────────────────────┐
│ PRIMARY OUTCOME:                                                       │
│   ln(MMR) : Log of Maternal Mortality Ratio (Deaths / 100k Live Births)│
│   Sensitivity Bounds: 80% Uncertainty Limits (0.1 and 0.9 Percentiles)  │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │
         ┌───────────────────────────┴───────────────────────────┐
         ▼                                                       ▼
┌──────────────────────────────────────┐  ┌──────────────────────────────────────┐
│ CORE EXPLANATORY VARIABLES:          │  │ COVARIATES & STRATIFIERS:            │
│ 1. ln(GDP per cap, Constant PPP $)   │  │ 1. Urban Population % (Infrastructure│
│ 2. Health Exp % GDP (Financing)      │  │ 2. World Bank Income Classification   │
│ 3. Total Fertility Rate (Births/woman│  │ 3. WHO Geographic Region             │
│ 4. Adolescent Fertility Rate (15-19) │  │ 4. COVID-19 Pandemic Indicator (2020+)│
└──────────────────────────────────────┘  └──────────────────────────────────────┘
```

#### A. Primary Outcome Variable
* **Maternal Mortality Ratio (MMR):** Number of maternal deaths per 100,000 live births in a calendar year.
  * *Source:* WHO/UN MMEIG 2025 estimation round (`estimates.csv`, parameter `mmr`).
  * *Point Estimate (`mmr_pt`):* Median posterior estimate (column `0.5`).
  * *Lower Bound (`mmr_low`):* 10th percentile of posterior distribution (column `0.1`).
  * *Upper Bound (`mmr_high`):* 90th percentile of posterior distribution (column `0.9`).
  * *Transformation:* Natural logarithm $\ln(\text{MMR})$ applied due to extreme positive skewness (range 0.1 to 1,661.5).

#### B. Primary Explanatory Variables
1. **Economic Development (Purchasing Power):**
   * *Indicator:* GDP per capita, PPP (constant 2021 international $) (`NY.GDP.PCAP.PP.KD`).
   * *Source:* World Bank / International Comparison Program (ICP).
   * *Transformation:* Natural logarithm $\ln(\text{GDP})$.
2. **Health System Financing Priority:**
   * *Indicator:* Current health expenditure as % of GDP (`SH.XPD.CHEX.GD.ZS`).
   * *Source:* WHO Global Health Expenditure Database (GHED) via World Bank.
   * *Interpretation:* Reflects the structural priority assigned to healthcare within national resource allocation.
3. **Demographic Fertility Dynamics:**
   * *Total Fertility Rate (TFR):* Number of children that would be born to a woman over her childbearing years (`SP.DYN.TFRT.IN`).
   * *Adolescent Fertility Rate (AFR):* Annual births per 1,000 adolescent women aged 15–19 (`SP.ADO.TFRT`).
   * *Source:* UN DESA Population Division (World Population Prospects 2024).

#### C. Control Variables & Stratifiers
1. **Urbanization:**
   * *Indicator:* Urban population as % of total population (`SP.URB.TOTL.IN.ZS`).
   * *Source:* UN Population Division (World Urbanization Prospects).
   * *Role:* Proxies physical geographic accessibility, road networks, and proximity to comprehensive emergency obstetric care (CEmOC) facilities.
2. **Stratification Classifiers:**
   * *World Bank Income Tier:* Low Income (LIC), Lower-Middle Income (LMIC), Upper-Middle Income (UMIC), High Income (HIC).
   * *WHO Region:* AFRO (Africa), AMRO (Americas), SEARO (South-East Asia), EURO (Europe), EMRO (Eastern Mediterranean), WPRO (Western Pacific).

---

### 5. Inclusion and Exclusion Criteria

#### Inclusions:
1. Sovereign countries and recognized national territories evaluated by the WHO/UN MMEIG 2025 round.
2. Calendar years 2000 through 2023 inclusive.

#### Exclusions:
1. Regional, continental, and economic aggregates (e.g., "World", "Sub-Saharan Africa", "Arab World", identified by `is_aggregate == 1` in World Bank metadata).
2. Non-sovereign overseas territories lacking independent economic and health expenditure reporting.
3. Country-year observations missing primary outcome or core explanatory variables (no forward-filling or imputation permitted under Rule 4).

---

### 6. Missing Data Handling Strategy

* **Empirical Missingness Reality:** Under Solution 1, missingness is exceptionally low:
  * MMR: 0.0% missing across all 195 countries.
  * TFR & Adolescent Fertility: 0.5% missing (194/195 countries complete).
  * Health Expenditure (% GDP): 3.2% missing (183/195 countries complete).
  * GDP per capita (constant PPP): 4.4% missing (185/195 countries complete).
* **Protocol Rule:** Complete case analysis on the balanced panel of countries with full 24-year data series.
* **Selection Bias Check:** A comparison table will explicitly compare baseline characteristics of included balanced countries (n=183) versus excluded countries (n=12, primarily micro-states or extreme conflict zones such as Somalia or Syria) to document the scope of external validity.

---

### 7. Statistical Analysis Plan

#### A. Descriptive & Bivariate Analysis
1. Distributional summaries (mean, standard deviation, median, interquartile range, minimum, maximum) for all variables across four benchmark years: 2000, 2010, 2015, 2023.
2. Spearman non-parametric correlation matrix across all study variables.
3. Cross-country scatterplots displaying log(MMR) versus log(GDP) and Health Exp % GDP, with locally weighted scatterplot smoothing (LOWESS).

#### B. Cross-Sectional Benchmark Models (OLS)
Estimated at benchmark years (2000, 2010, 2023) to assess cross-sectional structural shifts:
$$\ln(\text{MMR}_i) = \beta_0 + \beta_1 \ln(\text{GDP}_i) + \beta_2 \text{HealthExp}_i + \beta_3 \text{TFR}_i + \beta_4 \text{AdolescentFert}_i + \beta_5 \text{Urban}_i + \epsilon_i$$
with heteroskedasticity-robust (Huber-White) standard errors.

#### C. Primary Longitudinal Model: Two-Way Fixed Effects (TWFE) Panel Regression
To estimate within-country associations while controlling for unobserved time-invariant country characteristics (geography, historical institutions, baseline culture) and global secular time trends (medical advancements, global drug guidelines):
$$\ln(\text{MMR}_{it}) = \alpha_i + \gamma_t + \beta_1 \ln(\text{GDP}_{it}) + \beta_2 \text{HealthExp}_{it} + \beta_3 \text{TFR}_{it} + \beta_4 \text{AdolescentFert}_{it} + \beta_5 \text{Urban}_{it} + \epsilon_{it}$$
* Where $\alpha_i$ represents country fixed effects.
* Where $\gamma_t$ represents year fixed effects.
* Standard errors clustered at the country level to account for serial autocorrelation.

#### D. Pre-Specified Sensitivity & Robustness Analyses
1. **Uncertainty Interval Robustness:** Re-estimating the TWFE model replacing the median point estimate (`0.5`) with:
   * The lower 80% uncertainty bound (`0.1`).
   * The upper 80% uncertainty bound (`0.9`).
2. **Income-Tier Stratified Models:** Subgroup regressions across Low-Income, Lower-Middle Income, Upper-Middle Income, and High-Income groups to test for non-linear diminishing returns.
3. **Pre-Pandemic Restriction:** Re-estimating on 2000–2019 to verify that findings are not driven by COVID-19 pandemic anomalies.
4. **Unbalanced vs Balanced Panel Comparison:** Evaluating whether restricting to the balanced 183-country panel alters coefficient estimates.

---

### 8. Dissemination Standards and Intended Audience

* **Audience:** Community researchers, public health practitioners, academic epidemiologists, and healthcare analytics recruiters.
* **Tone:** Methodologically rigorous, transparent, objective, and community health oriented (strictly avoiding corporate-consulting or executive pitch tones).
* **Ethical Caveat (Rule 9):** All outputs will explicitly state that country-level ecological associations do not imply individual-level clinical causality (preventing ecological fallacy).
