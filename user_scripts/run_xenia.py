from pathlib import Path
import sys
import subprocess

sys.path.append("../dependencies/dev_scripts")

from build_ark import build_patch_ark
from check_git_updated import check_git_updated

# get the current working directory
cwd = Path().absolute()
root_dir = Path(__file__).parents[1] # root directory of the repo

cmd_xenia = "_xenia\\xenia_canary.exe _build\\xbox\\default_xenia.xex"

if check_git_updated:
    res = True
    if not root_dir.joinpath("_build/xbox/gen/patch_xbox_0.ark").is_file():
        print("RB3DX ark not found, building it now...")
        res = build_patch_ark(True)
    if res:
        print("Ready to run RB3DX in Xenia.")
        subprocess.run(cmd_xenia, shell=True, cwd="..")
else:
    print("Local repo out of date, pulling and building an updated RB3DX ark now...")
    if build_patch_ark(True):
        print("Ready to run RB3DX in Xenia.")
        subprocess.run(cmd_xenia, shell=True, cwd="..")