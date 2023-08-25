# build_ark.py
from pathlib import Path
from subprocess import CalledProcessError
from sys import platform
import subprocess
from check_git_updated import check_git_updated
import os
import shutil

def rm_tree(pth):
    pth = Path(pth)
    for child in pth.glob('*'):
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()

def make_executable_binaries():
    # Make the binaries executable if on a non-Windows platform
    if platform != "win32":
        try:
            cmd_chmod_arkhelper = ["chmod", "+x", "dependencies/linux/arkhelper"]
            subprocess.check_output(cmd_chmod_arkhelper, cwd="..")
        except subprocess.CalledProcessError:
            print("Failed to make arkhelper executable.")
            sys.exit(1)

        try:
            cmd_chmod_dtab = ["chmod", "+x", "dependencies/linux/dtab"]
            subprocess.check_output(cmd_chmod_dtab, cwd="..")
        except subprocess.CalledProcessError:
            print("Failed to make dtab executable.")
            sys.exit(1)

# darwin: mac

# if xbox is true, build the Xbox ARK
# else, build the PS3 ARK
def build_patch_ark(wii: bool, xbox: bool, rpcs3_directory: str = None, rpcs3_mode: bool = False):
    # directories used in this script
    cwd = Path().absolute() # current working directory (dev_scripts)
    root_dir = cwd.parents[0] # root directory of the repo
    ark_dir = root_dir.joinpath("_ark")
    if wii:
        hdr_location = root_dir.joinpath("_build/wii/wit_input/files/gen/main_wii.hdr")
        ark_location = root_dir.joinpath("_build/wii/wit_input/files/gen/main_wii_10.ark")

        # Delete existing Wii files
        if hdr_location.exists():
            hdr_location.unlink()
        if ark_location.exists():
            ark_location.unlink()

        # Copy Wii header and ark files from dependencies if they don't exist
        rebuild_hdr_location = root_dir.joinpath("dependencies/rebuild_files/main_wii.hdr")
        rebuild_ark_location = root_dir.joinpath("dependencies/rebuild_files/main_wii_10.ark")

        if not hdr_location.exists() and rebuild_hdr_location.exists():
            shutil.copyfile(rebuild_hdr_location, hdr_location)
        if not ark_location.exists() and rebuild_ark_location.exists():
            shutil.copyfile(rebuild_ark_location, ark_location)


    files_to_remove = "*_ps3" if xbox else "*_xbox"
    files_to_remove_wii = "*_ps3"
    if rpcs3_mode:
        if platform == "win32":
            build_location = rpcs3_directory + "\\game\\BLUS30463\\USRDIR\\gen"
        else:
            build_location = rpcs3_directory + "/game/BLUS30463/USRDIR/gen"
    else:
        if platform == "win32":
            build_location = "_build\\xbox\gen" if xbox else "_build\ps3\\USRDIR\gen"
        else:
            build_location = "_build/xbox/gen" if xbox else "_build/ps3/USRDIR/gen"
    if wii:
        if platform == "win32":
            build_location = "_build\\wii\wit_input\\files"
            hdr_location = "_build\\wii\wit_input\\files\\gen\\main_wii.hdr"
        else:
            build_location = "_build/wii/wit_input/files"
            hdr_location = "_build/wii/wit_input/files/gen/main_wii.hdr"

        # build the binaries if on linux/other OS
        if platform != "darwin":
            make_executable_binaries()
    patch_hdr_version = "patch_xbox" if xbox else "patch_ps3"

    # pull the latest changes from the Rock Band 3 Deluxe repo if necessary
    if not check_git_updated(repo_url="https://github.com/hmxmilohax/rock-band-3-deluxe", repo_root_path=root_dir):
        cmd_pull = "git pull https://github.com/hmxmilohax/rock-band-3-deluxe main".split()
        subprocess.run(cmd_pull, shell=(platform == "win32"), cwd="..")

    # temporarily move other console's files out of the ark to reduce overall size
    for f in ark_dir.rglob(files_to_remove):
        temp_path = str(f).replace(f"{str(root_dir)}\\", "").replace(f"{str(root_dir)}/","")
        # print(temp_path)
        the_new_filename = root_dir.joinpath("_tmp").joinpath(temp_path)
        the_new_filename.parent.mkdir(parents=True, exist_ok=True)
        # print(f"moving file {temp_path} to {the_new_filename}")
        f.rename(the_new_filename)
        
        # temporarily move other console's files out of the ark to reduce overall size
    if wii:
        for f in ark_dir.rglob(files_to_remove_wii):
            temp_path2 = str(f).replace(f"{str(root_dir)}\\", "").replace(f"{str(root_dir)}/","")
            # print(temp_path2)
            the_new_filename2 = root_dir.joinpath("_tmp2").joinpath(temp_path2)
            the_new_filename2.parent.mkdir(parents=True, exist_ok=True)
            # print(f"moving file {temp_path2} to {the_new_filename2}")
            f.rename(the_new_filename2)

    # build the ark
    print("Building Rock Band 3 Deluxe ARK...")
    failed = False
    if wii:
        try:
            if platform == "win32":
                cmd_build = f"dependencies\windows\\arkhelper.exe patchcreator {hdr_location} -a _ark -o {build_location}".split()
            elif platform == "darwin":
                cmd_build = f"dependencies/macos/arkhelper patchcreator {hdr_location} -a _ark -o {build_location}".split()
            else:
                cmd_build = f"dependencies/linux/arkhelper patchcreator {hdr_location} -a _ark -o {build_location}".split()
            subprocess.check_output(cmd_build, shell=(platform == "win32"), cwd="..")
        except CalledProcessError as e:
            failed = False
    else:
        try:
            if platform == "win32":
                cmd_build = f"dependencies\windows\\arkhelper.exe dir2ark _ark {build_location} -n {patch_hdr_version} -e -v 6".split()
            elif platform == "darwin":
                cmd_build = f"dependencies/macos/arkhelper dir2ark _ark {build_location} -n {patch_hdr_version} -e -v 6".split()
            else:
                cmd_build = f"dependencies/linux/arkhelper dir2ark _ark {build_location} -n {patch_hdr_version} -e -v 6".split()
            subprocess.check_output(cmd_build, shell=(platform == "win32"), cwd="..")
        except CalledProcessError as e:
            print(e.output)
            failed = True

    # move the other console's files back
    for g in root_dir.joinpath("_tmp").rglob(files_to_remove):
        final_path = str(g).replace(f"{str(root_dir)}\\_tmp\\", "").replace(f"{str(root_dir)}/_tmp/","")
        # print(final_path)
        g.rename(root_dir.joinpath(final_path))
    if wii:
        for g in root_dir.joinpath("_tmp2").rglob(files_to_remove_wii):
            final_path = str(g).replace(f"{str(root_dir)}\\_tmp2\\", "").replace(f"{str(root_dir)}/_tmp2/","")
            # print(final_path)
            g.rename(root_dir.joinpath(final_path))

    # remove temp directory
    if os.path.exists(root_dir.joinpath("_tmp")):
        rm_tree(root_dir.joinpath("_tmp"))
    if os.path.exists(root_dir.joinpath("_tmp2")):
        rm_tree(root_dir.joinpath("_tmp2"))

    if not failed:
        # print("Successfully built Rock Band 3 Deluxe ARK.")
        return True
    else:
        print("Error building ARK. Check your modifications or run git_reset.py to rebase your repo.")
        return False