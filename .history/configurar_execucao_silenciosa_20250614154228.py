#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para configurar execução silenciosa do MediaSlayer
Remove a tela preta do terminal
"""

import os
import sys
from pathlib import Path
import winshell
from win32com.client import Dispatch

def criar_atalho_silencioso():
    """Criar atalho silencioso na área de trabalho"""
    try:
        desktop = winshell.desktop()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Usar o launcher .pyw para execução silenciosa
        pyw_launcher = os.path.join(script_dir, "mediaslayer_launcher.pyw")
        
        if not os.path.exists(pyw_launcher):
            print("❌ Arquivo mediaslayer_launcher.pyw não encontrado!")
            return False
        
        # Criar atalho
        shell = Dispatch('WScript.Shell')
        shortcut_path = os.path.join(desktop, "MediaSlayer (Silencioso).lnk")
        shortcut = shell.CreateShortCut(shortcut_path)
        
        # Configurar atalho para execução silenciosa
        shortcut.Targetpath = pyw_launcher
        shortcut.WorkingDirectory = script_dir
        
        # Usar ícone personalizado se existir
        icon_path = os.path.join(script_dir, "mediaslayer.ico")
        if os.path.exists(icon_path):
            shortcut.IconLocation = icon_path
        else:
            shortcut.IconLocation = sys.executable.replace('python.exe', 'pythonw.exe') + ",0"
        
        shortcut.Description = "MediaSlayer - Execução Silenciosa (Sem Terminal)"
        shortcut.save()
        
        print("✅ Atalho silencioso criado com sucesso!")
        print(f"📍 Local: {shortcut_path}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar atalho silencioso: {str(e)}")
        return False

def atualizar_atalho_existente():
    """Atualizar atalho existente para execução silenciosa"""
    try:
        desktop = winshell.desktop()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        shortcut_path = os.path.join(desktop, "MediaSlayer.lnk")
        
        if not os.path.exists(shortcut_path):
            print("❌ Atalho MediaSlayer.lnk não encontrado na área de trabalho")
            return False
        
        # Atualizar atalho existente
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        
        # Usar o launcher .pyw
        pyw_launcher = os.path.join(script_dir, "mediaslayer_launcher.pyw")
        if os.path.exists(pyw_launcher):
            shortcut.Targetpath = pyw_launcher
            shortcut.Arguments = ""
        else:
            # Fallback para pythonw
            python_exe = sys.executable.replace('python.exe', 'pythonw.exe')
            script_path = os.path.join(script_dir, "media_downloader_gui.py")
            shortcut.Targetpath = python_exe
            shortcut.Arguments = f'"{script_path}"'
        
        shortcut.WorkingDirectory = script_dir
        shortcut.Description = "MediaSlayer - Universal Video Downloader (Silencioso)"
        shortcut.save()
        
        print("✅ Atalho existente atualizado para execução silenciosa!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao atualizar atalho: {str(e)}")
        return False

def criar_bat_silencioso():
    """Criar arquivo .bat otimizado para execução silenciosa"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        bat_path = os.path.join(script_dir, "MediaSlayer_Silencioso.bat")
        
        bat_content = '''@echo off
REM MediaSlayer - Execução Silenciosa
cd /d "%~dp0"

REM Verificar se existe o launcher .pyw
if exist "mediaslayer_launcher.pyw" (
    start "" "mediaslayer_launcher.pyw"
) else (
    REM Fallback para pythonw
    start "" pythonw "media_downloader_gui.py"
)

REM Sair imediatamente sem pausar
exit /b 0
'''
        
        with open(bat_path, 'w', encoding='utf-8') as f:
            f.write(bat_content)
        
        print(f"✅ Arquivo batch silencioso criado: {bat_path}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar arquivo batch: {str(e)}")
        return False

def verificar_dependencias():
    """Verificar se as dependências estão instaladas"""
    try:
        import winshell
        import win32com.client
        return True
    except ImportError:
        print("❌ Dependências não encontradas!")
        print("Execute: pip install pywin32 winshell")
        return False

def main():
    """Menu principal"""
    print("=" * 60)
    print("🛡️  MEDIASLAYER - CONFIGURAÇÃO DE EXECUÇÃO SILENCIOSA")
    print("=" * 60)
    print()
    print("Este script remove a tela preta (terminal) que aparece")
    print("quando você executa o MediaSlayer.")
    print()
    
    if not verificar_dependencias():
        input("Pressione Enter para sair...")
        return
    
    while True:
        print("\n📋 OPÇÕES DISPONÍVEIS:")
        print("1. ✨ Criar novo atalho silencioso")
        print("2. 🔄 Atualizar atalho existente")
        print("3. 📁 Criar arquivo .bat silencioso")
        print("4. 🚀 Fazer tudo (recomendado)")
        print("5. ❌ Sair")
        print()
        
        escolha = input("Escolha uma opção (1-5): ").strip()
        
        if escolha == "1":
            print("\n🔨 Criando atalho silencioso...")
            criar_atalho_silencioso()
            
        elif escolha == "2":
            print("\n🔄 Atualizando atalho existente...")
            atualizar_atalho_existente()
            
        elif escolha == "3":
            print("\n📁 Criando arquivo batch silencioso...")
            criar_bat_silencioso()
            
        elif escolha == "4":
            print("\n🚀 Executando todas as configurações...")
            print("\n1/3 - Criando atalho silencioso...")
            criar_atalho_silencioso()
            print("\n2/3 - Atualizando atalho existente...")
            atualizar_atalho_existente()
            print("\n3/3 - Criando arquivo batch silencioso...")
            criar_bat_silencioso()
            print("\n✅ Todas as configurações concluídas!")
            print("\n💡 DICAS:")
            print("• Use o atalho 'MediaSlayer (Silencioso)' para execução sem terminal")
            print("• O arquivo MediaSlayer_Silencioso.bat também executa sem terminal")
            print("• O atalho original foi atualizado para execução silenciosa")
            
        elif escolha == "5":
            print("\n👋 Saindo...")
            break
            
        else:
            print("❌ Opção inválida! Escolha entre 1-5.")
    
    print("\n🎯 Configuração concluída!")
    print("Agora o MediaSlayer não mostrará mais a tela preta do terminal.")
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main() 