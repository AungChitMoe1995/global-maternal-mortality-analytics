-- ====================================================================
-- DESCRIPTIVE AND STRATIFIED ANALYTICAL QUERIES
-- Database: data/processed/maternal_mortality.db
-- Author: Collaborative Research Team
-- Date: October 2026
-- ====================================================================

-- 1. Longitudinal Trajectories: Global MMR and Total Maternal Deaths by Year
SELECT 
    year,
    COUNT(DISTINCT country_iso3) AS countries,
    ROUND(AVG(mmr_pt), 1) AS mean_mmr,
    ROUND(MEDIAN(mmr_pt), 1) AS median_mmr,
    ROUND(SUM(maternal_deaths), 0) AS global_maternal_deaths,
    ROUND(SUM(live_births) / 1000000.0, 1) AS global_births_millions,
    ROUND(AVG(gdp_pcap_ppp), 0) AS mean_gdp_ppp,
    ROUND(AVG(chex_gdp_pct), 2) AS mean_health_exp_pct,
    ROUND(AVG(tfr), 2) AS mean_tfr,
    ROUND(AVG(ado_fert_rate), 1) AS mean_ado_fert
FROM analytical_master
GROUP BY year
ORDER BY year;

-- 2. Decadal Progress: Absolute and Relative MMR Changes by World Bank Income Group (2000 vs 2023)
WITH y2000 AS (
    SELECT country_iso3, income_level_name, mmr_pt AS mmr_2000, gdp_pcap_ppp AS gdp_2000, chex_gdp_pct AS chex_2000
    FROM analytical_master
    WHERE year = 2000 AND is_balanced_sample = 1
),
y2023 AS (
    SELECT country_iso3, mmr_pt AS mmr_2023, gdp_pcap_ppp AS gdp_2023, chex_gdp_pct AS chex_2023
    FROM analytical_master
    WHERE year = 2023 AND is_balanced_sample = 1
)
SELECT 
    y2000.income_level_name,
    COUNT(*) AS balanced_countries,
    ROUND(AVG(y2000.mmr_2000), 1) AS avg_mmr_2000,
    ROUND(AVG(y2023.mmr_2023), 1) AS avg_mmr_2023,
    ROUND(AVG(y2023.mmr_2023 - y2000.mmr_2000), 1) AS avg_absolute_change,
    ROUND(100.0 * AVG((y2023.mmr_2023 - y2000.mmr_2000) / y2000.mmr_2000), 1) AS avg_pct_change,
    ROUND(AVG(y2023.chex_2023 - y2000.chex_2000), 2) AS avg_health_exp_change
FROM y2000
JOIN y2023 ON y2000.country_iso3 = y2023.country_iso3
GROUP BY y2000.income_level_name
ORDER BY avg_mmr_2023 DESC;

-- 3. Regional Comparisons: MMR and Health System Prioritization (2023 Benchmark)
SELECT 
    region_name,
    COUNT(DISTINCT country_iso3) AS countries,
    ROUND(AVG(mmr_pt), 1) AS mean_mmr,
    ROUND(MIN(mmr_pt), 1) AS min_mmr,
    ROUND(MAX(mmr_pt), 1) AS max_mmr,
    ROUND(AVG(chex_gdp_pct), 2) AS mean_health_exp_pct,
    ROUND(AVG(gdp_pcap_ppp), 0) AS mean_gdp_ppp,
    ROUND(AVG(tfr), 2) AS mean_tfr,
    ROUND(AVG(ado_fert_rate), 1) AS mean_ado_fert
FROM analytical_master
WHERE year = 2023
GROUP BY region_name
ORDER BY mean_mmr DESC;

-- 4. Case Study Focus: Southeast Asia Country Profiles (2010 vs 2020 vs 2023)
SELECT 
    country_iso3,
    country_name,
    year,
    ROUND(mmr_pt, 1) AS mmr,
    ROUND(mmr_low, 1) AS mmr_low_80ui,
    ROUND(mmr_high, 1) AS mmr_high_80ui,
    ROUND(gdp_pcap_ppp, 0) AS gdp_ppp,
    ROUND(chex_gdp_pct, 2) AS health_exp_pct,
    ROUND(tfr, 2) AS tfr,
    ROUND(ado_fert_rate, 1) AS ado_fert
FROM analytical_master
WHERE country_iso3 IN ('MMR', 'THA', 'VNM', 'KHM', 'LAO', 'IDN', 'MYS', 'PHL')
  AND year IN (2010, 2020, 2023)
ORDER BY country_name, year;
