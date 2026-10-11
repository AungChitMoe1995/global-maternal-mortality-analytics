# METHODOLOGY AND ECONOMETRIC FRAMEWORK
## Macroeconomic Financing, Demographic Transition, and Global Maternal Mortality: A 24-Year Longitudinal Study across 195 Countries (177-Country Balanced Panel, 2000–2023)

**Author:** Dr. Aung Chit Moe (MBBS)  
**Investigator Profile:** MBBS Physician (Myanmar) transitioning into Healthcare Data Analytics  
**Date:** October 2026  
**Document Type:** Formal Methodological & Econometric Documentation  

---

### 1. Conceptual Framework: Macro-Structural Determinants of Maternal Survival

In clinical obstetrics, maternal deaths are directly caused by acute pathophysiological events: severe postpartum hemorrhage, eclamptic convulsions, puerperal sepsis, obstructed labor, or unsafe abortion complications. 

However, at the macro-epidemiological level, whether a woman survives an obstetric emergency is heavily determined by what Thaddeus and Maine (1994) conceptualized as the **Three Delays**:
1. *Delay 1: Deciding to seek care* (governed by female empowerment, awareness, cultural norms, and financial barriers).
2. *Delay 2: Reaching an adequate health facility* (governed by roads, transport infrastructure, and geographic accessibility).
3. *Delay 3: Receiving adequate, timely emergency care upon arrival* (governed by staffing, 24/7 surgical capacity, blood banking, and health system financing).

Our analytical framework models these macro-level structural enablers:

```
                           MACRO-STRUCTURAL DETERMINANTS
┌─────────────────────────────────┐       ┌─────────────────────────────────┐
│     MACROECONOMIC CAPACITY      │       │     HEALTH FINANCING PRIORITY   │
│  Real GDP per Capita (PPP 2021) │       │   Health Expenditure % of GDP   │
└────────────────┬────────────────┘       └────────────────┬────────────────┘
                 │                                         │
                 ▼                                         ▼
   [General Infrastructure & Roads]          [CEmOC Facilities & Staffing]
                 │                                         │
                 └──────────────────┬──────────────────────┘
                                    │
                                    ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                          OBSTETRIC RISK ENVIRONMENT                       │
│    • Total Fertility Rate (Cumulative Obstetric Lifetime Exposure)        │
│    • Adolescent Fertility Rate (Biological Immaturity & Marginalization)   │
│    • Urbanization % (Proximity to Referral Hospitals)                     │
└───────────────────────────────────┬───────────────────────────────────────┘
                                    │
                                    ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                          PRIMARY PUBLIC-HEALTH OUTCOME                    │
│           ln(MMR) : Maternal Deaths per 100,000 Live Births               │
│                 (WHO / UN MMEIG 2025 Estimation Round)                    │
└───────────────────────────────────────────────────────────────────────────┘
```

---

### 2. Mathematical Specification of Econometric Models

#### A. Dependent Variable Transformation
The distribution of maternal mortality ratio across countries is severely right-skewed (in 2023, spanning from 0.1 in San Marino to 992.8 in South Sudan, with a skewness coefficient > 2.5). We apply the natural logarithmic transformation:
$$y_{it} = \ln(\text{MMR}_{it})$$
This ensures residual homoskedasticity and normal error distributions, while allowing estimated coefficients to be interpreted as constant proportional elasticities or semi-elasticities.

#### B. Cross-Sectional Benchmark Models (OLS)
Estimated at benchmark years $t \in \{2000, 2010, 2023\}$:
$$\ln(\text{MMR}_i) = \beta_0 + \beta_1 \ln(\text{GDP}_{i}) + \beta_2 \text{HealthExp}_{i} + \beta_3 \text{TFR}_i + \beta_4 \text{AdoFert}_i + \beta_5 \text{Urban}_i + \epsilon_i$$
* **Variance-Covariance Estimation:** Huber-White heteroskedasticity-consistent standard errors (HC1) are used to prevent anti-conservative p-values.

#### C. Primary Longitudinal Model: Two-Way Fixed Effects (TWFE)
To isolate within-country changes over time and eliminate confounding from time-invariant national characteristics:
$$\ln(\text{MMR}_{it}) = \alpha_i + \gamma_t + \beta_1 \ln(\text{GDP}_{it}) + \beta_2 \text{HealthExp}_{it} + \beta_3 \text{TFR}_{it} + \beta_4 \text{AdoFert}_{it} + \beta_5 \text{Urban}_{it} + \epsilon_{it}$$
* $\alpha_i$ represents **Country Fixed Effects**, absorbing all historical, cultural, climatic, baseline institutional, and geographic traits of country $i$ that do not change over time.
* $\gamma_t$ represents **Year Fixed Effects**, absorbing all global time shocks (global economic cycles, WHO guideline releases, international drug availability, secular technological advances) that affect all countries equally in year $t$.
* **Within Transformation (Demeaning):**
  For each variable $z_{it}$, the two-way demeaned transformation is computed as:
  $$\tilde{z}_{it} = z_{it} - \bar{z}_{i\cdot} - \bar{z}_{\cdot t} + \bar{z}_{\cdot\cdot}$$
  where $\bar{z}_{i\cdot}$ is the country-specific mean, $\bar{z}_{\cdot t}$ is the annual cross-national mean, and $\bar{z}_{\cdot\cdot}$ is the grand sample mean.
* **Inference and Standard Errors:** Standard errors are clustered at the country level ($\text{CRV1}$):
  $$V_{\text{cluster}} = (X'X)^{-1} \left( \sum_{i=1}^G X_i' \hat{\epsilon}_i \hat{\epsilon}_i' X_i \right) (X'X)^{-1}$$
  This accounts for arbitrary serial correlation and heteroskedasticity across the 24 years within each country.

---

### 3. Handling of Posterior Estimation Uncertainty

The MMEIG 2025 dataset provides Bayesian posterior distributions with 80% Uncertainty Intervals:
* Lower bound: 10th percentile (`0.1`)
* Point estimate: 50th percentile (`0.5`)
* Upper bound: 90th percentile (`0.9`)

To ensure our findings are not artifacts of point estimate assumptions, we conduct **Extreme-Bound Sensitivity Re-Estimation**:
1. *Point Estimate Regression:* $\ln(\text{MMR}_{it}^{50\%})$ as outcome.
2. *Lower Bound Regression:* $\ln(\text{MMR}_{it}^{10\%})$ as outcome.
3. *Upper Bound Regression:* $\ln(\text{MMR}_{it}^{90\%})$ as outcome.

If coefficient signs and statistical significance remain stable across the lower and upper posterior bounds, the relationships are established as robust to measurement uncertainty.

---

### 4. Methodological Strengths & Distinctions from Prior Work

1. **Circumventing Circularity:** By focusing on health expenditure prioritization (% GDP), fertility dynamics, and constant-price purchasing power, we do not regress MMEIG estimates on skilled birth attendance in countries where MMEIG used SBA to generate the estimate.
2. **Elimination of Selection Bias:** Using Solution 1 maintains 177 countries (4,248 observations) in a continuous balanced panel, compared to <40 countries if adult literacy were used.
3. **Purchasing Power Parity:** Utilizing constant 2021 PPP dollars eliminates 24 years of exchange rate swings and inflation distortion.
