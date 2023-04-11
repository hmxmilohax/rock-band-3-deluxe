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

def download_raw_binary(url, output_dir, binary_name):
    print(f"Downloading {binary_name}...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    binary_path = output_dir / binary_name
    with open(binary_path, "wb") as f:
        f.write(response.content)

    print(f"Downloaded {binary_name}")

def download_and_extract_imagemagick(url, output_dir):
    if output_dir.exists() and any(output_dir.iterdir()):
        print(f"Directory {output_dir} already exists and has contents. Skipping download and extraction.")
        return
    
    output_dir.mkdir(parents=True, exist_ok=True)
    print("Downloading ImageMagick...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    image_magick_zip_path = output_dir / "ImageMagick-7.1.1-6-portable-Q8-x64.zip"
    with open(image_magick_zip_path, "wb") as f:
        f.write(response.content)

    # Extract contents of ImageMagick directly to the output_dir
    with zipfile.ZipFile(image_magick_zip_path, "r") as zip_ref:
        zip_ref.extractall(output_dir)

    os.remove(image_magick_zip_path)
    print("Downloaded and extracted ImageMagick")

    # Clean up the old folders
    old_folders = output_dir.glob("*")
    for folder in old_folders:
        if folder.is_dir() and folder.name.startswith("ImageMagick"):
            shutil.rmtree(folder)

# Get the script's file path and find the root directory of the repo
script_path = os.path.dirname(os.path.abspath(__file__))
repo_root = Path(script_path).parents[1]

# Set output directory
output_dir = repo_root / "dependencies" / "magick"

# Download and extract ImageMagick
image_magick_url = "https://imagemagick.org/archive/binaries/ImageMagick-7.1.1-6-portable-Q8-x64.zip"
download_and_extract_imagemagick(image_magick_url, output_dir)

# Download raw Linux binary
raw_linux_binary_url = "https://imagemagick.org/archive/binaries/magick"
binary_name = "magick"
download_raw_binary(raw_linux_binary_url, output_dir, binary_name)
