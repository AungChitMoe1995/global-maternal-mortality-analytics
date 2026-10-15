# Coverage and sample selection

Full grid: 4,680 rows in 195 countries and territories.

| variable               |   observed_rows |   missing_pct |
|:-----------------------|----------------:|--------------:|
| country_iso3           |            4680 |          0    |
| year                   |            4680 |          0    |
| mmr_low                |            4680 |          0    |
| mmr_pt                 |            4680 |          0    |
| mmr_high               |            4680 |          0    |
| maternal_deaths        |            4680 |          0    |
| live_births            |            4680 |          0    |
| lifetime_risk_1_in     |            4680 |          0    |
| sab_modeled_pct        |            4680 |          0    |
| iso2_code              |            4656 |          0.51 |
| country_name           |            4680 |          0    |
| region_name            |            4680 |          0    |
| income_level_name      |            4680 |          0    |
| gdp_pcap_ppp           |            4474 |          4.4  |
| gdp_pcap_curr          |            4595 |          1.82 |
| chex_gdp_pct           |            4529 |          3.23 |
| chex_pcap_curr         |            4526 |          3.29 |
| tfr                    |            4656 |          0.51 |
| ado_fert_rate          |            4656 |          0.51 |
| urban_pct              |            4656 |          0.51 |
| female_sec_enroll_pct  |            3250 |         30.56 |
| physicians_per_1k      |            2856 |         38.97 |
| nurses_midwives_per_1k |            2852 |         39.06 |
| wdi_sba_pct            |            2225 |         52.46 |
| log_mmr_pt             |            4680 |          0    |
| log_mmr_low            |            4680 |          0    |
| log_mmr_high           |            4680 |          0    |
| log_gdp_pcap_ppp       |            4474 |          4.4  |
| log_gdp_pcap_curr      |            4595 |          1.82 |
| log_chex_pcap_curr     |            4526 |          3.29 |
| is_mdg_era             |            4680 |          0    |
| is_sdg_era             |            4680 |          0    |
| is_covid_era           |            4680 |          0    |
| has_all_core_vars      |            4680 |          0    |
| is_balanced_sample     |            4680 |          0    |

## Included versus excluded

|   year | group    |   n_countries |   median_mmr |   mean_mmr |
|-------:|:---------|--------------:|-------------:|-----------:|
|   2000 | Included |           177 |        67.64 |     217.74 |
|   2000 | Excluded |            18 |       137.24 |     409.93 |
|   2023 | Included |           177 |        42.11 |     109.57 |
|   2023 | Excluded |            18 |        92.65 |     186.02 |

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

Selection follows completeness, not random sampling. See reports/tables/sample_selection.csv for predictor missingness. No missingness mechanism (MAR/MNAR) is established from these patterns alone.
