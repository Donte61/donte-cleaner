@echo off
title DonTe Cleaner - Starting...

REM Hide this console window and run Python without console
powershell -WindowStyle Hidden -Command "python '%~dp0main_no_console.py'"
