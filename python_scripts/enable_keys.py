# enable_keys.py
from pathlib import Path
import git

# get the current working directory
cwd = Path().absolute()

# clone/pull rb3_plus
rb3_plus_path = cwd.joinpath("rb3_plus")
try:
    repo = git.Repo.clone_from("https://github.com/rjkiv/rb3_plus.git", rb3_plus_path, branch="main")
except:
    repo = git.Repo(rb3_plus_path)
    origin = repo.remotes.origin
    origin.pull()

song_updates_folder = cwd.joinpath("_ark/songs/updates")
# traverse through the repo and find the moggs
for mogg in rb3_plus_path.glob("Pro Keys/*/*/*.mogg"):
    # insert the mogg into the respective song's update folder
    shortname = mogg.name.replace(".mogg","")
    mogg_update = shortname + "_update.mogg"
    song_update_path = song_updates_folder.joinpath(shortname)
    mogg_update_path = song_update_path.joinpath(mogg_update)
    mogg_update_path.write_bytes(mogg.read_bytes())

# uncomment the ADDED_MOGGS line
macros_path = cwd.joinpath("_ark/config/macros.dta")
macro_contents = []

macro_contents = [line for line in open(macros_path,"r")]
for i in range(len(macro_contents)):
    if "KEYS_ENABLED" in macro_contents[i]:
        macro_contents[i] = macro_contents[i].replace("; #define","#define")
        break
        
with open(macros_path,"w") as f:
    f.writelines(macro_contents)

print(f"Successfully enabled key upgrades on the RB3DX ark. Please rebuild in order to see them reflected in-game.")
