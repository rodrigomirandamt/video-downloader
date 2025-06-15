#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MediaSlayer - Interface o mais próxima possível do design React
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import yt_dlp
import os
import re
import signal
import time

class MediaSlayerGUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_variables()
        self.setup_styles()
        self.create_ui()
        
    def setup_window(self):
        """Configurar janela principal"""
        self.root.title("MediaSlayer")
        # Tamanho dinâmico: ocupa até 85% da tela, mas nunca ultrapassa o layout original (750x650)
        screen_w, screen_h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        win_w = min(750, int(screen_w * 0.85))
        win_h = min(650, int(screen_h * 0.85))

        # Guardar para usar em outros componentes (ex.: gradiente)
        self.window_width = win_w
        self.window_height = win_h

        self.root.geometry(f"{win_w}x{win_h}")
        # Limitar redimensionamento mínimo a 80 % destes valores
        self.root.minsize(int(win_w * 0.8), int(win_h * 0.8))
        # Gradiente de fundo simulado (slate-900 to slate-800)
        self.root.configure(bg='#0f172a')
        
        # Centralizar janela
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
    
    def setup_variables(self):
        """Inicializar variáveis"""
        self.url_var = tk.StringVar()
        self.format_var = tk.StringVar(value="mp4")
        self.quality_var = tk.StringVar(value="720p")
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="")
        
        self.download_path = os.path.join(os.getcwd(), "downloads")
        self.last_analyzed_url = ""
        self.video_info = None
        self.is_downloading = False
        self.platform = None
        self.cancel_requested = False
        self.logger = None
    
    def setup_styles(self):
        """Configurar estilos para combinar com o React"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Cores exatas do Tailwind CSS
        colors = {
            'slate_900': '#0f172a',
            'slate_800': '#1e293b', 
            'slate_700': '#334155',
            'slate_600': '#475569',
            'white': '#ffffff',
            'gray_300': '#d1d5db',
            'gray_400': '#9ca3af',
            'red_600': '#dc2626',
            'red_700': '#b91c1c',
            'red_400': '#f87171',
            'red_300': '#fca5a5',
            'orange_400': '#fb923c',
            'yellow_400': '#facc15',
            'blue_600': '#2563eb',
            'blue_700': '#1d4ed8',
            'purple_400': '#a78bfa',
            'green_400': '#4ade80',
            'red_500_30': '#ef444430'  # red-500/30
        }
        
        # Frame principal
        self.style.configure('Main.TFrame', background=colors['slate_900'])
        
        # Card translúcido (simulando backdrop-blur)
        self.style.configure('Card.TFrame', 
                           background=colors['slate_800'], 
                           relief='flat',
                           borderwidth=1)
        
        # Labels - Fontes reduzidas para interface mais compacta
        self.style.configure('Title.TLabel', 
                           background=colors['slate_900'], 
                           foreground=colors['white'], 
                           font=('Segoe UI', 24, 'bold'))  # Reduzido de 32 para 24
        
        self.style.configure('Subtitle.TLabel', 
                           background=colors['slate_900'], 
                           foreground=colors['gray_300'], 
                           font=('Segoe UI', 12))  # Reduzido de 14 para 12
        
        self.style.configure('CardTitle.TLabel', 
                           background=colors['slate_800'], 
                           foreground=colors['white'], 
                           font=('Segoe UI', 16, 'bold'))  # Reduzido de 18 para 16
        
        self.style.configure('CardDesc.TLabel', 
                           background=colors['slate_800'], 
                           foreground=colors['gray_400'], 
                           font=('Segoe UI', 10))  # Reduzido de 11 para 10
        
        self.style.configure('FieldLabel.TLabel', 
                           background=colors['slate_800'], 
                           foreground=colors['gray_300'], 
                           font=('Segoe UI', 9, 'bold'))
        
        # Entry com estilo React - Fonte reduzida
        self.style.configure('Modern.TEntry',
                           fieldbackground=colors['slate_700'],
                           foreground=colors['white'],
                           borderwidth=1,
                           insertcolor=colors['white'],
                           font=('Segoe UI', 11))  # Reduzido de 12 para 11
        
        # Combobox - Fonte reduzida
        self.style.configure('Modern.TCombobox',
                           fieldbackground='#000000',  # black
                           foreground=colors['white'],
                           borderwidth=1,
                           font=('Segoe UI', 10))  # Reduzido de 11 para 10
        # White arrow
        self.style.map('Modern.TCombobox', fieldbackground=[('readonly', '#000000')], foreground=[('readonly', colors['white'])])
        
        # Botão com gradiente vermelho - Padding reduzido
        self.style.configure('RedGradient.TButton', 
                           background=colors['red_600'], 
                           foreground=colors['white'],
                           borderwidth=0,
                           font=('Segoe UI', 11, 'bold'),  # Reduzido de 12 para 11
                           padding=(15, 10))  # Reduzido de (20, 14) para (15, 10)
        
        self.style.map('RedGradient.TButton',
                      background=[('active', colors['red_700']),
                                ('pressed', colors['red_700'])])
        
        # Progress bar
        self.style.configure('Modern.Horizontal.TProgressbar',
                           background=colors['red_600'],
                           troughcolor=colors['slate_700'],
                           borderwidth=0)
    
    def create_gradient_frame(self, parent, color1, color2, width, height):
        """Simular gradiente com Canvas"""
        canvas = tk.Canvas(parent, width=width, height=height, highlightthickness=0)
        
        # Criar gradiente vertical
        for i in range(height):
            ratio = i / height
            # Interpolação simples entre as cores
            r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
            r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
            
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            
            color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_line(0, i, width, i, fill=color)
        
        return canvas
    
    def create_ui(self):
        """Criar interface idêntica ao React"""
        # Container principal com gradiente
        main_frame = ttk.Frame(self.root, style='Main.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Simular gradiente de fundo usando as dimensões calculadas da janela
        gradient_canvas = self.create_gradient_frame(
            main_frame, '#0f172a', '#1e293b', self.window_width, self.window_height
        )
        gradient_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Container centralizado
        center_frame = ttk.Frame(main_frame, style='Main.TFrame')
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Título principal simples e compacto
        # Card principal - Padding reduzido
        
        # Card principal - Padding reduzido
        card_frame = ttk.Frame(center_frame, style='Card.TFrame', padding="30")  # Reduzido de 40 para 30
        card_frame.pack(pady=(20, 0))  # Reduzido de 30 para 20
        
        # Header do card - versão compacta
        card_header = ttk.Frame(card_frame, style='Card.TFrame')
        card_header.pack(fill=tk.X, pady=(0, 10))  # Altura reduzida

        # Título único
        card_title = ttk.Label(card_header, text="Download Media", style='CardTitle.TLabel')
        card_title.pack()
        
        # Conteúdo do card
        card_content = ttk.Frame(card_frame, style='Card.TFrame')
        card_content.pack(fill=tk.BOTH, expand=True)
        
        # URL Input - Espaçamentos reduzidos
        url_section = ttk.Frame(card_content, style='Card.TFrame')
        url_section.pack(fill=tk.X, pady=(0, 18))  # Reduzido de 25 para 18
        
        # Label com ícone
        url_label_frame = ttk.Frame(url_section, style='Card.TFrame')
        url_label_frame.pack(fill=tk.X, pady=(0, 8))  # Reduzido de 10 para 8
        
        url_label = ttk.Label(url_label_frame, text="⚡ Target URL", style='FieldLabel.TLabel')
        url_label.pack(side=tk.LEFT)
        
        # Container para input com ícone
        url_input_frame = ttk.Frame(url_section, style='Card.TFrame')
        url_input_frame.pack(fill=tk.X)
        
        self.url_entry = ttk.Entry(url_input_frame, textvariable=self.url_var, 
                                  style='Modern.TEntry', font=('Segoe UI', 11))  # Fonte reduzida de 12 para 11
        self.url_entry.pack(fill=tk.X, ipady=10)  # Reduzido de 12 para 10
        self.url_entry.bind('<KeyRelease>', self.on_url_change)
        
        # Placeholder
        self.url_entry.insert(0, "https://youtube.com/watch?v=... or https://x.com/...")
        self.url_entry.bind('<FocusIn>', self.on_entry_focus_in)
        self.url_entry.bind('<FocusOut>', self.on_entry_focus_out)
        self.url_entry.configure(foreground='#9ca3af')
        
        # Badge de plataforma detectada
        self.platform_frame = ttk.Frame(url_section, style='Card.TFrame')
        self.platform_label = ttk.Label(self.platform_frame, text="", 
                                       background='#dc2626', foreground='white',
                                       font=('Segoe UI', 9, 'bold'), padding=(10, 5))
        
        # Dropdowns - Espaçamentos reduzidos
        dropdowns_frame = ttk.Frame(card_content, style='Card.TFrame')
        dropdowns_frame.pack(fill=tk.X, pady=(0, 18))  # Reduzido de 25 para 18
        dropdowns_frame.columnconfigure(0, weight=1)
        dropdowns_frame.columnconfigure(1, weight=1)
        
        # Format Enchantment
        format_frame = ttk.Frame(dropdowns_frame, style='Card.TFrame')
        format_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 12))  # Reduzido de 15 para 12
        
        format_label = ttk.Label(format_frame, text="💎 Format Enchantment", style='FieldLabel.TLabel')
        format_label.pack(anchor=tk.W, pady=(0, 8))  # Reduzido de 10 para 8
        
        self.format_combo = ttk.Combobox(format_frame, textvariable=self.format_var,
                                        values=["⚔️ MP4 (Video Scroll)", "🎵 MP3 (Audio Rune)", 
                                               "🛡️ WebM (Web Armor)", "🔮 WAV (Crystal Audio)"],
                                        state="readonly", style='Modern.TCombobox')
        self.format_combo.pack(fill=tk.X, ipady=6)  # Reduzido de 8 para 6
        self.format_combo.set("⚔️ MP4 (Video Scroll)")
        
        # Quality Level
        quality_frame = ttk.Frame(dropdowns_frame, style='Card.TFrame')
        quality_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(12, 0))  # Reduzido de 15 para 12
        
        quality_label = ttk.Label(quality_frame, text="👑 Quality Level", style='FieldLabel.TLabel')
        quality_label.pack(anchor=tk.W, pady=(0, 8))  # Reduzido de 10 para 8
        
        self.quality_combo = ttk.Combobox(quality_frame, textvariable=self.quality_var,
                                         values=["👑 1080p (Legendary)", "⭐ 720p (Epic)", 
                                                "🔸 480p (Rare)", "⚪ 360p (Common)"],
                                         state="readonly", style='Modern.TCombobox')
        self.quality_combo.pack(fill=tk.X, ipady=6)  # Reduzido de 8 para 6
        self.quality_combo.set("⭐ 720p (Epic)")
        
        # Progress Bar (inicialmente oculta)
        self.progress_frame = ttk.Frame(card_content, style='Card.TFrame')
        
        self.progress_status = ttk.Label(self.progress_frame, text="Casting download spell...", 
                                       style='FieldLabel.TLabel')
        self.progress_status.pack(side=tk.LEFT)
        
        self.progress_percent = ttk.Label(self.progress_frame, text="0%", 
                                        style='FieldLabel.TLabel', foreground='#f87171')
        self.progress_percent.pack(side=tk.RIGHT)
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, variable=self.progress_var,
                                           maximum=100, style='Modern.Horizontal.TProgressbar')
        self.progress_bar.pack(fill=tk.X, pady=(10, 0), ipady=2)
        
        # NEW: Scrolling text area for logs
        self.log_text = scrolledtext.ScrolledText(card_content, width=80, height=8,
                                                  background='#1e293b', foreground='#d1d5db',
                                                  font=('Consolas', 9), state='disabled', wrap='word',
                                                  borderwidth=1, relief='solid')
        self.log_text.pack(fill=tk.BOTH, pady=(10, 0))
        
        # Container para botões
        button_frame = ttk.Frame(card_content, style='Card.TFrame')
        button_frame.pack(fill=tk.X, pady=(18, 0))
        
        # Botão de download - Espaçamento reduzido
        self.download_btn = ttk.Button(button_frame, text="⚔️ Execute Download Quest", 
                                      command=self.start_download, style='RedGradient.TButton')
        self.download_btn.pack(fill=tk.X, ipady=6)
        
        # Botão de cancelar (inicialmente oculto)
        self.cancel_btn = ttk.Button(button_frame, text="❌ Cancel Quest", 
                                    command=self.cancel_download, style='RedGradient.TButton')
        self.cancel_btn.pack_forget()

        # --- Download Location Section ---
        path_section = ttk.Frame(card_content, style='Card.TFrame')
        path_section.pack(fill=tk.X, pady=(0, 18))

        path_label = ttk.Label(path_section, text="📂 Download Location", style='FieldLabel.TLabel')
        path_label.pack(anchor=tk.W, pady=(0, 8))

        path_inner = ttk.Frame(path_section, style='Card.TFrame')
        path_inner.pack(fill=tk.X)

        self.download_path_var = tk.StringVar(value=self.download_path)
        self.path_entry = ttk.Entry(path_inner, textvariable=self.download_path_var,
                                   style='Modern.TEntry', font=('Segoe UI', 10))
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6)

        browse_btn = ttk.Button(path_inner, text="Browse", command=self.browse_path,
                                style='RedGradient.TButton')
        browse_btn.pack(side=tk.LEFT, padx=(8,0))
    
    def on_entry_focus_in(self, event):
        """Remover placeholder"""
        if self.url_var.get() == "https://youtube.com/watch?v=... or https://x.com/...":
            self.url_var.set("")
            self.url_entry.configure(foreground='#ffffff')
    
    def on_entry_focus_out(self, event):
        """Adicionar placeholder"""
        if not self.url_var.get():
            self.url_var.set("https://youtube.com/watch?v=... or https://x.com/...")
            self.url_entry.configure(foreground='#9ca3af')
    
    def detect_platform(self, url):
        """Detectar plataforma"""
        if not url or url == "https://youtube.com/watch?v=... or https://x.com/...":
            return None
        if re.search(r'(youtube\.com|youtu\.be)', url):
            return "youtube"
        elif re.search(r'(twitter\.com|x\.com|t\.co)', url):
            return "twitter"
        return None
    
    def on_url_change(self, event=None):
        """Callback quando URL muda"""
        url = self.url_var.get().strip()
        platform = self.detect_platform(url)
        
        if platform:
            # Mostrar badge da plataforma
            self.platform_frame.pack(pady=(10, 0))
            if platform == "youtube":
                self.platform_label.config(text="⚔️ YouTube realm detected", background='#dc2626')
            else:
                self.platform_label.config(text="⚔️ X (Twitter) realm detected", background='#2563eb')
            self.platform_label.pack()
            self.platform = platform
            
            # Analisar automaticamente
            if url != self.last_analyzed_url:
                self.root.after(1000, lambda: self.analyze_url_automatically(url))
        else:
            self.platform_frame.pack_forget()
            self.platform = None
    
    def analyze_url_automatically(self, url):
        """Analisar URL automaticamente"""
        if not url or url == self.last_analyzed_url or url == "https://youtube.com/watch?v=... or https://x.com/...":
            return
            
        self.last_analyzed_url = url
        platform = self.detect_platform(url)
        
        if not platform:
            return
        
        def analyze():
            try:
                with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    self.video_info = info
                    
            except Exception as e:
                pass
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def get_format_options(self):
        """Obter opções de formato"""
        format_text = self.format_var.get()
        quality_text = self.quality_var.get()
        
        if "MP4" in format_text:
            format_type = "mp4"
        elif "MP3" in format_text:
            return "bestaudio/best"
        elif "WebM" in format_text:
            format_type = "webm"
        elif "WAV" in format_text:
            return "bestaudio[ext=wav]/bestaudio"
        else:
            format_type = "mp4"
        
        if "1080p" in quality_text:
            return f"best[height<=1080]"
        elif "720p" in quality_text:
            return f"best[height<=720]"
        elif "480p" in quality_text:
            return f"best[height<=480]"
        elif "360p" in quality_text:
            return f"best[height<=360]"
        else:
            return "best"
    
    def update_progress(self, percent, finished=False):
        """Update progress bar in main thread"""
        def _update():
            self.progress_var.set(percent)
            self.progress_percent.config(text=f"{percent:.0f}%")
            if finished:
                self.progress_status.config(text="Quest completed! Media successfully captured!")
        self.root.after(0, _update)
    
    def progress_hook(self, d):
        """Hook de progresso (thread-safe)"""
        if d['status'] == 'downloading':
            percent = None
            if 'total_bytes' in d and d['total_bytes']:
                percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
            elif '_percent_str' in d:
                try:
                    percent_str = d['_percent_str'].strip('%')
                    percent = float(percent_str)
                except:
                    pass
            if percent is not None:
                self.update_progress(percent)
        elif d['status'] == 'finished':
            self.update_progress(100, finished=True)
    
    def download_media(self):
        """Baixar mídia"""
        url = self.url_var.get().strip()
        if not url or url == "https://youtube.com/watch?v=... or https://x.com/...":
            messagebox.showerror("Error", "Please enter a valid URL")
            return
        
        platform = self.detect_platform(url)
        if not platform:
            messagebox.showerror("Error", "Invalid URL! Please use a YouTube or X (Twitter) URL")
            return
        
        # Update download path from UI
        self.download_path = self.download_path_var.get() or self.download_path
        os.makedirs(self.download_path, exist_ok=True)
        
        # Mostrar progresso
        self.progress_frame.pack(fill=tk.X, pady=(0, 25))
        
        ydl_opts = {
            'outtmpl': os.path.join(self.download_path, '%(uploader)s - %(title)s.%(ext)s'),
            'format': self.get_format_options(),
            'progress_hooks': [self.progress_hook],
            'quiet': False,  # Enable verbose output for debugging
            'no_warnings': False,  # Show warnings for debugging
            'socket_timeout': 30,  # Add timeout to prevent hanging
            'retries': 3,  # Retry failed downloads
            'logger': self.logger if self.logger else None  # NEW
        }
        
        # Add Twitter/X specific options
        if platform == "twitter":
            ydl_opts.update({
                'extractor_args': {
                    'twitter': {
                        'api': ['syndication', 'legacy', 'graphql']  # Try multiple APIs
                    }
                }
            })
        
        try:
            if self.cancel_requested:
                return
                
            self.progress_status.config(text="Casting download spell...")
            self.root.update()  # Force UI update
            self.add_log("Starting analysis of target URL...")  # NEW
            
            if self.cancel_requested:
                return
            
            # First, try to extract info to validate URL
            self.progress_status.config(text="Analyzing target...")
            self.root.update()
            
            with yt_dlp.YoutubeDL({**ydl_opts, 'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                if not info:
                    raise Exception("Could not extract video information")
            
            if self.cancel_requested:
                return
            
            # If info extraction succeeds, proceed with download
            self.progress_status.config(text="Casting download spell...")
            self.root.update()
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            if not self.cancel_requested:
                messagebox.showinfo("Success", "✅ Quest completed! Media successfully captured and added to your inventory!")
                self.add_log("Download completed successfully!")  # NEW
            
        except Exception as e:
            error_msg = f"❌ Quest failed! The download spell was interrupted: {str(e)}"
            print(f"Download error: {e}")  # Print to console for debugging
            self.add_log(f"ERROR: {e}")  # NEW
            messagebox.showerror("Error", error_msg)
        finally:
            self.progress_var.set(0)
            self.download_btn.config(state='normal', text="⚔️ Execute Download Quest")
            self.is_downloading = False
            self.root.after(3000, lambda: self.progress_frame.pack_forget())
    
    def cancel_download(self):
        """Cancel ongoing download"""
        self.cancel_requested = True
        self.progress_status.config(text="Cancelling quest...")
        
    def download_with_timeout(self):
        """Download with timeout mechanism"""
        self.download_result = None
        self.download_error = None
        self.cancel_requested = False
        
        def download_worker():
            try:
                self.download_media()
                self.download_result = "success"
            except Exception as e:
                self.download_error = str(e)
        
        # Start download in separate thread
        download_thread = threading.Thread(target=download_worker, daemon=True)
        download_thread.start()
        
        # Monitor progress with timeout (5 minutes)
        timeout = 300  # 5 minutes
        start_time = time.time()
        
        while download_thread.is_alive():
            if self.cancel_requested:
                # User cancelled
                self.progress_status.config(text="Quest cancelled by user!")
                break
            elif time.time() - start_time > timeout:
                # Timeout reached
                self.progress_status.config(text="Download timeout - Quest abandoned!")
                messagebox.showerror("Timeout", "❌ Download timed out after 5 minutes. The spell may have been blocked by the realm's defenses.")
                break
            
            # Update UI and wait
            self.root.update()
            time.sleep(0.1)
        
        # Reset UI state
        self.progress_var.set(0)
        self.download_btn.config(state='normal', text="⚔️ Execute Download Quest")
        self.download_btn.pack(fill=tk.X, ipady=6)
        self.cancel_btn.pack_forget()
        self.is_downloading = False
        self.root.after(3000, lambda: self.progress_frame.pack_forget())

    def start_download(self):
        """Iniciar download"""
        if self.is_downloading:
            return
            
        self.is_downloading = True
        self.download_btn.config(state='disabled', text="🔄 Casting Spell...")
        self.download_btn.pack_forget()
        self.cancel_btn.pack(fill=tk.X, ipady=6)
        # NEW: reset log and initialize logger
        self.log_text.configure(state='normal')
        self.log_text.delete('1.0', tk.END)
        self.log_text.configure(state='disabled')
        self.logger = self.YTDLogger(self.add_log)
        threading.Thread(target=self.download_with_timeout, daemon=True).start()

    def add_log(self, message):
        """Thread-safe append to log box"""
        def _append():
            self.log_text.configure(state='normal')
            self.log_text.insert(tk.END, message + "\n")
            self.log_text.yview(tk.END)
            self.log_text.configure(state='disabled')

        self.root.after(0, _append)

    def browse_path(self):
        """Open a folder selection dialog and update download path"""
        from tkinter import filedialog
        selected = filedialog.askdirectory(initialdir=self.download_path_var.get() or os.getcwd())
        if selected:
            self.download_path_var.set(selected)
            self.download_path = selected

    class YTDLogger:
        """Custom logger for yt-dlp that writes to GUI log"""
        def __init__(self, callback):
            self._callback = callback
        def debug(self, msg):
            self._callback(msg)
        def info(self, msg):
            self._callback(msg)
        def warning(self, msg):
            self._callback(f"WARNING: {msg}")
        def error(self, msg):
            self._callback(f"ERROR: {msg}")

def main():
    """Função principal"""
    root = tk.Tk()
    app = MediaSlayerGUI(root)
    
    def on_closing():
        root.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main() 