del "%~dp0gen\main_wii.hdr"
del "%~dp0gen\main_wii_10.ark"
copy "%~dp0vanilla_hdr\main_wii.hdr" "%~dp0gen\main_wii.hdr"
"%~dp0..\..\..\windows\arkhelper.exe" patchcreator "%~dp0gen\main_wii.hdr" "%~dp0..\sys\main.dol" -a "%~dp0_ark" -o %~dp0
del "%~dp0main.dol"