# add_rb3_plus_keys.py
from pathlib import Path
from parse_song_dta import parse_song_dta
from song_dict_to_dta import song_dict_to_dta
from pull_repo import pull_repo
import subprocess
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

# clone/pull rb3_plus
rb3_plus_path = pull_repo(repo_url="https://github.com/rjkiv/rb3_plus.git", repo_path=cwd)

merged_songs = {}

song_update_path = root_dir.joinpath("_ark/songs/updates")
venue_update_dta = []

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
            merged_songs[pro_song.stem]["extra_authoring"] = "disc_update"
            venue_update_dta.append(f"({pro_song.stem} (version 30))\n")          
        elif pro_file.suffix == ".mid":
            # print(pro_file.name)
            key_midi = MidiFile(pro_file)
            upd_midi = MidiFile()
            final_midi = MidiFile()

            # check the songs/updates folder for an _update.mid
            # if one exists:
            if song_update_path.joinpath(f"{pro_song.stem}/{pro_song.stem}_update.mid").is_file():
                # print(f"{pro_song.stem} - mid file exists")
                upd_midi = MidiFile(song_update_path.joinpath(f"{pro_song.stem}/{pro_song.stem}_update.mid"))
                for track in upd_midi.tracks:
                    if "KEYS" not in track.name and "VENUE" not in track.name:
                        final_midi.tracks.append(track)
                for track in key_midi.tracks:
                    if pro_song.stem not in track.name:
                        final_midi.tracks.append(track)
                        # we duplicate the real keys tracks to avoid oddities where key charts sometimes don't load
                        # blame RB3 for this, not me
                        if "REAL_KEYS" in track.name:
                            final_midi.tracks.append(track)
                final_midi.save(song_update_path.joinpath(f"{pro_song.stem}/{pro_song.stem}_update.mid"))
            else:
                # print(f"{pro_song.stem} - mid file does not exist")
                for track in key_midi.tracks:
                    final_midi.tracks.append(track)
                    # we duplicate the real keys tracks to avoid oddities where key charts sometimes don't load
                    # blame RB3 for this, not me
                    if "REAL_KEYS" in track.name:
                        final_midi.tracks.append(track)
                song_update_path.joinpath(f"{pro_song.stem}").mkdir(parents=True, exist_ok=True)
                final_midi.save(song_update_path.joinpath(f"{pro_song.stem}/{pro_song.stem}_update.mid"))
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

print(f"Successfully enabled key upgrades on the Rock Band 3 Deluxe ark. Please rebuild in order to see them reflected in-game.")