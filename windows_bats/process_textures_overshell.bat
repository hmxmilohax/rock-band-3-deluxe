cd "%~dp0..\custom_textures/overshell/rb4_early"
FOR /F "tokens=*" %%G IN ('dir /b *.jpg') DO "%~dp0..\dependencies\magick\magick.exe" convert "%~dp0..\custom_textures\overshell/rb4_early/%%G" "%~dp0..\custom_textures\overshell/rb4_early\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.bmp') DO "%~dp0..\dependencies\magick\magick.exe" convert "%~dp0..\custom_textures\overshell/rb4_early/%%G" "%~dp0..\custom_textures\overshell/rb4_early\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0..\dependencies\superfreq.exe" png2tex "%~dp0..\custom_textures\overshell/rb4_early/%%G" "%~dp0..\_ark\ui\overshell/rb4_early\gen\%%~nG.png_xbox" --platform x360 --miloVersion 26
cd "%~dp0..\_ark/ui/overshell/rb4_early/gen"
FOR /F "tokens=*" %%G IN ('dir /b *.png_xbox') DO python "%~dp0..\dependencies\swap_rb_art_bytes.py" "%~dp0..\_ark/ui/overshell/rb4_early/gen/%%G" "%~dp0..\_ark/ui/overshell/rb4_early/gen/%%~nG.png_ps3"
cd "%~dp0..\custom_textures/overshell/rb4_rivals"
FOR /F "tokens=*" %%G IN ('dir /b *.jpg') DO "%~dp0..\dependencies\magick\magick.exe" convert "%~dp0..\custom_textures\overshell/rb4_rivals/%%G" "%~dp0..\custom_textures\overshell/rb4_rivals\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.bmp') DO "%~dp0..\dependencies\magick\magick.exe" convert "%~dp0..\custom_textures\overshell/rb4_rivals/%%G" "%~dp0..\custom_textures\overshell/rb4_rivals\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0..\dependencies\superfreq.exe" png2tex "%~dp0..\custom_textures\overshell/rb4_rivals/%%G" "%~dp0..\_ark\ui\overshell/rb4_rivals\gen\%%~nG.png_xbox" --platform x360 --miloVersion 26
cd "%~dp0..\_ark/ui/overshell/rb4_rivals/gen"
FOR /F "tokens=*" %%G IN ('dir /b *.png_xbox') DO python "%~dp0..\dependencies\swap_rb_art_bytes.py" "%~dp0..\_ark/ui/overshell/rb4_rivals/gen/%%G" "%~dp0..\_ark/ui/overshell/rb4_rivals/gen/%%~nG.png_ps3"
pause