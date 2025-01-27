#!/usr/bin/env python3

import re
import os

# Resolve the file path and print the current working directory
file_path = os.path.abspath("_ark/dx/macros/dx_macros.dta")
print("Resolved File Path:", file_path)
print("Current Working Directory:", os.getcwd())

# Check if the file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

# Read the entire file with explicit UTF-8 encoding
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Debug: Print the original content
print("Original Content:\n", content)

# Replace the line that begins with optional whitespace, then a semicolon, then "#define DX_PTBR (1)"
# Handles both Linux (\n) and Windows (\r\n) line endings
content = re.sub(r'(?m)^[ \t]*;#define DX_PTBR \(1\)\r?$', '#define DX_PTBR (1)', content)

# Debug: Print the modified content
print("Modified Content:\n", content)

# Write back the modified content with explicit UTF-8 encoding
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Uncommenting completed successfully!")
