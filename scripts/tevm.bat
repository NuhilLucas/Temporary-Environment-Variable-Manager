@echo off
set "ROOT=%~dp0.."
set "CALLFROM=%CD%"
set "PYTHONPATH=%ROOT%\src"
cd /d "%ROOT%"
"%ROOT%/python_standalone/python.exe" -m tevm.main "%CALLFROM%." tevm %*