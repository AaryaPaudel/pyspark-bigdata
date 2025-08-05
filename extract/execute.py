import os
import sys
import json
from kaggle.api.kaggle_api_extended import KaggleApi

def download_with_kaggle_api(dataset_name, download_dir):
    """
    Downloads and unzips a dataset from Kaggle using the API.
    """
    os.makedirs(download_dir, exist_ok=True)
    api = KaggleApi()
    api.authenticate()
    print(f"⬇️ Downloading dataset: {dataset_name}")
    api.dataset_download_files(dataset_name, path=download_dir, unzip=True)
    print(f"✅ Dataset downloaded and extracted to: {download_dir}")

def fix_json_file(json_file_path):
    """
    Converts a single large dictionary JSON file to NDJSON (newline-delimited).
    """
    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)

        fixed_path = json_file_path.replace(".json", "_fixed.json")
        with open(fixed_path, 'w') as f:
            for key, value in data.items():
                record = {key: value}
                f.write(json.dumps(record) + '\n')

        os.remove(json_file_path)
        print(f"✅ Fixed JSON file written to: {fixed_path}")
    except FileNotFoundError:
        print(f"⚠️ JSON file not found: {json_file_path}. Skipping fix.")
    except json.JSONDecodeError:
        print(f"❌ JSON parsing error. File might not be valid JSON.")

def run_etl(dataset_name, output_dir, json_filename="data.json"):
    print(f"📦 Dataset to download: {dataset_name}")
    print(f"📂 Output directory: {output_dir}")
    download_with_kaggle_api(dataset_name, output_dir)

    # List files to verify contents
    print("📁 Files in dataset:")
    for f in os.listdir(output_dir):
        print(" -", f)

    # Fix JSON only if present
    json_path = os.path.join(output_dir, json_filename)
    if os.path.exists(json_path):
        fix_json_file(json_path)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        dataset_name = sys.argv[1]
        output_dir = sys.argv[2]
    else:
        # Fallback defaults for Jupyter or no arguments
        dataset_name = "zynicide/wine-reviews"
        output_dir = "./data"

    run_etl(dataset_name, output_dir)
