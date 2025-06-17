#!/usr/bin/env python3
"""
Build script for MediaSlayer macOS App
This script creates a complete macOS application bundle
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parent.parent
SPEC_PATH = ROOT / 'packaging' / 'MediaSlayer.spec'
ICON_SCRIPT_PATH = ROOT / 'packaging' / 'create_icon.py'

sys.path.insert(0, str(Path(__file__).parent))

def check_dependencies():
    """Check if required dependencies are available"""
    print("🔍 Checking dependencies...")
    
    # Check PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller {PyInstaller.__version__} found")
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Check Pillow for icon creation
    try:
        import PIL
        print(f"✅ Pillow found")
    except ImportError:
        print("❌ Pillow not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "Pillow"])
    
    # Check yt-dlp
    try:
        import yt_dlp
        print(f"✅ yt-dlp found")
    except ImportError:
        print("❌ yt-dlp not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"])

def create_icon():
    """Create the app icon"""
    print("\n🎨 Creating app icon...")
    
    try:
        spec = importlib.util.spec_from_file_location('create_icon', ICON_SCRIPT_PATH)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        create_app_icon = module.create_app_icon
        
        icon_path = create_app_icon()
        if icon_path and os.path.exists(icon_path):
            print(f"✅ Icon created: {icon_path}")
            return icon_path
        else:
            print("⚠️ Could not create .icns file, using PNG fallback")
            return "icons/icon_1024x1024.png"
    except Exception as e:
        print(f"⚠️ Icon creation failed: {e}")
        return None

def update_spec_file(icon_path):
    """Update the spec file with the icon path"""
    print(f"\n📝 Updating spec file with icon: {icon_path}")
    
    spec_file = str(SPEC_PATH)
    
    if not os.path.exists(spec_file):
        print(f"❌ Spec file {spec_file} not found!")
        return False
    
    # Read the spec file
    with open(spec_file, 'r') as f:
        content = f.read()
    
    # Update the icon path
    if icon_path:
        content = content.replace("icon=None", f"icon='{icon_path}'")
    
    # Write back the updated content
    with open(spec_file, 'w') as f:
        f.write(content)
    
    print("✅ Spec file updated")
    return True

def clean_build():
    """Clean previous build artifacts"""
    print("\n🧹 Cleaning previous build...")
    
    dirs_to_clean = ['build', 'dist']
    files_to_clean = ['MediaSlayer.spec~']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ Removed {dir_name}/")
    
    for file_name in files_to_clean:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"✅ Removed {file_name}")

def build_app():
    """Build the macOS app using PyInstaller"""
    print("\n🔨 Building macOS app...")
    
    try:
        # Run PyInstaller with the spec file
        cmd = [sys.executable, "-m", "PyInstaller", "--clean", "--noconfirm", str(SPEC_PATH)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ App built successfully!")
            return True
        else:
            print(f"❌ Build failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False

def post_build_setup():
    """Post-build setup and verification"""
    print("\n🔧 Post-build setup...")
    
    app_path = "dist/MediaSlayer.app"
    
    if not os.path.exists(app_path):
        print(f"❌ App not found at {app_path}")
        return False
    
    # Create a symlink to Applications folder (optional)
    try:
        applications_link = "dist/Applications"
        if not os.path.exists(applications_link):
            os.symlink("/Applications", applications_link)
            print("✅ Created Applications symlink")
    except Exception as e:
        print(f"⚠️ Could not create Applications symlink: {e}")
    
    # Make the app executable
    try:
        executable_path = f"{app_path}/Contents/MacOS/MediaSlayer"
        if os.path.exists(executable_path):
            os.chmod(executable_path, 0o755)
            print("✅ Made app executable")
    except Exception as e:
        print(f"⚠️ Could not set executable permissions: {e}")
    
    return True

def create_dmg():
    """Create a DMG file for distribution"""
    print("\n📦 Creating DMG file...")
    
    try:
        dmg_name = "MediaSlayer-1.0.0.dmg"
        
        # Remove existing DMG
        if os.path.exists(dmg_name):
            os.remove(dmg_name)
        
        # Create DMG using hdiutil
        cmd = [
            "hdiutil", "create", 
            "-volname", "MediaSlayer",
            "-srcfolder", "dist",
            "-ov", "-format", "UDZO",
            dmg_name
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ DMG created: {dmg_name}")
            return True
        else:
            print(f"⚠️ DMG creation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"⚠️ DMG creation error: {e}")
        return False

def main():
    """Main build process"""
    print("🚀 MediaSlayer macOS App Builder")
    print("=" * 40)
    
    # Check dependencies
    check_dependencies()
    
    # Create icon
    icon_path = create_icon()
    
    # Update spec file with icon
    if icon_path:
        update_spec_file(icon_path)
    
    # Clean previous build
    clean_build()
    
    # Build the app
    if build_app():
        # Post-build setup
        if post_build_setup():
            print("\n🎉 Build completed successfully!")
            print(f"📱 App location: dist/MediaSlayer.app")
            
            # Create DMG
            create_dmg()
            
            print("\n📋 Next steps:")
            print("1. Test the app: open dist/MediaSlayer.app")
            print("2. Copy to Applications: cp -r dist/MediaSlayer.app /Applications/")
            print("3. Or install from DMG if created")
            
            return True
    
    print("\n❌ Build failed!")
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 