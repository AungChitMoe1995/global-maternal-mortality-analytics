# Raw Data Directory (`data/raw/`)

To keep the repository lightweight (~12 MB instead of 151 MB) and prevent committing 106 MB of extracted upstream archive artifacts, the raw downloaded archives and API extracts under `data/raw/mmeig/` and `data/raw/world_bank/` are excluded via `.gitignore`.

All cleaned and integrated analytical datasets (`data/processed/maternal_mortality_analytical_master.csv`, `.parquet`, and `maternal_mortality.db`) and full cryptographic provenance (`data/metadata/download_manifest.json`) are committed directly in the repository so you can run all statistical analyses, tests, notebooks, and visualizations immediately after cloning.

---

## Reproducing Raw Downloads from Official Sources

To download the exact raw files from the WHO/UN MMEIG CDN and World Bank WDI REST API v2 and verify their SHA-256 hashes against [`data/metadata/download_manifest.json`](../metadata/download_manifest.json):

```bash
# 1. Download & extract WHO/UN MMEIG 2025 Revision archive and report PDF
python src/download_mmeig.py

# 2. Download World Bank WDI indicators (2000–2023) and country classification metadata
python src/download_world_bank.py

# 3. Verify cryptographic hashes, coverage matrices, and raw schema
python src/inspect_sources.py
pytest tests/ -v
```

---

## Primary Upstream Files & SHA-256 Checksums

| Resource ID | Local Path | Size (Bytes) | SHA-256 Checksum |
| :--- | :--- | :---: | :--- |
| `MMEIG_2025_ESTIMATES_ZIP` | `data/raw/mmeig/trends-in-maternal-mortality-2000-to-2023-estimates-data.zip` | `12,411,704` | `c8b60a75cbcb64f7bc7c05d2dea725d885d3915b052307cd588c3fbf766b9227` |
| `MMEIG_2025_REPORT_PDF` | `data/raw/mmeig/9789240108462-eng.pdf` | `4,772,148` | `e2e6773eb78614e99707a9d658a54317d4fa122492318f5bb7e76cfd42dc7869` |
| `WB_COUNTRY_METADATA` | `data/raw/world_bank/csv/wb_countries_metadata.csv` | `26,501` | `0e54f9d231b2eb8b9eb5a268cedf207febccea71869d488777c2c47a086d7548` |

See [`data/metadata/download_manifest.json`](../metadata/download_manifest.json) for the complete manifest of all 18 raw resources and their SHA-256 digests.
