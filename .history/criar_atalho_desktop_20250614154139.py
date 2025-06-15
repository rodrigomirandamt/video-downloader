#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar atalho do MediaSlayer na área de trabalho
"""

import os
import sys
from pathlib import Path
import winshell
from win32com.client import Dispatch

def criar_atalho_desktop():
    """Criar atalho na área de trabalho"""
    try:
        # Caminhos
        desktop = winshell.desktop()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Verificar se existe o launcher .pyw (execução silenciosa)
        pyw_launcher = os.path.join(script_dir, "mediaslayer_launcher.pyw")
        if os.path.exists(pyw_launcher):
            # Usar o launcher .pyw que não mostra terminal
            python_exe = sys.executable.replace('python.exe', 'pythonw.exe')
            script_path = pyw_launcher
        else:
            # Fallback para o script original com pythonw
            python_exe = sys.executable.replace('python.exe', 'pythonw.exe')
            script_path = os.path.join(script_dir, "media_downloader_gui.py")
        
        # Criar atalho
        shell = Dispatch('WScript.Shell')
        shortcut_path = os.path.join(desktop, "MediaSlayer.lnk")
        shortcut = shell.CreateShortCut(shortcut_path)
        
        # Configurar atalho
        shortcut.Targetpath = python_exe
        shortcut.Arguments = f'"{script_path}"'
        shortcut.WorkingDirectory = script_dir
        shortcut.IconLocation = python_exe + ",0"
        shortcut.Description = "MediaSlayer - Universal Video Downloader"
        
        # Salvar
        shortcut.save()
        
        print("✅ Atalho criado com sucesso na área de trabalho!")
        print(f"📍 Local: {shortcut_path}")
        
    except ImportError:
        print("❌ Erro: Instale as dependências necessárias:")
        print("pip install pywin32 winshell")
        
    except Exception as e:
        print(f"❌ Erro ao criar atalho: {str(e)}")

if __name__ == "__main__":
    criar_atalho_desktop()
    input("Pressione Enter para continuar...") 