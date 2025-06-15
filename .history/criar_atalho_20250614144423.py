#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar atalho do MediaSlayer na área de trabalho
"""

import os
import winshell
from win32com.client import Dispatch

def criar_atalho_desktop():
    """Criar atalho na área de trabalho"""
    try:
        # Caminho do script atual
        script_dir = os.path.dirname(os.path.abspath(__file__))
        bat_file = os.path.join(script_dir, "MediaSlayer.bat")
        
        # Caminho da área de trabalho
        desktop = winshell.desktop()
        
        # Caminho do atalho
        shortcut_path = os.path.join(desktop, "⚔️ MediaSlayer.lnk")
        
        # Criar atalho
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = bat_file
        shortcut.WorkingDirectory = script_dir
        shortcut.Description = "MediaSlayer - Universal Video Downloader"
        shortcut.save()
        
        print("✅ Atalho criado na área de trabalho!")
        print(f"📂 Local: {shortcut_path}")
        
    except ImportError:
        print("❌ Módulos necessários não encontrados.")
        print("💡 Instale com: pip install pywin32 winshell")
        
        # Método alternativo usando PowerShell
        criar_atalho_powershell()
        
    except Exception as e:
        print(f"❌ Erro ao criar atalho: {str(e)}")
        criar_atalho_powershell()

def criar_atalho_powershell():
    """Criar atalho usando PowerShell"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        bat_file = os.path.join(script_dir, "MediaSlayer.bat")
        
        # Script PowerShell para criar atalho
        ps_script = f'''
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\\Desktop\\⚔️ MediaSlayer.lnk")
$Shortcut.TargetPath = "{bat_file}"
$Shortcut.WorkingDirectory = "{script_dir}"
$Shortcut.Description = "MediaSlayer - Universal Video Downloader"
$Shortcut.Save()
'''
        
        # Executar PowerShell
        import subprocess
        result = subprocess.run(['powershell', '-Command', ps_script], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Atalho criado na área de trabalho usando PowerShell!")
        else:
            print("❌ Erro ao criar atalho via PowerShell")
            criar_atalho_manual()
            
    except Exception as e:
        print(f"❌ Erro no PowerShell: {str(e)}")
        criar_atalho_manual()

def criar_atalho_manual():
    """Instruções para criar atalho manualmente"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bat_file = os.path.join(script_dir, "MediaSlayer.bat")
    
    print("\n📋 Para criar o atalho manualmente:")
    print("1. Clique com botão direito na área de trabalho")
    print("2. Selecione 'Novo' > 'Atalho'")
    print(f"3. Cole este caminho: {bat_file}")
    print("4. Clique em 'Avançar'")
    print("5. Digite o nome: ⚔️ MediaSlayer")
    print("6. Clique em 'Concluir'")

if __name__ == "__main__":
    print("⚔️ Criador de Atalho do MediaSlayer")
    print("=" * 40)
    criar_atalho_desktop() 