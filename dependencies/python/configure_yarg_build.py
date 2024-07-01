#!/usr/bin/python3

# this is just the old script with everything not related to yarg stripped out
# i didn't feel like rewriting it
# -- dark

from lib import ninja_syntax
from pathlib import Path
import sys

ninja = ninja_syntax.Writer(open("build.ninja", "w+"))

match sys.platform:
    case "win32":
        ninja.variable("silence", ">nul")
        ninja.rule("copy", "cmd /c copy $in $out $silence")
        ninja.rule("bswap", "dependencies\\windows\\swap_art_bytes.exe $in $out")
        ninja.variable("superfreq", "dependencies\\windows\\superfreq.exe")
        ninja.variable("arkhelper", "dependencies\\windows\\arkhelper.exe")
    case "darwin":
        ninja.variable("silence", "> /dev/null")
        ninja.rule("copy", "cp $in $out")
        ninja.rule(
            "bswap", "python3 dependencies/python/swap_rb_art_bytes.py $in $out"
        )
        ninja.variable("superfreq", "dependencies/macos/superfreq")
        ninja.variable("arkhelper", "dependencies/macos/arkhelper")
    case "linux":
        ninja.variable("silence", "> /dev/null")
        ninja.rule("copy", "cp --reflink=auto $in $out")
        ninja.rule("bswap", "dependencies/linux/swap_art_bytes $in $out")
        ninja.variable("superfreq", "dependencies/linux/superfreq")
        ninja.variable("arkhelper", "dependencies/linux/arkhelper")

ninja.rule("sfreq", "$superfreq png2tex $in $out -l error --miloVersion 26 --platform x360")

ninja.rule("dtacheck", "$dtacheck $in .dtacheckfns")

def convert_pngs():
    files = list(Path("_ark", "songs").rglob("*.png"))

    output_files = []
    for f in files:
        target_filename = Path("gen", f.stem + ".png_xbox")
        xbox_directory = Path("obj", "yarg", "ark").joinpath(
            *f.parent.parts[1:]
        )
        xbox_output = xbox_directory.joinpath(target_filename)
        ninja.build(str(xbox_output), "sfreq", str(f))
        output_files.append(str(xbox_output))

    return output_files

# this is greasy but i don't see a better way of doing this
def yarg_rewrite_output_path(path: Path):
    path_parts = list(path.parts)
    if "updates" not in  path.parts:
        path_parts.insert(3, "updates")


    path_parts.pop(2)
    path_parts.pop(2)
    path_parts.insert(2, "songs_updates")

    return Path(*path_parts)

def copy_yarg_built_files(files):
    output_files = []
    for i in files:
        in_path = Path(i)
        index = in_path.parts.index("ark")
        out_path = Path("out", "yarg").joinpath(*in_path.parts[index + 1 :])
        out_path = yarg_rewrite_output_path(out_path)
        ninja.build(str(out_path), "copy", str(in_path))
        output_files.append(str(out_path))


    return output_files

def copy_yarg_rawfiles():
    def file_filter(file: Path):
        if file.suffix.endswith("_ps3"):
            return False
        if file.suffix.endswith("_xbox"):
            return False
        if file.suffix.endswith("_wii"):
            return False
        if file.suffix.endswith(".png"):
            return False
        if file.is_dir():
            return False
        if file.name.endswith("_update.txt"):
            return False
        return True

    files = filter(file_filter, Path("_ark", "songs").rglob("*"))

    output_files = []
    for f in files:
        index = f.parts.index("_ark")
        out_path = Path("out", "yarg").joinpath(*f.parts[index + 1 :])
        out_path = yarg_rewrite_output_path(out_path)

        if "missing_song_data.dta" in out_path.parts:
            continue
        if "missing_song_data_updates.dta" in out_path.parts:
            continue

        if not out_path.name.endswith("_update.txt"):
            ninja.build(str(out_path), "copy", str(f))
            output_files.append(str(out_path))

    # manually copy the songs dta
    ninja.build(
        str(Path("out", "yarg", "songs_updates", "songs_updates.dta")),
        "copy",
        str(Path("_ark", "dx", "song_updates", "songs_updates.dta")),
    )

    return output_files


arkfiles = convert_pngs()

# copy files
buildfiles = copy_yarg_built_files(arkfiles)
buildfiles += copy_yarg_rawfiles()

ninja.build("all", "phony", buildfiles)