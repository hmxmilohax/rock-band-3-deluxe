#!/usr/bin/python3
from lib import ninja_syntax
from pathlib import Path
import sys
import argparse

parser = argparse.ArgumentParser(prog="configure")
parser.add_argument("platform")
parser.add_argument(
    "--fun", action="store_true", help="break CI and annoy Dark at the same time"
)

parser.add_argument(
    "--no-updates", action="store_true", help="disable dx song updates"
)
parser.add_argument("--define", action="append", help="Defines a macro in dx_build_marcos.dta, for debugging")


args = parser.parse_args()

def print_color_text(*args):
    text = " ".join(map(str, args[:-1]))
    color_code = args[-1]
    print(f"\033[{color_code}m{text}\033[0m")

if args.fun:
    print_color_text(f"▛▀▖      ▌   ▛▀▖        ▌ ▞▀▖ ▛▀▖   ▜          ", "1;36")  # Cyan text
    print_color_text(f"▙▄▘▞▀▖▞▀▖▌▗▘ ▙▄▘▝▀▖▛▀▖▞▀▌  ▄▘ ▌ ▌▞▀▖▐ ▌ ▌▚▗▘▞▀▖", "1;36")  # Cyan text
    print_color_text(f"▌▚ ▌ ▌▌ ▖▛▚  ▌ ▌▞▀▌▌ ▌▌ ▌ ▖ ▌ ▌ ▌▛▀ ▐ ▌ ▌▗▚ ▛▀ ", "1;36")  # Cyan text
    print_color_text(f"▘ ▘▝▀ ▝▀ ▘ ▘ ▀▀ ▝▀▘▘ ▘▝▀▘ ▝▀  ▀▀ ▝▀▘ ▘▝▀▘▘ ▘▝▀▘", "1;36")  # Cyan text
    match args.platform:
        case "ps3":
            print_color_text(f"Platform: {args.platform}", "1;38;5;196")
        case "xbox":
            print_color_text(f"Platform: {args.platform}", "1;32")
        case "wii":
            print_color_text(f"Platform: {args.platform}", "1;36")
else:
    print("Configuring Rock Band 3 Deluxe...")
    print(f"Platform: {args.platform}")

ninja = ninja_syntax.Writer(open("build.ninja", "w+"))

# configure tools
# TODO: clean this up
ark_dir = Path("obj", args.platform, "ark")
match sys.platform:
    case "win32":
        ninja.variable("silence", ">nul")
        ninja.rule("copy", "cmd /c copy $in $out $silence", description="COPY $in")
        ninja.rule("bswap", "dependencies\\windows\\swap_art_bytes.exe $in $out", description="BSWAP $in")
        ninja.rule("version", "python dependencies\\python\\gen_version.py $out", description="Writing version info")
        ninja.rule("song_update_hash", "python dependencies\\python\\gen_song_update_hash.py $out", description="Writing song hash")
        ninja.rule("defines", "python dependencies\\python\\gen_defines.py $out $defines", description="Generating build defines")
        ninja.rule("png_list", "python dependencies\\python\\png_list.py $dir $out", description="PNGLIST $dir")
        ninja.rule("generate_theme_data", "python dependencies\\python\\generate_theme_data.py $dir $out", description="THEMEDATA $dir")
        match args.platform:
            case "ps3":
                ninja.variable("superfreq", "dependencies\\windows\\superfreq.exe")
            case "xbox":
                ninja.variable("superfreq", "dependencies\\windows\\superfreq.exe")
            case "wii":
                ninja.variable("superfreq", "dependencies\\windows\\superfreq_wii.exe")
        ninja.variable("arkhelper", "dependencies\\windows\\arkhelper.exe")
        ninja.variable("dtab", "dependencies\\windows\\dtab.exe")
        ninja.variable("dtacheck", "dependencies\\windows\\dtacheck.exe")
        ninja.variable("prefabulous", "dependencies\\windows\\prefabulous.exe")
        ninja.rule("prefab_import", 'cmd /c ""%prefabulous%" "%scene%" "%in%" && type nul > "%out%""', description="PREFAB %in% -> %scene%", pool="console",)
    case "darwin":
        ninja.variable("silence", "> /dev/null")
        ninja.rule("copy", "cp $in $out", description="COPY $in")
        ninja.rule("bswap", "python3 dependencies/python/swap_rb_art_bytes.py $in $out", description="BSWAP $in")
        ninja.rule("version", "python3 dependencies/python/gen_version.py $out", description="Writing version info")
        ninja.rule("song_update_hash", "python3 dependencies/python/gen_song_update_hash.py $out", description="Writing song hash")
        ninja.rule("defines", "python3 dependencies/python/gen_defines.py $out $defines", description="Generating build defines")
        ninja.rule("png_list", "python3 dependencies/python/png_list.py $dir $out", description="PNGLIST $dir")
        ninja.rule("generate_theme_data", "python3 dependencies/python/generate_theme_data.py $dir $out", description="THEMEDATA $dir")
        match args.platform:
            case "ps3":
                ninja.variable("superfreq", "dependencies/macos/superfreq")
            case "xbox":
                ninja.variable("superfreq", "dependencies/macos/superfreq")
            case "wii":
                ninja.variable("superfreq", "dependencies/macos/superfreq_wii")
        ninja.variable("arkhelper", "dependencies/macos/arkhelper")
        ninja.variable("dtab", "dependencies/macos/dtab")
        ninja.variable("dtacheck", "dependencies/macos/dtacheck")
        ninja.variable("prefabulous", "dependencies/macos/prefabulous")  # or linux path
        ninja.rule("prefab_import", '"$prefabulous" "$scene" "$in" && touch "$out"', description="PREFAB $in -> $scene", pool="console",)
    case "linux":
        ninja.variable("silence", "> /dev/null")
        ninja.rule("copy", "cp --reflink=auto $in $out",description="COPY $in")
        ninja.rule("bswap", "dependencies/linux/swap_art_bytes $in $out", "BSWAP $in")
        ninja.rule("version", "python dependencies/python/gen_version.py $out", description="Writing version info")
        ninja.rule("song_update_hash", "python dependencies/python/gen_song_update_hash.py $out", description="Writing song hash")
        ninja.rule("defines", "python dependencies/python/gen_defines.py $out $defines", description="Generating build defines")
        ninja.rule("png_list", "python dependencies/python/png_list.py $dir $out", description="PNGLIST $dir")
        ninja.rule("generate_theme_data", "python dependencies/python/generate_theme_data.py $dir $out", description="THEMEDATA $dir")
        match args.platform:
            case "ps3":
                ninja.variable("superfreq", "dependencies/linux/superfreq")
            case "xbox":
                ninja.variable("superfreq", "dependencies/linux/superfreq")
            case "wii":
                ninja.variable("superfreq", "dependencies/linux/superfreq_wii")
        ninja.variable("arkhelper", "dependencies/linux/arkhelper")
        ninja.variable("dtab", "dependencies/linux/dtab")
        ninja.variable("dtacheck", "dependencies/linux/dtacheck")
        ninja.variable("prefabulous", "dependencies/linux/prefabulous")
        ninja.rule("prefab_import", '"$prefabulous" "$scene" "$in" && touch "$out"', description="PREFAB $in -> $scene", pool="console",)

match args.platform:
    case "ps3":
        out_dir = Path("out", args.platform, "USRDIR", "gen")
        ninja.rule(
            "ark",
            f"$arkhelper dir2ark -n patch_ps3 -e -s 4073741823 -v 6 --logLevel error {ark_dir} {out_dir}",
            description="Building ark",
        )
    case "xbox":
        out_dir = Path("out", args.platform, "gen")
        ninja.rule(
            "ark",
            f"$arkhelper dir2ark -n patch_xbox -e -v 6 -s 4073741823 --logLevel error {ark_dir} {out_dir}",
            description="Building ark",
        )
    case "wii":
        out_dir = Path("out", args.platform, "files")
        ninja.rule(
            "ark",
            f"$arkhelper patchcreator -a {ark_dir} -o {out_dir} platform/wii/files/gen/main_wii.hdr platform/wii/sys/main.dol --logLevel error",
            description="Building ark",
        )

ninja.rule(
    "sfreq",
    "$superfreq png2tex -l error --miloVersion 26 --platform $platform $in $out $flags",
    description="SFREQ $in"
)

ninja.rule("dtacheck", "$dtacheck $in .dtacheckfns", description="DTACHECK $in")
ninja.rule("dtab_serialize", "$dtab -b $in $out", description="DTAB SER $in")
ninja.rule("dtab_encrypt", "$dtab -e $in $out", description="DTAB ENC $in")
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
    # macos fucking sucks actually
    if ".DS_Store" in file.parts:
        return False
    if file.is_dir():
        return False
    if file.name.startswith("prefabs.milo_"):
        return False
    if file.suffix.endswith("_ps3") and args.platform != "ps3":
        return False
    if file.suffix.endswith("_xbox") and args.platform != "xbox":
        return False
    if file.suffix.endswith("_wii") and args.platform != "wii":
        return False
    if (args.platform == "wii"  or args.no_updates) and file.parts[slice(2)] == ("_ark", "songs"):
        return False
    if file.name.endswith("_update.txt"):
        return False

    return True

# build ark files
ark_files = []

mip_entries = {
    # outputted textures are DXT1, and they have very weird behavior with a 2-3 mipmap level
    # just commenting them out for now
    # Highway
    Path("_ark", "dx", "custom_textures", "highways"): 6,

    # Streak
    Path("_ark", "dx", "custom_textures", "streaks"): 6,

    # Overdrive
    Path("_ark", "dx", "custom_textures", "overdrive"): 5,

    # Keyboard
    #Path("_ark", "dx", "custom_textures", "_additional_textures", "pk_song_key"): 2,
    #Path("_ark", "dx", "custom_textures", "keyboard", "keyboard_lanes"): 2,
    #Path("_ark", "dx", "custom_textures", "keyboard", "keyboard_press"): 3,

    # Rails
    #Path("_ark", "dx", "custom_textures", "rails", "rails_track"): 3,
    #Path("_ark", "dx", "custom_textures", "rails", "rails_bracket"): 3,

    # Multiplier ring
    Path("_ark", "dx", "custom_textures", "multiplier_ring", "multiplier_ring_fx_stripes"): 4,
    #Path("_ark", "dx", "custom_textures", "multiplier_ring", "multiplier_ring_glow"): 3,
    #Path("_ark", "dx", "custom_textures", "multiplier_ring", "multiplier_ring_bg"): 3,
    #Path("_ark", "dx", "custom_textures", "multiplier_ring", "multiplier_ring_lens"): 3,
    #Path("_ark", "dx", "custom_textures", "multiplier_ring", "multiplier_ring_lens_vox"): 3,
    #Path("_ark", "dx", "custom_textures", "multiplier_ring", "multiplier_ring_plate"): 3,
    #Path("_ark", "dx", "custom_textures", "multiplier_ring", "multiplier_ring_plate_fc"): 3,

    # Gems
    Path("_ark", "dx", "custom_textures", "gems", "gems_default"): 5,
    Path("_ark", "dx", "custom_textures", "gems", "gems_emissive"): 5,
    Path("_ark", "dx", "custom_textures", "gems", "gems_hopo"): 5,
    Path("_ark", "dx", "custom_textures", "gems", "gems_emissive_hopo"): 5,
    #Path("_ark", "dx", "custom_textures", "gems", "gems_emissive_dynamic"): 2,
    Path("_ark", "dx", "custom_textures", "gems", "gems_keys"): 4,
    Path("_ark", "dx", "custom_textures", "gems", "gems_cymbals"): 5,
    Path("_ark", "dx", "custom_textures", "gems", "gems_cymbals_emissive"): 5,
    Path("_ark", "dx", "custom_textures", "gems", "gems_gliss"): 4,

    # Strikeline
    #Path("_ark", "dx", "custom_textures", "strikeline", "strikeline_green"): 2,
    #Path("_ark", "dx", "custom_textures", "strikeline", "strikeline_red"): 2,
    #Path("_ark", "dx", "custom_textures", "strikeline", "strikeline_yellow"): 2,
    #Path("_ark", "dx", "custom_textures", "strikeline", "strikeline_blue"): 2,
    #Path("_ark", "dx", "custom_textures", "strikeline", "strikeline_orange"): 2,

    # Flares
    #Path("_ark", "dx", "custom_textures", "flares", "flares_guitar_inner"): 3,
    #Path("_ark", "dx", "custom_textures", "flares", "flares_guitar_outer"): 2,
    #Path("_ark", "dx", "custom_textures", "flares", "flares_guitar_style"): 2,
    #Path("_ark", "dx", "custom_textures", "flares", "flares_inner"): 3,
    Path("_ark", "dx", "custom_textures", "flares", "flares_outer"): 4,
    #Path("_ark", "dx", "custom_textures", "flares", "flares_style"): 3,

    # Particles
    #Path("_ark", "dx", "custom_textures", "particles", "particles_gem_cap"): 3,
    Path("_ark", "dx", "custom_textures", "particles", "particles_glass1"): 4,
    #Path("_ark", "dx", "custom_textures", "particles", "particles_glass1_neg"): 3,
    #Path("_ark", "dx", "custom_textures", "particles", "particles_glass2"): 3,
    Path("_ark", "dx", "custom_textures", "particles", "particles_shockwave"): 5,
    #Path("_ark", "dx", "custom_textures", "particles", "particles_smoke"): 3,
    #Path("_ark", "dx", "custom_textures", "particles", "particles_spark"): 3,
    Path("_ark", "dx", "custom_textures", "particles", "particles_sparks_radial"): 4,
    Path("_ark", "dx", "custom_textures", "particles", "particles_sparks_vertical"): 4,

    # Score box
    #Path("_ark", "dx", "custom_textures", "score", "scoreboard_frame"): 3,
    #Path("_ark", "dx", "custom_textures", "score", "scoreboard_lens"): 3,
    #Path("_ark", "dx", "custom_textures", "score", "star_multiplier_meter_frame"): 4,
    #Path("_ark", "dx", "custom_textures", "score", "star_multiplier_meter_lens"): 4,

    # Font
    Path("_ark", "dx", "custom_textures", "font"): 6,

    # Solo box
    Path("_ark", "dx", "custom_textures", "solo_box"): 4,

    # Big rock ending
    Path("_ark", "dx", "custom_textures", "bre", "bre_shield"): 5,
    Path("_ark", "dx", "custom_textures", "bre", "bre_black_wing"): 5,
    #Path("_ark", "dx", "custom_textures", "bre", "bre_blossom"): 3,

    # Crowd meter
    #Path("_ark", "dx", "custom_textures", "crowd_meter", "crowd_meter_frame"): 3,
    #Path("_ark", "dx", "custom_textures", "crowd_meter", "crowd_meter_lens"): 3,

    # Stars
    #Path("_ark", "dx", "custom_textures", "stars", "score_star_frame"): 3,
    #Path("_ark", "dx", "custom_textures", "stars", "score_star_gold"): 3,
    #Path("_ark", "dx", "custom_textures", "stars", "score_star_gold_flash"): 3,
    #Path("_ark", "dx", "custom_textures", "stars", "score_star_crimson"): 3,
    Path("_ark", "dx", "custom_textures", "stars", "score_tour_icon"): 4,

    # Beat lines
    #Path("_ark", "dx", "custom_textures", "rails", "beat_lines"): 2,

    # Overdrive bar
    #Path("_ark", "dx", "custom_textures", "overdrive_bar", "od_bar_sun_fx"): 3,
    Path("_ark", "dx", "custom_textures", "overdrive_bar", "od_bar_background"): 4,
    #Path("_ark", "dx", "custom_textures", "overdrive_bar", "od_bar_lens"): 2,
    #Path("_ark", "dx", "custom_textures", "overdrive_bar", "od_bar_long"): 2,

    # Vocal highway
    Path("_ark", "dx", "custom_textures", "vocal_highway", "vocal_highway_bg"): 4,
    Path("_ark", "dx", "custom_textures", "vocal_highway", "vocal_highway_no_tonic"): 4,
    #Path("_ark", "dx", "custom_textures", "vocal_highway", "vocal_highway_bg_blue"): 2,
    #Path("_ark", "dx", "custom_textures", "vocal_highway", "vocal_highway_bg_brown"): 2,

    # Vocal arrows
    #Path("_ark", "dx", "custom_textures", "vocal_arrows", "vocal_arrow"): 4,
    #Path("_ark", "dx", "custom_textures", "vocal_arrows", "vocal_arrow_outline"): 4,

    # Vocal notes
    Path("_ark", "dx", "custom_textures", "vocal_note", "vocal_note_tube"): 5,
    #Path("_ark", "dx", "custom_textures", "vocal_note", "vocal_note_talkie"): 4,
    Path("_ark", "dx", "custom_textures", "vocal_note", "vocal_note_tamb_gem"): 4,
    Path("_ark", "dx", "custom_textures", "vocal_note", "vocal_note_off"): 4,
    Path("_ark", "dx", "custom_textures", "vocal_note", "vocal_note_on"): 4,

    # Additional textures
    Path("_ark", "dx", "custom_textures", "_additional_textures", "countdown_circle.png"): 4,
    Path("_ark", "dx", "custom_textures", "_additional_textures", "countdown_circle_meter_wipe.png"): 4,
}

# (dark): i love O(n*m) complexity
def find_mip_entry(path: Path):
    for key, value in mip_entries.items():
        if path.is_relative_to(key):
            return value

    return None

for f in filter(ark_file_filter, Path("_ark").rglob("*")):
    match f.suffixes:
        case [".png"]:
            output_directory = Path("obj", args.platform, "ark").joinpath(
                *f.parent.parts[1:]
            )

            variables = {}
            mip_level = find_mip_entry(f)

            if mip_level != None:
                variables["flags"] = "--mipmaps %d" % mip_level

            match args.platform:
                case "ps3":
                    variables["platform"] = "x360"
                    target_filename = Path("gen", f.stem + ".png_ps3")
                    xbox_filename = Path("gen", f.stem + ".png_xbox")
                    xbox_directory = Path("obj", args.platform, "raw").joinpath(
                        *f.parent.parts[1:]
                    )
                    xbox_output = xbox_directory.joinpath(xbox_filename)
                    ps3_output = output_directory.joinpath(target_filename)
                    ninja.build(str(xbox_output), "sfreq", str(f), variables=variables)
                    ninja.build(str(ps3_output), "bswap", str(xbox_output))
                    ark_files.append(str(ps3_output))
                case "xbox":
                    variables["platform"] = "x360"
                    target_filename = Path("gen", f.stem + ".png_xbox")
                    xbox_directory = Path("obj", args.platform, "ark").joinpath(
                        *f.parent.parts[1:]
                    )
                    xbox_output = xbox_directory.joinpath(target_filename)
                    ninja.build(str(xbox_output), "sfreq", str(f), variables=variables)
                    ark_files.append(str(xbox_output))
                case "wii":
                    variables = {"platform": "wii"}
                    target_filename = Path("gen", f.stem + ".png_wii")
                    wii_directory = Path("obj", args.platform, "ark").joinpath(
                        *f.parent.parts[1:]
                    )
                    wii_output = wii_directory.joinpath(target_filename)
                    ninja.build(str(wii_output), "sfreq", str(f), variables=variables)
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
            if not out_path.name.endswith("_update.txt"):
                ninja.build(str(out_path), "copy", str(f))
                ark_files.append(str(out_path))

if args.platform in ("ps3", "xbox"):
    milo_name = f"prefabs.milo_{'ps3' if args.platform == 'ps3' else 'xbox'}"

    # Prefer main/shared, fallback to shared
    src_candidates = [
        Path("_ark", "char", "main", "shared", "gen", milo_name),
        Path("_ark", "char", "shared", "gen", milo_name),
    ]
    src_scene = next((p for p in src_candidates if p.exists()), None)

    staged_scene = Path("obj", args.platform, "ark", "char", "main", "shared", "gen", milo_name)

    if src_scene is not None:
        # Always stage the base scene (this ensures it lands in obj/... even if no prefabs to add)
        ninja.build(str(staged_scene), "copy", str(src_scene))
        ark_files.append(str(staged_scene))

        custom_dir = Path("_ark", "char", "custom_prefabs")
        if custom_dir.exists() and src_scene is not None:
            stamps_dir = Path("obj", args.platform, "stamps")
            stamps_dir.mkdir(parents=True, exist_ok=True)

            last_stamp = None
            for pf in sorted(custom_dir.iterdir()):
                if not (pf.is_file() and pf.suffix == "" and pf.name != ".gitkeep"):
                    continue

                stamp = stamps_dir / f"prefab_{pf.name}.stamp"

                implicit_inputs = [str(staged_scene)]
                if last_stamp is not None:
                    implicit_inputs.append(str(last_stamp))

                # NOTE: pf is the *explicit input*, so rule can use $in
                ninja.build(
                    str(stamp),
                    "prefab_import",
                    str(pf),
                    implicit=implicit_inputs,
                    variables={"scene": str(staged_scene)},
                )
                ark_files.append(str(stamp))
                last_stamp = stamp

# write version info
dta = Path("obj", args.platform, "raw", "dx", "locale", "dx_version.dta")
dtb = Path("obj", args.platform, "raw", "dx", "locale", "gen", "dx_version.dtb")
enc = Path("obj", args.platform, "ark", "dx", "locale", "gen", "dx_version.dtb")

ninja.build(str(dta), "version", implicit="_always")
ninja.build(str(dtb), "dtab_serialize", str(dta))
ninja.build(str(enc), "dtab_encrypt", str(dtb))

ark_files.append(str(enc))

# generate song update hash
dta = Path("obj", args.platform, "raw", "dx", "dx_song_update_hash.dta")
dtb = Path("obj", args.platform, "raw", "dx", "gen", "dx_song_update_hash.dtb")
enc = Path("obj", args.platform, "ark", "dx", "gen", "dx_song_update_hash.dtb")

ninja.build(str(dta), "song_update_hash", implicit="_always")
ninja.build(str(dtb), "dtab_serialize", str(dta))
ninja.build(str(enc), "dtab_encrypt", str(dtb))

ark_files.append(str(enc))

# generate build defines
dta = Path("obj", args.platform, "raw", "dx", "macros", "dx_build_macros.dta")
dtb = Path("obj", args.platform, "raw", "dx", "macros", "gen", "dx_build_macros.dtb")
enc = Path("obj", args.platform, "ark", "dx", "macros", "gen", "dx_build_macros.dtb")

ninja.build(str(dta), "defines", implicit="_always", variables={"defines": " ".join(args.define) if args.define else None})
ninja.build(str(dtb), "dtab_serialize", str(dta))
ninja.build(str(enc), "dtab_encrypt", str(dtb))

ark_files.append(str(enc))

# generate texture lists
def generate_file_list(input_path: Path):
    base = input_path.parts[1:]
    dta = Path("obj", args.platform, "raw").joinpath(*base).joinpath("_list.dta")
    dtb = Path("obj", args.platform, "raw").joinpath(*base).joinpath("gen", "_list.dtb")
    enc = Path("obj", args.platform, "ark").joinpath(*base).joinpath("gen", "_list.dtb")
    ninja.build(str(dta), "png_list", variables={"dir": str(input_path)}, implicit="_always")
    ninja.build(str(dtb), "dtab_serialize", str(dta))
    ninja.build(str(enc), "dtab_encrypt", str(dtb))

def generate_theme_data(input_path: Path):
    base = input_path.parts[1:]
    dta = Path("obj", args.platform, "raw").joinpath(*base).joinpath("_themedata.dta")
    dtb = Path("obj", args.platform, "raw").joinpath(*base).joinpath("gen", "_themedata.dtb")
    enc = Path("obj", args.platform, "ark").joinpath(*base).joinpath("gen", "_themedata.dtb")
    ninja.build(str(dta), "generate_theme_data", variables={"dir": str(input_path)}, implicit="_always")
    ninja.build(str(dtb), "dtab_serialize", str(dta))
    ninja.build(str(enc), "dtab_encrypt", str(dtb))

generate_file_list(Path("_ark", "dx", "custom_textures", "highways"))
generate_file_list(Path("_ark", "dx", "custom_textures", "streaks"))
generate_file_list(Path("_ark", "dx", "custom_textures", "overdrive"))
generate_file_list(Path("_ark", "dx", "custom_textures", "gems", "gems_default"))
generate_file_list(Path("_ark", "dx", "custom_textures", "strikeline", "strikeline_guitar"))
generate_file_list(Path("_ark", "dx", "custom_textures", "flares", "flares_guitar_style"))
generate_file_list(Path("_ark", "dx", "custom_textures", "particles", "particles_spark"))
generate_file_list(Path("_ark", "dx", "custom_textures", "sustains"))
generate_file_list(Path("_ark", "dx", "custom_textures", "score", "scoreboard_frame"))
generate_file_list(Path("_ark", "dx", "custom_textures", "rails", "beat_lines"))
generate_file_list(Path("_ark", "dx", "custom_textures", "stars", "score_star_frame"))
generate_file_list(Path("_ark", "dx", "custom_textures", "font"))
generate_file_list(Path("_ark", "dx", "custom_textures", "solo_box"))
generate_file_list(Path("_ark", "dx", "custom_textures", "bre", "bre_shield"))
generate_file_list(Path("_ark", "dx", "custom_textures", "rails", "rails_track"))
generate_file_list(Path("_ark", "dx", "custom_textures", "lanes", "gem_mash_green_emmisive"))
generate_file_list(Path("_ark", "dx", "custom_textures", "overdrive_bar", "od_bar_background"))
generate_file_list(Path("_ark", "dx", "custom_textures", "multiplier_ring", "multiplier_ring_plate_fc"))
generate_file_list(Path("_ark", "dx", "custom_textures", "crowd_meter", "crowd_meter_frame"))
generate_file_list(Path("_ark", "dx", "custom_textures", "keyboard", "keyboard_lanes"))
generate_file_list(Path("_ark", "dx", "custom_textures", "vocal_highway", "vocal_highway_bg"))
generate_file_list(Path("_ark", "dx", "custom_textures", "vocal_arrows", "vocal_arrow"))
generate_file_list(Path("_ark", "dx", "custom_textures", "vocal_note", "vocal_note_tube"))
generate_file_list(Path("_ark", "dx", "custom_textures", "vocal_overdrive", "vocal_overdrive_now_bar"))

generate_file_list(Path("_ark", "dx", "models", "gems"))
generate_theme_data(Path("_ark", "dx", "models", "gems"))

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

# make the all target build everything
ninja.build("all", "phony", build_files)
ninja.close()