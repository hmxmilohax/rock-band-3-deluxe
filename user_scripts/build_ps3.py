import sys
sys.path.append("../dependencies/dev_scripts")

from build_ark import build_patch_ark
from download_mackiloha import download_mackiloha

successful_extraction = download_mackiloha()

if successful_extraction:
    build_patch_ark(False)
    print("You may find the files needed to place on your PS3 in /_build/PS3/.")
else:
    print("Failed to extract Mackiloha-suite-archive.zip. Please check the download and extraction process.")
