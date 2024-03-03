# add_devbuild.py
from pathlib import Path
import subprocess
import sys


commit = subprocess.check_output(["git", "describe", "--always", "--dirty"],text=True).strip("\n")

version = "1.1.0-nightly+{commit}"

print(f'(message_motd "Rock Band 3 Deluxe 1.1.0-nightly+{commit} Loaded! Thanks for playing!")')
print(f'(message_motd_signin "Rock Band 3 Deluxe 1.1.0-nightly+{commit} Loaded! Thanks for playing!")')
print(f'(message_motd_noconnection "Rock Band 3 Deluxe 1.1.0-nightly+{commit} Loaded! Thanks for playing!")')
print(f'(rb3e_mod_string "RB3DX 1.1.0-nightly+{commit}")')