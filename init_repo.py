import os
import sys
import subprocess
from pathlib import Path
import time
import random
import platform
import re
import argparse

def install_python_packages():
    packages = ["requests", "gitpython", "mido"]
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    print("Python packages installed successfully")

def get_pip_command():
    try:
        subprocess.check_call([sys.executable, "-m", "pip3", "--version"])
        return "pip3"
    except subprocess.CalledProcessError:
        pass

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"])
        return "pip"
    except subprocess.CalledProcessError:
        pass

    return None

def install_pip():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"])
        print("pip is already installed.")
    except subprocess.CalledProcessError:
        print("pip is not installed. Installing pip...")
        if os.name == "nt":  # Running on Windows
            subprocess.check_call([sys.executable, "get-pip.py"])
        else:  # Running on Linux or macOS
            subprocess.check_call([sys.executable, "-m", "ensurepip"])
        print("pip installed successfully.")

def upgrade_pip(pip_command):
    try:
        print(f"Upgrading {pip_command}...")
        subprocess.check_call([sys.executable, "-m", pip_command, "install", "--upgrade", "pip"])
        print(f"{pip_command} upgraded successfully")
    except subprocess.CalledProcessError:
        print(f"Failed to upgrade {pip_command}. Continuing with the current version.")

def install_dotnet_runtime():
    if os.name == "nt":  # Running on Windows
        command = "winget install Microsoft.DotNet.DesktopRuntime.6"
        print(f"Installing .NET Desktop Runtime 6: running '{command}'")
        subprocess.call(command, shell=True)
    elif platform.system() == "Darwin":  # Running on macOS
        commands = [
            "brew update",
            "brew install --cask dotnet"
        ]
    else:  # Running on Linux
        with open("/etc/os-release") as os_release_file:
            os_release_data = os_release_file.read().lower()

        if "arch" in os_release_data:
            commands = [
                "sudo pacman -Syyu --noconfirm",
                "sudo pacman -S dotnet-runtime --noconfirm",
            ]
        else:  # Ubuntu
            commands = [
                "wget https://packages.microsoft.com/ubuntu/20.04/prod/pool/main/a/aspnetcore-runtime-6.0/aspnetcore-runtime-6.0.14-x64.deb",
                "sudo dpkg -i aspnetcore-runtime-6.0.14-x64.deb",
                "rm aspnetcore-runtime-6.0.14-x64.deb",
                "sudo apt-get install -y dotnet-runtime-6.0",
            ]
        for command in commands:
            print(f"Running '{command}'")
            subprocess.call(command, shell=True)

def install_git_cli():
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True)
        if "git version" in result.stdout:
            print("Git is already installed.")
            return True
    except FileNotFoundError:
        pass

    if os.name == "nt":
        print("Git is not installed. Installing now...")

        command = 'winget install --id Git.Git -e --source winget --silent'
        print(f"Running '{command}'")
        subprocess.check_call(command, shell=True)

        print("Git installed. Please close this cmd window and run the script again.")
        return False
    elif platform.system() == "Darwin":  # Running on macOS
        try:
            subprocess.check_call(["brew", "install", "git"])
            print("Git installed successfully.")
            return True
        except subprocess.CalledProcessError:
            print("Error installing Git. Please install Git manually and run the script again.")
            return False
    else:
        print("Git is not installed. Please install git and run the script again.")
        return False

last_reminder_time = time.time()

projects = [
    "Guitar Hero 1 Deluxe",
    "Guitar Hero 2 Deluxe",
    "Guitar Hero Encore: Rocks The 80's Deluxe",
    "Rock Band 1 Deluxe",
    "Rock Band 2 Deluxe",
    "Rock Band 3 Deluxe",
    "Rock Band 4 Deluxe",
    "LEGO Rock Band Deluxe",
    "The Beatles Rock Band Deluxe",
    "Green Day Rock Band Deluxe",
    "Amplitude (2016) Deluxe",
    "Amplitude (2003) Deluxe",
    "Dance Central 1 Deluxe",
    "Karaoke Revolution Party Deluxe",
    "DX Settings Loader",
]

shown_projects = []

def get_next_project():
    global projects, shown_projects
    if not shown_projects or len(shown_projects) == len(projects):
        shown_projects = random.sample(projects, len(projects))
    next_project = shown_projects.pop(0)
    return next_project

def fetch_progress(op_code, cur_count, max_count=None, message=""):
    global last_reminder_time
    if message:
        try:
            # Use regex to extract transferred and rate values from the message
            transferred_match = re.search(r"(\d+(\.\d+)?\s(?:GiB|KiB|MiB))", message)
            rate_match = re.search(r"(\d+(\.\d+)?\s(?:GiB|KiB|MiB)/s)", message)

            if transferred_match and rate_match:
                transferred = transferred_match.group(0)
                rate = rate_match.group(0)

                formatted_message = f"{repo_name}: {transferred} | {rate}"
                print(formatted_message)

            current_time = time.time()
            if current_time - last_reminder_time >= 15:
                next_project = get_next_project()
                print(f"Reminder: Don't forget to play {next_project}!")
                last_reminder_time = current_time
        except IndexError:
            # Skip printing if the message format is unexpected
            pass

def git_init_pull_repo(repo_url, repo_name, branch="main"):
    import git
    current_dir = Path().resolve()

    # Check if the current directory contains only the init_repo.py script
    current_dir_files = list(Path(current_dir).iterdir())
    if len(current_dir_files) == 1 and current_dir_files[0].name == "init_repo.py":
        target_dir = current_dir
    else:
        target_dir = current_dir / repo_name
        if not target_dir.exists():
            target_dir.mkdir()

    git_dir = target_dir / ".git"
    if git_dir.exists():
        print("Found an existing .git directory. Resetting the repository...")
        repo = git.Repo(target_dir)
        repo.git.reset("--hard")
        origin = repo.remote("origin")
        # Create the branch if it does not exist
        if branch not in repo.branches:
            repo.git.checkout("-b", branch)
        # Set the upstream branch
        repo.git.branch(f"--set-upstream-to={origin}/{branch}", branch)
        repo.git.pull()
        print(f"Reset and pulled the '{branch}' branch of '{repo_url}' into the '{target_dir}'")
    else:
        # Initialize the git repository
        repo = git.Repo.init(target_dir)
        print(f"Initialized git repository, cloning {repo_url}")

        # Configure a dummy user for the repository
        repo.config_writer().set_value("user", "email", "you@example.com").release()
        repo.config_writer().set_value("user", "name", "Your Name").release()

        # Pull the repository
        origin = repo.create_remote("origin", repo_url)
        origin.fetch(progress=fetch_progress)
        origin.pull(branch)
        print(f"Pulled '{branch}' branch of '{repo_url}' into the '{target_dir}'")

if __name__ == "__main__":
    try:
        install_pip()
        pip_command = get_pip_command()
        upgrade_pip(pip_command)
        install_dotnet_runtime()
        install_python_packages()
        if "SKIP_GIT_INSTALL" not in os.environ:
            git_installed = install_git_cli()
            if not git_installed:
                sys.exit(0)
        repo_url = "https://github.com/hmxmilohax/rock-band-3-deluxe"
        repo_name = "rock-band-3-deluxe"
        git_init_pull_repo(repo_url, repo_name)
    except Exception as e:
        print(f"An error occurred: {e}")