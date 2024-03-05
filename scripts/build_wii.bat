@echo off
cd "%~dp0"
set "dolphin_path="
set "base_dol_path="
set "debug_dol_path="
set "config_file=dx_config.ini"

for /f "tokens=1,* delims== " %%A in (%config_file%) do (
    if "%%A"=="dolphin_path" set "dolphin_path=%%~B"
    if "%%A"=="base_dol_path" set "base_dol_path=%%~B"
    if "%%A"=="debug_dol_path" set "debug_dol_path=%%~B"
)

if defined dolphin_path echo 1.0 dol path set, copying files on completion
if defined base_dol_path echo Dolphin directory set, launching Dolphin on completion
if defined debug_dol_path echo Debug dol path set, launching debug instead of vanilla

cd "%~dp0.."
del >nul 2>&1 /s /q obj\wii\*.dtb
python dependencies\python\configure_build.py wii --fun
dependencies\windows\ninja
if %errorlevel% neq 0 (pause /b %errorlevel% && exit /b %errorlevel%)

if not defined dolphin_path (
    start "" "%~dp0..\out\wii\files"
    goto :end
)

if not defined base_dol_path goto :end
copy "%~dp0..\out\wii\files\gen\main_wii.hdr" "%base_dol_path%\..\files\gen\main_wii.hdr" >nul
copy "%~dp0..\out\wii\files\gen\main_wii_10.ark" "%base_dol_path%\..\files\gen\main_wii_10.ark" >nul
if defined debug_dol_path goto :copy_debug
START "" "%dolphin_path%\dolphin.exe" "%base_dol_path%\main.dol"

:copy_debug
copy "%~dp0..\out\wii\files\gen\main_wii.hdr" "%debug_dol_path%\..\files\gen\main_wii.hdr" >nul
copy "%~dp0..\out\wii\files\gen\main_wii_10.ark" "%debug_dol_path%\..\files\gen\main_wii_10.ark" >nul
START "" "%dolphin_path%\dolphin.exe" "%debug_dol_path%\main.dol"

:end