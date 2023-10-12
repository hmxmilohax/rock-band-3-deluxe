@echo off
cd "%~dp0.."
del /s /q obj\*.dtb
python dependencies\python\configure_build.py xbox
dependencies\windows\ninja
PAUSE