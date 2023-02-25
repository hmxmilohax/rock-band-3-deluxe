# git_reset.py
import subprocess

cmd_reset = "git reset --hard".split()
subprocess.run(cmd_reset)

cmd_pull = "git pull".split()
subprocess.run(cmd_pull)