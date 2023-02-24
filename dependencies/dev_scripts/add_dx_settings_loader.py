# add_rb3_plus_pro_strings.py
from pathlib import Path
import subprocess

try:
    import git
except:
    cmd_install = "pip install gitpython".split()
    subprocess.run(cmd_install)

def download_loader():

    print("Downloading DX Settings Loader...")
        
    # get the current working directory
    cwd = Path(__file__).parent
    # print(cwd)
    # get the root directory of the repo
    root_dir = Path(__file__).parents[2]
    # print(root_dir)

    # clone/pull rb3_plus
    dx_settings_loader_path = cwd.joinpath("dx-settings-loader")
    try:
        repo = git.Repo.clone_from("https://github.com/hmxmilohax/dx-settings-loader.git", dx_settings_loader_path, branch="main")
        print("Successfully Downloaded DX Settings Loader...")
    except:
        repo = git.Repo(dx_settings_loader_path)
        origin = repo.remotes.origin
        origin.pull()
        print("Successfully Downloaded DX Settings Loader...")

if __name__ == "__main__":
    download_loader()