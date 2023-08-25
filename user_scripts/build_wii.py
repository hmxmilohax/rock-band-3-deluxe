import sys
sys.path.append("../dependencies/dev_scripts")

from download_mackiloha import download_mackiloha
from build_ark import build_patch_ark

# Download and extract Mackiloha-suite-archive.zip
if not download_mackiloha():
    print("Failed to download and extract Mackiloha-suite-archive.zip. Exiting.")
    sys.exit(1)

if build_patch_ark(True, False, rpcs3_mode=False):
    print("Wii built successfully!")
    print("Complete! You may find the files needed in /_build/Wii/.")
else:
    print("Error building Wii ARK. Check your modifications or run git_reset.py to rebase your repo.")
