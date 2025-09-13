from pathlib import Path
import subprocess
import sys


path = sys.argv[1]

f = open(path, "w")

if len(sys.argv) > 2:
    for i in range(2, len(sys.argv)):
        f.write(f"#define {sys.argv[i]} (1)\n")

f.close()