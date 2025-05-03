from pathlib import Path
import sys

directory = Path(sys.argv[1])

if not directory.is_dir():
    raise Exception("not a directory")

out_path = sys.argv[2]

f = open(out_path, "w")
for dir in directory.glob("*/"):
    f.write(f"({dir.stem}\n#include {dir.stem}/theme.dta \n)\n")

f.close()