"""
integrate_data.py
=================
Data integration and feature engineering pipeline for the Maternal Mortality
Community Research Project (2000–2023).

Transforms verified raw MMEIG and World Bank datasets into:
1. Processed CSV: data/processed/maternal_mortality_analytical_master.csv
2. Parquet format: data/processed/maternal_mortality_analytical_master.parquet
3. Relational SQLite database: data/processed/maternal_mortality.db

Author: Collaborative Research Team
Date: October 2026
License: Open Data / Research Use
"""

import os
import sys
import sqlite3
import numpy as np
import pandas as pd

def build_analytical_master(base_dir: str):
    print("=" * 70)
    print("PHASE 3A: DATA INTEGRATION & ANALYTICAL DATASET CREATION")
    print("=" * 70)
    
    raw_mmeig_dir = os.path.join(base_dir, "data", "raw", "mmeig", "extracted", "Estimate_data_v2")
    raw_wb_dir = os.path.join(base_dir, "data", "raw", "world_bank", "csv")
    processed_dir = os.path.join(base_dir, "data", "processed")
    os.makedirs(processed_dir, exist_ok=True)
    
    # ---------------------------------------------------------
    # 1. Load and Harmonize MMEIG Primary Estimates
    # ---------------------------------------------------------
    mmeig_file = os.path.join(raw_mmeig_dir, "Estimates", "estimates.csv")
    print(f"[1/5] Loading MMEIG estimates from {mmeig_file}...")
    df_mmeig = pd.read_csv(mmeig_file)
    df_mmeig = df_mmeig[(df_mmeig["year_mid"] >= 2000) & (df_mmeig["year_mid"] <= 2023)].copy()
    
    # Extract core parameters
    piv_mmr = df_mmeig[df_mmeig["parameter"] == "mmr"].rename(columns={
        "iso_alpha_3_code": "country_iso3", "year_mid": "year",
        "0.1": "mmr_low", "0.5": "mmr_pt", "0.9": "mmr_high"
    })[["country_iso3", "year", "mmr_low", "mmr_pt", "mmr_high"]]
    
    piv_deaths = df_mmeig[df_mmeig["parameter"] == "maternal_deaths"].rename(columns={
        "iso_alpha_3_code": "country_iso3", "year_mid": "year",
        "0.5": "maternal_deaths"
    })[["country_iso3", "year", "maternal_deaths"]]
    
    piv_births = df_mmeig[df_mmeig["parameter"] == "births"].rename(columns={
        "iso_alpha_3_code": "country_iso3", "year_mid": "year",
        "0.5": "live_births"
    })[["country_iso3", "year", "live_births"]]
    
    piv_risk = df_mmeig[df_mmeig["parameter"] == "lifetime_risk_1_in"].rename(columns={
        "iso_alpha_3_code": "country_iso3", "year_mid": "year",
        "0.5": "lifetime_risk_1_in"
    })[["country_iso3", "year", "lifetime_risk_1_in"]]
    
    # Merge MMEIG fields
    df_mmeig_merged = piv_mmr.merge(piv_deaths, on=["country_iso3", "year"], how="left")
    df_mmeig_merged = df_mmeig_merged.merge(piv_births, on=["country_iso3", "year"], how="left")
    df_mmeig_merged = df_mmeig_merged.merge(piv_risk, on=["country_iso3", "year"], how="left")
    print(f"      MMEIG harmonized: {len(df_mmeig_merged)} country-year records ({df_mmeig_merged['country_iso3'].nunique()} countries).")
    
    # Also load MMEIG internal modeled SAB
    sab_excel = os.path.join(raw_mmeig_dir, "Other inputs", "estimates_base_0all_indicators_v2_sab_shared.xlsx")
    if os.path.exists(sab_excel):
        print(f"      Loading MMEIG internal modeled SAB from {sab_excel}...")
        df_sab = pd.read_excel(sab_excel)
        df_sab_sub = df_sab[(df_sab["year"] >= 2000) & (df_sab["year"] <= 2023)].rename(columns={
            "iso_alpha_3_code": "country_iso3",
            "X0.5": "sab_modeled_share"
        })[["country_iso3", "year", "sab_modeled_share"]]
        df_sab_sub["sab_modeled_pct"] = df_sab_sub["sab_modeled_share"] * 100.0
        df_mmeig_merged = df_mmeig_merged.merge(df_sab_sub[["country_iso3", "year", "sab_modeled_pct"]], on=["country_iso3", "year"], how="left")
    
    # ---------------------------------------------------------
    # 2. Load World Bank Country Metadata (Entities)
    # ---------------------------------------------------------
    wb_meta_file = os.path.join(raw_wb_dir, "wb_countries_metadata.csv")
    print(f"[2/5] Loading country classifications from {wb_meta_file}...")
    df_wb_meta = pd.read_csv(wb_meta_file)
    
    # Exclude regional/economic aggregates
    df_countries = df_wb_meta[df_wb_meta["is_aggregate"] == 0].rename(columns={
        "country_id": "country_iso3"
    })[["country_iso3", "iso2_code", "country_name", "region_name", "income_level_name"]]
    
    # ---------------------------------------------------------
    # 3. Load World Bank Study Indicators
    # ---------------------------------------------------------
    print("[3/5] Loading World Bank indicators...")
    indicators_map = {
        "NY.GDP.PCAP.PP.KD.csv": "gdp_pcap_ppp",
        "NY.GDP.PCAP.CD.csv": "gdp_pcap_curr",
        "SH.XPD.CHEX.GD.ZS.csv": "chex_gdp_pct",
        "SH.XPD.CHEX.PC.CD.csv": "chex_pcap_curr",
        "SP.DYN.TFRT.IN.csv": "tfr",
        "SP.ADO.TFRT.csv": "ado_fert_rate",
        "SP.URB.TOTL.IN.ZS.csv": "urban_pct",
        "SE.SEC.ENRR.FE.csv": "female_sec_enroll_pct",
        "SH.MED.PHYS.ZS.csv": "physicians_per_1k",
        "SH.MED.NUMW.P3.csv": "nurses_midwives_per_1k",
        "SH.STA.BRTC.ZS.csv": "wdi_sba_pct"
    }
    
    wb_indicator_dfs = {}
    for fname, colname in indicators_map.items():
        fpath = os.path.join(raw_wb_dir, fname)
        if os.path.exists(fpath):
            df_ind = pd.read_csv(fpath)
            sub = df_ind[(df_ind["year"] >= 2000) & (df_ind["year"] <= 2023)].rename(columns={
                "country_iso3": "country_iso3",
                "value": colname
            })[["country_iso3", "year", colname]]
            wb_indicator_dfs[colname] = sub
        else:
            print(f"      [WARNING] Indicator file missing: {fname}")
            
    # ---------------------------------------------------------
    # 4. Integrate into Master Analytical DataFrame
    # ---------------------------------------------------------
    print("[4/5] Merging primary outcome and explanatory variables...")
    # Base is MMEIG merged (195 countries x 24 years = 4,680)
    master = df_mmeig_merged.merge(df_countries, on="country_iso3", how="left")
    
    # Join WB indicators
    for colname, df_sub in wb_indicator_dfs.items():
        master = master.merge(df_sub, on=["country_iso3", "year"], how="left")
        
    # Standardize country name for entities not in WB (e.g. Cook Islands COK)
    master.loc[master["country_iso3"] == "COK", "country_name"] = "Cook Islands"
    master.loc[master["country_iso3"] == "COK", "region_name"] = "East Asia & Pacific"
    master.loc[master["country_iso3"] == "COK", "income_level_name"] = "High income"
    
    # ---------------------------------------------------------
    # 5. Feature Engineering & Transformations
    # ---------------------------------------------------------
    print("[5/5] Performing feature transformations & sample flagging...")
    
    # Natural Log Transformations (with robust handling of strictly positive numbers)
    master["log_mmr_pt"] = np.log(master["mmr_pt"])
    master["log_mmr_low"] = np.log(master["mmr_low"])
    master["log_mmr_high"] = np.log(master["mmr_high"])
    
    master["log_gdp_pcap_ppp"] = np.log(master["gdp_pcap_ppp"])
    master["log_gdp_pcap_curr"] = np.log(master["gdp_pcap_curr"])
    master["log_chex_pcap_curr"] = np.log(master["chex_pcap_curr"])
    
    # Decade / Epoch Era Indicators
    # MDG: 2000-2015, SDG: 2016-2023, COVID: 2020-2023
    master["is_mdg_era"] = (master["year"] <= 2015).astype(int)
    master["is_sdg_era"] = (master["year"] >= 2016).astype(int)
    master["is_covid_era"] = (master["year"] >= 2020).astype(int)
    
    # Balanced Panel Identifier for Solution 1 Core Variables
    # Core variables: log_mmr_pt, log_gdp_pcap_ppp, chex_gdp_pct, tfr, ado_fert_rate, urban_pct
    core_cols = ["log_mmr_pt", "log_gdp_pcap_ppp", "chex_gdp_pct", "tfr", "ado_fert_rate", "urban_pct"]
    master["has_all_core_vars"] = master[core_cols].notnull().all(axis=1).astype(int)
    
    # Identify countries with complete 24/24 series for all core variables
    complete_countries = master.groupby("country_iso3")["has_all_core_vars"].sum()
    balanced_countries = complete_countries[complete_countries == 24].index.tolist()
    
    master["is_balanced_sample"] = master["country_iso3"].isin(balanced_countries).astype(int)
    
    print(f"\n[SUMMARY OF ANALYTICAL MASTER]")
    print(f"  Total Observations: {len(master):,} rows across {master['country_iso3'].nunique()} countries and {master['year'].nunique()} years (2000-2023).")
    print(f"  Balanced Panel Countries (100% complete): {len(balanced_countries)} countries ({len(balanced_countries) * 24:,} observations).")
    print(f"  Unbalanced Usable Observations: {master['has_all_core_vars'].sum():,} observations.")
    
    # Sort logically
    master = master.sort_values(["country_iso3", "year"]).reset_index(drop=True)
    
    # ---------------------------------------------------------
    # 6. Save Formats (CSV, Parquet, SQLite)
    # ---------------------------------------------------------
    csv_out = os.path.join(processed_dir, "maternal_mortality_analytical_master.csv")
    parquet_out = os.path.join(processed_dir, "maternal_mortality_analytical_master.parquet")
    db_out = os.path.join(processed_dir, "maternal_mortality.db")
    
    master.to_csv(csv_out, index=False)
    print(f"  [SAVED] CSV analytical dataset: {csv_out} ({os.path.getsize(csv_out):,} bytes)")
    
    master.to_parquet(parquet_out, index=False)
    print(f"  [SAVED] Parquet dataset: {parquet_out} ({os.path.getsize(parquet_out):,} bytes)")
    
    # SQLite Database Export
    conn = sqlite3.connect(db_out)
    master.to_sql("analytical_master", conn, if_exists="replace", index=False)
    
    # Save standalone normalized tables in SQLite
    df_countries.to_sql("dim_countries", conn, if_exists="replace", index=False)
    df_mmeig_merged.to_sql("fact_mmeig_estimates", conn, if_exists="replace", index=False)
    
    conn.commit()
    conn.close()
    print(f"  [SAVED] SQLite database: {db_out} ({os.path.getsize(db_out):,} bytes)")
    
    return master

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    build_analytical_master(base_dir)
