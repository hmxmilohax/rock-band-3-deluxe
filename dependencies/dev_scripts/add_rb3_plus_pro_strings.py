# give_3dx_pro_strings.py
from pathlib import Path
from mido import MidiFile
from parse_song_dta import parse_song_dta
import json
import git

def integrate_rb3_plus():

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

    # load all the legacy song info from the pre-compiled json file
    with open(root_dir.joinpath("dependencies/song_info.json")) as json_file:
        all_the_song_info = json.load(json_file)

    merged_songs = {}

    # traverse through rb3_plus/Pro Strings and find both _plus.mid and upgrades.dta
    for pro_song in rb3_plus_path.glob("Pro Strings/*/*"):
        print(pro_song.stem)
        for pro_file in pro_song.glob("*"):
            # if working with a dta, parse it, and merge it with song info from the mega dta
            if pro_file.name == "upgrades.dta":
                upgrade_dict = parse_song_dta(pro_file)
                original_song_dict = all_the_song_info["songs"][pro_song.stem]
                merged_songs[pro_song.stem] = {}
                merged_songs[pro_song.stem]["rank"] = original_song_dict["rank"] | upgrade_dict["songs"][pro_song.stem]["rank"]
                merged_songs[pro_song.stem]["real_guitar_tuning"] = upgrade_dict["songs"][pro_song.stem]["real_guitar_tuning"]
                merged_songs[pro_song.stem]["real_bass_tuning"] = upgrade_dict["songs"][pro_song.stem]["real_bass_tuning"]
                merged_songs[pro_song.stem]["extra_authoring"] = "disc_update"
            # if working with a mid, 
            elif "_plus.mid" in pro_file.name:
                print(pro_file.name)
                # if an update mid in the ark exists, merge the pro upgrade mid with it
                if root_dir.joinpath(f"_ark/songs/updates/{pro_song.stem}/{pro_song.stem}_update.mid").is_file():
                    print("This song has an update file, will merge")
                    mid_original = MidiFile(root_dir.joinpath(f"_ark/songs/updates/{pro_song.stem}/{pro_song.stem}_update.mid"))
                    
                    mid_plus = MidiFile(pro_file)
                    mid_merged = MidiFile()

                    for track in mid_original.tracks:
                        if "PART REAL_GUITAR" not in track.name and "PART REAL_BASS" not in track.name:
                            mid_merged.tracks.append(track)
                            
                    for track in mid_plus.tracks:
                        if "PART REAL" in track.name:
                            mid_merged.tracks.append(track)

                    mid_merged.save(root_dir.joinpath(f"_ark/songs/updates/{pro_song.stem}/{pro_song.stem}_update.mid"))
                # otherwise, copy the mid from rb3_plus directly into the song update folder
                else:
                    print("This song does not have an update file - will copy the _plus mid directly into the update location")
                    root_dir.joinpath(f"_ark/songs/updates/{pro_song.stem}").mkdir(parents=True, exist_ok=True)
                    destination_path = root_dir.joinpath(f"_ark/songs/updates/{pro_song.stem}/{pro_song.stem}_update.mid")
                    destination_path.write_bytes(pro_file.read_bytes())

    # # write the new upgrade dta info to the bottom of missing_song_data.dta
    # with open(root_dir.joinpath("_ark/songs/missing_song_data.dta"), "r", encoding="ISO-8859-1") as f:
    #     missing_dta = [line for line in f.readlines()]

    # rb3_plus_index = missing_dta.index("; rb3_plus pro strings upgrades - generated automatically\n")
    # missing_dta = missing_dta[:rb3_plus_index + 1]
        
    # generate dta to return
    return merged_songs

    rb3_plus_pro_dta = []
    rb3_plus_pro_dta.append("; rb3_plus pro string upgrades\n")

    for song in merged_songs.keys():
        rank_str = ""
        for rank in merged_songs[song]["rank"]:
            rank_str += f"({rank} {merged_songs[song]['rank'][rank]}) "

        rb3_plus_pro_dta.append(f"({song} (rank {rank_str})\n")
        rb3_plus_pro_dta.append(f"\t(real_guitar_tuning ({' '.join(str(x) for x in merged_songs[song]['real_guitar_tuning'])})) (real_bass_tuning ({' '.join(str(x) for x in merged_songs[song]['real_bass_tuning'])})) (extra_authoring disc_update))\n")

    # with open(root_dir.joinpath("_ark/songs/missing_song_data.dta"), "w", encoding="ISO-8859-1") as f:
    #     f.writelines(missing_dta)

    print(f"Successfully merged rb3_plus pro string upgrades into the RB3DX ark.")

    return rb3_plus_pro_dta
