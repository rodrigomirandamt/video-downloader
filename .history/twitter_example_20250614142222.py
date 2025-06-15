#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo simples de uso do Twitter Downloader
"""

from twitter_downloader import TwitterDownloader

def exemplo_basico():
    """Exemplo básico de download de um tweet"""
    
    # Criar instância do downloader
    downloader = TwitterDownloader()
    
    # URL de exemplo (substitua por uma URL real)
    tweet_url = "https://twitter.com/username/status/1234567890"
    
    print("🐦 Exemplo de uso do Twitter Downloader")
    print("=" * 40)
    
    # 1. Extrair informações do tweet
    print("\n1️⃣ Extraindo informações...")
    info = downloader.extract_tweet_info(tweet_url)
    if info:
        print(f"📝 Título: {info['title']}")
        print(f"👤 Autor: {info['uploader']}")
        print(f"📅 Data: {info['upload_date']}")
    
    # 2. Listar formatos disponíveis
    print("\n2️⃣ Formatos disponíveis:")
    downloader.list_formats(tweet_url)
    
    # 3. Fazer download
    print("\n3️⃣ Fazendo download...")
    success = downloader.download_tweet(tweet_url, quality='best')
    
    if success:
        print("✅ Download concluído com sucesso!")
        print(f"📂 Arquivos salvos em: {downloader.output_path}")
    else:
        print("❌ Falha no download")

def exemplo_avancado():
    """Exemplo com configurações avançadas"""
    
    # Criar downloader com pasta personalizada
    custom_path = "./meus_downloads_twitter"
    downloader = TwitterDownloader(output_path=custom_path)
    
    print("🔧 Exemplo avançado")
    print("=" * 40)
    
    # URLs de exemplo
    urls = [
        "https://twitter.com/user1/status/123",
        "https://twitter.com/user2/status/456",
        "https://x.com/user3/status/789"
    ]
    
    for url in urls:
        print(f"\n🔍 Processando: {url}")
        
        # Verificar se é URL válida
        if downloader.is_valid_twitter_url(url):
            print("✅ URL válida")
            
            # Extrair informações
            info = downloader.extract_tweet_info(url)
            if info:
                print(f"📝 Tweet: {info['title'][:50]}...")
                
                # Download em qualidade baixa para economizar espaço
                downloader.download_tweet(url, quality='low')
        else:
            print("❌ URL inválida")

def exemplo_usuario():
    """Exemplo de download de mídia de um usuário"""
    
    downloader = TwitterDownloader()
    
    print("👤 Download de mídia de usuário")
    print("=" * 40)
    
    # Nome do usuário (sem @)
    username = "exemplo_usuario"
    
    print(f"🔍 Buscando mídia recente de @{username}...")
    
    # Baixar últimos 5 posts com mídia
    success = downloader.download_user_media(username, limit=5)
    
    if success:
        print("✅ Download de mídia do usuário concluído!")
    else:
        print("❌ Erro no download da mídia do usuário")

if __name__ == "__main__":
    print("🐦 Exemplos de uso do Twitter Downloader")
    print("=" * 50)
    
    print("\n📋 Escolha um exemplo:")
    print("1. Exemplo básico")
    print("2. Exemplo avançado")
    print("3. Download de mídia de usuário")
    print("0. Sair")
    
    choice = input("\n🔢 Sua escolha: ").strip()
    
    if choice == "1":
        exemplo_basico()
    elif choice == "2":
        exemplo_avancado()
    elif choice == "3":
        exemplo_usuario()
    elif choice == "0":
        print("👋 Até logo!")
    else:
        print("❌ Opção inválida")
        
    print("\n" + "=" * 50)
    print("💡 Dica: Para usar URLs reais, edite este arquivo")
    print("   e substitua as URLs de exemplo por URLs válidas do Twitter/X") 