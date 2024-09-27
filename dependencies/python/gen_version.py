# add_devbuild.py
import sys

version = f"1.1.0-beta12"

path = sys.argv[1]

f = open(path, "w")

f.write(f'(message_motd "Rock Band 3 Deluxe {version} Loaded! Thanks for playing!")\n')
f.write(f'(message_motd_signin "Rock Band 3 Deluxe {version} Loaded! Thanks for playing!")\n')
f.write(f'(message_motd_noconnection "Rock Band 3 Deluxe {version} Loaded! Thanks for playing!")\n')
f.write(f'(rb3e_mod_string "RB3DX {version}")\n')

f.close()