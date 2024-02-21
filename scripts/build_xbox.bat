@echo off
cd "%~dp0.."
echo Deleting old Xbox DTBs, if present...
del >nul 2>&1 /s /q obj\xbox\*.dtb
echo.
python dependencies\dev_scripts\add_devbuild.py
python dependencies\python\configure_build.py xbox --fun
dependencies\windows\ninja
python dependencies\dev_scripts\remove_devbuild.py
PAUSE