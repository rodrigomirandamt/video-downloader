@echo off
title 🐦 Baixador de Vídeos do Twitter
cd /d "%~dp0"

echo.
echo ========================================
echo    🐦 Baixador de Vídeos do Twitter
echo ========================================
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

REM Run the Twitter video downloader
echo 🚀 Iniciando baixador de vídeos...
python baixar_video_twitter.py

pause 