# add_rb3_plus_pro_strings.py
from pathlib import Path
import git

def add_strings():

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

    mega_upgrade_dta = []

    # traverse through rb3_plus/Pro Strings and find both _plus.mid and upgrades.dta
    for pro_song in rb3_plus_path.glob("Pro Strings/*/*"):
        print(pro_song.stem)
        for pro_file in pro_song.glob("*"):
            # if working with a dta, append it to the mega dta in here
            if pro_file.name == "upgrades.dta":
                mega_upgrade_dta.extend([line for line in open(pro_file, "r")])
                mega_upgrade_dta.append("\n")
            # if working with a mid, copy it
            elif "_plus.mid" in pro_file.name:
                # copy the mid from rb3_plus directly into the song update folder
                root_dir.joinpath(f"_ark/songs_upgrades/rb3_plus").mkdir(parents=True, exist_ok=True)
                destination_path = root_dir.joinpath(f"_ark/songs_upgrades/rb3_plus/{pro_file.name}")
                destination_path.write_bytes(pro_file.read_bytes())

    for i in range(len(mega_upgrade_dta)):
        if "(midi_file \"songs_upgrades/" in mega_upgrade_dta[i]:
            mega_upgrade_dta[i] = mega_upgrade_dta[i].replace("songs_upgrades/", "songs_upgrades/rb3_plus/")

    with open(root_dir.joinpath(f"_ark/songs_upgrades/rb3_plus.dta"), "w") as f:
        f.writelines(mega_upgrade_dta)

    with open(root_dir.joinpath(f"_ark/songs_upgrades/upgrades.dta"), "w") as ff:
        ff.write("#include vanilla.dta\n")
        ff.write("#include rb3_plus.dta")

    print(f"Successfully added rb3_plus pro string upgrades into the RB3DX ark.")

if __name__ == "__main__":
    add_strings()