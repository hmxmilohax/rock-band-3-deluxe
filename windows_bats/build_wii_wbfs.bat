@echo off
echo:
cd "%~dp0../_build/wii/"
DEL /F RB3Deluxe.wbfs
echo:Building Wii WBFS
wit COPY "wit_input" "RB3Deluxe.wbfs"