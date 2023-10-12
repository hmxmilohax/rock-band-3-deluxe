@echo off
cd "%~dp0.."
del /s /q obj\*.dtb
python dependencies\python\configure_build.py ps3
dependencies\windows\ninja
PAUSE