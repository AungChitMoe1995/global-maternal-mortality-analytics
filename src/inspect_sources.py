"""
inspect_sources.py
==================
Deep verification and profiling module for MMEIG and World Bank datasets.
Performs data quality checks, schema inspection, coverage matrix generation,
and indicator inventory generation for Phase 1 of the Maternal Mortality Research Project.

Author: Collaborative Research Team
Date: October 2026
"""

import os
import sys
import json
import glob
import pandas as pd
import numpy as np

def run_inspection(base_dir: str):
    print("=" * 70)
    print("PHASE 1: SOURCE INSPECTION, DATA VERIFICATION & QUALITY AUDIT")
    print("=" * 70)
    
    metadata_dir = os.path.join(base_dir, "data", "metadata")
    os.makedirs(metadata_dir, exist_ok=True)
    
    # -------------------------------------------------------------
    # 1. World Bank Country Metadata Audit
    # -------------------------------------------------------------
    wb_country_meta_file = os.path.join(base_dir, "data", "raw", "world_bank", "csv", "wb_countries_metadata.csv")
    if os.path.exists(wb_country_meta_file):
        df_wb_countries = pd.read_csv(wb_country_meta_file)
        wb_genuine_countries = df_wb_countries[df_wb_countries["is_aggregate"] == 0]
        wb_aggregates = df_wb_countries[df_wb_countries["is_aggregate"] == 1]
        print(f"[WB ENTITIES] Total: {len(df_wb_countries)} | Genuine Countries: {len(wb_genuine_countries)} | Aggregates: {len(wb_aggregates)}")
    else:
        print("[WARNING] World Bank country metadata file not found.")
        df_wb_countries = pd.DataFrame()
        wb_genuine_countries = pd.DataFrame()
        wb_aggregates = pd.DataFrame()

    # -------------------------------------------------------------
    # 2. MMEIG Country Estimates Audit
    # -------------------------------------------------------------
    mmeig_estimates_file = os.path.join(base_dir, "data", "raw", "mmeig", "extracted", "Estimate_data_v2", "Estimates", "estimates.csv")
    if not os.path.exists(mmeig_estimates_file):
        print(f"[ERROR] MMEIG estimates file not found at {mmeig_estimates_file}")
        return
        
    df_mmeig = pd.read_csv(mmeig_estimates_file)
    print(f"\n[MMEIG ESTIMATES.CSV]")
    print(f"  Shape: {df_mmeig.shape}")
    print(f"  Columns: {df_mmeig.columns.tolist()}")
    print(f"  Total Rows: {len(df_mmeig):,}")
    print(f"  Years available: {df_mmeig['year_mid'].min()} to {df_mmeig['year_mid'].max()} (Total years: {df_mmeig['year_mid'].nunique()})")
    
    mmeig_countries = sorted(df_mmeig["iso_alpha_3_code"].unique().tolist())
    print(f"  Unique ISO-3 country entities: {len(mmeig_countries)}")
    
    # Check parameters
    param_counts = df_mmeig["parameter"].value_counts().to_dict()
    print("  Parameters in MMEIG:")
    for p, c in param_counts.items():
        print(f"    - {p}: {c:,} records")
        
    # Restrict to primary research window: 2000-2023
    df_mmeig_study = df_mmeig[(df_mmeig["year_mid"] >= 2000) & (df_mmeig["year_mid"] <= 2023)]
    print(f"\n  [MMEIG Study Window 2000-2023]")
    print(f"    Rows: {len(df_mmeig_study):,}")
    print(f"    Years: {df_mmeig_study['year_mid'].nunique()} (2000-2023 = 24 years)")
    print(f"    Expected MMR country-years: {len(mmeig_countries)} * 24 = {len(mmeig_countries) * 24}")
    
    mmr_sub = df_mmeig_study[df_mmeig_study["parameter"] == "mmr"]
    print(f"    Actual MMR records: {len(mmr_sub)}")
    
    # Check duplicates
    dups = mmr_sub.duplicated(subset=["iso_alpha_3_code", "year_mid"]).sum()
    print(f"    Duplicate (country, year) records in MMR: {dups}")
    
    # Check nulls in point estimate and uncertainty bounds
    null_pt = mmr_sub["0.5"].isnull().sum()
    null_low = mmr_sub["0.1"].isnull().sum()
    null_high = mmr_sub["0.9"].isnull().sum()
    print(f"    Nulls in MMR (pt estimate 0.5): {null_pt}")
    print(f"    Nulls in MMR (lower 80% UI 0.1): {null_low}")
    print(f"    Nulls in MMR (upper 80% UI 0.9): {null_high}")
    
    # Consistency check: 0.1 <= 0.5 <= 0.9
    ui_inconsistent = (mmr_sub["0.1"] > mmr_sub["0.5"]) | (mmr_sub["0.5"] > mmr_sub["0.9"])
    print(f"    UI order violations (low > pt or pt > high): {ui_inconsistent.sum()}")
    
    # Range of MMR
    print(f"    MMR median (0.5) range: min={mmr_sub['0.5'].min():.1f}, median={mmr_sub['0.5'].median():.1f}, max={mmr_sub['0.5'].max():.1f}")
    
    # -------------------------------------------------------------
    # 3. World Bank Indicators Audit
    # -------------------------------------------------------------
    wb_csv_dir = os.path.join(base_dir, "data", "raw", "world_bank", "csv")
    wb_csv_files = glob.glob(os.path.join(wb_csv_dir, "*.csv"))
    
    print("\n" + "=" * 70)
    print("WORLD BANK INDICATORS AUDIT (2000-2023)")
    print("=" * 70)
    
    indicator_summary_records = []
    wb_data_dict = {}
    
    # Also include MMEIG indicators in inventory
    mmeig_meta_entries = [
        {
            "indicator_code": "MMEIG.MMR",
            "indicator_name": "Maternal mortality ratio (modeled estimate, per 100,000 live births)",
            "research_domain": "Primary Outcome: Maternal Mortality",
            "source_organization": "WHO, UNICEF, UNFPA, World Bank Group, UNDESA (MMEIG 2025 round)",
            "data_type": "Modeled Bayesian estimate (BMat / BMis) with 80% UI",
            "unit": "Deaths per 100,000 live births",
            "periodicity": "Annual (2000-2023 available; 1985-2023 in raw)",
            "total_mmeig_countries": len(mmeig_countries),
            "study_period_expected_obs": len(mmeig_countries) * 24,
            "study_period_valid_obs": len(mmr_sub),
            "study_period_missing_pct": round((1 - len(mmr_sub) / (len(mmeig_countries) * 24)) * 100, 2),
            "year_2023_valid_obs": len(mmr_sub[mmr_sub["year_mid"] == 2023]),
            "year_2023_missing_pct": round((1 - len(mmr_sub[mmr_sub["year_mid"] == 2023]) / len(mmeig_countries)) * 100, 2),
            "countries_with_complete_series": len(mmr_sub.groupby("iso_alpha_3_code").filter(lambda g: len(g) == 24)["iso_alpha_3_code"].unique()),
            "min_val": round(mmr_sub["0.5"].min(), 1),
            "median_val": round(mmr_sub["0.5"].median(), 1),
            "max_val": round(mmr_sub["0.5"].max(), 1),
            "notes": "Point estimate is median (0.5); 80% uncertainty interval provided (0.1 and 0.9 percentiles)."
        },
        {
            "indicator_code": "MMEIG.MATDEATHS",
            "indicator_name": "Estimated number of maternal deaths",
            "research_domain": "Maternal Mortality Burden",
            "source_organization": "WHO/UN MMEIG 2025 round",
            "data_type": "Modeled estimate with 80% UI",
            "unit": "Absolute number of deaths",
            "periodicity": "Annual (2000-2023)",
            "total_mmeig_countries": len(mmeig_countries),
            "study_period_expected_obs": len(mmeig_countries) * 24,
            "study_period_valid_obs": len(df_mmeig_study[df_mmeig_study["parameter"] == "maternal_deaths"]),
            "study_period_missing_pct": round((1 - len(df_mmeig_study[df_mmeig_study["parameter"] == "maternal_deaths"]) / (len(mmeig_countries) * 24)) * 100, 2),
            "year_2023_valid_obs": len(df_mmeig_study[(df_mmeig_study["parameter"] == "maternal_deaths") & (df_mmeig_study["year_mid"] == 2023)]),
            "year_2023_missing_pct": round((1 - len(df_mmeig_study[(df_mmeig_study["parameter"] == "maternal_deaths") & (df_mmeig_study["year_mid"] == 2023)]) / len(mmeig_countries)) * 100, 2),
            "countries_with_complete_series": len(df_mmeig_study[df_mmeig_study["parameter"] == "maternal_deaths"].groupby("iso_alpha_3_code").filter(lambda g: len(g) == 24)["iso_alpha_3_code"].unique()),
            "min_val": round(df_mmeig_study[df_mmeig_study["parameter"] == "maternal_deaths"]["0.5"].min(), 1),
            "median_val": round(df_mmeig_study[df_mmeig_study["parameter"] == "maternal_deaths"]["0.5"].median(), 1),
            "max_val": round(df_mmeig_study[df_mmeig_study["parameter"] == "maternal_deaths"]["0.5"].max(), 1),
            "notes": "Calculated from PM, all-cause female deaths, and live births."
        },
        {
            "indicator_code": "MMEIG.LIFETIMERISK_1_IN",
            "indicator_name": "Adult lifetime risk of maternal death (1 in N)",
            "research_domain": "Maternal Mortality Lifetime Burden",
            "source_organization": "WHO/UN MMEIG 2025 round",
            "data_type": "Modeled probability conversion",
            "unit": "1 in N women aged 15",
            "periodicity": "Annual (2000-2023)",
            "total_mmeig_countries": len(mmeig_countries),
            "study_period_expected_obs": len(mmeig_countries) * 24,
            "study_period_valid_obs": len(df_mmeig_study[df_mmeig_study["parameter"] == "lifetime_risk_1_in"]),
            "study_period_missing_pct": round((1 - len(df_mmeig_study[df_mmeig_study["parameter"] == "lifetime_risk_1_in"]) / (len(mmeig_countries) * 24)) * 100, 2),
            "year_2023_valid_obs": len(df_mmeig_study[(df_mmeig_study["parameter"] == "lifetime_risk_1_in") & (df_mmeig_study["year_mid"] == 2023)]),
            "year_2023_missing_pct": round((1 - len(df_mmeig_study[(df_mmeig_study["parameter"] == "lifetime_risk_1_in") & (df_mmeig_study["year_mid"] == 2023)]) / len(mmeig_countries)) * 100, 2),
            "countries_with_complete_series": len(df_mmeig_study[df_mmeig_study["parameter"] == "lifetime_risk_1_in"].groupby("iso_alpha_3_code").filter(lambda g: len(g) == 24)["iso_alpha_3_code"].unique()),
            "min_val": round(df_mmeig_study[df_mmeig_study["parameter"] == "lifetime_risk_1_in"]["0.5"].min(), 1),
            "median_val": round(df_mmeig_study[df_mmeig_study["parameter"] == "lifetime_risk_1_in"]["0.5"].median(), 1),
            "max_val": round(df_mmeig_study[df_mmeig_study["parameter"] == "lifetime_risk_1_in"]["0.5"].max(), 1),
            "notes": "Cumulative risk that a 15-year-old girl will die of maternal cause taking into account competing mortality."
        }
    ]
    for m in mmeig_meta_entries:
        indicator_summary_records.append(m)

    # Process each World Bank CSV
    for csv_file in sorted(wb_csv_files):
        fname = os.path.basename(csv_file)
        if fname == "wb_countries_metadata.csv":
            continue
            
        code = fname.replace(".csv", "")
        df_wb = pd.read_csv(csv_file)
        
        # Load metadata JSON if exists
        meta_json_file = os.path.join(base_dir, "data", "raw", "world_bank", "json", f"{code}_metadata.json")
        ind_name = code
        source_org = "World Bank"
        source_note = ""
        periodicity = "Annual"
        if os.path.exists(meta_json_file):
            try:
                with open(meta_json_file, "r", encoding="utf-8") as f:
                    mj = json.load(f)
                    if len(mj) > 1 and len(mj[1]) > 0:
                        ind_info = mj[1][0]
                        ind_name = ind_info.get("name", code)
                        source_org = ind_info.get("sourceOrganization", "World Bank")
                        source_note = ind_info.get("sourceNote", "")
            except Exception:
                pass
                
        # Separate country records from aggregates
        # Using country_iso3 and wb_genuine_countries or checking if ISO3 is in mmeig_countries
        df_wb_mmeig_countries = df_wb[df_wb["country_iso3"].isin(mmeig_countries)].copy()
        
        # Check duplicates
        dups = df_wb_mmeig_countries.duplicated(subset=["country_iso3", "year"]).sum()
        
        # Valid observations in study window 2000-2023
        valid_obs = df_wb_mmeig_countries[df_wb_mmeig_countries["value"].notnull()]
        n_valid = len(valid_obs)
        expected_total = len(mmeig_countries) * 24
        missing_pct = round((1 - n_valid / expected_total) * 100, 2)
        
        # Year 2023 specifically
        y2023 = df_wb_mmeig_countries[df_wb_mmeig_countries["year"] == 2023]
        n_2023_valid = y2023["value"].notnull().sum()
        missing_2023_pct = round((1 - n_2023_valid / len(mmeig_countries)) * 100, 2)
        
        # Series completeness per country
        obs_per_country = valid_obs.groupby("country_iso3")["year"].count()
        complete_series = (obs_per_country == 24).sum()
        ge_1_obs = len(obs_per_country)
        
        # Value statistics
        min_v = round(valid_obs["value"].min(), 2) if n_valid > 0 else np.nan
        med_v = round(valid_obs["value"].median(), 2) if n_valid > 0 else np.nan
        max_v = round(valid_obs["value"].max(), 2) if n_valid > 0 else np.nan
        
        # Store in dict for coverage matrix
        wb_data_dict[code] = df_wb_mmeig_countries.set_index(["country_iso3", "year"])["value"]
        
        print(f"\n[{code}] {ind_name}")
        print(f"  Valid country-years (out of {expected_total}): {n_valid:,} ({100 - missing_pct:.1f}% coverage, {missing_pct:.1f}% missing)")
        print(f"  Year 2023 coverage: {n_2023_valid} / {len(mmeig_countries)} ({100 - missing_2023_pct:.1f}% coverage, {missing_2023_pct:.1f}% missing)")
        print(f"  Countries with >= 1 observation: {ge_1_obs} / {len(mmeig_countries)}")
        print(f"  Countries with complete 24/24 series: {complete_series} / {len(mmeig_countries)}")
        print(f"  Values: min={min_v}, median={med_v}, max={max_v}")
        print(f"  Duplicates: {dups}")
        
        # Classify data collection type
        data_type = "Direct/Administrative"
        if "LITR" in code or "BRTC" in code or "ANVC" in code:
            data_type = "Survey-based / Administrative (intermittent)"
        elif "TFRT" in code or "ADO" in code or "URB" in code:
            data_type = "UN Population Division modeled/projected time series"
        elif "PHYS" in code or "NUMW" in code:
            data_type = "WHO registry / National workforce reports (sparse)"
        elif "GDP" in code or "CHEX" in code:
            data_type = "National Accounts / WHO Global Health Expenditure Database"

        indicator_summary_records.append({
            "indicator_code": code,
            "indicator_name": ind_name,
            "research_domain": "Healthcare Access / Socioeconomic",
            "source_organization": source_org,
            "data_type": data_type,
            "unit": df_wb["unit"].dropna().iloc[0] if (df_wb["unit"].notnull().any() and df_wb["unit"].dropna().iloc[0] != "") else "Standard",
            "periodicity": periodicity,
            "total_mmeig_countries": len(mmeig_countries),
            "study_period_expected_obs": expected_total,
            "study_period_valid_obs": n_valid,
            "study_period_missing_pct": missing_pct,
            "year_2023_valid_obs": int(n_2023_valid),
            "year_2023_missing_pct": missing_2023_pct,
            "countries_with_complete_series": int(complete_series),
            "min_val": min_v,
            "median_val": med_v,
            "max_val": max_v,
            "notes": (source_note[:150] + "...") if len(source_note) > 150 else source_note
        })

    # Save Indicator Inventory CSV
    df_inv = pd.DataFrame(indicator_summary_records)
    inv_path = os.path.join(metadata_dir, "indicator_inventory.csv")
    df_inv.to_csv(inv_path, index=False)
    print(f"\n[SAVED] Indicator Inventory saved to {inv_path} ({len(df_inv)} indicators).")
    
    # -------------------------------------------------------------
    # 4. Build Country-Year Coverage Matrix (2000-2023)
    # -------------------------------------------------------------
    print("\n" + "=" * 70)
    print("BUILDING COUNTRY-YEAR COVERAGE MATRIX (195 Countries x 24 Years = 4,680 Grid Cells)")
    print("=" * 70)
    
    years = list(range(2000, 2024))
    index_tuples = [(c, y) for c in mmeig_countries for y in years]
    idx = pd.MultiIndex.from_tuples(index_tuples, names=["country_iso3", "year"])
    
    df_coverage = pd.DataFrame(index=idx)
    
    # Add MMR presence
    mmr_indexed = mmr_sub.set_index(["iso_alpha_3_code", "year_mid"])["0.5"]
    df_coverage["MMR_observed"] = mmr_indexed.notnull().astype(int)
    
    # Add World Bank indicators presence (1 if observed, 0 if missing)
    for code, series in wb_data_dict.items():
        col_name = f"{code}_observed"
        df_coverage[col_name] = series.reindex(idx).notnull().astype(int)
        
    df_coverage_reset = df_coverage.reset_index()
    cov_path = os.path.join(metadata_dir, "country_year_coverage.csv")
    df_coverage_reset.to_csv(cov_path, index=False)
    print(f"[SAVED] Country-Year Coverage Matrix saved to {cov_path} ({len(df_coverage_reset)} rows).")
    
    print("\nInspection complete.")

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    run_inspection(base_dir)
