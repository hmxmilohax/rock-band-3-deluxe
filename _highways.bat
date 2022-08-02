del /f "%~dp0_ark\ui\track\surfaces\highways.dta"
cd "%~dp0custom_textures\highways"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE ren @file !Phile: =_!"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE  ren @file !Phile:-=_!"
for /f "Tokens=*" %%f in ('dir /l/b/a-d/s') do (move /y "%%f" "%%f")
for %%i in (*.bmp) do @echo "%%~ni">> highways.dta
for %%i in (*.png) do @echo "%%~ni">> highways.dta
for %%i in (*.jpg) do @echo "%%~ni">> highways.dta
move "%~dp0custom_textures\highways\highways.dta" "%~dp0_ark\ui\track\surfaces\highways.dta"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0dependencies/magick/magick.exe" convert "%~dp0custom_textures\highways/%%G" -resize 256x512! -filter Box "%~dp0custom_textures\highways\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.jpg') DO "%~dp0dependencies/magick/magick.exe" convert "%~dp0custom_textures\highways/%%G" -resize 256x512! -filter Box "%~dp0custom_textures\highways\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.bmp') DO "%~dp0dependencies/magick/magick.exe" convert "%~dp0custom_textures\highways/%%G" -resize 256x512! -filter Box "%~dp0custom_textures\highways\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0dependencies/superfreq.exe" png2tex "%~dp0custom_textures\highways/%%G" "%~dp0_ark\ui\track\surfaces\gen\%%~nG.png_xbox" --platform x360 --miloVersion 26
cd "%~dp0_ark/ui/track/surfaces/gen"
FOR /F "tokens=*" %%G IN ('dir /b *.png_xbox') DO python "%~dp0dependencies/swap_dds_bytes.py" "%~dp0_ark/ui/track/surfaces/gen/%%G" "%~dp0_ark/ui/track/surfaces/gen/%%~nG.png_ps3"