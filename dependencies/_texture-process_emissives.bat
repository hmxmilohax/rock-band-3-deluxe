del /f "%~dp0_ark\ui\track\emissives\emissives.dta"
cd "%~dp0custom_textures\emissives"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE ren @file !Phile: =_!"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE  ren @file !Phile:-=_!"
for /f "Tokens=*" %%f in ('dir /l/b/a-d/s') do (move /y "%%f" "%%f")
for %%i in (*.bmp) do @echo "%%~ni">> emissives.dta
for %%i in (*.png) do @echo "%%~ni">> emissives.dta
for %%i in (*.jpg) do @echo "%%~ni">> emissives.dta
move "%~dp0custom_textures\emissives\emissives.dta" "%~dp0_ark\ui\track\emissives\emissives.dta"
"%~dp0dependencies/sed.exe" -i -e ":a;N;$!ba;s/\n/\t/g" "%~dp0_ark\ui\track\emissives\emissives.dta"
"%~dp0dependencies/sed.exe" -i -e "s/\t/ /g" "%~dp0_ark\ui\track\emissives\emissives.dta"
"%~dp0dependencies/sed.exe" -i -e "s/\"bass_emissive_aqua\"/          \"bass_emissive_aqua\"/g" "%~dp0_ark\ui\track\emissives\emissives.dta"
%~dp0dependencies/sed.exe -i -e "/^          \"bass_emissive_aqua\"/{r %~dp0_ark\ui\track\emissives\emissives.dta" -e "d;}" %~dp0_ark\ui\overshell\slot_states.dta
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0dependencies/magick/magick.exe" convert "%~dp0custom_textures\emissives/%%G" -resize 256x512! -filter Box -alpha set -background none -channel A -evaluate multiply 0.5 +channel "%~dp0custom_textures\emissives\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.jpg') DO "%~dp0dependencies/magick/magick.exe" convert "%~dp0custom_textures\emissives/%%G" -resize 256x512! -filter Box -alpha set -background none -channel A -evaluate multiply 0.5 +channel "%~dp0custom_textures\emissives\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.bmp') DO "%~dp0dependencies/magick/magick.exe" convert "%~dp0custom_textures\emissives/%%G" -resize 256x512! -filter Box -alpha set -background none -channel A -evaluate multiply 0.5 +channel "%~dp0custom_textures\emissives\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0dependencies/superfreq.exe" png2tex "%~dp0custom_textures\emissives/%%G" "%~dp0_ark\ui\track\emissives\gen\%%~nG.png_xbox" --platform x360 --miloVersion 26
cd "%~dp0_ark/ui/track/emissives/gen"
FOR /F "tokens=*" %%G IN ('dir /b *.png_xbox') DO python "%~dp0dependencies/swap_rb_art_bytes.py" "%~dp0_ark/ui/track/emissives/gen/%%G" "%~dp0_ark/ui/track/emissives/gen/%%~nG.png_ps3"