# add_rb3_plus_keys.py
from pathlib import Path
from parse_song_dta import parse_song_dta
from song_dict_to_dta import song_dict_to_dta
from add_rb3_plus_pro_strings import add_strings
from pull_repo import pull_repo
import json
import subprocess
try:
    import mido
    from mido import MidiFile
except:
    cmd_mido = "pip install mido".split()
    subprocess.run(cmd_mido)
try:
    import git
except:
    cmd_install = "pip install gitpython".split()
    subprocess.run(cmd_install)

add_strings()
    
# get the current working directory
cwd = Path(__file__).parent
# print(cwd)
# get the root directory of the repo
root_dir = Path(__file__).parents[2]
# print(root_dir)

# clone/pull rb3_plus
rb3_plus_path = pull_repo(repo_url="https://github.com/rjkiv/rb3_plus.git", repo_path=cwd)

# load all the legacy song info from the pre-compiled json file
with open(root_dir.joinpath("dependencies/song_info.json")) as json_file:
    all_the_song_info = json.load(json_file)

vanilla_dta = parse_song_dta(root_dir.joinpath("_ark/songs/dta_sections/vanilla.dta"))

merged_songs = {}

song_update_path = root_dir.joinpath("_ark/songs/updates")
song_upgrade_path = root_dir.joinpath("_ark/songs_upgrades/rb3_plus.dta")
song_upgrade_dta = [line for line in open(song_upgrade_path, "r")]
overwrite_rb3_plus_dta = False
venue_update_dta = []

def shortname_upgrade_check(shortname: str):
    for line in song_upgrade_dta:
        if f"({shortname}" in line:
            return True
    return False

def get_song_id(shortname: str):
    if "song_id" in all_the_song_info["songs"][shortname]:
        return all_the_song_info["songs"][shortname]["song_id"]
    elif "song_id" in vanilla_dta['songs'][shortname]:
        return vanilla_dta['songs'][shortname]['song_id']
    else:
        print("ERROR: song id not found")
        exit()

# traverse through rb3_plus/Pro Keys and find mid, mogg, and songs.dta
for pro_song in rb3_plus_path.glob("Pro Keys/*/*"):
    # print(pro_song.stem)
    for pro_file in pro_song.glob("*"):
        if pro_file.name == "songs.dta":
            # print(pro_file.name)
            song_keys_dict = parse_song_dta(pro_file)
            # print(song_keys_dict)
            merged_songs[pro_song.stem] = {}
            merged_songs[pro_song.stem]["song"] = {}
            merged_songs[pro_song.stem]["song"]["tracks"] = song_keys_dict["songs"][pro_song.stem]["song"]["tracks"]
            if "crowd_channels" in song_keys_dict["songs"][pro_song.stem]["song"]:
                merged_songs[pro_song.stem]["song"]["crowd_channels"] = song_keys_dict["songs"][pro_song.stem]["song"]["crowd_channels"]
            merged_songs[pro_song.stem]["song"]["pans"] = song_keys_dict["songs"][pro_song.stem]["song"]["pans"]
            merged_songs[pro_song.stem]["song"]["vols"] = song_keys_dict["songs"][pro_song.stem]["song"]["vols"]
            merged_songs[pro_song.stem]["song"]["cores"] = song_keys_dict["songs"][pro_song.stem]["song"]["cores"]
            merged_songs[pro_song.stem]["rank"] = song_keys_dict["songs"][pro_song.stem]["rank"]
            venue_update_dta.append(f"({pro_song.stem} (version 30))\n")
            # if this song doesn't currently have an entry in rb3_plus.dta, add one
            if not shortname_upgrade_check(pro_song.stem):
                song_upgrade_dta.append(f"({pro_song.stem}\n   (upgrade_version 1)\n")
                song_upgrade_dta.append(f"   (midi_file \"songs_upgrades/rb3_plus/{pro_song.stem}_plus.mid\")\n")
                song_upgrade_dta.append(f"   (song_id {get_song_id(pro_song.stem)})\n)\n")
                overwrite_rb3_plus_dta = True               
        elif pro_file.suffix == ".mid":
            # print(pro_file.name)
            key_midi = MidiFile(pro_file)
            final_midi = MidiFile()
            # for track in key_midi.tracks:
            #     print(track.name)
            # if a _plus mid exists in the rb3_plus path, append the key tracks to it
            if root_dir.joinpath(f"_ark/songs_upgrades/rb3_plus/{pro_song.stem}_plus.mid").is_file():
                # print("this song has an upgrade file already - must merge")
                pro_str_midi = MidiFile(root_dir.joinpath(f"_ark/songs_upgrades/rb3_plus/{pro_song.stem}_plus.mid"))
                for track in pro_str_midi.tracks:
                    if "KEYS" not in track.name and "VENUE" not in track.name:
                        final_midi.tracks.append(track)
                    # print(track.name)
                for track in key_midi.tracks:
                    if pro_song.stem not in track.name:
                        final_midi.tracks.append(track)
                        # we duplicate the real keys tracks to avoid oddities where key charts sometimes don't load
                        # blame RB3 for this, not me
                        if "REAL_KEYS" in track.name:
                            final_midi.tracks.append(track)
                final_midi.save(root_dir.joinpath(f"_ark/songs_upgrades/rb3_plus/{pro_song.stem}_plus.mid"))
            # else, copy the _plus mid into it directly
            else:
                # print("this song doesn't have an upgrade file - will duplicate real key tracks and move file over")
                for track in key_midi.tracks:
                    final_midi.tracks.append(track)
                    # we duplicate the real keys tracks to avoid oddities where key charts sometimes don't load
                    # blame RB3 for this, not me
                    if "REAL_KEYS" in track.name:
                        final_midi.tracks.append(track)
                final_midi.save(root_dir.joinpath(f"_ark/songs_upgrades/rb3_plus/{pro_song.stem}_plus.mid"))
        elif pro_file.suffix == ".mogg":
            # print(pro_file.name)
            song_update_path.joinpath(pro_song.stem).mkdir(parents=True, exist_ok=True)
            destination_path = song_update_path.joinpath(f"{pro_song.stem}/{pro_song.stem}_update.mogg")
            destination_path.write_bytes(pro_file.read_bytes())

# add (version 30) to missing song updates to ensure we're using the new style venues
with open(root_dir.joinpath(f"_ark/songs/dta_sections/key_venue_updates.dta"), "w") as f_upd:
    f_upd.writelines(venue_update_dta)

with open(root_dir.joinpath(f"_ark/songs/dta_sections/keys.dta"), "w") as f:
    for line in song_dict_to_dta(merged_songs):
        f.write(f"{line}\n")

# overwrite rb3_plus.dta
if overwrite_rb3_plus_dta:
    with open(song_upgrade_path, "w") as f:
        f.writelines(song_upgrade_dta)

print(f"Successfully enabled key upgrades on the RB3DX ark. Please rebuild in order to see them reflected in-game.")