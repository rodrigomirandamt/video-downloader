import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import yt_dlp
import os
import time
from pathlib import Path
import webbrowser
from datetime import datetime
import json

class ModernYouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_variables()
        self.setup_styles()
        self.create_modern_ui()
        self.load_settings()
        
    def setup_window(self):
        """Configure main window with modern styling"""
        self.root.title("🎥 YouTube Downloader Pro")
        self.root.geometry("800x700")
        self.root.minsize(700, 600)
        self.root.configure(bg='#1e1e1e')
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
        
        # Configure window icon (if available)
        try:
            self.root.iconbitmap('youtube.ico')
        except:
            pass
    
    def setup_variables(self):
        """Initialize all variables"""
        self.url_var = tk.StringVar()
        self.path_var = tk.StringVar()
        self.quality_var = tk.StringVar(value="720p (HD)")
        self.format_var = tk.StringVar(value="mp4")
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Pronto para download")
        self.speed_var = tk.StringVar(value="")
        self.eta_var = tk.StringVar(value="")
        
        # Default paths
        self.download_path = os.path.join(os.getcwd(), "downloads")
        self.path_var.set(self.download_path)
        
        # Settings
        self.settings_file = "downloader_settings.json"
        self.download_history = []
        
    def setup_styles(self):
        """Configure modern ttk styles"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure modern colors
        colors = {
            'bg': '#1e1e1e',
            'fg': '#ffffff',
            'select_bg': '#0078d4',
            'select_fg': '#ffffff',
            'button_bg': '#0078d4',
            'button_hover': '#106ebe',
            'entry_bg': '#2d2d2d',
            'frame_bg': '#252525'
        }
        
        # Configure styles
        self.style.configure('Modern.TFrame', background=colors['bg'])
        self.style.configure('Card.TFrame', background=colors['frame_bg'], relief='flat', borderwidth=1)
        self.style.configure('Modern.TLabel', background=colors['bg'], foreground=colors['fg'], font=('Segoe UI', 10))
        self.style.configure('Title.TLabel', background=colors['bg'], foreground=colors['fg'], font=('Segoe UI', 18, 'bold'))
        self.style.configure('Subtitle.TLabel', background=colors['bg'], foreground='#cccccc', font=('Segoe UI', 9))
        
        # Button styles
        self.style.configure('Modern.TButton', 
                           background=colors['button_bg'], 
                           foreground=colors['fg'],
                           borderwidth=0,
                           focuscolor='none',
                           font=('Segoe UI', 10, 'bold'))
        self.style.map('Modern.TButton',
                      background=[('active', colors['button_hover']),
                                ('pressed', '#005a9e')])
        
        # Entry styles
        self.style.configure('Modern.TEntry',
                           fieldbackground=colors['entry_bg'],
                           foreground=colors['fg'],
                           borderwidth=1,
                           insertcolor=colors['fg'])
        
        # Combobox styles
        self.style.configure('Modern.TCombobox',
                           fieldbackground=colors['entry_bg'],
                           foreground=colors['fg'],
                           borderwidth=1)
        
        # Progress bar
        self.style.configure('Modern.Horizontal.TProgressbar',
                           background=colors['select_bg'],
                           troughcolor=colors['entry_bg'],
                           borderwidth=0,
                           lightcolor=colors['select_bg'],
                           darkcolor=colors['select_bg'])
    
    def create_modern_ui(self):
        """Create the modern professional UI"""
        # Main container
        main_container = ttk.Frame(self.root, style='Modern.TFrame', padding="20")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=1)
        
        # Header section
        self.create_header(main_container)
        
        # URL input section
        self.create_url_section(main_container)
        
        # Settings section
        self.create_settings_section(main_container)
        
        # Progress section
        self.create_progress_section(main_container)
        
        # Log section
        self.create_log_section(main_container)
        
        # Footer section
        self.create_footer(main_container)
    
    def create_header(self, parent):
        """Create professional header"""
        header_frame = ttk.Frame(parent, style='Modern.TFrame')
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 30))
        header_frame.columnconfigure(0, weight=1)
        
        # Title with icon
        title_frame = ttk.Frame(header_frame, style='Modern.TFrame')
        title_frame.grid(row=0, column=0)
        
        title_label = ttk.Label(title_frame, text="🎥 YouTube Downloader Pro", style='Title.TLabel')
        title_label.grid(row=0, column=0)
        
        subtitle_label = ttk.Label(header_frame, text="Download de vídeos do YouTube com qualidade profissional", 
                                 style='Subtitle.TLabel')
        subtitle_label.grid(row=1, column=0, pady=(5, 0))
    
    def create_url_section(self, parent):
        """Create URL input section"""
        url_card = ttk.Frame(parent, style='Card.TFrame', padding="20")
        url_card.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        url_card.columnconfigure(1, weight=1)
        
        # URL label
        url_label = ttk.Label(url_card, text="🔗 URL do YouTube:", style='Modern.TLabel')
        url_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 8))
        
        # URL input frame
        url_input_frame = ttk.Frame(url_card, style='Modern.TFrame')
        url_input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        url_input_frame.columnconfigure(0, weight=1)
        
        # URL entry
        self.url_entry = ttk.Entry(url_input_frame, textvariable=self.url_var, 
                                  style='Modern.TEntry', font=('Segoe UI', 11))
        self.url_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Paste button
        paste_btn = ttk.Button(url_input_frame, text="📋 Colar", 
                              command=self.paste_url, style='Modern.TButton')
        paste_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Analyze button
        analyze_btn = ttk.Button(url_input_frame, text="🔍 Analisar", 
                               command=self.analyze_video, style='Modern.TButton')
        analyze_btn.grid(row=0, column=2)
        
        # Video info frame (initially hidden)
        self.info_frame = ttk.Frame(url_card, style='Modern.TFrame')
        self.info_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        self.info_frame.columnconfigure(1, weight=1)
        
        # Video info labels
        self.title_info = ttk.Label(self.info_frame, text="", style='Modern.TLabel', wraplength=500)
        self.duration_info = ttk.Label(self.info_frame, text="", style='Subtitle.TLabel')
        self.uploader_info = ttk.Label(self.info_frame, text="", style='Subtitle.TLabel')
        
        # Initially hide info
        self.hide_video_info()
    
    def create_settings_section(self, parent):
        """Create settings section"""
        settings_card = ttk.Frame(parent, style='Card.TFrame', padding="20")
        settings_card.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        settings_card.columnconfigure(1, weight=1)
        
        # Settings title
        settings_title = ttk.Label(settings_card, text="⚙️ Configurações de Download", style='Modern.TLabel')
        settings_title.grid(row=0, column=0, columnspan=4, sticky=tk.W, pady=(0, 15))
        
        # Quality selection
        quality_label = ttk.Label(settings_card, text="Qualidade:", style='Modern.TLabel')
        quality_label.grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        
        quality_combo = ttk.Combobox(settings_card, textvariable=self.quality_var,
                                   values=["2160p (4K)", "1440p (2K)", "1080p (Full HD)", 
                                          "720p (HD)", "480p", "360p", "240p", "Apenas Áudio"],
                                   state="readonly", style='Modern.TCombobox', width=15)
        quality_combo.grid(row=1, column=1, sticky=tk.W, padx=(0, 20))
        
        # Format selection
        format_label = ttk.Label(settings_card, text="Formato:", style='Modern.TLabel')
        format_label.grid(row=1, column=2, sticky=tk.W, padx=(0, 10))
        
        format_combo = ttk.Combobox(settings_card, textvariable=self.format_var,
                                  values=["mp4", "webm", "mkv", "mp3", "m4a"],
                                  state="readonly", style='Modern.TCombobox', width=10)
        format_combo.grid(row=1, column=3, sticky=tk.W)
        
        # Download path
        path_label = ttk.Label(settings_card, text="📁 Pasta de Download:", style='Modern.TLabel')
        path_label.grid(row=2, column=0, columnspan=4, sticky=tk.W, pady=(15, 8))
        
        path_frame = ttk.Frame(settings_card, style='Modern.TFrame')
        path_frame.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E))
        path_frame.columnconfigure(0, weight=1)
        
        path_entry = ttk.Entry(path_frame, textvariable=self.path_var, 
                              state='readonly', style='Modern.TEntry')
        path_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        browse_btn = ttk.Button(path_frame, text="📂 Procurar", 
                               command=self.browse_folder, style='Modern.TButton')
        browse_btn.grid(row=0, column=1)
    
    def create_progress_section(self, parent):
        """Create progress section"""
        progress_card = ttk.Frame(parent, style='Card.TFrame', padding="20")
        progress_card.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        progress_card.columnconfigure(0, weight=1)
        
        # Download button
        self.download_btn = ttk.Button(progress_card, text="⬇️ BAIXAR VÍDEO", 
                                     command=self.start_download, style='Modern.TButton')
        self.download_btn.grid(row=0, column=0, pady=(0, 20))
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(progress_card, variable=self.progress_var,
                                          maximum=100, length=500, style='Modern.Horizontal.TProgressbar')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status info frame
        status_frame = ttk.Frame(progress_card, style='Modern.TFrame')
        status_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        status_frame.columnconfigure(0, weight=1)
        status_frame.columnconfigure(2, weight=1)
        
        # Status label
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var, style='Modern.TLabel')
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Speed label
        self.speed_label = ttk.Label(status_frame, textvariable=self.speed_var, style='Subtitle.TLabel')
        self.speed_label.grid(row=0, column=1, padx=(20, 0))
        
        # ETA label
        self.eta_label = ttk.Label(status_frame, textvariable=self.eta_var, style='Subtitle.TLabel')
        self.eta_label.grid(row=0, column=2, sticky=tk.E)
    
    def create_log_section(self, parent):
        """Create log section"""
        log_card = ttk.Frame(parent, style='Card.TFrame', padding="20")
        log_card.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        log_card.columnconfigure(0, weight=1)
        log_card.rowconfigure(1, weight=1)
        parent.rowconfigure(4, weight=1)
        
        # Log title
        log_title = ttk.Label(log_card, text="📋 Log de Download", style='Modern.TLabel')
        log_title.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Log text area with scrollbar
        log_frame = ttk.Frame(log_card, style='Modern.TFrame')
        log_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(log_frame, height=8, wrap=tk.WORD, 
                               bg='#2d2d2d', fg='#ffffff', 
                               font=('Consolas', 9), insertbackground='#ffffff',
                               selectbackground='#0078d4', selectforeground='#ffffff',
                               borderwidth=0, highlightthickness=0)
        
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Log buttons
        log_btn_frame = ttk.Frame(log_card, style='Modern.TFrame')
        log_btn_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        clear_btn = ttk.Button(log_btn_frame, text="🗑️ Limpar Log", 
                              command=self.clear_log, style='Modern.TButton')
        clear_btn.grid(row=0, column=0, sticky=tk.W)
        
        open_folder_btn = ttk.Button(log_btn_frame, text="📂 Abrir Pasta", 
                                   command=self.open_download_folder, style='Modern.TButton')
        open_folder_btn.grid(row=0, column=1, sticky=tk.E, padx=(10, 0))
    
    def create_footer(self, parent):
        """Create footer section"""
        footer_frame = ttk.Frame(parent, style='Modern.TFrame')
        footer_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        footer_frame.columnconfigure(1, weight=1)
        
        # Version info
        version_label = ttk.Label(footer_frame, text="YouTube Downloader Pro v2.0 - Feito com ❤️", 
                                style='Subtitle.TLabel')
        version_label.grid(row=0, column=0, sticky=tk.W)
    
    def paste_url(self):
        """Paste URL from clipboard"""
        try:
            clipboard_content = self.root.clipboard_get()
            self.url_var.set(clipboard_content)
            self.log_message("✅ URL colada da área de transferência")
            self.analyze_video()
        except:
            self.log_message("❌ Nenhuma URL encontrada na área de transferência")
    
    def analyze_video(self):
        """Analyze video information"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Erro", "Por favor, insira uma URL do YouTube")
            return
        
        def analyze():
            try:
                self.update_status("🔍 Analisando vídeo...")
                self.log_message(f"🔍 Analisando: {url}")
                
                ydl_opts = {'quiet': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    
                    title = info.get('title', 'N/A')
                    duration = info.get('duration', 0)
                    uploader = info.get('uploader', 'N/A')
                    
                    # Format duration
                    if duration:
                        minutes, seconds = divmod(duration, 60)
                        duration_str = f"{minutes:02d}:{seconds:02d}"
                    else:
                        duration_str = "N/A"
                    
                    # Update UI
                    self.show_video_info(title, duration_str, uploader)
                    self.log_message(f"✅ Vídeo analisado com sucesso!")
                    self.update_status("✅ Vídeo analisado - Pronto para download")
                    
            except Exception as e:
                self.log_message(f"❌ Erro ao analisar vídeo: {str(e)}")
                self.update_status("❌ Erro na análise")
                self.hide_video_info()
        
        thread = threading.Thread(target=analyze, daemon=True)
        thread.start()
    
    def show_video_info(self, title, duration, uploader):
        """Show video information"""
        self.title_info.configure(text=f"📹 {title}")
        self.duration_info.configure(text=f"⏱️ Duração: {duration}")
        self.uploader_info.configure(text=f"👤 Canal: {uploader}")
        
        self.title_info.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        self.duration_info.grid(row=1, column=0, sticky=tk.W, pady=(0, 2))
        self.uploader_info.grid(row=2, column=0, sticky=tk.W)
    
    def hide_video_info(self):
        """Hide video information"""
        self.title_info.grid_remove()
        self.duration_info.grid_remove()
        self.uploader_info.grid_remove()
    
    def browse_folder(self):
        """Browse for download folder"""
        folder = filedialog.askdirectory(initialdir=self.path_var.get())
        if folder:
            self.path_var.set(folder)
            self.download_path = folder
            self.log_message(f"📁 Pasta alterada para: {folder}")
    
    def get_format_selector(self):
        """Get format selector based on quality and format"""
        quality = self.quality_var.get()
        format_ext = self.format_var.get()
        
        if "Apenas Áudio" in quality:
            if format_ext in ['mp3', 'm4a']:
                return f"bestaudio[ext={format_ext}]/bestaudio"
            return "bestaudio/best"
        
        # Extract resolution
        if "4K" in quality or "2160p" in quality:
            height = "2160"
        elif "2K" in quality or "1440p" in quality:
            height = "1440"
        elif "1080p" in quality:
            height = "1080"
        elif "720p" in quality:
            height = "720"
        elif "480p" in quality:
            height = "480"
        elif "360p" in quality:
            height = "360"
        elif "240p" in quality:
            height = "240"
        else:
            height = "720"
        
        return f"best[height<={height}][ext={format_ext}]/best[height<={height}]/best"
    
    def progress_hook(self, d):
        """Progress hook for yt-dlp"""
        if d['status'] == 'downloading':
            if 'total_bytes' in d and d['total_bytes']:
                percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                self.progress_var.set(percent)
                
                # Speed
                speed = d.get('speed', 0)
                if speed:
                    speed_str = f"🚀 {speed/1024/1024:.1f} MB/s"
                    self.speed_var.set(speed_str)
                
                # ETA
                eta = d.get('eta', 0)
                if eta:
                    eta_str = f"⏱️ {eta}s restantes"
                    self.eta_var.set(eta_str)
                
                self.update_status(f"📥 Baixando... {percent:.1f}%")
                
        elif d['status'] == 'finished':
            self.progress_var.set(100)
            self.update_status("✅ Download concluído!")
            self.speed_var.set("")
            self.eta_var.set("")
            filename = os.path.basename(d['filename'])
            self.log_message(f"✅ Concluído: {filename}")
    
    def download_video(self):
        """Download video"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Erro", "Por favor, insira uma URL do YouTube")
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
            self.update_status("🚀 Iniciando download...")
            self.log_message(f"🚀 Iniciando download: {url}")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # Add to history
            self.add_to_history(url)
            
            self.log_message("🎉 Download concluído com sucesso!")
            messagebox.showinfo("Sucesso", f"Vídeo baixado com sucesso!\n\nSalvo em: {self.download_path}")
            
        except Exception as e:
            error_msg = f"❌ Erro no download: {str(e)}"
            self.log_message(error_msg)
            self.update_status("❌ Falha no download")
            messagebox.showerror("Erro no Download", str(e))
        
        finally:
            self.download_btn.configure(state='normal', text="⬇️ BAIXAR VÍDEO")
            self.progress_var.set(0)
            self.speed_var.set("")
            self.eta_var.set("")
    
    def start_download(self):
        """Start download in separate thread"""
        self.download_btn.configure(state='disabled', text="⏳ Baixando...")
        self.progress_var.set(0)
        
        thread = threading.Thread(target=self.download_video, daemon=True)
        thread.start()
    
    def clear_log(self):
        """Clear log text"""
        self.log_text.delete(1.0, tk.END)
    
    def open_download_folder(self):
        """Open download folder"""
        if os.path.exists(self.download_path):
            os.startfile(self.download_path)
        else:
            messagebox.showwarning("Pasta Não Encontrada", 
                                 f"Pasta de download não existe: {self.download_path}")
    
    def log_message(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_status(self, message):
        """Update status message"""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def add_to_history(self, url):
        """Add URL to download history"""
        self.download_history.append({
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'path': self.download_path
        })
        self.save_settings()
    
    def load_settings(self):
        """Load settings from file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.download_path = settings.get('download_path', self.download_path)
                    self.path_var.set(self.download_path)
                    self.quality_var.set(settings.get('quality', '720p (HD)'))
                    self.format_var.set(settings.get('format', 'mp4'))
                    self.download_history = settings.get('history', [])
        except:
            pass
    
    def save_settings(self):
        """Save settings to file"""
        try:
            settings = {
                'download_path': self.download_path,
                'quality': self.quality_var.get(),
                'format': self.format_var.get(),
                'history': self.download_history[-50:]  # Keep last 50 downloads
            }
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
        except:
            pass

def main():
    root = tk.Tk()
    app = ModernYouTubeDownloader(root)
    
    # Save settings on close
    def on_closing():
        app.save_settings()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main() 