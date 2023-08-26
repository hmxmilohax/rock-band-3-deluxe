@echo off
echo:
cd "%~dp0../_build/wii/"
DEL /F RB3Deluxe.iso
echo:Building Wii ISO
wit COPY "wit_input" "RB3Deluxe.iso"