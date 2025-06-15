#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simples para baixar vídeos do Twitter/X
Uso: Cole a URL do tweet e o vídeo será baixado
"""

import yt_dlp
import os
import re

def baixar_video_twitter(url_tweet):
    """
    Baixa vídeo de um tweet do Twitter/X
    
    Args:
        url_tweet (str): URL do tweet com vídeo
    """
    
    # Criar pasta para downloads
    pasta_downloads = os.path.join(os.getcwd(), "videos_twitter")
    os.makedirs(pasta_downloads, exist_ok=True)
    
    # Configurações para baixar vídeos do Twitter
    opcoes = {
        'outtmpl': os.path.join(pasta_downloads, '%(uploader)s_%(title)s.%(ext)s'),
        'format': 'best[ext=mp4]/best',  # Prioriza MP4
        'writeinfojson': False,  # Não salvar metadados
        'writethumbnail': False,  # Não salvar thumbnail
        'quiet': True,  # Silenciar saídas desnecessárias
        'no_warnings': True,  # Remover avisos
    }
    
    try:
        print(f"🔍 Analisando tweet: {url_tweet}")
        
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            # Extrair informações primeiro
            info = ydl.extract_info(url_tweet, download=False)
            
            if info:
                titulo = info.get('title', 'Sem título')
                autor = info.get('uploader', 'Desconhecido')
                duracao = info.get('duration', 0)
                
                print(f"📝 Título: {titulo}")
                print(f"👤 Autor: @{autor}")
                if duracao:
                    print(f"⏱️ Duração: {duracao} segundos")
                
                # Verificar se tem vídeo
                if info.get('formats'):
                    print("\n⬇️ Baixando vídeo...")
                    ydl.download([url_tweet])
                    print(f"✅ Vídeo baixado com sucesso!")
                    print(f"📂 Salvo em: {pasta_downloads}")
                else:
                    print("❌ Nenhum vídeo encontrado neste tweet")
            else:
                print("❌ Não foi possível obter informações do tweet")
                
    except Exception as e:
        print(f"❌ Erro ao baixar: {str(e)}")
        print("💡 Verifique se a URL está correta e se o tweet contém vídeo")

def validar_url_twitter(url):
    """Verifica se a URL é válida do Twitter/X"""
    padroes = [
        r'https?://(?:www\.)?twitter\.com/\w+/status/\d+',
        r'https?://(?:www\.)?x\.com/\w+/status/\d+',
        r'https?://t\.co/\w+'
    ]
    return any(re.match(padrao, url) for padrao in padroes)

def main():
    """Função principal"""
    print("🐦 Baixador de Vídeos do Twitter/X")
    print("=" * 40)
    print("Cole a URL do tweet com vídeo que você quer baixar")
    print()
    
    while True:
        url = input("🔗 URL do tweet (ou 'sair' para encerrar): ").strip()
        
        if url.lower() in ['sair', 'exit', 'quit', '']:
            print("👋 Até logo!")
            break
            
        if validar_url_twitter(url):
            print()
            baixar_video_twitter(url)
            print("\n" + "-" * 40)
        else:
            print("❌ URL inválida! Use uma URL do Twitter/X como:")
            print("   https://twitter.com/usuario/status/1234567890")
            print("   https://x.com/usuario/status/1234567890")

if __name__ == "__main__":
    main() 