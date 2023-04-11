import os
import shutil
import tempfile
import zipfile
from pathlib import Path
import subprocess
# Check if requests is installed and install it if necessary
try:
    import requests
except ImportError:
    subprocess.check_call(["python", "-m", "pip", "install", "requests"])
    import requests

def download_and_extract_zip(url, output_dir):
    print("Downloading RB3Enhanced. Learn more at https://rb3e.rbenhanced.rocks/ and https://github.com/RBEnhanced/RB3Enhanced...")
    response = requests.get(url)
    response.raise_for_status()

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_zip_path = Path(tmpdir) / "RB3Enhanced_0.6-Xbox.zip"
        with open(tmp_zip_path, "wb") as f:
            f.write(response.content)

        with zipfile.ZipFile(tmp_zip_path, "r") as zip_ref:
            zip_ref.extractall(tmpdir)

        for item in os.listdir(tmpdir):
            item_path = Path(tmpdir) / item
            if item_path.is_file():
                if item not in ("INSTALLING_360.txt", "RB3ELoader.xex"):
                    shutil.copy(item_path, output_dir)
            else:
                for sub_item in os.listdir(item_path):
                    sub_item_path = item_path / sub_item
                    shutil.copytree(sub_item_path, output_dir / sub_item, dirs_exist_ok=True)

    print("RB3Enhanced for Xenia installation complete.")


def download_source_code(url, output_dir):
    print("Downloading the RB3Enhanced source...")
    response = requests.get(url)
    response.raise_for_status()

    source_code_zip_path = output_dir / "RB3Enhanced-master.zip"
    with open(source_code_zip_path, "wb") as f:
        f.write(response.content)

def main():
    script_path = Path(__file__).resolve().parent
    repo_root = script_path.parent
    xbox_directory = repo_root / "_build/Xbox"

    # Create the output directory if it doesn't exist
    xbox_directory.mkdir(parents=True, exist_ok=True)

    # Download and extract the zip file
    rb_enhanced_zip_url = "https://dl.rbenhanced.rocks/rb3e/0.6/RB3Enhanced_0.6-Xbox.zip"
    download_and_extract_zip(rb_enhanced_zip_url, xbox_directory)

    # Download the source code
    source_code_url = "https://github.com/RBEnhanced/RB3Enhanced/archive/refs/heads/master.zip"
    download_source_code(source_code_url, xbox_directory)


if __name__ == "__main__":
    main()
