@echo off
cd "%~dp0.."
echo Deleting old Xbox DTBs, if present...
del >nul 2>&1 /s /q obj\xbox\*.dtb
echo.
python dependencies\python\configure_build.py xbox
dependencies\windows\ninja
PAUSE