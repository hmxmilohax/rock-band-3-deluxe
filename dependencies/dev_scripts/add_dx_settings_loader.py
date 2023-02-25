# add_rb3_plus_pro_strings.py
from pathlib import Path
from pull_repo import pull_repo
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

    # clone/pull dx_settings_loader_path
    dx_settings_loader_path = pull_repo(repo_url="https://github.com/hmxmilohax/dx-settings-loader.git", repo_path=cwd)

if __name__ == "__main__":
    download_loader()