@echo off
cd "%~dp0"
set "xenia_path="
set "base_xex_path="
set "config_file=dx_config.ini"

for /f "tokens=1,* delims== " %%A in (%config_file%) do (
    if "%%A"=="xenia_path" set "xenia_path=%%~B"
    if "%%A"=="base_xex_path" set "base_xex_path=%%~B"
)

if defined xenia_path echo 1.0 xex path set, copying files on completion
if defined base_xex_path echo Xenia directory set, launching Xenia Canary on completion

cd "%~dp0.."
del >nul 2>&1 /s /q obj\xbox\*.dtb
python dependencies\python\configure_build.py xbox --fun
dependencies\windows\ninja
if %errorlevel% neq 0 (pause /b %errorlevel% && exit /b %errorlevel%)

if not defined xenia_path (
    start "" "%~dp0..\out\xbox"
    goto :end
)

if not defined base_xex_path goto :end
copy "%~dp0..\out\xbox\gen\patch_xbox.hdr" "%base_xex_path%\gen\patch_xbox.hdr" >nul
copy "%~dp0..\out\xbox\gen\patch_xbox_0.ark" "%base_xex_path%\gen\patch_xbox_0.ark" >nul
copy "%~dp0..\out\xbox\default.xex" "%base_xex_path%\default.xex" >nul
START "" "%xenia_path%\xenia_canary.exe" "%base_xex_path%\default.xex"

:end