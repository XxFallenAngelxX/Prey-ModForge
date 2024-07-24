@echo off
SETLOCAL

cd /d %~dp0

REM Set console to use UTF-8 encoding
chcp 65001

REM Run the Python script
echo Running Prey-ModForge.py...
python Prey-ModForge.py

REM Keep the console open
exit /b