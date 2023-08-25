@echo off
echo:
rm "%~dp0../_build/wii/RB3Deluxe.wbfs"
echo:Building Wii WBFS
wit COPY "%~dp0../_build/wii/wit_input" "%~dp0../_build/wii/RB3Deluxe.wbfs"