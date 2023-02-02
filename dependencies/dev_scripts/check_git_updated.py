from pathlib import Path
from sys import platform
import subprocess

def check_git_updated() -> bool:

    cwd = Path().absolute() # current working directory (dev_scripts)
    root_dir = cwd.parents[0] # root directory of the repo

    # retrieve current commit and compare against latest
    with open(root_dir.joinpath(".git/refs/heads/main"),"r") as g:
        local_commit = g.read()
    local_commit = local_commit.strip()

    cmd_get_latest_commit = "git ls-remote https://github.com/hmxmilohax/rock-band-3-deluxe.git HEAD".split()
    latest_commit =  subprocess.check_output(cmd_get_latest_commit, shell=(platform == "win32"), cwd="..")
    latest_commit = latest_commit.decode()
    latest_commit = latest_commit.replace("HEAD","").strip()

    # print(latest_commit)
    # print(local_commit)

    return (local_commit == latest_commit)