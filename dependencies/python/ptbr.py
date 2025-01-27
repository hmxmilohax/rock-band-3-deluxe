#!/usr/bin/env python3

import re

file_path = os.path.abspath("_ark/dx/macros/dx_macros.dta")

import os
print("Current Working Directory:", os.getcwd())

# Read the entire file
with open(file_path, "r") as f:
    content = f.read()

# Replace the line that begins with optional whitespace, then a semicolon, then "#define DX_PTBR (1)"
content = re.sub(r'(?m)^[ \t]*;#define DX_PTBR \(1\)', '#define DX_PTBR (1)', content)

# Write back the modified content
with open(file_path, "w") as f:
    f.write(content)
