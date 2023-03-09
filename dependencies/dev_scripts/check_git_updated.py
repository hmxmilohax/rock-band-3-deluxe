from pathlib import Path
from sys import platform
import subprocess

# pass in the repo url, and the path in which to look for .git/refs/heads
# will return True if the repo is up to date, False if a pull is needed
def check_git_updated(repo_url: str, repo_root_path: Path) -> bool:
    repo_name = repo_url.split("/")
    repo_name = repo_name[-1].replace(".git","")

    print(f"Checking for new updates from repo {repo_name}...")

    # retrieve current commit and compare against latest
    if repo_root_path.joinpath(".git/refs/heads/main").is_file():
        with open(repo_root_path.joinpath(".git/refs/heads/main"),"r") as g:
            local_commit = g.read()
    elif repo_root_path.joinpath(".git/refs/heads/master").is_file():
        with open(repo_root_path.joinpath(".git/refs/heads/master"),"r") as g:
            local_commit = g.read()
    else:
        return False
    local_commit = local_commit.strip()

    cmd_get_latest_commit = f"git ls-remote {repo_url} HEAD".split()
    latest_commit =  subprocess.check_output(cmd_get_latest_commit, shell=(platform == "win32"), cwd="..")
    latest_commit = latest_commit.decode()
    latest_commit = latest_commit.replace("HEAD","").strip()

    print(f"Local commit: {local_commit}")
    print(f"Latest commit: {latest_commit}")

    return (local_commit == latest_commit)