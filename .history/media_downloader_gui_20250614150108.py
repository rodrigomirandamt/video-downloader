#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MediaSlayer - Downloader Universal de Vídeos
Interface gráfica moderna para baixar vídeos do YouTube e Twitter/X
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import yt_dlp
import os
import re
from pathlib import Path
import time
from datetime import datetime

class MediaSlayerGUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_variables()
        self.setup_styles()
        self.create_modern_ui()
        
    def setup_window(self):
        """Configurar janela principal com estilo moderno"""
        self.root.title("⚔️ MediaSlayer - Universal Video Downloader")
        self.root.geometry("900x800")
        self.root.minsize(800, 700)
        self.root.configure(bg='#1e1e1e')
        
        # Centralizar janela
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
        
        # Tentar definir ícone
        try:
            self.root.iconbitmap('mediaslayer.ico')
        except:
            pass
    
    def setup_variables(self):
        """Inicializar todas as variáveis"""
        self.url_var = tk.StringVar()
        self.path_var = tk.StringVar()
        self.quality_var = tk.StringVar(value="720p")
        self.format_var = tk.StringVar(value="mp4")
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Pronto para iniciar sua quest")
        self.platform_var = tk.StringVar(value="")
        
        # Caminhos padrão
        self.download_path = os.path.join(os.getcwd(), "downloads")
        self.path_var.set(self.download_path)
        
        # Stats RPG
        self.xp = 1250
        self.level = 7
        self.downloads_count = 0
    
    def setup_styles(self):
        """Configurar estilos modernos"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Cores do tema escuro
        colors = {
            'bg': '#1e1e1e',
            'fg': '#ffffff',
            'card_bg': '#252525',
            'button_bg': '#dc2626',
            'button_hover': '#b91c1c',
            'entry_bg': '#374151',
            'accent': '#ef4444'
        }
        
        # Configurar estilos
        self.style.configure('Dark.TFrame', background=colors['bg'])
        self.style.configure('Card.TFrame', background=colors['card_bg'], relief='flat', borderwidth=2)
        self.style.configure('Dark.TLabel', background=colors['bg'], foreground=colors['fg'], font=('Segoe UI', 10))
        self.style.configure('Title.TLabel', background=colors['bg'], foreground=colors['fg'], font=('Segoe UI', 24, 'bold'))
        self.style.configure('Subtitle.TLabel', background=colors['bg'], foreground='#9ca3af', font=('Segoe UI', 12))
        self.style.configure('Stats.TLabel', background=colors['bg'], foreground='#fbbf24', font=('Segoe UI', 11, 'bold'))
        
        # Botões
        self.style.configure('Quest.TButton', 
                           background=colors['button_bg'], 
                           foreground=colors['fg'],
                           borderwidth=0,
                           focuscolor='none',
                           font=('Segoe UI', 12, 'bold'),
                           padding=(20, 10))
        
        # Entrada de texto
        self.style.configure('Dark.TEntry',
                           fieldbackground=colors['entry_bg'],
                           foreground=colors['fg'],
                           borderwidth=2,
                           insertcolor=colors['fg'],
                           font=('Segoe UI', 11))
        
        # Combobox
        self.style.configure('Dark.TCombobox',
                           fieldbackground=colors['entry_bg'],
                           foreground=colors['fg'],
                           borderwidth=2,
                           font=('Segoe UI', 10))
        
        # Barra de progresso
        self.style.configure('Quest.Horizontal.TProgressbar',
                           background=colors['accent'],
                           troughcolor=colors['entry_bg'],
                           borderwidth=0,
                           lightcolor=colors['accent'],
                           darkcolor=colors['accent'])
    
    def create_modern_ui(self):
        """Criar interface moderna inspirada no design RPG"""
        # Container principal
        main_container = ttk.Frame(self.root, style='Dark.TFrame', padding="30")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=1)
        
        # Header com stats RPG
        self.create_header(main_container)
        
        # Título principal
        self.create_title(main_container)
        
        # Card principal
        self.create_main_card(main_container)
        
        # Recursos RPG
        self.create_features(main_container)
        
        # Footer
        self.create_footer(main_container)
    
    def create_header(self, parent):
        """Criar header com stats RPG"""
        header_frame = ttk.Frame(parent, style='Dark.TFrame')
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        header_frame.columnconfigure(1, weight=1)
        
        # Stats da esquerda
        left_stats = ttk.Frame(header_frame, style='Dark.TFrame')
        left_stats.grid(row=0, column=0, sticky=tk.W)
        
        level_label = ttk.Label(left_stats, text=f"👑 Level {self.level}", style='Stats.TLabel')
        level_label.grid(row=0, column=0, padx=(0, 20))
        
        xp_label = ttk.Label(left_stats, text=f"⭐ {self.xp} XP", style='Stats.TLabel')
        xp_label.grid(row=0, column=1, padx=(0, 20))
        
        # Stats da direita
        right_stats = ttk.Frame(header_frame, style='Dark.TFrame')
        right_stats.grid(row=0, column=2, sticky=tk.E)
        
        hunter_label = ttk.Label(right_stats, text="💎 Media Hunter", style='Stats.TLabel')
        hunter_label.grid(row=0, column=0)
    
    def create_title(self, parent):
        """Criar título principal"""
        title_frame = ttk.Frame(parent, style='Dark.TFrame')
        title_frame.grid(row=1, column=0, pady=(0, 30))
        
        # Título com ícones
        title_container = ttk.Frame(title_frame, style='Dark.TFrame')
        title_container.pack()
        
        sword_label = ttk.Label(title_container, text="⚔️", font=('Segoe UI', 32), 
                               background='#1e1e1e', foreground='#ef4444')
        sword_label.pack(side=tk.LEFT, padx=(0, 15))
        
        title_label = ttk.Label(title_container, text="MediaSlayer", style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        shield_label = ttk.Label(title_container, text="🛡️", font=('Segoe UI', 32), 
                                background='#1e1e1e', foreground='#3b82f6')
        shield_label.pack(side=tk.LEFT, padx=(15, 0))
        
        # Subtítulo
        subtitle_label = ttk.Label(title_frame, 
                                  text="Embarque em sua quest digital para capturar mídia lendária do YouTube e X",
                                  style='Subtitle.TLabel')
        subtitle_label.pack(pady=(10, 0))
    
    def create_main_card(self, parent):
        """Criar card principal"""
        card_frame = ttk.Frame(parent, style='Card.TFrame', padding="30")
        card_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 30))
        card_frame.columnconfigure(0, weight=1)
        
        # Título do card
        card_title = ttk.Label(card_frame, text="🎯 Iniciar Sua Quest", 
                              font=('Segoe UI', 16, 'bold'), 
                              background='#252525', foreground='#ffffff')
        card_title.grid(row=0, column=0, pady=(0, 20))
        
        # URL Input
        self.create_url_section(card_frame)
        
        # Configurações
        self.create_settings_section(card_frame)
        
        # Progresso
        self.create_progress_section(card_frame)
        
        # Botão de download
        self.create_download_button(card_frame)
    
    def create_url_section(self, parent):
        """Criar seção de URL"""
        url_frame = ttk.Frame(parent, style='Card.TFrame')
        url_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        url_frame.columnconfigure(1, weight=1)
        
        # Label
        url_label = ttk.Label(url_frame, text="⚡ URL Alvo:", 
                             font=('Segoe UI', 11, 'bold'),
                             background='#252525', foreground='#ffffff')
        url_label.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 8))
        
        # Entry
        self.url_entry = ttk.Entry(url_frame, textvariable=self.url_var, 
                                  style='Dark.TEntry', font=('Segoe UI', 12), width=50)
        self.url_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.url_entry.bind('<KeyRelease>', self.on_url_change)
        

        
        # Platform indicator
        self.platform_label = ttk.Label(url_frame, text="", 
                                       font=('Segoe UI', 10, 'bold'),
                                       background='#252525', foreground='#ef4444')
        self.platform_label.grid(row=2, column=0, columnspan=3, pady=(10, 0))
    
    def create_settings_section(self, parent):
        """Criar seção de configurações"""
        settings_frame = ttk.Frame(parent, style='Card.TFrame')
        settings_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        settings_frame.columnconfigure(0, weight=1)
        settings_frame.columnconfigure(1, weight=1)
        
        # Qualidade
        quality_frame = ttk.Frame(settings_frame, style='Card.TFrame')
        quality_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        quality_label = ttk.Label(quality_frame, text="👑 Nível de Qualidade:", 
                                 font=('Segoe UI', 10, 'bold'),
                                 background='#252525', foreground='#ffffff')
        quality_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.quality_combo = ttk.Combobox(quality_frame, textvariable=self.quality_var,
                                         values=["1080p (Lendário)", "720p (Épico)", "480p (Raro)", "360p (Comum)"],
                                         state="readonly", style='Dark.TCombobox')
        self.quality_combo.pack(fill=tk.X)
        
        # Formato
        format_frame = ttk.Frame(settings_frame, style='Card.TFrame')
        format_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        format_label = ttk.Label(format_frame, text="💎 Encantamento de Formato:", 
                                font=('Segoe UI', 10, 'bold'),
                                background='#252525', foreground='#ffffff')
        format_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.format_combo = ttk.Combobox(format_frame, textvariable=self.format_var,
                                        values=["mp4 (Pergaminho de Vídeo)", "mp3 (Runa de Áudio)", "webm (Armadura Web)"],
                                        state="readonly", style='Dark.TCombobox')
        self.format_combo.pack(fill=tk.X)
        
        # Pasta de destino
        path_frame = ttk.Frame(settings_frame, style='Card.TFrame')
        path_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(15, 0))
        path_frame.columnconfigure(0, weight=1)
        
        path_label = ttk.Label(path_frame, text="📂 Cofre do Tesouro:", 
                              font=('Segoe UI', 10, 'bold'),
                              background='#252525', foreground='#ffffff')
        path_label.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        self.path_entry = ttk.Entry(path_frame, textvariable=self.path_var, 
                                   style='Dark.TEntry', state='readonly')
        self.path_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        browse_btn = ttk.Button(path_frame, text="📁 Explorar", 
                               command=self.browse_folder, style='Quest.TButton')
        browse_btn.grid(row=1, column=1)
    
    def create_progress_section(self, parent):
        """Criar seção de progresso"""
        progress_frame = ttk.Frame(parent, style='Card.TFrame')
        progress_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        progress_frame.columnconfigure(0, weight=1)
        
        # Status
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_var,
                                     font=('Segoe UI', 10),
                                     background='#252525', foreground='#9ca3af')
        self.status_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # Barra de progresso
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                           maximum=100, length=400, style='Quest.Horizontal.TProgressbar')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
    
    def create_download_button(self, parent):
        """Criar botão de download"""
        self.download_btn = ttk.Button(parent, text="⚔️ Executar Quest de Download", 
                                      command=self.start_download, style='Quest.TButton')
        self.download_btn.grid(row=4, column=0, pady=(10, 0))
    
    def create_features(self, parent):
        """Criar seção de recursos"""
        features_frame = ttk.Frame(parent, style='Dark.TFrame')
        features_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 30))
        features_frame.columnconfigure(0, weight=1)
        features_frame.columnconfigure(1, weight=1)
        features_frame.columnconfigure(2, weight=1)
        
        # Título
        features_title = ttk.Label(features_frame, text="🛡️ Habilidades da Guilda ⚔️", 
                                  font=('Segoe UI', 18, 'bold'),
                                  background='#1e1e1e', foreground='#ffffff')
        features_title.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Feature cards
        self.create_feature_card(features_frame, 0, "⚡", "Velocidade Relâmpago", 
                               "Aproveite o poder da magia de download ancestral")
        self.create_feature_card(features_frame, 1, "👑", "Qualidade Lendária", 
                               "Forje mídia em múltiplos formatos com encantamentos épicos")
        self.create_feature_card(features_frame, 2, "💎", "Suporte Multi-Reino", 
                               "Conquiste YouTube, X (Twitter) e outros reinos digitais")
    
    def create_feature_card(self, parent, col, icon, title, description):
        """Criar card de recurso"""
        card = ttk.Frame(parent, style='Card.TFrame', padding="20")
        card.grid(row=1, column=col, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10)
        
        icon_label = ttk.Label(card, text=icon, font=('Segoe UI', 24),
                              background='#252525', foreground='#ef4444')
        icon_label.pack(pady=(0, 10))
        
        title_label = ttk.Label(card, text=title, font=('Segoe UI', 12, 'bold'),
                               background='#252525', foreground='#ffffff')
        title_label.pack(pady=(0, 5))
        
        desc_label = ttk.Label(card, text=description, font=('Segoe UI', 9),
                              background='#252525', foreground='#9ca3af',
                              wraplength=200, justify=tk.CENTER)
        desc_label.pack()
    
    def create_footer(self, parent):
        """Criar footer"""
        footer_frame = ttk.Frame(parent, style='Dark.TFrame')
        footer_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(20, 0))
        
        footer_label = ttk.Label(footer_frame, 
                                text="⚔️ © 2024 MediaSlayer Guild. Forjado para aventuras lendárias. 🛡️",
                                font=('Segoe UI', 9),
                                background='#1e1e1e', foreground='#6b7280')
        footer_label.pack()
    
    def detect_platform(self, url):
        """Detectar plataforma da URL"""
        if not url:
            return None
            
        if re.search(r'(youtube\.com|youtu\.be)', url):
            return "youtube"
        elif re.search(r'(twitter\.com|x\.com|t\.co)', url):
            return "twitter"
        return None
    
    def on_url_change(self, event=None):
        """Callback quando URL muda"""
        url = self.url_var.get()
        platform = self.detect_platform(url)
        
        if platform == "youtube":
            self.platform_label.config(text="🎥 Reino do YouTube detectado", foreground='#ef4444')
            self.platform_var.set("youtube")
        elif platform == "twitter":
            self.platform_label.config(text="🐦 Reino do X (Twitter) detectado", foreground='#3b82f6')
            self.platform_var.set("twitter")
        else:
            self.platform_label.config(text="")
            self.platform_var.set("")
    
    def paste_url(self):
        """Colar URL da área de transferência"""
        try:
            clipboard_content = self.root.clipboard_get()
            self.url_var.set(clipboard_content)
            self.on_url_change()
            self.update_status("URL colada da área de transferência")
        except:
            self.update_status("Nenhuma URL encontrada na área de transferência")
    
    def analyze_url(self):
        """Analisar URL"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Erro", "Por favor, insira uma URL")
            return
        
        platform = self.detect_platform(url)
        if not platform:
            messagebox.showerror("Erro", "URL inválida! Use uma URL do YouTube ou X (Twitter)")
            return
        
        def analyze():
            try:
                self.update_status("🔍 Analisando mídia...")
                with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    
                    title = info.get('title', 'N/A')
                    uploader = info.get('uploader', 'N/A')
                    duration = info.get('duration', 0)
                    
                    message = f"📝 Título: {title}\n👤 Autor: {uploader}"
                    if duration:
                        message += f"\n⏱️ Duração: {duration} segundos"
                    
                    messagebox.showinfo("Informações da Mídia", message)
                    self.update_status("Análise concluída")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao analisar: {str(e)}")
                self.update_status("Erro na análise")
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def browse_folder(self):
        """Navegar por pastas"""
        folder = filedialog.askdirectory(initialdir=self.download_path)
        if folder:
            self.download_path = folder
            self.path_var.set(folder)
            self.update_status(f"Pasta alterada para: {folder}")
    
    def get_format_options(self):
        """Obter opções de formato"""
        quality = self.quality_var.get().split()[0]  # Pegar apenas a resolução
        format_type = self.format_var.get().split()[0]  # Pegar apenas o formato
        
        if format_type == "mp3":
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
            return "best"
    
    def progress_hook(self, d):
        """Hook de progresso"""
        if d['status'] == 'downloading':
            if 'total_bytes' in d and d['total_bytes']:
                percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                self.progress_var.set(percent)
                self.update_status(f"⬇️ Baixando... {percent:.1f}%")
            elif '_percent_str' in d:
                try:
                    percent_str = d['_percent_str'].strip('%')
                    percent = float(percent_str)
                    self.progress_var.set(percent)
                    self.update_status(f"⬇️ Baixando... {percent:.1f}%")
                except:
                    pass
        elif d['status'] == 'finished':
            self.progress_var.set(100)
            self.update_status("✅ Quest concluída! Mídia capturada com sucesso!")
    
    def download_media(self):
        """Baixar mídia"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Erro", "Por favor, insira uma URL")
            return
        
        platform = self.detect_platform(url)
        if not platform:
            messagebox.showerror("Erro", "URL inválida! Use uma URL do YouTube ou X (Twitter)")
            return
        
        # Criar pasta de download
        os.makedirs(self.download_path, exist_ok=True)
        
        # Configurar opções
        ydl_opts = {
            'outtmpl': os.path.join(self.download_path, '%(uploader)s_%(title)s.%(ext)s'),
            'format': self.get_format_options(),
            'progress_hooks': [self.progress_hook],
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': True,
        }
        
        try:
            self.update_status("🚀 Iniciando quest de download...")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # Atualizar stats
            self.downloads_count += 1
            self.xp += 50
            
            messagebox.showinfo("Sucesso", "✅ Quest concluída! Mídia adicionada ao seu inventário!")
            self.update_status("Pronto para próxima quest")
            
        except Exception as e:
            messagebox.showerror("Erro", f"❌ Quest falhou: {str(e)}")
            self.update_status("Quest falhou - tente novamente")
        finally:
            self.progress_var.set(0)
            self.download_btn.config(state='normal', text="⚔️ Executar Quest de Download")
    
    def start_download(self):
        """Iniciar download em thread separada"""
        self.download_btn.config(state='disabled', text="🔄 Executando Quest...")
        threading.Thread(target=self.download_media, daemon=True).start()
    
    def update_status(self, message):
        """Atualizar status"""
        self.status_var.set(message)
        self.root.update_idletasks()

def main():
    """Função principal"""
    root = tk.Tk()
    app = MediaSlayerGUI(root)
    
    # Configurar fechamento
    def on_closing():
        root.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main() 