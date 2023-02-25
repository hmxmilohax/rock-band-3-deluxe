# build_ark.py
from pathlib import Path
from subprocess import CalledProcessError
from sys import platform
import subprocess
from pathlib import Path
from check_git_updated_settings import check_git_updated

def rm_tree(pth):
    pth = Path(pth)
    for child in pth.glob('*'):
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()

def make_executable_binaries():
    if platform == "darwin":
        cmd_chmod_arkhelper_mac = "chmod +x dependencies/macOS//arkhelper".split()
        subprocess.check_output(cmd_chmod_arkhelper_mac, shell=(platform == "win32"), cwd="..")
        cmd_chmod_dtab_mac = "chmod +x dependencies/macOS//dtab".split()
        subprocess.check_output(cmd_chmod_dtab_mac, shell=(platform == "win32"), cwd="..")
    else:
        cmd_chmod_arkhelper_linux = "chmod +x dependencies/linux//arkhelper".split()
        subprocess.check_output(cmd_chmod_arkhelper_linux, shell=(platform == "win32"), cwd="..")
        cmd_chmod_dtab_linux = "chmod +x dependencies/linux//dtab".split()
        subprocess.check_output(cmd_chmod_dtab_linux, shell=(platform == "win32"), cwd="..")

# darwin: mac

# if xbox is true, build the Xbox ARK
# else, build the PS3 ARK
def build_dxsl_ark():
    # directories used in this script
    cwd = Path().absolute() # current working directory (dev_scripts)
    root_dir = cwd.parents[0] # root directory of the repo

    print("Building DX Settings Loader...")

    ark_location = root_dir.joinpath("dependencies/dev_scripts/dx-settings-loader/_ark")
    build_location = root_dir.joinpath("dependencies/dev_scripts/dx-settings-loader/_build//xbox/gen")
    
    if platform == "win32":
        arkhelperwin_location = root_dir.joinpath("dependencies/windows//arkhelper.exe")
    else:
        arkhelpermac_location = root_dir.joinpath("dependencies/macOS//arkhelper")
        dtabmac_location = root_dir.joinpath("dependencies/macOS//dtab")
        arkhelperlinux_location = root_dir.joinpath("dependencies/linux//arkhelper")
        # build the binaries if on linux/other OS
        if platform != "darwin":
            make_executable_binaries()
    patch_hdr_version = "dxsl_xbox"

    # pull the latest changes from the RB3DX repo if necessary
    if not check_git_updated():
        cmd_pull = "git pull https://github.com/hmxmilohax/dx-settings-loader main".split()
        subprocess.run(cmd_pull, shell=(platform == "win32"))


    # build the ark
    failed = False
    try:
        if platform == "win32":
            cmd_build = f"{arkhelperwin_location} dir2ark {ark_location} {build_location} -n {patch_hdr_version} -e -v 5".split()
        elif platform == "darwin":
            cmd_build = f"{arkhelpermac_location} dir2ark {ark_location} {build_location} -n {patch_hdr_version} -e -v 5".split()
        else:
            cmd_build = f"{arkhelperlinux_location} dir2ark {ark_location} {build_location} -n {patch_hdr_version} -e -v 5".split()
        subprocess.check_output(cmd_build, shell=(platform == "win32"), cwd="..")
    except CalledProcessError as e:
        print(e.output)
        failed = True

    if not failed:
        print("Successfully built DX Settings Loader ARK.")
        print("Copying DX Settings Loader to final build path.")
        source1_path = root_dir.joinpath("dependencies/dev_scripts/dx-settings-loader/_build//xbox/gen/dxsl_xbox.hdr")
        destination1_path = root_dir.joinpath("_build//xbox/gen/dxsl_xbox.hdr")
        destination1_path.write_bytes(source1_path.read_bytes())
        source2_path = root_dir.joinpath("dependencies/dev_scripts/dx-settings-loader/_build//xbox/gen/dxsl_xbox_0.ark")
        destination2_path = root_dir.joinpath("_build//xbox/gen/dxsl_xbox_0.ark")
        destination2_path.write_bytes(source2_path.read_bytes())
        source3_path = root_dir.joinpath("dependencies/dev_scripts/dx-settings-loader/_build//xbox/dx-settings-loader.xex")
        destination3_path = root_dir.joinpath("_build//xbox/dx-settings-loader.xex")
        destination3_path.write_bytes(source3_path.read_bytes())
        return True
    else:
        print("Error building ARK. Check your modifications or run git_reset.py to rebase your repo.")
        return False