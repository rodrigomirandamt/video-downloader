#!/usr/bin/env python3
"""
Create a simple app icon for MediaSlayer
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_app_icon():
    """Create a simple app icon"""
    # Icon sizes for macOS
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    
    # Create directory for icons
    icon_dir = "icons"
    os.makedirs(icon_dir, exist_ok=True)
    
    for size in sizes:
        # Create a new image with the specified size
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Create a gradient background
        for i in range(size):
            ratio = i / size
            # Dark blue to red gradient
            r = int(15 + (220 - 15) * ratio)  # 15 to 220
            g = int(23 + (38 - 23) * ratio)   # 23 to 38
            b = int(42 + (66 - 42) * ratio)   # 42 to 66
            
            draw.rectangle([0, i, size, i+1], fill=(r, g, b, 255))
        
        # Add a border
        border_width = max(1, size // 64)
        draw.rectangle([0, 0, size-1, size-1], outline=(255, 255, 255, 128), width=border_width)
        
        # Add a play button symbol
        play_size = size // 3
        play_x = size // 2 - play_size // 3
        play_y = size // 2 - play_size // 2
        
        # Draw play triangle
        points = [
            (play_x, play_y),
            (play_x, play_y + play_size),
            (play_x + int(play_size * 0.866), play_y + play_size // 2)
        ]
        draw.polygon(points, fill=(255, 255, 255, 200))
        
        # Add download arrow
        arrow_size = size // 4
        arrow_x = size // 2 + size // 6
        arrow_y = size // 2 + size // 6
        
        # Draw arrow shaft
        shaft_width = max(1, size // 32)
        draw.rectangle([
            arrow_x - shaft_width // 2,
            arrow_y - arrow_size // 2,
            arrow_x + shaft_width // 2,
            arrow_y + arrow_size // 3
        ], fill=(255, 255, 255, 180))
        
        # Draw arrow head
        head_points = [
            (arrow_x - arrow_size // 4, arrow_y + arrow_size // 4),
            (arrow_x + arrow_size // 4, arrow_y + arrow_size // 4),
            (arrow_x, arrow_y + arrow_size // 2)
        ]
        draw.polygon(head_points, fill=(255, 255, 255, 180))
        
        # Save the icon
        icon_path = os.path.join(icon_dir, f"icon_{size}x{size}.png")
        img.save(icon_path, 'PNG')
        print(f"Created icon: {icon_path}")
    
    # Create .icns file for macOS
    try:
        # Use the largest size as the main icon
        main_icon = Image.open(os.path.join(icon_dir, "icon_1024x1024.png"))
        icns_path = os.path.join(icon_dir, "MediaSlayer.icns")
        main_icon.save(icns_path, 'ICNS')
        print(f"Created macOS icon: {icns_path}")
        return icns_path
    except Exception as e:
        print(f"Could not create .icns file: {e}")
        return None

if __name__ == "__main__":
    # Ensure Homebrew binaries (like ffmpeg) are on PATH when the app is launched from Finder
    HOMEBREW_PREFIX = "/opt/homebrew/bin"
    if HOMEBREW_PREFIX not in os.environ.get("PATH", ""):
        os.environ["PATH"] = os.environ.get("PATH", "") + os.pathsep + HOMEBREW_PREFIX
    create_app_icon() 