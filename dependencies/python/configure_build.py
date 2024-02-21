#!/usr/bin/python3
from lib import ninja_syntax
from pathlib import Path
import sys
import os

platform = sys.argv[1]
ninja = ninja_syntax.Writer(open("build.ninja", "w+"))

print("Configuring Rock Band 3 Deluxe...")

def print_color_text(*args):
    text = ' '.join(map(str, args[:-1]))
    color_code = args[-1]
    print(f"\033[{color_code}m{text}\033[0m")

if len(sys.argv) > 2 and sys.argv[2] == "--fun":
    print_color_text(f"▛▀▖      ▌   ▛▀▖        ▌ ▞▀▖ ▛▀▖   ▜          ", "1;36")  # Cyan text
    print_color_text(f"▙▄▘▞▀▖▞▀▖▌▗▘ ▙▄▘▝▀▖▛▀▖▞▀▌  ▄▘ ▌ ▌▞▀▖▐ ▌ ▌▚▗▘▞▀▖", "1;36")  # Cyan text
    print_color_text(f"▌▚ ▌ ▌▌ ▖▛▚  ▌ ▌▞▀▌▌ ▌▌ ▌ ▖ ▌ ▌ ▌▛▀ ▐ ▌ ▌▗▚ ▛▀ ", "1;36")  # Cyan text
    print_color_text(f"▘ ▘▝▀ ▝▀ ▘ ▘ ▀▀ ▝▀▘▘ ▘▝▀▘ ▝▀  ▀▀ ▝▀▘ ▘▝▀▘▘ ▘▝▀▘", "1;36")  # Cyan text
    match platform:
        case "ps3":
            print_color_text(f"Platform: {platform}", "1;38;5;196")
        case "xbox":
            print_color_text(f"Platform: {platform}", "1;32;40")
        case "wii":
            print_color_text(f"Platform: {platform}", "1;36")
else:
    print(f"Platform: {platform}")

def configure_tools(platform="ps3"):
    ark_dir = Path("obj", platform, "ark")
    match sys.platform:
        case "win32":
            ninja.variable("silence", ">nul")
            ninja.rule("copy", "cmd /c copy $in $out $silence")
            ninja.rule("bswap", "dependencies\\windows\\swap_art_bytes.exe $in $out")
            ninja.variable("superfreq", "dependencies\\windows\\superfreq.exe")
            ninja.variable("arkhelper", "dependencies\\windows\\arkhelper.exe")
            ninja.variable("dtab", "dependencies\\windows\\dtab.exe")
            ninja.variable("dtacheck", "dependencies\\windows\\dtacheck.exe")
        case "darwin":
            ninja.variable("silence", "> /dev/null")
            ninja.rule("copy", "cp $in $out")
            ninja.rule(
                "bswap", "python3 dependencies/python/swap_rb_art_bytes.py $in $out"
            )
            ninja.variable("superfreq", "dependencies/macos/superfreq")
            ninja.variable("arkhelper", "dependencies/macos/arkhelper")
            ninja.variable("dtab", "dependencies/macos/dtab")
            # dtacheck needs to be compiled for mac
            ninja.variable("dtacheck", "true")
        case "linux":
            ninja.variable("silence", "> /dev/null")
            ninja.rule("copy", "cp --reflink=auto $in $out")
            ninja.rule("bswap", "dependencies/linux/swap_art_bytes $in $out")
            ninja.variable("superfreq", "dependencies/linux/superfreq")
            ninja.variable("arkhelper", "dependencies/linux/arkhelper")
            ninja.variable("dtab", "dependencies/linux/dtab")
            ninja.variable("dtacheck", "dependencies/linux/dtacheck")

    match platform:
        case "ps3":
            out_dir = Path("out", platform, "USRDIR", "gen")
            ninja.rule(
                "ark",
                f"$arkhelper dir2ark {ark_dir} {out_dir} -n patch_ps3 -e -s 4073741823 -v 6 $silence",
                description="Building ARK",
            )
        case "xbox":
            out_dir = Path("out", platform, "gen")
            ninja.rule(
                "ark",
                f"$arkhelper dir2ark {ark_dir} {out_dir} -n patch_xbox -e -v 6 -s 4073741823 $silence",
                description="Building ARK",
            )
        case "wii":
            out_dir = Path("out", platform, "files")
            ninja.rule(
                "ark",
                f"$arkhelper patchcreator -a {ark_dir} -o {out_dir} platform/wii/files/gen/main_wii.hdr platform/wii/sys/main.dol $silence",
                description="Building ARK",
            )

    ninja.rule("sfreq", "$superfreq png2tex $in $out --miloVersion 26 --platform x360")
    ninja.rule("dtacheck", "$dtacheck $in .dtacheckfns")
    ninja.rule("dtab_serialize", "$dtab -b $in $out")
    ninja.rule("dtab_encrypt", "$dtab -e $in $out")

def wii_file_filer(file: Path):
    if file.parts[slice(2)] == ("_ark", "songs"):
        return False
    if file.parts[slice(3)] == ("_ark", "dx", "song_updates"):
        return False

    return True

def copy_rawfiles(platform):
    def file_filter(file: Path):
        if file.suffix.endswith("_ps3") and platform != "ps3":
            return False
        if file.suffix.endswith("_xbox") and platform != "xbox":
            return False
        if file.suffix.endswith("_wii") and platform != "wii":
            return False
        if file.suffix.endswith(".dta"):
            return False
        if file.suffix.endswith(".png"):
            return False
        if file.is_dir():
            return False
        return True

    files = filter(file_filter, Path("_ark").rglob("*"))

    if platform == "wii":
        files = filter(wii_file_filer, files)

    output_files = []
    for f in files:
        index = f.parts.index("_ark")
        out_path = Path("obj", platform, "ark").joinpath(*f.parts[index + 1 :])
        ninja.build(str(out_path), "copy", str(f))
        output_files.append(str(out_path))

    return output_files


def run_dtab():
    files = list(Path("_ark").rglob("*.dta"))

    if platform == "wii":
        files = filter(wii_file_filer, files)

    output_files = []
    for f in files:
        target_filename = Path("gen", f.stem + ".dtb")
        stamp_filename = Path("gen", f.stem + ".dtb.stamp")

        output_directory = Path("obj", platform, "ark").joinpath(*f.parent.parts[1:])
        serialize_directory = Path("obj", platform, "raw").joinpath(*f.parent.parts[1:])

        serialize_output = serialize_directory.joinpath(target_filename)
        encryption_output = output_directory.joinpath(target_filename)
        stamp = serialize_directory.joinpath(stamp_filename)
        ninja.build(str(stamp), "dtacheck", str(f))
        ninja.build(str(serialize_output), "dtab_serialize", str(f), implicit=str(stamp))
        ninja.build(str(encryption_output), "dtab_encrypt", str(serialize_output))
        output_files.append(str(encryption_output))

    return output_files

def convert_pngs(platform):
    files = list(Path("_ark").rglob("*.png"))

    if platform == "yarg":
        files = list(Path("_ark", "songs").rglob("*.png"))

    if platform == "wii":
        files = filter(wii_file_filer, files)

    output_files = []
    for f in files:
        output_directory = Path("obj", platform, "ark").joinpath(*f.parent.parts[1:])
        match platform:
            case "ps3":
                target_filename = Path("gen", f.stem + ".png_ps3")
                xbox_filename = Path("gen", f.stem + ".png_xbox")
                xbox_directory = Path("obj", platform, "raw").joinpath(
                    *f.parent.parts[1:]
                )
                xbox_output = xbox_directory.joinpath(xbox_filename)
                ps3_output = output_directory.joinpath(target_filename)
                ninja.build(str(xbox_output), "sfreq", str(f))
                ninja.build(str(ps3_output), "bswap", str(xbox_output))
                output_files.append(str(ps3_output))
            case "xbox":
                target_filename = Path("gen", f.stem + ".png_xbox")
                xbox_directory = Path("obj", platform, "ark").joinpath(
                    *f.parent.parts[1:]
                )
                xbox_output = xbox_directory.joinpath(target_filename)
                ninja.build(str(xbox_output), "sfreq", str(f))
                output_files.append(str(xbox_output))
            case "yarg":
                target_filename = Path("gen", f.stem + ".png_xbox")
                xbox_directory = Path("obj", platform, "ark").joinpath(
                    *f.parent.parts[1:]
                )
                xbox_output = xbox_directory.joinpath(target_filename)
                ninja.build(str(xbox_output), "sfreq", str(f))
                output_files.append(str(xbox_output))

    return output_files


def copy_buildfiles(platform):
    files = [x for x in Path("platform", platform).rglob("*") if x.is_file()]
    output_files = []
    for f in files:
        index = f.parts.index(platform)
        out_path = Path("out", platform).joinpath(*f.parts[index + 1 :])
        ninja.build(str(out_path), "copy", str(f))
        output_files.append(str(out_path))

    return output_files


def generate_ark(platform, deps):
    match platform:
        case "ps3":
            hdr = str(Path("out", platform, "USRDIR", "gen", "patch_xbox.hdr"))
            ninja.build(
                str(Path("out", platform, "USRDIR", "gen", "patch_ps3_0.ark")),
                "ark",
                implicit=deps,
                implicit_outputs=[hdr],
            )
            return [hdr]
        case "xbox":
            hdr = str(Path("out", platform, "gen", "patch_xbox.hdr"))
            ninja.build(
                str(Path("out", platform, "gen", "patch_xbox_0.ark")),
                "ark",
                implicit=deps,
                implicit_outputs=hdr,
            )
            return [hdr]
        case "wii":
            hdr = str(Path("out", platform, "files", "gen", "main_wii.hdr"))
            ninja.build(
                str(Path("out", platform, "files", "gen", "main_wii_10.ark")),
                "ark",
                implicit=deps,
                implicit_outputs=hdr,
            )
            return [hdr]

    raise Exception("invalid platform")



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
        out_path = Path("out", platform).joinpath(*in_path.parts[index + 1 :])
        out_path = yarg_rewrite_output_path(out_path)
        ninja.build(str(out_path), "copy", str(in_path))
        output_files.append(str(out_path))


    return output_files


def copy_yarg_rawfiles(platform):
    def file_filter(file: Path):
        if file.suffix.endswith("_ps3") and platform != "ps3":
            return False
        if file.suffix.endswith("_xbox") and platform != "xbox":
            return False
        if file.suffix.endswith(".png"):
            return False
        if file.is_dir():
            return False
        return True

    files = filter(file_filter, Path("_ark", "songs").rglob("*"))

    output_files = []
    for f in files:
        index = f.parts.index("_ark")
        out_path = Path("out", platform).joinpath(*f.parts[index + 1 :])
        out_path = yarg_rewrite_output_path(out_path)

        if "missing_song_data.dta" in out_path.parts:
            continue
        if "missing_song_data_updates.dta" in out_path.parts:
            continue

        ninja.build(str(out_path), "copy", str(f))
        output_files.append(str(out_path))

    # manually copy the songs dta
    ninja.build(
        str(Path("out", platform, "songs_updates", "songs_updates.dta")),
        "copy",
        str(Path("_ark", "dx", "song_updates", "songs_updates.dta")),
    )

    return output_files


configure_tools(platform)

match platform:
    case "yarg":
        # generate and copy files into the ark
        arkfiles = convert_pngs(platform)

        # copy files
        buildfiles = copy_yarg_built_files(arkfiles)
        buildfiles += copy_yarg_rawfiles("yarg")

        ninja.build("all", "phony", buildfiles)

    case _:
        buildfiles = []
        if platform != "wii":
            buildfiles += copy_buildfiles(platform)

        # generate and copy files into the ark
        arkfiles = copy_rawfiles(platform)
        arkfiles += run_dtab()
        arkfiles += convert_pngs(platform)

        # build ark
        buildfiles += generate_ark(platform, arkfiles)

        ninja.build("all", "phony", buildfiles)