import threading
import yt_dlp
import os
import traceback
from queue import Queue

class Downloader:
    """Handles all video download operations in a separate thread."""

    def __init__(self, message_queue: Queue):
        """
        Initializes the Downloader.
        
        Args:
            message_queue: A queue to send messages (logs, progress, status) to the UI thread.
        """
        self.message_queue = message_queue
        self.cancel_requested = False
        self.download_thread = None

    def _send_message(self, msg_type, **kwargs):
        """Sends a message to the UI thread's queue."""
        self.message_queue.put({'type': msg_type, **kwargs})

    def _progress_hook(self, d):
        """yt-dlp hook to capture download progress."""
        if self.cancel_requested:
            raise Exception("Download cancelled by user")

        if d['status'] == 'downloading':
            percent = None
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            
            if total_bytes:
                percent = (d.get('downloaded_bytes', 0) / total_bytes) * 100
            elif d.get('_percent_str'):
                try:
                    percent_str = d['_percent_str'].strip().replace('%', '')
                    percent = float(percent_str)
                except (ValueError, TypeError):
                    percent = None
            
            if percent is not None:
                self._send_message('progress', value=percent)

        elif d['status'] == 'finished':
            self._send_message('progress', value=100)

    def _download_task(self, url, ydl_opts):
        """The actual download task that runs in a thread."""
        try:
            self._send_message('log', text=f"Starting download for: {url}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            if not self.cancel_requested:
                self._send_message('log', text="Download completed successfully.")

        except Exception as e:
            if "cancelled by user" not in str(e).lower():
                self._send_message('log', text=f"ERROR: {e}")
        finally:
            self._send_message('done')

    def start_download(self, url, download_path, format_options, platform):
        """Starts the video download in a new thread."""
        self.cancel_requested = False

        ydl_opts = {
            'outtmpl': os.path.join(download_path, '%(uploader)s - %(title)s.%(ext)s'),
            'format': format_options,
            'progress_hooks': [self._progress_hook],
            'logger': self._YTDLogger(lambda msg: self._send_message('log', text=msg)),
            'abort_on_error': True,
            'socket_timeout': 30,
            'retries': 3,
            'no_warnings': True,
        }

        if platform == "twitter":
            ydl_opts['extractor_args'] = {'twitter': {'api': ['syndication', 'legacy', 'graphql']}}

        self.download_thread = threading.Thread(
            target=self._download_task,
            args=(url, ydl_opts),
            daemon=True
        )
        self.download_thread.start()

    def cancel_download(self):
        """Signals the download thread to cancel."""
        if self.download_thread and self.download_thread.is_alive():
            self.cancel_requested = True
            self._send_message('log', text="Cancellation requested by user.")

    class _YTDLogger:
        """A simple logger for yt-dlp to route messages to our log callback."""
        def __init__(self, callback):
            self._callback = callback
        def debug(self, msg):
            if msg.startswith('[youtube]') or 'Extracting' in msg or 'Downloading' in msg:
                 self._callback(msg)
        def info(self, msg):
            self._callback(msg)
        def warning(self, msg):
            self._callback(f"WARNING: {msg}")
        def error(self, msg):
            self._callback(f"ERROR: {msg}")



