import os
import zipfile
import shutil
import requests
from pathlib import Path

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

    with zipfile.ZipFile(image_magick_zip_path, "r") as zip_ref:
        zip_ref.extractall(output_dir)

    os.remove(image_magick_zip_path)
    print("Downloaded and extracted ImageMagick")

    magick_dir = output_dir / "magick"

    if magick_dir.exists():
        shutil.rmtree(magick_dir)

    magick_dir.mkdir()

    # Move the ImageMagick contents to the magick folder
    for item in output_dir.iterdir():
        if item.name != "magick":
            shutil.move(str(item), str(magick_dir / item.name))

    # Clean up the old folders
    old_folders = output_dir.glob("*")
    for folder in old_folders:
        if folder.is_dir() and folder.name != "magick":
            shutil.rmtree(folder)

# Get the script's file path and find the root directory of the repo
script_path = os.path.dirname(os.path.abspath(__file__))
repo_root = Path(script_path).parents[1]

# Set output directory
output_dir = repo_root / "dependencies" / "magick"

# Download and extract ImageMagick
image_magick_url = "https://imagemagick.org/archive/binaries/ImageMagick-7.1.1-6-portable-Q8-x64.zip"
download_and_extract_imagemagick(image_magick_url, output_dir)
