@echo off
pushd "%~dp0"
chcp 65001 >nul 2>nul
where py >nul 2>nul && (set PY=py) || (set PY=python)
echo.
echo   === LOS VERSOS ===
%PY% medir_contra_corpus.py --salida medicion-versos.json
echo.
echo   === EL COMENTARIO ===
%PY% medir_contra_corpus.py --comentario --salida medicion-comentario.json
echo.
popd
pause
