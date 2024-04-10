#!/usr/bin/python3
from lib import ninja_syntax
from pathlib import Path
import sys
import argparse
import json
import os

vanilla_files = False
generate_texture_list = False
new_gen = True

script_dir = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(script_dir, 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

ninja = ninja_syntax.Writer(open("build.ninja", "w+"))

parser = argparse.ArgumentParser(prog="configure")
parser.add_argument("platform")
parser.add_argument(
    "--no-updates", action="store_true", help="disable dx song updates"
)

args = parser.parse_args()

game_name = config.get("game_name", "")
ark_version = config.get("ark_version", "")
vanilla_files = config.get("vanilla_files", False)
new_gen = config.get("new_gen", False)
hdr_name = config.get("hdr_name", "")
dtb_encrypt = config.get("dtb_encrypt", "")
miloVersion = config.get("miloVersion", "")

if game_name == "Guitar Hero II Deluxe":
    from vanilla_files import vanilla
    if args.platform == "ps2":
        hdr_name = hdr_name.upper()
        dtb_encrypt = dtb_encrypt.upper()
        miloVersion = "--preset gh2"

if game_name == "Rock Band 3 Deluxe":
        match args.platform:
            case "ps3":
                hdr_name = hdr_name + "_ps3"
            case "xbox":
                hdr_name = hdr_name + "_xbox"

print(f"Configuring {game_name}...")
print(f"Platform: {args.platform}")

# configure tools
ark_dir = Path("obj", args.platform, "ark")
match sys.platform:
    case "win32":
        ninja.variable("silence", ">nul")
        ninja.rule("copy", "cmd /c copy $in $out $silence", description="COPY $in")
        if new_gen == True:
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
        if new_gen == True:
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
        if new_gen == True:
            ninja.rule("bswap", "dependencies/linux/swap_art_bytes $in $out", "BSWAP $in")
        ninja.rule("version", "python dependencies/python/gen_version.py $out", description="Writing version info")
        ninja.rule("png_list", "python dependencies/python/png_list.py $dir $out", description="PNGLIST $dir")
        ninja.variable("superfreq", "dependencies/linux/superfreq")
        ninja.variable("arkhelper", "dependencies/linux/arkhelper")
        ninja.variable("dtab", "dependencies/linux/dtab")
        ninja.variable("dtacheck", "dependencies/linux/dtacheck")

match args.platform:
    case "ps3":
        out_dir = Path("out", args.platform, "USRDIR", "gen")
        ninja.rule(
            "ark",
            f"$arkhelper dir2ark -n {hdr_name} -e -s 4073741823 {ark_version} --logLevel error {ark_dir} {out_dir}",
            description="Building ark",
        )
    case "xbox":
        out_dir = Path("out", args.platform, "gen")
        ninja.rule(
            "ark",
            f"$arkhelper dir2ark -n {hdr_name} -e {ark_version} -s 4073741823 --logLevel error {ark_dir} {out_dir}",
            description="Building ark",
        )
    case "wii":
        out_dir = Path("out", args.platform, "files")
        ninja.rule(
            "ark",
            f"$arkhelper patchcreator -a {ark_dir} -o {out_dir} platform/wii/files/gen/main_wii.hdr platform/wii/sys/main.dol --logLevel error",
            description="Building ark",
        )
    case "ps2":
        out_dir = Path("out", args.platform, "GEN")
        ninja.rule(
            "ark",
            f"$arkhelper dir2ark -n {hdr_name.toupper()} {ark_version} -s 4073741823 --logLevel error {ark_dir} {out_dir}",
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
if args.platform != "wii":
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
    if file.suffix.endswith("mogg") and new_gen != True:
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

if vanilla_files == True:
    ark_files, vanilla_files = vanilla(ark_files, args.platform, ninja, Path)

def generate_texture_list(input_path: Path):
    base = input_path.parts[1:]
    dta = Path("obj", args.platform, "raw").joinpath(*base).joinpath("_list.dta")
    dtb = Path("obj", args.platform, "raw").joinpath(*base).joinpath("gen", "_list.dtb")
    enc = Path("obj", args.platform, "ark").joinpath(*base).joinpath("gen", "_list.dtb")
    ninja.build(str(dta), "png_list", variables={"dir": str(input_path)}, implicit="_always")
    ninja.build(str(dtb), "dtab_serialize", str(dta))
    ninja.build(str(enc), "dtab_encrypt", str(dtb))

generate_texture_list(Path("_ark", "dx", "custom_textures", "highways"))
generate_texture_list(Path("_ark", "dx", "custom_textures", "streaks"))
generate_texture_list(Path("_ark", "dx", "custom_textures", "overdrive"))
generate_texture_list(Path("_ark", "dx", "custom_textures", "gems", "gems_default"))
generate_texture_list(Path("_ark", "dx", "custom_textures", "strikeline", "strikeline_guitar"))
generate_texture_list(Path("_ark", "dx", "custom_textures", "flames", "flames_spark"))
generate_texture_list(Path("_ark", "dx", "custom_textures", "sustains"))
generate_texture_list(Path("_ark", "dx", "custom_textures", "score", "scoreboard_frame"))
generate_texture_list(Path("_ark", "dx", "custom_textures", "rails", "beat_lines"))
generate_texture_list(Path("_ark", "dx", "custom_textures", "stars", "score_star_frame"))
generate_texture_list(Path("_ark", "dx", "custom_textures", "font"))
generate_texture_list(Path("_ark", "dx", "custom_textures", "solo_box"))
generate_texture_list(Path("_ark", "dx", "custom_textures", "bre", "bre_shield"))
generate_texture_list(Path("_ark", "dx", "custom_textures", "rails", "rails_track"))
generate_texture_list(Path("_ark", "dx", "custom_textures", "lanes", "gem_mash_green_emmisive"))
generate_texture_list(Path("_ark", "dx", "custom_textures", "overdrive_bar", "od_bar_background"))
generate_texture_list(Path("_ark", "dx", "custom_textures", "multiplier_ring", "multiplier_ring_plate_fc"))
generate_texture_list(Path("_ark", "dx", "custom_textures", "crowd_meter", "crowd_meter_frame"))
generate_texture_list(Path("_ark", "dx", "custom_textures", "keyboard", "keyboard_lanes"))
generate_texture_list(Path("_ark", "dx", "custom_textures", "vocal_highway", "vocal_highway_bg"))
generate_texture_list(Path("_ark", "dx", "custom_textures", "vocal_arrows", "vocal_arrow"))
generate_texture_list(Path("_ark", "dx", "custom_textures", "vocal_note", "vocal_note_tube"))
generate_texture_list(Path("_ark", "dx", "custom_textures", "vocal_overdrive", "vocal_overdrive_now_bar"))

# build ark
match args.platform:
    case "ps3":
        hdr = str(Path("out", args.platform, "USRDIR", "gen", "patch_ps3.hdr"))
        ninja.build(
            str(Path("out", args.platform, "USRDIR", "gen", "patch_ps3_0.ark")),
            "ark",
            implicit=ark_files,
            implicit_outputs=[hdr],
        )
        build_files.append(hdr)
    case "xbox":
        hdr = str(Path("out", args.platform, "gen", "patch_xbox.hdr"))
        ninja.build(
            str(Path("out", args.platform, "gen", "patch_xbox_0.ark")),
            "ark",
            implicit=ark_files,
            implicit_outputs=hdr,
        )
        build_files.append(hdr)
    case "wii":
        hdr = str(Path("out", args.platform, "files", "gen", "main_wii.hdr"))
        ninja.build(
            str(Path("out", args.platform, "files", "gen", "main_wii_10.ark")),
            "ark",
            implicit=ark_files,
            implicit_outputs=hdr,
        )
        build_files.append(hdr)
    case "ps2":
        hdr = str(Path("out", args.platform, "GEN", "MAIN.HDR"))
        ninja.build(
            str(Path("out", args.platform, "GEN", "MAIN_0.ARK")),
            "ark",
            implicit=ark_files,
            implicit_outputs=hdr,
        )
        build_files.append(hdr)

# make the all target build everything
ninja.build("all", "phony", build_files)
ninja.close()