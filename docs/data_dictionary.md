# DATA DICTIONARY
## Maternal Mortality Analytical Database (2000–2023)

**Master Dataset:** `data/processed/maternal_mortality_analytical_master.csv` / `.parquet` / `.db`  
**Observational Unit:** Country-Year Grid Cell (195 Sovereign Countries × 24 Calendar Years = 4,680 Observations)  
**Author:** Collaborative Research Team  
**Date:** October 2026  

---

### Variable Definitions & Metadata

| Variable Name | Storage Type | Domain | Measurement Unit | Value Range (Observed) | Missing % (2000–2023) | Description & Provenance |
|---|---|---|---|---|---|---|
| `country_iso3` | TEXT | Identifier | ISO 3166-1 alpha-3 | 195 codes | **0.0%** | Standard 3-letter international country identifier (e.g., `MMR`, `THA`, `USA`). Primary key component. |
| `year` | INTEGER | Temporal | Calendar Year | 2000 – 2023 | **0.0%** | Annual calendar year. Primary key component. |
| `country_name` | TEXT | Geography | String | 195 entities | **0.0%** | Standardized sovereign country name from World Bank metadata. |
| `region_name` | TEXT | Geography | Category | 7 World Bank regions | **0.0%** | Regional grouping (e.g., `East Asia & Pacific`, `Sub-Saharan Africa`, `Europe & Central Asia`). |
| `income_level_name` | TEXT | Socioeconomic | Category | 4 World Bank tiers | **0.0%** | World Bank income classification: `Low income`, `Lower middle income`, `Upper middle income`, `High income`. |
| `mmr_pt` | REAL | Primary Outcome | Deaths / 100k births | 0.1 – 1,661.5 | **0.0%** | **Maternal Mortality Ratio (Point Estimate):** Posterior median (50th percentile) estimate of maternal deaths per 100,000 live births. *Source: WHO/UN MMEIG 2025 round.* |
| `mmr_low` | REAL | Outcome Bound | Deaths / 100k births | 0.1 – 1,446.5 | **0.0%** | **Lower 80% Uncertainty Bound:** 10th percentile of posterior distribution. *Source: WHO/UN MMEIG 2025.* |
| `mmr_high` | REAL | Outcome Bound | Deaths / 100k births | 0.2 – 1,939.8 | **0.0%** | **Upper 80% Uncertainty Bound:** 90th percentile of posterior distribution. *Source: WHO/UN MMEIG 2025.* |
| `log_mmr_pt` | REAL | Transformed Outcome | Natural log | -2.30 – 7.42 | **0.0%** | Natural logarithm of `mmr_pt`: $\ln(\text{mmr\_pt})$. Primary dependent variable in regression models. |
| `log_mmr_low` | REAL | Transformed Bound | Natural log | -2.30 – 7.28 | **0.0%** | Natural logarithm of `mmr_low`: $\ln(\text{mmr\_low})$. Used for lower-bound sensitivity re-estimation. |
| `log_mmr_high` | REAL | Transformed Bound | Natural log | -1.61 – 7.57 | **0.0%** | Natural logarithm of `mmr_high`: $\ln(\text{mmr\_high})$. Used for upper-bound sensitivity re-estimation. |
| `maternal_deaths` | REAL | Mortality Burden | Count of deaths | 0.0 – 81,173.0 | **0.0%** | Estimated absolute annual maternal deaths in the population. *Source: WHO/UN MMEIG 2025.* |
| `live_births` | REAL | Demography | Count of births | 185 – 28,142,504 | **0.0%** | Annual live births from UN DESA World Population Prospects (WPP 2024). Denominator for MMR calculation. |
| `lifetime_risk_1_in` | REAL | Cumulative Risk | 1 in N women | 17 – 100,000 | **0.0%** | Adult lifetime risk of maternal death expressed as 1 in N women aged 15 dying of obstetric causes. *Source: MMEIG 2025.* |
| `gdp_pcap_ppp` | REAL | Macroeconomic | Constant 2021 intl $ | \$702.8 – \$149,025.1 | **4.4%** | **GDP per capita, PPP:** Real per capita gross domestic product adjusted for purchasing power parity (constant 2021 international dollars). *Source: World Bank (`NY.GDP.PCAP.PP.KD`).* |
| `log_gdp_pcap_ppp` | REAL | Transformed Predictor | Natural log | 6.56 – 11.91 | **4.4%** | Natural logarithm of real GDP per capita: $\ln(\text{gdp\_pcap\_ppp})$. Core explanatory variable. |
| `gdp_pcap_curr` | REAL | Macroeconomic | Current US$ | \$109.6 – \$256,799.9 | **1.8%** | Nominal GDP per capita in unadjusted current US dollars. *Source: World Bank (`NY.GDP.PCAP.CD`).* |
| `log_gdp_pcap_curr` | REAL | Transformed Predictor | Natural log | 4.70 – 12.46 | **1.8%** | Natural logarithm of nominal GDP per capita: $\ln(\text{gdp\_pcap\_curr})$. |
| `chex_gdp_pct` | REAL | Health Financing | Percentage (%) | 1.22% – 27.09% | **3.2%** | **Current Health Expenditure as % of GDP:** Domestic prioritization of total health spending. *Source: WHO GHED via World Bank (`SH.XPD.CHEX.GD.ZS`).* |
| `chex_pcap_curr` | REAL | Health Financing | Current US$ | \$4.18 – \$13,473.2 | **3.3%** | Total current health expenditure per capita in nominal US dollars. *Source: WHO GHED (`SH.XPD.CHEX.PC.CD`).* |
| `log_chex_pcap_curr`| REAL | Transformed Predictor | Natural log | 1.43 – 9.51 | **3.3%** | Natural logarithm of health spending per capita: $\ln(\text{chex\_pcap\_curr})$. |
| `tfr` | REAL | Demography | Births per woman | 0.72 – 7.83 | **0.5%** | **Total Fertility Rate:** Average number of children born to a woman over her childbearing life. *Source: UN WPP 2024 (`SP.DYN.TFRT.IN`).* |
| `ado_fert_rate` | REAL | Demography | Births / 1,000 ages 15–19 | 0.51 – 206.36 | **0.5%** | **Adolescent Fertility Rate:** Annual births per 1,000 adolescent girls aged 15–19. *Source: UN WPP 2024 (`SP.ADO.TFRT`).* |
| `urban_pct` | REAL | Infrastructure | Percentage (%) | 8.04% – 100.0% | **0.5%** | **Urban Population %:** Percentage of national population residing in urban areas. *Source: UN WUP (`SP.URB.TOTL.IN.ZS`).* |
| `sab_modeled_pct` | REAL | Clinical Covariate | Percentage (%) | 8.89% – 100.0% | **0.0%** | **Modeled Skilled Attendant at Birth (%):** Continuous time series modeled by WHO/UNICEF Joint Database. *Source: MMEIG internal input archive.* |
| `wdi_sba_pct` | REAL | Clinical Covariate | Percentage (%) | 5.60% – 100.0% | **52.5%** | Survey-based Skilled Birth Attendance from routine DHS/MICS reports in WDI (`SH.STA.BRTC.ZS`). (100% missing in 2023). |
| `female_sec_enroll_pct` | REAL | Female Education | Gross enrollment % | 0.0% – 174.8% | **30.6%** | Female gross secondary school enrollment ratio. *Source: UNESCO UIS via World Bank (`SE.SEC.ENRR.FE`).* |
| `physicians_per_1k`| REAL | Health Workforce | Physicians / 1k pop | 0.01 – 9.54 | **39.0%** | Medical doctor density. *Source: WHO GHO via World Bank (`SH.MED.PHYS.ZS`).* |
| `nurses_midwives_per_1k`| REAL | Health Workforce | Nurses/Midwives / 1k pop | 0.09 – 20.83 | **39.1%** | Nursing and midwifery personnel density. *Source: WHO GHO via World Bank (`SH.MED.NUMW.P3`).* |
| `is_mdg_era` | INTEGER | Epoch Flag | Binary (0 or 1) | 0 or 1 | **0.0%** | Indicator equal to 1 if year is between 2000 and 2015 (MDG tracking window), 0 otherwise. |
| `is_sdg_era` | INTEGER | Epoch Flag | Binary (0 or 1) | 0 or 1 | **0.0%** | Indicator equal to 1 if year is between 2016 and 2023 (SDG tracking window), 0 otherwise. |
| `is_covid_era` | INTEGER | Epoch Flag | Binary (0 or 1) | 0 or 1 | **0.0%** | Indicator equal to 1 if year is between 2020 and 2023 (COVID-19 pandemic period), 0 otherwise. |
| `has_all_core_vars`| INTEGER | Sample Flag | Binary (0 or 1) | 0 or 1 | **0.0%** | Complete case flag: equal to 1 if all 6 core model variables are non-null in that country-year, 0 otherwise (4,406 complete cases). |
| `is_balanced_sample`| INTEGER | Sample Flag | Binary (0 or 1) | 0 or 1 | **0.0%** | Balanced panel membership flag: equal to 1 if the country has all 24 years complete for core model variables (177 countries, 4,248 obs), 0 otherwise. |
