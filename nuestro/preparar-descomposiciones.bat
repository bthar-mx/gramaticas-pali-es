@echo off
pushd "%~dp0"
chcp 65001 >nul 2>nul
where py >nul 2>nul && (set PY=py) || (set PY=python)
echo.
set PYTHONIOENCODING=utf-8
%PY% preparar_descomposiciones.py
echo.
popd
pause
