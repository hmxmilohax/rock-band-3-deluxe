del /f "%~dp0_ark\ui\track\spotlights\spotlights.dta"
cd "%~dp0custom_textures\spotlights"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE ren @file !Phile: =_!"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE  ren @file !Phile:-=_!"
for /f "Tokens=*" %%f in ('dir /l/b/a-d/s') do (move /y "%%f" "%%f")
for %%i in (*.bmp) do @echo "%%~ni">> spotlights.dta
for %%i in (*.png) do @echo "%%~ni">> spotlights.dta
for %%i in (*.jpg) do @echo "%%~ni">> spotlights.dta
move "%~dp0custom_textures\spotlights\spotlights.dta" "%~dp0_ark\ui\track\spotlights\spotlights.dta"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0dependencies/magick/magick.exe" convert "%~dp0custom_textures\spotlights/%%G" -resize 256x512! -filter Box -alpha set -background none -channel A -evaluate multiply 0.5 +channel "%~dp0custom_textures\spotlights\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.jpg') DO "%~dp0dependencies/magick/magick.exe" convert "%~dp0custom_textures\spotlights/%%G" -resize 256x512! -filter Box -alpha set -background none -channel A -evaluate multiply 0.5 +channel "%~dp0custom_textures\spotlights\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.bmp') DO "%~dp0dependencies/magick/magick.exe" convert "%~dp0custom_textures\spotlights/%%G" -resize 256x512! -filter Box -alpha set -background none -channel A -evaluate multiply 0.5 +channel "%~dp0custom_textures\spotlights\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0dependencies/superfreq.exe" png2tex "%~dp0custom_textures\spotlights/%%G" "%~dp0_ark\ui\track\spotlights\gen\%%~nG.png_xbox" --platform x360 --miloVersion 26
cd "%~dp0_ark/ui/track/spotlights/gen"
FOR /F "tokens=*" %%G IN ('dir /b *.png_xbox') DO python "%~dp0dependencies/swap_dds_bytes.py" "%~dp0_ark/ui/track/spotlights/gen/%%G" "%~dp0_ark/ui/track/spotlights/gen/%%~nG.png_ps3"