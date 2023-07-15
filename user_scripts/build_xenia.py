import sys
import subprocess
sys.path.append("../dependencies/dev_scripts")

from download_mackiloha import download_mackiloha

from download_xenia import setup_xenia
from build_ark import build_patch_ark

# Download and extract Mackiloha-suite-archive.zip
if not download_mackiloha():
    print("Failed to download and extract Mackiloha-suite-archive.zip. Exiting.")
    sys.exit(1)

if build_patch_ark(True, rpcs3_mode=False):
    print("Xbox ARK built successfully.")
    print("Checking for updates to Xenia Canary")
    setup_xenia()
    cmd_xenia = "_xenia\\xenia_canary.exe _build\\xbox\\default.xex"
    subprocess.run(cmd_xenia, shell=True, cwd="..")
else:
    print("Error building Xbox ARK. Check your modifications or run git_reset.py to rebase your repo.")
