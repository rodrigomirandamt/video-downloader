@echo off
title YouTube Video Downloader
cd /d "%~dp0"

echo Starting YouTube Video Downloader...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if yt-dlp is installed
python -c "import yt_dlp" >nul 2>&1
if errorlevel 1 (
    echo Installing yt-dlp...
    pip install yt-dlp
    if errorlevel 1 (
        echo Error: Failed to install yt-dlp
        pause
        exit /b 1
    )
)

REM Run the GUI
python youtube_gui.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo An error occurred. Check the message above.
    pause
) 