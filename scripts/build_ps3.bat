@echo off
cd "%~dp0.."
echo Deleting old PS3 DTBs, if present...
del >nul 2>&1 /s /q obj\ps3\*.dtb
echo.
python dependencies\python\add_devbuild.py
python dependencies\python\configure_build.py ps3 --fun
dependencies\windows\ninja
python dependencies\python\remove_devbuild.py
PAUSE