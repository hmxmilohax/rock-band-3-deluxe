# disable_animation.py
from pathlib import Path

def rm_tree(pth):
    pth = Path(pth)
    for child in pth.glob('*'):
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()

# get the current working directory
cwd = Path().absolute()
root_dir = Path(__file__).parents[1] # root directory of the repo

animated_smashers_folder = root_dir.joinpath("_ark/ui/track/animated_smashers")
animated_surfaces_folder = root_dir.joinpath("_ark/ui/track/animated_surfaces")
animated_gems_folder = root_dir.joinpath("_ark/ui/track/animated_gems")

rm_tree(animated_gems_folder)
rm_tree(animated_smashers_folder)
rm_tree(animated_surfaces_folder)

# comment the ANIMATION_ENABLED line
macros_path = root_dir.joinpath("_ark/config/macros.dta")
macro_contents = []

macro_contents = [line for line in open(macros_path,"r")]
for i in range(len(macro_contents)):
    if "ANIMATION_ENABLED" in macro_contents[i]:
        if ";#define" not in macro_contents[i]:
            macro_contents[i] = ";" + macro_contents[i]
        break

with open(macros_path,"w") as f:
    f.writelines(macro_contents)

print(f"Successfully disabled animated_textures on the Rock Band 3 Deluxe ark. Please rebuild in order to see them reflected in-game.")
