del /f "%~dp0..\_ark\ui\track\voxnotes\voxnotes.dta"
cd "%~dp0..\custom_textures\voxnotes"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE ren @file !Phile: =_!"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE  ren @file !Phile:-=_!"
for /f "Tokens=*" %%f in ('dir /l/b/a-d/s') do (move /y "%%f" "%%f")
for %%i in (*.bmp) do @echo "%%~ni">> voxnotes.dta
for %%i in (*.png) do @echo "%%~ni">> voxnotes.dta
for %%i in (*.jpg) do @echo "%%~ni">> voxnotes.dta
move "%~dp0..\custom_textures\voxnotes\voxnotes.dta" "%~dp0..\_ark\ui\track\voxnotes\voxnotes.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/vocal_tube_matrix_//g" "%~dp0..\_ark\ui\track\voxnotes\voxnotes.dta"
FOR /F "tokens=*" %%G IN ('dir /b *.jpg') DO "%~dp0..\dependencies/magick/magick.exe" convert "%~dp0..\custom_textures\voxnotes/%%G" "%~dp0..\custom_textures\voxnotes\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.bmp') DO "%~dp0..\dependencies/magick/magick.exe" convert "%~dp0..\custom_textures\voxnotes/%%G" "%~dp0..\custom_textures\voxnotes\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0..\dependencies/windows/superfreq.exe" png2tex "%~dp0..\custom_textures\voxnotes/%%G" "%~dp0..\_ark\ui\track\voxnotes\gen\%%~nG.png_xbox" --platform x360 --miloVersion 26
del sed* /a /s
cd "%~dp0..\_ark/ui/track/voxnotes/gen"
FOR /F "tokens=*" %%G IN ('dir /b *.png_xbox') DO python "%~dp0..\dependencies/swap_rb_art_bytes.py" "%~dp0..\_ark/ui/track/voxnotes/gen/%%G" "%~dp0..\_ark/ui/track/voxnotes/gen/%%~nG.png_ps3"
