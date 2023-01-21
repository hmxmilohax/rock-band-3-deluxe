# git_reset.py
from pathlib import Path
import subprocess

# get current working directory (user_scripts)
cwd = Path().absolute()

# get the root directory of the repo
root_dir = Path(__file__).parents[1]
cmd_reset = "git reset --hard".split()
subprocess.run(cmd_reset)