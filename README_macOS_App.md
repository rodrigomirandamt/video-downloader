# MediaSlayer macOS App

<img src="icons/icon_256x256.png" alt="MediaSlayer Icon" width="128" height="128">

A native macOS application for downloading videos from YouTube and other platforms with a beautiful, modern interface.

## ✨ Features

- **Native macOS App**: Clean, native macOS application bundle (.app)
- **Beautiful UI**: Modern, gradient-based interface inspired by gaming aesthetics
- **Multi-Platform Support**: Download from YouTube, Twitter/X, and more
- **Format Options**: MP4, MP3, WebM, WAV with quality selection
- **Smart Format Fallbacks**: Automatically finds the best available format
- **Progress Tracking**: Real-time download progress with detailed logging
- **Error Recovery**: Intelligent error handling with helpful suggestions

## 🚀 Installation

### Option 1: Build from Source

1. Clone or download this repository
2. Open Terminal (not PowerShell)
3. Run the build command:

```bash
conda remove pathlib --yes && pip3 install pyinstaller pillow yt-dlp && python3 create_icon.py && sed -i '' "s/icon=None/icon='icons\/MediaSlayer.icns'/g" MediaSlayer.spec && rm -rf build dist && python3 -m PyInstaller --clean MediaSlayer.spec && chmod +x "dist/MediaSlayer.app/Contents/MacOS/MediaSlayer" && ln -sf /Applications dist/Applications && echo "✅ MediaSlayer.app created successfully!"
```

4. Install the app:
```bash
cp -r dist/MediaSlayer.app /Applications/
```

### Option 2: Pre-built App (if available)

1. Download the `.dmg` file
2. Open the DMG and drag MediaSlayer to Applications
3. Launch from Applications or Spotlight

## 🎮 Usage

1. **Launch the App**: Open MediaSlayer from Applications or Spotlight
2. **Enter URL**: Paste a YouTube, Twitter/X, or other supported URL
3. **Choose Format**: Select your preferred format (MP4, MP3, WebM, WAV)
4. **Select Quality**: Pick quality level (1080p, 720p, 480p, 360p)
5. **Set Download Location**: Choose where to save your files
6. **Execute Quest**: Click the download button and watch the magic happen!

## 🔧 Technical Details

### Built With
- **Python 3.11+**: Core application logic
- **Tkinter**: Native GUI framework
- **yt-dlp**: Powerful media extraction engine
- **PyInstaller**: macOS app bundling
- **Pillow**: Icon generation and image processing

### App Structure
```
MediaSlayer.app/
├── Contents/
│   ├── Info.plist          # App metadata
│   ├── MacOS/
│   │   └── MediaSlayer     # Main executable
│   ├── Resources/          # App resources
│   └── Frameworks/         # Python runtime
```

### Supported Platforms
- YouTube (youtube.com, youtu.be)
- Twitter/X (twitter.com, x.com)
- Many other platforms supported by yt-dlp

### Format Options
- **Video**: MP4, WebM with quality selection
- **Audio**: MP3, WAV for audio-only downloads
- **Smart Fallbacks**: Automatically tries alternative formats if preferred isn't available

## 🛠️ Development

### Project Structure
```
video-downloader/
├── src/
│   └── media_downloader_gui.py    # Main GUI application
├── MediaSlayer.py                 # macOS app launcher
├── MediaSlayer.spec              # PyInstaller configuration
├── create_icon.py                # Icon generation script
├── build_app.sh                  # Build script
├── build_instructions.md         # Build instructions
└── icons/                        # Generated app icons
```

### Key Improvements Made
1. **Enhanced Format Selection**: Robust fallback system for format compatibility
2. **Smart Error Handling**: Detects format issues and suggests alternatives
3. **Native macOS Integration**: Proper app bundle with metadata
4. **Professional Icon**: Custom-generated app icon with play/download symbols
5. **Improved UI**: Compact, modern interface with proper spacing

### Building from Source
See `build_instructions.md` for detailed build instructions.

## 🔒 Security & Privacy

- **No Data Collection**: MediaSlayer doesn't collect or transmit user data
- **Local Processing**: All downloads are processed locally on your Mac
- **Open Source**: Full source code available for inspection
- **Network Access**: Required only for downloading media content

## 🐛 Troubleshooting

### Common Issues

**App won't start**
- Check Console.app for error messages
- Ensure all dependencies are properly bundled
- Try rebuilding the app

**Download fails**
- Check internet connection
- Try different quality settings
- Some videos may have restricted access

**Format not available error**
- App automatically tries fallback formats
- Try selecting a different quality level
- MP3 format works for most content

### Getting Help
1. Check the in-app error messages and suggestions
2. Look at the download logs in the app
3. Try different format/quality combinations
4. Ensure the URL is supported

## 📜 License

This project is open source. Please respect the terms of service of the platforms you download from.

## 🙏 Acknowledgments

- **yt-dlp**: The powerful engine that makes downloads possible
- **Python/Tkinter**: For the cross-platform GUI framework
- **PyInstaller**: For creating native macOS app bundles

---

**MediaSlayer** - Your quest for media download excellence begins here! ⚔️ 