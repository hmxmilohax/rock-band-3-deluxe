del /f "%~dp0..\_ark\ui\track\keyboards\keyboards.dta"
cd "%~dp0..\custom_textures\keyboards"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE ren @file !Phile: =_!"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE  ren @file !Phile:-=_!"
for /f "Tokens=*" %%f in ('dir /l/b/a-d/s') do (move /y "%%f" "%%f")
for %%i in (*.bmp) do @echo "%%~ni">> keyboards.dta
for %%i in (*.png) do @echo "%%~ni">> keyboards.dta
for %%i in (*.jpg) do @echo "%%~ni">> keyboards.dta
move "%~dp0..\custom_textures\keyboards\keyboards.dta" "%~dp0..\_ark\ui\track\keyboards\keyboards.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/gem_mash_prokeys_//g" "%~dp0..\_ark\ui\track\keyboards\keyboards.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/gem_smasher_sharp_diffuse_nomip_//g" "%~dp0..\_ark\ui\track\keyboards\keyboards.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/track_lanes_keyboard_//g" "%~dp0..\_ark\ui\track\keyboards\keyboards.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/press_//g" "%~dp0..\_ark\ui\track\keyboards\keyboards.dta"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0..\dependencies/windows/superfreq.exe" png2tex "%~dp0..\custom_textures\keyboards/%%G" "%~dp0..\_ark\ui\track\keyboards\gen\%%~nG.png_xbox" --platform x360 --miloVersion 26
cd "%~dp0..\_ark/ui/track/keyboards/gen"
FOR /F "tokens=*" %%G IN ('dir /b *.png_xbox') DO python "%~dp0..\dependencies/swap_rb_art_bytes.py" "%~dp0..\_ark/ui/track/keyboards/gen/%%G" "%~dp0..\_ark/ui/track/keyboards/gen/%%~nG.png_ps3"