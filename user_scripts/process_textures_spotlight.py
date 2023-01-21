# process_textures_spotlight.py
from pathlib import Path
import subprocess

# per jnack:
# It makes a dta listing all the files in the spotlight folder in the destination format, 
# converts images of various types to a uniform png, 
# then makes png_xbox and png_ps3 files, 
# and moves them into _ark

# BATCH FILE CODE
# del /f "%~dp0_ark\ui\track\spotlights\spotlights.dta"
# cd "%~dp0custom_textures\spotlights"
# forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE ren @file !Phile: =_!"
# forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE  ren @file !Phile:-=_!"
# for /f "Tokens=*" %%f in ('dir /l/b/a-d/s') do (move /y "%%f" "%%f")
# for %%i in (*.bmp) do @echo "%%~ni">> spotlights.dta
# for %%i in (*.png) do @echo "%%~ni">> spotlights.dta
# for %%i in (*.jpg) do @echo "%%~ni">> spotlights.dta
# move "%~dp0custom_textures\spotlights\spotlights.dta" "%~dp0_ark\ui\track\spotlights\spotlights.dta"
# "%~dp0dependencies/sed.exe" -i -e "s/gem_cymbal_diffuse_//g" "%~dp0_ark\ui\track\spotlights\spotlights.dta"
# "%~dp0dependencies/sed.exe" -i -e "s/prism_gem_keyboard_style_//g" "%~dp0_ark\ui\track\spotlights\spotlights.dta"
# "%~dp0dependencies/sed.exe" -i -e "s/prism_spotlights_//g" "%~dp0_ark\ui\track\spotlights\spotlights.dta"
# "%~dp0dependencies/sed.exe" -i -e ":a;N;$!ba;s/\n/\t/g" "%~dp0_ark\ui\track\spotlights\spotlights.dta"
# "%~dp0dependencies/sed.exe" -i -e "s/\t/ /g" "%~dp0_ark\ui\track\spotlights\spotlights.dta"
# "%~dp0dependencies/sed.exe" -i -e "s/\"rb2_bass_superstreak\"/          \"rb2_bass_superstreak\"/g" "%~dp0_ark\ui\track\spotlights\spotlights.dta"


# %~dp0dependencies/sed.exe -i -e "/^          \"rb2_bass_superstreak\"/{r %~dp0_ark\ui\track\spotlights\spotlights.dta" -e "d;}" %~dp0_ark\ui\overshell\slot_states.dta


# FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0dependencies/magick/magick.exe" convert "%~dp0custom_textures\spotlights/%%G" -resize 256x512! -filter Box -alpha set -background none +channel "%~dp0custom_textures\spotlights\%%~nG.png"
# FOR /F "tokens=*" %%G IN ('dir /b *.jpg') DO "%~dp0dependencies/magick/magick.exe" convert "%~dp0custom_textures\spotlights/%%G" -resize 256x512! -filter Box -alpha set -background none +channel "%~dp0custom_textures\spotlights\%%~nG.png"
# FOR /F "tokens=*" %%G IN ('dir /b *.bmp') DO "%~dp0dependencies/magick/magick.exe" convert "%~dp0custom_textures\spotlights/%%G" -resize 256x512! -filter Box -alpha set -background none +channel "%~dp0custom_textures\spotlights\%%~nG.png"
# FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0dependencies/superfreq.exe" png2tex "%~dp0custom_textures\spotlights/%%G" "%~dp0_ark\ui\track\spotlights\gen\%%~nG.png_xbox" --platform x360 --miloVersion 26
# cd "%~dp0_ark/ui/track/spotlights/gen"
# FOR /F "tokens=*" %%G IN ('dir /b *.png_xbox') DO python "%~dp0dependencies/swap_rb_art_bytes.py" "%~dp0_ark/ui/track/spotlights/gen/%%G" "%~dp0_ark/ui/track/spotlights/gen/%%~nG.png_ps3"

# get current working directory (user_scripts)
cwd = Path().absolute()

# get the root directory of the repo
root_dir = Path(__file__).parents[1]

# process the spotlights
spotlight_dir = root_dir.joinpath("custom_textures/spotlights")

spotlight_dta = []

for spotlight in spotlight_dir.glob("*"):
    print(spotlight.name)
    if spotlight.suffix == ".png" or spotlight.suffix == ".jpg" or spotlight.suffix == ".bmp":
        spotlight_dta.append(spotlight.stem)

spotlight_dta.sort()

print(spotlight_dta)

spotlight_output_dir = root_dir.joinpath("_ark/ui/track/spotlights")

with open(spotlight_output_dir.joinpath("spotlights.dta"), "w", encoding="ISO-8859-1") as dta_output:
    for asdf in spotlight_dta:
        dta_output.write(f"\"{asdf}\"\n")

# write these spotlights to slot_states.dta
with open(root_dir.joinpath("_ark/ui/overshell/slot_states.dta"), "r", encoding="ISO-8859=1") as f:
    slot_states_dta = [line for line in f.readlines()]

for i in range(len(slot_states_dta)):
    if "; paste your spotlights.dta contents here" in slot_states_dta[i]:
        print(f"found at index {i}")
        spotlight_index_begin = i
    elif "; end spotlights.dta contents" in slot_states_dta[i]:
        spotlight_index_end = i
        break

# get number of leading spaces in first line
leading_spaces = len(slot_states_dta[spotlight_index_begin]) - len(slot_states_dta[spotlight_index_begin].lstrip())
print(leading_spaces)

slot_state_additions = []
slot_state_additions.append(f"{' ' * leading_spaces}(\n")
for addition in spotlight_dta:
    slot_state_additions.append(f"{' ' * (leading_spaces + 2)}\"{addition}\"\n")
slot_state_additions.append(f"{' ' * leading_spaces})\n")

# for a in slot_state_additions:
#     print(a)

new_slot_states_dta = slot_states_dta[:spotlight_index_begin+1]
new_slot_states_dta.extend(slot_state_additions)
new_slot_states_dta.extend(slot_states_dta[spotlight_index_end:])

# print(new_slot_states_dta)

with open(root_dir.joinpath("_ark/ui/overshell/slot_states.dta"), "w", encoding="ISO-8859=1") as ff:
    ff.writelines(new_slot_states_dta)

# convert images to uniform png
# FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0dependencies/magick/magick.exe" convert "%~dp0custom_textures\spotlights/%%G" -resize 256x512! -filter Box -alpha set -background none +channel "%~dp0custom_textures\spotlights\%%~nG.png"
# FOR /F "tokens=*" %%G IN ('dir /b *.jpg') DO "%~dp0dependencies/magick/magick.exe" convert "%~dp0custom_textures\spotlights/%%G" -resize 256x512! -filter Box -alpha set -background none +channel "%~dp0custom_textures\spotlights\%%~nG.png"
# FOR /F "tokens=*" %%G IN ('dir /b *.bmp') DO "%~dp0dependencies/magick/magick.exe" convert "%~dp0custom_textures\spotlights/%%G" -resize 256x512! -filter Box -alpha set -background none +channel "%~dp0custom_textures\spotlights\%%~nG.png"
# FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0dependencies/superfreq.exe" png2tex "%~dp0custom_textures\spotlights/%%G" "%~dp0_ark\ui\track\spotlights\gen\%%~nG.png_xbox" --platform x360 --miloVersion 26
# cd "%~dp0_ark/ui/track/spotlights/gen"
# FOR /F "tokens=*" %%G IN ('dir /b *.png_xbox') DO python "%~dp0dependencies/swap_rb_art_bytes.py" "%~dp0_ark/ui/track/spotlights/gen/%%G" "%~dp0_ark/ui/track/spotlights/gen/%%~nG.png_ps3"

for img in spotlight_dir.glob("*"):
    if img.suffix == ".png" or img.suffix == ".jpg" or img.suffix == ".bmp":
        cmd_convert_png = f"dependencies\magick\magick.exe convert custom_textures\spotlights\{img.name} -resize 256x512! -filter Box -alpha set -background none +channel custom_textures\spotlights\{img.name}".split()
        subprocess.run(cmd_convert_png, shell=True, cwd="..")

for sl_png in spotlight_dir.glob("*"):
    if sl_png.suffix == ".png":
        cmd_make_xbox_png = f"dependencies\superfreq.exe png2tex custom_textures\spotlights\{sl_png.name} _ark\\ui\\track\spotlights\gen\{sl_png.stem}.png_xbox --platform x360 --miloVersion 26".split()
        subprocess.run(cmd_make_xbox_png, shell=True, cwd="..")

output_dir = spotlight_output_dir.joinpath("gen")
for png_xbox in output_dir.glob("*"):
    cmd_ps3 = f"python dependencies\dev_scripts\swap_rb_art_bytes.py _ark\\ui\\track\spotlights\gen\{png_xbox.name} _ark\\ui\\track\spotlights\gen\{png_xbox.stem}.png_ps3".split()
    subprocess.run(cmd_ps3, shell=True, cwd="..", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)