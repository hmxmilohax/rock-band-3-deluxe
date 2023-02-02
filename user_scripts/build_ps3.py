import sys
sys.path.append("../dependencies/dev_scripts")

from build_ark import build_patch_ark

build_patch_ark(False)
print("You may find the files needed to place on your PS3 in /_build/PS3/.")