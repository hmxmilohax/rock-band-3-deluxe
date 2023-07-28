# enable_stock_pad.py
from pathlib import Path
import shutil

def copy_folder_contents(source, destination):
    # Ensure the destination folder exists
    destination.mkdir(parents=True, exist_ok=True)

    for item in source.iterdir():
        target = destination / item.name
        if item.is_file():
            # Copy files, overwriting existing files in the destination
            shutil.copy2(item, target)
        else:
            # Recursively copy subfolders
            copy_folder_contents(item, target)

def main():
    # get the current working directory (where this script resides)
    cwd = Path().absolute()
    # get the root directory of the repo
    root_dir = Path(__file__).parents[2]

    # Set the source and destination folders
    source_folder = root_dir / "dependencies" / "_rb3_plus_keys_moggs_enc"
    destination_folder = root_dir / "_ark" / "songs" / "updates"

    # Copy the contents of the source folder into the destination folder
    copy_folder_contents(source_folder, destination_folder)

    missing_song_data_path = root_dir / "_ark" / "dx" / "macros" / "dx_macros.dta"
    missing_song_data = [line for line in open(missing_song_data_path, "r")]

    overwritten = False
    for i in range(len(missing_song_data)):
        if "; #define KEYS_BUILD" in missing_song_data[i]:
            missing_song_data[i] = missing_song_data[i].replace("; #define", "#define")
            overwritten = True
            break

    if overwritten:
        with open(missing_song_data_path, "w") as f:
            f.writelines(missing_song_data)

if __name__ == "__main__":
    main()
