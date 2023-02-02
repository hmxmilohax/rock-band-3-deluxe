import sys
sys.path.append("../dependencies/dev_scripts")

from build_ark import build_patch_ark

build_patch_ark(True)
print("Ready to run RB3DX in Xenia.")