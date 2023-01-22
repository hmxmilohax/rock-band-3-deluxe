import sys
sys.path.append("../dependencies/dev_scripts")

from build_ark import build_patch_ark

build_patch_ark(True)
print("You may find the files needed to place on your Xbox 360 in /_build/Xbox/.")