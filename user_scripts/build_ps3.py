# build_xbox.py
from pathlib import Path
from subprocess import CalledProcessError
import subprocess

def rm_tree(pth):
    pth = Path(pth)
    for child in pth.glob('*'):
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()

# directories used in this script
cwd = Path().absolute() # current working directory (user_scripts)
root_dir = Path(__file__).parents[1] # root directory of the repo
ark_dir = root_dir.joinpath("_ark")

# pull the latest changes from the RB3DX repo
cmd_pull = "git pull https://github.com/hmxmilohax/rock-band-3-deluxe main".split()
subprocess.run(cmd_pull, shell=True, cwd="..")

# temporarily move Xbox files out of the ark to reduce overall size
for f in ark_dir.rglob("*_xbox"):
    temp_path = str(f).replace(f"{str(root_dir)}\\", "")
    # print(temp_path)
    the_new_filename = root_dir.joinpath("_tmp").joinpath(temp_path)
    the_new_filename.parent.mkdir(parents=True, exist_ok=True)
    f.rename(the_new_filename)

# build the ark
failed = False
try:
    cmd_build = f"dependencies\\arkhelper.exe dir2ark _ark _build\ps3\\USRDIR\gen -n patch_ps3 -e -v 6".split()
    subprocess.check_output(cmd_build, shell=True, cwd="..")
except CalledProcessError as e:
    print(e.output)
    failed = True

# move the Xbox files back
for g in root_dir.joinpath("_tmp").rglob("*_xbox"):
    final_path = str(g).replace(f"{str(root_dir)}\\_tmp\\", "")
    # print(final_path)
    g.rename(root_dir.joinpath(final_path))

# remove temp directory
rm_tree(root_dir.joinpath("_tmp"))

if not failed:
    print("Successfully built Rock Band 3 Deluxe ARK. You may find the files needed to place on your PS3 in /_build/PS3/.")
else:
    print("Error building ARK. Check your modifications or run git_reset.py to rebase your repo.")