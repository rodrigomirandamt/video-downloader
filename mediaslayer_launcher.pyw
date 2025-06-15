#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launcher silencioso para o MediaSlayer
Arquivo .pyw é executado automaticamente sem terminal
"""

import os
import sys

# Adicionar o diretório atual ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Importar e executar o MediaSlayer
from media_downloader_gui import main

if __name__ == "__main__":
    main() 