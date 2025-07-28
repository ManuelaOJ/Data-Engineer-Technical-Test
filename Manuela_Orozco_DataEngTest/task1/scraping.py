# %%
import os
import requests
from bs4 import BeautifulSoup
import hashlib
import pandas as pd
import time
from pathlib import Path
from datetime import datetime, timezone
import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
import re


def extract_pdf_links(base_folder, url):
    base_folder = Path(base_folder)
    url = url

    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    if not base_folder.exists():
        base_folder.mkdir(parents=True, exist_ok=True)

    pdf_links = []

    for link in soup.find_all("a", href=True):
        href = link["href"]
        if (
            ("Q1" in href or "Q2" in href or "Q3" in href or "Q4" in href)
            and "Consolidated" in href
            and href.endswith(".pdf")
        ):
            if any(year in href for year in ["2021", "2022", "2023", "2024", "2025"]):
                pdf_links.append(href)

    return pdf_links


def create_clean_filename(url, year, quarter):
    original_filename = url.split("/")[-1].split("_", 1)[-1]
    original_filename = original_filename.replace("%20", " ").replace("%26", "&")

    if quarter:
        clean_name = f"Consolidated_Financial_Statements_Q{quarter}_{year}.pdf"
    else:
        clean_name = original_filename

    return clean_name


def download_and_save_pdf(url, year, quarter, base_folder):
    try:
        if year and quarter:
            folder_path = Path(base_folder, f"{year}_Q{quarter}")
        else:
            folder_path = Path(base_folder, "unknown")

        folder_path.mkdir(parents=True, exist_ok=True)

        filename = create_clean_filename(url, year, quarter)
        file_path = folder_path / filename

        if file_path.exists():
            print(f"File already exists: {file_path}")
            return True

        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Saved: {file_path}")
        return True

    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")
        return False


def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


def get_file_metadata(file_path):
    try:
        file_stats = os.stat(file_path)

        metadata = {
            "filename": file_path.name,
            "filesize": file_stats.st_size,
            "sha256": calculate_sha256(file_path),
            "download_timestamp": datetime.now(timezone.utc).isoformat(),
        }

        year, quarter = extract_year_quarter(file_path.name)
        metadata["year"] = year
        metadata["quarter"] = quarter

        return metadata

    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return None


def load_existing_metadata(parquet_path):
    if parquet_path.exists():
        try:
            table = pq.read_table(parquet_path)
            existing_df = table.to_pandas()
            return existing_df

        except Exception as e:
            print(f"Error loading existing metadata: {str(e)}")
            return pd.DataFrame(
                columns=["filename", "filesize", "sha256", "download_timestamp"]
            )
    else:
        return pd.DataFrame(
            columns=["filename", "filesize", "sha256", "download_timestamp"]
        )


def find_all_pdf_files(bronze_dir):
    bronze_path = Path(bronze_dir)
    pdf_files = []

    for pdf_file in bronze_path.rglob("*.pdf"):
        pdf_files.append(pdf_file)

    print(f"Found {len(pdf_files)} PDF files")
    return pdf_files


def process_metadata(bronze_dir, parquet_file):

    parquet_path = Path(bronze_dir, parquet_file)
    existing_df = load_existing_metadata(parquet_path)
    existing_hashes = (
        set(existing_df["sha256"].tolist()) if not existing_df.empty else set()
    )

    pdf_files = find_all_pdf_files(bronze_dir)

    new_metadata = []
    skipped_count = 0
    processed_count = 0

    for pdf_file in pdf_files:

        metadata = get_file_metadata(pdf_file)

        if metadata is None:
            continue

        if metadata["sha256"] in existing_hashes:
            print(f"Skipping {pdf_file.name} - SHA256 hash already exists in metadata")
            skipped_count += 1
            continue

        new_metadata.append(metadata)
        existing_hashes.add(metadata["sha256"])
        processed_count += 1

    if new_metadata:
        new_df = pd.DataFrame(new_metadata)

        if not existing_df.empty:
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        else:
            combined_df = new_df

        combined_df = combined_df.sort_values("filename").reset_index(drop=True)

        try:
            table = pa.Table.from_pandas(combined_df)
            pq.write_table(table, parquet_path)
        except Exception as e:
            print(f"Error with PyArrow, falling back to pandas: {e}")
            combined_df.to_parquet(parquet_path, index=False, engine="pyarrow")

        print(f"\n--- Metadata Processing Complete ---")
        print(f"Saved metadata to: {parquet_path}")
        print(f"Total records in metadata: {len(combined_df)}")
        print(f"New files processed: {processed_count}")
        print(f"Files skipped (already existed): {skipped_count}")

        print(f"\n--- Sample of Metadata ---")
        print(combined_df)

    else:
        print(f"\n--- No New Files to Process ---")
        print(f"Files skipped (already existed): {skipped_count}")
        print(f"Total records in existing metadata: {len(existing_df)}")


def extract_year_quarter(url):

    filename = url.split("/")[-1]

    year_match = re.search(r"(202[1-5])", filename)
    year = year_match.group(1) if year_match else None

    quarter_match = re.search(r"Q([1-4])", filename)
    quarter = quarter_match.group(1) if quarter_match else None

    if "YE_Q4" in filename or ("Q4" in filename and "YE" in filename):
        quarter = "4"

    return year, quarter


def main():
    base_folder = "Manuela_Orozco_DataEngTest/task1/bronze"
    url = "https://www.mineros.com.co/investors/financial-reports"
    pdf_links = extract_pdf_links(base_folder, url)
    successful_downloads = 0
    failed_downloads = 0

    for url in pdf_links:
        year, quarter = extract_year_quarter(url)

        if download_and_save_pdf(url, year, quarter, base_folder):
            successful_downloads += 1
        else:
            failed_downloads += 1

        time.sleep(1)

    print(f"\n--- Download Summary ---")
    print(f"Successful downloads: {successful_downloads}")
    print(f"Failed downloads: {failed_downloads}")
    print(f"Total files processed: {len(pdf_links)}")
    process_metadata(base_folder, "metadata_bronze.parquet")


if __name__ == "__main__":
    main()
