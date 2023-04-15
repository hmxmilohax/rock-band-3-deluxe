del /f "%~dp0..\_ark\ui\track\gems\gems.dta"
cd "%~dp0..\custom_textures\gems"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE ren @file !Phile: =_!"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE  ren @file !Phile:-=_!"
for /f "Tokens=*" %%f in ('dir /l/b/a-d/s') do (move /y "%%f" "%%f")
for %%i in (*.bmp) do @echo "%%~ni">> gems.dta
for %%i in (*.png) do @echo "%%~ni">> gems.dta
for %%i in (*.jpg) do @echo "%%~ni">> gems.dta
move "%~dp0..\custom_textures\gems\gems.dta" "%~dp0..\_ark\ui\track\gems\gems.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/gem_cymbal_diffuse_//g" "%~dp0..\_ark\ui\track\gems\gems.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/gem_cymbal_ems_//g" "%~dp0..\_ark\ui\track\gems\gems.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/gem_mash_green_emmisive_//g" "%~dp0..\_ark\ui\track\gems\gems.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/gem_mash_red_emmisive_//g" "%~dp0..\_ark\ui\track\gems\gems.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/gem_mash_yellow_emmisive_//g" "%~dp0..\_ark\ui\track\gems\gems.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/gem_mash_blue_emmisive_//g" "%~dp0..\_ark\ui\track\gems\gems.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/gem_mash_orange_emmisive_//g" "%~dp0..\_ark\ui\track\gems\gems.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/gliss_gems_//g" "%~dp0..\_ark\ui\track\gems\gems.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/prism_gem_keyboard_style_//g" "%~dp0..\_ark\ui\track\gems\gems.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/prism_gems_//g" "%~dp0..\_ark\ui\track\gems\gems.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/prism_gem_emissive_//g" "%~dp0..\_ark\ui\track\gems\gems.dta"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0..\dependencies/magick/magick.exe" convert "%~dp0..\custom_textures\gems/%%G" "%~dp0..\custom_textures\gems\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.jpg') DO "%~dp0..\dependencies/magick/magick.exe" convert "%~dp0..\custom_textures\gems/%%G" "%~dp0..\custom_textures\gems\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.bmp') DO "%~dp0..\dependencies/magick/magick.exe" convert "%~dp0..\custom_textures\gems/%%G" "%~dp0..\custom_textures\gems\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0..\dependencies/windows/superfreq.exe" png2tex "%~dp0..\custom_textures\gems/%%G" "%~dp0..\_ark\ui\track\gems\gen\%%~nG.png_xbox" --platform x360 --miloVersion 26
cd "%~dp0..\_ark/ui/track/gems/gen"
FOR /F "tokens=*" %%G IN ('dir /b *.png_xbox') DO python "%~dp0..\dependencies/swap_rb_art_bytes.py" "%~dp0..\_ark/ui/track/gems/gen/%%G" "%~dp0..\_ark/ui/track/gems/gen/%%~nG.png_ps3"