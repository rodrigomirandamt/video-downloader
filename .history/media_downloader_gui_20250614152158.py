#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MediaSlayer - Downloader Universal de Vídeos
Interface baseada no design da imagem fornecida
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import yt_dlp
import os
import re
from pathlib import Path
import sys

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
        self.root.geometry("600x700")
        self.root.minsize(500, 600)
        # Cor de fundo escura como na imagem
        self.root.configure(bg='#2d3748')
        
        # Centralizar janela
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
    
    def setup_variables(self):
        """Inicializar variáveis"""
        self.url_var = tk.StringVar()
        self.format_var = tk.StringVar(value="MP4 (Video Scroll)")
        self.quality_var = tk.StringVar(value="720p (Epic)")
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Ready for download")
        
        # Pasta padrão
        self.download_path = os.path.join(os.getcwd(), "downloads")
        
        # Controle de análise
        self.last_analyzed_url = ""
        self.video_info = None
        self.is_downloading = False
    
    def setup_styles(self):
        """Configurar estilos para combinar com a imagem"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Cores baseadas na imagem
        colors = {
            'bg': '#2d3748',           # Fundo principal
            'card_bg': '#4a5568',      # Fundo do card
            'input_bg': '#2d3748',     # Fundo dos inputs
            'button_bg': '#e53e3e',    # Vermelho do botão
            'button_hover': '#c53030', # Vermelho mais escuro
            'text': '#ffffff',         # Texto branco
            'text_secondary': '#a0aec0', # Texto secundário
            'border': '#4a5568'        # Bordas
        }
        
        # Frame styles
        self.style.configure('Dark.TFrame', background=colors['bg'])
        self.style.configure('Card.TFrame', 
                           background=colors['card_bg'], 
                           relief='solid', 
                           borderwidth=1,
                           bordercolor=colors['border'])
        
        # Label styles
        self.style.configure('Dark.TLabel', 
                           background=colors['bg'], 
                           foreground=colors['text'], 
                           font=('Segoe UI', 10))
        
        self.style.configure('Card.TLabel', 
                           background=colors['card_bg'], 
                           foreground=colors['text'], 
                           font=('Segoe UI', 10))
        
        self.style.configure('Title.TLabel', 
                           background=colors['card_bg'], 
                           foreground=colors['text'], 
                           font=('Segoe UI', 18, 'bold'))
        
        self.style.configure('Subtitle.TLabel', 
                           background=colors['card_bg'], 
                           foreground=colors['text_secondary'], 
                           font=('Segoe UI', 10))
        
        self.style.configure('FieldLabel.TLabel', 
                           background=colors['card_bg'], 
                           foreground=colors['text_secondary'], 
                           font=('Segoe UI', 9))
        
        # Entry style
        self.style.configure('Dark.TEntry',
                           fieldbackground=colors['input_bg'],
                           foreground=colors['text'],
                           borderwidth=1,
                           insertcolor=colors['text'],
                           font=('Segoe UI', 11))
        
        # Combobox style
        self.style.configure('Dark.TCombobox',
                           fieldbackground=colors['input_bg'],
                           foreground=colors['text'],
                           borderwidth=1,
                           font=('Segoe UI', 10))
        
        # Button style - vermelho como na imagem
        self.style.configure('Quest.TButton', 
                           background=colors['button_bg'], 
                           foreground=colors['text'],
                           borderwidth=0,
                           font=('Segoe UI', 12, 'bold'),
                           padding=(20, 12))
        
        self.style.map('Quest.TButton',
                      background=[('active', colors['button_hover'])])
        
        # Progress bar
        self.style.configure('Quest.Horizontal.TProgressbar',
                           background=colors['button_bg'],
                           troughcolor=colors['input_bg'],
                           borderwidth=0)
    
    def create_ui(self):
        """Criar interface idêntica à imagem"""
        # Container principal com fundo escuro
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=60)
        
        # Ícone de download centralizado (círculo vermelho)
        icon_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        icon_frame.pack(pady=(0, 20))
        
        # Simular o ícone circular vermelho com um canvas
        icon_canvas = tk.Canvas(icon_frame, width=60, height=60, 
                               bg='#2d3748', highlightthickness=0)
        icon_canvas.pack()
        
        # Desenhar círculo vermelho
        icon_canvas.create_oval(10, 10, 50, 50, fill='#e53e3e', outline='#e53e3e')
        # Desenhar seta de download (simplificada)
        icon_canvas.create_polygon(30, 20, 25, 30, 35, 30, fill='white')
        icon_canvas.create_rectangle(28, 30, 32, 40, fill='white', outline='white')
        
        # Card principal
        card_frame = ttk.Frame(main_frame, style='Card.TFrame', padding="30")
        card_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título "Begin Your Quest"
        title_label = ttk.Label(card_frame, text="Begin Your Quest", style='Title.TLabel')
        title_label.pack(pady=(0, 5))
        
        # Subtítulo
        subtitle_label = ttk.Label(card_frame, 
                                  text="Enter the URL of your target media and select your preferred enchantment",
                                  style='Subtitle.TLabel')
        subtitle_label.pack(pady=(0, 25))
        
        # Campo Target URL
        url_frame = ttk.Frame(card_frame, style='Card.TFrame')
        url_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Label com ícone de raio
        url_label_frame = ttk.Frame(url_frame, style='Card.TFrame')
        url_label_frame.pack(fill=tk.X, pady=(0, 8))
        
        url_label = ttk.Label(url_label_frame, text="⚡ Target URL", style='FieldLabel.TLabel')
        url_label.pack(side=tk.LEFT)
        
        # Campo de entrada da URL
        self.url_entry = ttk.Entry(url_frame, textvariable=self.url_var, 
                                  style='Dark.TEntry', font=('Segoe UI', 11))
        self.url_entry.pack(fill=tk.X, ipady=8)
        self.url_entry.bind('<KeyRelease>', self.on_url_change)
        
        # Configurar placeholder
        self.url_entry.insert(0, "https://youtube.com/watch?v=... or https://x.com/...")
        self.url_entry.bind('<FocusIn>', self.on_entry_focus_in)
        self.url_entry.bind('<FocusOut>', self.on_entry_focus_out)
        self.url_entry.configure(foreground='#a0aec0')
        
        # Container para os dois dropdowns
        dropdowns_frame = ttk.Frame(card_frame, style='Card.TFrame')
        dropdowns_frame.pack(fill=tk.X, pady=(0, 25))
        dropdowns_frame.columnconfigure(0, weight=1)
        dropdowns_frame.columnconfigure(1, weight=1)
        
        # Format Enchantment
        format_frame = ttk.Frame(dropdowns_frame, style='Card.TFrame')
        format_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        format_label_frame = ttk.Frame(format_frame, style='Card.TFrame')
        format_label_frame.pack(fill=tk.X, pady=(0, 8))
        
        format_label = ttk.Label(format_label_frame, text="💎 Format Enchantment", style='FieldLabel.TLabel')
        format_label.pack(side=tk.LEFT)
        
        self.format_combo = ttk.Combobox(format_frame, textvariable=self.format_var,
                                        values=["⚔️ MP4 (Video Scroll)", "🎵 MP3 (Audio Rune)", 
                                               "🛡️ WebM (Web Armor)", "🔮 WAV (Crystal Audio)"],
                                        state="readonly", style='Dark.TCombobox')
        self.format_combo.pack(fill=tk.X, ipady=6)
        
        # Quality Level
        quality_frame = ttk.Frame(dropdowns_frame, style='Card.TFrame')
        quality_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        quality_label_frame = ttk.Frame(quality_frame, style='Card.TFrame')
        quality_label_frame.pack(fill=tk.X, pady=(0, 8))
        
        quality_label = ttk.Label(quality_label_frame, text="👑 Quality Level", style='FieldLabel.TLabel')
        quality_label.pack(side=tk.LEFT)
        
        self.quality_combo = ttk.Combobox(quality_frame, textvariable=self.quality_var,
                                         values=["👑 1080p (Legendary)", "⭐ 720p (Epic)", 
                                                "🔸 480p (Rare)", "⚪ 360p (Common)"],
                                         state="readonly", style='Dark.TCombobox')
        self.quality_combo.pack(fill=tk.X, ipady=6)
        
        # Área de progresso (inicialmente oculta)
        self.progress_frame = ttk.Frame(card_frame, style='Card.TFrame')
        
        self.status_label = ttk.Label(self.progress_frame, textvariable=self.status_var, 
                                     style='FieldLabel.TLabel')
        self.status_label.pack(pady=(0, 5))
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, variable=self.progress_var,
                                           maximum=100, style='Quest.Horizontal.TProgressbar')
        self.progress_bar.pack(fill=tk.X, ipady=3)
        
        # Botão "Execute Download Quest"
        self.download_btn = ttk.Button(card_frame, text="⚔️ Execute Download Quest", 
                                      command=self.start_download, style='Quest.TButton')
        self.download_btn.pack(fill=tk.X, pady=(15, 0), ipady=5)
    
    def on_entry_focus_in(self, event):
        """Remover placeholder quando focar no campo"""
        if self.url_var.get() == "https://youtube.com/watch?v=... or https://x.com/...":
            self.url_var.set("")
            self.url_entry.configure(foreground='#ffffff')
    
    def on_entry_focus_out(self, event):
        """Adicionar placeholder se campo estiver vazio"""
        if not self.url_var.get():
            self.url_var.set("https://youtube.com/watch?v=... or https://x.com/...")
            self.url_entry.configure(foreground='#a0aec0')
    
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
        if url and url != "https://youtube.com/watch?v=... or https://x.com/...":
            # Analisar automaticamente após 1 segundo de inatividade
            self.root.after(1000, lambda: self.analyze_url_automatically(url))
    
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
                self.update_status("🔍 Analyzing video...")
                
                with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    
                    title = info.get('title', 'N/A')
                    self.video_info = info
                    
                    self.update_status(f"✅ Found: {title[:50]}...")
                    
            except Exception as e:
                self.update_status("❌ Error analyzing URL")
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def get_format_options(self):
        """Obter opções de formato"""
        format_text = self.format_var.get()
        quality_text = self.quality_var.get()
        
        # Extrair formato
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
        
        # Extrair qualidade
        if "1080p" in quality_text:
            return f"best[height<=1080][ext={format_type}]"
        elif "720p" in quality_text:
            return f"best[height<=720][ext={format_type}]"
        elif "480p" in quality_text:
            return f"best[height<=480][ext={format_type}]"
        elif "360p" in quality_text:
            return f"best[height<=360][ext={format_type}]"
        else:
            return "best"
    
    def progress_hook(self, d):
        """Hook de progresso"""
        if d['status'] == 'downloading':
            if 'total_bytes' in d and d['total_bytes']:
                percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                self.progress_var.set(percent)
                self.update_status(f"⬇️ Downloading... {percent:.1f}%")
            elif '_percent_str' in d:
                try:
                    percent_str = d['_percent_str'].strip('%')
                    percent = float(percent_str)
                    self.progress_var.set(percent)
                    self.update_status(f"⬇️ Downloading... {percent:.1f}%")
                except:
                    pass
        elif d['status'] == 'finished':
            self.progress_var.set(100)
            self.update_status("✅ Download completed!")
    
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
        
        # Criar pasta
        os.makedirs(self.download_path, exist_ok=True)
        
        # Mostrar área de progresso
        self.progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Configurar yt-dlp
        ydl_opts = {
            'outtmpl': os.path.join(self.download_path, '%(uploader)s - %(title)s.%(ext)s'),
            'format': self.get_format_options(),
            'progress_hooks': [self.progress_hook],
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            self.update_status("🚀 Starting download...")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            messagebox.showinfo("Success", "✅ Download completed successfully!")
            self.update_status("Ready for next download")
            
        except Exception as e:
            error_msg = f"❌ Download failed: {str(e)}"
            messagebox.showerror("Error", error_msg)
            self.update_status("Download failed")
        finally:
            self.progress_var.set(0)
            self.download_btn.config(state='normal', text="⚔️ Execute Download Quest")
            self.is_downloading = False
            # Ocultar área de progresso após 3 segundos
            self.root.after(3000, lambda: self.progress_frame.pack_forget())
    
    def start_download(self):
        """Iniciar download"""
        if self.is_downloading:
            return
            
        self.is_downloading = True
        self.download_btn.config(state='disabled', text="🔄 Casting Spell...")
        threading.Thread(target=self.download_media, daemon=True).start()
    
    def update_status(self, message):
        """Atualizar status"""
        self.status_var.set(message)
        self.root.update_idletasks()

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