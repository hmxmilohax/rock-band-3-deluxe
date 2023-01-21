# process_textures_highway.py
from pathlib import Path
import subprocess

# per jnack:
# It makes a dta listing all the files in the highway folder in the destination format, 
# converts images of various types to a uniform png, 
# then makes png_xbox and png_ps3 files, 
# and moves them into _ark

# directories used in this script
cwd = Path().absolute() # current working directory (user_scripts)
root_dir = Path(__file__).parents[1] # root directory of the repo
highway_dir = root_dir.joinpath("custom_textures/highways") # where the custom highway images are
highway_output_dir = root_dir.joinpath("_ark/ui/track/highways") # where the outputted highway dta and png_xbox/ps3s will go
output_dir = highway_output_dir.joinpath("gen") # the actual folder containing the png_xbox/ps3s

# retrieve custom highway image names, and convert them to pngs
highway_dta = []

for highway in highway_dir.glob("*"):
    if highway.suffix == ".png" or highway.suffix == ".jpg" or highway.suffix == ".bmp":
        print(highway.name)
        highway_dta.append(highway.stem)
        cmd_convert_png = f"dependencies\magick\magick.exe convert custom_textures\highways\{highway.name} -resize 256x512! -filter Box custom_textures\highways\{highway.name}".split()
        subprocess.run(cmd_convert_png, shell=True, cwd="..")

highway_dta.sort()

# write highway image names to highways.dta
with open(highway_output_dir.joinpath("highways.dta"), "w", encoding="ISO-8859-1") as dta_output:
    for asdf in highway_dta:
        dta_output.write(f"\"{asdf}\"\n")

# open and write into slot_states.dta
with open(root_dir.joinpath("_ark/ui/overshell/slot_states.dta"), "r", encoding="ISO-8859=1") as f:
    slot_states_dta = [line for line in f.readlines()]

for i in range(len(slot_states_dta)):
    if "; paste your highways.dta contents here" in slot_states_dta[i]:
        highway_index_begin = i
    elif "; end highways.dta contents" in slot_states_dta[i]:
        highway_index_end = i
        break

leading_spaces = len(slot_states_dta[highway_index_begin]) - len(slot_states_dta[highway_index_begin].lstrip())
slot_state_additions = []
slot_state_additions.append(f"{' ' * leading_spaces}(\n")
for addition in highway_dta:
    slot_state_additions.append(f"{' ' * (leading_spaces + 2)}\"{addition}\"\n")
slot_state_additions.append(f"{' ' * leading_spaces})\n")

new_slot_states_dta = slot_states_dta[:highway_index_begin+1]
new_slot_states_dta.extend(slot_state_additions)
new_slot_states_dta.extend(slot_states_dta[highway_index_end:])

with open(root_dir.joinpath("_ark/ui/overshell/slot_states.dta"), "w", encoding="ISO-8859=1") as ff:
    ff.writelines(new_slot_states_dta)

# convert png's for use on both xbox and ps3
for new_png in highway_dir.glob("*"):
    if new_png.suffix == ".png":
        cmd_xbox = f"dependencies\superfreq.exe png2tex custom_textures\highways\{new_png.name} _ark\\ui\\track\highways\gen\{new_png.stem}.png_xbox --platform x360 --miloVersion 26".split()
        subprocess.run(cmd_xbox, shell=True, cwd="..")
        cmd_ps3 = f"python dependencies\dev_scripts\swap_rb_art_bytes.py _ark\\ui\\track\highways\gen\{new_png.stem}.png_xbox _ark\\ui\\track\highways\gen\{new_png.stem}.png_ps3".split()
        subprocess.run(cmd_ps3, shell=True, cwd="..", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        
print("Successfully implemented custom highway textures on the RB3DX ark. Please rebuild in order to see them reflected in-game.")