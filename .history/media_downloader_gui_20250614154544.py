#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MediaSlayer - Interface o mais próxima possível do design React
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import yt_dlp
import os
import re

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
        self.root.geometry("750x650")  # Reduzido de 800x900 para 750x650
        self.root.minsize(650, 550)    # Reduzido de 700x800 para 650x550
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
        
        # Entry com estilo React
        self.style.configure('Modern.TEntry',
                           fieldbackground=colors['slate_700'],
                           foreground=colors['white'],
                           borderwidth=1,
                           insertcolor=colors['white'],
                           font=('Segoe UI', 12))
        
        # Combobox
        self.style.configure('Modern.TCombobox',
                           fieldbackground=colors['slate_700'],
                           foreground=colors['white'],
                           borderwidth=1,
                           font=('Segoe UI', 11))
        
        # Botão com gradiente vermelho
        self.style.configure('RedGradient.TButton', 
                           background=colors['red_600'], 
                           foreground=colors['white'],
                           borderwidth=0,
                           font=('Segoe UI', 12, 'bold'),
                           padding=(20, 14))
        
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
        
        # Simular gradiente de fundo
        gradient_canvas = self.create_gradient_frame(main_frame, '#0f172a', '#1e293b', 800, 900)
        gradient_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Container centralizado
        center_frame = ttk.Frame(main_frame, style='Main.TFrame')
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Título principal com ícones
        title_container = ttk.Frame(center_frame, style='Main.TFrame')
        title_container.pack(pady=(0, 30))
        
        # Container para ícones e título
        icons_title_frame = ttk.Frame(title_container, style='Main.TFrame')
        icons_title_frame.pack()
        
        # Ícone esquerdo (Sword) - simulado com Canvas
        left_icon_canvas = tk.Canvas(icons_title_frame, width=80, height=80, 
                                   bg='#0f172a', highlightthickness=0)
        left_icon_canvas.pack(side=tk.LEFT, padx=(0, 15))
        
        # Gradiente vermelho para o ícone
        for i in range(80):
            for j in range(80):
                if 20 <= i <= 60 and 20 <= j <= 60:  # Área do ícone
                    left_icon_canvas.create_rectangle(i, j, i+1, j+1, fill='#dc2626', outline='#dc2626')
        
        # Desenhar espada simplificada
        left_icon_canvas.create_rectangle(35, 25, 45, 55, fill='white', outline='white')
        left_icon_canvas.create_rectangle(30, 50, 50, 60, fill='white', outline='white')
        
        # Título principal
        title_label = ttk.Label(icons_title_frame, text="MediaSlayer", style='Title.TLabel')
        title_label.pack(side=tk.LEFT, padx=(0, 15))
        
        # Ícone direito (Shield) - simulado
        right_icon_canvas = tk.Canvas(icons_title_frame, width=80, height=80, 
                                    bg='#0f172a', highlightthickness=0)
        right_icon_canvas.pack(side=tk.LEFT)
        
        # Gradiente azul para o ícone
        for i in range(80):
            for j in range(80):
                if 20 <= i <= 60 and 20 <= j <= 60:
                    right_icon_canvas.create_rectangle(i, j, i+1, j+1, fill='#2563eb', outline='#2563eb')
        
        # Desenhar escudo simplificado
        right_icon_canvas.create_polygon(40, 25, 30, 35, 30, 50, 40, 60, 50, 50, 50, 35, 
                                       fill='white', outline='white')
        
        # Subtítulo
        subtitle_label = ttk.Label(title_container, 
                                 text="Embark on your digital quest to capture and download legendary media from the realms of YouTube and X. Forge your collection!",
                                 style='Subtitle.TLabel', wraplength=600, justify='center')
        subtitle_label.pack(pady=(15, 0))
        
        # Card principal
        card_frame = ttk.Frame(center_frame, style='Card.TFrame', padding="40")
        card_frame.pack(pady=(30, 0))
        
        # Header do card
        card_header = ttk.Frame(card_frame, style='Card.TFrame')
        card_header.pack(fill=tk.X, pady=(0, 30))
        
        # Ícone de download no header
        download_icon_canvas = tk.Canvas(card_header, width=50, height=50, 
                                       bg='#1e293b', highlightthickness=0)
        download_icon_canvas.pack(pady=(0, 15))
        
        # Círculo vermelho com gradiente
        download_icon_canvas.create_oval(10, 10, 40, 40, fill='#dc2626', outline='#b91c1c', width=2)
        # Seta de download
        download_icon_canvas.create_polygon(25, 18, 20, 28, 30, 28, fill='white')
        download_icon_canvas.create_rectangle(23, 28, 27, 35, fill='white', outline='white')
        
        # Título do card
        card_title = ttk.Label(card_header, text="Begin Your Quest", style='CardTitle.TLabel')
        card_title.pack()
        
        # Descrição do card
        card_desc = ttk.Label(card_header, 
                            text="Enter the URL of your target media and select your preferred enchantment",
                            style='CardDesc.TLabel')
        card_desc.pack(pady=(5, 0))
        
        # Conteúdo do card
        card_content = ttk.Frame(card_frame, style='Card.TFrame')
        card_content.pack(fill=tk.BOTH, expand=True)
        
        # URL Input
        url_section = ttk.Frame(card_content, style='Card.TFrame')
        url_section.pack(fill=tk.X, pady=(0, 25))
        
        # Label com ícone
        url_label_frame = ttk.Frame(url_section, style='Card.TFrame')
        url_label_frame.pack(fill=tk.X, pady=(0, 10))
        
        url_label = ttk.Label(url_label_frame, text="⚡ Target URL", style='FieldLabel.TLabel')
        url_label.pack(side=tk.LEFT)
        
        # Container para input com ícone
        url_input_frame = ttk.Frame(url_section, style='Card.TFrame')
        url_input_frame.pack(fill=tk.X)
        
        self.url_entry = ttk.Entry(url_input_frame, textvariable=self.url_var, 
                                  style='Modern.TEntry', font=('Segoe UI', 12))
        self.url_entry.pack(fill=tk.X, ipady=12)
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
        
        # Dropdowns
        dropdowns_frame = ttk.Frame(card_content, style='Card.TFrame')
        dropdowns_frame.pack(fill=tk.X, pady=(0, 25))
        dropdowns_frame.columnconfigure(0, weight=1)
        dropdowns_frame.columnconfigure(1, weight=1)
        
        # Format Enchantment
        format_frame = ttk.Frame(dropdowns_frame, style='Card.TFrame')
        format_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 15))
        
        format_label = ttk.Label(format_frame, text="💎 Format Enchantment", style='FieldLabel.TLabel')
        format_label.pack(anchor=tk.W, pady=(0, 10))
        
        self.format_combo = ttk.Combobox(format_frame, textvariable=self.format_var,
                                        values=["⚔️ MP4 (Video Scroll)", "🎵 MP3 (Audio Rune)", 
                                               "🛡️ WebM (Web Armor)", "🔮 WAV (Crystal Audio)"],
                                        state="readonly", style='Modern.TCombobox')
        self.format_combo.pack(fill=tk.X, ipady=8)
        self.format_combo.set("⚔️ MP4 (Video Scroll)")
        
        # Quality Level
        quality_frame = ttk.Frame(dropdowns_frame, style='Card.TFrame')
        quality_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(15, 0))
        
        quality_label = ttk.Label(quality_frame, text="👑 Quality Level", style='FieldLabel.TLabel')
        quality_label.pack(anchor=tk.W, pady=(0, 10))
        
        self.quality_combo = ttk.Combobox(quality_frame, textvariable=self.quality_var,
                                         values=["👑 1080p (Legendary)", "⭐ 720p (Epic)", 
                                                "🔸 480p (Rare)", "⚪ 360p (Common)"],
                                         state="readonly", style='Modern.TCombobox')
        self.quality_combo.pack(fill=tk.X, ipady=8)
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
        
        # Botão de download
        self.download_btn = ttk.Button(card_content, text="⚔️ Execute Download Quest", 
                                      command=self.start_download, style='RedGradient.TButton')
        self.download_btn.pack(fill=tk.X, pady=(25, 0), ipady=8)
    
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
    
    def progress_hook(self, d):
        """Hook de progresso"""
        if d['status'] == 'downloading':
            if 'total_bytes' in d and d['total_bytes']:
                percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                self.progress_var.set(percent)
                self.progress_percent.config(text=f"{percent:.0f}%")
            elif '_percent_str' in d:
                try:
                    percent_str = d['_percent_str'].strip('%')
                    percent = float(percent_str)
                    self.progress_var.set(percent)
                    self.progress_percent.config(text=f"{percent:.0f}%")
                except:
                    pass
        elif d['status'] == 'finished':
            self.progress_var.set(100)
            self.progress_percent.config(text="100%")
            self.progress_status.config(text="Quest completed! Media successfully captured!")
    
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
        
        os.makedirs(self.download_path, exist_ok=True)
        
        # Mostrar progresso
        self.progress_frame.pack(fill=tk.X, pady=(0, 25))
        
        ydl_opts = {
            'outtmpl': os.path.join(self.download_path, '%(uploader)s - %(title)s.%(ext)s'),
            'format': self.get_format_options(),
            'progress_hooks': [self.progress_hook],
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            self.progress_status.config(text="Casting download spell...")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            messagebox.showinfo("Success", "✅ Quest completed! Media successfully captured and added to your inventory!")
            
        except Exception as e:
            error_msg = f"❌ Quest failed! The download spell was interrupted: {str(e)}"
            messagebox.showerror("Error", error_msg)
        finally:
            self.progress_var.set(0)
            self.download_btn.config(state='normal', text="⚔️ Execute Download Quest")
            self.is_downloading = False
            self.root.after(3000, lambda: self.progress_frame.pack_forget())
    
    def start_download(self):
        """Iniciar download"""
        if self.is_downloading:
            return
            
        self.is_downloading = True
        self.download_btn.config(state='disabled', text="🔄 Casting Spell...")
        threading.Thread(target=self.download_media, daemon=True).start()

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