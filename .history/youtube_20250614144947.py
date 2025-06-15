# First, install yt-dlp (run this once)
# !pip install yt-dlp

import yt_dlp
import os

def download_youtube_video(url, output_path=None):
    """
    Download a YouTube video using yt-dlp
    
    Args:
        url (str): YouTube video URL
        output_path (str): Directory to save the video (defaults to ./videos)
    """
    # Get the directory where this notebook is located and create videos folder
    if output_path is None:
        current_dir = os.getcwd()  # Current working directory
        output_path = os.path.join(current_dir, "videos")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    print(f"Downloading to: {output_path}")
    
    # Configure yt-dlp options
    ydl_opts = {
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),  # Output filename template
        'format': 'best[height<=720]',  # Download best quality up to 720p
        'quiet': True,  # Silenciar saídas desnecessárias
        'no_warnings': True,  # Remover avisos
    }
    
    try:
        with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
            # Get video info first
            info = ydl.extract_info(url, download=False)
            print(f"Title: {info.get('title', 'N/A')}")
            print(f"Duration: {info.get('duration', 'N/A')} seconds")
            print(f"Uploader: {info.get('uploader', 'N/A')}")
            
        # Download the video with full options
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Starting download...")
            ydl.download([url])
            print("Download completed!")
            
    except Exception as e:
        print(f"Error downloading video: {str(e)}")

# Example usage:
# Replace with any YouTube video URL
youtube_url = "https://www.youtube.com/shorts/9yuGcsOoTsw"

# Uncomment the line below to download
download_youtube_video(youtube_url)
