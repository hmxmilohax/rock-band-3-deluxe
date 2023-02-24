import sys
import subprocess

sys.path.append("../dependencies/dev_scripts")

from add_dx_settings_loader import download_loader

download_loader()

from build_dx_settings_ark import build_dxsl_ark

build_dxsl_ark()

from build_ark import build_patch_ark

if build_patch_ark(True):
    print("Ready to run RB3DX in Xenia.")
    cmd_xenia = "_xenia\\xenia_canary.exe _build\\xbox\\dx-settings-loader.xex"
    subprocess.run(cmd_xenia, shell=True, cwd="..")