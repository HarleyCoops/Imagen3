@echo off
REM Setup script for Imagen 3 API Integration
REM This script installs dependencies and runs the test setup

echo Setting up Imagen 3 API Integration...
echo =======================================

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Python is required but not installed.
    echo Please install Python and try again.
    exit /b 1
)

REM Check if pip is installed
pip --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: pip is required but not installed.
    echo Please install pip and try again.
    exit /b 1
)

REM Create virtual environment (optional)
set /p create_venv=Do you want to create a virtual environment? (y/n): 

if /i "%create_venv%"=="y" (
    echo Creating virtual environment...
    
    REM Check if venv module is available
    python -m venv --help >nul 2>&1
    if %ERRORLEVEL% neq 0 (
        echo Error: Python venv module is not available.
        echo Please install the Python venv package and try again.
        exit /b 1
    )
    
    REM Create and activate virtual environment
    python -m venv venv
    call venv\Scripts\activate.bat
    
    echo Virtual environment created and activated.
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

if %ERRORLEVEL% neq 0 (
    echo Error: Failed to install dependencies.
    exit /b 1
)

echo Dependencies installed successfully.

REM Prompt for API key if not set
findstr /C:"your_api_key_here" .env >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo.
    echo You need to set up your Gemini API key.
    echo Get your API key from https://makersuite.google.com/
    set /p api_key=Enter your Gemini API key: 
    
    if not "%api_key%"=="" (
        REM Create a temporary file with the updated content
        type .env | findstr /v "GEMINI_API_KEY" > .env.tmp
        echo GEMINI_API_KEY=%api_key% >> .env.tmp
        move /y .env.tmp .env >nul
        echo API key saved to .env file.
    ) else (
        echo No API key provided. You'll need to edit the .env file manually.
    )
)

REM Run the test setup
echo.
echo Running setup test...
python test_setup.py

echo.
echo Setup complete!
echo To generate images, run: python app.py "your prompt here"
echo To start the web interface, run: python web_interface.py
