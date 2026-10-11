"""
download_mmeig.py
=================
Acquisition module for the WHO/UN MMEIG (Maternal Mortality Estimation Inter-Agency Group)
2025 estimation round: 'Trends in maternal mortality 2000 to 2023'.

Author: Collaborative Research Team
Date: October 2026
License: Open Data / Research Use
"""

import os
import sys
import json
import hashlib
import zipfile
import datetime
import requests

WHO_ZIP_URL = "https://cdn.who.int/media/docs/default-source/reproductive-health/maternal-health/trends-in-maternal-mortality-2000-to-2023-estimates-data.zip?sfvrsn=4718f695_7"
WHO_REPORT_PDF_URL = "https://iris.who.int/server/api/core/bitstreams/29f43a3d-2228-489c-b1e7-b2f28e9101ce/content"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

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
    
    # Update or append
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

def download_file(url: str, dest_path: str, resource_id: str, description: str, manifest_path: str, timeout: int = 60) -> bool:
    headers = {"User-Agent": USER_AGENT}
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Check if already exists
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 0:
        print(f"[EXISTS] {dest_path} already present ({os.path.getsize(dest_path)} bytes). Verifying...")
        file_hash = calculate_sha256(dest_path)
        entry = {
            "resource_id": resource_id,
            "description": description,
            "source": "WHO/UN MMEIG",
            "url": url,
            "local_path": os.path.relpath(dest_path).replace("\\", "/"),
            "file_size_bytes": os.path.getsize(dest_path),
            "sha256": file_hash,
            "retrieval_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "status": "VERIFIED_EXISTING"
        }
        update_manifest(entry, manifest_path)
        return True

    print(f"[DOWNLOADING] {description} from {url}...")
    try:
        resp = requests.get(url, headers=headers, stream=True, timeout=timeout)
        resp.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=16384):
                f.write(chunk)
        
        file_hash = calculate_sha256(dest_path)
        size = os.path.getsize(dest_path)
        print(f"[SUCCESS] Downloaded to {dest_path} ({size} bytes, SHA-256: {file_hash[:12]}...)")
        
        entry = {
            "resource_id": resource_id,
            "description": description,
            "source": "WHO/UN MMEIG",
            "url": url,
            "local_path": os.path.relpath(dest_path).replace("\\", "/"),
            "file_size_bytes": size,
            "sha256": file_hash,
            "retrieval_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "status": "SUCCESS"
        }
        update_manifest(entry, manifest_path)
        return True
    except Exception as e:
        print(f"[ERROR] Failed to download {description}: {e}")
        entry = {
            "resource_id": resource_id,
            "description": description,
            "source": "WHO/UN MMEIG",
            "url": url,
            "local_path": os.path.relpath(dest_path).replace("\\", "/"),
            "file_size_bytes": 0,
            "sha256": None,
            "retrieval_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "status": f"FAILED: {str(e)}"
        }
        update_manifest(entry, manifest_path)
        return False

def extract_archive(zip_path: str, target_dir: str):
    print(f"[EXTRACTING] {zip_path} -> {target_dir}...")
    os.makedirs(target_dir, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as z:
        for member in z.infolist():
            if not member.filename.startswith("__MACOSX") and not member.filename.endswith(".DS_Store"):
                z.extract(member, target_dir)
    print("[SUCCESS] Archive extracted.")

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    raw_mmeig_dir = os.path.join(base_dir, "data", "raw", "mmeig")
    manifest_file = os.path.join(base_dir, "data", "metadata", "download_manifest.json")
    
    zip_dest = os.path.join(raw_mmeig_dir, "trends-in-maternal-mortality-2000-to-2023-estimates-data.zip")
    pdf_dest = os.path.join(raw_mmeig_dir, "9789240108462-eng.pdf")
    extract_dest = os.path.join(raw_mmeig_dir, "extracted")
    
    print("=" * 60)
    print("MMEIG Data Acquisition: 2000-2023 Estimation Round")
    print("=" * 60)
    
    zip_ok = download_file(
        url=WHO_ZIP_URL,
        dest_path=zip_dest,
        resource_id="MMEIG_2025_ESTIMATES_ZIP",
        description="WHO/UN MMEIG Trends in Maternal Mortality 2000-2023 Complete Estimates and Inputs ZIP",
        manifest_path=manifest_file
    )
    
    pdf_ok = download_file(
        url=WHO_REPORT_PDF_URL,
        dest_path=pdf_dest,
        resource_id="MMEIG_2025_REPORT_PDF",
        description="WHO/UN MMEIG Trends in Maternal Mortality 2000-2023 Full Report PDF (ISBN 9789240108462)",
        manifest_path=manifest_file
    )
    
    if zip_ok and os.path.exists(zip_dest):
        extract_archive(zip_dest, extract_dest)
        
    print("\nMMEIG acquisition finished.")

if __name__ == "__main__":
    main()
