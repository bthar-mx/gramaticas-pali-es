@echo off
chcp 65001 >nul
cd /d "%~dp0"
setlocal
where py >nul 2>&1 && (set PY=py) || (set PY=python)
echo.
echo   Comparando cada archivo que el motor lee contra su huella guardada.
echo   "igual" es lo que se espera. Cualquier "CAMBIO" o "FALTA" es el aviso.
echo.
%PY% congelar.py
echo.
pause
