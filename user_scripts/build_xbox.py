import sys
sys.path.append("../dependencies/dev_scripts")
from build_dx_settings_ark import build_dxsl_ark
from build_ark import build_patch_ark

if build_dxsl_ark():
    if build_patch_ark(True):
        print("You may find the files needed to place on your Xbox 360 in /_build/Xbox/.")