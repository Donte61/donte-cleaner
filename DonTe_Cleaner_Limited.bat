@echo off
title DonTe Cleaner v2.0 - Limited Mode Startup

cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                    DonTe Cleaner v2.0                     ║
echo ║                     Limited Mode                           ║
echo ║          No Admin Privileges Required                      ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo [INFO] Starting DonTe Cleaner in Limited Mode...
echo [INFO] Some features will be disabled (registry, services)
echo [INFO] Press Ctrl+C anytime to cancel
echo.

REM Set environment variable to skip admin check
set DONTE_LIMITED_MODE=1

REM Change to script directory
cd /d "%~dp0"

REM Start with pythonw.exe for clean experience
pythonw.exe main.py 2>nul

if errorlevel 1 (
    echo [WARN] pythonw.exe failed, trying python.exe...
    python.exe main.py
)

echo.
echo [INFO] DonTe Cleaner Limited Mode has been closed.
pause
