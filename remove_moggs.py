# add_moggs.py
from pathlib import Path

# get the current working directory
cwd = Path().absolute()

mogg_count = 0

# start at the songs updates folder, and find moggs
song_updates_folder = cwd.joinpath("_ark/songs/updates")
for path in song_updates_folder.rglob("*/*.mogg"):
    print(path)
    path.unlink(missing_ok=True)
    mogg_count += 1

# comment the ADDED_MOGGS line
macros_path = cwd.joinpath("_ark/config/macros.dta")
macro_contents = []

macro_contents = [line for line in open(macros_path,"r")]
for i in range(len(macro_contents)):
    if "ADDED_MOGGS" in macro_contents[i]:
        if "; #define" not in macro_contents[i]:
            macro_contents[i] = "; " + macro_contents[i]
        break

with open(macros_path,"w") as f:
    f.writelines(macro_contents)

print(f"Successfully removed {mogg_count} moggs from the RB3DX ark. Please rebuild in order to see these changes reflected in-game.")
