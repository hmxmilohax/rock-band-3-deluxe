@echo off
cd "%~dp0"
set "rpcs3_path="
set "base_eboot_path="
set "config_file=dx_config.ini"

for /f "tokens=1,* delims== " %%A in (%config_file%) do (
    if "%%A"=="rpcs3_path" set "rpcs3_path=%%~B"
    if "%%A"=="rpcs3_rb3e" set "rpcs3_rb3e=%%~B"
    if "%%A"=="base_eboot_path" set "base_eboot_path=%%~B"
    if "%%A"=="run_rich_presence" set "run_rich_presence=%%~B"
)

if defined rpcs3_path echo RPCS3 directory set, copying files on completion
if defined base_eboot_path echo 1.0 eboot path set, launching RPCS3 on completion
if defined run_rich_presence echo Rich Presence Enabled
if defined rpcs3_rb3e echo RB3Enhanced installed, skipping eboot copy

cd "%~dp0.."
del >nul 2>&1 /s /q obj\ps3\*.dtb
python dependencies\python\configure_build.py ps3 --fun
dependencies\windows\ninja
if %errorlevel% neq 0 (pause /b %errorlevel% && exit /b %errorlevel%)

if not defined rpcs3_path (
    start "" "%~dp0..\out\ps3"
    goto :end
)

copy "%~dp0..\out\ps3\USRDIR\gen\patch_ps3.hdr" "%rpcs3_path%\dev_hdd0\game\BLUS30463\USRDIR\gen\patch_ps3.hdr" >nul
copy "%~dp0..\out\ps3\USRDIR\gen\patch_ps3_0.ark" "%rpcs3_path%\dev_hdd0\game\BLUS30463\USRDIR\gen\patch_ps3_0.ark" >nul
copy "%~dp0..\out\ps3\USRDIR\band_s.self" "%rpcs3_path%\dev_hdd0\game\BLUS30463\USRDIR\band_s.self" >nul
copy "%~dp0..\out\ps3\ICON0.PNG" "%rpcs3_path%\dev_hdd0\game\BLUS30463\ICON0.PNG" >nul
copy "%~dp0..\out\ps3\ICON1.PAM" "%rpcs3_path%\dev_hdd0\game\BLUS30463\ICON1.PAM" >nul
copy "%~dp0..\out\ps3\PIC1.PNG" "%rpcs3_path%\dev_hdd0\game\BLUS30463\PIC1.PNG" >nul
if defined rpcs3_rb3e goto :rpcs3_start
copy "%~dp0..\out\ps3\USRDIR\EBOOT.BIN" "%rpcs3_path%\dev_hdd0\game\BLUS30463\USRDIR\EBOOT.BIN" >nul

:rpcs3_start
if not defined base_eboot_path goto :end
taskkill /IM rpcs3.exe /F
START "" "%rpcs3_path%\rpcs3.exe" "%base_eboot_path%" --no-gui

if not defined run_rich_presence goto :end
cd "%~dp0"
START /B python dx_discordrp.py

:end