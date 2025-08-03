@echo off
cd /d "%~dp0"
echo =============================================
echo    DonTe Cleaner - Yonetici Modu Baslatiyor
echo =============================================
echo.
echo Program yonetici izinleri ile calistirilacak.
echo Lutfen UAC (Kullanici Hesabi Denetimi) penceresinde "Evet" seciniz.
echo.
echo Eger stil hatasi alirsaniz:
echo 1. test_simple.py dosyasini deneyin
echo 2. Bu batch dosyasini yonetici olarak calistirin
echo.
pause
echo.
echo Yonetici olarak baslatiliyor...
powershell -Command "Start-Process python -ArgumentList 'main.py' -Verb RunAs"
echo.
echo Eger pencere acilmazsa, CMD'yi yonetici olarak acip 'python main.py' yazin.
pause
