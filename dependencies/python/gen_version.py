# add_devbuild.py
from pathlib import Path
import math
import subprocess
import sys

branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"],text=True).strip("\n")
commit = subprocess.check_output(["git", "describe", "--always", "--dirty"],text=True).strip("\n")

# revision number is number of days since jan 9, 2022 (rb3dx's initial commit)
epoch = 1641743933
now = int(subprocess.check_output(["git", "show", "--no-patch", "--format=%at"],text=True).strip("\n"))
rev = math.floor((now - epoch) / 86400)

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
f.write(f'(rb3dx_commit "{commit}")\n')
f.write(f'(rb3dx_version "{version}")\n')

f.close()