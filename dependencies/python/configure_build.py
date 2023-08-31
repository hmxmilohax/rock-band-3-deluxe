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
                                   
====================================                           """
)

print(f"Platform: {platform}")

def configure_tools(platform="ps3"):
    ark_dir = Path("obj", platform, "ark")
    match sys.platform:
        case "win32":
            ninja.variable("silence", ">nul")
            ninja.rule("copy", "cmd /c copy $in $out $silence")
            ninja.rule("bswap", "python dependencies\\python\\swap_rb_art_bytes.py $in $out")
            ninja.variable("superfreq", "dependencies\\windows\\superfreq.exe")
            ninja.variable("arkhelper", "dependencies\\windows\\arkhelper.exe")
            ninja.variable("dtab", "dependencies\\windows\\dtab.exe")
        case "linux":
            ninja.variable("silence", "> /dev/null")
            ninja.rule("copy", "cp --reflink=auto $in $out")
            ninja.rule("bswap", "python dependencies/python/swap_rb_art_bytes.py $in $out")
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
        serialize_directory = Path("obj", platform, "dtab_raw").joinpath(*f.parent.parts[1:])

        serialize_output = serialize_directory.joinpath(target_filename)
        encryption_output = output_directory.joinpath(target_filename)
        ninja.build(str(serialize_output), "dtab_serialize", str(f))
        ninja.build(str(encryption_output), "dtab_encrypt", str(serialize_output))
        output_files.append(str(encryption_output))

    return output_files


def process_textures(
    platform, input_dir: Path, output_dir: Path, name: str, prefix: str
):
    names = []
    output_files = []
    texture_list = []

    output_dir = Path("obj", platform, "ark").joinpath(output_dir.joinpath("gen"))
    tmp_dir = Path("obj", platform, name)

    # build list of files and convert textures
    for i in input_dir.iterdir():
        if i.is_dir():
            continue

        if i.stem.startswith(prefix):
            texture_list.append(i.stem.removeprefix(prefix))

        match platform:
            case "ps3":
                xbox_file = tmp_dir.joinpath(f"{i.stem}.png_xbox")
                ps3_file = output_dir.joinpath(f"{i.stem}.png_ps3")

                ninja.build(str(xbox_file), "sfreq", str(i))
                ninja.build(str(ps3_file), "bswap", str(xbox_file))
                output_files.append(str(ps3_file))
            case "xbox":
                xbox_file = output_dir.joinpath(f"{i.stem}.png_xbox")

                ninja.build(str(xbox_file), "sfreq", str(i))
                output_files.append(str(xbox_file))

    # write the file list and run dtab on it
    raw_file = tmp_dir.joinpath(f"{name}.dta")
    serialized_file = tmp_dir.joinpath(f"{name}.dtb")
    encrypted_file = output_dir.joinpath(f"{name}.dtb")

    os.makedirs(tmp_dir, exist_ok=True)
    f = open(raw_file, "w+")
    texture_list.sort()
    for i in texture_list:
        f.write(f'"{i}"\n')

    ninja.build(str(serialized_file), "dtab_serialize", str(raw_file))
    ninja.build(str(encrypted_file), "dtab_encrypt", str(serialized_file))

    output_files.append(str(encrypted_file))

    return output_files


def copy_buildfiles(platform):
    files = [x for x in Path("_build", platform).rglob("*") if x.is_file()]
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
arkfiles += process_textures(
    platform,
    Path("custom_textures", "multiplier_ring"),
    Path("ui", "track", "multiplier_ring"),
    "multiplier_ring",
    "streak_meter_plate_fc_",
)
arkfiles += process_textures(
    platform,
    Path("custom_textures", "smashers"),
    Path("ui", "track", "smashers"),
    "smashers",
    "square_smasher_bright_green_",
)
arkfiles += process_textures(
    platform,
    Path("custom_textures", "stars"),
    Path("ui", "track", "stars"),
    "stars",
    "score_star_gold_",
)

arkfiles += process_textures(
    platform,
    Path("custom_textures", "sustains"),
    Path("ui", "track", "sustains"),
    "sustains",
    "gem_trails_",
)

arkfiles += process_textures(
    platform,
    Path("custom_textures", "overdrive_bar"),
    Path("ui", "track", "overdrive_bar"),
    "overdrive_bar",
    "fx_rising_sun_",
)

arkfiles += process_textures(
    platform,
    Path("custom_textures", "lanes"),
    Path("ui", "track", "lanes"),
    "lanes",
    "gem_mash_blue_emmisive_",
)

arkfiles += process_textures(
    platform,
    Path("custom_textures", "rails"),
    Path("ui", "track", "rails"),
    "rails",
    "rails_",
)

arkfiles += process_textures(
    platform,
    Path("custom_textures", "crowd_meter"),
    Path("ui", "track", "crowd_meter"),
    "crowd_meter",
    "crowd_meter_frame_",
)

arkfiles += process_textures(
    platform,
    Path("custom_textures", "highways"),
    Path("ui", "track", "highways"),
    "highways",
    "",
)

arkfiles += process_textures(
    platform,
    Path("custom_textures", "emissives"),
    Path("ui", "track", "emissives"),
    "emissives",
    "",
)

arkfiles += process_textures(
    platform,
    Path("custom_textures", "flames"),
    Path("ui", "track", "flames"),
    "flames",
    "fx_smasher_smoke_",
)

arkfiles += process_textures(
    platform,
    Path("custom_textures", "gems"),
    Path("ui", "track", "gems"),
    "gems",
    "gliss_gems_",
)

arkfiles += process_textures(
    platform,
    Path("custom_textures", "score_box"),
    Path("ui", "track", "score_box"),
    "score_box",
    "scoreboard_frame_",
)

arkfiles += process_textures(
    platform,
    Path("custom_textures", "keyboards"),
    Path("ui", "track", "keyboards"),
    "keyboards",
    "track_lanes_keyboard_press_",
)

arkfiles += process_textures(
    platform,
    Path("custom_textures", "voxarrow"),
    Path("ui", "track", "voxarrow"),
    "voxarrow",
    "arrow_lead_c_",
)

arkfiles += process_textures(
    platform,
    Path("custom_textures", "voxnotes"),
    Path("ui", "track", "voxnotes"),
    "voxnotes",
    "talky_mask_",
)

arkfiles += process_textures(
    platform,
    Path("custom_textures", "spotlights"),
    Path("ui", "track", "spotlights"),
    "spotlights",
    "",
)

arkfiles += process_textures(
    platform,
    Path("custom_textures", "voxod"),
    Path("ui", "track", "voxod"),
    "voxod",
    "sunburst_nomip_",
)

arkfiles += process_textures(
    platform,
    Path("custom_textures", "voxhw"),
    Path("ui", "track", "voxhw"),
    "voxhw",
    "lyrics_bg_blue_",
)

arkfiles += process_textures(
    platform,
    Path("custom_textures", "font"),
    Path("ui", "track", "font"),
    "font",
    "pentatonic_hub_",
)

# these will still generate a dta list, but the game will not attempt to load it
arkfiles += process_textures(
    platform,
    Path("custom_textures", "animated_gems", "gem_cymbal_diffuse_rb4"),
    Path("ui", "track", "animated_gems", "gem_cymbal_diffuse_rb4"),
    "rb4_anim1",
    "",
)

arkfiles += process_textures(
    platform,
    Path("custom_textures", "animated_gems", "prism_gem_keyboard_style_rb4"),
    Path("ui", "track", "animated_gems", "prism_gem_keyboard_style_rb4"),
    "rb4_anim2",
    "",
)

arkfiles += process_textures(
    platform,
    Path("custom_textures", "animated_gems", "prism_gems_rb4"),
    Path("ui", "track", "animated_gems", "prism_gems_rb4"),
    "rb4_anim3",
    "",
)

# build ark
buildfiles += generate_ark(platform, arkfiles)

ninja.build("all", "phony", buildfiles)