del /f "%~dp0_ark\ui\track\keyboards\keyboards.dta"
cd "%~dp0custom_textures\keyboards"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE ren @file !Phile: =_!"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE  ren @file !Phile:-=_!"
for /f "Tokens=*" %%f in ('dir /l/b/a-d/s') do (move /y "%%f" "%%f")
for %%i in (*.bmp) do @echo "%%~ni">> keyboards.dta
for %%i in (*.png) do @echo "%%~ni">> keyboards.dta
for %%i in (*.jpg) do @echo "%%~ni">> keyboards.dta
move "%~dp0custom_textures\keyboards\keyboards.dta" "%~dp0_ark\ui\track\keyboards\keyboards.dta"
"%~dp0dependencies/sed.exe" -i -e "s/gem_mash_prokeys_ems_//g" "%~dp0_ark\ui\track\keyboards\keyboards.dta"
"%~dp0dependencies/sed.exe" -i -e "s/gem_mash_prokeys_//g" "%~dp0_ark\ui\track\keyboards\keyboards.dta"
"%~dp0dependencies/sed.exe" -i -e "s/gem_smasher_sharp_diffuse_nomip_//g" "%~dp0_ark\ui\track\keyboards\keyboards.dta"
"%~dp0dependencies/sed.exe" -i -e "s/track_lanes_keyboard_press_//g" "%~dp0_ark\ui\track\keyboards\keyboards.dta"
"%~dp0dependencies/sed.exe" -i -e "s/track_lanes_keyboard_//g" "%~dp0_ark\ui\track\keyboards\keyboards.dta"
"%~dp0dependencies/sed.exe" -i -e ":a;N;$!ba;s/\n/\t/g" "%~dp0_ark\ui\track\keyboards\keyboards.dta"
"%~dp0dependencies/sed.exe" -i -e "s/\t/ /g" "%~dp0_ark\ui\track\keyboards\keyboards.dta"
"%~dp0dependencies/sed.exe" -i -e "s/\"blue_k\"/          \"blue_k\"/g" "%~dp0_ark\ui\track\keyboards\keyboards.dta"
%~dp0dependencies/sed.exe -i -e "/^          \"blue_k\"/{r %~dp0_ark\ui\track\keyboards\keyboards.dta" -e "d;}" %~dp0_ark\ui\overshell\slot_states.dta
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0dependencies/magick/magick.exe" convert "%~dp0custom_textures\keyboards/%%G" "%~dp0custom_textures\keyboards\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.jpg') DO "%~dp0dependencies/magick/magick.exe" convert "%~dp0custom_textures\keyboards/%%G" "%~dp0custom_textures\keyboards\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.bmp') DO "%~dp0dependencies/magick/magick.exe" convert "%~dp0custom_textures\keyboards/%%G" "%~dp0custom_textures\keyboards\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0dependencies/superfreq.exe" png2tex "%~dp0custom_textures\keyboards/%%G" "%~dp0_ark\ui\track\keyboards\gen\%%~nG.png_xbox" --platform x360 --miloVersion 26
cd "%~dp0_ark/ui/track/keyboards/gen"
FOR /F "tokens=*" %%G IN ('dir /b *.png_xbox') DO python "%~dp0dependencies/swap_rb_art_bytes.py" "%~dp0_ark/ui/track/keyboards/gen/%%G" "%~dp0_ark/ui/track/keyboards/gen/%%~nG.png_ps3"