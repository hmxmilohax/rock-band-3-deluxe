@echo off
cd "%~dp0.."
python dependencies\python\configure_build.py xbox
dependencies\windows\ninja
PAUSE