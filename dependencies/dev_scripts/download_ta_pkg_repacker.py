import os
import zipfile
import shutil
import time
from pathlib import Path

# Check if requests is installed and install it if necessary
try:
    import requests
except ImportError:
    subprocess.check_call(["python", "-m", "pip", "install", "requests"])
    import requests

def download_and_extract_ta_pkg_repacker(url, output_dir, max_retries=3):
    for attempt in range(max_retries):
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            print("Downloading TrueAncestor_PKG_Repacker_v2.45.zip...")
            response = requests.get(url)
            response.raise_for_status()

            ta_pkg_zip_path = output_dir / "TrueAncestor_PKG_Repacker_v2.45.zip"
            with open(ta_pkg_zip_path, "wb") as f:
                f.write(response.content)

            with zipfile.ZipFile(ta_pkg_zip_path, "r") as zip_ref:
                zip_ref.extractall(output_dir)

            os.remove(ta_pkg_zip_path)
            print("Downloaded and extracted TrueAncestor_PKG_Repacker_v2.45.zip")
            break
        except (requests.exceptions.RequestException, zipfile.BadZipFile) as e:
            print(f"Error during download or extraction (attempt {attempt + 1}): {e}")
            if attempt + 1 == max_retries:
                raise
            time.sleep(5)  # Wait for 5 seconds before retrying

    data_dir = output_dir / "data"
    history_txt = output_dir / "history.txt"
    repacker_exe = output_dir / "repacker.exe"
    tool_dir = output_dir / "tool"
    ta_pkg_repacker_tools = output_dir.parent / "ta_pkg_repacker_tools"

    if data_dir.exists():
        shutil.rmtree(data_dir)
    if history_txt.exists():
        os.remove(history_txt)
    if repacker_exe.exists():
        os.remove(repacker_exe)

    ta_pkg_repacker_tools.mkdir(parents=True, exist_ok=True)

    if tool_dir.exists():
        for item in tool_dir.iterdir():
            shutil.move(str(item), str(ta_pkg_repacker_tools / item.name))
        os.rmdir(tool_dir)

    shutil.rmtree(output_dir)

    # Copy package.conf
    package_conf_src = repo_root / "dependencies/package.conf"
    package_conf_dst = ta_pkg_repacker_tools / "package.conf"
    shutil.copy(package_conf_src, package_conf_dst)

# Get the script's file path and find the root directory of the repo
script_path = os.path.dirname(os.path.abspath(__file__))
repo_root = Path(script_path).parents[1]

# Set output directory
output_dir = repo_root / "dependencies/TrueAncestor_PKG_Repacker_v2.45"

# Download TrueAncestor_PKG_Repacker_2.00.zip
ta_pkg_url = "https://download854.mediafire.com/7vua4gyosbcgf_yIfLoBcf_mcIw7VfldOoXesGZIfrpy3WOLGBeVfwNe7yRaT-f7cEFS5JronexqTHW16OyAKmxzlow/3gpppcmydlwd4ud/TrueAncestor_PKG_Repacker_v2.45.zip"
download_and_extract_ta_pkg_repacker(ta_pkg_url, output_dir)