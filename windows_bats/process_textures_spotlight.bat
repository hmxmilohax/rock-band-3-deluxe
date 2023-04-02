del /f "%~dp0..\_ark\ui\track\spotlights\spotlights.dta"
cd "%~dp0..\custom_textures\spotlights"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE ren @file !Phile: =_!"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE  ren @file !Phile:-=_!"
for /f "Tokens=*" %%f in ('dir /l/b/a-d/s') do (move /y "%%f" "%%f")
for %%i in (*.bmp) do @echo "%%~ni">> spotlights.dta
for %%i in (*.png) do @echo "%%~ni">> spotlights.dta
for %%i in (*.jpg) do @echo "%%~ni">> spotlights.dta
move "%~dp0..\custom_textures\spotlights\spotlights.dta" "%~dp0..\_ark\ui\track\spotlights\spotlights.dta"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0..\dependencies/magick/magick.exe" convert "%~dp0..\custom_textures\spotlights/%%G" "%~dp0..\custom_textures\spotlights\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.jpg') DO "%~dp0..\dependencies/magick/magick.exe" convert "%~dp0..\custom_textures\spotlights/%%G" "%~dp0..\custom_textures\spotlights\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.bmp') DO "%~dp0..\dependencies/magick/magick.exe" convert "%~dp0..\custom_textures\spotlights/%%G" "%~dp0..\custom_textures\spotlights\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0..\dependencies/windows/superfreq.exe" png2tex "%~dp0..\custom_textures\spotlights/%%G" "%~dp0..\_ark\ui\track\spotlights\gen\%%~nG.png_xbox" --platform x360 --miloVersion 26
cd "%~dp0..\_ark/ui/track/spotlights/gen"
FOR /F "tokens=*" %%G IN ('dir /b *.png_xbox') DO python "%~dp0..\dependencies/swap_rb_art_bytes.py" "%~dp0..\_ark/ui/track/spotlights/gen/%%G" "%~dp0..\_ark/ui/track/spotlights/gen/%%~nG.png_ps3"
