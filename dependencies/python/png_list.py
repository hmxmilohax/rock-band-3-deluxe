from pathlib import Path
import sys

directory = Path(sys.argv[1])
out_path = sys.argv[2]

f = open(out_path, "w")
for file in directory.glob("*"):
    f.write(f"'{file.stem}'\n")

f.close()