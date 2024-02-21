@echo off
cd "%~dp0.."
echo Deleting old Wii DTBs, if present...
del >nul 2>&1 /s /q obj\wii\*.dtb
echo.
python dependencies\dev_scripts\add_devbuild.py
python dependencies\python\configure_build.py wii --fun
dependencies\windows\ninja
python dependencies\dev_scripts\remove_devbuild.py
PAUSE