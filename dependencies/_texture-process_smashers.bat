del /f "%~dp0_ark\ui\track\smashers\smashers.dta"
cd "%~dp0custom_textures\smashers"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE ren @file !Phile: =_!"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE  ren @file !Phile:-=_!"
for /f "Tokens=*" %%f in ('dir /l/b/a-d/s') do (move /y "%%f" "%%f")
for %%i in (*.bmp) do @echo "%%~ni">> smashers.dta
for %%i in (*.png) do @echo "%%~ni">> smashers.dta
for %%i in (*.jpg) do @echo "%%~ni">> smashers.dta
move "%~dp0custom_textures\smashers\smashers.dta" "%~dp0_ark\ui\track\smashers\smashers.dta"
"%~dp0dependencies/sed.exe" -i -e "s/gem_smashers_drum_//g" "%~dp0_ark\ui\track\smashers\smashers.dta"
"%~dp0dependencies/sed.exe" -i -e "s/gem_smashers_guitar_//g" "%~dp0_ark\ui\track\smashers\smashers.dta"
"%~dp0dependencies/sed.exe" -i -e "s/square_smasher_bright_green_//g" "%~dp0_ark\ui\track\smashers\smashers.dta"
"%~dp0dependencies/sed.exe" -i -e "s/square_smasher_bright_red_//g" "%~dp0_ark\ui\track\smashers\smashers.dta"
"%~dp0dependencies/sed.exe" -i -e "s/square_smasher_bright_yellow_//g" "%~dp0_ark\ui\track\smashers\smashers.dta"
"%~dp0dependencies/sed.exe" -i -e "s/square_smasher_bright_blue_//g" "%~dp0_ark\ui\track\smashers\smashers.dta"
"%~dp0dependencies/sed.exe" -i -e "s/square_smasher_bright_orange_//g" "%~dp0_ark\ui\track\smashers\smashers.dta"
"%~dp0dependencies/sed.exe" -i -e ":a;N;$!ba;s/\n/\t/g" "%~dp0_ark\ui\track\smashers\smashers.dta"
"%~dp0dependencies/sed.exe" -i -e "s/\t/ /g" "%~dp0_ark\ui\track\smashers\smashers.dta"
"%~dp0dependencies/sed.exe" -i -e "s/\"rb2\"/               \"rb2\"/g" "%~dp0_ark\ui\track\smashers\smashers.dta"
%~dp0dependencies/sed.exe -i -e "/^               \"rb2\"/{r %~dp0_ark\ui\track\smashers\smashers.dta" -e "d;}" %~dp0_ark\ui\overshell\slot_states.dta
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0dependencies/magick/magick.exe" convert "%~dp0custom_textures\smashers/%%G" "%~dp0custom_textures\smashers\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.jpg') DO "%~dp0dependencies/magick/magick.exe" convert "%~dp0custom_textures\smashers/%%G" "%~dp0custom_textures\smashers\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.bmp') DO "%~dp0dependencies/magick/magick.exe" convert "%~dp0custom_textures\smashers/%%G" "%~dp0custom_textures\smashers\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0dependencies/superfreq.exe" png2tex "%~dp0custom_textures\smashers/%%G" "%~dp0_ark\ui\track\smashers\gen\%%~nG.png_xbox" --platform x360 --miloVersion 26
cd "%~dp0_ark/ui/track/smashers/gen"
FOR /F "tokens=*" %%G IN ('dir /b *.png_xbox') DO python "%~dp0dependencies/swap_rb_art_bytes.py" "%~dp0_ark/ui/track/smashers/gen/%%G" "%~dp0_ark/ui/track/smashers/gen/%%~nG.png_ps3"