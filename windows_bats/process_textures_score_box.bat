del /f "%~dp0..\_ark\ui\track\score_box\score_box.dta"
cd "%~dp0..\custom_textures\score_box"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE ren @file !Phile: =_!"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE  ren @file !Phile:-=_!"
for /f "Tokens=*" %%f in ('dir /l/b/a-d/s') do (move /y "%%f" "%%f")
for %%i in (*.bmp) do @echo "%%~ni">> score_box.dta
for %%i in (*.png) do @echo "%%~ni">> score_box.dta
for %%i in (*.jpg) do @echo "%%~ni">> score_box.dta
move "%~dp0..\custom_textures\score_box\score_box.dta" "%~dp0..\_ark\ui\track\score_box\score_box.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/score_boxboard_frame_//g" "%~dp0..\_ark\ui\track\score_box\score_box.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/score_boxboard_lens_//g" "%~dp0..\_ark\ui\track\score_box\score_box.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/star_multiplier_meter_frame_//g" "%~dp0..\_ark\ui\track\score_box\score_box.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/star_multiplier_meter_lens_//g" "%~dp0..\_ark\ui\track\score_box\score_box.dta"
FOR /F "tokens=*" %%G IN ('dir /b *.jpg') DO "%~dp0..\dependencies/magick/magick.exe" convert "%~dp0..\custom_textures\score_box/%%G" "%~dp0..\custom_textures\score_box\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.bmp') DO "%~dp0..\dependencies/magick/magick.exe" convert "%~dp0..\custom_textures\score_box/%%G" "%~dp0..\custom_textures\score_box\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0..\dependencies/windows/superfreq.exe" png2tex "%~dp0..\custom_textures\score_box/%%G" "%~dp0..\_ark\ui\track\score_box\gen\%%~nG.png_xbox" --platform x360 --miloVersion 26
del sed* /a /s
cd "%~dp0..\_ark/ui/track/score_box/gen"
FOR /F "tokens=*" %%G IN ('dir /b *.png_xbox') DO python "%~dp0..\dependencies/swap_rb_art_bytes.py" "%~dp0..\_ark/ui/track/score_box/gen/%%G" "%~dp0..\_ark/ui/track/score_box/gen/%%~nG.png_ps3"
