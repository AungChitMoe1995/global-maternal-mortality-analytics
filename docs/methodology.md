# Methods

## Research question and design

How did estimated national maternal mortality change from 2000 to 2023, how did inequalities differ by fixed income classification, and what exploratory associations appear with economic and demographic indicators?

This is a secondary analysis of public country-year aggregates. Descriptive analyses retain all 195 countries and territories. Regression analyses use 177 countries with complete data for all 24 years (4,248 rows) and compare the result with 4,406 complete country-years in an unbalanced panel. Equal country-year weighting describes the average country association rather than the average pregnancy.

## Outcome and provenance

MMR is estimated maternal deaths per 100,000 live births. The 2025 MMEIG estimation round supplies posterior medians and marginal 80% uncertainty limits, not complete annual censuses of maternal deaths. GDP uses constant 2021 international PPP dollars. SHA-256 records establish file identity, not scientific validity. See the [source register](source_register.md) and [calculated audit](data_quality_report.md).

## Dependence on the upstream model

The [WHO report](https://pmnch.who.int/docs/librariesprovider9/meeting-reports/9789240108462-web-final.pdf?sfvrsn=db2a572e_3), sections 3.2.4 and 3.4.2, identifies GDP per capita, general fertility rate and skilled birth attendance as BMat predictors. In data-sparse settings these predictors can strongly inform the estimated mortality trajectory. Regressing MMEIG MMR on GDP is therefore partly dependent on the construction of the outcome. Total fertility rate is distinct from general fertility rate, but related demographic inputs also limit independence. Omitting skilled birth attendance does not remove circularity. The models describe associations in this snapshot and do not independently estimate effects of GDP or fertility.

## Descriptive estimands

- Country mean and country median MMR give every country equal weight.
- Derived aggregate MMR is 100,000 × sum(country posterior median maternal deaths) / sum(live births). It is a snapshot calculation and need not equal the posterior median of the official aggregate. Marginal uncertainty limits are not summed to construct aggregate uncertainty.
- Income classifications come from the WDI country metadata acquired with this dataset and remain fixed throughout 2000–2023. They are not historical income classifications. Cook Islands lacks a WDI classification and is labeled Unclassified.
- Expenditure quartile boundaries come from the observed 2023 balanced sample. Both counts and boundaries are exported.

## Exploratory model specification

`log(MMR_it) = country_FE_i + year_FE_t + b1*log(GDP_PPP_it) + b2*CHE_GDP_it + b3*TFR_it + b4*adolescent_fertility_it + b5*urban_pct_it + error_it`.

Explicit country/year dummy variables correctly handle both balanced and unbalanced samples. The full design parameter count enters the cluster covariance finite-sample correction. Panel standard errors cluster by country, with t inference on G−1 degrees of freedom. Cross-sectional fits in 2000, 2010 and 2023 use HC1 standard errors with t inference. Fixed effects account for fixed national differences and common year shocks, not time-varying confounding or reverse causality. Log transformation does not guarantee normal or homoskedastic residuals.

GDP is a log-log coefficient. Other slopes are semi-elasticities per displayed indicator unit. Report estimates with 95% confidence intervals. These intervals are conditional regression intervals, not intervals for an intervention effect and not a full propagation of MMEIG estimation uncertainty. No predictive validation is claimed.

## Sensitivity analyses actually implemented

1. All complete country-years, with country and year effects.
2. Balanced countries restricted to 2000–2019.
3. Separate lower and upper marginal MMR uncertainty-limit outcomes.
4. Consecutive annual first differences of outcome and predictors, with year effects and country-clustered inference.
5. Separate models within the fixed income tiers. These exploratory subgroup analyses have fewer country clusters and do not establish differences between subgroup coefficients.

Outcome-bound replacements are not joint posterior draws. They neither supply posterior coefficient uncertainty nor prove robustness to measurement error. A source-quality-restricted analysis is not implemented because defensible country-period CRVS quality classifications have not been constructed. Presence of any CRVS record alone would not justify such a classification.

## Diagnostics and sample selection

Export within-transformed predictor VIF, country-model residuals, pooled within-country lag-1 residual correlation and GDP slopes after omitting one country at a time. The omission exercise re-demeans the remaining rectangular panel and uses least squares; it is a descriptive influence diagnostic without new inferential claims. Compare baseline and endpoint characteristics and missingness for included and excluded countries. Complete-case analysis can exclude countries systematically and does not eliminate selection bias.

## Interpretation of financing and fertility

Current health expenditure as a share of GDP includes public, private and external financing. It does not isolate government priority, maternal health budgets or efficient service delivery. The GDP denominator can change independently of spending. [WHO publishes distinct financing indicators](https://www.who.int/data/gho/data/themes/topics/indicator-groups/indicator-group-details/GHO/health-expenditure) for government expenditure, private expenditure and out-of-pocket payments.

National total fertility does not measure a woman's parity or spacing. Adolescent fertility is a national birth rate, not an individual risk estimate. The dataset cannot identify hemorrhage, eclampsia, referral delays, roads or blood-bank mechanisms. Such mechanisms require appropriate clinical or health-system data and separate literature evidence.
