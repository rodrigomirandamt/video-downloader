import threading
import yt_dlp
import os
import traceback

class Downloader:
    """Handles all video download operations in a separate thread."""

    def __init__(self, progress_callback=None, log_callback=None, done_callback=None):
        """
        Initializes the Downloader.
        
        Args:
            progress_callback: A function to call with download progress (0-100).
            log_callback: A function to call for logging messages.
            done_callback: A function to call when the download is finished, fails, or is cancelled.
        """
        self.progress_callback = progress_callback
        self.log_callback = log_callback
        self.done_callback = done_callback
        self.cancel_requested = False
        self.download_thread = None

    def _log(self, message):
        if self.log_callback:
            self.log_callback(message)

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
            
            if percent is not None and self.progress_callback:
                self.progress_callback(percent)

        elif d['status'] == 'finished':
            if self.progress_callback:
                self.progress_callback(100)

    def _download_task(self, url, ydl_opts):
        """The actual download task that runs in a thread."""
        try:
            self._log(f"Starting download for: {url}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            if not self.cancel_requested:
                self._log("Download completed successfully.")

        except Exception as e:
            if "cancelled by user" not in str(e).lower():
                self._log(f"ERROR: {e}")
        finally:
            if self.done_callback:
                self.done_callback()

    def start_download(self, url, download_path, format_options, platform):
        """Starts the video download in a new thread."""
        self.cancel_requested = False

        ydl_opts = {
            'outtmpl': os.path.join(download_path, '%(uploader)s - %(title)s.%(ext)s'),
            'format': format_options,
            'progress_hooks': [self._progress_hook],
            'logger': self._YTDLogger(self._log),
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
        self._log("--- CANCEL TRACEBACK ---")
        traceback.print_stack(file=self._LogProxy(self._log))
        self._log("--------------------------")

        if self.download_thread and self.download_thread.is_alive():
            self.cancel_requested = True
            self._log("Cancellation requested by user.")

    class _YTDLogger:
        """A simple logger for yt-dlp to route messages to our log callback."""
        def __init__(self, callback):
            self._callback = callback
        def debug(self, msg):
            # yt-dlp debug messages are very noisy, only log if starts with "youtube" or a clear message
            if msg.startswith('[youtube]') or 'Extracting' in msg or 'Downloading' in msg:
                 self._callback(msg)
        def info(self, msg):
            self._callback(msg)
        def warning(self, msg):
            self._callback(f"WARNING: {msg}")
        def error(self, msg):
            self._callback(f"ERROR: {msg}")

class _LogProxy:
    """A helper class to redirect traceback's print output to our logger."""
    def __init__(self, log_fn):
        self.log_fn = log_fn
    def write(self, s):
        self.log_fn(s)
    def flush(self):
        pass



