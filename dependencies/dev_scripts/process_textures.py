# process_textures.py
from pathlib import Path
import subprocess

# per jnack:
# It makes a dta listing all the files in the emissive folder in the destination format, 
# converts images of various types to a uniform png, 
# then makes png_xbox and png_ps3 files, 
# and moves them into _ark

# EMISSIVES/HIGHWAYS/SPOTLIGHTS
# input folder: custom_textures/[EMISSIVES/HIGHWAYS/SPOTLIGHTS]
# output folder: _ark/ui/track/[EMISSIVES/HIGHWAYS/SPOTLIGHTS]
# take the images in the input folder, take their names, and put them in the output folder's dta
# add the image names and put them in slot_states.dta
# convert input images to pngs - REMEMBER: EACH TEXTURE ASSET USES A DIFFERENT COMMAND FOR PNG CONVERSION
# then convert pngs to png_xbox's/ps3's

# CUSTOM TRACK TEXTURES/OVERSHELL
# keep in mind overshell's output directory is different than custom track textures' output directory
# convert input images to pngs - REMEMBER: EACH TEXTURE ASSET USES A DIFFERENT COMMAND FOR PNG CONVERSION
# then convert pngs to png_xbox's/ps3's

# GEMS
# KEYBOARDS
# SMASHERS

def process_images(input_path: Path, output_path: Path, which_texture: str):
    print("Processing the provided images...")

    if which_texture == "highway":
        addnl_params = "-resize 256x512! -filter Box"
    elif which_texture == "emissive":
        addnl_params = "-resize 256x512! -filter Box -alpha set -background none -channel A -evaluate multiply 0.5 +channel"
    elif which_texture == "spotlight":
        addnl_params = "-resize 256x512! -filter Box -alpha set -background none +channel"
    else:
        addnl_params = ""

    # convert every image to .png
    for texture in input_path.glob("*"):
        if texture.suffix == ".png" or texture.suffix == ".jpg" or texture.suffix == ".bmp":
            cmd_convert_png = f"dependencies\magick\magick.exe convert {input_path}\{texture.name} {addnl_params} {input_path}\{texture.stem}.png".split()
            subprocess.run(cmd_convert_png, shell=True, cwd="..")

    # convert images to .png_xbox/ps3 and move them to output_path
    for new_texture in input_path.glob("*"):
        if new_texture.suffix == ".png":
            cmd_xbox = f"dependencies\superfreq.exe png2tex {input_path}\{new_texture.name} {output_path}\{new_texture.stem}.png_xbox --platform x360 --miloVersion 26".split()
            subprocess.run(cmd_xbox, shell=True, cwd="..")
            cmd_ps3 = f"python dependencies\dev_scripts\swap_rb_art_bytes.py {output_path}\{new_texture.stem}.png_xbox {output_path}\{new_texture.stem}.png_ps3".split()
            subprocess.run(cmd_ps3, shell=True, cwd="..", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

def generate_dtas(input_path: Path, output_path: Path, which_texture: str):
    root_dir = Path().absolute().parents[0] # root directory of the repo
    print("Generating the necessary dtas...")

    texture_dta = [texture.stem for texture in input_path.glob("*")]
    texture_dta.sort()

    with open(output_path.joinpath(f"{which_texture}s.dta"), "w", encoding="ISO-8859-1") as dta_output:
        for asdf in texture_dta:
            dta_output.write(f"\"{asdf}\"\n")

    # slot_states.dta stuff goes here
    # open and write into slot_states.dta
    with open(root_dir.joinpath("_ark/ui/overshell/slot_states.dta"), "r", encoding="ISO-8859=1") as f:
        slot_states_dta = [line for line in f.readlines()]

    for i in range(len(slot_states_dta)):
        if f"; paste your {which_texture}s.dta contents here" in slot_states_dta[i]:
            threshold_begin = i
        elif f"; end {which_texture}s.dta contents" in slot_states_dta[i]:
            threshold_end = i
            break

    leading_spaces = len(slot_states_dta[threshold_begin]) - len(slot_states_dta[threshold_begin].lstrip())
    slot_state_additions = []
    slot_state_additions.append(f"{' ' * leading_spaces}(\n")
    for addition in texture_dta:
        slot_state_additions.append(f"{' ' * (leading_spaces + 2)}\"{addition}\"\n")
    slot_state_additions.append(f"{' ' * leading_spaces})\n")

    new_slot_states_dta = slot_states_dta[:threshold_begin+1]
    new_slot_states_dta.extend(slot_state_additions)
    new_slot_states_dta.extend(slot_states_dta[threshold_end:])

    with open(root_dir.joinpath("_ark/ui/overshell/slot_states.dta"), "w", encoding="ISO-8859=1") as ff:
        ff.writelines(new_slot_states_dta)

def generate_dtas_concise(input_path: Path, output_path: Path, which_texture: str):
    root_dir = Path().absolute().parents[0] # root directory of the repo
    print("Generating the necessary dtas...")

    texture_dta = []

    for texture in input_path.glob("*"):
        if "rb2" in texture.stem and "rb2" not in texture_dta:
            texture_dta.append("rb2")
        elif "rb3" in texture.stem and "rb3" not in texture_dta:
            texture_dta.append("rb3")
        elif "rb4" in texture.stem and "rb4" not in texture_dta:
            texture_dta.append("rb4")

    texture_dta.sort()

    with open(output_path.joinpath(f"{which_texture}s.dta"), "w", encoding="ISO-8859-1") as dta_output:
        for asdf in texture_dta:
            dta_output.write(f"\"{asdf}\"\n")

    # slot_states.dta stuff goes here
    # open and write into slot_states.dta
    with open(root_dir.joinpath("_ark/ui/overshell/slot_states.dta"), "r", encoding="ISO-8859=1") as f:
        slot_states_dta = [line for line in f.readlines()]

    for i in range(len(slot_states_dta)):
        if f"; paste your {which_texture}s.dta contents here" in slot_states_dta[i]:
            threshold_begin = i
        elif f"; end {which_texture}s.dta contents" in slot_states_dta[i]:
            threshold_end = i
            break

    leading_spaces = len(slot_states_dta[threshold_begin]) - len(slot_states_dta[threshold_begin].lstrip())
    slot_state_additions = []
    slot_state_additions.append(f"{' ' * leading_spaces}(\n")
    for addition in texture_dta:
        slot_state_additions.append(f"{' ' * (leading_spaces + 2)}\"{addition}\"\n")
    slot_state_additions.append(f"{' ' * leading_spaces})\n")

    new_slot_states_dta = slot_states_dta[:threshold_begin+1]
    new_slot_states_dta.extend(slot_state_additions)
    new_slot_states_dta.extend(slot_states_dta[threshold_end:])

    with open(root_dir.joinpath("_ark/ui/overshell/slot_states.dta"), "w", encoding="ISO-8859=1") as ff:
        ff.writelines(new_slot_states_dta)

def generate_dtas_keyboard(input_path: Path, output_path: Path, which_texture: str):
    root_dir = Path().absolute().parents[0] # root directory of the repo
    print("Generating the necessary dtas...")

    texture_dta = []

    for texture in input_path.glob("*"):
        final_texture_name = texture.stem.replace("gem_mash_prokeys_","").replace("gem_smasher_sharp_diffuse_nomip_","").replace("track_lanes_keyboard_","").replace("track_lanes_keyboard_press_","")
        if final_texture_name not in texture_dta:
            texture_dta.append(final_texture_name)

    texture_dta.sort()

    with open(output_path.joinpath(f"{which_texture}s.dta"), "w", encoding="ISO-8859-1") as dta_output:
        for asdf in texture_dta:
            dta_output.write(f"\"{asdf}\"\n")

    # slot_states.dta stuff goes here
    # open and write into slot_states.dta
    with open(root_dir.joinpath("_ark/ui/overshell/slot_states.dta"), "r", encoding="ISO-8859=1") as f:
        slot_states_dta = [line for line in f.readlines()]

    for i in range(len(slot_states_dta)):
        if f"; paste your {which_texture}s.dta contents here" in slot_states_dta[i]:
            threshold_begin = i
        elif f"; end {which_texture}s.dta contents" in slot_states_dta[i]:
            threshold_end = i
            break

    leading_spaces = len(slot_states_dta[threshold_begin]) - len(slot_states_dta[threshold_begin].lstrip())
    slot_state_additions = []
    slot_state_additions.append(f"{' ' * leading_spaces}(\n")
    for addition in texture_dta:
        slot_state_additions.append(f"{' ' * (leading_spaces + 2)}\"{addition}\"\n")
    slot_state_additions.append(f"{' ' * leading_spaces})\n")

    new_slot_states_dta = slot_states_dta[:threshold_begin+1]
    new_slot_states_dta.extend(slot_state_additions)
    new_slot_states_dta.extend(slot_states_dta[threshold_end:])

    with open(root_dir.joinpath("_ark/ui/overshell/slot_states.dta"), "w", encoding="ISO-8859=1") as ff:
        ff.writelines(new_slot_states_dta)

def process_textures(which_texture: str):
    root_dir = Path().absolute().parents[0] # root directory of the repo

    if which_texture == "emissive":
        generate_dtas(input_path=root_dir.joinpath("custom_textures/emissives"), output_path=root_dir.joinpath("_ark/ui/track/emissives"), which_texture="emissive")
        process_images(input_path=root_dir.joinpath("custom_textures/emissives"), output_path=root_dir.joinpath("_ark/ui/track/emissives/gen"), which_texture="emissive")
        print("Successfully implemented custom emissive textures on the RB3DX ark. Please rebuild in order to see them reflected in-game.")
    elif which_texture == "highway":
        generate_dtas(input_path=root_dir.joinpath("custom_textures/highways"), output_path=root_dir.joinpath("_ark/ui/track/highways"), which_texture="highway")
        process_images(input_path=root_dir.joinpath("custom_textures/highways"), output_path=root_dir.joinpath("_ark/ui/track/highways/gen"), which_texture="highway")
        print("Successfully implemented custom highway textures on the RB3DX ark. Please rebuild in order to see them reflected in-game.")
    elif which_texture == "spotlight":
        generate_dtas(input_path=root_dir.joinpath("custom_textures/spotlights"), output_path=root_dir.joinpath("_ark/ui/track/spotlights"), which_texture="spotlight")
        process_images(input_path=root_dir.joinpath("custom_textures/spotlights"), output_path=root_dir.joinpath("_ark/ui/track/spotlights/gen"), which_texture="spotlight")
        print("Successfully implemented custom spotlight textures on the RB3DX ark. Please rebuild in order to see them reflected in-game.")
    elif which_texture == "custom_track":
        process_images(input_path=root_dir.joinpath("custom_textures/custom_track_textures"), output_path=root_dir.joinpath("_ark/ui/track/custom_track_textures/gen"), which_texture="custom_track")
        print("Successfully implemented custom track textures on the RB3DX ark. Please rebuild in order to see them reflected in-game.")
    elif which_texture == "overshell":
        process_images(input_path=root_dir.joinpath("custom_textures/overshell/rb4_early"), output_path=root_dir.joinpath("_ark/ui/overshell/rb4_early/gen"), which_texture="overshell")
        print("Successfully implemented custom overshell textures on the RB3DX ark. Please rebuild in order to see them reflected in-game.")
    elif which_texture == "smasher":
        generate_dtas_concise(input_path=root_dir.joinpath("custom_textures/smashers"), output_path=root_dir.joinpath("_ark/ui/track/smashers"), which_texture="smasher")
        process_images(input_path=root_dir.joinpath("custom_textures/smashers"), output_path=root_dir.joinpath("_ark/ui/track/smashers/gen"), which_texture="smasher")
        print("Successfully implemented custom smasher textures on the RB3DX ark. Please rebuild in order to see them reflected in-game.")
    elif which_texture == "gem":
        generate_dtas_concise(input_path=root_dir.joinpath("custom_textures/gems"), output_path=root_dir.joinpath("_ark/ui/track/gems"), which_texture="gem")
        process_images(input_path=root_dir.joinpath("custom_textures/gems"), output_path=root_dir.joinpath("_ark/ui/track/gems/gen"), which_texture="gem")
        print("Successfully implemented custom gem textures on the RB3DX ark. Please rebuild in order to see them reflected in-game.")
    elif which_texture == "keyboard":
        generate_dtas_keyboard(input_path=root_dir.joinpath("custom_textures/keyboards"), output_path=root_dir.joinpath("_ark/ui/track/keyboards"), which_texture="keyboard")
        process_images(input_path=root_dir.joinpath("custom_textures/keyboards"), output_path=root_dir.joinpath("_ark/ui/track/keyboards/gen"), which_texture="keyboard")
        print("Successfully implemented custom keyboard textures on the RB3DX ark. Please rebuild in order to see them reflected in-game.")