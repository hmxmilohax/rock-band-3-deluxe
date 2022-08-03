cd "%~dp0custom_textures/custom_track_textures"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0dependencies/magick/magick.exe" convert "%~dp0custom_textures\custom_track_textures/%%G" "%~dp0custom_textures\custom_track_textures\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.jpg') DO "%~dp0dependencies/magick/magick.exe" convert "%~dp0custom_textures\custom_track_textures/%%G" "%~dp0custom_textures\custom_track_textures\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.bmp') DO "%~dp0dependencies/magick/magick.exe" convert "%~dp0custom_textures\custom_track_textures/%%G" "%~dp0custom_textures\custom_track_textures\%%~nG.png"
FOR /F "tokens=*" %%G IN ('dir /b *.png') DO "%~dp0dependencies/superfreq.exe" png2tex "%~dp0custom_textures\custom_track_textures/%%G" "%~dp0_ark\ui\track\custom_track_textures\gen\%%~nG.png_xbox" --platform x360 --miloVersion 26
cd "%~dp0_ark/ui/track/custom_track_textures/gen"
FOR /F "tokens=*" %%G IN ('dir /b *.png_xbox') DO python "%~dp0dependencies/swap_rb_art_bytes.py" "%~dp0_ark/ui/track/custom_track_textures/gen/%%G" "%~dp0_ark/ui/track/custom_track_textures/gen/%%~nG.png_ps3"