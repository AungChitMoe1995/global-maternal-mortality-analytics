-- ====================================================================
-- DATA QUALITY AUDIT QUERIES
-- Database: data/processed/maternal_mortality.db
-- Author: Collaborative Research Team
-- Date: October 2026
-- ====================================================================

-- 1. Check for Duplicate (Country, Year) Records
SELECT 
    country_iso3, 
    year, 
    COUNT(*) AS record_count
FROM analytical_master
GROUP BY country_iso3, year
HAVING COUNT(*) > 1;

-- 2. Check Primary Outcome Uncertainty Interval Consistency (0.1 <= 0.5 <= 0.9)
SELECT 
    country_iso3, 
    year, 
    mmr_low, 
    mmr_pt, 
    mmr_high
FROM analytical_master
WHERE mmr_low > mmr_pt OR mmr_pt > mmr_high;

-- 3. Check for Impossible or Anomalous Negative / Zero Values in Strictly Positive Variables
SELECT 
    country_iso3, 
    year, 
    mmr_pt, 
    gdp_pcap_ppp, 
    chex_gdp_pct, 
    tfr, 
    ado_fert_rate
FROM analytical_master
WHERE mmr_pt <= 0 
   OR gdp_pcap_ppp <= 0 
   OR chex_gdp_pct <= 0 
   OR tfr <= 0 
   OR ado_fert_rate < 0
   OR urban_pct < 0 OR urban_pct > 100;

-- 4. Audit Core Variable Missingness Across Study Window (2000-2023)
SELECT 
    COUNT(*) AS total_grid_cells,
    SUM(CASE WHEN mmr_pt IS NULL THEN 1 ELSE 0 END) AS missing_mmr,
    SUM(CASE WHEN gdp_pcap_ppp IS NULL THEN 1 ELSE 0 END) AS missing_gdp_ppp,
    SUM(CASE WHEN chex_gdp_pct IS NULL THEN 1 ELSE 0 END) AS missing_chex_pct,
    SUM(CASE WHEN tfr IS NULL THEN 1 ELSE 0 END) AS missing_tfr,
    SUM(CASE WHEN ado_fert_rate IS NULL THEN 1 ELSE 0 END) AS missing_ado_fert,
    SUM(CASE WHEN urban_pct IS NULL THEN 1 ELSE 0 END) AS missing_urban,
    SUM(has_all_core_vars) AS complete_case_cells,
    ROUND(100.0 * SUM(has_all_core_vars) / COUNT(*), 2) AS complete_case_pct
FROM analytical_master;

-- 5. Audit Balanced Panel Coverage by Country
SELECT 
    is_balanced_sample,
    COUNT(DISTINCT country_iso3) AS country_count,
    COUNT(*) AS country_year_count
FROM analytical_master
GROUP BY is_balanced_sample;

-- 6. Summary Statistics by World Bank Income Group (Latest Year: 2023)
SELECT 
    income_level_name,
    COUNT(DISTINCT country_iso3) AS country_count,
    ROUND(AVG(mmr_pt), 1) AS mean_mmr,
    ROUND(MIN(mmr_pt), 1) AS min_mmr,
    ROUND(MAX(mmr_pt), 1) AS max_mmr,
    ROUND(AVG(gdp_pcap_ppp), 0) AS mean_gdp_ppp,
    ROUND(AVG(chex_gdp_pct), 2) AS mean_health_exp_pct,
    ROUND(AVG(tfr), 2) AS mean_tfr,
    ROUND(AVG(ado_fert_rate), 1) AS mean_ado_fert
FROM analytical_master
WHERE year = 2023
GROUP BY income_level_name
ORDER BY mean_mmr DESC;
