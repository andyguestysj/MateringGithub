@echo off
echo ===============================
echo TTRPG Project VENV Setup
echo ===============================

REM Check if .venv folder exists
if exist ".venv" (
    echo Virtual environment already exists.
) else (
    echo Creating virtual environment...
    python -m venv .venv

    if errorlevel 1 (
        echo Failed to create virtual environment.
        echo Make sure Python is installed and on PATH.
        pause
        exit /b 1
    )

    echo Virtual environment created.
)

REM Activate the virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Optional: install requirements if file exists
if exist "requirements.txt" (
    echo Installing dependencies...
    pip install -r requirements.txt
) else (
    echo No requirements.txt found, skipping install.
)

echo.
echo ===============================
echo Environment ready!
echo ===============================
echo.

REM Keep terminal open
cmd /k