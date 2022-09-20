del /f "%~dp0_ark\ui\track\gems\gems.dta"
cd "%~dp0custom_textures\gems"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE ren @file !Phile: =_!"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE  ren @file !Phile:-=_!"
for /f "Tokens=*" %%f in ('dir /l/b/a-d/s') do (move /y "%%f" "%%f")
for %%i in (*.bmp) do @echo "%%~ni">> gems.dta
for %%i in (*.png) do @echo "%%~ni">> gems.dta
for %%i in (*.jpg) do @echo "%%~ni">> gems.dta
move "%~dp0custom_textures\gems\gems.dta" "%~dp0_ark\ui\track\gems\gems.dta"
"%~dp0dependencies/sed.exe" -i -e "s/gem_cymbal_diffuse_//g" "%~dp0_ark\ui\track\gems\gems.dta"
"%~dp0dependencies/sed.exe" -i -e "s/prism_gem_keyboard_style_//g" "%~dp0_ark\ui\track\gems\gems.dta"
"%~dp0dependencies/sed.exe" -i -e "s/prism_gems_//g" "%~dp0_ark\ui\track\gems\gems.dta"
"%~dp0dependencies/sed.exe" -i -e ":a;N;$!ba;s/\n/\t/g" "%~dp0_ark\ui\track\gems\gems.dta"
"%~dp0dependencies/sed.exe" -i -e "s/\t/ /g" "%~dp0_ark\ui\track\gems\gems.dta"
"%~dp0dependencies/sed.exe" -i -e "s/\"rb3\"/          \"rb3\"/g" "%~dp0_ark\ui\track\gems\gems.dta"
%~dp0dependencies/sed.exe -i -e "/^          \"rb3\"/{r %~dp0_ark\ui\track\gems\gems.dta" -e "d;}" %~dp0_ark\ui\overshell\slot_states.dta
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0dependencies/magick/magick.exe" convert "%~dp0custom_textures\gems/%%G" "%~dp0custom_textures\gems\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.jpg') DO "%~dp0dependencies/magick/magick.exe" convert "%~dp0custom_textures\gems/%%G" "%~dp0custom_textures\gems\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.bmp') DO "%~dp0dependencies/magick/magick.exe" convert "%~dp0custom_textures\gems/%%G" "%~dp0custom_textures\gems\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0dependencies/superfreq.exe" png2tex "%~dp0custom_textures\gems/%%G" "%~dp0_ark\ui\track\gems\gen\%%~nG.png_xbox" --platform x360 --miloVersion 26
cd "%~dp0_ark/ui/track/gems/gen"
FOR /F "tokens=*" %%G IN ('dir /b *.png_xbox') DO python "%~dp0dependencies/swap_rb_art_bytes.py" "%~dp0_ark/ui/track/gems/gen/%%G" "%~dp0_ark/ui/track/gems/gen/%%~nG.png_ps3"