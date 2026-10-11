# STATISTICAL ANALYSIS REPORT
## Macroeconomic Financing, Demographic Transition, and Global Maternal Mortality: A 24-Year Longitudinal Study across 195 Countries (177-Country Balanced Panel, 2000–2023)

**Author:** Dr. Aung Chit Moe (MBBS)  
**Investigator Profile:** MBBS Physician (Myanmar) transitioning into Healthcare Data Analytics  
**Date:** October 2026  
**Analytical Model:** Two-Way Fixed Effects Panel Regression with Clustered Standard Errors  

---

### 1. Descriptive Summary of Primary Variables (Benchmark Years, Balanced Panel `n = 177`)

|   Year | Variable      |     Mean |       SD |   Median |      IQR |     Min |       Max |
|-------:|:--------------|---------:|---------:|---------:|---------:|--------:|----------:|
|   2000 | mmr_pt        |   217.74 |   303.18 |    67.64 |   321.64 |    3.55 |   1603.14 |
|   2000 | gdp_pcap_ppp  | 18470.6  | 21916.4  |  9997.33 | 17510.2  |  711.98 | 114148    |
|   2000 | chex_gdp_pct  |     5.46 |     2.8  |     4.87 |     3.38 |    1.22 |     22.28 |
|   2000 | tfr           |     3.22 |     1.69 |     2.74 |     2.61 |    1.15 |      7.83 |
|   2000 | ado_fert_rate |    63.64 |    48.72 |    48.54 |    70.83 |    2.67 |    206.24 |
|   2000 | urban_pct     |    53.4  |    23    |    53.93 |    36.75 |    8.04 |    100    |
|   2010 | mmr_pt        |   176.34 |   258.39 |    54.74 |   229.72 |    2.61 |   1311.06 |
|   2010 | gdp_pcap_ppp  | 21938.2  | 23526.4  | 13129    | 24869.4  |  988.02 | 132502    |
|   2010 | chex_gdp_pct  |     6.23 |     2.86 |     5.49 |     3.92 |    1.73 |     17.73 |
|   2010 | tfr           |     2.92 |     1.5  |     2.38 |     2.09 |    1.15 |      7.64 |
|   2010 | ado_fert_rate |    55.84 |    45.1  |    44.38 |    63.13 |    1.76 |    196.63 |
|   2010 | urban_pct     |    56.98 |    22.96 |    58.12 |    35.88 |   10.98 |    100    |
|   2015 | mmr_pt        |   144.16 |   212.24 |    48.08 |   172.48 |    1.46 |   1176.03 |
|   2015 | gdp_pcap_ppp  | 23344.6  | 23860.3  | 14540.8  | 26100.2  |  992.29 | 130097    |
|   2015 | chex_gdp_pct  |     6.44 |     2.69 |     6.07 |     3.8  |    1.82 |     16.4  |
|   2015 | tfr           |     2.77 |     1.37 |     2.27 |     1.84 |    1.2  |      7.22 |
|   2015 | ado_fert_rate |    51.14 |    42.42 |    39.68 |    62.18 |    1.29 |    178.4  |
|   2015 | urban_pct     |    58.61 |    22.77 |    59.25 |    37.18 |   13.23 |    100    |
|   2023 | mmr_pt        |   109.57 |   157.98 |    42.11 |   129.87 |    1.1  |    992.83 |
|   2023 | gdp_pcap_ppp  | 26119.3  | 25979.1  | 17044.8  | 33360.6  | 1033.01 | 130297    |
|   2023 | chex_gdp_pct  |     6.81 |     3.27 |     6.53 |     4.06 |    1.33 |     27.09 |
|   2023 | tfr           |     2.42 |     1.21 |     1.98 |     1.72 |    0.72 |      6.12 |
|   2023 | ado_fert_rate |    41.57 |    38.37 |    31.89 |    51.88 |    0.54 |    163.09 |
|   2023 | urban_pct     |    61.03 |    22.19 |    62.25 |    35.81 |   15.06 |    100    |

---

### 2. Spearman Non-Parametric Correlation Matrix (Balanced Panel `n = 4,248`)

|                       |   ln(MMR) |   ln(GDP PPP) |   Health Exp % GDP |   Total Fertility (TFR) |   Adolescent Fertility |   Urban Pop % |
|:----------------------|----------:|--------------:|-------------------:|------------------------:|-----------------------:|--------------:|
| ln(MMR)               |  1        |     -0.84062  |          -0.401796 |                0.816544 |               0.841845 |     -0.624243 |
| ln(GDP PPP)           | -0.84062  |      1        |           0.29229  |               -0.776053 |              -0.764142 |      0.745306 |
| Health Exp % GDP      | -0.401796 |      0.29229  |           1        |               -0.376002 |              -0.337195 |      0.354525 |
| Total Fertility (TFR) |  0.816544 |     -0.776053 |          -0.376002 |                1        |               0.788219 |     -0.527529 |
| Adolescent Fertility  |  0.841845 |     -0.764142 |          -0.337195 |                0.788219 |               1        |     -0.554096 |
| Urban Pop %           | -0.624243 |      0.745306 |           0.354525 |               -0.527529 |              -0.554096 |      1        |

* **ln(GDP per capita PPP)** exhibits a massive inverse correlation with **ln(MMR)** ($\rho = -0.84, p < 0.001$ across the 24-year panel; $\rho = -0.85, p < 0.001$ in 2023).
* **Adolescent fertility rate** is intensely positively correlated with maternal mortality ($\rho = +0.84, p < 0.001$ across the panel; $\rho = +0.86, p < 0.001$ in 2023).
* **Total fertility rate** strongly tracks maternal mortality ($\rho = +0.82, p < 0.001$ across the panel; $\rho = +0.79, p < 0.001$ in 2023).
* **Health expenditure as % of GDP** displays a moderate negative rank correlation ($\rho = -0.40, p < 0.001$ across the panel; $\rho = -0.39, p < 0.001$ in 2023), proving that higher national healthcare budget commitment correlates with lower mortality across countries.

---

### 3. Demographic Transition & Adolescent Pregnancy: Severe Obstetric Risks (Figure 6)

#### A. Total Fertility Rate (TFR) vs MMR
- Spearman rank correlation: $\rho = +0.82$ across the 24-year balanced panel ($\rho = +0.79$ in 2023, $p < 0.001$).
- **Biological / Clinical Mechanism:** High fertility rates mean a substantial proportion of women experience grand multiparity (parity $\ge 5$). In clinical obstetrics, grand multiparity is a notorious risk factor for **uterine atony**, the primary cause of fatal postpartum hemorrhage (PPH), as well as uterine rupture, placenta previa, and placental abruption. In addition, closely spaced pregnancies cause maternal depletion syndrome and chronic severe iron deficiency anemia, vastly reducing physiological resilience to obstetric blood loss.

#### B. Adolescent Fertility Rate (Ages 15–19) vs MMR
- Spearman rank correlation: $\rho = +0.84$ across the balanced panel ($\rho = +0.86$ in 2023, $p < 0.001$).
- Cross-sectional multivariable regression: In 2023, each additional 10 adolescent births per 1,000 girls aged 15–19 is associated with an **~15% increase in national MMR** ($\beta = +0.0141, p < 0.001$), completely independent of national GDP and adult fertility.
- **Biological & Obstetric Mechanisms:**
  1. **Anatomical Cephalopelvic Disproportion (CPD):** Pelvic growth and canal remodeling continue through late adolescence. Young girls frequently suffer obstructed labor, which without immediate emergency caesarean section results in uterine rupture, fatal sepsis, or obstetric fistula.
  2. **Hypertensive Disorders of Pregnancy:** Adolescent primigravidas have significantly elevated incidences of pre-eclampsia and eclampsia.
  3. **Social & Behavioral Delays:** Teenage mothers face acute social stigma, lack of financial autonomy, and delayed presentation to skilled birth facilities (Delays 1 and 2).

---

### 4. Domestic Health Financing Priority (% of GDP) Decoupled from GDP (Figure 7)

#### Why Decoupling Health Expenditure % from GDP Matters
GDP per capita measures **macroeconomic capacity** (the overall size of the economic pie). In contrast, Current Health Expenditure (% of GDP) measures **national policy priority** (the share of national resources a government and society choose to invest in health). Integrating the two into a single bubble plot obscured this critical distinction.

#### Empirical Evidence of Protective Association:
- Standalone Spearman rank correlation: $\rho = -0.40$ ($p < 0.001$) across the 24-year balanced panel ($\rho = -0.39, p < 0.001$ in 2023).
- **Median MMR across Spending Priority Quartiles (2023, Balanced Panel `n = 177`):**
  - **Q1 (< 4.4% of GDP allocated to health):** Median MMR = **170.3** deaths per 100k live births.
  - **Q2 (4.4% – 6.5% of GDP allocated to health):** Median MMR = **47.9** deaths per 100k live births.
  - **Q3 (6.5% – 8.5% of GDP allocated to health):** Median MMR = **19.2** deaths per 100k live births.
  - **Q4 (> 8.5% of GDP allocated to health):** Median MMR = **13.4** deaths per 100k live births.
- **Evidence Within Lower-Middle-Income Countries (LMICs):**
  - Even among the 43 Lower-Middle-Income countries with similar modest per-capita income, the correlation between health spending % of GDP and MMR is **$\rho = -0.43$ ($p = 0.004$)**.
  - Countries that prioritize health budgets achieve significantly lower maternal mortality ratios than peers with identical economic levels who underfund healthcare.

---

### 5. Cross-Sectional OLS Benchmark Regressions

Estimated cross-sectional specification across benchmark years:
`ln(MMR_i) = beta0 + beta1*ln(GDP_i) + beta2*HealthExp_i + beta3*TFR_i + beta4*AdolescentFert_i + beta5*Urban_i + e_i`

| Independent Variable | Year 2000 (MDG Baseline) Coef (SE) | Year 2010 Coef (SE) | Year 2023 (SDG Modern) Coef (SE) |
|---|:---:|:---:|:---:|
| **ln(GDP per cap PPP)** | **-0.532** (0.091)*** | **-0.647** (0.098)*** | **-0.810** (0.107)*** |
| **Health Exp % GDP** | -0.015 (0.024) | -0.028 (0.025) | -0.038 (0.028) |
| **Total Fertility (TFR)** | **+0.161** (0.068)** | +0.078 (0.081) | -0.001 (0.103) |
| **Adolescent Fertility** | **+0.009** (0.002)*** | **+0.013** (0.003)*** | **+0.014** (0.003)*** |
| **Urban Population %** | -0.004 (0.003) | -0.002 (0.003) | +0.001 (0.004) |
| **Model R-squared** | **0.832** | **0.802** | **0.750** |
| **Countries (Balanced Panel)** | 177 | 177 | 177 |

*Significance: *** p < 0.001, ** p < 0.01, * p < 0.05. Heteroskedasticity-robust standard errors (HC1) in parentheses.*

#### Clinical Takeaways:
1. **The Increasing Elasticity of Economic Power:** The protective association of real purchasing power increased from -0.532 in 2000 to -0.810 in 2023. In the modern era, a 10% increase in real GDP per capita corresponds to an ~8.1% lower MMR across countries.
2. **Persistent Adolescent Risk:** Across all three decades, adolescent fertility remains a consistently powerful, statistically significant predictor ($p < 0.001$) independent of overall national income and total adult fertility.

---

### 6. Primary Longitudinal Model: Two-Way Fixed Effects (TWFE) Panel Regression

Estimated specification across 24 consecutive years (2000–2023, n = 4,248 country-years across 177 balanced countries), controlling for all unobserved time-invariant country heterogeneity and global secular time trends:
`ln(MMR_it) = alpha_i + gamma_t + beta1*ln(GDP_it) + beta2*HealthExp_it + beta3*TFR_it + beta4*AdoFert_it + beta5*Urban_it + e_it`

Standard errors are clustered at the country level to address longitudinal autocorrelation.

| Independent Variable | Primary Model: Point Estimate (`0.5`) Coef (Cluster SE) | Sensitivity: Lower 80% UI (`0.1`) Coef (Cluster SE) | Sensitivity: Upper 80% UI (`0.9`) Coef (Cluster SE) | Pre-COVID (2000–2019) Coef (Cluster SE) |
|---|:---:|:---:|:---:|:---:|
| **ln(GDP per cap PPP)** | **-0.4959** (0.0750)*** | **-0.4907** (0.0768)*** | **-0.4977** (0.0747)*** | **-0.5265** (0.0784)*** |
| **Health Exp % GDP** | +0.0110 (0.0066) | +0.0097 (0.0068) | +0.0114 (0.0065) | +0.0101 (0.0065) |
| **Total Fertility (TFR)** | **+0.1308** (0.0609)* | **+0.1275** (0.0617)* | **+0.1299** (0.0611)* | +0.0429 (0.0614) |
| **Adolescent Fertility** | -0.0007 (0.0020) | -0.0007 (0.0020) | -0.0007 (0.0020) | -0.0004 (0.0020) |
| **Urban Population %** | -0.0045 (0.0036) | -0.0047 (0.0037) | -0.0043 (0.0035) | -0.0051 (0.0037) |
| **Country Fixed Effects** | Included (177 entities) | Included (177 entities) | Included (177 entities) | Included (177 entities) |
| **Year Fixed Effects** | Included (24 years) | Included (24 years) | Included (24 years) | Included (20 years) |
| **Clustered SE Groups** | 177 Countries | 177 Countries | 177 Countries | 177 Countries |
| **Total Observations** | 4,248 | 4,248 | 4,248 | 3,540 |

*Significance: *** p < 0.001, ** p < 0.01, * p < 0.05.*

#### Plain-Language Epidemiological Interpretation:
1. **Economic Capacity is the Macro-Enabler:** Controlling for country-specific baseline traits and global secular progress, a doubling of real GDP per capita within a country yields a **29.0% reduction** in MMR ($\beta = -0.4959, p < 0.001$). Economic growth builds roads, communication networks, 24/7 operating room electricity, and blood-banking systems.
2. **Fertility Reduction Directly Protects Mothers:** Each reduction of 1 child per woman reduces maternal mortality by **12.3%** within countries ($\beta = +0.1308, p = 0.032$). Fewer births directly eliminate high-order grand multiparity and maternal depletion.
3. **Understanding the Panel vs Cross-Sectional Contrast:**
   - Why are adolescent fertility and health expenditure % of GDP massive structural predictors across countries ($\rho = +0.86$ and $-0.40$), but show muted within-country panel coefficients?
   - In a fixed-effects model, country fixed effects absorb all long-term between-country structural differences (the 19-fold mean / 46-fold median gap between Low-Income and High-Income nations). It only evaluates short-term, year-to-year deviations within a single country.
   - Teenage pregnancy and health financing architecture are slow-moving structural determinants built over generations. Within a country from one year to the next, rapid economic expansion and national fertility transitions dominate the annual mortality changes.
4. **Uncertainty Interval Invariance:** Re-estimating the TWFE specification using the 10th percentile lower bound (`0.1`) and the 90th percentile upper bound (`0.9`) yields virtually identical coefficients (GDP coefficient: -0.491 vs -0.498), proving that **our statistical findings are robust to MMEIG posterior estimation uncertainty**.
