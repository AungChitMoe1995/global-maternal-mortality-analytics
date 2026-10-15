# Source register

- [WHO/UN MMEIG, Trends in maternal mortality 2000 to 2023](https://www.who.int/publications/i/item/9789240108462), published 7 April 2025. Outcome estimates, live births, maternal death estimates and uncertainty limits come from its linked distribution archive.
- [WHO full methodological report](https://pmnch.who.int/docs/librariesprovider9/meeting-reports/9789240108462-web-final.pdf?sfvrsn=db2a572e_3), sections 3.2.4 and 3.4.2, describes the GDP, general-fertility and skilled-attendance predictors and their role in data-sparse settings.
- [World Bank WDI](https://databank.worldbank.org/source/world-development-indicators) supplies economic and demographic indicators through the API. Indicator metadata and original responses are cached by acquisition scripts.
- [WHO financing definitions](https://www.who.int/data/gho/data/themes/topics/indicator-groups/indicator-group-details/GHO/health-expenditure) distinguish current expenditure from government expenditure and out-of-pocket financing.

The MMEIG and WDI series are not independent confirmations of mortality. GDP and demographic information can inform the MMEIG model. WDI also republishes indicators produced by other agencies. File hashes provide provenance, not validation of epidemiological truth.

Country metadata use World Bank regional groupings, not WHO regions. Income labels remain fixed to this acquisition snapshot. Cook Islands is Unclassified in WDI here.

## Acquired resources

The original retrieval timestamps are retained below. Cached raw files are rehashed by the audit when available. Re-downloading mutable WDI endpoints constitutes a new version.

| resource_id              | source                | retrieval_timestamp              | local_path                                                                  | sha256                                                           |
|:-------------------------|:----------------------|:---------------------------------|:----------------------------------------------------------------------------|:-----------------------------------------------------------------|
| MMEIG_2025_ESTIMATES_ZIP | WHO/UN MMEIG          | 2026-10-09T03:50:54.975952+00:00 | data/raw/mmeig/trends-in-maternal-mortality-2000-to-2023-estimates-data.zip | c8b60a75cbcb64f7bc7c05d2dea725d885d3915b052307cd588c3fbf766b9227 |
| MMEIG_2025_REPORT_PDF    | WHO/UN MMEIG          | 2026-10-09T03:50:54.975952+00:00 | data/raw/mmeig/9789240108462-eng.pdf                                        | e2e6773eb78614e99707a9d658a54317d4fa122492318f5bb7e76cfd42dc7869 |
| WB_COUNTRY_METADATA      | World Bank API v2     | 2026-10-09T03:51:49.743954+00:00 | data/raw/world_bank/csv/wb_countries_metadata.csv                           | 0e54f9d231b2eb8b9eb5a268cedf207febccea71869d488777c2c47a086d7548 |
| WB_IND_SH.MED.PHYS.ZS    | World Bank WDI API v2 | 2026-10-09T03:51:51.705637+00:00 | data/raw/world_bank/csv/SH.MED.PHYS.ZS.csv                                  | 581604a1a6e14bec215f526b5edc2bb7dc8ea0a7bc0b9a3708ae1114c8a2b5e7 |
| WB_IND_SE.ADT.LITR.FE.ZS | World Bank WDI API v2 | 2026-10-09T03:51:58.038989+00:00 | data/raw/world_bank/csv/SE.ADT.LITR.FE.ZS.csv                               | 056ecb8bd123f2df3d5188b63543ba301cc12d70316fa0845f80bf33b90ba025 |
| WB_IND_SH.STA.BRTC.ZS    | World Bank WDI API v2 | 2026-10-09T03:52:01.901131+00:00 | data/raw/world_bank/csv/SH.STA.BRTC.ZS.csv                                  | 36dddb991d6aab3cc582990b6c482706ad310d09ca30443892afdaa5690f4d68 |
| WB_IND_NY.GDP.PCAP.CD    | World Bank WDI API v2 | 2026-10-09T03:52:03.317572+00:00 | data/raw/world_bank/csv/NY.GDP.PCAP.CD.csv                                  | 23071668aef7ec8e457a96597dfcf0c9154aef86ddaa92fcc1d073db9f295fb2 |
| WB_IND_SH.XPD.CHEX.PC.CD | World Bank WDI API v2 | 2026-10-09T03:52:05.262935+00:00 | data/raw/world_bank/csv/SH.XPD.CHEX.PC.CD.csv                               | 2336952bd0145ed6c5ea96952b9400f501ea47b089584878062d268ef243aa65 |
| WB_IND_SP.DYN.TFRT.IN    | World Bank WDI API v2 | 2026-10-09T03:52:07.600454+00:00 | data/raw/world_bank/csv/SP.DYN.TFRT.IN.csv                                  | dd263d7c905dcc6d3f3283bb9c02d3e5c282519f2253c2c9d4753b8826c5afad |
| WB_IND_SP.ADO.TFRT       | World Bank WDI API v2 | 2026-10-09T03:52:11.150080+00:00 | data/raw/world_bank/csv/SP.ADO.TFRT.csv                                     | 402cea787c6eb76a5425a96f6ce0df578160c2c126b2c02f4667b593dcd2b166 |
| WB_IND_SP.URB.TOTL.IN.ZS | World Bank WDI API v2 | 2026-10-09T03:52:17.632821+00:00 | data/raw/world_bank/csv/SP.URB.TOTL.IN.ZS.csv                               | 5b59510989291a942336edbd117480a9a8e510927989f8f0414da52fbb6dd64b |
| WB_IND_NY.GDP.PCAP.PP.KD | World Bank WDI API v2 | 2026-10-09T03:52:19.481126+00:00 | data/raw/world_bank/csv/NY.GDP.PCAP.PP.KD.csv                               | 79c5d2e589cfc114674e3feafa9be61b495893504368434dd4d6d0c7c88e1194 |
| WB_IND_SH.XPD.CHEX.GD.ZS | World Bank WDI API v2 | 2026-10-09T03:52:20.832417+00:00 | data/raw/world_bank/csv/SH.XPD.CHEX.GD.ZS.csv                               | 5051d23730b8104bbe9a3e17413599f624f012f1d7345956b32c198df0aaf6aa |
| WB_IND_SH.MED.NUMW.P3    | World Bank WDI API v2 | 2026-10-09T03:52:29.891633+00:00 | data/raw/world_bank/csv/SH.MED.NUMW.P3.csv                                  | 434ff36b4edcdcda43c2b6996b8efab9e568cfb8a3d0ba08bc97ca9504cd2bb0 |
| WB_IND_SH.STA.ANVC.ZS    | World Bank WDI API v2 | 2026-10-09T03:52:39.162419+00:00 | data/raw/world_bank/csv/SH.STA.ANVC.ZS.csv                                  | bd3f63fc55d8fa56bbab6c90dd69453b878de5bd7a48e9ca9825482ed117c17d |
| WB_IND_SE.SEC.ENRR.FE    | World Bank WDI API v2 | 2026-10-09T03:52:47.023313+00:00 | data/raw/world_bank/csv/SE.SEC.ENRR.FE.csv                                  | 226f633983d82c91dbd3212c0b44ac0224f8324eab6888936859f87f8aafd0c8 |
