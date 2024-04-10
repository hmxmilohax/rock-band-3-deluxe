#!/usr/bin/python3
from lib import ninja_syntax
from pathlib import Path
import sys
import argparse
import os

game_name = "Rock Band 3 Deluxe"

#versions
#gh1, gh2 - " "
#rb1, track packs - "-v 4"
#rb2, tbrb, gdrb - "-v 5"
#rb3, dc, blitz - "-v 6"
ark_version = "-v 6"

#require user provided vanilla ark extract in "vanilla/platform" folder
vanilla_files = False

#set True for rb1 and newer 
new_gen = True
#rock band 1 has quirks that mix old_gen and new_gen
rb1 = False

#patch for patch arks, main for patchcreator, old gen, and rb1
hdr_name = "patch"

dtb_encrypt = "-e"
#versions
# gh1, gh2 - "--miloVersion 25"
# rb1 onward - "--miloVersion 26"
miloVersion = "--miloVersion 26"

#paths in _ark/dx/custom_textures that should generate list dtbs
custom_texture_paths = [
    "highways",
    "streaks",
    "overdrive",
    "gems/gems_default",
    "strikeline/strikeline_guitar",
    "flames/flames_spark",
    "sustains",
    "score/scoreboard_frame",
    "rails/beat_lines",
    "stars/score_star_frame",
    "font",
    "solo_box",
    "bre/bre_shield",
    "rails/rails_track",
    "lanes/gem_mash_green_emmisive",
    "overdrive_bar/od_bar_background",
    "multiplier_ring/multiplier_ring_plate_fc",
    "crowd_meter/crowd_meter_frame",
    "keyboard/keyboard_lanes",
    "vocal_highway/vocal_highway_bg",
    "vocal_arrows/vocal_arrow",
    "vocal_note/vocal_note_tube",
    "vocal_overdrive/vocal_overdrive_now_bar"
]

#patchcreator options
patchcreator = False
new_ark_part = "10"
dol_name = "main.dol"
elf_name = " "
bin_name = " "
xex_name = " "

parser = argparse.ArgumentParser(prog="configure")
parser.add_argument("platform")
parser.add_argument(
    "--no-updates", action="store_true", help="disable dx song updates"
)

args = parser.parse_args()

#new gen games (rb2 onward) add platform suffix to ark name
if new_gen == True:
    hdr_name = hdr_name + "_" + args.platform

if args.platform == "ps2":
    #all milo ps2 games from gh to rb use MAIN_0.ARK
    hdr_name = "MAIN"
    if new_gen == False:
        #pre rb2 does not use miloVersion for superfreq image generation on ps2
        miloVersion = " "
        if rb1 == False:
            #pre rb1 uses -E for dtb encryption on ps2
            dtb_encrypt = dtb_encrypt.upper()

print(f"Configuring {game_name}...")
print(f"Platform: {args.platform}")

ninja = ninja_syntax.Writer(open("build.ninja", "w+"))

# configure tools
ark_dir = Path("obj", args.platform, "ark")
match sys.platform:
    case "win32":
        ninja.variable("silence", ">nul")
        ninja.rule("copy", "cmd /c copy $in $out $silence", description="COPY $in")
        ninja.rule("bswap", "dependencies\\windows\\swap_art_bytes.exe $in $out", description="BSWAP $in")
        ninja.rule("version", "python dependencies\\python\\gen_version.py $out", description="Writing version info")
        ninja.rule("png_list", "python dependencies\\python\\png_list.py $dir $out", description="PNGLIST $dir")
        ninja.variable("superfreq", "dependencies\\windows\\superfreq.exe")
        ninja.variable("arkhelper", "dependencies\\windows\\arkhelper.exe")
        ninja.variable("dtab", "dependencies\\windows\\dtab.exe")
        ninja.variable("dtacheck", "dependencies\\windows\\dtacheck.exe")
    case "darwin":
        ninja.variable("silence", "> /dev/null")
        ninja.rule("copy", "cp $in $out", description="COPY $in")
        ninja.rule("bswap", "python3 dependencies/python/swap_rb_art_bytes.py $in $out", description="BSWAP $in")
        ninja.rule("version", "python3 dependencies/python/gen_version.py $out", description="Writing version info")
        ninja.rule("png_list", "python3 dependencies/python/png_list.py $dir $out", description="PNGLIST $dir")
        ninja.variable("superfreq", "dependencies/macos/superfreq")
        ninja.variable("arkhelper", "dependencies/macos/arkhelper")
        ninja.variable("dtab", "dependencies/macos/dtab")
        # dtacheck needs to be compiled for mac
        ninja.variable("dtacheck", "true")
    case "linux":
        ninja.variable("silence", "> /dev/null")
        ninja.rule("copy", "cp --reflink=auto $in $out",description="COPY $in")
        ninja.rule("bswap", "dependencies/linux/swap_art_bytes $in $out", "BSWAP $in")
        ninja.rule("version", "python dependencies/python/gen_version.py $out", description="Writing version info")
        ninja.rule("png_list", "python dependencies/python/png_list.py $dir $out", description="PNGLIST $dir")
        ninja.variable("superfreq", "dependencies/linux/superfreq")
        ninja.variable("arkhelper", "dependencies/linux/arkhelper")
        ninja.variable("dtab", "dependencies/linux/dtab")
        ninja.variable("dtacheck", "dependencies/linux/dtacheck")

#specify output directories per platform
match args.platform:
    case "ps3":
        out_dir = Path("out", args.platform, "USRDIR", "gen")
    case "xbox":
        out_dir = Path("out", args.platform, "gen")
    case "wii":
        out_dir = Path("out", args.platform, "files")
    case "ps2":
        out_dir = Path("out", args.platform, "GEN")

#building an ark
if args.platform in ["ps3", "xbox", "ps2"] and patchcreator == False:
    ark_encrypt = "-e"
    #ps2 pre rb1 does not encrypt the ark
    if args.platform == "ps2" and new_gen == False and rb1 == False:
        ark_encrypt = " "
    ninja.rule(
        "ark",
        f"$arkhelper dir2ark -n {hdr_name} {ark_version} {ark_encrypt} -s 4073741823 --logLevel error {ark_dir} {out_dir}",
        description="Building ark",
    )
#patchcreating an ark
if args.platform == "wii" or patchcreator == True:
    #patch creator time! force using main as the root name
    hdr_name = "main"
    #append platform if this is new style ark
    if new_gen == True:
        hdr_name = hdr_name + "_" + args.platform
    match args.platform:
        case "wii":
            hdr_path = "platform/" + args.platform + "/files/gen/" + hdr_name + ".hdr"
            exec_path = "platform/" + args.platform + "/sys/" + dol_name
        case "ps2":
            hdr_path = "platform/" + args.platform + "/GEN/" + hdr_name.upper() + ".HDR"
            exec_path = "platform/" + args.platform + "/" + elf_name
        case "ps3":
            hdr_path = "platform/" + args.platform + "/USRDIR/gen/" + hdr_name + ".hdr"
            exec_path = "platform/" + args.platform + "/USRDIR/" + bin_name
        case "xbox":
            hdr_path = "platform/" + args.platform + "/gen/" + hdr_name + ".hdr"
            exec_path = "platform/" + args.platform + "/" + xex_name
    ninja.rule(
        "ark",
        f"$arkhelper patchcreator -a {ark_dir} -o {out_dir} {hdr_path} {exec_path} --logLevel error",
        description="Building ark",
    )

ninja.rule(
    "sfreq",
    f"$superfreq png2tex -l error {miloVersion} --platform $platform $in $out",
    description="SFREQ $in"
    )
ninja.rule("dtacheck", "$dtacheck $in .dtacheckfns", description="DTACHECK $in")
ninja.rule("dtab_serialize", "$dtab -b $in $out", description="DTAB SER $in")
ninja.rule("dtab_encrypt", f"$dtab {dtb_encrypt} $in $out", description="DTAB ENC $in")
ninja.build("_always", "phony")

build_files = []

# copy platform files
if args.platform != "wii" and patchcreator == False:
    for f in filter(lambda x: x.is_file(), Path("platform", args.platform).rglob("*")):
        index = f.parts.index(args.platform)
        out_path = Path("out", args.platform).joinpath(*f.parts[index + 1 :])
        ninja.build(str(out_path), "copy", str(f))
        build_files.append(str(out_path))

def ark_file_filter(file: Path):
    if file.is_dir():
        return False
    if file.suffix.endswith("_ps3") and args.platform != "ps3":
        return False
    if file.suffix.endswith("_xbox") and args.platform != "xbox":
        return False
    if file.suffix.endswith("_wii") and args.platform != "wii":
        return False
    if file.suffix.endswith("mogg") and args.platform == "ps2":
        return False
    if any(file.suffix.endswith(suffix) for suffix in ["_ps2", "vgs"]) and args.platform != "ps2":
        return False
    if (args.platform == "wii"  or args.no_updates) and file.parts[slice(2)] == ("_ark", "songs"):
        return False

    return True

# build ark files
ark_files = []

for f in filter(ark_file_filter, Path("_ark").rglob("*")):
    match f.suffixes:
        case [".png"]:
            output_directory = Path("obj", args.platform, "ark").joinpath(
                *f.parent.parts[1:]
            )
            match args.platform:
                case "ps3":
                    target_filename = Path("gen", f.stem + ".png_ps3")
                    xbox_filename = Path("gen", f.stem + ".png_xbox")
                    xbox_directory = Path("obj", args.platform, "raw").joinpath(
                        *f.parent.parts[1:]
                    )
                    xbox_output = xbox_directory.joinpath(xbox_filename)
                    ps3_output = output_directory.joinpath(target_filename)
                    ninja.build(str(xbox_output), "sfreq", str(f), variables={"platform": "x360"})
                    ninja.build(str(ps3_output), "bswap", str(xbox_output))
                    ark_files.append(str(ps3_output))
                case "xbox":
                    target_filename = Path("gen", f.stem + ".png_xbox")
                    xbox_directory = Path("obj", args.platform, "ark").joinpath(
                        *f.parent.parts[1:]
                    )
                    xbox_output = xbox_directory.joinpath(target_filename)
                    ninja.build(str(xbox_output), "sfreq", str(f), variables={"platform": "x360"})
                    ark_files.append(str(xbox_output))
                case "wii":
                    target_filename = Path("gen", f.stem + ".png_wii")
                    wii_directory = Path("obj", args.platform, "ark").joinpath(
                        *f.parent.parts[1:]
                    )
                    wii_output = wii_directory.joinpath(target_filename)
                    ninja.build(str(wii_output), "sfreq", str(f), variables={"platform": "wii"})
                    ark_files.append(str(wii_output))
                #disabled as we need resizing
                #case "ps2":
                #    target_filename = Path("gen", f.stem + ".png_ps2")
                #    ps2_directory = Path("obj", args.platform, "ark").joinpath(
                #        *f.parent.parts[1:]
                #    )
                #    ps2_output = ps2_directory.joinpath(target_filename)
                #    ninja.build(str(ps2_output), "sfreq", str(f), variables={"platform": "ps2"})
                #    ark_files.append(str(ps2_output))

        case [".dta"]:
            target_filename = Path("gen", f.stem + ".dtb")
            stamp_filename = Path("gen", f.stem + ".dtb.checked")

            output_directory = Path("obj", args.platform, "ark").joinpath(
                *f.parent.parts[1:]
            )
            serialize_directory = Path("obj", args.platform, "raw").joinpath(
                *f.parent.parts[1:]
            )

            serialize_output = serialize_directory.joinpath(target_filename)
            encryption_output = output_directory.joinpath(target_filename)
            stamp = serialize_directory.joinpath(stamp_filename)
            ninja.build(str(stamp), "dtacheck", str(f))
            ninja.build(
                str(serialize_output),
                "dtab_serialize",
                str(f),
                implicit=[str(stamp), "_always"],
            )
            ninja.build(str(encryption_output), "dtab_encrypt", str(serialize_output))
            ark_files.append(str(encryption_output))
        case _:
            index = f.parts.index("_ark")
            out_path = Path("obj", args.platform, "ark").joinpath(*f.parts[index + 1 :])
            ninja.build(str(out_path), "copy", str(f))
            ark_files.append(str(out_path))

# write version info
dta = Path("obj", args.platform, "raw", "dx", "locale", "dx_version.dta")
dtb = Path("obj", args.platform, "raw", "dx", "locale", "gen", "dx_version.dtb")
enc = Path("obj", args.platform, "ark", "dx", "locale", "gen", "dx_version.dtb")

ninja.build(str(dta), "version", implicit="_always")
ninja.build(str(dtb), "dtab_serialize", str(dta))
ninja.build(str(enc), "dtab_encrypt", str(dtb))

ark_files.append(str(enc))

#copy vanilla files to obj if required
if vanilla_files == True and patchcreator == False:
    from vanilla_files import vanilla
    ark_files, vanilla_files = vanilla(ark_files, args.platform, ninja, Path)

def generate_texture_list(input_path: Path):
    base = input_path.parts[1:]
    dta = Path("obj", args.platform, "raw").joinpath(*base).joinpath("_list.dta")
    dtb = Path("obj", args.platform, "raw").joinpath(*base).joinpath("gen", "_list.dtb")
    enc = Path("obj", args.platform, "ark").joinpath(*base).joinpath("gen", "_list.dtb")
    ninja.build(str(dta), "png_list", variables={"dir": str(input_path)}, implicit="_always")
    ninja.build(str(dtb), "dtab_serialize", str(dta))
    ninja.build(str(enc), "dtab_encrypt", str(dtb))

root_path = Path("_ark", "dx", "custom_textures")
for texture_list_path in [root_path.joinpath(path) for path in custom_texture_paths]:
    generate_texture_list(texture_list_path)

# build ark
ark_part = "0"
if patchcreator == True:
    ark_part = new_ark_part
match args.platform:
    case "ps3":
        hdr = str(Path("out", args.platform, "USRDIR", hdr_name + ".hdr"))
        ark = str(Path("out", args.platform, "USRDIR", hdr_name + "_" + ark_part + ".ark"))
    case "xbox":
        hdr = str(Path("out", args.platform, hdr_name + ".hdr"))
        ark = str(Path("out", args.platform, hdr_name + "_" + ark_part + ".ark"))
    case "wii":
        hdr = str(Path("out", args.platform, "files", hdr_name + "_" + args.platform + ".hdr"))
        ark = str(Path("out", args.platform, "files", hdr_name + "_" + args.platform + "_" + ark_part + ".ark"))
    case "ps2":
        hdr = str(Path("out", args.platform, hdr_name + ".HDR"))
        ark = str(Path("out", args.platform, hdr_name + "_" + ark_part + ".ARK"))
ninja.build(
    ark,
    "ark",
    implicit=ark_files,
    implicit_outputs=[hdr],
)
build_files.append(hdr)

# make the all target build everything
ninja.build("all", "phony", build_files)
ninja.close()