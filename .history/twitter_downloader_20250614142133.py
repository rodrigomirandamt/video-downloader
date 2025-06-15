#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitter/X Content Downloader
Download videos, images, and GIFs from Twitter/X posts
"""

import yt_dlp
import os
import re
import requests
from pathlib import Path
from datetime import datetime
import json

class TwitterDownloader:
    def __init__(self, output_path=None):
        """
        Initialize Twitter Downloader
        
        Args:
            output_path (str): Directory to save downloads (defaults to ./twitter_downloads)
        """
        if output_path is None:
            self.output_path = os.path.join(os.getcwd(), "twitter_downloads")
        else:
            self.output_path = output_path
            
        # Create output directory
        os.makedirs(self.output_path, exist_ok=True)
        
        # Configure yt-dlp options for Twitter
        self.ydl_opts = {
            'outtmpl': os.path.join(self.output_path, '%(uploader)s_%(id)s_%(title)s.%(ext)s'),
            'format': 'best',
            'writeinfojson': True,  # Save metadata
            'writethumbnail': True,  # Save thumbnail
        }
    
    def is_valid_twitter_url(self, url):
        """
        Check if URL is a valid Twitter/X URL
        
        Args:
            url (str): URL to validate
            
        Returns:
            bool: True if valid Twitter URL
        """
        twitter_patterns = [
            r'https?://(?:www\.)?twitter\.com/\w+/status/\d+',
            r'https?://(?:www\.)?x\.com/\w+/status/\d+',
            r'https?://t\.co/\w+',
        ]
        
        return any(re.match(pattern, url) for pattern in twitter_patterns)
    
    def extract_tweet_info(self, url):
        """
        Extract tweet information without downloading
        
        Args:
            url (str): Twitter URL
            
        Returns:
            dict: Tweet information
        """
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'N/A'),
                    'uploader': info.get('uploader', 'N/A'),
                    'upload_date': info.get('upload_date', 'N/A'),
                    'description': info.get('description', 'N/A'),
                    'duration': info.get('duration', 'N/A'),
                    'view_count': info.get('view_count', 'N/A'),
                    'like_count': info.get('like_count', 'N/A'),
                    'repost_count': info.get('repost_count', 'N/A'),
                    'formats': len(info.get('formats', [])) if info.get('formats') else 0
                }
        except Exception as e:
            print(f"Erro ao extrair informações: {str(e)}")
            return None
    
    def download_tweet(self, url, quality='best', include_replies=False):
        """
        Download content from a Twitter post
        
        Args:
            url (str): Twitter URL
            quality (str): Video quality preference
            include_replies (bool): Include replies in thread
            
        Returns:
            bool: Success status
        """
        if not self.is_valid_twitter_url(url):
            print("❌ URL inválida. Use uma URL do Twitter/X válida.")
            return False
        
        try:
            # Configure options based on parameters
            opts = self.ydl_opts.copy()
            
            if quality == 'audio':
                opts['format'] = 'bestaudio/best'
            elif quality == 'low':
                opts['format'] = 'worst'
            else:
                opts['format'] = 'best'
            
            print(f"🔍 Analisando: {url}")
            
            # Extract info first
            info = self.extract_tweet_info(url)
            if info:
                print(f"📝 Tweet: {info['title']}")
                print(f"👤 Autor: {info['uploader']}")
                print(f"📅 Data: {info['upload_date']}")
                if info['duration'] != 'N/A':
                    print(f"⏱️ Duração: {info['duration']} segundos")
                print()
            
            # Download
            with yt_dlp.YoutubeDL(opts) as ydl:
                print("⬇️ Iniciando download...")
                ydl.download([url])
                print("✅ Download concluído!")
                return True
                
        except Exception as e:
            print(f"❌ Erro no download: {str(e)}")
            return False
    
    def download_user_media(self, username, limit=10):
        """
        Download recent media from a Twitter user
        
        Args:
            username (str): Twitter username (without @)
            limit (int): Number of recent posts to check
            
        Returns:
            list: List of downloaded files
        """
        try:
            user_url = f"https://twitter.com/{username}"
            
            opts = self.ydl_opts.copy()
            opts['playlistend'] = limit
            
            print(f"🔍 Buscando mídia recente de @{username}...")
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([user_url])
                
            print(f"✅ Download de mídia de @{username} concluído!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao baixar mídia do usuário: {str(e)}")
            return False
    
    def download_thread(self, url):
        """
        Download entire Twitter thread
        
        Args:
            url (str): URL of the first tweet in thread
            
        Returns:
            bool: Success status
        """
        try:
            opts = self.ydl_opts.copy()
            opts['writesubtitles'] = True
            
            print(f"🧵 Baixando thread completa...")
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
                
            print("✅ Thread baixada com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao baixar thread: {str(e)}")
            return False
    
    def list_formats(self, url):
        """
        List available formats for a Twitter post
        
        Args:
            url (str): Twitter URL
        """
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if 'formats' in info:
                    print("📋 Formatos disponíveis:")
                    print("-" * 50)
                    for fmt in info['formats']:
                        format_id = fmt.get('format_id', 'N/A')
                        ext = fmt.get('ext', 'N/A')
                        quality = fmt.get('quality', 'N/A')
                        filesize = fmt.get('filesize', 'N/A')
                        
                        if filesize != 'N/A' and filesize:
                            filesize_mb = round(filesize / (1024 * 1024), 2)
                            print(f"ID: {format_id} | Ext: {ext} | Qualidade: {quality} | Tamanho: {filesize_mb}MB")
                        else:
                            print(f"ID: {format_id} | Ext: {ext} | Qualidade: {quality}")
                else:
                    print("❌ Nenhum formato encontrado")
                    
        except Exception as e:
            print(f"❌ Erro ao listar formatos: {str(e)}")
    
    def open_download_folder(self):
        """Open the download folder in file explorer"""
        if os.path.exists(self.output_path):
            os.startfile(self.output_path)
        else:
            print(f"❌ Pasta não encontrada: {self.output_path}")


def main():
    """Main function with interactive menu"""
    print("🐦 Twitter/X Content Downloader")
    print("=" * 40)
    
    downloader = TwitterDownloader()
    
    while True:
        print("\n📋 Opções:")
        print("1. 📥 Baixar tweet específico")
        print("2. 🧵 Baixar thread completa")
        print("3. 👤 Baixar mídia de usuário")
        print("4. 📋 Listar formatos disponíveis")
        print("5. ℹ️  Extrair informações do tweet")
        print("6. 📂 Abrir pasta de downloads")
        print("7. ⚙️  Alterar pasta de destino")
        print("0. 🚪 Sair")
        
        choice = input("\n🔢 Escolha uma opção: ").strip()
        
        if choice == "1":
            url = input("🔗 Cole a URL do tweet: ").strip()
            if url:
                print("\n📊 Qualidade:")
                print("1. Melhor qualidade (padrão)")
                print("2. Menor qualidade")
                print("3. Apenas áudio")
                
                quality_choice = input("Escolha (1-3): ").strip()
                quality_map = {"1": "best", "2": "low", "3": "audio"}
                quality = quality_map.get(quality_choice, "best")
                
                downloader.download_tweet(url, quality)
            else:
                print("❌ URL não fornecida")
        
        elif choice == "2":
            url = input("🔗 Cole a URL do primeiro tweet da thread: ").strip()
            if url:
                downloader.download_thread(url)
            else:
                print("❌ URL não fornecida")
        
        elif choice == "3":
            username = input("👤 Digite o nome de usuário (sem @): ").strip()
            if username:
                try:
                    limit = int(input("📊 Quantos posts recentes verificar? (padrão: 10): ") or "10")
                    downloader.download_user_media(username, limit)
                except ValueError:
                    print("❌ Número inválido")
            else:
                print("❌ Nome de usuário não fornecido")
        
        elif choice == "4":
            url = input("🔗 Cole a URL do tweet: ").strip()
            if url:
                downloader.list_formats(url)
            else:
                print("❌ URL não fornecida")
        
        elif choice == "5":
            url = input("🔗 Cole a URL do tweet: ").strip()
            if url:
                info = downloader.extract_tweet_info(url)
                if info:
                    print("\n📊 Informações do Tweet:")
                    print("-" * 30)
                    for key, value in info.items():
                        print(f"{key.replace('_', ' ').title()}: {value}")
            else:
                print("❌ URL não fornecida")
        
        elif choice == "6":
            downloader.open_download_folder()
        
        elif choice == "7":
            new_path = input(f"📂 Nova pasta (atual: {downloader.output_path}): ").strip()
            if new_path:
                downloader.output_path = new_path
                downloader.ydl_opts['outtmpl'] = os.path.join(new_path, '%(uploader)s_%(id)s_%(title)s.%(ext)s')
                os.makedirs(new_path, exist_ok=True)
                print(f"✅ Pasta alterada para: {new_path}")
        
        elif choice == "0":
            print("👋 Até logo!")
            break
        
        else:
            print("❌ Opção inválida")


if __name__ == "__main__":
    # Example usage
    print("🐦 Twitter Content Downloader")
    print("=" * 40)
    
    # Quick download example (uncomment to use)
    # downloader = TwitterDownloader()
    # tweet_url = "https://twitter.com/username/status/1234567890"
    # downloader.download_tweet(tweet_url)
    
    # Run interactive menu
    main()