> Historical acquisition record: the current methods and sample counts are maintained in methodology.md and research_protocol.md. Original retrieval records below are retained for provenance.

# DATA ACQUISITION AND ENGINEERING RUN LOG
## Maternal Mortality Community Research Project (2000–2023)

**Author:** Collaborative Research Team  
**Investigator Profile:** MBBS Physician (Myanmar) transitioning into Health Data Analytics & Clinical Research  
**Phase:** Phase 1 Deliverable — Source Discovery, Data Acquisition, and Verification  
**Run Timestamp:** October 2026  
**Environment:** Windows (PowerShell), Python 3.12.8, Pandas 3.0.5, Requests 2.34.2, PyMuPDF 1.28.2, Pytest 9.1.1  

---

### 1. Execution Chronology

| Step | Action Description | Target Endpoint / Script | Execution Result / Status | Notes & Verification |
|---|---|---|---|---|
| **01** | Initial Directory Inspection | Workspace root | Clean directory | Initialized repository skeleton. |
| **02** | Python Environment Check | `python --version`, `pip list` | Python 3.12.8 | Verified presence of `pandas`, `requests`, `numpy`, `statsmodels`, `openpyxl`, `pymupdf`, `pytest`. |
| **03** | Source Discovery: UNICEF Portal | `https://data.unicef.org/...` | HTTP 403 Forbidden | Cloudflare bot protection on automated direct connection to UNICEF frontend. |
| **04** | Source Discovery: WHO Portal | `https://www.who.int/publications/i/item/9789240108462` | HTTP 200 OK | Successfully retrieved official WHO MMEIG publication page. |
| **05** | Link & Asset Extraction | WHO publication DOM parsing | Discovered official CDN ZIP and IRIS report bitstream | Located complete input dataset ZIP and official PDF report. |
| **06** | MMEIG Archive Acquisition | `https://cdn.who.int/.../trends-in-maternal-mortality-2000-to-2023-estimates-data.zip` | HTTP 200 OK (12,411,704 bytes) | Downloaded to `data/raw/mmeig/`. SHA-256 verified. |
| **07** | MMEIG Report PDF Acquisition | `https://iris.who.int/.../bitstreams/29f43a3d-.../content` | HTTP 200 OK (4,772,148 bytes) | Downloaded to `data/raw/mmeig/9789240108462-eng.pdf`. Full 132-page report verified. |
| **08** | MMEIG Archive Extraction | `trends-in-maternal-mortality-...zip` | Extracted to `data/raw/mmeig/extracted/` | Extracted 74 files including `estimates.csv`, `estimates_arr.csv`, `main_data.csv`, and 54 aggregate files. |
| **09** | MMEIG Schema & Integrity Audit | `scratch/inspect_estimates.py` | 100,029 rows across 195 countries (1985–2023) | Confirmed 15 epidemiological parameters, 80% Uncertainty Intervals (`0.1`, `0.5`, `0.9`), zero nulls in MMR, zero UI violations. |
| **10** | Methodological Review of Report PDF | `scratch/read_definitions.py`, `scratch/find_ui_details.py` | PyMuPDF extraction of Chapters 2 & 3 | Verified official definitions, 80% UI standard, and identified MMEIG model covariates (SBA, GDP, GFR). |
| **11** | World Bank API Metadata Verification | `https://api.worldbank.org/v2/indicator/{code}?format=json` | HTTP 200 OK across 12 candidate indicators | Verified indicator names, source organizations, and definitions. |
| **12** | World Bank Country Classification | `https://api.worldbank.org/v2/country?format=json&per_page=500` | HTTP 200 OK (296 entities) | Separated 217 sovereign countries from 79 regional/income aggregates. |
| **13** | World Bank Production Acquisition | `src/download_world_bank.py` | HTTP 200 OK across all indicators | Retrieved 6,360–6,384 records per indicator for 2000–2023. Saved raw JSON and CSV. |
| **14** | Source Profiling & Coverage Audit | `src/inspect_sources.py` | Generated inventory & coverage matrix | Profiled 195 MMEIG countries × 24 years (4,680 cells). Generated `indicator_inventory.csv` & `country_year_coverage.csv`. |
| **15** | Automated Test Suite Execution | `pytest tests/ -v` | 4 passed in 0.71s | Verified file existence, schema integrity, UI ordering, and manifest integrity. |

---

### 2. File Verification & Provenance Registry

#### Primary MMEIG Assets
* **Raw ZIP File:** `data/raw/mmeig/trends-in-maternal-mortality-2000-to-2023-estimates-data.zip`
  * Size: 12,411,704 bytes
  * SHA-256: `637651a02796120ef2dfcfb9bf9b5c3ff90250085a81ca6e8a0fa2e896cb077c`
  * Source URL: `https://cdn.who.int/media/docs/default-source/reproductive-health/maternal-health/trends-in-maternal-mortality-2000-to-2023-estimates-data.zip?sfvrsn=4718f695_7`
* **Official Report PDF:** `data/raw/mmeig/9789240108462-eng.pdf`
  * Size: 4,772,148 bytes
  * SHA-256: `a937a076722d36fa33c7f3cf2efeb7b1aeb0cfec2ad79ff1cbce1f6f1a8eec3d`
  * Source URL: `https://iris.who.int/server/api/core/bitstreams/29f43a3d-2228-489c-b1e7-b2f28e9101ce/content`
* **Country Estimates Table:** `data/raw/mmeig/extracted/Estimate_data_v2/Estimates/estimates.csv`
  * Rows: 100,029 | Columns: 7 | Countries: 195 | Years: 1985–2023
  * Primary Parameter: `mmr` (4,680 country-year records in 2000–2023 study window; 0 missing, 0 duplicates)

#### World Bank Indicator Assets
All acquired with 2000–2023 temporal filters, raw JSON preserved in `data/raw/world_bank/json/`, structured CSV in `data/raw/world_bank/csv/`:
1. `wb_countries_metadata.csv` (26,501 bytes, SHA-256: `e06c117b34f86d8a39a9c51235338169992f1f1d13f98218175510659be432e7`)
2. `NY.GDP.PCAP.CD.csv` (579,096 bytes, SHA-256: `c8a2b53460835f11aee699f790ddab8df21820dd5aeceea48c69cb452aa82a2d`)
3. `NY.GDP.PCAP.PP.KD.csv` (751,921 bytes, SHA-256: `ce4d1db26aaae8feec3a0c20ab24e23cfc2aa7c88b0a944cb4ca14fc9ae49f50`)
4. `SE.ADT.LITR.FE.ZS.csv` (747,826 bytes, SHA-256: `25c61ea0e801b702ecf0e7492f58fa99694e772eaef28b84931be0e657c74232`)
5. `SE.SEC.ENRR.FE.csv` (682,892 bytes, SHA-256: `25f6fa720e5884ce43dd6efc4bbcf4032d847da4f4b2ea62d5f1715451e50f58`)
6. `SH.MED.NUMW.P3.csv` (576,546 bytes, SHA-256: `3bdfdcba3b00fe6b2a08f51a21cf89eb52fcff8d6fc31bdfd9b3fe1966a987d6`)
7. `SH.MED.PHYS.ZS.csv` (519,128 bytes, SHA-256: `2fbf608bf3978cf4b64b3ef86909faae443658dc7a18bb931fa38dcdd9c1f2b2`)
8. `SH.STA.ANVC.ZS.csv` (577,766 bytes, SHA-256: `8c278a221fcaec97d1e99d4fb9fefcbe8a8c909c0fa4a9d70172ba9c7e098ffb`)
9. `SH.STA.BRTC.ZS.csv` (648,588 bytes, SHA-256: `0dc87c703b6dbe45e8557d42514aa41c304d96a5d429a3a9bf8c8313c01bf0ea`)
10. `SH.XPD.CHEX.GD.ZS.csv` (620,713 bytes, SHA-256: `bda8d98dcfdb2c219f9f8c679e9508544dca5f9172d5b62b0e6df2fc530ca063`)
11. `SH.XPD.CHEX.PC.CD.csv` (721,635 bytes, SHA-256: `4119e7a68427f71bce855019d08e1b12bdf776c59b2d8616194b5952db5a31a9`)
12. `SP.ADO.TFRT.csv` (737,052 bytes, SHA-256: `955d496e6761dc970c9973273eef1284d16ca40aa0ea03a5e019a16f27f093ee`)
13. `SP.DYN.TFRT.IN.csv` (615,865 bytes, SHA-256: `24b4cefe7b3ea66236bb339683e6022e11e8609ee2ba5c3bdfce8241763138b7`)
14. `SP.URB.TOTL.IN.ZS.csv` (677,667 bytes, SHA-256: `78e1b52bb3ebef226d9c8789cc647dfd31b53fba8e6c43dc2c2c0792db87e74c`)

---

### 3. Engineering Quality Controls and Non-Negotiable Compliance

* **Rule 1 (Legitimate Sources):** 100% of data acquired from official WHO and World Bank endpoints.
* **Rule 2 (Real Data Downloaded):** Real files downloaded, parsed, checksummed, and inspected.
* **Rule 3 (No Fabrication):** Zero simulated or synthetic numbers generated.
* **Rule 4 (No Forward-Filling / Interpolation):** Missing values preserved strictly as NaN / NULL.
* **Rule 5 (Distinguish Modeled vs Measured):** Bayesian modeled estimates (MMEIG MMR, UN WPP fertility) explicitly documented and separated from survey observations (SBA, ANC) and national accounts (GDP, health spending).
* **Rule 6 (Preserve Raw Files):** Raw files preserved unmodified in `data/raw/`.
* **Rule 7 (Provenance Documented):** Manifest, inventory, and coverage matrix saved in `data/metadata/`.
* **Rule 8 (Single Estimation Round):** 2025 estimation round used exclusively (superseding 2020 round).
* **Rule 9 (Association vs Causation):** Ecological nature of cross-country data explicitly noted.
* **Rule 10 (Pause at Phase 1):** Work halted at Phase 1 deliverables for collaborative review.
