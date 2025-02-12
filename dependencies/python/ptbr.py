#!/usr/bin/env python3

import re

file_path = "_ark/dx/macros/dx_macros.dta"

# Read the entire file
with open(file_path, "r") as f:
    content = f.read()

# Replace the line that begins with optional whitespace, then a semicolon, then "#define DX_PTBR (1)"
content = re.sub(r'(?m)^[ \t]*;#define DX_PTBR \(1\)', '#define DX_PTBR (1)', content)

# Write back the modified content
with open(file_path, "w") as f:
    f.write(content)

# Translate gen_version.py
gen_version_path = "dependencies/python/gen_version.py"
gen_version_content = []

with open(gen_version_path, "r") as f:
    gen_version_content = f.readlines()
        
with open(gen_version_path, "w") as f:
    for line in gen_version_content:
        if line.startswith("f.write(f'(message_motd"):
            f.write('f.write(f\'(message_motd "Rock Band 3 Deluxe {version} Carregado! Obrigado por jogar!")\')\n')
        elif line.startswith("f.write(f'(message_motd_signin"):
            f.write('f.write(f\'(message_motd_signin "Rock Band 3 Deluxe {version} Carregado! Obrigado por jogar!")\')\n')
        elif line.startswith("f.write(f'(message_motd_noconnection"):
            f.write('f.write(f\'(message_motd_noconnection "Rock Band 3 Deluxe {version} Carregado! Obrigado por jogar!")\')\n')
        else:
            f.write(f"{line}")