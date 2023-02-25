import sys
sys.path.append("../dependencies/dev_scripts")

from add_dx_settings_loader import download_loader

download_loader()

from build_dx_settings_ark import build_dxsl_ark

build_dxsl_ark()

from build_ark import build_patch_ark

build_patch_ark(True)
print("You may find the files needed to place on your Xbox 360 in /_build/Xbox/.")