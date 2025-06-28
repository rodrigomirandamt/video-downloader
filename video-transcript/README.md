# Video Transcript Downloader

A Python tool to download transcripts/subtitles from YouTube and other video sources supported by yt-dlp. The tool can convert subtitles to clean, well-formatted text with proper punctuation and paragraph breaks.

## Features

- Download auto-generated or manually created subtitles
- Support for multiple subtitle languages
- Convert subtitles to different formats (srt, vtt, txt)
- **Clean text formatting**: Remove timestamps and create readable text with proper sentences and paragraphs
- List available subtitles for a video
- Automatic cleanup of intermediate files when using clean text mode

## Installation

1. Clone this repository or download the script:

```bash
git clone https://github.com/yourusername/video-transcript-downloader.git
cd video-transcript-downloader
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Make sure you have ffmpeg installed (optional but recommended):
   - On macOS: `brew install ffmpeg`
   - On Ubuntu/Debian: `sudo apt-get install ffmpeg`
   - On Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## Usage

### Basic Usage

Download English subtitles and convert to clean, formatted text:

```bash
python3 video_transcribe.py --clean-text "https://www.youtube.com/watch?v=VIDEO_ID"
```

Download raw subtitles (with timestamps):

```bash
python3 video_transcribe.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Command Line Options

```
usage: video_transcribe.py [-h] [-o OUTPUT_DIR] [-l LANGUAGE] [-f {srt,vtt,txt}] 
                           [--no-auto] [--no-manual] [--download-video] 
                           [--clean-text] [--list-subs] [-v] url

positional arguments:
  url                   URL of the video to download transcript from

options:
  -h, --help            Show help message and exit
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Directory to save the transcript
  -l LANGUAGE, --language LANGUAGE
                        Language code for subtitles (default: en)
  -f {srt,vtt,txt}, --format {srt,vtt,txt}
                        Format of the subtitles (default: srt)
  --no-auto             Don't download auto-generated subtitles
  --no-manual           Don't download manually created subtitles
  --download-video      Also download the video file
  --clean-text          Create formatted text without timestamps (recommended)
  --list-subs           List available subtitles and exit
  -v, --verbose         Print verbose output
```

### Detailed Examples

#### List Available Subtitles

See what subtitle languages are available for a video:

```bash
python3 video_transcribe.py --list-subs "https://www.youtube.com/watch?v=VIDEO_ID"
```

#### Download Clean, Formatted Text (Recommended)

This creates a readable text file with proper sentences and paragraphs:

```bash
python3 video_transcribe.py --clean-text "https://www.youtube.com/watch?v=VIDEO_ID"
```

Output example:
```
We're no strangers to love. You know the rules and so do I. A full commitment's what I'm thinking of. You wouldn't get this from any other guy.

I just wanna tell you how I'm feeling. Gotta make you understand. Never gonna give you up. Never gonna let you down.

Never gonna run around and desert you. Never gonna make you cry. Never gonna say goodbye. Never gonna tell a lie and hurt you.
```

#### Download Specific Language

Download subtitles in French:

```bash
python3 video_transcribe.py --clean-text -l fr "https://www.youtube.com/watch?v=VIDEO_ID"
```

#### Choose Subtitle Format

Download in VTT format (useful for web players):

```bash
python3 video_transcribe.py -f vtt "https://www.youtube.com/watch?v=VIDEO_ID"
```

Download in SRT format (most compatible):

```bash
python3 video_transcribe.py -f srt "https://www.youtube.com/watch?v=VIDEO_ID"
```

#### Save to Specific Directory

Save transcript to a custom directory:

```bash
python3 video_transcribe.py --clean-text -o /path/to/transcripts "https://www.youtube.com/watch?v=VIDEO_ID"
```

#### Download Video with Subtitles

Download both the video file and subtitles:

```bash
python3 video_transcribe.py --download-video --clean-text "https://www.youtube.com/watch?v=VIDEO_ID"
```

#### Control Subtitle Sources

Download only auto-generated subtitles (no manual captions):

```bash
python3 video_transcribe.py --no-manual --clean-text "https://www.youtube.com/watch?v=VIDEO_ID"
```

Download only manually created subtitles (no auto-generated):

```bash
python3 video_transcribe.py --no-auto --clean-text "https://www.youtube.com/watch?v=VIDEO_ID"
```

#### Verbose Output

Get detailed information about the download process:

```bash
python3 video_transcribe.py --clean-text -v "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Advanced Examples

#### Multiple Language Downloads

To download subtitles in multiple languages, run separate commands:

```bash
python3 video_transcribe.py --clean-text -l en "https://www.youtube.com/watch?v=VIDEO_ID"
python3 video_transcribe.py --clean-text -l es "https://www.youtube.com/watch?v=VIDEO_ID"
python3 video_transcribe.py --clean-text -l fr "https://www.youtube.com/watch?v=VIDEO_ID"
```

#### Batch Processing

Create a simple bash script to process multiple videos:

```bash
#!/bin/bash
urls=(
    "https://www.youtube.com/watch?v=VIDEO_ID1"
    "https://www.youtube.com/watch?v=VIDEO_ID2"
    "https://www.youtube.com/watch?v=VIDEO_ID3"
)

for url in "${urls[@]}"; do
    python3 video_transcribe.py --clean-text "$url"
done
```

## Text Formatting Features

When using `--clean-text`, the tool:

1. **Removes all timestamps and metadata**
2. **Cleans up subtitle formatting** (removes VTT tags, cue identifiers, etc.)
3. **Creates proper sentences** using punctuation detection
4. **Groups sentences into paragraphs** (4 sentences per paragraph by default)
5. **Normalizes whitespace** for consistent formatting
6. **Automatically deletes** the original subtitle file, keeping only the clean text

## Supported Platforms

This tool works with any video platform supported by yt-dlp, including:

- YouTube
- Vimeo
- Dailymotion
- Facebook
- Instagram
- TikTok
- And many more...

## Common Language Codes

- `en` - English
- `es` - Spanish
- `fr` - French
- `de` - German
- `it` - Italian
- `pt` - Portuguese
- `ru` - Russian
- `ja` - Japanese
- `ko` - Korean
- `zh` - Chinese

## Troubleshooting

### No subtitles found
- Use `--list-subs` to see available languages
- Try using both `--no-auto` and `--no-manual` separately to see which type is available
- Some videos may not have subtitles in your requested language

### Permission errors
- Make sure you have write permissions in the output directory
- On Unix systems, you may need to make the script executable: `chmod +x video_transcribe.py`

### yt-dlp errors
- Update yt-dlp: `pip install --upgrade yt-dlp`
- Some videos may be geo-restricted or require authentication

## Output Files

- **With `--clean-text`**: Only creates `.txt` files with formatted text
- **Without `--clean-text`**: Creates subtitle files in the specified format (`.srt`, `.vtt`)
- **File naming**: Uses the video title and video ID for unique identification

## License

This project is open source. Please check the license file for details.

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The amazing tool that powers this script
- [ffmpeg](https://ffmpeg.org/) - For subtitle processing capabilities
