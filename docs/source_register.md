# SOURCE REGISTER
## Maternal Mortality Community Research Project (2000–2023)

**Author:** Collaborative Research Team  
**Investigator Profile:** MBBS Physician (Myanmar) transitioning into Health Data Analytics & Clinical Research  
**Phase:** Phase 1 Deliverable — Source Discovery, Data Acquisition, and Verification  
**Date of Audit:** October 2026  

---

### 1. Primary Authoritative Source: WHO / UN MMEIG (2025 Estimation Round)

* **Full Publication Title:** *Trends in maternal mortality 2000 to 2023: estimates by WHO, UNICEF, UNFPA, World Bank Group and UNDESA/Population Division*
* **Publishing Organizations:** World Health Organization (WHO), United Nations Children's Fund (UNICEF), United Nations Population Fund (UNFPA), World Bank Group, and United Nations Department of Economic and Social Affairs (UNDESA) Population Division.
* **Publication Date:** 7 April 2025
* **ISBN:** 978-92-4-010846-2
* **Official License:** Creative Commons Attribution-NonCommercial-ShareAlike 3.0 IGO ([CC BY-NC-SA 3.0 IGO](https://creativecommons.org/licenses/by-nc-sa/3.0/igo/deed.en))
* **Official Publication URL:** [https://www.who.int/publications/i/item/9789240108462](https://www.who.int/publications/i/item/9789240108462)
* **Digital Repository Record (IRIS):** [https://iris.who.int/handle/10665/376483](https://iris.who.int/handle/10665/376483)
* **Direct Report PDF Endpoint:** [https://iris.who.int/server/api/core/bitstreams/29f43a3d-2228-489c-b1e7-b2f28e9101ce/content](https://iris.who.int/server/api/core/bitstreams/29f43a3d-2228-489c-b1e7-b2f28e9101ce/content)
* **Official Data Distribution Zip:** [https://cdn.who.int/media/docs/default-source/reproductive-health/maternal-health/trends-in-maternal-mortality-2000-to-2023-estimates-data.zip?sfvrsn=4718f695_7](https://cdn.who.int/media/docs/default-source/reproductive-health/maternal-health/trends-in-maternal-mortality-2000-to-2023-estimates-data.zip?sfvrsn=4718f695_7)
* **Estimation Methodology Code Repository:** [https://github.com/WorldHealthOrganization/bmat](https://github.com/WorldHealthOrganization/bmat) (BMAT: Bayesian Maternal Mortality Model)
* **Country Profiles Portal:** [https://who.canto.global/b/HH627](https://who.canto.global/b/HH627)

#### Dataset Scope and Characteristics
* **Temporal Coverage:** 1985 to 2023 (complete annual time series; study focus is 2000–2023 covering MDG and SDG periods).
* **Geographic Coverage:** 195 sovereign countries and territories (ISO 3166-1 alpha-3).
* **Measures Provided:**
  1. `mmr`: Maternal Mortality Ratio (maternal deaths per 100,000 live births).
  2. `maternal_deaths`: Estimated absolute count of maternal deaths.
  3. `pm`: Proportion of maternal deaths among all-cause deaths in women aged 15–49.
  4. `lifetime_risk`: Adult lifetime probability of maternal death.
  5. `lifetime_risk_1_in`: Adult lifetime risk expressed as 1-in-N women.
  6. `births`: Annual live births (sourced from UN WPP 2024).
  7. `coviddeaths`, `matcoviddeaths`, `covidmmr`: Excess COVID-19 pandemic mortality attribution.
  8. `hiv_related_indirect_mmr`, `hiv_related_indirect_maternal_deaths`, `hiv_related_indirect_percentage`: HIV-associated indirect maternal mortality.
* **Uncertainty Interval Standard:** 80% Uncertainty Interval (UI), presented as the 10th percentile (`0.1`), median point estimate (`0.5`), and 90th percentile (`0.9`).
* **Input Files Available in Archive:**
  * `main_data.csv`: 4,578 empirical data points from CRVS, specialized mortality studies, and population-based surveys (DHS, MICS, RAMOS).
  * `Other inputs/estimates_base_0all_indicators_v2_sab_shared.xlsx`: Skilled Attendant at Birth (SAB) Bayesian modeled inputs (1985–2023).
  * `Other inputs/WPP2024_Fertility_summary_MMEIG.xlsx`: UN World Population Prospects (WPP 2024) fertility estimates.
  * `Other inputs/GDP MMEIG_2024-07-04 (1).xlsx`: Constant 2021 PPP GDP per capita inputs.

---

### 2. Secondary Authoritative Source: World Bank World Development Indicators (WDI)

* **Source Organization:** World Bank Group (Development Data Group)
* **Access Mechanism:** World Bank Indicators API v2 ([https://api.worldbank.org/v2](https://api.worldbank.org/v2))
* **Documentation:** [https://datahelpdesk.worldbank.org/knowledgebase/articles/898581-api-basic-call-structures](https://datahelpdesk.worldbank.org/knowledgebase/articles/898581-api-basic-call-structures)
* **License:** Creative Commons Attribution 4.0 International ([CC BY 4.0](https://datacatalog.worldbank.org/public-licenses#cc-by))
* **Database Release Version / Metadata Timestamp:** October 2026 update (API `lastupdated: 2026-10-08`)
* **Endpoint Pattern:** `https://api.worldbank.org/v2/country/all/indicator/{INDICATOR_CODE}?date=2000:2023&format=json&per_page=20000`

#### Indicators Registered & Acquired

| Indicator Code | Official Indicator Name | Research Domain | Periodicity | Primary Source Organization |
|---|---|---|---|---|
| `SH.MED.PHYS.ZS` | Physicians (per 1,000 people) | Healthcare Workforce | Annual (sparse) | World Health Organization (Global Health Observatory) |
| `SH.MED.NUMW.P3` | Nurses and midwives (per 1,000 people) | Healthcare Workforce | Annual (sparse) | World Health Organization (GHO) |
| `SE.ADT.LITR.FE.ZS` | Literacy rate, adult female (% ages 15+) | Female Education | Irregular | UNESCO Institute for Statistics (UIS) |
| `SE.SEC.ENRR.FE` | School enrollment, secondary, female (% gross) | Female Education | Annual (moderate) | UNESCO Institute for Statistics (UIS) |
| `SH.STA.BRTC.ZS` | Births attended by skilled health staff (%) | Maternal Healthcare Access | Irregular / Survey | UNICEF & WHO Joint Database |
| `SH.STA.ANVC.ZS` | Pregnant women receiving prenatal care (4+ visits, %) | Maternal Healthcare Access | Irregular / Survey | UNICEF & WHO Joint Database |
| `NY.GDP.PCAP.CD` | GDP per capita (current US$) | Economic Development | Annual | World Bank national accounts data |
| `NY.GDP.PCAP.PP.KD` | GDP per capita, PPP (constant 2021 intl $) | Economic Development (Comparable) | Annual | World Bank, International Comparison Program |
| `SH.XPD.CHEX.PC.CD` | Current health expenditure per capita (current US$) | Health Financing | Annual | World Health Organization (GHED) |
| `SH.XPD.CHEX.GD.ZS` | Current health expenditure (% of GDP) | Health Financing | Annual | World Health Organization (GHED) |
| `SP.DYN.TFRT.IN` | Fertility rate, total (births per woman) | Demographic / Fertility | Annual | UN Population Division (WPP 2024) |
| `SP.ADO.TFRT` | Adolescent fertility rate (births per 1,000 ages 15-19) | Adolescent Reproductive Health | Annual | UN Population Division (WPP 2024) |
| `SP.URB.TOTL.IN.ZS` | Urban population (% of total population) | Urbanization / Infrastructure | Annual | UN Population Division (World Urbanization Prospects) |

---

### 3. Investigation of Additional Potential Sources

As mandated by Phase 1, the following external sources were formally audited to assess whether they provide non-duplicative, openly accessible data for this research.

#### A. WHO Global Health Observatory (GHO)
* **Portal:** [https://www.who.int/data/gho](https://www.who.int/data/gho)
* **Access:** Open API (`https://ghoapi.azureedge.net/api/`) and open CSV downloads.
* **Assessment:** The GHO hosts the same underlying MMEIG estimates and the WHO Global Health Expenditure Database (GHED) indicators that are already mirrored in the World Bank WDI API. Directly querying GHO provides no additional maternal mortality data beyond the primary MMEIG 2025 archive. It remains a valuable reference for specific disease burden estimates if needed.

#### B. UNESCO Institute for Statistics (UIS)
* **Portal:** [https://uis.unesco.org/](https://uis.unesco.org/)
* **Access:** Open bulk download and API.
* **Assessment:** UIS is the source for female adult literacy (`SE.ADT.LITR.FE.ZS`) and secondary enrollment (`SE.SEC.ENRR.FE`). Inspection reveals that direct UIS data have identical coverage limitations to WDI: adult literacy is assessed intermittently through decennial censuses and national surveys, creating extensive gaps (>80% missingness). Secondary school enrollment provides substantially higher coverage and serves as a stronger proxy for female educational attainment across time.

#### C. UNDP Human Development Reports (HDR)
* **Portal:** [https://hdr.undp.org/data-center](https://hdr.undp.org/data-center)
* **Access:** Open download (Composite HDI and Gender Inequality Index [GII]).
* **Assessment:** The Gender Inequality Index (GII) incorporates maternal mortality ratio directly as one of its defining dimensions! Using GII as an independent explanatory variable to predict MMR would introduce mathematical endogeneity and collinearity. Standalone HDI components (education, income) are already captured directly via WDI indicators.

#### D. UN DESA Population Division (World Population Prospects 2024)
* **Portal:** [https://population.un.org/wpp/](https://population.un.org/wpp/)
* **Access:** Open CSV and Excel downloads.
* **Assessment:** WPP 2024 provides the demographic baseline for both MMEIG (female population 15–49, live births, all-cause female deaths) and WDI fertility indicators (`SP.DYN.TFRT.IN`, `SP.ADO.TFRT`). These demographic series are already directly included in our downloaded MMEIG archive (`Estimate_data_v2/Other inputs/WPP2024_Fertility_summary_MMEIG.xlsx`) and matched via the WDI API.

#### E. Demographic and Health Surveys (DHS) Program
* **Portal:** [https://dhsprogram.com/data/](https://dhsprogram.com/data/)
* **Access:** Restricted microdata; requires institutional project registration and research approval. Aggregate indicator reports are public via STATcompiler.
* **Assessment:** While DHS microdata offer deep clinical insight into maternal health practices (e.g., cesarean delivery rates, postpartum checks, transport barriers), the data are cross-sectional surveys conducted every 3–5 years across only ~90 low- and middle-income countries. Bypassing registration is prohibited by Rule 1. The national survey aggregates are already integrated into the MMEIG empirical input database (`main_data.csv`). Microdata analysis is beyond the scope of a cross-country macro-level study.

#### F. UNICEF Data Portal
* **Portal:** [https://data.unicef.org/](https://data.unicef.org/)
* **Access:** Open topic portal. Direct programmatic access to specific sub-pages may be subject to cloud security (HTTP 403 on automated scrapers), but official data files are mirrored through WHO and UN inter-agency releases.
* **Assessment:** UNICEF co-authors the MMEIG report and co-maintains the Joint Skilled Birth Attendance Database with WHO. The full data are already secured through the official WHO distribution package.

---

### 4. Summary of Provenance and Reproducibility Principles

1. **No Data Fabrication:** Every observation in the repository originates from official, traceable WHO/UN MMEIG or World Bank endpoints.
2. **Strict Raw File Preservation:** All downloaded files (`trends-in-maternal-mortality-2000-to-2023-estimates-data.zip`, `9789240108462-eng.pdf`, raw JSON and CSV indicator files) are preserved immutably in `data/raw/`.
3. **Cryptographic Verification:** Every file is hashed with SHA-256 and logged in `data/metadata/download_manifest.json`.
4. **Differentiation of Data Types:** Modeled Bayesian estimates (MMEIG MMR, UN WPP fertility) are strictly differentiated from survey-based intermittent metrics (SBA, literacy) and national accounts data (GDP, health expenditure).
