@echo off
title MediaSlayer - Universal Video Downloader
echo ========================================
echo    ⚔️ MediaSlayer - Iniciando... 🛡️
echo ========================================
echo.

cd /d "%~dp0"
python media_downloader_gui.py

if errorlevel 1 (
    echo.
    echo ❌ Erro ao executar o MediaSlayer!
    echo Verifique se o Python está instalado.
    echo Execute install_mediaslayer.bat primeiro.
    pause
) 