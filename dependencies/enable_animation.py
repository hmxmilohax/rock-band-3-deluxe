# enable_keys.py
from pathlib import Path
import shutil
import os
try:
    import git
    print("module 'git' is installed. Downloading/enabling additional rbdx_animated_textures, this may take some time.")
except ModuleNotFoundError:
    print("module 'git' is not installed. Install it via '/dependencies/install_gitpython.bat' or 'pip install gitpython'")
    sys.exit(1)
    
# get the current working directory
cwd = Path().absolute()

# clone/pull rbdx_animated_textures
rbdx_animated_textures_path = cwd.joinpath("rbdx_animated_textures")
try:
    repo = git.Repo.clone_from("https://github.com/jnackmclain/rbdx_animated_textures.git", rbdx_animated_textures_path, branch="main")
except:
    repo = git.Repo(rbdx_animated_textures_path)
    origin = repo.remotes.origin
    origin.pull()

animated_smashers_source_folder = cwd.joinpath("rbdx_animated_textures/animated_smashers")
animated_surfaces_source_folder = cwd.joinpath("rbdx_animated_textures/animated_surfaces")
animated_gems_source_folder = cwd.joinpath("rbdx_animated_textures/animated_gems")
animated_smashers_folder = cwd.joinpath("_ark/ui/track/animated_smashers")
animated_surfaces_folder = cwd.joinpath("_ark/ui/track/animated_surfaces")
animated_gems_folder = cwd.joinpath("_ark/ui/track/animated_gems")
files = os.listdir(rbdx_animated_textures_path)
shutil.copytree(animated_smashers_source_folder, animated_smashers_folder)
shutil.copytree(animated_surfaces_source_folder, animated_surfaces_folder)
shutil.copytree(animated_gems_source_folder, animated_gems_folder)

# uncomment the ANIMATION_ENABLED line
macros_path = cwd.joinpath("_ark/config/macros.dta")
macro_contents = []

macro_contents = [line for line in open(macros_path,"r")]
for i in range(len(macro_contents)):
    if "ANIMATION_ENABLED" in macro_contents[i]:
        macro_contents[i] = macro_contents[i].replace(";#define","#define")
        break
        
with open(macros_path,"w") as f:
    f.writelines(macro_contents)

print(f"Successfully enabled custom animations on the RB3DX ark. Please rebuild in order to see them reflected in-game.")
