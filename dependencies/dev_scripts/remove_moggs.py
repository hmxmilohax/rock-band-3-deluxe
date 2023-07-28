# enable_stock_pad.py
from pathlib import Path
import shutil
import os

def delete_mogg_files(destination_folder):
    for root, _, files in os.walk(destination_folder):
        for file in files:
            if file.endswith(".mogg"):
                file_path = os.path.join(root, file)
                os.remove(file_path)

def main():
    # get the current working directory (where this script resides)
    cwd = Path().absolute()
    # get the root directory of the repo
    root_dir = Path(__file__).parents[2]

    destination_folder = root_dir / "_ark" / "songs" / "updates"
    delete_mogg_files(destination_folder)

    missing_song_data_path = root_dir / "_ark" / "dx" / "macros" / "dx_macros.dta"
    missing_song_data = [line for line in open(missing_song_data_path, "r")]

    overwritten = False
    for i in range(len(missing_song_data)):
        if "#define KEYS_BUILD" in missing_song_data[i]:
            missing_song_data[i] = missing_song_data[i].replace("#define", "; #define")
            overwritten = True
            break

    if overwritten:
        with open(missing_song_data_path, "w") as f:
            f.writelines(missing_song_data)

if __name__ == "__main__":
    main()
