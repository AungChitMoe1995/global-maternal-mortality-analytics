# DATA COVERAGE AND FEASIBILITY REPORT
## Maternal Mortality Community Research Project (2000–2023)

**Author:** Collaborative Research Team  
**Investigator Profile:** MBBS Physician (Myanmar) transitioning into Health Data Analytics & Clinical Research  
**Phase:** Phase 1 Deliverable — Source Discovery, Data Acquisition, and Verification  
**Date of Audit:** October 2026  

---

### 1. Executive Summary of Empirical Coverage

The objective of Phase 1 was to determine what data are genuinely available across 195 countries and 24 years (2000–2023, representing 4,680 possible country-year grid cells), rather than assuming data completeness.

Based on actual downloads from the WHO/UN MMEIG 2025 estimation round and the World Bank WDI API (October 2026 release), the empirical findings demonstrate a **sharp methodological divide**:

```
[UNIVERSAL COVERAGE: >95% Complete]
├── MMEIG MMR (Modeled Bayesian Series): 100.0% (4,680 / 4,680)
├── Total Fertility Rate (UN WPP 2024):    99.5% (4,656 / 4,680)
├── Adolescent Fertility Rate (UN WPP):    99.5% (4,656 / 4,680)
├── Urban Population % (UN WUP):           99.5% (4,656 / 4,680)
├── Current Health Expenditure (% GDP):    96.8% (4,529 / 4,680)
└── GDP per capita, PPP (Constant 2021 $): 95.6% (4,474 / 4,680)

[MODERATE / RESTRICTED COVERAGE: 60%–70% Complete]
├── Female Secondary School Enrollment:    69.4% (3,250 / 4,680)
├── Physician Density (per 1k pop):        61.0% (2,856 / 4,680)
└── Nurse & Midwife Density (per 1k pop):   60.9% (2,852 / 4,680)

[SEVERELY SPARSE / SURVEY-BOUND: <50% Complete]
├── Skilled Birth Attendance (WDI):        47.5% (2,225 / 4,680; 0% in 2023)
├── Adult Female Literacy Rate:            19.2% (  897 / 4,680; 18% in 2023)
└── Prenatal Care (4+ visits, %):          15.8% (  739 / 4,680; 0% in 2023)
```

---

### 2. Deep Dive: Indicator Coverage Patterns (2000–2023)

#### A. Primary Outcome: Maternal Mortality Ratio (MMR)
* **Expected Country-Years:** 195 countries × 24 years = 4,680 observations.
* **Actual Valid Observations:** 4,680 (100.0% complete).
* **Missingness:** 0.0% overall, 0.0% in 2023.
* **Uncertainty Interval Integrity:** 80% Uncertainty Interval (`0.1` lower bound, `0.5` median point estimate, `0.9` upper bound) is 100% complete and ordered without violations.
* **Epidemiological Spread:**
  * Minimum: 0.1 deaths per 100,000 live births (San Marino, 2023).
  * Median: 57.8 deaths per 100,000 live births.
  * Maximum: 1,661.5 deaths per 100,000 live births (South Sudan, 2000).
  * 2023 Global Maximum: 994.4 deaths per 100,000 live births (South Sudan, 2023).

#### B. Demographic and Macroeconomic Drivers
1. **Total Fertility Rate (`SP.DYN.TFRT.IN`):**
   * Valid: 4,656 observations (99.5% coverage; 0.5% missing).
   * 194 out of 195 countries have a complete 24/24 annual time series (only Cook Islands is absent in WDI).
   * Range: 0.72 (South Korea, 2023) to 7.83 (Niger, 2004).
2. **Adolescent Fertility Rate (`SP.ADO.TFRT`):**
   * Valid: 4,656 observations (99.5% coverage). 194 countries complete.
   * Range: 0.51 to 206.36 births per 1,000 women aged 15–19.
3. **GDP per Capita, PPP Constant 2021 \$ (`NY.GDP.PCAP.PP.KD`):**
   * Valid: 4,474 observations (95.6% coverage; 4.4% missing).
   * 185 countries have complete 24/24 series; 187 countries have ≥1 observation.
   * In 2023, 186 / 195 countries (95.4%) are reported.
   * Essential for eliminating currency distortion across the 24-year timeframe.
4. **Current Health Expenditure as % of GDP (`SH.XPD.CHEX.GD.ZS`):**
   * Valid: 4,529 observations (96.8% coverage; 3.2% missing).
   * 183 countries have complete 24/24 series; 191 / 195 countries reported in 2023 (98.0%).

#### C. The Clinical Access and Education Bottleneck
1. **Adult Female Literacy Rate (`SE.ADT.LITR.FE.ZS`):**
   * Valid: 897 observations (80.8% missing overall; 82.0% missing in 2023).
   * **Zero countries** have a complete 24-year time series.
   * *Mechanism:* Literacy is collected through decennial censuses or sporadic adult surveys.
   * *Methodological Consequence:* Attempting to run a panel regression on female literacy would drop over 80% of country-years. Restricting analysis to complete cases would introduce catastrophic selection bias against low-income countries where censuses are infrequent.
   * *Viable Alternative:* **Female Secondary School Gross Enrollment (`SE.SEC.ENRR.FE`)** has 3,250 observations (69.4% coverage), covers 191 countries, and provides a continuous measure of female educational expansion.
2. **Skilled Birth Attendance (`SH.STA.BRTC.ZS` in WDI):**
   * Valid: 2,225 observations (52.5% missing overall; **100.0% missing in 2023**).
   * **Zero countries** have a complete 24-year series in WDI. Most low-income countries report once every 3–5 years (DHS/MICS survey cycles). High-income countries often do not report this indicator annually to the UN because hospital delivery is near 100%.
   * *Crucial Discovery:* Inside the MMEIG distribution archive (`Estimate_data_v2/Other inputs/estimates_base_0all_indicators_v2_sab_shared.xlsx`), the MMEIG team constructed an internally modeled annual Skilled Birth Attendant (`MNCH_SAB`) time series (1985–2023) for 249 countries with 95% credible intervals!
3. **Healthcare Workforce (Physicians & Nurses/Midwives per 1,000):**
   * Valid: ~2,855 observations (~61.0% coverage; ~39.0% missing).
   * Only 17 countries (primarily high-income European nations) report annually for all 24 years.
   * In 2023, missingness increases sharply (70.3% missing for physicians, 61.5% for nurses/midwives) due to reporting lags in national health workforce registries.

---

### 3. Missingness by World Bank Income Group and Geographic Region

An audit of the country-year coverage matrix reveals non-random missingness (Missing Not At Random — MNAR):

| Indicator | High Income (HIC) | Upper Middle Income (UMIC) | Lower Middle Income (LMIC) | Low Income (LIC) | Primary Missingness Driver |
|---|---|---|---|---|---|
| MMEIG MMR | 100% complete | 100% complete | 100% complete | 100% complete | Modeled annual series |
| GDP per cap (PPP) | 98.4% | 96.1% | 94.8% | 89.2% | Conflict / fragile states (e.g., Somalia, Syria) |
| Health Exp (% GDP) | 99.1% | 98.5% | 97.2% | 91.0% | National health account reporting delays |
| Fertility (TFR) | 100% | 100% | 100% | 100% | UN demographic estimation |
| Physician Density | 88.2% | 68.4% | 51.2% | 34.6% | Workforce registry underdevelopment in LICs |
| Skilled Birth Att. | 38.1% (low need) | 49.2% | 58.4% | 52.1% | Survey periodicity (DHS every 3–5 yrs) |
| Female Literacy | 12.4% (assumed 100%) | 22.1% | 24.8% | 18.5% | Census periodicity; HICs stop measuring basic literacy |

> [!WARNING]
> **Risk of Listwise Deletion Selection Bias:** If a multivariable panel model includes MMR, GDP, Physician Density, and Female Literacy simultaneously, listwise deletion would eliminate >85% of the global sample and drop almost all Low-Income Countries, invalidating any claim to represent global or community maternal health!

---

### 4. Methodological Assessment of the 8 Research Options

Based on the verified data in Phase 1, here is how the candidate research questions compare:

| Research Question | Empirical Feasibility | Usable Sample Size | Missingness Barrier | Main Risk / Limitation | Recommendation Status |
|---|---|---|---|---|---|
| **A: Healthcare Access & MMR (SBA, ANC)** | Moderate (Cross-sectional) / Poor (Annual Panel in WDI) | ~160 countries (multi-year average) | >50% missingness in WDI; 100% missing in 2023 | Endogeneity: MMEIG used SBA to model MMR in non-CRVS countries. | Feasible only using multi-year averages or MMEIG internal SAB model. |
| **B: Female Education & MMR (Literacy)** | Low (Literacy) / High (Secondary Enrollment) | Literacy: <40 countries in panel; Enrollment: ~170 countries | Literacy is >80% missing; no complete series | Literacy data exclude most low-income countries. | Feasible if operationalized via **Female Secondary School Enrollment** rather than basic literacy. |
| **C: Socioeconomic Development & Financing** | **Very High** | **183 countries** with complete 24-year panel (4,392 country-years) | <4% missingness | Skewed income distribution requires logarithmic transformation; aggregate macro proxy. | **Highly Recommended** (statistically rigorous, broad global representation). |
| **D: Fertility Dynamics & MMR** | **Very High** | **194 countries** with complete 24-year panel (4,656 country-years) | <0.5% missingness | Ecological interpretation: macro fertility is not individual parity. | **Highly Recommended** (investigates demographic transition & adolescent risk). |
| **E: Changes & Trajectories (2000–2023)** | **Very High** | **195 countries** (100% complete) | **0.0% missingness** | Must account for 80% uncertainty intervals; percentage changes sensitive to low baselines. | **Highly Recommended** (leverages official MMEIG ARR metrics and MDG/SDG milestones). |
| **F: Health Workforce & MMR (Physicians)** | Moderate | ~140 countries (intermittent panel) | 39% missing overall; 70% in 2023 | National density conceals severe rural-urban maldistribution. | Viable as a cross-sectional or pooled panel study. |
| **G: Inequalities Between Groups** | **Very High** | **195 countries** grouped by WB income & WHO regions | **0.0% missingness** | Must avoid committing ecological fallacy. | **Highly Recommended** (essential for public-health equity and community research). |
| **H: COVID-19 Period Impact (2020–2022)** | **High** | **195 countries** | 0.0% in MMEIG COVID parameters | Distinguishing pandemic disruptions from model assumptions. | Strong complementary component. |
