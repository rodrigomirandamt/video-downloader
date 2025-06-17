import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import os
import re
from .styles import setup_styles
from ..services.downloader import Downloader

class MainWindow:
    """The main GUI window for the MediaSlayer application."""

    def __init__(self, root):
        self.root = root
        self.is_downloading = False
        self.download_completed = False
        
        self._setup_variables()
        self._setup_window()
        self.downloader = Downloader(
            progress_callback=self._update_progress_safe,
            log_callback=self._add_log_safe,
            done_callback=self._on_download_done_safe
        )
        self.create_ui()

    def _setup_variables(self):
        """Initialize all Tkinter variables."""
        self.url_var = tk.StringVar()
        self.format_var = tk.StringVar()
        self.quality_var = tk.StringVar()
        self.progress_var = tk.DoubleVar()
        self.download_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        self.download_path_var = tk.StringVar(value=self.download_path)
        self.platform = None
        
    def _setup_window(self):
        """Configure the main application window."""
        self.root.title("MediaSlayer")
        self.root.geometry("600x750")
        self.root.minsize(550, 700)
        self.root.configure(background='#1e293b')
        self.style = setup_styles()

    def create_ui(self):
        """Create and layout all the UI widgets."""
        main_frame = ttk.Frame(self.root, style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # --- Title ---
        title_label = ttk.Label(main_frame, text="MediaSlayer", font=("Segoe UI", 24, "bold"), background='#1e293b', foreground='#dc2626')
        title_label.pack(pady=(0, 20))

        # --- URL Input ---
        self._create_url_input(main_frame)
        
        # --- Format and Quality Dropdowns ---
        self._create_dropdowns(main_frame)
        
        # --- Download Location ---
        self._create_path_input(main_frame)

        # --- Progress Bar and Logs ---
        self._create_progress_and_logs(main_frame)
        
        # --- Action Buttons ---
        self._create_action_buttons(main_frame)

        self.url_entry.focus_set()

    def _create_url_input(self, parent):
        url_section = ttk.Frame(parent, style='TFrame')
        url_section.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(url_section, text="⚡ Target URL", style='FieldLabel.TLabel', background='#1e293b').pack(anchor=tk.W, pady=(0, 5))
        self.url_entry = ttk.Entry(url_section, textvariable=self.url_var, style='Modern.TEntry')
        self.url_entry.pack(fill=tk.X, ipady=10)
        self.url_entry.bind('<FocusIn>', self._prepare_for_new_download)

    def _create_dropdowns(self, parent):
        dropdowns_frame = ttk.Frame(parent, style='TFrame')
        dropdowns_frame.pack(fill=tk.X, pady=(0, 15))
        dropdowns_frame.columnconfigure(0, weight=1)
        dropdowns_frame.columnconfigure(1, weight=1)

        # Format
        format_frame = ttk.Frame(dropdowns_frame, style='TFrame')
        format_frame.grid(row=0, column=0, sticky='ew', padx=(0, 10))
        ttk.Label(format_frame, text="💎 Format Enchantment", style='FieldLabel.TLabel', background='#1e293b').pack(anchor=tk.W, pady=(0, 5))
        self.format_combo = ttk.Combobox(format_frame, textvariable=self.format_var, values=["⚔️ MP4", "🎵 MP3", "🛡️ WebM", "🔮 WAV"], state="readonly", style='Modern.TCombobox')
        self.format_combo.pack(fill=tk.X)
        self.format_combo.set("⚔️ MP4")

        # Quality
        quality_frame = ttk.Frame(dropdowns_frame, style='TFrame')
        quality_frame.grid(row=0, column=1, sticky='ew', padx=(10, 0))
        ttk.Label(quality_frame, text="👑 Quality Level", style='FieldLabel.TLabel', background='#1e293b').pack(anchor=tk.W, pady=(0, 5))
        self.quality_combo = ttk.Combobox(quality_frame, textvariable=self.quality_var, values=["👑 1080p", "⭐ 720p", "🔸 480p", "⚪ 360p"], state="readonly", style='Modern.TCombobox')
        self.quality_combo.pack(fill=tk.X)
        self.quality_combo.set("⭐ 720p")

    def _create_path_input(self, parent):
        path_section = ttk.Frame(parent, style='TFrame')
        path_section.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(path_section, text="📂 Download Location", style='FieldLabel.TLabel', background='#1e293b').pack(anchor=tk.W, pady=(0, 5))
        
        path_inner = ttk.Frame(path_section, style='TFrame')
        path_inner.pack(fill=tk.X)

        self.path_entry = ttk.Entry(path_inner, textvariable=self.download_path_var, style='Modern.TEntry')
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_btn = ttk.Button(path_inner, text="Browse", command=self._browse_path, style='RedGradient.TButton')
        browse_btn.pack(side=tk.LEFT, padx=(10, 0))

    def _create_progress_and_logs(self, parent):
        self.progress_frame = ttk.Frame(parent, style='TFrame')
        # Packed later when download starts

        self.progress_status = ttk.Label(self.progress_frame, text="Casting download spell...", style='TLabel')
        self.progress_status.pack(side=tk.LEFT)
        self.progress_percent = ttk.Label(self.progress_frame, text="0%", style='TLabel', foreground='#f87171')
        self.progress_percent.pack(side=tk.RIGHT)
        self.progress_bar = ttk.Progressbar(self.progress_frame, variable=self.progress_var, maximum=100, style='Modern.Horizontal.TProgressbar')
        self.progress_bar.pack(fill=tk.X, pady=(5, 0))
        
        self.log_text = scrolledtext.ScrolledText(parent, height=10, background='#1e293b', foreground='#d1d5db', font=('Consolas', 9), state='disabled', wrap='word', relief='solid', borderwidth=0, highlightthickness=1, highlightbackground="#475569")
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=(0,15))

    def _create_action_buttons(self, parent):
        button_frame = ttk.Frame(parent, style='TFrame')
        button_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.download_btn = ttk.Button(button_frame, text="⚔️ Execute Download Quest", command=self._start_download, style='RedGradient.TButton')
        self.download_btn.pack(fill=tk.X, ipady=8)
        
        self.cancel_btn = ttk.Button(button_frame, text="❌ Cancel Quest", command=self._cancel_download, style='RedGradient.TButton')
        # Packed later when download starts
        
    def _start_download(self):
        if self.is_downloading:
            return

        self.download_completed = False
        url = self.url_var.get().strip()
        
        # --- Perform platform validation right when the button is clicked ---
        self._detect_platform(url)
        
        if not url or not self.platform:
            messagebox.showerror("Error", "Please enter a valid YouTube or X/Twitter URL.")
            return

        self.is_downloading = True
        self.download_btn.pack_forget()
        self.cancel_btn.pack(fill=tk.X, ipady=8)
        
        self.progress_frame.pack(fill=tk.X, pady=(0, 10), before=self.log_text)
        self.progress_var.set(0)
        self.progress_percent.config(text="0%")

        self.log_text.configure(state='normal')
        self.log_text.delete('1.0', tk.END)
        self.log_text.configure(state='disabled')
        
        format_str = self.format_var.get().split(" ")[-1]
        quality_str = self.quality_var.get().split(" ")[-1]
        format_options = self._get_format_options(format_str, quality_str)

        self.downloader.start_download(url, self.download_path_var.get(), format_options, self.platform)

    def _cancel_download(self):
        self.downloader.cancel_download()

    def _on_download_done_safe(self):
        """A thread-safe method to reset the UI after download completion."""
        self.download_completed = True
        self.root.after(0, self._reset_ui)

    def _reset_ui(self):
        self.is_downloading = False
        self.cancel_btn.pack_forget()
        self.download_btn.pack(fill=tk.X, ipady=8)
        self.root.after(3000, self.progress_frame.pack_forget)

    def _update_progress_safe(self, percent):
        """Thread-safe method to update the progress bar."""
        self.root.after(0, lambda: self.progress_var.set(percent))
        self.root.after(0, lambda: self.progress_percent.config(text=f"{int(percent)}%"))

    def _add_log_safe(self, message):
        """Thread-safe method to add a message to the log."""
        self.root.after(0, lambda: self._add_log(message))

    def _add_log(self, message):
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.yview(tk.END)
        self.log_text.configure(state='disabled')

    def _browse_path(self):
        selected = filedialog.askdirectory(initialdir=self.download_path_var.get())
        if selected:
            self.download_path_var.set(selected)

    def _detect_platform(self, url):
        """Detects the platform from the URL and sets self.platform."""
        if re.search(r'(youtube\.com|youtu\.be)', url):
            self.platform = "youtube"
        elif re.search(r'(twitter\.com|x\.com)', url):
            self.platform = "twitter"
        else:
            self.platform = None

    def _get_format_options(self, format_type, quality_text):
        if format_type in ["MP3", "WAV"]:
            return f"bestaudio/best[ext={format_type.lower()}]"
        
        quality_map = {
            "1080p": "best[height<=1080]",
            "720p": "best[height<=720]",
            "480p": "best[height<=480]",
            "360p": "best[height<=360]",
        }
        quality_selector = quality_map.get(quality_text, "best")
        
        # Flexible format string for video
        return f"{quality_selector}[ext={format_type.lower()}]/{quality_selector}/bestvideo+bestaudio/best"

    def _prepare_for_new_download(self, event=None):
        """Clears the interface when the user is ready to start a new download."""
        if self.download_completed and not self.is_downloading:
            self.url_var.set("")
            self.log_text.configure(state='normal')
            self.log_text.delete('1.0', tk.END)
            self.log_text.configure(state='disabled')
            self.progress_frame.pack_forget() # Hide the old progress bar immediately
            self.download_completed = False



