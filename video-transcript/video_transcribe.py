#!/usr/bin/env python3
"""
Video Transcription Tool using yt-dlp

This script allows you to download transcripts/subtitles from YouTube and other 
video sources supported by yt-dlp.

Features:
- Download auto-generated or manually created subtitles
- Support for multiple subtitle languages
- Convert subtitles to different formats (srt, vtt, txt)
- Option to remove timestamps for clean text output
"""

import os
import sys
import argparse
import subprocess
import json
import re
from pathlib import Path


def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, text=True)
    except FileNotFoundError:
        print("Error: yt-dlp is not installed. Please install it first.")
        print("Installation: pip install yt-dlp")
        return False
    
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
    except FileNotFoundError:
        print("Warning: ffmpeg is not installed. Some features might not work properly.")
        print("It's recommended to install ffmpeg for better subtitle processing.")
    
    return True


def list_available_subtitles(url):
    """List all available subtitles for a video."""
    command = ["yt-dlp", "--list-subs", url]
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error listing subtitles: {result.stderr}")
        return None
    
    print("\nAvailable subtitles:")
    print(result.stdout)
    
    # Extract language codes
    languages = []
    lines = result.stdout.split('\n')
    for line in lines:
        if re.search(r'^\w+(-\w+)?(\s+\w+)?', line):
            parts = line.split()
            if parts and len(parts) >= 1:
                languages.append(parts[0])
    
    return languages


def download_transcript(url, output_dir=None, language="en", format="srt", 
                        auto_subs=True, manual_subs=True, skip_download=True, 
                        clean_text=False, verbose=False):
    """
    Download transcript from a video URL.
    
    Args:
        url: URL of the video
        output_dir: Directory to save the transcript
        language: Language code for the subtitles
        format: Format of the subtitles (srt, vtt, txt)
        auto_subs: Whether to download auto-generated subtitles
        manual_subs: Whether to download manually created subtitles
        skip_download: Whether to skip downloading the video
        clean_text: Whether to remove timestamps and create clean text
        verbose: Whether to print verbose output
    
    Returns:
        Path to the downloaded transcript file or None if failed
    """
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    # Base command
    command = ["yt-dlp"]
    
    # Add options
    if skip_download:
        command.append("--skip-download")
    
    if manual_subs:
        command.append("--write-sub")
    
    if auto_subs:
        command.append("--write-auto-sub")
    
    # Add language
    command.extend(["--sub-lang", language])
    
    # Add format
    command.extend(["--sub-format", format])
    
    # Add output directory if specified
    if output_dir:
        command.extend(["-o", os.path.join(output_dir, "%(title)s.%(ext)s")])
    
    # Add URL
    command.append(url)
    
    if verbose:
        print(f"Running command: {' '.join(command)}")
    
    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error downloading transcript: {result.stderr}")
        return None
    
    # Find the subtitle file
    output_files = []
    
    # Parse the output to find the subtitle file
    for line in result.stdout.split('\n'):
        if "Writing video subtitles to:" in line:
            subtitle_file = line.split("Writing video subtitles to:")[1].strip()
            output_files.append(subtitle_file)
    
    if not output_files:
        print("No subtitle file found in the output.")
        if verbose:
            print(result.stdout)
        return None
    
    # If clean text option is enabled, convert to plain text without timestamps
    if clean_text and output_files:
        txt_files = []
        for subtitle_file in output_files:
            txt_file = os.path.splitext(subtitle_file)[0] + ".txt"
            if format == "srt":
                convert_srt_to_txt(subtitle_file, txt_file)
            elif format == "vtt":
                convert_vtt_to_txt(subtitle_file, txt_file)
            txt_files.append(txt_file)
            # Remove the original subtitle file since we only want the clean text
            try:
                os.remove(subtitle_file)
                if verbose:
                    print(f"Removed original subtitle file: {subtitle_file}")
            except OSError:
                pass
        return txt_files


def convert_srt_to_txt(srt_file, txt_file):
    """Convert SRT file to plain text with well-formatted sentences and paragraphs."""
    import itertools
    try:
        with open(srt_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove timestamps and indices
        lines = content.split('\n')
        text_lines = []
        for line in lines:
            if not line.strip():
                continue
            if line.strip().isdigit():
                continue
            if re.match(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', line):
                continue
            text_lines.append(line.strip())

        # Join lines, then split into sentences
        raw_text = ' '.join(text_lines)
        # Normalize spaces
        raw_text = re.sub(r'\s+', ' ', raw_text)
        # Split into sentences using punctuation
        sentences = re.split(r'(?<=[.!?]) +', raw_text)

        # Group sentences into paragraphs (every 4 sentences = 1 paragraph)
        paragraph_size = 4
        paragraphs = [' '.join(sentences[i:i+paragraph_size]).strip() for i in range(0, len(sentences), paragraph_size)]
        formatted_text = '\n\n'.join(paragraphs)

        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(formatted_text)

        print(f"Created clean text file: {txt_file}")
        return True
    except Exception as e:
        print(f"Error converting SRT to TXT: {e}")
        return False


def convert_vtt_to_txt(vtt_file, txt_file):
    """Convert VTT file to plain text with well-formatted sentences and paragraphs."""
    import itertools
    try:
        with open(vtt_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove WEBVTT header, timestamps, and cue identifiers
        lines = content.split('\n')
        text_lines = []
        for line in lines:
            if line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
                continue
            if not line.strip():
                continue
            if re.match(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}', line):
                continue
            if line.strip().isdigit():
                continue
            # Remove inline VTT tags (e.g., <c>...</c> and <...>)
            clean_line = re.sub(r'<[^>]+>', '', line)
            text_lines.append(clean_line.strip())

        # Join lines, then split into sentences
        raw_text = ' '.join(text_lines)
        # Normalize spaces
        raw_text = re.sub(r'\s+', ' ', raw_text)
        # Split into sentences using punctuation
        sentences = re.split(r'(?<=[.!?]) +', raw_text)

        # Group sentences into paragraphs (every 4 sentences = 1 paragraph)
        paragraph_size = 4
        paragraphs = [' '.join(sentences[i:i+paragraph_size]).strip() for i in range(0, len(sentences), paragraph_size)]
        formatted_text = '\n\n'.join(paragraphs)

        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(formatted_text)

        print(f"Created clean text file: {txt_file}")
        return True
    except Exception as e:
        print(f"Error converting VTT to TXT: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Download video transcripts using yt-dlp")
    
    parser.add_argument("url", help="URL of the video to download transcript from")
    parser.add_argument("-o", "--output-dir", help="Directory to save the transcript")
    parser.add_argument("-l", "--language", default="en", help="Language code for subtitles (default: en)")
    parser.add_argument("-f", "--format", default="srt", choices=["srt", "vtt", "txt"], 
                        help="Format of the subtitles (default: srt)")
    parser.add_argument("--no-auto", action="store_true", help="Don't download auto-generated subtitles")
    parser.add_argument("--no-manual", action="store_true", help="Don't download manually created subtitles")
    parser.add_argument("--download-video", action="store_true", help="Also download the video")
    parser.add_argument("--clean-text", action="store_true", 
                        help="Create a clean text file without timestamps")
    parser.add_argument("--list-subs", action="store_true", 
                        help="List available subtitles and exit")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print verbose output")
    
    args = parser.parse_args()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # List available subtitles if requested
    if args.list_subs:
        list_available_subtitles(args.url)
        sys.exit(0)
    
    # Download transcript
    output_files = download_transcript(
        args.url,
        output_dir=args.output_dir,
        language=args.language,
        format=args.format,
        auto_subs=not args.no_auto,
        manual_subs=not args.no_manual,
        skip_download=not args.download_video,
        clean_text=args.clean_text,
        verbose=args.verbose
    )
    
    if output_files:
        print(f"\nTranscript downloaded successfully:")
        for file in output_files:
            print(f"- {file}")
    else:
        print("Failed to download transcript.")
        sys.exit(1)


if __name__ == "__main__":
    main()
