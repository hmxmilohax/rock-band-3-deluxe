# add_rb3_plus_keys.py
from pathlib import Path
from mido import MidiFile
from parse_song_dta import parse_song_dta
from song_dict_to_dta import song_dict_to_dta
import git

print("Downloading/enabling additional rb3_plus song data, this may take some time.")
    
# get the current working directory
cwd = Path().absolute()
# get the root directory of the repo
root_dir = Path(__file__).parents[2]
print(root_dir)

# clone/pull rb3_plus
rb3_plus_path = cwd.joinpath("rb3_plus")
try:
    repo = git.Repo.clone_from("https://github.com/rjkiv/rb3_plus.git", rb3_plus_path, branch="main")
except:
    repo = git.Repo(rb3_plus_path)
    origin = repo.remotes.origin
    origin.pull()

merged_songs = {}

song_update_path = root_dir.joinpath("_ark/songs/updates")

# traverse through rb3_plus/Pro Keys and find mid, mogg, and songs.dta
for pro_song in rb3_plus_path.glob("Pro Keys/*/*"):
    print(pro_song.stem)
    for pro_file in pro_song.glob("*"):
        if pro_file.name == "songs.dta":
            print(pro_file.name)
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
            merged_songs[pro_song.stem]["version"] = 30
            merged_songs[pro_song.stem]["extra_authoring"] = "disc_update"
        elif pro_file.suffix == ".mid":
            print(pro_file.name)
            final_midi = MidiFile()
            # if an update mid exists, append the key tracks to it
            if root_dir.joinpath(f"_ark/songs/updates/{pro_song.stem}/{pro_song.stem}_update.mid").is_file():
                print("this song has an update file, will merge")
                old_upd_midi = MidiFile(root_dir.joinpath(f"_ark/songs/updates/{pro_song.stem}/{pro_song.stem}_update.mid"))
                # for track in combined_mid.tracks:
                #     print(track.name)
                for track in old_upd_midi.tracks:
                    final_midi.tracks.append(track)
                keys_mid = MidiFile(pro_file)
                for track in keys_mid.tracks:
                    if pro_song.stem not in track.name:
                        # print(track.name)
                        final_midi.tracks.append(track)
                        if "REAL_KEYS" in track.name:
                            final_midi.tracks.append(track)
                final_midi.save(root_dir.joinpath(f"_ark/songs/updates/{pro_song.stem}/{pro_song.stem}_update.mid"))
            # else, just straight up copy the mid to the update location
            else:
                print("This song does not have an update file - will copy the _plus mid directly into the update location")
                for track in MidiFile(pro_file).tracks:
                    final_midi.tracks.append(track)
                    if "REAL_KEYS" in track.name:
                        final_midi.tracks.append(track)
                root_dir.joinpath(f"_ark/songs/updates/{pro_song.stem}").mkdir(parents=True, exist_ok=True)
                final_midi.save(root_dir.joinpath(f"_ark/songs/updates/{pro_song.stem}/{pro_song.stem}_update.mid"))
        elif pro_file.suffix == ".mogg":
            print(pro_file.name)
            root_dir.joinpath(f"_ark/songs/updates/{pro_song.stem}").mkdir(parents=True, exist_ok=True)
            destination_path = root_dir.joinpath(f"_ark/songs/updates/{pro_song.stem}/{pro_song.stem}_update.mogg")
            destination_path.write_bytes(pro_file.read_bytes())

    # for line in song_dict_to_dta(merged_songs):
    #     print(line)

with open(root_dir.joinpath(f"_ark/songs/dta_sections/keys.dta"), "w") as fff:
    for line in song_dict_to_dta(merged_songs):
        fff.write(f"{line}\n")

missing_song_data_path = root_dir.joinpath("_ark/songs/missing_song_data.dta")
missing_song_data = [line for line in open(missing_song_data_path, "r")]

# uncomment keys.dta
overwritten = False
for i in range(len(missing_song_data)):
    if ";#include dta_sections/keys.dta" in missing_song_data[i]:
        missing_song_data[i] = missing_song_data[i].replace(";#include", "#include")
        overwritten = True
        break

if overwritten:
    with open(missing_song_data_path, "w") as f:
        f.writelines(missing_song_data)