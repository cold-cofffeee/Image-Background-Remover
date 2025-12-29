@echo off
REM Start script for Windows
echo Starting Image Background Remover...
echo.

REM Check if virtual environment exists
if not exist venv (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if model exists
if not exist saved_models\u2net\u2net.pth (
    echo WARNING: Model file not found!
    echo Attempting to download...
    python download_model.py
    if errorlevel 1 (
        echo ERROR: Could not download model. Please run setup.bat
        pause
        exit /b 1
    )
)

REM Start the application
echo Starting Flask application...
python app.py

pause
