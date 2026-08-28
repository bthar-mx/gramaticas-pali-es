@echo off
chcp 65001 >nul
cd /d "%~dp0"
setlocal

rem Busca el Python que haya. En Windows el lanzador suele ser «py».
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

%PY% solucionar_sandhis.py %*

echo.
pause
