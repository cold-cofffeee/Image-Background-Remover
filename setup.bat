@echo off
REM Setup script for Windows
echo ========================================
echo Image Background Remover - Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo Step 1: Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat

echo Step 3: Upgrading pip...
python -m pip install --upgrade pip

echo Step 4: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo Step 5: Downloading model file...
python download_model.py
if errorlevel 1 (
    echo WARNING: Model download failed. You may need to download it manually.
    echo See DEPLOYMENT.md for instructions.
)

echo Step 6: Creating .env file...
if not exist .env (
    copy .env.example .env
    echo Created .env file from .env.example
    echo Please edit .env file with your configuration
) else (
    echo .env file already exists, skipping...
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the application:
echo   1. Activate virtual environment: venv\Scripts\activate
echo   2. Run: python app.py
echo.
echo Or use: start.bat
echo.
pause
