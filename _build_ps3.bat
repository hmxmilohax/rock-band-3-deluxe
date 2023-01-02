git pull https://github.com/hmxmilohax/rock-band-3-deluxe main
@echo off
echo:
echo:Temporarily moving Xbox files out of the ark path to reduce final ARK size
@%SystemRoot%\System32\robocopy.exe "%~dp0\_ark" "%~dp0_temp\_ark" *.milo_xbox /S /MOVE /XD "%~dp0_temp\_ark" /NDL /NFL /NJH /NJS /R:0 >nul
@%SystemRoot%\System32\robocopy.exe "%~dp0\_ark" "%~dp0_temp\_ark" *.png_xbox /S /MOVE /XD "%~dp0_temp\_ark" /NDL /NFL /NJH /NJS /R:0 >nul
@%SystemRoot%\System32\robocopy.exe "%~dp0\_ark" "%~dp0_temp\_ark" *.bmp_xbox /S /MOVE /XD "%~dp0_temp\_ark" /NDL /NFL /NJH /NJS /R:0 >nul
echo:
echo:Building PS3 ARK
"%~dp0dependencies/arkhelper" dir2ark "%~dp0\_ark" "%~dp0\_build\ps3\USRDIR\gen" -n "patch_ps3" -e -v 6 >nul
echo:
echo:Moving back Xbox files
echo:
@%SystemRoot%\System32\robocopy.exe "%~dp0_temp\_ark" "%~dp0\_ark" *.milo_xbox /S /MOVE /XD "%~dp0_ark" /NDL /NFL /NJH /NJS /R:0 >nul
@%SystemRoot%\System32\robocopy.exe "%~dp0_temp\_ark" "%~dp0\_ark" *.png_xbox /S /MOVE /XD "%~dp0_ark" /NDL /NFL /NJH /NJS /R:0 >nul
@%SystemRoot%\System32\robocopy.exe "%~dp0_temp\_ark" "%~dp0\_ark" *.bmp_xbox /S /MOVE /XD "%~dp0_ark" /NDL /NFL /NJH /NJS /R:0 >nul
rd _temp
echo:Successfully built Rock Band 3 Deluxe ARK. You may find the files needed to place on your PS3 in /_build/PS3/
pause