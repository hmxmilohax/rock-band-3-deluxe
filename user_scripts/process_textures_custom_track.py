# process_textures_custom_track.py
from pathlib import Path
import subprocess

# per jnack:
# It makes a dta listing all the files in the custom track textures folder in the destination format, 
# converts images of various types to a uniform png, 
# then makes png_xbox and png_ps3 files, 
# and moves them into _ark

# directories used in this script
cwd = Path().absolute() # current working directory (user_scripts)
root_dir = Path(__file__).parents[1] # root directory of the repo
custom_img_dir = root_dir.joinpath("custom_textures/custom_track_textures") # where the custom track textures are
custom_output_dir = root_dir.joinpath("_ark/ui/track/custom_track_textures") # where the outputted custom track png_xbox/ps3s will go
output_dir = custom_output_dir.joinpath("gen") # the actual folder containing the png_xbox/ps3s

# retrieve custom track texture image names, and convert them to pngs
for img in custom_img_dir.glob("*"):
    if img.suffix == ".png" or img.suffix == ".jpg" or img.suffix == ".bmp":
        print(img.name)
        cmd_convert_png = f"dependencies\magick\magick.exe convert custom_textures\custom_track_textures\{img.name} custom_textures\custom_track_textures\{img.stem}.png".split()
        subprocess.run(cmd_convert_png, shell=True, cwd="..")

# convert png's for use on both xbox and ps3
for new_png in custom_img_dir.glob("*"):
    if new_png.suffix == ".png":
        cmd_xbox = f"dependencies\superfreq.exe png2tex custom_textures\custom_track_textures\{new_png.name} _ark\\ui\\track\custom_track_textures\gen\{new_png.stem}.png_xbox --platform x360 --miloVersion 26".split()
        subprocess.run(cmd_xbox, shell=True, cwd="..")
        cmd_ps3 = f"python dependencies\dev_scripts\swap_rb_art_bytes.py _ark\\ui\\track\custom_track_textures\gen\{new_png.stem}.png_xbox _ark\\ui\\track\custom_track_textures\gen\{new_png.stem}.png_ps3".split()
        subprocess.run(cmd_ps3, shell=True, cwd="..", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        
print("Successfully implemented custom track textures on the RB3DX ark. Please rebuild in order to see them reflected in-game.")