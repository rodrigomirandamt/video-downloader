import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import yt_dlp
import os
from pathlib import Path

class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Set modern theme
        style = ttk.Style()
        style.theme_use('winnative')
        
        # Configure colors
        self.root.configure(bg='#f0f0f0')
        
        # Default download path
        self.download_path = os.path.join(os.getcwd(), "videos")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🎥 YouTube Video Downloader", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # URL input
        ttk.Label(main_frame, text="YouTube URL:", font=('Arial', 10)).grid(
            row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        self.url_var = tk.StringVar()
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=50)
        url_entry.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Paste button
        paste_btn = ttk.Button(main_frame, text="📋 Paste", command=self.paste_url)
        paste_btn.grid(row=2, column=2, padx=(10, 0), pady=(0, 15))
        
        # Download path
        ttk.Label(main_frame, text="Download Folder:", font=('Arial', 10)).grid(
            row=3, column=0, sticky=tk.W, pady=(0, 5))
        
        path_frame = ttk.Frame(main_frame)
        path_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        path_frame.columnconfigure(0, weight=1)
        
        self.path_var = tk.StringVar(value=self.download_path)
        path_entry = ttk.Entry(path_frame, textvariable=self.path_var, state='readonly')
        path_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        browse_btn = ttk.Button(path_frame, text="📁 Browse", command=self.browse_folder)
        browse_btn.grid(row=0, column=1)
        
        # Quality selection
        ttk.Label(main_frame, text="Video Quality:", font=('Arial', 10)).grid(
            row=5, column=0, sticky=tk.W, pady=(0, 5))
        
        self.quality_var = tk.StringVar(value="720p")
        quality_combo = ttk.Combobox(main_frame, textvariable=self.quality_var, 
                                   values=["1080p", "720p", "480p", "360p", "Audio Only"], 
                                   state="readonly", width=20)
        quality_combo.grid(row=6, column=0, sticky=tk.W, pady=(0, 20))
        
        # Download button
        self.download_btn = ttk.Button(main_frame, text="⬇️ Download Video", 
                                     command=self.start_download, style='Accent.TButton')
        self.download_btn.grid(row=7, column=0, columnspan=3, pady=(0, 20))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to download")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                               font=('Arial', 9), foreground='#666')
        status_label.grid(row=9, column=0, columnspan=3, pady=(0, 10))
        
        # Log text area
        ttk.Label(main_frame, text="Download Log:", font=('Arial', 10)).grid(
            row=10, column=0, sticky=tk.W, pady=(10, 5))
        
        log_frame = ttk.Frame(main_frame)
        log_frame.grid(row=11, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(11, weight=1)
        
        self.log_text = tk.Text(log_frame, height=8, wrap=tk.WORD, font=('Consolas', 9))
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Clear log button
        clear_btn = ttk.Button(main_frame, text="🗑️ Clear Log", command=self.clear_log)
        clear_btn.grid(row=12, column=0, sticky=tk.W, pady=(5, 0))
        
        # Open folder button
        open_folder_btn = ttk.Button(main_frame, text="📂 Open Download Folder", 
                                   command=self.open_download_folder)
        open_folder_btn.grid(row=12, column=2, sticky=tk.E, pady=(5, 0))
        
    def paste_url(self):
        try:
            clipboard_content = self.root.clipboard_get()
            self.url_var.set(clipboard_content)
            self.log_message("URL pasted from clipboard")
        except:
            self.log_message("No URL found in clipboard")
    
    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.download_path)
        if folder:
            self.download_path = folder
            self.path_var.set(folder)
            self.log_message(f"Download folder changed to: {folder}")
    
    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
    
    def open_download_folder(self):
        if os.path.exists(self.download_path):
            os.startfile(self.download_path)
        else:
            messagebox.showwarning("Folder Not Found", 
                                 f"Download folder does not exist: {self.download_path}")
    
    def log_message(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_status(self, message):
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def get_format_selector(self):
        quality = self.quality_var.get()
        if quality == "Audio Only":
            return "bestaudio/best"
        elif quality == "1080p":
            return "best[height<=1080]"
        elif quality == "720p":
            return "best[height<=720]"
        elif quality == "480p":
            return "best[height<=480]"
        elif quality == "360p":
            return "best[height<=360]"
        else:
            return "best[height<=720]"
    
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            if 'total_bytes' in d:
                percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                self.progress_var.set(percent)
                self.update_status(f"Downloading... {percent:.1f}%")
            elif '_percent_str' in d:
                percent_str = d['_percent_str'].strip('%')
                try:
                    percent = float(percent_str)
                    self.progress_var.set(percent)
                    self.update_status(f"Downloading... {percent:.1f}%")
                except:
                    pass
        elif d['status'] == 'finished':
            self.progress_var.set(100)
            self.update_status("Download completed!")
            self.log_message(f"✅ Downloaded: {d['filename']}")
    
    def download_video(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        
        # Create output directory
        os.makedirs(self.download_path, exist_ok=True)
        
        # Configure yt-dlp options
        ydl_opts = {
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
            'format': self.get_format_selector(),
            'progress_hooks': [self.progress_hook],
        }
        
        try:
            self.update_status("Getting video information...")
            self.log_message(f"🔍 Processing URL: {url}")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get video info first
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'N/A')
                duration = info.get('duration', 'N/A')
                uploader = info.get('uploader', 'N/A')
                
                self.log_message(f"📹 Title: {title}")
                self.log_message(f"⏱️ Duration: {duration} seconds")
                self.log_message(f"👤 Uploader: {uploader}")
                self.log_message("🚀 Starting download...")
                
                # Download the video
                ydl.download([url])
                
                self.log_message("✅ Download completed successfully!")
                messagebox.showinfo("Success", f"Video downloaded successfully!\n\nSaved to: {self.download_path}")
                
        except Exception as e:
            error_msg = f"❌ Error downloading video: {str(e)}"
            self.log_message(error_msg)
            self.update_status("Download failed")
            messagebox.showerror("Download Error", str(e))
        
        finally:
            self.download_btn.configure(state='normal', text="⬇️ Download Video")
            self.progress_var.set(0)
    
    def start_download(self):
        self.download_btn.configure(state='disabled', text="⏳ Downloading...")
        self.progress_var.set(0)
        
        # Run download in separate thread to prevent GUI freezing
        thread = threading.Thread(target=self.download_video, daemon=True)
        thread.start()

def main():
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main() 