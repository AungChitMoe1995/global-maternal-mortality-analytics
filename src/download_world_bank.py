"""
download_world_bank.py
======================
Acquisition module for World Bank World Development Indicators (WDI) API
for the Maternal Mortality Community Research Project (2000-2023).

Queries both metadata and time-series data for candidate indicators,
saves raw API responses (JSON and CSV), tracks provenance, and updates
the download manifest.

Author: Collaborative Research Team
Date: October 2026
License: Open Data / CC BY 4.0
"""

import os
import sys
import json
import time
import hashlib
import datetime
import requests
import pandas as pd

BASE_URL = "https://api.worldbank.org/v2"
USER_AGENT = "MMR-Research-Project/1.0 (Public Health Community Study; Contact: researcher@local)"

# Candidate Indicators to acquire
INDICATORS = {
    # 8 Initial Candidate Indicators
    "SH.MED.PHYS.ZS": {
        "domain": "Healthcare workforce",
        "description": "Physicians per 1,000 population"
    },
    "SE.ADT.LITR.FE.ZS": {
        "domain": "Female education",
        "description": "Literacy rate, adult female (%)"
    },
    "SH.STA.BRTC.ZS": {
        "domain": "Maternal healthcare access",
        "description": "Births attended by skilled health staff (%)"
    },
    "NY.GDP.PCAP.CD": {
        "domain": "Economic development",
        "description": "GDP per capita, current US$"
    },
    "SH.XPD.CHEX.PC.CD": {
        "domain": "Health financing",
        "description": "Current health expenditure per capita, current US$"
    },
    "SP.DYN.TFRT.IN": {
        "domain": "Fertility",
        "description": "Total fertility rate (births per woman)"
    },
    "SP.ADO.TFRT": {
        "domain": "Adolescent fertility",
        "description": "Adolescent fertility rate (births per 1,000 women ages 15-19)"
    },
    "SP.URB.TOTL.IN.ZS": {
        "domain": "Urbanization",
        "description": "Urban population (% of total)"
    },
    # Complementary & Methodological Indicators
    "NY.GDP.PCAP.PP.KD": {
        "domain": "Economic development (Constant PPP)",
        "description": "GDP per capita, PPP (constant 2021 international $)"
    },
    "SH.XPD.CHEX.GD.ZS": {
        "domain": "Health financing (% GDP)",
        "description": "Current health expenditure (% of GDP)"
    },
    "SH.MED.NUMW.P3": {
        "domain": "Healthcare workforce",
        "description": "Nurses and midwives per 1,000 population"
    },
    "SH.STA.ANVC.ZS": {
        "domain": "Maternal healthcare access",
        "description": "Pregnant women receiving prenatal care (at least 4 visits, %)"
    },
    "SE.SEC.ENRR.FE": {
        "domain": "Female education (Enrollment)",
        "description": "School enrollment, secondary, female (% gross)"
    }
}

def calculate_sha256(filepath: str) -> str:
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def update_manifest(entry: dict, manifest_path: str):
    os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
    manifest = []
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)
        except Exception:
            manifest = []
    
    updated = False
    for i, item in enumerate(manifest):
        if item.get("resource_id") == entry.get("resource_id"):
            manifest[i] = entry
            updated = True
            break
    if not updated:
        manifest.append(entry)
        
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

def fetch_json_with_retry(url: str, retries: int = 3, timeout: int = 30):
    headers = {"User-Agent": USER_AGENT}
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, headers=headers, timeout=timeout)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            if attempt == retries:
                raise e
            time.sleep(2 * attempt)

def download_country_metadata(raw_dir: str, manifest_path: str):
    url = f"{BASE_URL}/country?format=json&per_page=500"
    print(f"\n[COUNTRY METADATA] Fetching from {url}...")
    dest_json = os.path.join(raw_dir, "json", "wb_countries_metadata.json")
    dest_csv = os.path.join(raw_dir, "csv", "wb_countries_metadata.csv")
    os.makedirs(os.path.dirname(dest_json), exist_ok=True)
    os.makedirs(os.path.dirname(dest_csv), exist_ok=True)
    
    try:
        data = fetch_json_with_retry(url)
        with open(dest_json, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            
        countries_list = data[1]
        records = []
        for c in countries_list:
            records.append({
                "country_id": c.get("id"),
                "iso2_code": c.get("iso2Code"),
                "country_name": c.get("name"),
                "region_id": c.get("region", {}).get("id"),
                "region_name": c.get("region", {}).get("value"),
                "income_level_id": c.get("incomeLevel", {}).get("id"),
                "income_level_name": c.get("incomeLevel", {}).get("value"),
                "lending_type_id": c.get("lendingType", {}).get("id"),
                "lending_type_name": c.get("lendingType", {}).get("value"),
                "capital_city": c.get("capitalCity"),
                "is_aggregate": 1 if c.get("region", {}).get("value") == "Aggregates" else 0
            })
        df = pd.DataFrame(records)
        df.to_csv(dest_csv, index=False)
        
        sha = calculate_sha256(dest_csv)
        print(f"[COUNTRY METADATA] Saved {len(df)} records ({df['is_aggregate'].sum()} aggregates, {len(df) - df['is_aggregate'].sum()} countries).")
        update_manifest({
            "resource_id": "WB_COUNTRY_METADATA",
            "description": "World Bank Country and Entity Classification Metadata",
            "source": "World Bank API v2",
            "url": url,
            "local_path": os.path.relpath(dest_csv).replace("\\", "/"),
            "file_size_bytes": os.path.getsize(dest_csv),
            "sha256": sha,
            "retrieval_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "status": "SUCCESS"
        }, manifest_path)
    except Exception as e:
        print(f"[ERROR] Failed to fetch country metadata: {e}")

def download_indicator(code: str, meta: dict, raw_dir: str, manifest_path: str):
    domain = meta["domain"]
    desc = meta["description"]
    print(f"\n[{code}] ({domain}: {desc})")
    
    # 1. Fetch metadata
    meta_url = f"{BASE_URL}/indicator/{code}?format=json"
    data_url = f"{BASE_URL}/country/all/indicator/{code}?date=2000:2023&format=json&per_page=20000"
    
    json_path = os.path.join(raw_dir, "json", f"{code}.json")
    meta_path = os.path.join(raw_dir, "json", f"{code}_metadata.json")
    csv_path = os.path.join(raw_dir, "csv", f"{code}.csv")
    
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    
    try:
        # Indicator metadata
        meta_json = fetch_json_with_retry(meta_url)
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta_json, f, indent=2)
            
        # Indicator data
        data_json = fetch_json_with_retry(data_url)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data_json, f, indent=2)
            
        page_info = data_json[0]
        raw_records = data_json[1] if len(data_json) > 1 else []
        
        rows = []
        for r in raw_records:
            rows.append({
                "indicator_id": r.get("indicator", {}).get("id"),
                "indicator_name": r.get("indicator", {}).get("value"),
                "country_iso2": r.get("country", {}).get("id"),
                "country_name": r.get("country", {}).get("value"),
                "country_iso3": r.get("countryiso3code"),
                "year": int(r.get("date")),
                "value": r.get("value"),
                "unit": r.get("unit"),
                "obs_status": r.get("obs_status"),
                "decimal": r.get("decimal")
            })
            
        df = pd.DataFrame(rows)
        df.to_csv(csv_path, index=False)
        
        non_null_count = df["value"].notnull().sum()
        total_count = len(df)
        pct_non_null = (non_null_count / total_count * 100) if total_count > 0 else 0
        
        print(f"  -> Total records: {total_count}, Non-null: {non_null_count} ({pct_non_null:.1f}%), Years: {df['year'].min()}-{df['year'].max()}")
        
        sha = calculate_sha256(csv_path)
        update_manifest({
            "resource_id": f"WB_IND_{code}",
            "indicator_code": code,
            "description": desc,
            "domain": domain,
            "source": "World Bank WDI API v2",
            "url": data_url,
            "local_path": os.path.relpath(csv_path).replace("\\", "/"),
            "file_size_bytes": os.path.getsize(csv_path),
            "sha256": sha,
            "total_records": total_count,
            "non_null_records": int(non_null_count),
            "retrieval_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "status": "SUCCESS"
        }, manifest_path)
        
    except Exception as e:
        print(f"  [ERROR] {code} failed: {e}")
        update_manifest({
            "resource_id": f"WB_IND_{code}",
            "indicator_code": code,
            "description": desc,
            "domain": domain,
            "source": "World Bank WDI API v2",
            "url": data_url,
            "local_path": None,
            "file_size_bytes": 0,
            "sha256": None,
            "retrieval_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "status": f"FAILED: {str(e)}"
        }, manifest_path)

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    raw_wb_dir = os.path.join(base_dir, "data", "raw", "world_bank")
    manifest_file = os.path.join(base_dir, "data", "metadata", "download_manifest.json")
    
    print("=" * 60)
    print("World Bank WDI Data Acquisition: 2000-2023")
    print("=" * 60)
    
    download_country_metadata(raw_wb_dir, manifest_file)
    
    for code, meta in INDICATORS.items():
        download_indicator(code, meta, raw_wb_dir, manifest_file)
        
    print("\nWorld Bank acquisition finished.")

if __name__ == "__main__":
    main()
