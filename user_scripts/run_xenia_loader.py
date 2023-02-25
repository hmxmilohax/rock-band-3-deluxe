from pathlib import Path
import sys
import subprocess

sys.path.append("../dependencies/dev_scripts")
from build_dx_settings_ark import build_dxsl_ark
from check_git_updated import check_git_updated

# get the current working directory
cwd = Path(__file__).parent
root_dir = Path(__file__).parents[1] # root directory of the repo

cmd_xenia = "_xenia\\xenia_canary.exe _build\\xbox\\dx-settings-loader.xex"

if check_git_updated(repo_url="https://github.com/hmxmilohax/dx-settings-loader", repo_root_path=root_dir.joinpath("dependencies/dev_scripts/dx-settings-loader")):
    res = True
    if not root_dir.joinpath("_build/xbox/gen/dxsl_xbox_0.ark").is_file():
        print("DXSL ark not found, building it now...")
        res = build_dxsl_ark()
    if res:
        print("Ready to run DXSL in Xenia.")
        subprocess.run(cmd_xenia, shell=True, cwd="..")
else:
    print("Local repo out of date, pulling and building an updated DXSL ark now...")
    if build_dxsl_ark():
        print("Ready to run DXSL in Xenia.")
        subprocess.run(cmd_xenia, shell=True, cwd="..")