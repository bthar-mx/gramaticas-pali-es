@echo off
chcp 65001 >nul
cd /d "%~dp0"
setlocal
where py >nul 2>&1 && (set PY=py) || (set PY=python)
%PY% solucionar_sandhis.py --cobertura
echo.
pause
