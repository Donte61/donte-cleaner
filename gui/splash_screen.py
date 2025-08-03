"""
DonTe Cleaner - Modern Splash Screen
Professional startup screen with animations
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import math

class ModernSplashScreen:
    def __init__(self, parent, duration=3000):
        self.parent = parent
        self.duration = duration
        self.splash = None
        self.animation_running = True
        self.progress_value = 0
        
        # Modern colors
        self.colors = {
            'bg_primary': '#0d1117',      # GitHub dark background
            'bg_secondary': '#161b22',     # Slightly lighter
            'accent_blue': '#58a6ff',      # GitHub blue
            'accent_green': '#3fb950',     # GitHub green
            'accent_purple': '#a5a5ff',    # Light purple
            'text_white': '#f0f6fc',       # White text
            'text_gray': '#8b949e',        # Gray text
            'border': '#30363d'            # Border color
        }
        
        self.create_splash()
        self.start_animation()
    
    def create_safe_progressbar(self, parent, style="TProgressbar", **kwargs):
        """Create a progressbar with fallback styling"""
        try:
            # Try with custom style first
            return ttk.Progressbar(parent, style=style, **kwargs)
        except tk.TclError:
            try:
                # Try with basic TProgressbar
                return ttk.Progressbar(parent, style="TProgressbar", **kwargs)
            except tk.TclError:
                # Last resort - no style
                return ttk.Progressbar(parent, **kwargs)
    
    def create_splash(self):
        """Create modern splash screen"""
        # Create splash window
        self.splash = tk.Toplevel()
        self.splash.title("DonTe Cleaner")
        self.splash.geometry("500x350")
        self.splash.configure(bg=self.colors['bg_primary'])
        self.splash.resizable(False, False)
        self.splash.overrideredirect(True)  # Remove window decorations
        
        # Center on screen
        self.center_window()
        
        # Main container with gradient effect
        main_frame = tk.Frame(self.splash, bg=self.colors['bg_primary'])
        main_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Create border effect
        border_frame = tk.Frame(main_frame, bg=self.colors['accent_blue'], height=2)
        border_frame.pack(fill="x", side="top")
        
        # Content area
        content_frame = tk.Frame(main_frame, bg=self.colors['bg_secondary'])
        content_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Logo area
        self.create_logo_section(content_frame)
        
        # Title and version
        self.create_title_section(content_frame)
        
        # Loading section
        self.create_loading_section(content_frame)
        
        # Status text
        self.status_label = tk.Label(content_frame, 
                                   text="Initializing...",
                                   font=("Segoe UI", 10),
                                   fg=self.colors['text_gray'],
                                   bg=self.colors['bg_secondary'])
        self.status_label.pack(pady=(10, 5))
        
        # Copyright
        copyright_label = tk.Label(content_frame,
                                 text="© 2025 DonTe Cleaner - Professional Windows Optimizer",
                                 font=("Segoe UI", 8),
                                 fg=self.colors['text_gray'],
                                 bg=self.colors['bg_secondary'])
        copyright_label.pack(side="bottom", pady=(0, 15))
    
    def create_logo_section(self, parent):
        """Create animated logo section"""
        logo_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        logo_frame.pack(pady=(30, 10))
        
        # Create ASCII art logo
        logo_text = """
    ██████╗  ██████╗ ███╗   ██╗████████╗███████╗
    ██╔══██╗██╔═══██╗████╗  ██║╚══██╔══╝██╔════╝
    ██║  ██║██║   ██║██╔██╗ ██║   ██║   █████╗  
    ██║  ██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  
    ██████╔╝╚██████╔╝██║ ╚████║   ██║   ███████╗
    ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝
        """
        
        self.logo_label = tk.Label(logo_frame,
                                 text=logo_text,
                                 font=("Consolas", 8, "bold"),
                                 fg=self.colors['accent_blue'],
                                 bg=self.colors['bg_secondary'],
                                 justify="center")
        self.logo_label.pack()
    
    def create_title_section(self, parent):
        """Create title and version section"""
        title_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        title_frame.pack(pady=(0, 20))
        
        # Main title
        title_label = tk.Label(title_frame,
                             text="DonTe Cleaner",
                             font=("Segoe UI", 24, "bold"),
                             fg=self.colors['text_white'],
                             bg=self.colors['bg_secondary'])
        title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(title_frame,
                                text="Professional Windows Optimizer",
                                font=("Segoe UI", 12),
                                fg=self.colors['accent_green'],
                                bg=self.colors['bg_secondary'])
        subtitle_label.pack(pady=(5, 0))
        
        # Version
        version_label = tk.Label(title_frame,
                               text="Version 2.0 - Advanced Edition",
                               font=("Segoe UI", 10),
                               fg=self.colors['text_gray'],
                               bg=self.colors['bg_secondary'])
        version_label.pack(pady=(5, 0))
    
    def create_loading_section(self, parent):
        """Create modern loading section"""
        loading_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        loading_frame.pack(pady=(20, 10))
        
        # Progress bar with custom style
        style = ttk.Style()
        try:
            style.configure("Splash.TProgressbar",
                           background=self.colors['accent_blue'],
                           bordercolor=self.colors['border'],
                           lightcolor=self.colors['accent_blue'],
                           darkcolor=self.colors['accent_blue'],
                           troughcolor=self.colors['bg_primary'],
                           borderwidth=1,
                           relief="flat")
            
            self.progress_bar = self.create_safe_progressbar(loading_frame,
                                                           style="Splash.TProgressbar",
                                                           length=300,
                                                           mode='determinate',
                                                           maximum=100)
        except Exception:
            # Fallback to basic progressbar
            self.progress_bar = self.create_safe_progressbar(loading_frame,
                                                           length=300,
                                                           mode='determinate',
                                                           maximum=100)
        self.progress_bar.pack(pady=(0, 10))
        
        # Loading dots animation
        self.loading_dots = tk.Label(loading_frame,
                                   text="●○○○○",
                                   font=("Segoe UI", 16),
                                   fg=self.colors['accent_purple'],
                                   bg=self.colors['bg_secondary'])
        self.loading_dots.pack()
    
    def center_window(self):
        """Center splash screen on monitor"""
        self.splash.update_idletasks()
        x = (self.splash.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.splash.winfo_screenheight() // 2) - (350 // 2)
        self.splash.geometry(f"500x350+{x}+{y}")
    
    def start_animation(self):
        """Start splash screen animations"""
        # Start animations directly without threading
        self.animate_progress()
        self.animate_loading_dots()
        self.animate_logo_glow()
        
        # Auto-close after duration
        self.splash.after(self.duration, self.close_splash)
    
    def animate_progress(self):
        """Animate progress bar"""
        steps = ["Initializing system...", 
                "Loading modules...", 
                "Checking privileges...", 
                "Setting up interface...", 
                "Ready!"]
        
        def update_step(step_index):
            if not self.animation_running or step_index >= len(steps):
                return
                
            progress = (step_index + 1) * 20
            
            # Update progress bar safely
            try:
                self.progress_bar.config(value=progress)
                self.status_label.config(text=steps[step_index])
            except tk.TclError:
                return
            
            # Schedule next update
            self.splash.after(500, lambda: update_step(step_index + 1))
        
        # Start the animation
        update_step(0)
    
    def animate_loading_dots(self):
        """Animate loading dots"""
        dots_patterns = [
            "●○○○○", "○●○○○", "○○●○○", "○○○●○", "○○○○●",
            "○○○●○", "○○●○○", "○●○○○", "●○○○○"
        ]
        
        def update_dots(pattern_index):
            if not self.animation_running:
                return
                
            pattern = dots_patterns[pattern_index % len(dots_patterns)]
            try:
                self.loading_dots.config(text=pattern)
            except tk.TclError:
                return
            
            # Schedule next update
            self.splash.after(200, lambda: update_dots(pattern_index + 1))
        
        # Start animation
        update_dots(0)
    
    def animate_logo_glow(self):
        """Animate logo glow effect"""
        colors = [self.colors['accent_blue'], self.colors['accent_purple'], 
                 self.colors['accent_green'], self.colors['accent_blue']]
        
        def update_glow(color_index):
            if not self.animation_running:
                return
                
            color = colors[color_index % len(colors)]
            try:
                self.logo_label.config(fg=color)
            except tk.TclError:
                return
            
            # Schedule next update
            self.splash.after(800, lambda: update_glow(color_index + 1))
        
        # Start animation
        update_glow(0)
    
    def close_splash(self):
        """Close splash screen with fade effect"""
        global _splash_instance
        
        self.animation_running = False
        
        # Fade out effect
        for alpha in range(100, 0, -5):
            try:
                if self.splash and self.splash.winfo_exists():
                    self.splash.attributes("-alpha", alpha / 100)
                    time.sleep(0.03)
                else:
                    break
            except:
                break
        
        try:
            if self.splash and self.splash.winfo_exists():
                self.splash.destroy()
                self.splash = None
        except:
            pass
        
        # Clear global instance
        if _splash_instance == self:
            _splash_instance = None
            pass
    
    def show(self):
        """Show splash screen"""
        if self.splash:
            self.splash.lift()
            self.splash.attributes("-topmost", True)
            return self.splash

# Global splash instance to prevent duplicates
_splash_instance = None

def show_splash_screen(parent, duration=3000):
    """Show splash screen and return the splash object"""
    global _splash_instance
    
    # If splash is already shown, return existing instance
    if _splash_instance and _splash_instance.splash and _splash_instance.splash.winfo_exists():
        return _splash_instance.splash
    
    # Create new splash instance
    _splash_instance = ModernSplashScreen(parent, duration)
    return _splash_instance.show()
