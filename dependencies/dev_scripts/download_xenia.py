import os
import re
import zipfile
from pathlib import Path
import subprocess
import shutil
import time
import subprocess
# Check if requests is installed and install it if necessary
try:
    import requests
except ImportError:
    subprocess.check_call(["python", "-m", "pip", "install", "requests"])
    import requests

XENIA_CANARY_REPO = "https://api.github.com/repos/xenia-canary/xenia-canary/releases/latest"
EXE_NAME = "xenia_canary.exe"

def fetch_latest_release_info():
    response = requests.get(XENIA_CANARY_REPO)
    response.raise_for_status()
    return response.json()

def download_file(url, destination):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(destination, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

def create_portable_file(directory):
    portable_file = directory / "portable.txt"
    if not portable_file.exists():
        with open(portable_file, "w") as f:
            pass

def download_patch_file(destination_dir):

# https://raw.githubusercontent.com/jnackmclain/game-patches/rb3dx-rb3e-patches/patches/45410914%20-%20Rock%20Band%203.patch.toml
# https://raw.githubusercontent.com/xenia-canary/game-patches/patches/45410914%20-%20Rock%20Band%203.patch.toml
    url = "https://raw.githubusercontent.com/jnackmclain/game-patches/rb3dx-rb3e-patches/patches/45410914%20-%20Rock%20Band%203.patch.toml"
    response = requests.get(url)
    response.raise_for_status()

    patches_folder = destination_dir / "patches"
    patches_folder.mkdir(parents=True, exist_ok=True)

    patch_file_path = patches_folder / "45410914 - Rock Band 3.patch.toml"
    with open(patch_file_path, "wb") as f:
        f.write(response.content)

def extract_zip(zip_path, destination):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(destination)

def update_toml_line(line, prefix, desired_value):
    if line.startswith(prefix):
        return f"{prefix} {desired_value}\n"
    return line

def update_patch_file(patch_file_path):
    lines_to_update = ["    is_enabled = true"]

    with open(patch_file_path, "r") as f:
        lines = f.readlines()

    with open(patch_file_path, "w") as f:
        for i, line in enumerate(lines):
            if line.strip() == 'author = "InvoxiPlayGames"' and i < len(lines) - 1:
                next_line = lines[i + 1].strip()
                if next_line != "is_enabled = true":
                    lines[i + 1] = "    is_enabled = true\n"

            f.write(lines[i])

def modify_config_file(config_path):
    with open(config_path, "r") as f:
        lines = f.readlines()

    with open(config_path, "w") as f:
        for line in lines:
            line = update_toml_line(line, "max_queued_frames =", "3")
            line = update_toml_line(line, "allow_game_relative_writes =", "true")
            line = update_toml_line(line, "writable_code_segments =", "true")
            line = update_toml_line(line, "license_mask =", "1")
            line = update_toml_line(line, "gpu =", "\"vulkan\"")
            f.write(line)

def download_and_extract_x360ce(url, output_dir):
    source_txt = output_dir / "x360ce_source.txt"

    if source_txt.is_file():
        print("x360ce_source.txt exists, skipping download")
        return

    print("Downloading x360ce_x64.zip...")
    response = requests.get(url)
    response.raise_for_status()

    x360ce_zip_path = output_dir / "x360ce_x64.zip"
    with open(x360ce_zip_path, "wb") as f:
        f.write(response.content)

    with zipfile.ZipFile(x360ce_zip_path, "r") as zip_ref:
        zip_ref.extractall(output_dir)

    os.remove(x360ce_zip_path)
    print("Downloaded x360ce_x64")

    with open(source_txt, "w") as f:
        f.write(url)

def setup_xenia():
    # Determine the destination directory
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent.parent
    destination_dir = repo_root / "_xenia"
    
    # Create the destination directory if it doesn't exist
    destination_dir.mkdir(parents=True, exist_ok=True)

    create_portable_file(destination_dir)

    download_patch_file(destination_dir)

    # Download x360ce_x64.zip
    x360ce_url = "https://emutopia.com/index.php?option=com_cobalt&task=files.download&tmpl=component&id=12279&fid=20&fidx=3&rid=541&return=aHR0cHM6Ly9lbXV0b3BpYS5jb20vaW5kZXgucGhwL2VtdWxhdG9ycy9pdGVtLzI0MC1nYW1lcGFkcy81NDEteDM2MGNl"
    download_and_extract_x360ce(x360ce_url, destination_dir)

    patch_file_path = destination_dir / "patches" / "45410914 - Rock Band 3.patch.toml"
    update_patch_file(patch_file_path)

    # Fetch the latest release information
    release_info = fetch_latest_release_info()
    latest_commit_hash = release_info["target_commitish"]

    # Check if the latest commit hash is already installed
    local_commit_hash_file = destination_dir / "xenia_canary_commit_hash.txt"
    if local_commit_hash_file.exists():
        with open(local_commit_hash_file, "r") as f:
            local_commit_hash = f.read().strip()
    else:
        local_commit_hash = None

    if local_commit_hash != latest_commit_hash:
        # Download the latest release
        asset = next((asset for asset in release_info["assets"] if asset["name"] == "xenia_canary.zip"), None)
        if asset is None:
            raise ValueError("xenia_canary.zip not found in the release assets.")

        tmp_dir = repo_root / "tmp"
        tmp_dir.mkdir(parents=True, exist_ok=True)
        download_path = tmp_dir / "xenia_canary.zip"
        download_file(asset["browser_download_url"], str(download_path))

        # Extract the zip file
        extract_zip(str(download_path), str(destination_dir))

        # Update the commit hash file
        with open(local_commit_hash_file, "w") as f:
            f.write(latest_commit_hash)

        # Clean up the tmp directory
        shutil.rmtree(tmp_dir)

        if local_commit_hash is None:
            print(f"Xenia Canary {latest_commit_hash} has been installed.")
        else:
            print(f"Xenia Canary has been updated from {local_commit_hash} to {latest_commit_hash}.")
    else:
        print(f"Latest Xenia Canary {latest_commit_hash} is already installed.")

    # Check if xenia-canary.config.toml exists, if not, create it
    config_file_path = destination_dir / "xenia-canary.config.toml"
    if not config_file_path.exists():
        exe_path = destination_dir / EXE_NAME
        process = subprocess.Popen(str(exe_path), close_fds=True)
        time.sleep(1)  # Wait for 2 seconds before terminating the process
        process.terminate()
        process.wait()

    # Modify the config file
    modify_config_file(config_file_path)

if __name__ == "__setup_xenia__":
    setup_xenia()
