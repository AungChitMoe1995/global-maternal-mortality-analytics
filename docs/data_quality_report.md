# Data quality audit

Overall result: **PASS**. 19 calculated checks.

| check                                               |   violations | status   |
|:----------------------------------------------------|-------------:|:---------|
| Unique country-year keys                            |            0 | PASS     |
| One complete 2000–2023 outcome grid per country     |            0 | PASS     |
| Finite positive MMR and ordered uncertainty limits  |            0 | PASS     |
| gdp_pcap_ppp: finite positive observed values       |            0 | PASS     |
| chex_gdp_pct: finite positive observed values       |            0 | PASS     |
| tfr: finite positive observed values                |            0 | PASS     |
| live_births: finite positive observed values        |            0 | PASS     |
| Finite nonnegative observed adolescent fertility    |            0 | PASS     |
| Observed urban percentages in [0,100]               |            0 | PASS     |
| log_mmr_pt: consistent with natural logarithm       |            0 | PASS     |
| log_mmr_low: consistent with natural logarithm      |            0 | PASS     |
| log_mmr_high: consistent with natural logarithm     |            0 | PASS     |
| log_gdp_pcap_ppp: consistent with natural logarithm |            0 | PASS     |
| Complete-case flag matches finite core values       |            0 | PASS     |
| Balanced-panel flag matches 24 complete years       |            0 | PASS     |
| CSV and SQLite values agree                         |            0 | PASS     |
| Enforced schema foreign keys have no orphan rows    |            0 | PASS     |
| CSV and Parquet values agree                        |            0 | PASS     |
| Cached raw-file SHA-256 agrees with manifest        |            0 | PASS     |

Missingness is reported separately. Allowed missing explanatory data do not make a row suitable for regression. These checks assess data integrity, not scientific validity, absence of bias, or correctness of upstream national estimates.

## Missing values

|                        |   missing_rows |
|:-----------------------|---------------:|
| country_iso3           |              0 |
| year                   |              0 |
| mmr_low                |              0 |
| mmr_pt                 |              0 |
| mmr_high               |              0 |
| maternal_deaths        |              0 |
| live_births            |              0 |
| lifetime_risk_1_in     |              0 |
| sab_modeled_pct        |              0 |
| iso2_code              |             24 |
| country_name           |              0 |
| region_name            |              0 |
| income_level_name      |              0 |
| gdp_pcap_ppp           |            206 |
| gdp_pcap_curr          |             85 |
| chex_gdp_pct           |            151 |
| chex_pcap_curr         |            154 |
| tfr                    |             24 |
| ado_fert_rate          |             24 |
| urban_pct              |             24 |
| female_sec_enroll_pct  |           1430 |
| physicians_per_1k      |           1824 |
| nurses_midwives_per_1k |           1828 |
| wdi_sba_pct            |           2455 |
| log_mmr_pt             |              0 |
| log_mmr_low            |              0 |
| log_mmr_high           |              0 |
| log_gdp_pcap_ppp       |            206 |
| log_gdp_pcap_curr      |             85 |
| log_chex_pcap_curr     |            154 |
| is_mdg_era             |              0 |
| is_sdg_era             |              0 |
| is_covid_era           |              0 |
| has_all_core_vars      |              0 |
| is_balanced_sample     |              0 |

## Raw-file provenance

| resource_id              | status   |
|:-------------------------|:---------|
| MMEIG_2025_ESTIMATES_ZIP | MATCH    |
| MMEIG_2025_REPORT_PDF    | MATCH    |
| WB_COUNTRY_METADATA      | MATCH    |
| WB_IND_SH.MED.PHYS.ZS    | MATCH    |
| WB_IND_SE.ADT.LITR.FE.ZS | MATCH    |
| WB_IND_SH.STA.BRTC.ZS    | MATCH    |
| WB_IND_NY.GDP.PCAP.CD    | MATCH    |
| WB_IND_SH.XPD.CHEX.PC.CD | MATCH    |
| WB_IND_SP.DYN.TFRT.IN    | MATCH    |
| WB_IND_SP.ADO.TFRT       | MATCH    |
| WB_IND_SP.URB.TOTL.IN.ZS | MATCH    |
| WB_IND_NY.GDP.PCAP.PP.KD | MATCH    |
| WB_IND_SH.XPD.CHEX.GD.ZS | MATCH    |
| WB_IND_SH.MED.NUMW.P3    | MATCH    |
| WB_IND_SH.STA.ANVC.ZS    | MATCH    |
| WB_IND_SE.SEC.ENRR.FE    | MATCH    |

NOT_CACHED means that raw provenance was not rechecked locally. A missing raw cache is allowed in the lightweight clone. A mismatching cached hash fails the audit. Re-downloading current WDI data is a new data version and may change findings. The project performs no additional interpolation; upstream MMEIG and WDI series may themselves be modeled or interpolated.
