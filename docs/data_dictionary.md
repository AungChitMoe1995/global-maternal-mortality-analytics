# Data dictionary

One row is one country/territory and calendar year. Missing values remain missing.

| Field | Definition |
|---|---|
| country_iso3 / iso2_code | Country identifiers used in integration |
| country_name | Country/territory name |
| year | Calendar year, 2000–2023 |
| region_name | Acquisition-time World Bank region, not WHO region |
| income_level_name | Acquisition-time WDI income label, held fixed across years |
| mmr_pt / mmr_low / mmr_high | MMEIG posterior median MMR and marginal 10th/90th percentiles, maternal deaths per 100,000 live births |
| maternal_deaths | Country posterior median estimate of maternal deaths |
| live_births | Annual live births supplied by the MMEIG/WPP distribution |
| lifetime_risk_1_in | Estimated lifetime maternal mortality risk as 1 in N |
| gdp_pcap_ppp | GDP per capita, constant 2021 international PPP dollars |
| gdp_pcap_curr | GDP per capita, current US dollars, not used as the longitudinal economic predictor |
| chex_gdp_pct | Current health expenditure as % GDP, including multiple financing sources |
| chex_pcap_curr | Current health expenditure per capita, current US dollars |
| tfr | Total fertility rate, births per woman under current age-specific rates, not individual parity |
| ado_fert_rate | Annual births per 1,000 women aged 15–19 |
| urban_pct | Urban population as % total population, not a direct measure of referral access |
| sab_modeled_pct | MMEIG internally modeled skilled birth attendance %, retained as supplementary context |
| wdi_sba_pct | WDI skilled birth attendance %, intermittently observed |
| female_sec_enroll_pct | Gross female secondary enrollment %, may exceed 100 |
| physicians_per_1k / nurses_midwives_per_1k | National workforce density, potentially incomplete |
| log_* | Natural logarithm of the named positive measure |
| has_all_core_vars | Finite log MMR and all five regression predictors in this row |
| is_balanced_sample | All 24 country-years have finite core variables |
| is_mdg_era / is_sdg_era / is_covid_era | Descriptive period flags: through 2015, from 2016, and from 2020 |

Source measures may themselves be estimated. The project adds no interpolation. GDP and demographic series are not independent of MMEIG's estimation inputs.
