# remove_rb3_plus_keys.py
from pathlib import Path
# Check if mido is installed and install it if necessary
try:
    import mido
    from mido import MidiFile
except ImportError:
    subprocess.check_call(["python", "-m", "pip", "install", "mido"])
    import mido
    from mido import MidiFile
# Check if git is installed and install it if necessary
try:
    import git
except ImportError:
    subprocess.check_call(["python", "-m", "pip", "install", "gitpython"])
    import git
    
# get the current working directory
cwd = Path(__file__).parent
# print(cwd)
# get the root directory of the repo
root_dir = Path(__file__).parents[2]
# print(root_dir)

merged_songs = {}

song_update_path = root_dir.joinpath("_ark/songs/updates")
key_dta_path = root_dir.joinpath("_ark/songs/dta_sections/keys.dta")
key_venue_dta_path = root_dir.joinpath("_ark/songs/dta_sections/key_venue_updates.dta")

# for each shortname in key_venue_updates.dta:
venue_update_dta = [line for line in open(key_venue_dta_path,"r")]
for song in venue_update_dta:
    shortname = song.strip("(").split()[0]
    # print(shortname)
    shortname_update_path = song_update_path.joinpath(shortname)
    # delete that song's mogg
    if shortname_update_path.joinpath(f"{shortname}_update.mogg").is_file():
        shortname_update_path.joinpath(f"{shortname}_update.mogg").unlink()
    # revert that song's update midi so no keys stuff is in there
    if shortname_update_path.joinpath(f"{shortname}_update.mid").is_file():
        upd_midi = MidiFile(shortname_update_path.joinpath(f"{shortname}_update.mid"))
        final_midi = MidiFile()
        non_key_track_cnt = 0
        for track in upd_midi.tracks:
            if "KEYS" not in track.name and "VENUE" not in track.name:
                non_key_track_cnt += 1
                final_midi.tracks.append(track)
        # if there was ONLY keys stuff in the update midi, just delete the update midi outright
        if non_key_track_cnt == 1:
            shortname_update_path.joinpath(f"{shortname}_update.mid").unlink()
        else:
            final_midi.save(shortname_update_path.joinpath(f"{shortname}_update.mid"))
    # if this then results in an empty song update folder, delete that as well
    try:
        shortname_update_path.rmdir()
    except:
        pass

# when all the above is done, delete the contents of keys.dta and key_venue_updates.dta
with open(key_dta_path,"w") as k:
    k.write("")

with open(key_venue_dta_path, "w") as kk:
    kk.write("")

print(f"Successfully disabled key upgrades on the Rock Band 3 Deluxe ark. Please rebuild in order to see them reflected in-game.")