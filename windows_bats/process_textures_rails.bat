del /f "%~dp0..\_ark\ui\track\rails\rails.dta"
cd "%~dp0..\custom_textures\rails"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE ren @file !Phile: =_!"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE  ren @file !Phile:-=_!"
for /f "Tokens=*" %%f in ('dir /l/b/a-d/s') do (move /y "%%f" "%%f")
for %%i in (*.bmp) do @echo "%%~ni">> rails.dta
for %%i in (*.png) do @echo "%%~ni">> rails.dta
for %%i in (*.jpg) do @echo "%%~ni">> rails.dta
move "%~dp0..\custom_textures\rails\rails.dta" "%~dp0..\_ark\ui\track\rails\rails.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/beat_marker_//g" "%~dp0..\_ark\ui\track\rails\rails.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/rails_//g" "%~dp0..\_ark\ui\track\rails\rails.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/smasher_plate_bracket_//g" "%~dp0..\_ark\ui\track\rails\rails.dta"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0..\dependencies/magick/magick.exe" convert "%~dp0..\custom_textures\rails/%%G" "%~dp0..\custom_textures\rails\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.jpg') DO "%~dp0..\dependencies/magick/magick.exe" convert "%~dp0..\custom_textures\rails/%%G" "%~dp0..\custom_textures\rails\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.bmp') DO "%~dp0..\dependencies/magick/magick.exe" convert "%~dp0..\custom_textures\rails/%%G" "%~dp0..\custom_textures\rails\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0..\dependencies/windows/superfreq.exe" png2tex "%~dp0..\custom_textures\rails/%%G" "%~dp0..\_ark\ui\track\rails\gen\%%~nG.png_xbox" --platform x360 --miloVersion 26
cd "%~dp0..\_ark/ui/track/rails/gen"
FOR /F "tokens=*" %%G IN ('dir /b *.png_xbox') DO python "%~dp0..\dependencies/swap_rb_art_bytes.py" "%~dp0..\_ark/ui/track/rails/gen/%%G" "%~dp0..\_ark/ui/track/rails/gen/%%~nG.png_ps3"
