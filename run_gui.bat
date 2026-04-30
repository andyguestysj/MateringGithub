@echo off
cd /d "%~dp0"
echo Starting TTRPG Campaign Manager GUI...
echo.
python -m src.main
if errorlevel 1 (
    echo.
    echo The application closed with an error.
    echo Check the messages above.
    pause
)
