# disable_keys.py
from pathlib import Path
import os
import shutil

# get the current working directory
cwd = Path().absolute()

animated_smashers_folder = cwd.joinpath("_ark/ui/track/animated_smashers")
animated_surfaces_folder = cwd.joinpath("_ark/ui/track/animated_surfaces")
animated_gems_folder = cwd.joinpath("_ark/ui/track/animated_gems")

shutil.rmtree(animated_smashers_folder)
shutil.rmtree(animated_surfaces_folder)
shutil.rmtree(animated_gems_folder)

# comment the ANIMATION_ENABLED line
macros_path = cwd.joinpath("_ark/config/macros.dta")
macro_contents = []

macro_contents = [line for line in open(macros_path,"r")]
for i in range(len(macro_contents)):
    if "ANIMATION_ENABLED" in macro_contents[i]:
        if ";#define" not in macro_contents[i]:
            macro_contents[i] = ";" + macro_contents[i]
        break

with open(macros_path,"w") as f:
    f.writelines(macro_contents)

print(f"Successfully disabled animated_textures on the RB3DX ark. Please rebuild in order to see them reflected in-game.")
