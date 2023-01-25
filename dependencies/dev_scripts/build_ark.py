# build_ark.py
from pathlib import Path
from subprocess import CalledProcessError
from sys import platform
import subprocess

def rm_tree(pth):
    pth = Path(pth)
    for child in pth.glob('*'):
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()

# if xbox is true, build the Xbox ARK
# else, build the PS3 ARK
def build_patch_ark(xbox: bool):
    # directories used in this script
    cwd = Path().absolute() # current working directory (dev_scripts)
    root_dir = cwd.parents[0] # root directory of the repo
    ark_dir = root_dir.joinpath("_ark")

    files_to_remove = "*_ps3" if xbox else "*_xbox"
    build_location = "_build\\xbox\gen" if xbox else "_build\ps3\\USRDIR\gen"
    patch_hdr_version = "patch_xbox" if xbox else "patch_ps3"

    # pull the latest changes from the RB3DX repo
    cmd_pull = "git pull https://github.com/hmxmilohax/rock-band-3-deluxe main".split()
    subprocess.run(cmd_pull, shell=True, cwd="..")

    # temporarily move other console's files out of the ark to reduce overall size
    for f in ark_dir.rglob(files_to_remove):
        temp_path = str(f).replace(f"{str(root_dir)}\\", "")
        the_new_filename = root_dir.joinpath("_tmp").joinpath(temp_path)
        the_new_filename.parent.mkdir(parents=True, exist_ok=True)
        f.rename(the_new_filename)

    # build the ark
    failed = False
    try:
        if platform == "win32":
            cmd_build = f"dependencies\\arkhelper.exe dir2ark _ark {build_location} -n {patch_hdr_version} -e -v 6".split()
        else:
            cmd_build = f"dependencies\\arkhelper dir2ark _ark {build_location} -n {patch_hdr_version} -e -v 6".split()
        subprocess.check_output(cmd_build, shell=True, cwd="..")
    except CalledProcessError as e:
        print(e.output)
        failed = True

    # move the other console's files back
    for g in root_dir.joinpath("_tmp").rglob(files_to_remove):
        final_path = str(g).replace(f"{str(root_dir)}\\_tmp\\", "")
        # print(final_path)
        g.rename(root_dir.joinpath(final_path))

    # remove temp directory
    rm_tree(root_dir.joinpath("_tmp"))

    if not failed:
        print("Successfully built Rock Band 3 Deluxe ARK.")
    else:
        print("Error building ARK. Check your modifications or run git_reset.py to rebase your repo.")