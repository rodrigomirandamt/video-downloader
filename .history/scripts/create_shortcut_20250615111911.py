#!/usr/bin/env python3
"""
create_shortcut.py
------------------
Utility script to create a working Windows shortcut ( .lnk ) on the Desktop
that launches MediaSlayer in silent (no-terminal) mode.

Run with:
    python create_shortcut.py

Requirements: winshell, pywin32 (already listed in requirements.txt).
"""
import os
import sys
from pathlib import Path

try:
    import winshell
    from win32com.client import Dispatch
    from PIL import Image  # For PNG → ICO conversion
except ImportError as exc:
    print("❌ Required modules not found (winshell, pywin32). Run: pip install winshell pywin32")
    sys.exit(1)


SCRIPT_DIR = Path(__file__).resolve().parent
DESKTOP = Path(winshell.desktop())

# Choose launcher script (prefer .pyw) and ensure we always call it through pythonw.exe
pythonw_exe = Path(sys.executable).with_name("pythonw.exe")
if not pythonw_exe.exists():
    # In rare cases pythonw.exe may not exist (store install); fall back to python.exe
    pythonw_exe = Path(sys.executable)

# Select script to launch
py_script = None
launcher_pyw = SCRIPT_DIR / "mediaslayer_launcher.pyw"
if launcher_pyw.exists():
    py_script = launcher_pyw
else:
    py_script = SCRIPT_DIR / "media_downloader_gui.py"

# These two values will populate the shortcut
TARGET_PATH = str(pythonw_exe)
TARGET_ARGS = f'"{py_script}"'

shortcut_path = DESKTOP / "MediaSlayer.lnk"

def create_shortcut():
    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(str(shortcut_path))

    shortcut.Targetpath = TARGET_PATH
    shortcut.Arguments = TARGET_ARGS

    shortcut.WorkingDirectory = str(SCRIPT_DIR)

    # --- Icon handling ---
    png_icon = SCRIPT_DIR / "icone.png"  # User-provided PNG
    ico_icon = SCRIPT_DIR / "icone.ico"

    if png_icon.exists():
        # Convert PNG to ICO on first run (requires Pillow)
        if not ico_icon.exists() and Image is not None:
            try:
                img = Image.open(png_icon)
                # Save multiple sizes for best scaling
                img.save(ico_icon, sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
            except Exception as exc:
                print(f"⚠️  Could not convert PNG to ICO: {exc}")

        if ico_icon.exists():
            shortcut.IconLocation = str(ico_icon)
    else:
        # Fallback to existing mediaslayer.ico
        default_icon = SCRIPT_DIR / "mediaslayer.ico"
        if default_icon.exists():
            shortcut.IconLocation = str(default_icon)

    shortcut.Description = "MediaSlayer – Video Downloader"
    shortcut.save()
    print(f"✅ Shortcut created at: {shortcut_path}")


def main():
    create_shortcut()


if __name__ == "__main__":
    main() 