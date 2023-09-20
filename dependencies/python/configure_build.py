#!/usr/bin/python3
from lib import ninja_syntax
from pathlib import Path
import sys
import os

platform = sys.argv[1]
ninja = ninja_syntax.Writer(open("build.ninja", "w+"))

print(
    """
        #       mmmm      #        
  m mm  #mmm   "   "#  mmm#  m   m 
  #"  " #" "#    mmm" #" "#   #m#  
  #     #   #      "# #   #   m#m  
  #     ##m#"  "mmm#" "#m##  m" "m 
                                   
===================================="""
)

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
        case "darwin":
            ninja.variable("silence", "> /dev/null")
            ninja.rule("copy", "cp $in $out")
            ninja.rule("bswap", "python3 dependencies/python/swap_rb_art_bytes.py $in $out")
            ninja.variable("superfreq", "dependencies/macos/superfreq")
            ninja.variable("arkhelper", "dependencies/macos/arkhelper")
            ninja.variable("dtab", "dependencies/macos/dtab")
        case "linux":
            ninja.variable("silence", "> /dev/null")
            ninja.rule("copy", "cp --reflink=auto $in $out")
            ninja.rule("bswap", "dependencies/linux/swap_art_bytes $in $out")
            ninja.variable("superfreq", "dependencies/linux/superfreq")
            ninja.variable("arkhelper", "dependencies/linux/arkhelper")
            ninja.variable("dtab", "dependencies/linux/dtab")

    match platform:
        case "ps3":
            out_dir = Path("out", platform, "USRDIR", "gen")
            ninja.rule(
                "ark",
                f"$arkhelper dir2ark {ark_dir} {out_dir} -n patch_ps3 -e -v 6 $silence",
                description="Building ARK",
            )
        case "xbox":
            out_dir = Path("out", platform, "gen")
            ninja.rule(
                "ark",
                f"$arkhelper dir2ark {ark_dir} {out_dir} -n patch_xbox -e -v 6 $silence",
                description="Building ARK",
            )

    ninja.rule("sfreq", "$superfreq png2tex $in $out --miloVersion 26 --platform x360")
    ninja.rule("dtab_serialize", "$dtab -b $in $out")
    ninja.rule("dtab_encrypt", "$dtab -e $in $out")


def copy_rawfiles(platform):
    def file_filter(file: Path):
        if file.suffix.endswith("_ps3") and platform != "ps3":
            return False
        if file.suffix.endswith("_xbox") and platform != "xbox":
            return False
        if file.suffix.endswith("_wii"): # TODO: remove this when we clean up the wii files
            return False
        if file.suffix.endswith(".dta"):
            return False
        if file.suffix.endswith(".png"):
            return False
        if file.is_dir():
            return False
        return True

    files = filter(file_filter, Path("_ark").rglob("*"))
    output_files = []
    for f in files:
        index = f.parts.index("_ark")
        out_path = Path("obj", platform, "ark").joinpath(*f.parts[index + 1 :])
        ninja.build(str(out_path), "copy", str(f))
        output_files.append(str(out_path))

    return output_files


def run_dtab():
    files = list(Path("_ark").rglob("*.dta"))
    output_files = []
    for f in files:
        target_filename = Path("gen", f.stem + ".dtb")

        output_directory = Path("obj", platform, "ark").joinpath(*f.parent.parts[1:])
        serialize_directory = Path("obj", platform, "raw").joinpath(*f.parent.parts[1:])

        serialize_output = serialize_directory.joinpath(target_filename)
        encryption_output = output_directory.joinpath(target_filename)
        ninja.build(str(serialize_output), "dtab_serialize", str(f))
        ninja.build(str(encryption_output), "dtab_encrypt", str(serialize_output))
        output_files.append(str(encryption_output))

    return output_files

def convert_pngs(platform):
    files = list(Path("_ark").rglob("*.png"))
    output_files = []
    for f in files:
        output_directory = Path("obj", platform, "ark").joinpath(*f.parent.parts[1:])
        match platform:
            case "ps3":
                target_filename = Path("gen", f.stem + ".png_ps3")
                xbox_filename = Path("gen", f.stem + ".png_xbox")
                xbox_directory = Path("obj", platform, "raw").joinpath(*f.parent.parts[1:])
                xbox_output = xbox_directory.joinpath(xbox_filename)
                ps3_output = output_directory.joinpath(target_filename)
                ninja.build(str(xbox_output), "sfreq", str(f))
                ninja.build(str(ps3_output), "bswap", str(xbox_output))
                output_files.append(str(ps3_output))
            case "xbox":
                target_filename = Path("gen", f.stem + ".png_xbox")
                xbox_directory = Path("obj", platform, "ark").joinpath(*f.parent.parts[1:])
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
                str(Path("out", platform, "USRDIR","gen", "patch_ps3_0.ark")),
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

    raise Exception("invalid platform")


configure_tools(platform)
# copy initial build files
buildfiles = copy_buildfiles(platform)

# generate and copy files into the ark
arkfiles = copy_rawfiles(platform)
arkfiles += run_dtab()
arkfiles += convert_pngs(platform)

# build ark
buildfiles += generate_ark(platform, arkfiles)

ninja.build("all", "phony", buildfiles)