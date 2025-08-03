"""
DonTe Cleaner - Advanced Theme System
Multiple beautiful themes with smooth transitions
"""

import tkinter as tk
from tkinter import ttk
import time
import threading

class AdvancedThemeManager:
    def __init__(self, root):
        self.root = root
        self.current_theme = "dark"
        
        # Define multiple themes
        self.themes = {
            "dark": {
                "name": "GitHub Dark",
                "bg_primary": "#0d1117",
                "bg_secondary": "#161b22", 
                "bg_medium": "#21262d",
                "bg_light": "#30363d",
                "text_white": "#f0f6fc",
                "text_secondary": "#8b949e",
                "text_muted": "#6e7681",
                "accent_blue": "#58a6ff",
                "accent_green": "#3fb950",
                "accent_red": "#f85149",
                "accent_orange": "#d29922",
                "accent_purple": "#a5a5ff",
                "border": "#30363d",
                "button_bg": "#21262d",
                "button_hover": "#30363d"
            },
            
            "light": {
                "name": "GitHub Light",
                "bg_primary": "#ffffff",
                "bg_secondary": "#f6f8fa",
                "bg_medium": "#eaeef2",
                "bg_light": "#d0d7de",
                "text_white": "#24292f",
                "text_secondary": "#656d76",
                "text_muted": "#8c959f",
                "accent_blue": "#0969da",
                "accent_green": "#1a7f37",
                "accent_red": "#d1242f",
                "accent_orange": "#bc4c00",
                "accent_purple": "#8250df",
                "border": "#d0d7de",
                "button_bg": "#f6f8fa",
                "button_hover": "#eaeef2"
            },
            
            "neon": {
                "name": "Cyberpunk Neon",
                "bg_primary": "#0a0a0f",
                "bg_secondary": "#1a1a2e",
                "bg_medium": "#16213e",
                "bg_light": "#0f4c75",
                "text_white": "#00ff9f",
                "text_secondary": "#7fffd4",
                "text_muted": "#4169e1",
                "accent_blue": "#00bfff",
                "accent_green": "#00ff00",
                "accent_red": "#ff1493",
                "accent_orange": "#ff8c00",
                "accent_purple": "#da70d6",
                "border": "#00bfff",
                "button_bg": "#1a1a2e",
                "button_hover": "#16213e"
            },
            
            "minimal": {
                "name": "Minimal Clean",
                "bg_primary": "#fafafa",
                "bg_secondary": "#f5f5f5",
                "bg_medium": "#eeeeee",
                "bg_light": "#e0e0e0",
                "text_white": "#212121",
                "text_secondary": "#424242",
                "text_muted": "#757575",
                "accent_blue": "#2196f3",
                "accent_green": "#4caf50",
                "accent_red": "#f44336",
                "accent_orange": "#ff9800",
                "accent_purple": "#9c27b0",
                "border": "#e0e0e0",
                "button_bg": "#f5f5f5",
                "button_hover": "#eeeeee"
            },
            
            "gaming": {
                "name": "Gaming RGB",
                "bg_primary": "#0c0c0c",
                "bg_secondary": "#1c1c1c",
                "bg_medium": "#2c2c2c",
                "bg_light": "#3c3c3c",
                "text_white": "#ffffff",
                "text_secondary": "#cccccc",
                "text_muted": "#999999",
                "accent_blue": "#00d4ff",
                "accent_green": "#39ff14",
                "accent_red": "#ff073a",
                "accent_orange": "#ff6600",
                "accent_purple": "#bf00ff",
                "border": "#ff0080",
                "button_bg": "#1c1c1c",
                "button_hover": "#2c2c2c"
            }
        }
        
        self.setup_styles()
    
    def setup_styles(self):
        """Setup advanced TTK styles for all themes"""
        self.style = ttk.Style()
        
        # Configure all theme styles
        for theme_name, colors in self.themes.items():
            self.configure_theme_styles(theme_name, colors)
    
    def configure_theme_styles(self, theme_name, colors):
        """Configure TTK styles for a specific theme"""
        prefix = f"{theme_name.title()}."
        
        # Frame styles
        self.style.configure(f"{prefix}TFrame",
                           background=colors['bg_secondary'],
                           relief="flat",
                           borderwidth=0)
        
        self.style.configure(f"{prefix}Card.TFrame",
                           background=colors['bg_medium'],
                           relief="solid",
                           borderwidth=1,
                           bordercolor=colors['border'])
        
        # Label styles
        self.style.configure(f"{prefix}TLabel",
                           background=colors['bg_secondary'],
                           foreground=colors['text_white'],
                           font=("Segoe UI", 10))
        
        self.style.configure(f"{prefix}Title.TLabel",
                           background=colors['bg_secondary'],
                           foreground=colors['text_white'],
                           font=("Segoe UI", 16, "bold"))
        
        self.style.configure(f"{prefix}CardTitle.TLabel",
                           background=colors['bg_medium'],
                           foreground=colors['text_white'],
                           font=("Segoe UI", 12, "bold"))
        
        self.style.configure(f"{prefix}CardText.TLabel",
                           background=colors['bg_medium'],
                           foreground=colors['text_secondary'],
                           font=("Segoe UI", 9))
        
        # Button styles
        self.style.configure(f"{prefix}TButton",
                           background=colors['button_bg'],
                           foreground=colors['text_white'],
                           borderwidth=1,
                           relief="solid",
                           focuscolor=colors['accent_blue'])
        
        self.style.map(f"{prefix}TButton",
                      background=[('active', colors['button_hover']),
                                ('pressed', colors['accent_blue'])])
        
        # Success button
        self.style.configure(f"{prefix}Success.TButton",
                           background=colors['accent_green'],
                           foreground=colors['text_white'])
        
        self.style.map(f"{prefix}Success.TButton",
                      background=[('active', colors['accent_green']),
                                ('pressed', colors['accent_green'])])
        
        # Danger button
        self.style.configure(f"{prefix}Danger.TButton",
                           background=colors['accent_red'],
                           foreground=colors['text_white'])
        
        # Notebook styles
        self.style.configure(f"{prefix}TNotebook",
                           background=colors['bg_secondary'],
                           borderwidth=0)
        
        self.style.configure(f"{prefix}TNotebook.Tab",
                           background=colors['bg_light'],
                           foreground=colors['text_secondary'],
                           padding=[20, 10],
                           font=("Segoe UI", 10, "bold"))
        
        self.style.map(f"{prefix}TNotebook.Tab",
                      background=[('selected', colors['accent_blue']),
                                ('active', colors['bg_medium'])],
                      foreground=[('selected', colors['text_white']),
                                ('active', colors['text_white'])])
        
        # Progressbar styles
        self.style.configure(f"{prefix}TProgressbar",
                           background=colors['accent_blue'],
                           troughcolor=colors['bg_light'],
                           borderwidth=0,
                           lightcolor=colors['accent_blue'],
                           darkcolor=colors['accent_blue'])
        
        # Success progressbar
        self.style.configure(f"{prefix}Success.TProgressbar",
                           background=colors['accent_green'],
                           troughcolor=colors['bg_light'])
        
        # LabelFrame styles
        self.style.configure(f"{prefix}TLabelframe",
                           background=colors['bg_secondary'],
                           foreground=colors['text_white'],
                           borderwidth=2,
                           relief="solid",
                           bordercolor=colors['border'])
        
        self.style.configure(f"{prefix}TLabelframe.Label",
                           background=colors['bg_secondary'],
                           foreground=colors['accent_blue'],
                           font=("Segoe UI", 11, "bold"))
    
    def apply_theme(self, theme_name, animate=True):
        """Apply a theme with smooth transition"""
        if theme_name not in self.themes:
            return False
        
        if animate:
            self.animate_theme_transition(theme_name)
        else:
            self.instant_theme_change(theme_name)
        
        self.current_theme = theme_name
        return True
    
    def instant_theme_change(self, theme_name):
        """Instantly change theme"""
        colors = self.themes[theme_name]
        prefix = f"{theme_name.title()}."
        
        # Update root window
        self.root.configure(bg=colors['bg_primary'])
        
        # Apply theme prefix to all styles
        self.set_theme_prefix(prefix)
    
    def animate_theme_transition(self, theme_name):
        """Animate theme transition with fade effect"""
        def transition():
            # Create transition overlay
            overlay = tk.Toplevel(self.root)
            overlay.geometry(self.root.geometry())
            overlay.configure(bg='black')
            overlay.attributes('-alpha', 0.0)
            overlay.attributes('-topmost', True)
            overlay.overrideredirect(True)
            
            # Fade in
            for alpha in range(0, 80, 5):
                overlay.attributes('-alpha', alpha / 100)
                time.sleep(0.02)
            
            # Change theme
            self.instant_theme_change(theme_name)
            
            # Fade out
            for alpha in range(80, 0, -5):
                overlay.attributes('-alpha', alpha / 100)
                time.sleep(0.02)
            
            overlay.destroy()
        
        threading.Thread(target=transition, daemon=True).start()
    
    def set_theme_prefix(self, prefix):
        """Update all widget styles to use theme prefix"""
        try:
            # This would need to be called on all widgets
            # For now, we'll just update the style mapping
            pass
        except Exception as e:
            print(f"Theme update error: {e}")
    
    def get_current_colors(self):
        """Get current theme colors"""
        return self.themes[self.current_theme]
    
    def get_available_themes(self):
        """Get list of available themes"""
        return [(name, theme["name"]) for name, theme in self.themes.items()]
    
    def create_theme_preview(self, parent, theme_name, width=200, height=150):
        """Create a preview widget for theme selection"""
        colors = self.themes[theme_name]
        
        # Preview frame
        preview_frame = tk.Frame(parent, 
                               bg=colors['bg_secondary'],
                               relief="solid",
                               borderwidth=2,
                               width=width,
                               height=height)
        preview_frame.pack_propagate(False)
        
        # Header
        header = tk.Frame(preview_frame, bg=colors['accent_blue'], height=30)
        header.pack(fill="x")
        
        tk.Label(header, text=colors['name'], 
                bg=colors['accent_blue'], 
                fg=colors['text_white'],
                font=("Segoe UI", 10, "bold")).pack(pady=5)
        
        # Content area
        content = tk.Frame(preview_frame, bg=colors['bg_secondary'])
        content.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Sample elements
        tk.Label(content, text="Sample Text", 
                bg=colors['bg_secondary'], 
                fg=colors['text_white']).pack(anchor="w")
        
        tk.Label(content, text="Secondary Text", 
                bg=colors['bg_secondary'], 
                fg=colors['text_secondary']).pack(anchor="w")
        
        # Sample button
        btn_frame = tk.Frame(content, bg=colors['bg_medium'], height=30)
        btn_frame.pack(fill="x", pady=5)
        
        tk.Label(btn_frame, text="Button", 
                bg=colors['accent_green'], 
                fg=colors['text_white'],
                padx=10, pady=5).pack(side="left")
        
        # Color palette
        palette_frame = tk.Frame(content, bg=colors['bg_secondary'])
        palette_frame.pack(fill="x", pady=5)
        
        color_samples = [colors['accent_blue'], colors['accent_green'], 
                        colors['accent_red'], colors['accent_orange']]
        
        for i, color in enumerate(color_samples):
            color_box = tk.Frame(palette_frame, bg=color, width=20, height=20)
            color_box.pack(side="left", padx=2)
        
        return preview_frame
    
    def create_theme_selector(self, parent):
        """Create theme selection widget"""
        selector_frame = tk.Frame(parent)
        selector_frame.pack(fill="x", pady=10)
        
        tk.Label(selector_frame, text="Choose Theme:", 
                font=("Segoe UI", 12, "bold")).pack(anchor="w")
        
        # Theme buttons
        themes_frame = tk.Frame(selector_frame)
        themes_frame.pack(fill="x", pady=10)
        
        for theme_id, theme_name in self.get_available_themes():
            btn = tk.Button(themes_frame, 
                          text=theme_name,
                          command=lambda t=theme_id: self.apply_theme(t),
                          padx=15, pady=8)
            btn.pack(side="left", padx=5)
        
        return selector_frame

def create_theme_manager(root):
    """Create and return theme manager instance"""
    return AdvancedThemeManager(root)
