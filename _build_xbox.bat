git pull https://github.com/hmxmilohax/rock-band-3-deluxe main
@echo off
echo:
echo:Temporarily moving PS3 files out of the ark path to reduce final ARK size
@%SystemRoot%\System32\robocopy.exe "%~dp0\_ark" "%~dp0_temp\_ark" *.milo_ps3 /S /MOVE /XD "%~dp0_temp\_ark" /NDL /NFL /NJH /NJS /R:0 >nul
@%SystemRoot%\System32\robocopy.exe "%~dp0\_ark" "%~dp0_temp\_ark" *.png_ps3 /S /MOVE /XD "%~dp0_temp\_ark" /NDL /NFL /NJH /NJS /R:0 >nul
@%SystemRoot%\System32\robocopy.exe "%~dp0\_ark" "%~dp0_temp\_ark" *.bmp_ps3 /S /MOVE /XD "%~dp0_temp\_ark" /NDL /NFL /NJH /NJS /R:0 >nul
echo:
echo:Building Xbox ARK
"%~dp0dependencies/arkhelper" dir2ark "%~dp0\_ark" "%~dp0\_build\xbox\gen" -n "patch_xbox" -e -v 6
echo:
echo:Moving back PS3 files
echo:
@%SystemRoot%\System32\robocopy.exe "%~dp0_temp\_ark" "%~dp0\_ark" *.milo_ps3 /S /MOVE /XD "%~dp0_ark" /NDL /NFL /NJH /NJS /R:0 >nul
@%SystemRoot%\System32\robocopy.exe "%~dp0_temp\_ark" "%~dp0\_ark" *.png_ps3 /S /MOVE /XD "%~dp0_ark" /NDL /NFL /NJH /NJS /R:0 >nul
@%SystemRoot%\System32\robocopy.exe "%~dp0_temp\_ark" "%~dp0\_ark" *.bmp_ps3 /S /MOVE /XD "%~dp0_ark" /NDL /NFL /NJH /NJS /R:0 >nul
rd _temp
echo:Successfully built Rock Band 3 Deluxe ARK. You may find the files needed to place on your Xbox 360 in /_build/Xbox/
pause