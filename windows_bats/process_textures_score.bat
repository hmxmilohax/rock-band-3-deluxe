del /f "%~dp0..\_ark\ui\track\score\score.dta"
cd "%~dp0..\custom_textures\score"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE ren @file !Phile: =_!"
forfiles /s /m *.* /C "cmd /e:on /v:on /c set \"Phile=@file\" & if @ISDIR==FALSE  ren @file !Phile:-=_!"
for /f "Tokens=*" %%f in ('dir /l/b/a-d/s') do (move /y "%%f" "%%f")
for %%i in (*.bmp) do @echo "%%~ni">> score.dta
for %%i in (*.png) do @echo "%%~ni">> score.dta
for %%i in (*.jpg) do @echo "%%~ni">> score.dta
move "%~dp0..\custom_textures\score\score.dta" "%~dp0..\_ark\ui\track\score\score.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/score_meter_wipe_//g" "%~dp0..\_ark\ui\track\score\score.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/score_star_frame_//g" "%~dp0..\_ark\ui\track\score\score.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/score_star_gold_//g" "%~dp0..\_ark\ui\track\score\score.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/scoreboard_frame_//g" "%~dp0..\_ark\ui\track\score\score.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/scoreboard_lens_//g" "%~dp0..\_ark\ui\track\score\score.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/star_multiplier_meter_frame_//g" "%~dp0..\_ark\ui\track\score\score.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/star_multiplier_meter_lens_//g" "%~dp0..\_ark\ui\track\score\score.dta"
"%~dp0..\dependencies/sed.exe" -i -e "s/tour_icon_//g" "%~dp0..\_ark\ui\track\score\score.dta"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0..\dependencies/magick/magick.exe" convert "%~dp0..\custom_textures\score/%%G" "%~dp0..\custom_textures\score\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.jpg') DO "%~dp0..\dependencies/magick/magick.exe" convert "%~dp0..\custom_textures\score/%%G" "%~dp0..\custom_textures\score\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.bmp') DO "%~dp0..\dependencies/magick/magick.exe" convert "%~dp0..\custom_textures\score/%%G" "%~dp0..\custom_textures\score\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0..\dependencies/windows/superfreq.exe" png2tex "%~dp0..\custom_textures\score/%%G" "%~dp0..\_ark\ui\track\score\gen\%%~nG.png_xbox" --platform x360 --miloVersion 26
cd "%~dp0..\_ark/ui/track/score/gen"
FOR /F "tokens=*" %%G IN ('dir /b *.png_xbox') DO python "%~dp0..\dependencies/swap_rb_art_bytes.py" "%~dp0..\_ark/ui/track/score/gen/%%G" "%~dp0..\_ark/ui/track/score/gen/%%~nG.png_ps3"
