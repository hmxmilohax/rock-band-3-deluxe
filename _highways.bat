del /f "%~dp0_ark\ui\track\surfaces\highways.dta"
cd "%~dp0highways"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE ren @file !Phile: =_!"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE  ren @file !Phile:-=_!"
for /f "Tokens=*" %%f in ('dir /l/b/a-d/s') do (move /y "%%f" "%%f")
for %%i in (*.bmp) do @echo "%%~ni">> highways.dta
for %%i in (*.png) do @echo "%%~ni">> highways.dta
for %%i in (*.jpg) do @echo "%%~ni">> highways.dta
move "%~dp0highways\highways.dta" "%~dp0_ark\ui\track\surfaces\highways.dta"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0dependencies/magick/magick.exe" convert "%~dp0highways/%%G" -resize 256x512! -filter Box "%~dp0highways\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.jpg') DO "%~dp0dependencies/magick/magick.exe" convert "%~dp0highways/%%G" -resize 256x512! -filter Box "%~dp0highways\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.bmp') DO "%~dp0dependencies/magick/magick.exe" convert "%~dp0highways/%%G" -resize 256x512! -filter Box "%~dp0highways\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0dependencies/superfreq.exe" png2tex "%~dp0highways/%%G" "%~dp0_ark\ui\track\surfaces\gen\%%~nG.bmp_xbox" --platform x360 --miloVersion 26
cd "%~dp0_ark/ui/track/surfaces/gen"
FOR /F "tokens=*" %%G IN ('dir /b *.bmp_xbox') DO python "%~dp0dependencies/swap_dds_bytes.py" "%~dp0_ark/ui/track/surfaces/gen/%%G" "%~dp0_ark/ui/track/surfaces/gen/%%~nG.bmp_ps3"