@chcp 65001 >nul
@echo off
setlocal

echo.
echo ==================================================
echo        Environmental Initialization Tools
echo ==================================================
echo This Operation Will Run The Following Programs In Sequence:
echo   - get-python.exe
echo   - get-pip.exe
echo   - install-dependency.exe
echo.

echo If Started, Your Current [python standalone], [pip] and [Third-Party Dependencies] Will All Be Directly Removed And Reinstalled.
set /p "confirm=Sure To Start? (y/n):"

if /i not "%confirm%"=="y" (
    echo Operation Cancelled.
    pause
    exit /b 0
)

set "APP1=.\tools\get-python.exe"
set "APP2=.\tools\get-pip.exe"
set "APP3=.\tools\install_dependency.exe"

for %%A in ("%APP1%" "%APP2%" "%APP3%") do (
    if not exist "%%~A" (
        echo Error: The Executable File Not Found %%~A
        echo Please Makesure All Executable Files Are Located In The.\tools\ Directory.
        pause
        exit /b 1
    )
)

echo ==================================================
echo Running %APP1% ...
echo ==================================================
call "%APP1%"
if %ERRORLEVEL% NEQ 0 (
    pause
    exit /b %ERRORLEVEL%
)

echo ==================================================
echo Running %APP2% ...
echo ==================================================
call "%APP2%"
if %ERRORLEVEL% NEQ 0 (
    pause
    exit /b %ERRORLEVEL%
)

echo ==================================================
echo Running %APP3% ...
echo ==================================================
call "%APP3%"
if %ERRORLEVEL% NEQ 0 (
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ✅ Succeed!
pause