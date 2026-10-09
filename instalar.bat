@echo off
echo ========================================
echo BASA CELULAR FULL - Instalador Automatico
echo 17 Modulos - NOBACI + NICSP + NIIF + BIG4
echo ========================================

python --version >nul 2>&1
if errorlevel 1 (
  echo Python no instalado. Instalando...
  winget install Python.Python.3.11
)

echo Instalando dependencias...
pip install flask pandas requests

echo Creando licencias...
echo {"cliente":"DEMO","tipo":"FULL","modulos":["M1","M2","M3","M4","M5","M6","M7","M8","M9","M10","M11","M12","M13","M14","M15","M16","M17"],"precio":185000} > licencia_FULL.json
echo {"cliente":"Ayuntamiento SDN","tipo":"INDEPENDIENTE","modulos":["M3"],"precio":15000} > licencia_M3.json

echo.
echo Instalacion completa!
echo.
echo Modos de uso:
echo   Independiente: python basa_celular_full_17modulos.py --celula M3
echo   FULL: python basa_celular_full_17modulos.py --full
echo   Gateway: python basa_celular_full_17modulos.py --gateway
echo.
echo Facturacion:
echo   M3 solo = RD$15,000/mes
echo   M3+M1 = RD$30,000/mes
echo   FULL 17 modulos = RD$185,000/mes
echo.
pause
