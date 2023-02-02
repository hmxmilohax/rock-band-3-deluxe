# run_xenia.py
import subprocess

cmd_xenia = "_xenia\\xenia_canary.exe _build\\xbox\\default_xenia.xex"
subprocess.run(cmd_xenia, shell=True, cwd="..")