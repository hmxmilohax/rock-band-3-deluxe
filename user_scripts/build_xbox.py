import sys
sys.path.append("../dependencies/dev_scripts")

from download_mackiloha import download_mackiloha
from build_dx_settings_ark import build_dxsl_ark
from build_ark import build_patch_ark

# Download and extract Mackiloha-suite-archive.zip
if not download_mackiloha():
    print("Failed to download and extract Mackiloha-suite-archive.zip. Exiting.")
    sys.exit(1)

if build_dxsl_ark():
    if build_patch_ark(True):
        print("You may find the files needed to place on your Xbox 360 in /_build/Xbox/.")
