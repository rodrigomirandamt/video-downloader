# MediaSlayer - Video Downloader

A modern, user-friendly video downloader with support for YouTube, X (Twitter), and other platforms.

## Project Structure

```
youtube/
├── src/                          # Main source code
│   ├── media_downloader_gui.py   # Main GUI application
│   └── mediaslayer_launcher.pyw  # Silent launcher (no console)
├── assets/                       # Icons and images
│   ├── icone.png                 # Main icon (PNG)
│   ├── icone.ico                 # Windows icon (ICO)
│   ├── mediaslayer.ico           # Legacy icon
│   └── interface-imagem.png      # Interface screenshot
├── scripts/                      # Utility scripts
│   └── create_shortcut.py        # Creates Windows desktop shortcut
├── legacy/                       # Old/deprecated files
│   ├── configurar_execucao_silenciosa.py
│   ├── executar_mediaslayer.bat
│   └── executar_mediaslayer_silencioso.bat
├── downloads/                    # Default download location
├── run.py                        # Main launcher script
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python run.py
   ```

3. **Create desktop shortcut (Windows):**
   ```bash
   python scripts/create_shortcut.py
   ```

## Windows Shortcut notes

The `scripts/create_shortcut.py` utility automatically:

1. Locates `pythonw.exe` (falls back to `python.exe` if not found).
2. Points the shortcut to `run.py` so the GUI opens exactly like `python run.py`.
3. Uses `assets/icone.png` → `icone.ico` as the icon (it will convert on first run – requires Pillow).
4. Places `MediaSlayer.lnk` on your desktop.

If you change the icon, just replace `assets/icone.png` and rerun the shortcut script.

> **Tip**  –  If the shortcut fails to launch, right-click → Properties and confirm:
> * Target:  `"…pythonw.exe" "…\run.py"`
> * Start in: project root (same folder that contains `run.py`).

## Dependency notes

`yt-dlp`, `tkinter` and `Pillow` are platform-independent.
`pywin32` and `winshell` are only used for Windows-specific features (shortcut creation). On macOS/Linux you can omit them or safely ignore errors related to shortcut scripts.

## Features

- Clean, modern interface optimized for small screens
- Support for YouTube and X (Twitter) downloads
- Multiple format options (MP4, MP3, WebM, WAV)
- Quality selection (1080p, 720p, 480p, 360p)
- Real-time download progress
- Silent execution (no console window)
- Automatic platform detection

## Usage

1. Enter a video URL in the input field
2. Select your preferred format and quality
3. Choose download location (optional)
4. Click "Execute Download Quest" to start

## Supported Platforms

- YouTube (youtube.com, youtu.be)
- X/Twitter (x.com, twitter.com)
- Many other platforms supported by yt-dlp

## Requirements

- Python 3.7+
- Windows (for desktop shortcut creation)
- Internet connection

## Dependencies

- `yt-dlp` - Video downloading engine
- `tkinter` - GUI framework (included with Python)
- `pywin32` - Windows integration
- `winshell` - Windows shell operations
- `Pillow` - Image processing for icons

## License

This project uses yt-dlp for video downloading. Please respect the terms of service of the platforms you download from. 