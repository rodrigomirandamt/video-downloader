#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo de uso do baixador de vídeos do Twitter
"""

from baixar_video_twitter import baixar_video_twitter

# Exemplo de uso direto
def exemplo_rapido():
    """Exemplo de download rápido"""
    
    print("🐦 Exemplo de Download de Vídeo do Twitter")
    print("=" * 45)
    
    # SUBSTITUA esta URL por uma URL real de um tweet com vídeo
    url_exemplo = "https://twitter.com/usuario/status/1234567890"
    
    print("💡 Para usar este exemplo:")
    print("1. Encontre um tweet com vídeo no Twitter/X")
    print("2. Copie a URL do tweet")
    print("3. Substitua a URL abaixo pela URL real")
    print("4. Execute este script")
    print()
    
    print(f"🔗 URL de exemplo: {url_exemplo}")
    print()
    
    # Descomente a linha abaixo e coloque uma URL real para testar
    # baixar_video_twitter(url_exemplo)
    
    print("⚠️  Para testar, descomente a linha no código e use uma URL real!")

if __name__ == "__main__":
    exemplo_rapido() 