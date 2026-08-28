@echo off
chcp 65001 >nul
cd /d "%~dp0"
setlocal

where py >nul 2>&1 && (set PY=py) || (
  where python >nul 2>&1 && (set PY=python) || (
    where python3 >nul 2>&1 && (set PY=python3) || (
      echo.
      echo   No encuentro Python en esta computadora.
      echo   Instalalo desde https://www.python.org/downloads/ y marca
      echo   la casilla "Add python.exe to PATH" durante la instalacion.
      echo.
      pause
      exit /b 1
    )
  )
)

echo.
echo   Abriendo la pantalla del solucionador...
echo   Se abre sola en el navegador. Para cerrarla, cerra esta ventana.
echo.

%PY% pantalla.py

echo.
pause
