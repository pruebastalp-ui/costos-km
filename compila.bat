@echo off
echo ==========================================
echo  COMPILADOR EXE - CALCULO DE COSTOS
echo ==========================================

echo.
echo Limpiando compilaciones anteriores...

rmdir /s /q build
rmdir /s /q dist
del *.spec

echo.
echo Generando ejecutable...

pyinstaller --onefile --noconsole ^
 --add-data "templates;templates" ^
 --add-data "static;static" ^
 app.py

echo.
echo ==========================================
echo  COMPILACION FINALIZADA
echo ==========================================
echo.

echo El ejecutable se encuentra en:
echo dist\app.exe

pause