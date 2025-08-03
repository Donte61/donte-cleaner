@echo off
cd /d "%~dp0"
echo =============================================
echo    DonTe Cleaner - Normal Mod Baslatiyor
echo =============================================
echo.
echo Program sinirli modda calisacak.
echo Bazi ozellikler (hizmet yonetimi, kayit defteri) kullanilmayacak.
echo.
echo Eger stil hatasi alirsaniz, test_simple.py dosyasini calistiriniz.
echo.
pause
echo.
echo Ana program baslatiliyor...
python main.py
if errorlevel 1 (
    echo.
    echo Hata olustu! Basit test surumunu deneyin:
    echo python test_simple.py
    pause
)
