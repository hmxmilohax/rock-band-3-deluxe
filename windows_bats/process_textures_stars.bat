del /f "%~dp0..\_ark\ui\track\stars\stars.dta"
cd "%~dp0..\custom_textures\stars"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE ren @file !Phile: =_!"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE  ren @file !Phile:-=_!"
for /f "Tokens=*" %%f in ('dir /l/b/a-d/s') do (move /y "%%f" "%%f")
for %%i in (*.bmp) do @echo "%%~ni">> stars.dta
for %%i in (*.png) do @echo "%%~ni">> stars.dta
for %%i in (*.jpg) do @echo "%%~ni">> stars.dta
move "%~dp0..\custom_textures\stars\stars.dta" "%~dp0..\_ark\ui\track\stars\stars.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/stars_meter_wipe_//g" "%~dp0..\_ark\ui\track\stars\stars.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/stars_star_frame_//g" "%~dp0..\_ark\ui\track\stars\stars.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/stars_star_gold_//g" "%~dp0..\_ark\ui\track\stars\stars.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/tour_icon_//g" "%~dp0..\_ark\ui\track\stars\stars.dta"
FOR /F "tokens=*" %%G IN ('dir /b *.jpg') DO "%~dp0..\dependencies/magick/magick.exe" convert "%~dp0..\custom_textures\stars/%%G" "%~dp0..\custom_textures\stars\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.bmp') DO "%~dp0..\dependencies/magick/magick.exe" convert "%~dp0..\custom_textures\stars/%%G" "%~dp0..\custom_textures\stars\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0..\dependencies/windows/superfreq.exe" png2tex "%~dp0..\custom_textures\stars/%%G" "%~dp0..\_ark\ui\track\stars\gen\%%~nG.png_xbox" --platform x360 --miloVersion 26
del sed* /a /s
cd "%~dp0..\_ark/ui/track/stars/gen"
FOR /F "tokens=*" %%G IN ('dir /b *.png_xbox') DO python "%~dp0..\dependencies/swap_rb_art_bytes.py" "%~dp0..\_ark/ui/track/stars/gen/%%G" "%~dp0..\_ark/ui/track/stars/gen/%%~nG.png_ps3"
