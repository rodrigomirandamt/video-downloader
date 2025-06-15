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
except ImportError as exc:
    print("❌ Required modules not found (winshell, pywin32). Run: pip install winshell pywin32")
    sys.exit(1)


SCRIPT_DIR = Path(__file__).resolve().parent
DESKTOP = Path(winshell.desktop())

# Prefer the .pyw launcher so the GUI opens without a console window
launcher_path = SCRIPT_DIR / "mediaslayer_launcher.pyw"
if not launcher_path.exists():
    # Fall back to the main .py file executed via pythonw
    pythonw = Path(sys.executable).with_name("pythonw.exe")
    if not pythonw.exists():
        pythonw = Path(sys.executable)  # last resort; may open a console
    launcher_path = f"{pythonw} \"{SCRIPT_DIR / 'media_downloader_gui.py'}\""
    use_args = False
else:
    use_args = False  # shortcut TargetPath will be launcher directly

shortcut_path = DESKTOP / "MediaSlayer.lnk"

def create_shortcut():
    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(str(shortcut_path))

    if isinstance(launcher_path, Path):
        shortcut.Targetpath = str(launcher_path)
    else:
        # launcher_path already contains pythonw & script, split appropriately
        first, *rest = launcher_path.split(" ")
        shortcut.Targetpath = first
        shortcut.Arguments = " ".join(rest)

    shortcut.WorkingDirectory = str(SCRIPT_DIR)

    icon_path = SCRIPT_DIR / "mediaslayer.ico"
    if icon_path.exists():
        shortcut.IconLocation = str(icon_path)

    shortcut.Description = "MediaSlayer – Video Downloader"
    shortcut.save()
    print(f"✅ Shortcut created at: {shortcut_path}")


def main():
    create_shortcut()


if __name__ == "__main__":
    main() 