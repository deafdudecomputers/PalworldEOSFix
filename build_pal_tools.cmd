@echo off
title Palworld Tools Builder
echo ========================================
echo   CLEANING PREVIOUS BUILDS
echo ========================================
if exist PalworldEOSFix rmdir /s /q PalworldEOSFix
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
echo.
echo ========================================
echo   BUILDING PALWORLD FIXER TOOLS
echo ========================================
if not exist pal.ico (
    echo [ERROR] pal.ico not found! 
    echo Please place pal.ico in this folder.
    pause
    exit /b
)
echo [1/2] Building PalworldEOSFix.exe...
pyinstaller --clean --onefile --noconsole --uac-admin --icon=pal.ico --add-data "pal.ico;." PalworldEOSFix.py
echo.
echo [2/2] Building PalworldEOSTest.exe...
pyinstaller --clean --onefile --noconsole --uac-admin --icon=pal.ico --add-data "pal.ico;." PalworldEOSTest.py
echo.
echo ========================================
echo   CLEANING UP TEMPORARY FILES
echo ========================================
if exist build rmdir /s /q build
if exist PalworldEOSFix.spec del /q PalworldEOSFix.spec
if exist PalworldEOSTest.spec del /q PalworldEOSTest.spec
if exist dist (
    ren dist PalworldEOSFix
)
echo.
echo ========================================
echo   BUILD COMPLETE!
echo ========================================
if exist PalworldEOSFix (
    start "" "PalworldEOSFix"
)
pause