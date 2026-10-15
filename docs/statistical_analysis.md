# Global Maternal Mortality, 2000–2023

## Statistical analysis


MMEIG estimates already use GDP, general fertility and skilled birth attendance. Regressions on these modeled outcomes are exploratory associations, not independent estimates of causal effects. National fertility does not measure individual parity or spacing.


## Samples


|   all_countries |   all_rows |   balanced_countries |   balanced_rows |   complete_rows |   complete_countries |
|----------------:|-----------:|---------------------:|----------------:|----------------:|---------------------:|
|             195 |       4680 |                  177 |            4248 |            4406 |                  186 |


## Full-sample trends


|   year |   n_countries |   median_mmr |   mean_mmr |   maternal_deaths |   live_births |   aggregate_mmr |
|-------:|--------------:|-------------:|-----------:|------------------:|--------------:|----------------:|
|   2000 |           195 |        70.99 |     235.48 |            440079 |   1.35309e+08 |          325.24 |
|   2010 |           195 |        56.14 |     185.89 |            359736 |   1.42998e+08 |          251.57 |
|   2015 |           195 |        51.87 |     155.75 |            322169 |   1.43934e+08 |          223.83 |
|   2023 |           195 |        46.65 |     116.62 |            248743 |   1.31841e+08 |          188.67 |


Aggregate MMR is 100,000 times the sum of country median death estimates divided by total live births. It is a derived snapshot aggregate, not the official posterior median or uncertainty interval of a global total. Country means and medians answer different questions and weight each country equally.



## Selection into the balanced panel


|   year | group    |   n_countries |   median_mmr |   mean_mmr |
|-------:|:---------|--------------:|-------------:|-----------:|
|   2000 | Included |           177 |        67.64 |     217.74 |
|   2000 | Excluded |            18 |       137.24 |     409.93 |
|   2023 | Included |           177 |        42.11 |     109.57 |
|   2023 | Excluded |            18 |        92.65 |     186.02 |


Excluded countries:


| country_iso3   | country_name              | income_level_name   |
|:---------------|:--------------------------|:--------------------|
| AFG            | Afghanistan               | Low income          |
| COK            | Cook Islands              | Unclassified        |
| CUB            | Cuba                      | Upper middle income |
| DJI            | Djibouti                  | Lower middle income |
| ERI            | Eritrea                   | Low income          |
| IRQ            | Iraq                      | Upper middle income |
| MCO            | Monaco                    | High income         |
| MNE            | Montenegro                | Upper middle income |
| PRI            | Puerto Rico (US)          | High income         |
| PRK            | Korea, Dem. People's Rep. | Low income          |
| SOM            | Somalia, Fed. Rep.        | Low income          |
| SSD            | South Sudan               | Low income          |
| SYR            | Syrian Arab Republic      | Low income          |
| TLS            | Timor-Leste               | Lower middle income |
| UKR            | Ukraine                   | Upper middle income |
| VEN            | Venezuela, RB             | Lower middle income |
| YEM            | Yemen, Rep.               | Low income          |
| ZWE            | Zimbabwe                  | Lower middle income |


Selection is associated with data availability. Neither balanced nor unbalanced complete-case analysis removes this bias.



## Model specification and inference


Log MMR is regressed on log constant-PPP GDP, current health expenditure (% GDP), total fertility, adolescent fertility and urban population (%). Panel fits include explicit country and year dummy columns. Cluster covariance includes the full design rank in its finite-sample adjustment, with t inference using the number of country clusters minus one degrees of freedom. Cross-sections use HC1 standard errors. First differences use consecutive annual changes and year effects. All fits give equal weight to country-years. Fixed effects do not remove changing confounding, reverse causality, or dependence introduced by the MMEIG model.



### Balanced panel

177 countries, 4248 observations.


| label                               |   coefficient |      se |   ci_low |   ci_high |   p_value |
|:------------------------------------|--------------:|--------:|---------:|----------:|----------:|
| Log GDP per capita (constant PPP)   |      -0.49595 | 0.07681 | -0.64754 |  -0.34436 |   0.00000 |
| Current health expenditure (% GDP)  |       0.01097 | 0.00673 | -0.00231 |   0.02425 |   0.10493 |
| Total fertility (births/woman)      |       0.13077 | 0.06240 |  0.00761 |   0.25393 |   0.03755 |
| Adolescent fertility (births/1,000) |      -0.00071 | 0.00207 | -0.00480 |   0.00337 |   0.73176 |
| Urban population (%)                |      -0.00453 | 0.00367 | -0.01178 |   0.00272 |   0.21953 |


### All complete country-years

186 countries, 4406 observations.


| label                               |   coefficient |      se |   ci_low |   ci_high |   p_value |
|:------------------------------------|--------------:|--------:|---------:|----------:|----------:|
| Log GDP per capita (constant PPP)   |      -0.49364 | 0.07197 | -0.63562 |  -0.35165 |   0.00000 |
| Current health expenditure (% GDP)  |       0.00875 | 0.00656 | -0.00418 |   0.02169 |   0.18358 |
| Total fertility (births/woman)      |       0.14323 | 0.05815 |  0.02850 |   0.25796 |   0.01469 |
| Adolescent fertility (births/1,000) |      -0.00071 | 0.00196 | -0.00457 |   0.00316 |   0.71897 |
| Urban population (%)                |      -0.00385 | 0.00341 | -0.01058 |   0.00289 |   0.26090 |


### Balanced panel, 2000–2019

177 countries, 3540 observations.


| label                               |   coefficient |      se |   ci_low |   ci_high |   p_value |
|:------------------------------------|--------------:|--------:|---------:|----------:|----------:|
| Log GDP per capita (constant PPP)   |      -0.52655 | 0.08684 | -0.69793 |  -0.35517 |   0.00000 |
| Current health expenditure (% GDP)  |       0.00241 | 0.00632 | -0.01007 |   0.01489 |   0.70325 |
| Total fertility (births/woman)      |       0.04287 | 0.06358 | -0.08261 |   0.16834 |   0.50105 |
| Adolescent fertility (births/1,000) |       0.00040 | 0.00192 | -0.00340 |   0.00419 |   0.83661 |
| Urban population (%)                |       0.00086 | 0.00353 | -0.00611 |   0.00783 |   0.80728 |


### Outcome: lower 80% UI limit

177 countries, 4248 observations.


| label                               |   coefficient |      se |   ci_low |   ci_high |   p_value |
|:------------------------------------|--------------:|--------:|---------:|----------:|----------:|
| Log GDP per capita (constant PPP)   |      -0.49435 | 0.08296 | -0.65808 |  -0.33061 |   0.00000 |
| Current health expenditure (% GDP)  |       0.01109 | 0.00667 | -0.00208 |   0.02426 |   0.09838 |
| Total fertility (births/woman)      |       0.11096 | 0.06314 | -0.01365 |   0.23557 |   0.08059 |
| Adolescent fertility (births/1,000) |      -0.00125 | 0.00201 | -0.00521 |   0.00271 |   0.53373 |
| Urban population (%)                |      -0.00304 | 0.00393 | -0.01080 |   0.00472 |   0.44018 |


### Outcome: upper 80% UI limit

177 countries, 4248 observations.


| label                               |   coefficient |      se |   ci_low |   ci_high |   p_value |
|:------------------------------------|--------------:|--------:|---------:|----------:|----------:|
| Log GDP per capita (constant PPP)   |      -0.47730 | 0.07624 | -0.62777 |  -0.32683 |   0.00000 |
| Current health expenditure (% GDP)  |       0.01069 | 0.00721 | -0.00354 |   0.02492 |   0.13990 |
| Total fertility (births/woman)      |       0.13307 | 0.06380 |  0.00717 |   0.25897 |   0.03843 |
| Adolescent fertility (births/1,000) |      -0.00026 | 0.00225 | -0.00470 |   0.00418 |   0.90860 |
| Urban population (%)                |      -0.00506 | 0.00375 | -0.01246 |   0.00234 |   0.17864 |


### Consecutive annual first differences

177 countries, 4071 observations.


| label                               |   coefficient |      se |   ci_low |   ci_high |   p_value |
|:------------------------------------|--------------:|--------:|---------:|----------:|----------:|
| Log GDP per capita (constant PPP)   |      -0.20096 | 0.05154 | -0.30268 |  -0.09925 |   0.00014 |
| Current health expenditure (% GDP)  |       0.00887 | 0.00364 |  0.00169 |   0.01605 |   0.01576 |
| Total fertility (births/woman)      |       0.17394 | 0.10449 | -0.03228 |   0.38017 |   0.09777 |
| Adolescent fertility (births/1,000) |      -0.00243 | 0.00191 | -0.00620 |   0.00134 |   0.20541 |
| Urban population (%)                |      -0.00102 | 0.00322 | -0.00737 |   0.00533 |   0.75180 |


### Low income subset

18 countries, 432 observations.


| label                               |   coefficient |      se |   ci_low |   ci_high |   p_value |
|:------------------------------------|--------------:|--------:|---------:|----------:|----------:|
| Log GDP per capita (constant PPP)   |      -0.37899 | 0.20085 | -0.80275 |   0.04477 |   0.07637 |
| Current health expenditure (% GDP)  |       0.00839 | 0.01372 | -0.02056 |   0.03735 |   0.54883 |
| Total fertility (births/woman)      |       0.06065 | 0.11990 | -0.19232 |   0.31363 |   0.61947 |
| Adolescent fertility (births/1,000) |       0.00100 | 0.00263 | -0.00455 |   0.00655 |   0.70870 |
| Urban population (%)                |       0.00875 | 0.01094 | -0.01433 |   0.03184 |   0.43471 |


### Lower middle income subset

43 countries, 1032 observations.


| label                               |   coefficient |      se |   ci_low |   ci_high |   p_value |
|:------------------------------------|--------------:|--------:|---------:|----------:|----------:|
| Log GDP per capita (constant PPP)   |      -0.57509 | 0.15657 | -0.89106 |  -0.25911 |   0.00067 |
| Current health expenditure (% GDP)  |       0.02239 | 0.01290 | -0.00364 |   0.04842 |   0.08986 |
| Total fertility (births/woman)      |       0.22766 | 0.09769 |  0.03051 |   0.42481 |   0.02466 |
| Adolescent fertility (births/1,000) |      -0.00074 | 0.00293 | -0.00666 |   0.00517 |   0.80082 |
| Urban population (%)                |       0.00680 | 0.00537 | -0.00403 |   0.01762 |   0.21234 |


### Upper middle income subset

54 countries, 1296 observations.


| label                               |   coefficient |      se |   ci_low |   ci_high |   p_value |
|:------------------------------------|--------------:|--------:|---------:|----------:|----------:|
| Log GDP per capita (constant PPP)   |      -0.36990 | 0.12787 | -0.62636 |  -0.11343 |   0.00553 |
| Current health expenditure (% GDP)  |       0.01039 | 0.01010 | -0.00986 |   0.03064 |   0.30802 |
| Total fertility (births/woman)      |      -0.06388 | 0.11552 | -0.29558 |   0.16783 |   0.58263 |
| Adolescent fertility (births/1,000) |      -0.00432 | 0.00396 | -0.01226 |   0.00362 |   0.28033 |
| Urban population (%)                |      -0.00704 | 0.00626 | -0.01959 |   0.00551 |   0.26560 |


### High income subset

62 countries, 1488 observations.


| label                               |   coefficient |      se |   ci_low |   ci_high |   p_value |
|:------------------------------------|--------------:|--------:|---------:|----------:|----------:|
| Log GDP per capita (constant PPP)   |      -0.57821 | 0.13293 | -0.84402 |  -0.31240 |   0.00005 |
| Current health expenditure (% GDP)  |      -0.00704 | 0.01439 | -0.03582 |   0.02173 |   0.62636 |
| Total fertility (births/woman)      |       0.12508 | 0.12744 | -0.12975 |   0.37992 |   0.33022 |
| Adolescent fertility (births/1,000) |      -0.00039 | 0.00577 | -0.01193 |   0.01116 |   0.94661 |
| Urban population (%)                |      -0.01763 | 0.01237 | -0.04236 |   0.00710 |   0.15914 |


### 2000 cross-section

177 countries, 177 observations.


| label                               |   coefficient |      se |   ci_low |   ci_high |   p_value |
|:------------------------------------|--------------:|--------:|---------:|----------:|----------:|
| Log GDP per capita (constant PPP)   |      -0.53218 | 0.08971 | -0.70925 |  -0.35511 |   0.00000 |
| Current health expenditure (% GDP)  |      -0.03023 | 0.02793 | -0.08536 |   0.02489 |   0.28053 |
| Total fertility (births/woman)      |       0.26156 | 0.05111 |  0.16067 |   0.36246 |   0.00000 |
| Adolescent fertility (births/1,000) |       0.00905 | 0.00173 |  0.00562 |   0.01247 |   0.00000 |
| Urban population (%)                |      -0.00224 | 0.00394 | -0.01001 |   0.00554 |   0.57062 |


### 2010 cross-section

177 countries, 177 observations.


| label                               |   coefficient |      se |   ci_low |   ci_high |   p_value |
|:------------------------------------|--------------:|--------:|---------:|----------:|----------:|
| Log GDP per capita (constant PPP)   |      -0.64668 | 0.10423 | -0.85242 |  -0.44094 |   0.00000 |
| Current health expenditure (% GDP)  |      -0.04552 | 0.02278 | -0.09048 |  -0.00056 |   0.04727 |
| Total fertility (births/woman)      |       0.15027 | 0.06803 |  0.01598 |   0.28456 |   0.02851 |
| Adolescent fertility (births/1,000) |       0.01256 | 0.00206 |  0.00849 |   0.01662 |   0.00000 |
| Urban population (%)                |      -0.00181 | 0.00392 | -0.00954 |   0.00592 |   0.64468 |


### 2023 cross-section

177 countries, 177 observations.


| label                               |   coefficient |      se |   ci_low |   ci_high |   p_value |
|:------------------------------------|--------------:|--------:|---------:|----------:|----------:|
| Log GDP per capita (constant PPP)   |      -0.80983 | 0.10674 | -1.02053 |  -0.59914 |   0.00000 |
| Current health expenditure (% GDP)  |      -0.03794 | 0.02751 | -0.09224 |   0.01635 |   0.16957 |
| Total fertility (births/woman)      |      -0.00123 | 0.10283 | -0.20421 |   0.20175 |   0.99048 |
| Adolescent fertility (births/1,000) |       0.01406 | 0.00308 |  0.00798 |   0.02014 |   0.00001 |
| Urban population (%)                |       0.00101 | 0.00388 | -0.00666 |   0.00868 |   0.79495 |


## Diagnostics


| term             | label                               |   vif |
|:-----------------|:------------------------------------|------:|
| log_gdp_pcap_ppp | Log GDP per capita (constant PPP)   | 1.047 |
| chex_gdp_pct     | Current health expenditure (% GDP)  | 1.036 |
| tfr              | Total fertility (births/woman)      | 1.841 |
| ado_fert_rate    | Adolescent fertility (births/1,000) | 1.716 |
| urban_pct        | Urban population (%)                | 1.115 |


Within-panel VIF measures collinearity after country/year effects are removed.


|   residual_lag1_correlation |   leave_one_out_gdp_min |   leave_one_out_gdp_max |
|----------------------------:|------------------------:|------------------------:|
|                     0.74266 |                -0.51765 |                -0.46966 |


Residual serial dependence and influential-country slopes are diagnostics, not evidence of causal identification. Clustered SE account for within-country dependence under the cluster assumptions, but do not propagate upstream MMEIG uncertainty or all cross-country dependence.



## Outcome-bound sensitivity


The lower/upper 80% UI fits replace every outcome by its marginal lower/upper limit. These two vectors are not joint posterior draws. They do not yield a posterior interval for a coefficient, represent a worst-case bound, or establish robustness to measurement error. Full uncertainty propagation would require suitable joint posterior draws and an explicit analysis plan.



## Expenditure quartiles


| quartile   |   n_countries |   median_mmr |   lower_chex_pct |   upper_chex_pct |
|:-----------|--------------:|-------------:|-----------------:|-----------------:|
| Q1         |            45 |      170.31  |            1.327 |            4.437 |
| Q2         |            44 |       47.93  |            4.437 |            6.535 |
| Q3         |            44 |       19.204 |            6.535 |            8.501 |
| Q4         |            44 |       13.365 |            8.501 |           27.09  |


Current expenditure is not government budget priority. Its ratio to GDP may change because either numerator or denominator changes.



## Remaining limits


The observational ecological design cannot identify individual risk, parity, birth spacing, health-system mechanisms or intervention effects. The current metadata classify countries using one acquisition-time income classification throughout 2000–2023. Income-stratified results are exploratory, with fewer country clusters in each subgroup. No CRVS-only analysis is claimed: a defensible source-quality classification has not been constructed. No model here establishes predictive performance on unseen countries or future years.



## Reproducibility


Analytical input SHA-256: `1dc945fec2030f3e21e5f47bd0ccfd31bc3dfbb036dcf9c070cc14213522e0e2`. Machine-readable coefficients, sample comparisons, VIF, country omissions and residuals are in `reports/tables/`.



Sources: [WHO 2025 report](https://www.who.int/publications/i/item/9789240108462), [WHO health financing metadata](https://www.who.int/data/gho/data/themes/topics/indicator-groups/indicator-group-details/GHO/health-expenditure).
