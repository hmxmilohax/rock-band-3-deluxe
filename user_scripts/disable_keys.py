# disable_keys.py
from pathlib import Path

cwd = Path().absolute()
root_dir = cwd.parent

dta_section_path = root_dir.joinpath("_ark/songs/dta_sections")

# delete the contents of keys.dta and key_venue_updates.dta
with open(dta_section_path.joinpath("keys.dta"),"w") as k:
    k.write("")

with open(dta_section_path.joinpath("key_venue_updates.dta"),"w") as kk:
    kk.write("")

# delete any moggs in the update folder
song_update_path = root_dir.joinpath("_ark/songs/updates")
for filename in song_update_path.glob("*/*.mogg"):
    filename.unlink()
    # and if this then results in an empty folder, delete that as well
    try:
        filename.parent.rmdir()
    except:
        pass

print(f"Successfully disabled key upgrades on the RB3DX ark. Please rebuild in order to see them reflected in-game.")