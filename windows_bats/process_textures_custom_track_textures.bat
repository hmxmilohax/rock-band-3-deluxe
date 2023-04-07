cd "..\custom_textures/custom_track_textures"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0..\dependencies/magick/magick.exe" convert "%~dp0..\custom_textures\custom_track_textures/%%G" "%~dp0..\custom_textures\custom_track_textures\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.jpg') DO "%~dp0..\dependencies/magick/magick.exe" convert "%~dp0..\custom_textures\custom_track_textures/%%G" "%~dp0..\custom_textures\custom_track_textures\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.bmp') DO "%~dp0..\dependencies/magick/magick.exe" convert "%~dp0..\custom_textures\custom_track_textures/%%G" "%~dp0..\custom_textures\custom_track_textures\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0..\dependencies/superfreq.exe" png2tex "%~dp0..\custom_textures\custom_track_textures/%%G" "%~dp0..\_ark\ui\track\custom_track_textures\gen\%%~nG.png_xbox" --platform x360 --miloVersion 26
cd "%~dp0..\_ark/ui/track/custom_track_textures/gen"
FOR /F "tokens=*" %%G IN ('dir /b *.png_xbox') DO python "%~dp0..\dependencies/swap_rb_art_bytes.py" "%~dp0..\_ark/ui/track/custom_track_textures/gen/%%G" "%~dp0..\_ark/ui/track/custom_track_textures/gen/%%~nG.png_ps3"