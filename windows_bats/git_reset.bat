@echo off
cd "%~dp0../user_scripts"
echo You are about to reset the repo. Close this window to abort, or press any key to proceed.
PAUSE
python "%~dp0../user_scripts/git_reset.py"
PAUSE