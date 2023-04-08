del /f "%~dp0..\_ark\ui\track\smashers\smashers.dta"
cd "%~dp0..\custom_textures\smashers"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE ren @file !Phile: =_!"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE  ren @file !Phile:-=_!"
for /f "Tokens=*" %%f in ('dir /l/b/a-d/s') do (move /y "%%f" "%%f")
for %%i in (*.bmp) do @echo "%%~ni">> smashers.dta
for %%i in (*.png) do @echo "%%~ni">> smashers.dta
for %%i in (*.jpg) do @echo "%%~ni">> smashers.dta
move "%~dp0..\custom_textures\smashers\smashers.dta" "%~dp0..\_ark\ui\track\smashers\smashers.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/gem_smashers_//g" "%~dp0..\_ark\ui\track\smashers\smashers.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/guitar_//g" "%~dp0..\_ark\ui\track\smashers\smashers.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/drum_//g" "%~dp0..\_ark\ui\track\smashers\smashers.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/square_smasher_bright_//g" "%~dp0..\_ark\ui\track\smashers\smashers.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/green_//g" "%~dp0..\_ark\ui\track\smashers\smashers.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/red_//g" "%~dp0..\_ark\ui\track\smashers\smashers.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/yellow_//g" "%~dp0..\_ark\ui\track\smashers\smashers.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/blue_//g" "%~dp0..\_ark\ui\track\smashers\smashers.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/orange_//g" "%~dp0..\_ark\ui\track\smashers\smashers.dta"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0..\dependencies/magick/magick.exe" convert "%~dp0..\custom_textures\smashers/%%G" "%~dp0..\custom_textures\smashers\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.jpg') DO "%~dp0..\dependencies/magick/magick.exe" convert "%~dp0..\custom_textures\smashers/%%G" "%~dp0..\custom_textures\smashers\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.bmp') DO "%~dp0..\dependencies/magick/magick.exe" convert "%~dp0..\custom_textures\smashers/%%G" "%~dp0..\custom_textures\smashers\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0..\dependencies/windows/superfreq.exe" png2tex "%~dp0..\custom_textures\smashers/%%G" "%~dp0..\_ark\ui\track\smashers\gen\%%~nG.png_xbox" --platform x360 --miloVersion 26
cd "%~dp0..\_ark/ui/track/smashers/gen"
FOR /F "tokens=*" %%G IN ('dir /b *.png_xbox') DO python "%~dp0..\dependencies/swap_rb_art_bytes.py" "%~dp0..\_ark/ui/track/smashers/gen/%%G" "%~dp0..\_ark/ui/track/smashers/gen/%%~nG.png_ps3"
