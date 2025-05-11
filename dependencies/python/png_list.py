from pathlib import Path
import sys

directory = Path(sys.argv[1])

if not directory.is_dir():
    raise Exception("not a directory")

out_path = sys.argv[2]

f = open(out_path, "w")
for file in sorted(directory.glob("*")):
    if file.name != ".DS_Store":
        f.write(f"'{file.stem}'\n")

f.close()