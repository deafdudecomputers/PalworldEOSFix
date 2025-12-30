@echo off
title Palworld Tools Builder
echo ========================================
echo   KILLING EXISTING PROCESSES
echo ========================================
:: This ensures the files aren't "in use" before we try to delete/build
taskkill /F /IM PalworldEOSFix.exe /T >nul 2>&1
taskkill /F /IM PalworldEOSTest.exe /T >nul 2>&1
timeout /t 1 /nobreak >nul

echo ========================================
echo   CLEANING PREVIOUS BUILDS
echo ========================================
if exist "PalworldEOSFix" rmdir /s /q "PalworldEOSFix"
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

echo.
echo ========================================
echo   BUILDING PALWORLD FIXER TOOLS
echo ========================================
if not exist pal.ico (
    echo [ERROR] pal.ico not found! 
    pause
    exit /b
)

:: Added --noupx to prevent the python3.dll compression failure
echo [1/2] Building PalworldEOSFix.exe...
pyinstaller --clean --onefile --noconsole --noupx --uac-admin --icon=pal.ico --add-data "pal.ico;." PalworldEOSFix.py

echo.
echo [2/2] Building PalworldEOSTest.exe...
pyinstaller --clean --onefile --noconsole --noupx --uac-admin --icon=pal.ico --add-data "pal.ico;." PalworldEOSTest.py

echo.
echo ========================================
echo   CLEANING UP TEMPORARY FILES
echo ========================================
if exist build rmdir /s /q build
if exist PalworldEOSFix.spec del /q PalworldEOSFix.spec
if exist PalworldEOSTest.spec del /q PalworldEOSTest.spec

if exist "dist" (
    if exist "PalworldEOSFix" rmdir /s /q "PalworldEOSFix"
    ren "dist" "PalworldEOSFix"
)

echo.
echo ========================================
echo   BUILD COMPLETE!
echo ========================================
if exist "PalworldEOSFix" (
    start "" "PalworldEOSFix"
)
pause