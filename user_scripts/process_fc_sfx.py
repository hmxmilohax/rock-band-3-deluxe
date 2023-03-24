from pathlib import Path
import sys
from sys import platform
import subprocess

root_dir = Path().absolute().parents[0] # root directory of the repo
print("Generating the necessary dtas...")

input_path=root_dir.joinpath(f"_ark/sfx/streams/fc/")

texture_dta = [texture.stem for texture in input_path.glob("*")]

texture_dta.sort()

with open(root_dir.joinpath(f"_ark/ui/endgame/fullcombo.dta"), "w", encoding="ISO-8859-1") as dta_output:
    for asdf in texture_dta:
        dta_output.write(f"\"{asdf}\"\n")