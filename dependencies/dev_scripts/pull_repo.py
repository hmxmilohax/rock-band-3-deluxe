# pull_repo.py
from pathlib import Path
try:
    import git
except:
    cmd_install = "pip install gitpython".split()
    subprocess.run(cmd_install)

# pass in the repo url and repo path, and this function will clone/pull from said repo
# with the repo contents going in repo_path/(name of repo)
# will return a Path object directed to (name of repo)
def pull_repo(repo_url: str, repo_path: Path) -> Path:
    repo_name = repo_url.split("/")
    repo_name = repo_name[-1].replace(".git","")
    print(f"Pulling from repo {repo_name} - this may take some time.")
    
    # clone/pull the repo
    repo_pull_path = repo_path.joinpath(f"{repo_name}")
    try:
        repo = git.Repo.clone_from(repo_url, repo_pull_path, branch="main")
    except:
        repo = git.Repo(repo_pull_path)
        origin = repo.remotes.origin
        origin.pull()

    print(f"Contents from repo {repo_name} successfully pulled.")
    return repo_pull_path

def main():
    pull_repo(repo_url="https://github.com/rjkiv/rb3_plus.git", repo_path=Path(__file__).parent)

if __name__ == "__main__":
    main()