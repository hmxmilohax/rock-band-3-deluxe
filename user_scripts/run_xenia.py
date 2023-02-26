from pathlib import Path
import sys
import subprocess

sys.path.append("../dependencies/dev_scripts")
from build_ark import build_patch_ark
from build_dx_settings_ark import build_dxsl_ark
from check_git_updated import check_git_updated

# get the current working directory
cwd = Path(__file__).parent
root_dir = Path(__file__).parents[1] # root directory of the repo

cmd_xenia_loader = "_xenia\\xenia_canary.exe _build\\xbox\\dx-settings-loader.xex"
cmd_xenia = "_xenia\\xenia_canary.exe _build\\xbox\\default.xex"

dx_res = True
if check_git_updated(repo_url="https://github.com/hmxmilohax/dx-settings-loader", repo_root_path=root_dir.joinpath("dependencies/dev_scripts/dx-settings-loader")):
    if not root_dir.joinpath("_build/xbox/gen/dxsl_xbox_0.ark").is_file():
        print("DXSL ark not found, building it now...")
        dx_res = build_dxsl_ark()
else:
    print("Local repo out of date, pulling and building an updated DXSL ark now...")
    dx_res = build_dxsl_ark()

rb3dx_res = True
if check_git_updated(repo_url="https://github.com/hmxmilohax/rock-band-3-deluxe", repo_root_path=root_dir):
    if not root_dir.joinpath("_build/xbox/gen/patch_xbox_0.ark").is_file():
        print("Rock Band 3 Deluxe ark not found, building it now...")
        rb3dx_res = build_patch_ark(True)
else:
    print("Local repo out of date, pulling and building an updated Rock Band 3 Deluxe ark now...")
    rb3dx_res = build_patch_ark(True)
    
if dx_res:
    print("Ready to run DXSL in Xenia.")
    subprocess.run(cmd_xenia_loader, shell=True, cwd="..")
# if rb3dx_res:
#     print("Ready to run Rock Band 3 Deluxe in Xenia.")
#     subprocess.run(cmd_xenia, shell=True, cwd="..")