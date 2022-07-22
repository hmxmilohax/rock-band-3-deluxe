# add_moggs.py
from pathlib import Path

# get the current working directory
cwd = Path().absolute()

# check if moggs_keys exists, if not, exit the program
mogg_folder = cwd.joinpath("moggs_keys")
if not mogg_folder.is_dir():
    print("ERROR: moggs_keys folder not found. Place the moggs_keys folder in this directory and try again.")
else:
    songs_folder = cwd.joinpath("_ark/songs")
    song_updates_folder = cwd.joinpath("_ark/songs/updates")
    mogg_count = 0
    # for every mogg in the moggs_keys folder
    for mogg in mogg_folder.glob("*"):
        mogg_count += 1
        # insert the mogg into the respective song's update folder
        shortname = mogg.name.replace("_update.mogg","")
        song_update_path = song_updates_folder.joinpath(shortname)
        mogg.rename(song_update_path/mogg.name)

    # uncomment the ADDED_MOGGS line
    macros_path = cwd.joinpath("_ark/config/macros.dta")
    macro_contents = []
    
    macro_contents = [line for line in open(macros_path,"r")]
    for i in range(len(macro_contents)):
        if "ADDED_MOGGS" in macro_contents[i]:
            macro_contents[i] = macro_contents[i].replace("; #define","#define")
            break
            
    with open(macros_path,"w") as f:
        f.writelines(macro_contents)

    print(f"Successfully moved {mogg_count} moggs into the RB3DX ark. Please rebuild in order to see these changes reflected in-game.")
