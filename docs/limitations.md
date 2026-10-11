# STUDY LIMITATIONS AND METHODOLOGICAL CAVEATS
## Macroeconomic Financing, Demographic Transition, and Global Maternal Mortality (2000–2023)

**Author:** Collaborative Research Team  
**Investigator Profile:** MBBS Physician (Myanmar) transitioning into Healthcare Data Analytics  
**Date:** October 2026  
**Document Type:** Formal Methodological Review & Limitations  

---

### 1. The Ecological Fallacy (Rule 9 Compliance)

The most fundamental methodological limitation of this study is its **cross-country ecological design**. All observations represent national population-level aggregates (country-years), not individual clinical encounters.

* **Clinical Distinction:** Finding that countries with higher real GDP per capita or lower adolescent fertility have lower maternal mortality ratios does **not** mean that wealth directly guarantees individual maternal survival, nor that every pregnant adolescent woman faces an identical biological risk.
* **Mechanism:** Country-level associations capture structural health-system environments (availability of emergency transport, comprehensive obstetric surgery, electricity, and blood supply), which operate at the ecological level. Inferring individual clinical outcomes from national averages is an ecological fallacy.

---

### 2. Nature of the Outcome: Modeled Bayesian Posterior Estimates

As thoroughly verified in Phase 1 and detailed in Chapter 3 of the WHO report:
* Only approximately **54% of global country-years in MMEIG's empirical database** originate from complete Civil Registration and Vital Statistics (CRVS) death registration systems (mostly in High-Income and Upper-Middle-Income countries).
* For low- and lower-middle-income countries (including Myanmar, South Sudan, and much of sub-Saharan Africa), maternal deaths are captured through periodic household surveys (DHS, MICS) or censuses. The annual time series between survey rounds is estimated using the **BMat Bayesian hierarchical model**.
* **Implication:** The outcome variable `mmr_pt` is not an error-free, direct census count. It is a posterior median estimate accompanied by an **80% Uncertainty Interval**. While our sensitivity models demonstrated that regression coefficients remain stable when re-estimated using the lower (`0.1`) and upper (`0.9`) uncertainty limits, the underlying model-based smoothing must be kept in mind when interpreting annual year-to-year shifts.

---

### 3. Limitations of Macro Health Expenditure Indicators

We used **Current Health Expenditure as a percentage of GDP (`chex_gdp_pct`)** from the WHO Global Health Expenditure Database:
* **Allocation Efficiency vs Total Volume:** Spending more on healthcare as a share of GDP does not guarantee that funds reach maternal and child health. A country may allocate high expenditure to tertiary hospital subsidies in capital cities while rural health posts lack basic magnesium sulfate, oxytocin, and sterile delivery kits.
* **Public vs Out-of-Pocket Financing:** `chex_gdp_pct` aggregates both general government health expenditure and private out-of-pocket (OOP) payments. High out-of-pocket spending can act as a financial barrier that delays emergency care (Delay 1), exacerbating maternal risk even while increasing total expenditure.
* **Lagged Health System Capital:** Health expenditure is recorded as an annual flow. In reality, maternal mortality reduction requires multi-year cumulative investments in physical operating theaters, midwifery training colleges, and blood bank infrastructure.

---

### 4. Masking of Severe Sub-National Disparities

National averages inherently obscure sub-national and demographic inequities:
* **Rural vs Urban Disparity:** In countries like Myanmar, Nigeria, or India, maternal mortality ratios in remote, rural, or conflict-affected townships are frequently 3 to 5 times higher than in major metropolitan centers.
* **Ethnic and Socioeconomic Stratification:** National aggregates do not reflect disparities across ethnic minority groups, marginalized indigenous communities, or internally displaced populations (IDPs).

---

### 5. COVID-19 Period Disruptions (2020–2023)

The 2020–2023 period coincided with unprecedented multidimensional global disruptions:
* Direct viral excess maternal mortality (SARS-CoV-2 infection during pregnancy).
* Severe health system disruption (antenatal clinics closed, midwives reassigned, supply chains severed).
* National economic contractions and vital registration interruptions.
* While MMEIG explicitly modeled pandemic mortality attribution (`matcoviddeaths`, `covidmmr`), separating direct biological effects from broader systemic health system paralysis remains complex.
