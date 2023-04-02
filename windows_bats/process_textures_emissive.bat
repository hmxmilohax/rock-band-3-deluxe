del /f "%~dp0..\_ark\ui\track\emissives\emissives.dta"
cd "%~dp0..\custom_textures\emissives"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE ren @file !Phile: =_!"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE  ren @file !Phile:-=_!"
for /f "Tokens=*" %%f in ('dir /l/b/a-d/s') do (move /y "%%f" "%%f")
for %%i in (*.bmp) do @echo "%%~ni">> emissives.dta
for %%i in (*.png) do @echo "%%~ni">> emissives.dta
for %%i in (*.jpg) do @echo "%%~ni">> emissives.dta
move "%~dp0..\custom_textures\emissives\emissives.dta" "%~dp0..\_ark\ui\track\emissives\emissives.dta"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0..\dependencies/magick/magick.exe" convert "%~dp0..\custom_textures\emissives/%%G" "%~dp0..\custom_textures\emissives\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.jpg') DO "%~dp0..\dependencies/magick/magick.exe" convert "%~dp0..\custom_textures\emissives/%%G" "%~dp0..\custom_textures\emissives\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.bmp') DO "%~dp0..\dependencies/magick/magick.exe" convert "%~dp0..\custom_textures\emissives/%%G" "%~dp0..\custom_textures\emissives\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0..\dependencies/windows/superfreq.exe" png2tex "%~dp0..\custom_textures\emissives/%%G" "%~dp0..\_ark\ui\track\emissives\gen\%%~nG.png_xbox" --platform x360 --miloVersion 26
cd "%~dp0..\_ark/ui/track/emissives/gen"
FOR /F "tokens=*" %%G IN ('dir /b *.png_xbox') DO python "%~dp0..\dependencies/swap_rb_art_bytes.py" "%~dp0..\_ark/ui/track/emissives/gen/%%G" "%~dp0..\_ark/ui/track/emissives/gen/%%~nG.png_ps3"
