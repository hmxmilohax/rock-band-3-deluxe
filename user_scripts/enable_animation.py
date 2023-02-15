# enable_animation.py
from pathlib import Path
from sys import platform
import subprocess
try:
    import git
except:
    cmd_install = "pip install gitpython".split()
    subprocess.run(cmd_install)

# get the current working directory
cwd = Path().absolute()
root_dir = Path(__file__).parents[1] # root directory of the repo
dependencies_dir = root_dir.joinpath("dependencies")

# clone/pull rbdx_animated_textures
rbdx_animated_textures_path = dependencies_dir.joinpath("rbdx_animated_textures")
try:
    repo = git.Repo.clone_from("https://github.com/hmxmilohax/rbdx_animated_textures.git", rbdx_animated_textures_path, branch="main")
except:
    repo = git.Repo(rbdx_animated_textures_path)
    origin = repo.remotes.origin
    origin.pull()

animated_folder_list = ["animated_gems", "animated_smashers", "animated_surfaces"]
for folder in animated_folder_list:
    for f in rbdx_animated_textures_path.joinpath(folder).rglob("*"):
        if f.is_file():
            if platform == "win32":
                repo_root_path = str(f).replace(f"{str(root_dir)}\\dependencies\\rbdx_animated_textures\\", "")
            else:
                repo_root_path = str(f).replace(f"{str(root_dir)}/dependencies/rbdx_animated_textures/", "")
            # print(repo_root_path)
            anim_dest_path = root_dir.joinpath(f"_ark/ui/track").joinpath(repo_root_path)
            anim_dest_path.parent.mkdir(parents=True, exist_ok=True)
            anim_dest_path.write_bytes(f.read_bytes())

# uncomment the ANIMATION_ENABLED line
macros_path = root_dir.joinpath("_ark/config/macros.dta")
macro_contents = []

macro_contents = [line for line in open(macros_path,"r")]
for i in range(len(macro_contents)):
    if "ANIMATION_ENABLED" in macro_contents[i]:
        macro_contents[i] = macro_contents[i].replace(";#define","#define")
        break
        
with open(macros_path,"w") as f:
    f.writelines(macro_contents)

print(f"Successfully enabled custom animations on the RB3DX ark. Please rebuild in order to see them reflected in-game.")
