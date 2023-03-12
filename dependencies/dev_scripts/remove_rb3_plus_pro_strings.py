# remove_rb3_plus_pro_strings.py
from pathlib import Path

def rm_tree(pth):
    pth = Path(pth)
    for child in pth.glob('*'):
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()

# get the current working directory
cwd = Path(__file__).parent
# print(cwd)
# get the root directory of the repo
root_dir = Path(__file__).parents[2]

song_upgrade_path = root_dir.joinpath("_ark/songs_upgrades")

# remove the rb3_plus folder in songs_upgrades
try:
    rm_tree(song_upgrade_path.joinpath("rb3_plus"))
except:
    pass

with open(song_upgrade_path.joinpath("rb3_plus.dta"), "w") as f:
    f.write("")

print(f"Successfully disabled rb3_plus pro string upgrades on the Rock Band 3 Deluxe ark.")