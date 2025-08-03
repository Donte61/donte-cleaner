@echo off
title DonTe Cleaner v2.0

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                    DonTe Cleaner v2.0                     ║
echo ║           Professional Windows Optimization Tool           ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Starting DonTe Cleaner...

REM Change to script directory
cd /d "%~dp0"

REM Try pythonw.exe first (no console), fallback to python.exe
pythonw.exe main.py 2>nul
if errorlevel 1 (
    echo Warning: pythonw.exe not found, using python.exe
    python.exe main.py
)

echo.
echo DonTe Cleaner has been closed.
pause
