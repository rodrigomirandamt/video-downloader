#!/bin/bash
# MediaSlayer macOS App Builder Script

echo "🚀 Building MediaSlayer macOS App"
echo "================================="

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install pyinstaller pillow yt-dlp

# Create icon
echo "🎨 Creating app icon..."
python3 create_icon.py

# Update spec file with icon path
echo "📝 Updating spec file..."
if [ -f "icons/MediaSlayer.icns" ]; then
    sed -i '' "s/icon=None/icon='icons\/MediaSlayer.icns'/g" MediaSlayer.spec
else
    sed -i '' "s/icon=None/icon='icons\/icon_1024x1024.png'/g" MediaSlayer.spec
fi

# Clean previous build
echo "🧹 Cleaning previous build..."
rm -rf build dist

# Build the app
echo "🔨 Building app with PyInstaller..."
python3 -m PyInstaller --clean MediaSlayer.spec

# Check if build was successful
if [ -d "dist/MediaSlayer.app" ]; then
    echo "✅ Build successful!"
    echo "📱 App created at: dist/MediaSlayer.app"
    
    # Make executable
    chmod +x "dist/MediaSlayer.app/Contents/MacOS/MediaSlayer"
    
    # Create Applications symlink
    ln -sf /Applications dist/Applications 2>/dev/null || true
    
    echo ""
    echo "🎉 MediaSlayer.app is ready!"
    echo "📋 Next steps:"
    echo "1. Test: open dist/MediaSlayer.app"
    echo "2. Install: cp -r dist/MediaSlayer.app /Applications/"
    echo ""
else
    echo "❌ Build failed!"
    exit 1
fi 