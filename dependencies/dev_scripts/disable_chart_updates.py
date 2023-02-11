# enable_stock_pad.py
from pathlib import Path

def main():

    # get the current working directory (where this script resides)
    cwd = Path().absolute()
    # get the root directory of the repo
    root_dir = Path(__file__).parents[2]
    
    missing_song_data_path = root_dir.joinpath("_ark/songs/missing_song_data.dta")
    missing_song_data = [line for line in open(missing_song_data_path, "r")]

    overwritten = False
    for i in range(len(missing_song_data)):
        if "#include dta_sections/harms_and_updates.dta" in missing_song_data[i]:
            missing_song_data[i] = missing_song_data[i].replace("#include", ";#include")
            overwritten = True
            break

    if overwritten:
        with open(missing_song_data_path, "w") as f:
            f.writelines(missing_song_data)

if __name__ == "__main__":
    main()