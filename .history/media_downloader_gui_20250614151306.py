#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MediaSlayer - Downloader Universal de Vídeos
Interface simples para baixar vídeos do YouTube e Twitter/X
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
        self.root.title("⚔️ MediaSlayer - Universal Video Downloader")
        self.root.geometry("700x500")
        self.root.minsize(600, 400)
        self.root.configure(bg='#2b2b2b')
        
        # Centralizar janela
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
    
    def setup_variables(self):
        """Inicializar variáveis"""
        self.url_var = tk.StringVar()
        self.path_var = tk.StringVar()
        self.quality_var = tk.StringVar(value="720p")
        self.format_var = tk.StringVar(value="mp4")
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Pronto para download")
        
        # Pasta padrão
        self.download_path = os.path.join(os.getcwd(), "downloads")
        self.path_var.set(self.download_path)
        
        # Controle de análise
        self.last_analyzed_url = ""
        self.video_info = None
    
    def setup_styles(self):
        """Configurar estilos"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Cores
        colors = {
            'bg': '#2b2b2b',
            'fg': '#ffffff',
            'card_bg': '#3c3c3c',
            'button_bg': '#0078d4',
            'entry_bg': '#404040',
            'success': '#28a745',
            'error': '#dc3545'
        }
        
        # Estilos
        self.style.configure('Dark.TFrame', background=colors['bg'])
        self.style.configure('Card.TFrame', background=colors['card_bg'], relief='solid', borderwidth=1)
        self.style.configure('Dark.TLabel', background=colors['bg'], foreground=colors['fg'], font=('Segoe UI', 10))
        self.style.configure('Title.TLabel', background=colors['bg'], foreground=colors['fg'], font=('Segoe UI', 16, 'bold'))
        self.style.configure('Info.TLabel', background=colors['card_bg'], foreground='#cccccc', font=('Segoe UI', 9))
        
        self.style.configure('Modern.TButton', 
                           background=colors['button_bg'], 
                           foreground=colors['fg'],
                           borderwidth=0,
                           font=('Segoe UI', 10, 'bold'),
                           padding=(15, 8))
        
        self.style.configure('Dark.TEntry',
                           fieldbackground=colors['entry_bg'],
                           foreground=colors['fg'],
                           borderwidth=1,
                           insertcolor=colors['fg'],
                           font=('Segoe UI', 11))
        
        self.style.configure('Dark.TCombobox',
                           fieldbackground=colors['entry_bg'],
                           foreground=colors['fg'],
                           borderwidth=1,
                           font=('Segoe UI', 10))
        
        self.style.configure('Modern.Horizontal.TProgressbar',
                           background=colors['button_bg'],
                           troughcolor=colors['entry_bg'],
                           borderwidth=0)
    
    def create_ui(self):
        """Criar interface simplificada"""
        main_frame = ttk.Frame(self.root, style='Dark.TFrame', padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="⚔️ MediaSlayer", style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Card principal
        card_frame = ttk.Frame(main_frame, style='Card.TFrame', padding="20")
        card_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        card_frame.columnconfigure(0, weight=1)
        
        # URL
        url_label = ttk.Label(card_frame, text="URL do Vídeo:", style='Dark.TLabel')
        url_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.url_entry = ttk.Entry(card_frame, textvariable=self.url_var, 
                                  style='Dark.TEntry', font=('Segoe UI', 11))
        self.url_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10), ipady=5)
        self.url_entry.bind('<KeyRelease>', self.on_url_change)
        
        # Info do vídeo
        self.info_frame = ttk.Frame(card_frame, style='Card.TFrame')
        self.info_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        self.info_frame.columnconfigure(0, weight=1)
        
        self.info_label = ttk.Label(self.info_frame, text="", style='Info.TLabel', wraplength=500)
        self.info_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Configurações
        config_frame = ttk.Frame(card_frame, style='Card.TFrame')
        config_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        config_frame.columnconfigure(0, weight=1)
        config_frame.columnconfigure(1, weight=1)
        
        # Qualidade
        quality_label = ttk.Label(config_frame, text="Qualidade:", style='Dark.TLabel')
        quality_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.quality_combo = ttk.Combobox(config_frame, textvariable=self.quality_var,
                                         values=["1080p", "720p", "480p", "360p"],
                                         state="readonly", style='Dark.TCombobox', width=10)
        self.quality_combo.grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        
        # Formato
        format_label = ttk.Label(config_frame, text="Formato:", style='Dark.TLabel')
        format_label.grid(row=0, column=1, sticky=tk.W)
        
        self.format_combo = ttk.Combobox(config_frame, textvariable=self.format_var,
                                        values=["mp4", "mp3", "webm"],
                                        state="readonly", style='Dark.TCombobox', width=10)
        self.format_combo.grid(row=1, column=1, sticky=tk.W)
        
        # Pasta
        path_frame = ttk.Frame(card_frame, style='Card.TFrame')
        path_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        path_frame.columnconfigure(0, weight=1)
        
        path_label = ttk.Label(path_frame, text="Pasta de Destino:", style='Dark.TLabel')
        path_label.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        self.path_entry = ttk.Entry(path_frame, textvariable=self.path_var, 
                                   style='Dark.TEntry', state='readonly')
        self.path_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        browse_btn = ttk.Button(path_frame, text="Procurar", 
                               command=self.browse_folder, style='Modern.TButton')
        browse_btn.grid(row=1, column=1)
        
        # Progresso
        progress_frame = ttk.Frame(card_frame, style='Card.TFrame')
        progress_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        progress_frame.columnconfigure(0, weight=1)
        
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_var, style='Info.TLabel')
        self.status_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                           maximum=100, style='Modern.Horizontal.TProgressbar')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), ipady=3)
        
        # Console de log
        self.console_frame = ttk.Frame(progress_frame, style='Card.TFrame')
        self.console_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        self.console_frame.columnconfigure(0, weight=1)
        
        console_label = ttk.Label(self.console_frame, text="Log do Download:", style='Dark.TLabel')
        console_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.console_text = tk.Text(self.console_frame, height=6, width=60, 
                                   bg='#1e1e1e', fg='#00ff00', font=('Consolas', 9),
                                   state='disabled', wrap=tk.WORD)
        self.console_text.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        console_scroll = ttk.Scrollbar(self.console_frame, orient="vertical", command=self.console_text.yview)
        console_scroll.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.console_text.configure(yscrollcommand=console_scroll.set)
        
        # Botão de download
        self.download_btn = ttk.Button(card_frame, text="⬇️ Baixar Vídeo", 
                                      command=self.start_download, style='Modern.TButton')
        self.download_btn.grid(row=6, column=0, pady=(15, 0), ipady=5)
    
    def log_to_console(self, message):
        """Adicionar mensagem ao console"""
        self.console_text.config(state='normal')
        self.console_text.insert(tk.END, f"{message}\n")
        self.console_text.see(tk.END)
        self.console_text.config(state='disabled')
        self.root.update_idletasks()
    
    def detect_platform(self, url):
        """Detectar plataforma"""
        if not url:
            return None
        if re.search(r'(youtube\.com|youtu\.be)', url):
            return "youtube"
        elif re.search(r'(twitter\.com|x\.com|t\.co)', url):
            return "twitter"
        return None
    
    def analyze_url_automatically(self, url):
        """Analisar URL automaticamente"""
        if not url or url == self.last_analyzed_url:
            return
            
        self.last_analyzed_url = url
        platform = self.detect_platform(url)
        
        if not platform:
            self.info_label.config(text="❌ URL inválida")
            return
        
        def analyze():
            try:
                self.update_status("🔍 Analisando vídeo...")
                self.log_to_console(f"[INFO] Analisando URL: {url}")
                
                with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    
                    title = info.get('title', 'N/A')
                    uploader = info.get('uploader', 'N/A')
                    duration = info.get('duration', 0)
                    
                    self.video_info = info
                    
                    info_text = f"📺 {title}\n👤 {uploader}"
                    if duration:
                        mins, secs = divmod(duration, 60)
                        info_text += f"\n⏱️ {mins:02d}:{secs:02d}"
                    
                    platform_emoji = "🎥" if platform == "youtube" else "🐦"
                    info_text = f"{platform_emoji} {info_text}"
                    
                    self.info_label.config(text=info_text)
                    self.update_status("✅ Vídeo analisado - Pronto para download")
                    self.log_to_console(f"[SUCCESS] Vídeo encontrado: {title}")
                    
            except Exception as e:
                self.info_label.config(text=f"❌ Erro ao analisar: {str(e)}")
                self.update_status("❌ Erro na análise")
                self.log_to_console(f"[ERROR] Falha na análise: {str(e)}")
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def on_url_change(self, event=None):
        """Callback quando URL muda"""
        url = self.url_var.get().strip()
        # Analisar automaticamente após 1 segundo de inatividade
        self.root.after(1000, lambda: self.analyze_url_automatically(url))
    
    def browse_folder(self):
        """Navegar por pastas"""
        folder = filedialog.askdirectory(initialdir=self.download_path)
        if folder:
            self.download_path = folder
            self.path_var.set(folder)
            self.update_status(f"Pasta alterada: {folder}")
    
    def get_format_options(self):
        """Obter opções de formato"""
        quality = self.quality_var.get()
        format_type = self.format_var.get()
        
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
        """Hook de progresso com log detalhado"""
        if d['status'] == 'downloading':
            if 'total_bytes' in d and d['total_bytes']:
                percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                speed = d.get('speed', 0)
                speed_str = f"{speed/1024/1024:.1f} MB/s" if speed else "N/A"
                
                self.progress_var.set(percent)
                self.update_status(f"⬇️ Baixando... {percent:.1f}% - {speed_str}")
                
                if percent % 10 < 1:  # Log a cada 10%
                    self.log_to_console(f"[DOWNLOAD] {percent:.1f}% concluído - Velocidade: {speed_str}")
                    
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
            filename = os.path.basename(d['filename'])
            self.update_status("✅ Download concluído!")
            self.log_to_console(f"[SUCCESS] Download finalizado: {filename}")
            
        elif d['status'] == 'error':
            self.log_to_console(f"[ERROR] Erro no download: {d.get('error', 'Erro desconhecido')}")
    
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
        
        # Criar pasta
        os.makedirs(self.download_path, exist_ok=True)
        
        # Limpar console
        self.console_text.config(state='normal')
        self.console_text.delete(1.0, tk.END)
        self.console_text.config(state='disabled')
        
        # Configurar yt-dlp
        ydl_opts = {
            'outtmpl': os.path.join(self.download_path, '%(uploader)s - %(title)s.%(ext)s'),
            'format': self.get_format_options(),
            'progress_hooks': [self.progress_hook],
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            self.log_to_console(f"[INFO] Iniciando download...")
            self.log_to_console(f"[INFO] URL: {url}")
            self.log_to_console(f"[INFO] Qualidade: {self.quality_var.get()}")
            self.log_to_console(f"[INFO] Formato: {self.format_var.get()}")
            self.log_to_console(f"[INFO] Destino: {self.download_path}")
            
            self.update_status("🚀 Iniciando download...")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            self.log_to_console(f"[SUCCESS] ✅ Download concluído com sucesso!")
            messagebox.showinfo("Sucesso", "✅ Download concluído!")
            self.update_status("Pronto para próximo download")
            
        except Exception as e:
            error_msg = f"❌ Download falhou: {str(e)}"
            self.log_to_console(f"[ERROR] {error_msg}")
            messagebox.showerror("Erro", error_msg)
            self.update_status("Download falhou")
        finally:
            self.progress_var.set(0)
            self.download_btn.config(state='normal', text="⬇️ Baixar Vídeo")
    
    def start_download(self):
        """Iniciar download"""
        self.download_btn.config(state='disabled', text="🔄 Baixando...")
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