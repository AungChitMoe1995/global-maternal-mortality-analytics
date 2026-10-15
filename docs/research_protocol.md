# Analysis plan and amendment record

**Author:** Dr. Aung Chit Moe (MBBS). **Revision date:** 15 October 2026.

This is a documented analysis plan for a portfolio secondary-data study. It was revised after inspecting data and results and is **not a preregistered protocol**. Hypotheses and specification choices should not be described as prospectively registered.

## Objectives

1. Describe 2000–2023 maternal mortality trends across all 195 countries and territories.
2. Compare country-level inequality by fixed income classification and distinguish country averages from a birth-based aggregate ratio.
3. Explore associations of estimated MMR with economic and demographic indicators while explicitly acknowledging upstream model dependence.

## Population and samples

Full outcome grid: 4,680 country-years. Balanced regression sample: 177 countries and 4,248 rows. All-complete-row comparison: 4,406 observations in 186 countries. Inclusion requires finite outcome and five finite core predictors. The project adds no interpolation or carry-forward values.

## Implemented analyses

The [methods](methodology.md) define units, models, inference, sensitivity analyses and diagnostics. The [statistical report](statistical_analysis.md) contains calculated tables for each fit, including income subsets and unbalanced comparison. Excluded countries and selection summaries are exported. No significance threshold determines which fitted coefficients appear in outputs.

## Changes from the earlier repository release

- Primary contribution changed from claims about macroeconomic effects to descriptive trends and inequalities with exploratory regressions.
- Corrected the claim that excluding SBA removes circularity. GDP and related demographic inputs remain relevant to MMEIG outcome construction.
- Added previously described but absent unbalanced and income-stratified fits, consecutive first differences, VIF, residual diagnostics and country omissions.
- Replaced manual two-way demeaning for panel inference with explicit FE dummy fits that handle unbalanced samples and include FE parameters in covariance correction.
- Corrected outdated 183/12 sample counts to the computed sample. Removed claims that a balanced panel eliminates selection bias.
- Renamed lower/upper uncertainty-bound fits as sensitivity exercises rather than complete measurement-error robustness.
- Removed unmeasured clinical mechanisms and policy effects from the study's findings.
- Rebuilt reports and presentation artifacts from machine-readable results, with input hashes and calculated audit outcomes.

## Remaining analyses not claimed

CRVS-quality-restricted models, full joint-posterior uncertainty propagation, causal identification, and prospective prediction require additional inputs or study design. No ethics approval or journal publication is claimed. This repository uses public national aggregates and contains no patient records.
