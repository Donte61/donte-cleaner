@echo off
title DonTe Cleaner v2.0 - Professional Startup

cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                    DonTe Cleaner v2.0                     ║
echo ║           Professional Windows Optimization Tool           ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo [INFO] Starting DonTe Cleaner...
echo [INFO] Press Ctrl+C anytime to cancel
echo.

REM Change to script directory
cd /d "%~dp0"

REM Try pythonw.exe first (no console), fallback to python.exe
echo [INFO] Attempting to start with pythonw.exe (silent mode)...
pythonw.exe main.py 2>nul

if errorlevel 1 (
    echo [WARN] pythonw.exe failed, trying python.exe...
    python.exe main.py
    
    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to start DonTe Cleaner
        echo [ERROR] Please ensure Python is installed and in PATH
        echo.
        echo Possible solutions:
        echo 1. Install Python from python.org
        echo 2. Add Python to system PATH
        echo 3. Run from command prompt: python main.py
        echo.
        pause
        exit /b 1
    )
)

echo.
echo [INFO] DonTe Cleaner has been closed.
pause
