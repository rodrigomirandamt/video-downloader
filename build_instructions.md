# Build MediaSlayer macOS App

Follow these steps to create a macOS app from the MediaSlayer video downloader:

## Prerequisites

1. Make sure you have Python 3 installed
2. Open Terminal (not PowerShell)

## Step 1: Fix conda pathlib conflict

```bash
conda remove pathlib --yes
```

## Step 2: Install dependencies

```bash
pip3 install pyinstaller pillow yt-dlp
```

## Step 3: Create the app icon

```bash
python3 create_icon.py
```

## Step 4: Update the spec file

```bash
# Update the spec file to use the created icon
sed -i '' "s/icon=None/icon='icons\/MediaSlayer.icns'/g" MediaSlayer.spec
```

## Step 5: Clean and build

```bash
# Clean previous builds
rm -rf build dist

# Build the app
python3 -m PyInstaller --clean MediaSlayer.spec
```

## Step 6: Finalize the app

```bash
# Make executable
chmod +x "dist/MediaSlayer.app/Contents/MacOS/MediaSlayer"

# Create Applications symlink for easy installation
ln -sf /Applications dist/Applications
```

## Step 7: Test and install

```bash
# Test the app
open dist/MediaSlayer.app

# Install to Applications folder
cp -r dist/MediaSlayer.app /Applications/
```

## Alternative: One-line build command

If you prefer, you can run this single command in Terminal (not PowerShell):

```bash
conda remove pathlib --yes && pip3 install pyinstaller pillow yt-dlp && python3 create_icon.py && sed -i '' "s/icon=None/icon='icons\/MediaSlayer.icns'/g" MediaSlayer.spec && rm -rf build dist && python3 -m PyInstaller --clean MediaSlayer.spec && chmod +x "dist/MediaSlayer.app/Contents/MacOS/MediaSlayer" && ln -sf /Applications dist/Applications && echo "✅ MediaSlayer.app created successfully!"
```

## Troubleshooting

- If you get pathlib errors, make sure to remove the conda pathlib package first
- If the app doesn't start, check the Console app for error messages
- The app will be created in the `dist/` folder
- Use Terminal (bash/zsh), not PowerShell for building 