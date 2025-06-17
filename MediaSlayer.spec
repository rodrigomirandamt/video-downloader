# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path

# Get the current directory
current_dir = Path.cwd()

# Define the main script
main_script = 'MediaSlayer.py'

# Data files to include
added_files = [
    ('src', 'src'),
    ('downloads', 'downloads'),
    ('README.md', '.'),
    ('requirements.txt', '.'),
]

# Hidden imports (dependencies that PyInstaller might miss)
hidden_imports = [
    'yt_dlp',
    'yt_dlp.extractor',
    'yt_dlp.extractor.youtube',
    'yt_dlp.extractor.twitter',
    'yt_dlp.postprocessor',
    'tkinter',
    'tkinter.ttk',
    'tkinter.messagebox',
    'tkinter.scrolledtext',
    'tkinter.filedialog',
    'threading',
    'os',
    'sys',
    'pathlib',
    're',
    'time',
    'signal',
]

# Analysis configuration
a = Analysis(
    [main_script],
    pathex=[str(current_dir)],
    binaries=[],
    datas=added_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Process the analysis
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Create the executable
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MediaSlayer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# Create the macOS app bundle
app = BUNDLE(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='MediaSlayer.app',
    icon='icons/MediaSlayer.icns''icons/MediaSlayer.icns',  # We'll add an icon later if needed
    bundle_identifier='com.mediaslayer.app',
    version='1.0.0',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
        'CFBundleDocumentTypes': [],
        'CFBundleName': 'MediaSlayer',
        'CFBundleDisplayName': 'MediaSlayer',
        'CFBundleGetInfoString': 'MediaSlayer - Video Downloader',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': 'Copyright © 2024 MediaSlayer',
        'LSMinimumSystemVersion': '10.9.0',
        'NSHighResolutionCapable': True,
        'NSRequiresAquaSystemAppearance': False,
        'LSApplicationCategoryType': 'public.app-category.utilities',
        'NSAppTransportSecurity': {
            'NSAllowsArbitraryLoads': True
        },
        'NSMicrophoneUsageDescription': 'MediaSlayer may need microphone access for certain video processing features.',
        'NSCameraUsageDescription': 'MediaSlayer may need camera access for certain video processing features.',
        'NSNetworkUsageDescription': 'MediaSlayer needs network access to download videos from the internet.',
    },
) 