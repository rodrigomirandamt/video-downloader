@echo off
echo ========================================
echo    MediaSlayer - Instalacao Automatica
echo ========================================
echo.

echo Instalando dependencias...
pip install yt-dlp --upgrade
echo.

echo Verificando instalacao...
python -c "import yt_dlp; print('yt-dlp instalado com sucesso!')"
echo.

echo ========================================
echo    Instalacao concluida!
echo    Execute: python media_downloader_gui.py
echo ========================================
pause 