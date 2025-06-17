import tkinter as tk
from tkinter import ttk

def setup_styles():
    """Configure all the custom styles for the application widgets."""
    style = ttk.Style()
    
    # Define color palette inspired by a modern, dark gaming UI
    colors = {
        'slate_800': '#1e293b',
        'slate_700': '#334155',
        'slate_600': '#475569',
        'slate_400': '#94a3b8',
        'slate_300': '#d1d5db',
        'red_600': '#dc2626',
        'red_700': '#b91c1c',
        'blue_600': '#2563eb',
        'white': '#ffffff',
        'black': '#000000',
    }

    # --- Global Style Configurations ---
    style.theme_use('clam') # 'clam' is a good base for custom styling
    
    # --- Frame Styles ---
    style.configure('TFrame', background=colors['slate_800'])
    style.configure('Card.TFrame', background=colors['slate_700'], borderwidth=1, relief='solid')

    # --- Label Styles ---
    style.configure('TLabel', background=colors['slate_800'], foreground=colors['slate_300'], font=('Segoe UI', 10))
    style.configure('CardTitle.TLabel', background=colors['slate_700'], foreground=colors['white'], font=('Segoe UI', 16, 'bold'))
    style.configure('FieldLabel.TLabel', background=colors['slate_700'], foreground=colors['slate_300'], font=('Segoe UI', 10, 'bold'))
    
    # --- Entry (Input) Style ---
    style.configure('Modern.TEntry',
                    background=colors['slate_800'],
                    foreground=colors['white'],
                    fieldbackground=colors['slate_800'],
                    insertcolor=colors['white'],
                    borderwidth=1,
                    relief='solid',
                    padding=(10, 8))
    style.map('Modern.TEntry',
              bordercolor=[('focus', colors['blue_600'])],
              relief=[('focus', 'solid')])

    # --- Combobox (Dropdown) Style ---
    style.configure('Modern.TCombobox',
                    arrowcolor=colors['white'],
                    selectbackground=colors['slate_600'],
                    selectforeground=colors['white'],
                    fieldbackground=colors['slate_800'],
                    background=colors['slate_800'],
                    foreground=colors['white'],
                    padding=10)
    style.map('Modern.TCombobox',
              background=[('readonly', colors['slate_800'])],
              fieldbackground=[('readonly', colors['slate_800'])],
              selectbackground=[('readonly', colors['slate_600'])],
              bordercolor=[('focus', colors['blue_600'])])

    # --- Button Style ---
    style.configure('RedGradient.TButton',
                    background=colors['red_600'],
                    foreground=colors['white'],
                    font=('Segoe UI', 12, 'bold'),
                    borderwidth=0,
                    relief='flat',
                    padding=(15, 10))
    style.map('RedGradient.TButton',
              background=[('active', colors['red_700']), ('pressed', colors['red_700'])])
              
    # --- Progress Bar Style ---
    style.configure('Modern.Horizontal.TProgressbar',
                    background=colors['red_600'],
                    troughcolor=colors['slate_700'],
                    borderwidth=1,
                    relief='solid')
    
    return style



