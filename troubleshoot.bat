@echo off
title DonTe Cleaner - Sorun Giderme
cd /d "%~dp0"
color 0f

echo =============================================
echo    DonTe Cleaner - Sorun Giderme
echo =============================================
echo.
echo Bu araç DonTe Cleaner ile ilgili sorunları tespit eder.
echo.

:menu
echo Secenekler:
echo 1. Basit Test (Minimal GUI)
echo 2. Ana Program (Normal Mod)
echo 3. Ana Program (Yonetici Modu)
echo 4. Sistem Bilgileri
echo 5. Bagimliliklari Kontrol Et
echo 6. Log Dosyasini Gor
echo 7. Cikis
echo.
set /p choice="Seciminizi yapin (1-7): "

if "%choice%"=="1" goto simple_test
if "%choice%"=="2" goto normal_mode
if "%choice%"=="3" goto admin_mode
if "%choice%"=="4" goto system_info
if "%choice%"=="5" goto check_deps
if "%choice%"=="6" goto show_log
if "%choice%"=="7" goto exit

echo Gecersiz secim! Lutfen 1-7 arasinda bir sayi girin.
echo.
goto menu

:simple_test
echo.
echo Basit test baslatiliyor...
python test_simple.py
if errorlevel 1 (
    echo HATA: Basit test bile calismadi!
    echo Python veya tkinter kurulu olmayabilir.
) else (
    echo Basit test tamamlandi.
)
echo.
pause
goto menu

:normal_mode
echo.
echo Normal mod baslatiliyor...
python main.py
echo.
pause
goto menu

:admin_mode
echo.
echo Yonetici modu baslatiliyor...
powershell -Command "Start-Process python -ArgumentList 'main.py' -Verb RunAs"
echo Program arka planda baslatildi.
echo.
pause
goto menu

:system_info
echo.
echo ========== Sistem Bilgileri ==========
echo Python Surumu:
python --version
echo.
echo Pip Surumu:
pip --version
echo.
echo Kurulu Paketler:
pip list | findstr "psutil\|wmi\|requests"
echo.
echo Windows Surumu:
ver
echo.
echo Yonetici Izni:
net session >nul 2>&1
if errorlevel 1 (
    echo Hayir - Normal kullanici
) else (
    echo Evet - Yonetici
)
echo =====================================
echo.
pause
goto menu

:check_deps
echo.
echo ========== Bagimliliklari Kontrol Et ==========
echo Gerekli paketler kontrol ediliyor...
echo.

echo tkinter kontrol ediliyor...
python -c "import tkinter; print('tkinter: OK')" 2>nul || echo "tkinter: HATA!"

echo psutil kontrol ediliyor...
python -c "import psutil; print('psutil: OK')" 2>nul || echo "psutil: HATA!"

echo wmi kontrol ediliyor...
python -c "import wmi; print('wmi: OK')" 2>nul || echo "wmi: HATA!"

echo requests kontrol ediliyor...
python -c "import requests; print('requests: OK')" 2>nul || echo "requests: HATA!"

echo.
echo Eksik paketleri yuklemek icin:
echo pip install -r requirements.txt
echo ============================================
echo.
pause
goto menu

:show_log
echo.
echo ========== Son Log Kayitlari ==========
if exist "logs\*.log" (
    for /f %%i in ('dir /b /o:d logs\*.log') do set lastlog=%%i
    echo Log dosyasi: logs\!lastlog!
    echo.
    type "logs\!lastlog!" | more
) else (
    echo Log dosyasi bulunamadi.
)
echo =====================================
echo.
pause
goto menu

:exit
echo.
echo DonTe Cleaner Sorun Giderme kapanıyor...
exit /b 0
