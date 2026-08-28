@echo off
pushd "%~dp0"
chcp 65001 >nul 2>nul
where py >nul 2>nul && (set PY=py) || (set PY=python)
echo.
set BASE=C:\Users\User\Sandhi\fuentes\dpd\dpd-mobile.db
if not exist "%BASE%" (
  echo   No esta en %BASE%
  echo   Arrastra aqui el archivo .db y pulsa Enter:
  set /p BASE=  
)
set BASE=%BASE:"=%
set PYTHONIOENCODING=utf-8
%PY% exportar_dpd.py "%BASE%"
echo.
popd
pause
