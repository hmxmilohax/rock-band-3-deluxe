# process_textures.py
from pathlib import Path
from sys import platform
import subprocess

# per jnack:
# It makes a dta listing all the files in the [respective texture] folder in the destination format, 
# converts images of various types to a uniform png, 
# then makes png_xbox and png_ps3 files, 
# and moves them into _ark

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

    root_dir = Path().absolute().parents[0]

    relative_input_path = f"{str(input_path).replace(str(root_dir),'')}"[1:]
    relative_output_path = f"{str(output_path).replace(str(root_dir),'')}"[1:]

    # convert every image to .png
    for texture in input_path.glob("*"):
        if texture.suffix == ".png" or texture.suffix == ".jpg" or texture.suffix == ".bmp":
            if platform == "win32":
                cmd_convert_png = f"dependencies\magick\magick.exe convert {relative_input_path}\{texture.name} {addnl_params} {relative_input_path}\{texture.stem}.png".split()
            else:
                cmd_chmod_magick = "chmod +x dependencies/magick/magick".split()
                subprocess.run(cmd_chmod_magick, shell=(platform == "win32"), cwd="..")
                cmd_convert_png = f"dependencies/magick/magick convert {relative_input_path}/{texture.name} {addnl_params} {relative_input_path}/{texture.stem}.png".split()
            subprocess.run(cmd_convert_png, shell=(platform == "win32"), cwd="..")

    # convert images to .png_xbox/ps3 and move them to output_path
    for new_texture in input_path.glob("*"):
        if new_texture.suffix == ".png":
            # first, convert image from png to png_xbox
            if platform == "win32":
                cmd_xbox = f"dependencies\windows\superfreq.exe png2tex {relative_input_path}\{new_texture.name} {relative_output_path}\{new_texture.stem}.png_xbox --platform x360 --miloVersion 26".split()
            elif platform == "darwin":
                cmd_xbox = f"dependencies/macos/superfreq png2tex {relative_input_path}/{new_texture.name} {relative_output_path}/{new_texture.stem}.png_xbox --platform x360 --miloVersion 26".split()
            else:
                # if on linux/other OS, make binary executable
                cmd_chmod_superfreq = "chmod +x dependencies/superfreq".split()
                subprocess.run(cmd_chmod_superfreq, shell=(platform == "win32"), cwd="..")
                cmd_xbox = f"dependencies/linux/superfreq png2tex {relative_input_path}/{new_texture.name} {relative_output_path}/{new_texture.stem}.png_xbox --platform x360 --miloVersion 26".split()
            subprocess.run(cmd_xbox, shell=(platform == "win32"), cwd="..")
            # now, convert png_xboxes to png_ps3s
            if platform == "win32":
                cmd_ps3 = f"python dependencies\dev_scripts\swap_rb_art_bytes.py {relative_output_path}\{new_texture.stem}.png_xbox {relative_output_path}\{new_texture.stem}.png_ps3".split()
            else:
                cmd_ps3 = f"python dependencies/dev_scripts/swap_rb_art_bytes.py {relative_output_path}/{new_texture.stem}.png_xbox {relative_output_path}/{new_texture.stem}.png_ps3".split()
            subprocess.run(cmd_ps3, shell=(platform == "win32"), cwd="..", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

def generate_dtas(input_path: Path, output_path: Path, which_texture: str):
    root_dir = Path().absolute().parents[0] # root directory of the repo
    print("Generating the necessary dtas...")

    texture_dta = []

    if which_texture == "gem" or which_texture == "smasher":
        for texture in input_path.glob("*"):
            if "rb2" in texture.stem and "rb2" not in texture_dta:
                texture_dta.append("rb2")
            elif "rb3" in texture.stem and "rb3" not in texture_dta:
                texture_dta.append("rb3")
            elif "rb4" in texture.stem and "rb4" not in texture_dta:
                texture_dta.append("rb4")
    elif which_texture == "keyboard":
        for texture in input_path.glob("*"):
            final_texture_name = texture.stem.replace("gem_mash_prokeys_","").replace("gem_smasher_sharp_diffuse_nomip_","").replace("track_lanes_keyboard_","").replace("track_lanes_keyboard_press_","")
            if final_texture_name not in texture_dta:
                texture_dta.append(final_texture_name)
    else:
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

def process_textures(which_texture: str):
    root_dir = Path().absolute().parents[0] # root directory of the repo

    if which_texture == "emissive" or which_texture == "highway" or which_texture == "spotlight" or which_texture == "smasher" or which_texture == "gem" or which_texture == "keyboard":
        generate_dtas(input_path=root_dir.joinpath(f"custom_textures/{which_texture}s"), output_path=root_dir.joinpath(f"_ark/ui/track/{which_texture}s"), which_texture=which_texture)
        process_images(input_path=root_dir.joinpath(f"custom_textures/{which_texture}s"), output_path=root_dir.joinpath(f"_ark/ui/track/{which_texture}s/gen"), which_texture=which_texture)
        print(f"Successfully implemented custom {which_texture} textures on the Rock Band 3 Deluxe ark. Please rebuild in order to see them reflected in-game.")
    elif which_texture == "custom_track":
        process_images(input_path=root_dir.joinpath("custom_textures/custom_track_textures"), output_path=root_dir.joinpath("_ark/ui/track/custom_track_textures/gen"), which_texture="custom_track")
        print("Successfully implemented custom track textures on the Rock Band 3 Deluxe ark. Please rebuild in order to see them reflected in-game.")
    elif which_texture == "overshell":
        process_images(input_path=root_dir.joinpath("custom_textures/overshell/rb4_early"), output_path=root_dir.joinpath("_ark/ui/overshell/rb4_early/gen"), which_texture="overshell")
        print("Successfully implemented custom overshell textures on the Rock Band 3 Deluxe ark. Please rebuild in order to see them reflected in-game.")