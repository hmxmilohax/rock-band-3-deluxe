@echo off
cd "%~dp0.."
python dependencies\python\configure_build.py ps3
dependencies\windows\ninja
PAUSE