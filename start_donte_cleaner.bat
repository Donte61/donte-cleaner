@echo off
title DonTe Cleaner v3.0 - Starter

echo ========================================
echo  DonTe Cleaner v3.0 - System Optimizer
echo ========================================
echo.

echo Checking system requirements...

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo ✓ Python found

:: Check if required files exist
if not exist "main.py" (
    echo ERROR: main.py not found
    echo Please ensure you're running this from the DonTe Cleaner directory
    pause
    exit /b 1
)

echo ✓ Main files found

:: Install/Update requirements if needed
if exist "requirements.txt" (
    echo Installing/updating requirements...
    python -m pip install -r requirements.txt --quiet
    echo ✓ Requirements updated
)

:: Check for admin privileges
net session >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Running as Administrator - Full functionality available
    set "ADMIN_MODE=1"
) else (
    echo ⚠ Running without Administrator privileges
    echo   Some optimization features will be limited
    echo   Restart as Administrator for full functionality
    set "ADMIN_MODE=0"
)

echo.
echo Starting DonTe Cleaner...
echo.

:: Start the application
python main.py

:: Check exit code
if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo Application ended with errors
    echo Exit code: %errorlevel%
    echo.
    echo Troubleshooting:
    echo 1. Run diagnostic_tool.py for detailed analysis
    echo 2. Check logs\ directory for error details
    echo 3. Ensure all dependencies are installed
    echo 4. Try running as Administrator
    echo ========================================
    pause
)

echo.
echo DonTe Cleaner closed normally
pause
