@echo off
REM ReWear Clothing System - Quick Start Script for Windows

echo.
echo ========================================
echo ReWear Clothing System - Quick Setup
echo ========================================
echo.

REM Check Python version
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo Found %PYTHON_VERSION%
echo.

REM Setup backend
echo Setting up Backend...
cd backend

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo Warning: Please update .env file with your configuration
)

echo Backend setup complete
echo.

REM Return to root directory
cd ..

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To run ReWear:
echo.
echo 1. Start Backend (Terminal 1):
echo    cd backend
echo    venv\Scripts\activate
echo    python app.py
echo.
echo 2. Start Frontend (Terminal 2):
echo    cd frontend
echo    python -m http.server 8000
echo.
echo 3. Open browser:
echo    http://localhost:8000
echo.
echo API Documentation: See docs/API_DOCUMENTATION.md
echo System Architecture: See SYSTEM_ARCHITECTURE.md
echo ReadMe: See README.md
echo.
echo Happy sustainable shopping!
echo.
pause
