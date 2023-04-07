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

def download_and_extract_ta_pkg_repacker(url, output_dir, num_retries=3, retry_delay=5):
    for i in range(num_retries):
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            print("Downloading TrueAncestor_PKG_Repacker_v2.45.zip...")
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            ta_pkg_zip_path = output_dir / "TrueAncestor_PKG_Repacker_v2.45.zip"
            with open(ta_pkg_zip_path, "wb") as f:
                f.write(response.content)

            with zipfile.ZipFile(ta_pkg_zip_path, "r") as zip_ref:
                zip_ref.extractall(output_dir)

            os.remove(ta_pkg_zip_path)
            print("Downloaded and extracted TrueAncestor_PKG_Repacker_v2.45.zip")

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

            # Copy package.conf
            package_conf_src = repo_root / "dependencies" / "package.conf"
            package_conf_dst = ta_pkg_repacker_tools / "package.conf"
            shutil.copy(package_conf_src, package_conf_dst)

            shutil.rmtree(output_dir)
            return

        except Exception as e:
            print(f"Error encountered while downloading and extracting TrueAncestor_PKG_Repacker_v2.45.zip: {e}")
            if i == num_retries - 1:
                raise
            else:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)

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
ta_pkg_url = "https://www.newgrounds.com/dump/download/3e81199977d984b586c8e081a680f371"
download_and_extract_ta_pkg_repacker(ta_pkg_url, output_dir)
