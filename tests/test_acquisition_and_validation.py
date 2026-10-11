"""
test_acquisition_and_validation.py
==================================
Automated unit and validation tests for Phase 1–5 data acquisition,
cryptographic provenance, analytical panel integrity, and headline statistics.

Author: Dr. Aung Chit Moe (MBBS)
Date: October 2026
"""

import os
import json
import sqlite3
import pytest
import numpy as np
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_MMEIG_ZIP = os.path.join(
    BASE_DIR, "data", "raw", "mmeig", "trends-in-maternal-mortality-2000-to-2023-estimates-data.zip"
)
RAW_WB_META = os.path.join(
    BASE_DIR, "data", "raw", "world_bank", "csv", "wb_countries_metadata.csv"
)


@pytest.mark.skipif(
    not os.path.exists(RAW_MMEIG_ZIP),
    reason="Raw MMEIG archive not downloaded in lightweight clone (run python src/download_mmeig.py)"
)
def test_mmeig_raw_files_and_schema():
    raw_mmeig_dir = os.path.join(BASE_DIR, "data", "raw", "mmeig")
    zip_path = os.path.join(raw_mmeig_dir, "trends-in-maternal-mortality-2000-to-2023-estimates-data.zip")
    pdf_path = os.path.join(raw_mmeig_dir, "9789240108462-eng.pdf")
    estimates_csv = os.path.join(raw_mmeig_dir, "extracted", "Estimate_data_v2", "Estimates", "estimates.csv")

    assert os.path.exists(zip_path), f"MMEIG zip file missing: {zip_path}"
    assert os.path.getsize(zip_path) == 12_411_704, "MMEIG zip file size mismatch"

    assert os.path.exists(pdf_path), f"MMEIG report PDF missing: {pdf_path}"
    assert os.path.getsize(pdf_path) == 4_772_148, "MMEIG PDF file size mismatch"

    assert os.path.exists(estimates_csv), f"Extracted estimates.csv missing: {estimates_csv}"
    df = pd.read_csv(estimates_csv)

    required_cols = ['iso_alpha_3_code', 'year_mid', 'parameter', '0.1', '0.5', '0.9', 'estimate_version']
    for c in required_cols:
        assert c in df.columns, f"Required column {c} missing in estimates.csv"

    assert df['iso_alpha_3_code'].nunique() == 195, "Expected 195 unique countries in MMEIG"
    mmr = df[(df['parameter'] == 'mmr') & (df['year_mid'] >= 2000) & (df['year_mid'] <= 2023)]
    assert len(mmr) == 195 * 24, "Expected exactly 4680 MMR country-year observations"
    assert mmr.duplicated(subset=['iso_alpha_3_code', 'year_mid']).sum() == 0, "Duplicate MMR records detected"
    violations = ((mmr['0.1'] > mmr['0.5']) | (mmr['0.5'] > mmr['0.9'])).sum()
    assert violations == 0, "Uncertainty interval ordering violated (0.1 <= 0.5 <= 0.9)"


@pytest.mark.skipif(
    not os.path.exists(RAW_WB_META),
    reason="Raw World Bank CSVs not downloaded in lightweight clone (run python src/download_world_bank.py)"
)
def test_wb_raw_files_and_country_metadata():
    wb_csv_dir = os.path.join(BASE_DIR, "data", "raw", "world_bank", "csv")
    meta_csv = os.path.join(wb_csv_dir, "wb_countries_metadata.csv")

    assert os.path.exists(meta_csv), "World Bank country metadata CSV missing"
    df_meta = pd.read_csv(meta_csv)
    assert len(df_meta) >= 290, "Expected at least 290 entities in WB metadata"
    assert 'is_aggregate' in df_meta.columns, "Expected is_aggregate column in WB metadata"

    key_indicators = [
        "NY.GDP.PCAP.CD.csv",
        "NY.GDP.PCAP.PP.KD.csv",
        "SH.MED.PHYS.ZS.csv",
        "SH.STA.BRTC.ZS.csv",
        "SP.DYN.TFRT.IN.csv",
        "SP.ADO.TFRT.csv",
        "SP.URB.TOTL.IN.ZS.csv",
    ]
    for ki in key_indicators:
        ki_path = os.path.join(wb_csv_dir, ki)
        assert os.path.exists(ki_path), f"Indicator file missing: {ki_path}"
        df_ind = pd.read_csv(ki_path)
        assert len(df_ind) > 0, f"Indicator file empty: {ki_path}"


def test_phase1_metadata_and_manifest_provenance():
    metadata_dir = os.path.join(BASE_DIR, "data", "metadata")
    manifest_file = os.path.join(metadata_dir, "download_manifest.json")
    inv_file = os.path.join(metadata_dir, "indicator_inventory.csv")
    cov_file = os.path.join(metadata_dir, "country_year_coverage.csv")

    assert os.path.exists(manifest_file), "download_manifest.json missing"
    assert os.path.exists(inv_file), "indicator_inventory.csv missing"
    assert os.path.exists(cov_file), "country_year_coverage.csv missing"

    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    assert len(manifest) >= 10, "Manifest should have at least 10 logged items"
    for item in manifest:
        assert "sha256" in item and len(item["sha256"]) == 64, f"Missing valid SHA-256 hash in {item.get('resource_id')}"

    df_inv = pd.read_csv(inv_file)
    assert len(df_inv) >= 12, "Indicator inventory should have at least 12 indicators"

    df_cov = pd.read_csv(cov_file)
    assert len(df_cov) == 195 * 24, "Coverage matrix should have exactly 4,680 rows (195 countries x 24 years)"


def test_analytical_master_panel_and_headline_metrics():
    proc_dir = os.path.join(BASE_DIR, "data", "processed")
    csv_path = os.path.join(proc_dir, "maternal_mortality_analytical_master.csv")
    parquet_path = os.path.join(proc_dir, "maternal_mortality_analytical_master.parquet")
    db_path = os.path.join(proc_dir, "maternal_mortality.db")

    assert os.path.exists(csv_path), "Master CSV missing"
    assert os.path.exists(parquet_path), "Master Parquet missing"
    assert os.path.exists(db_path), "SQLite database missing"

    df = pd.read_csv(csv_path)
    df_pq = pd.read_parquet(parquet_path)
    assert len(df) == 4680, "Expected 4,680 total country-year rows (195 countries x 24 years)"
    assert len(df_pq) == 4680, "Parquet row count must match CSV (4,680 rows)"
    assert df['country_iso3'].nunique() == 195, "Expected 195 sovereign countries in full grid"

    # Check balanced panel
    bal = df[df['is_balanced_sample'] == 1]
    assert len(bal) == 4248, "Expected 4,248 country-year rows in balanced panel (177 countries x 24 years)"
    assert bal['country_iso3'].nunique() == 177, "Expected 177 countries in balanced core panel"

    # Uncertainty interval ordering
    assert ((df['mmr_low'] <= df['mmr_pt']) & (df['mmr_pt'] <= df['mmr_high'])).all(), "MMR interval ordering violated"

    # Verify global median MMR in 2000 and 2023 (balanced panel)
    med_2000 = bal[bal['year'] == 2000]['mmr_pt'].median()
    med_2023 = bal[bal['year'] == 2023]['mmr_pt'].median()
    assert round(med_2000, 2) == 67.64, f"Expected 2000 median MMR 67.64, got {med_2000:.2f}"
    assert round(med_2023, 2) == 42.11, f"Expected 2023 median MMR 42.11, got {med_2023:.2f}"

    # Verify 2023 balanced-panel income group statistics
    bal_2023 = bal[bal['year'] == 2023]
    hi = bal_2023[bal_2023['income_level_name'] == 'High income']
    li = bal_2023[bal_2023['income_level_name'] == 'Low income']
    assert len(hi) == 62, f"Expected 62 High-Income countries in balanced panel, got {len(hi)}"
    assert len(li) == 18, f"Expected 18 Low-Income countries in balanced panel, got {len(li)}"
    assert round(hi['mmr_pt'].mean(), 1) == 19.5, f"Expected HI mean MMR 19.5, got {hi['mmr_pt'].mean():.1f}"
    assert round(li['mmr_pt'].mean(), 1) == 370.1, f"Expected LI mean MMR 370.1, got {li['mmr_pt'].mean():.1f}"
    assert round(hi['mmr_pt'].median(), 1) == 7.7, f"Expected HI median MMR 7.7, got {hi['mmr_pt'].median():.1f}"
    assert round(li['mmr_pt'].median(), 1) == 354.0, f"Expected LI median MMR 354.0, got {li['mmr_pt'].median():.1f}"

    # Verify SQLite database matches
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM analytical_master;")
    assert cur.fetchone()[0] == 4680
    cur.execute("SELECT COUNT(*) FROM analytical_master WHERE is_balanced_sample = 1;")
    assert cur.fetchone()[0] == 4248
    conn.close()


def test_dashboard_offline_bundle_and_links():
    dash_html = os.path.join(BASE_DIR, "dashboard", "index.html")
    chart_js = os.path.join(BASE_DIR, "dashboard", "chart.umd.min.js")
    readme_md = os.path.join(BASE_DIR, "README.md")

    assert os.path.exists(dash_html), "dashboard/index.html missing"
    assert os.path.exists(chart_js), "Vendored dashboard/chart.umd.min.js missing"
    assert os.path.getsize(chart_js) > 150_000, "chart.umd.min.js unexpectedly small"

    with open(dash_html, "r", encoding="utf-8") as f:
        html_content = f.read()
    assert 'src="chart.umd.min.js"' in html_content, "Dashboard must reference local chart.umd.min.js"
    assert "cdn.jsdelivr.net" not in html_content, "Dashboard must not depend on external CDN scripts"

    with open(readme_md, "r", encoding="utf-8") as f:
        readme_content = f.read()
    assert "file:///" not in readme_content, "README.md must not contain local file:/// links"
