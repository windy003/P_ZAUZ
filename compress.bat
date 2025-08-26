@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Compressing: %~1
echo Current directory: %cd%

REM Use specified Python path
"C:\Users\92892\AppData\Local\Programs\Python\Python313\python.exe" zip_tool.py -c "%~1"

REM Auto close after completion
exit