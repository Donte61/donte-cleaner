"""
Modern Themes Page for DonTe Cleaner v3.0
"""

import tkinter as tk
from tkinter import messagebox
from gui.modern_ui import HolographicCard, AnimatedButton

class ThemesPage:
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.colors = main_window.colors
        self.current_theme = "Dark Modern"
        
        # Create themes interface
        self.create_themes_interface()
    
    def create_themes_interface(self):
        """Create themes interface"""
        main_frame = tk.Frame(self.parent, bg=self.colors['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Theme selection
        self.create_theme_selection(main_frame)
        
        # Color customization
        self.create_color_customization(main_frame)
        
        # Preview section
        self.create_preview_section(main_frame)
    
    def create_header(self, parent):
        """Create header section"""
        header_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Title
        title_label = tk.Label(header_frame, text="🎨 Theme Manager",
                              bg=self.colors['bg_primary'], fg=self.colors['accent_secondary'],
                              font=('Segoe UI', 24, 'bold'))
        title_label.pack(side='left')
        
        # Apply theme button
        self.apply_btn = AnimatedButton(header_frame, text="✨ Apply Theme",
                                       width=150, height=40,
                                       bg_color=self.colors['accent_secondary'],
                                       hover_color='#ff4081',
                                       text_color='white',
                                       command=self.apply_theme)
        self.apply_btn.pack(side='right')
    
    def create_theme_selection(self, parent):
        """Create theme selection section"""
        selection_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        selection_frame.pack(fill='x', pady=(0, 20))
        
        # Preset themes card
        themes_card = HolographicCard(selection_frame, width=800, height=300,
                                     title="🎭 Preset Themes")
        themes_card.pack()
        
        # Theme options
        themes = [
            {
                "name": "Dark Modern",
                "description": "Sleek dark interface with cyan accents",
                "preview_bg": "#0d1117",
                "preview_accent": "#00d8ff",
                "is_current": True
            },
            {
                "name": "Light Modern", 
                "description": "Clean light interface with blue accents",
                "preview_bg": "#ffffff",
                "preview_accent": "#0066cc",
                "is_current": False
            },
            {
                "name": "Cyberpunk",
                "description": "Neon-styled interface with purple/pink",
                "preview_bg": "#0a0a0a",
                "preview_accent": "#ff00ff",
                "is_current": False
            },
            {
                "name": "Gaming",
                "description": "High-contrast gaming-focused design",
                "preview_bg": "#001122",
                "preview_accent": "#00ff00",
                "is_current": False
            }
        ]
        
        # Create theme selection grid
        theme_frame = tk.Frame(themes_card, bg=self.colors['bg_tertiary'])
        theme_frame.place(x=50, y=60)
        
        self.selected_theme = tk.StringVar(value="Dark Modern")
        
        for i, theme in enumerate(themes):
            row = i // 2
            col = i % 2
            
            # Theme container
            container = tk.Frame(theme_frame, bg=self.colors['bg_secondary'], 
                                relief='raised', bd=2)
            container.grid(row=row, column=col, padx=15, pady=15, sticky='w')
            
            # Theme preview
            preview = tk.Frame(container, bg=theme['preview_bg'], 
                             width=150, height=80)
            preview.pack(side='left', padx=10, pady=10)
            preview.pack_propagate(False)
            
            # Preview accent
            accent = tk.Frame(preview, bg=theme['preview_accent'], 
                            width=130, height=10)
            accent.place(x=10, y=60)
            
            # Theme info
            info_frame = tk.Frame(container, bg=self.colors['bg_secondary'])
            info_frame.pack(side='left', padx=10, pady=10, fill='y')
            
            # Theme name with radio button
            name_frame = tk.Frame(info_frame, bg=self.colors['bg_secondary'])
            name_frame.pack(anchor='w')
            
            radio = tk.Radiobutton(name_frame, text=theme['name'],
                                  variable=self.selected_theme,
                                  value=theme['name'],
                                  bg=self.colors['bg_secondary'],
                                  fg=self.colors['text_primary'],
                                  selectcolor=self.colors['bg_tertiary'],
                                  font=('Segoe UI', 12, 'bold'),
                                  command=self.theme_selected)
            radio.pack(side='left')
            
            if theme['is_current']:
                current_label = tk.Label(name_frame, text="(Current)",
                                       bg=self.colors['bg_secondary'],
                                       fg=self.colors['success'],
                                       font=('Segoe UI', 9))
                current_label.pack(side='left', padx=(5, 0))
            
            # Description
            desc_label = tk.Label(info_frame, text=theme['description'],
                                 bg=self.colors['bg_secondary'],
                                 fg=self.colors['text_secondary'],
                                 font=('Segoe UI', 9),
                                 wraplength=200)
            desc_label.pack(anchor='w', pady=(5, 0))
    
    def create_color_customization(self, parent):
        """Create color customization section"""
        custom_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        custom_frame.pack(fill='x', pady=(0, 20))
        
        # Color picker card
        color_card = HolographicCard(custom_frame, width=380, height=250,
                                    title="🎨 Color Customization")
        color_card.pack(side='left', padx=(0, 20))
        
        # Color options
        colors = [
            ("Primary Accent", "#00d8ff"),
            ("Secondary Accent", "#ff0080"),
            ("Success Color", "#00ff80"),
            ("Warning Color", "#ffd700"),
            ("Danger Color", "#ff4444")
        ]
        
        for i, (name, color) in enumerate(colors):
            color_frame = tk.Frame(color_card, bg=self.colors['bg_tertiary'])
            color_frame.place(x=20, y=60 + i * 35)
            
            # Color preview
            color_preview = tk.Frame(color_frame, bg=color, width=30, height=20)
            color_preview.pack(side='left', padx=(0, 10))
            color_preview.pack_propagate(False)
            
            # Color name
            color_label = tk.Label(color_frame, text=name,
                                  bg=self.colors['bg_tertiary'],
                                  fg=self.colors['text_primary'],
                                  font=('Segoe UI', 10))
            color_label.pack(side='left')
            
            # Change button
            change_btn = AnimatedButton(color_frame, text="Change",
                                       width=60, height=20,
                                       bg_color=self.colors['bg_secondary'],
                                       hover_color=self.colors['accent_primary'],
                                       text_color=self.colors['text_primary'],
                                       command=lambda c=color: self.change_color(c))
            change_btn.pack(side='right')
        
        # Font settings card
        font_card = HolographicCard(custom_frame, width=380, height=250,
                                   title="🔤 Font Settings")
        font_card.pack(side='left')
        
        # Font family
        font_family_label = tk.Label(font_card, text="Font Family:",
                                    bg=self.colors['bg_tertiary'],
                                    fg=self.colors['text_primary'],
                                    font=('Segoe UI', 11, 'bold'))
        font_family_label.place(x=20, y=60)
        
        self.font_var = tk.StringVar(value="Segoe UI")
        font_combo = tk.OptionMenu(font_card, self.font_var,
                                  "Segoe UI", "Arial", "Calibri", "Consolas", "Times New Roman")
        font_combo.config(bg=self.colors['bg_secondary'], fg=self.colors['text_primary'])
        font_combo.place(x=20, y=85)
        
        # Font size
        size_label = tk.Label(font_card, text="UI Scale:",
                             bg=self.colors['bg_tertiary'],
                             fg=self.colors['text_primary'],
                             font=('Segoe UI', 11, 'bold'))
        size_label.place(x=20, y=130)
        
        self.scale_var = tk.DoubleVar(value=1.0)
        scale_frame = tk.Frame(font_card, bg=self.colors['bg_tertiary'])
        scale_frame.place(x=20, y=155)
        
        scale_slider = tk.Scale(scale_frame, from_=0.8, to=1.5, resolution=0.1,
                               variable=self.scale_var, orient='horizontal',
                               bg=self.colors['bg_secondary'],
                               fg=self.colors['text_primary'],
                               troughcolor=self.colors['bg_primary'])
        scale_slider.pack()
        
        # Animation settings
        anim_label = tk.Label(font_card, text="Animations:",
                             bg=self.colors['bg_tertiary'],
                             fg=self.colors['text_primary'],
                             font=('Segoe UI', 11, 'bold'))
        anim_label.place(x=200, y=60)
        
        self.animations_var = tk.BooleanVar(value=True)
        anim_check = tk.Checkbutton(font_card, text="Enable animations",
                                   variable=self.animations_var,
                                   bg=self.colors['bg_tertiary'],
                                   fg=self.colors['text_primary'],
                                   selectcolor=self.colors['bg_secondary'],
                                   font=('Segoe UI', 10))
        anim_check.place(x=200, y=85)
        
        self.particles_var = tk.BooleanVar(value=True)
        particles_check = tk.Checkbutton(font_card, text="Particle effects",
                                        variable=self.particles_var,
                                        bg=self.colors['bg_tertiary'],
                                        fg=self.colors['text_primary'],
                                        selectcolor=self.colors['bg_secondary'],
                                        font=('Segoe UI', 10))
        particles_check.place(x=200, y=110)
    
    def create_preview_section(self, parent):
        """Create theme preview section"""
        preview_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        preview_frame.pack(fill='x')
        
        # Preview card
        preview_card = HolographicCard(preview_frame, width=800, height=200,
                                      title="👁️ Theme Preview")
        preview_card.pack()
        
        # Preview content
        preview_content = tk.Frame(preview_card, bg=self.colors['bg_secondary'])
        preview_content.place(x=50, y=60)
        
        # Sample UI elements
        sample_label = tk.Label(preview_content, text="Sample Interface Elements",
                               bg=self.colors['bg_secondary'],
                               fg=self.colors['text_primary'],
                               font=('Segoe UI', 14, 'bold'))
        sample_label.pack(pady=5)
        
        # Sample buttons
        btn_frame = tk.Frame(preview_content, bg=self.colors['bg_secondary'])
        btn_frame.pack(pady=10)
        
        primary_btn = AnimatedButton(btn_frame, text="Primary Button",
                                    width=120, height=30,
                                    bg_color=self.colors['accent_primary'],
                                    hover_color='#00ff80',
                                    text_color='black',
                                    command=lambda: None)
        primary_btn.pack(side='left', padx=5)
        
        secondary_btn = AnimatedButton(btn_frame, text="Secondary",
                                      width=120, height=30,
                                      bg_color=self.colors['accent_secondary'],
                                      hover_color='#ff4081',
                                      text_color='white',
                                      command=lambda: None)
        secondary_btn.pack(side='left', padx=5)
        
        success_btn = AnimatedButton(btn_frame, text="Success",
                                    width=120, height=30,
                                    bg_color=self.colors['success'],
                                    hover_color='#4caf50',
                                    text_color='white',
                                    command=lambda: None)
        success_btn.pack(side='left', padx=5)
        
        # Sample text
        text_frame = tk.Frame(preview_content, bg=self.colors['bg_secondary'])
        text_frame.pack(pady=5)
        
        primary_text = tk.Label(text_frame, text="Primary text color",
                               bg=self.colors['bg_secondary'],
                               fg=self.colors['text_primary'],
                               font=('Segoe UI', 10))
        primary_text.pack()
        
        secondary_text = tk.Label(text_frame, text="Secondary text color",
                                 bg=self.colors['bg_secondary'],
                                 fg=self.colors['text_secondary'],
                                 font=('Segoe UI', 9))
        secondary_text.pack()
        
        # Action buttons
        action_frame = tk.Frame(preview_card, bg=self.colors['bg_tertiary'])
        action_frame.place(x=500, y=80)
        
        export_btn = AnimatedButton(action_frame, text="📁 Export Theme",
                                   width=120, height=30,
                                   bg_color=self.colors['accent_gold'],
                                   hover_color='#ffed4a',
                                   text_color='black',
                                   command=self.export_theme)
        export_btn.pack(pady=5)
        
        import_btn = AnimatedButton(action_frame, text="📥 Import Theme",
                                   width=120, height=30,
                                   bg_color=self.colors['bg_secondary'],
                                   hover_color=self.colors['accent_primary'],
                                   text_color=self.colors['text_primary'],
                                   command=self.import_theme)
        import_btn.pack(pady=5)
        
        reset_btn = AnimatedButton(action_frame, text="🔄 Reset to Default",
                                  width=120, height=30,
                                  bg_color=self.colors['danger'],
                                  hover_color='#f44336',
                                  text_color='white',
                                  command=self.reset_theme)
        reset_btn.pack(pady=5)
    
    def theme_selected(self):
        """Handle theme selection"""
        selected = self.selected_theme.get()
        
        # Show what theme was selected
        self.show_notification(f"Selected theme: {selected}", "info")
    
    def apply_theme(self):
        """Apply the selected theme"""
        selected = self.selected_theme.get()
        
        # Show applying notification
        self.show_notification(f"Applying {selected} theme...", "info")
        
        # Simulate theme application
        self.main_window.root.after(1000, lambda: self.theme_applied(selected))
    
    def theme_applied(self, theme_name):
        """Handle theme application completion"""
        self.current_theme = theme_name
        
        # Play theme change sound
        if hasattr(self.main_window, 'sound_effects'):
            self.main_window.sound_effects.play_theme_change()
        
        # Show success notification
        self.show_notification(f"✅ {theme_name} theme applied successfully!", "success")
    
    def change_color(self, current_color):
        """Change a specific color"""
        self.show_notification(f"Color picker for {current_color} would open here", "info")
    
    def export_theme(self):
        """Export current theme"""
        self.show_notification("Theme exported successfully!", "success")
    
    def import_theme(self):
        """Import a theme"""
        self.show_notification("Theme import dialog would open here", "info")
    
    def reset_theme(self):
        """Reset to default theme"""
        if messagebox.askyesno("Reset Theme", "Reset to default Dark Modern theme?"):
            self.selected_theme.set("Dark Modern")
            self.show_notification("Theme reset to Dark Modern", "success")
    
    def show_notification(self, message, type="info"):
        """Show notification to user"""
        # Create a temporary notification label
        notification = tk.Toplevel(self.main_window.root)
        notification.title("Theme Manager")
        notification.geometry("400x100")
        notification.configure(bg=self.colors['bg_secondary'])
        notification.transient(self.main_window.root)
        notification.grab_set()
        
        # Center the notification
        notification.update_idletasks()
        x = (notification.winfo_screenwidth() // 2) - (200)
        y = (notification.winfo_screenheight() // 2) - (50)
        notification.geometry(f"400x100+{x}+{y}")
        
        # Notification content
        if type == "success":
            bg_color = self.colors['success']
            icon = "✅"
        elif type == "warning":
            bg_color = self.colors['accent_gold'] 
            icon = "⚠️"
        elif type == "error":
            bg_color = self.colors['danger']
            icon = "❌"
        else:
            bg_color = self.colors['accent_primary']
            icon = "ℹ️"
        
        label = tk.Label(notification, text=f"{icon} {message}",
                        bg=bg_color, fg='white',
                        font=('Segoe UI', 11, 'bold'),
                        wraplength=350)
        label.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Auto-close after 3 seconds
        notification.after(3000, notification.destroy)
