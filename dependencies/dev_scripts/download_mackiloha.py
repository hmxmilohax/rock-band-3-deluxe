import os
import zipfile
import shutil
from pathlib import Path
import subprocess
# Check if requests is installed and install it if necessary
try:
    import requests
except ImportError:
    subprocess.check_call(["python", "-m", "pip", "install", "requests"])
    import requests

def download_and_extract_mackiloha_suite(url, output_dir):
    print("Downloading Mackiloha-suite-archive.zip...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    max_retries = 3
    retry_count = 0
    while retry_count < max_retries:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            mackiloha_zip_path = output_dir / "Mackiloha-suite-archive.zip"
            with open(mackiloha_zip_path, "wb") as f:
                f.write(response.content)

            with zipfile.ZipFile(mackiloha_zip_path, "r") as zip_ref:
                zip_ref.extractall(output_dir)

            os.remove(mackiloha_zip_path)
            print("Downloaded and extracted Mackiloha-suite-archive.zip")
            return True
        except Exception as e:
            print(f"Error downloading {url} ({str(e)}), retrying in 5 seconds...")
            time.sleep(5)
            retry_count += 1
    print(f"Failed to download {url} after {max_retries} attempts.")
    return False


def check_extracted_contents(output_dir: Path) -> bool:
    # List the expected extracted contents
    expected_contents = [
        output_dir / "Mackiloha-master.zip",
        output_dir / "windows" / "arkhelper.exe",
        output_dir / "linux" / "arkhelper",
        output_dir / "macOS" / "arkhelper",
    ]
    
    # Check if all expected contents exist
    for expected_content in expected_contents:
        if not expected_content.exists():
            return False
    
    return True

def download_mackiloha() -> bool:
    # Get the script's file path and find the root directory of the repo
    script_path = os.path.dirname(os.path.abspath(__file__))
    repo_root = Path(script_path).parents[1]

    # Set output directory
    output_dir = repo_root / "dependencies"

    # Check if the extracted contents already exist
    extracted_contents_exist = check_extracted_contents(output_dir)
    
    if extracted_contents_exist:
        print("Extracted contents already exist. Skipping the download.")
        return True

    # Download Mackiloha-suite-archive.zip
    mackiloha_url = "https://archive.org/download/mackiloha-suite-archive/Mackiloha-suite-archive.zip"

    return download_and_extract_mackiloha_suite(mackiloha_url, output_dir)

if __name__ == "__main__":
    download_mackiloha()

