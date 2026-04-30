@echo off
cd /d "%~dp0"
echo ===============================
echo TTRPG Project VENV Setup
echo ===============================

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
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

if exist "requirements.txt" (
    echo Installing dependencies...
    pip install -r requirements.txt
) else (
    echo No requirements.txt found, skipping install.
)

echo.
echo Environment ready.
echo To run the GUI, type:
echo python -m src.main
echo.
cmd /k
