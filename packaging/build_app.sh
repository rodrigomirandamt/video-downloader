#!/bin/bash
# MediaSlayer macOS App Builder Script

# Determine repo root (one level up from this script)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.." || exit 1

echo "🚀 Building MediaSlayer macOS App"
echo "================================="

# 1. Ensure dependencies for build are installed in current env
pip3 install --upgrade pyinstaller pillow yt-dlp >/dev/null 2>&1

# 2. (Re)generate icon (does nothing if file already exists)
python3 packaging/create_icon.py

# 3. Clean previous build artifacts
rm -rf build dist

# 4. Build the app (non-interactive)
python3 -m PyInstaller --noconfirm --clean packaging/MediaSlayer.spec

# 5. Verify & output result
if [ -d "dist/MediaSlayer.app" ]; then
  echo "✅ Build successful! Bundle at dist/MediaSlayer.app"
else
  echo "❌ Build failed! Check PyInstaller output above."; exit 1
fi 