@echo off
title ⚔️ MediaSlayer - Universal Video Downloader
cd /d "%~dp0"

echo.
echo ========================================
echo    ⚔️ MediaSlayer - Universal Downloader
echo ========================================
echo.
echo Iniciando interface gráfica...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado!
    echo Por favor, instale Python de https://python.org
    echo.
    pause
    exit /b 1
)

REM Check if yt-dlp is installed
python -c "import yt_dlp" >nul 2>&1
if errorlevel 1 (
    echo 📦 Instalando yt-dlp...
    pip install yt-dlp
    if errorlevel 1 (
        echo ❌ Erro ao instalar yt-dlp
        pause
        exit /b 1
    )
    echo ✅ yt-dlp instalado com sucesso!
    echo.
)

REM Run the MediaSlayer GUI
echo 🚀 Abrindo MediaSlayer...
python media_downloader_gui.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ❌ Ocorreu um erro. Verifique a mensagem acima.
    pause
) 