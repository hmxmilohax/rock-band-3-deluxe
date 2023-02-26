import sys
import subprocess
sys.path.append("../dependencies/dev_scripts")
from build_dx_settings_ark import build_dxsl_ark
from build_ark import build_patch_ark

if build_dxsl_ark():
    if build_patch_ark(True):
        print("Ready to run Rock Band 3 Deluxe in Xenia.")
        cmd_xenia = "_xenia\\xenia_canary.exe _build\\xbox\\dx-settings-loader.xex"
        subprocess.run(cmd_xenia, shell=True, cwd="..")