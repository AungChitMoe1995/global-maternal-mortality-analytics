-- ====================================================================
-- SCHEMA DEFINITION: MATERNAL MORTALITY RESEARCH DATABASE
-- Database: data/processed/maternal_mortality.db
-- Author: Collaborative Research Team
-- Date: October 2026
-- ====================================================================

-- 1. Dimension Table: Countries and Territories
CREATE TABLE IF NOT EXISTS dim_countries (
    country_iso3        TEXT PRIMARY KEY,
    iso2_code           TEXT,
    country_name        TEXT NOT NULL,
    region_name         TEXT,
    income_level_name   TEXT
);

-- 2. Fact Table: WHO/UN MMEIG 2025 Maternal Mortality Estimates
CREATE TABLE IF NOT EXISTS fact_mmeig_estimates (
    country_iso3        TEXT NOT NULL,
    year                INTEGER NOT NULL,
    mmr_low             REAL NOT NULL, -- 10th percentile (lower 80% UI)
    mmr_pt              REAL NOT NULL, -- 50th percentile (median point estimate)
    mmr_high            REAL NOT NULL, -- 90th percentile (upper 80% UI)
    maternal_deaths     REAL,          -- Estimated absolute maternal deaths
    live_births         REAL,          -- WPP 2024 annual live births
    lifetime_risk_1_in  REAL,          -- 1 in N lifetime risk of maternal death
    sab_modeled_pct     REAL,          -- Modeled Skilled Attendant at Birth (%)
    PRIMARY KEY (country_iso3, year),
    FOREIGN KEY (country_iso3) REFERENCES dim_countries(country_iso3)
);

-- 3. Integrated Analytical Master Table
CREATE TABLE IF NOT EXISTS analytical_master (
    country_iso3            TEXT NOT NULL,
    year                    INTEGER NOT NULL,
    country_name            TEXT,
    region_name             TEXT,
    income_level_name       TEXT,
    
    -- Primary Outcome: MMEIG MMR
    mmr_pt                  REAL NOT NULL,
    mmr_low                 REAL NOT NULL,
    mmr_high                REAL NOT NULL,
    log_mmr_pt              REAL NOT NULL,
    log_mmr_low             REAL NOT NULL,
    log_mmr_high            REAL NOT NULL,
    maternal_deaths         REAL,
    live_births             REAL,
    lifetime_risk_1_in      REAL,
    
    -- Economic Development
    gdp_pcap_ppp            REAL, -- Constant 2021 PPP intl $
    log_gdp_pcap_ppp        REAL,
    gdp_pcap_curr           REAL, -- Current US$
    log_gdp_pcap_curr       REAL,
    
    -- Health System Financing Priority
    chex_gdp_pct            REAL, -- Current health exp as % of GDP
    chex_pcap_curr          REAL, -- Current health exp per capita (US$)
    log_chex_pcap_curr      REAL,
    
    -- Demographic & Reproductive Transition
    tfr                     REAL, -- Total fertility rate (births/woman)
    ado_fert_rate           REAL, -- Adolescent fertility rate (births/1k girls 15-19)
    
    -- Infrastructure & Environment
    urban_pct               REAL, -- Urban population % of total
    
    -- Clinical Access & Workforce (Supplemental / Gapped)
    sab_modeled_pct         REAL, -- MMEIG internal modeled SBA (%)
    wdi_sba_pct             REAL, -- WDI survey-based SBA (%)
    female_sec_enroll_pct   REAL, -- UNESCO female secondary gross enrollment (%)
    physicians_per_1k       REAL, -- WHO physicians per 1,000 pop
    nurses_midwives_per_1k  REAL, -- WHO nurses and midwives per 1,000 pop
    
    -- Methodological Flags & Stratifiers
    is_mdg_era              INTEGER NOT NULL, -- 2000-2015
    is_sdg_era              INTEGER NOT NULL, -- 2016-2023
    is_covid_era            INTEGER NOT NULL, -- 2020-2023
    has_all_core_vars       INTEGER NOT NULL, -- Complete case flag (1 or 0)
    is_balanced_sample      INTEGER NOT NULL, -- In balanced 177-country panel (1 or 0)
    
    PRIMARY KEY (country_iso3, year),
    FOREIGN KEY (country_iso3) REFERENCES dim_countries(country_iso3)
);

-- Indices for rapid query performance
CREATE INDEX IF NOT EXISTS idx_analytical_year ON analytical_master(year);
CREATE INDEX IF NOT EXISTS idx_analytical_country ON analytical_master(country_iso3);
CREATE INDEX IF NOT EXISTS idx_analytical_income ON analytical_master(income_level_name);
CREATE INDEX IF NOT EXISTS idx_analytical_region ON analytical_master(region_name);
CREATE INDEX IF NOT EXISTS idx_analytical_balanced ON analytical_master(is_balanced_sample);
