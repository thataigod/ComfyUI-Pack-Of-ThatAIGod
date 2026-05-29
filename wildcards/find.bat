@echo off
setlocal enabledelayedexpansion

:: === CONFIGURATION ===
set "searchWord=fan"
set "searchFolder=%~dp0autowildcards"

echo Searching for "%searchWord%" in "%searchFolder%"...
echo.

:: Use quotes properly to handle spaces in paths
for /R "%searchFolder%" %%f in (*) do (
    findstr /I /C:"%searchWord%" "%%f" >nul 2>&1
    if !errorlevel! neq 1 (
        echo ========================================
        echo File: "%%f"
        echo ----------------------------------------
        findstr /N /I /C:"%searchWord%" "%%f"
        echo.
    )
)

echo Search complete.
pause
