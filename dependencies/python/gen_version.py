# add_devbuild.py
from pathlib import Path
import subprocess
import sys

branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"],text=True).strip("\n")
rev = subprocess.check_output(["git", "rev-list", "--count", "HEAD"],text=True).strip("\n")
commit = subprocess.check_output(["git", "describe", "--always", "--dirty"],text=True).strip("\n")

if branch == "develop":
    version = f"r{rev}+{commit}"
else:
    version = f"{branch}+{commit}"

path = sys.argv[1]

f = open(path, "w")

f.write(f'(message_motd "Rock Band 3 Deluxe r{rev} Loaded! Thanks for playing!")\n')
f.write(f'(message_motd_signin "Rock Band 3 Deluxe r{rev} Loaded! Thanks for playing!")\n')
f.write(f'(message_motd_noconnection "Rock Band 3 Deluxe r{rev} Loaded! Thanks for playing!")\n')
f.write(f'(rb3e_mod_string "RB3DX {version}")\n')

f.close()