@echo off
echo ========================================
echo    MediaSlayer - Instalacao Automatica
echo ========================================
echo.

echo Instalando dependencias...
pip install yt-dlp --upgrade
pip install pywin32 winshell
echo.

echo Verificando instalacao...
python -c "import yt_dlp; print('yt-dlp instalado com sucesso!')"
echo.

echo Criando atalho na area de trabalho...
python criar_atalho_desktop.py
echo.

echo ========================================
echo    Instalacao concluida!
echo    Use o atalho na area de trabalho
echo    ou execute: python media_downloader_gui.py
echo ========================================
pause 