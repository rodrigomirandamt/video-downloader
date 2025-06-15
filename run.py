#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MediaSlayer - Main Launcher
Simple entry point that launches the GUI from src/
"""

import os
import sys
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

# Import and run the main GUI
from media_downloader_gui import main

if __name__ == "__main__":
    main() 