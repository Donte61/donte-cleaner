"""
Modern Settings Page for DonTe Cleaner v3.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from gui.modern_ui import HolographicCard, AnimatedButton, StatusIndicator

class SettingsPage:
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.colors = main_window.colors
        self.settings_file = "config/settings.json"
        
        # Comprehensive settings data
        self.settings = {
            'general': {
                'auto_start': False,
                'notifications_enabled': True,
                'sound_enabled': True,
                'startup_scan': True,
                'minimize_to_tray': True,
                'check_updates': True,
                'send_statistics': False,
                'auto_optimization': False,
                'language': 'turkish'
            },
            'performance': {
                'scan_threads': 4,
                'memory_limit': 512,
                'cleanup_schedule': 'weekly',
                'deep_scan': False,
                'real_time_protection': True,
                'gaming_mode_auto': False,
                'temp_cleanup_size': 100,
                'scan_frequency': 'weekly'
            },
            'interface': {
                'animations': True,
                'sound_effects': True,
                'transparency': 0.95,
                'language': 'turkish',
                'theme': 'dark',
                'admin_mode_warning': True
            },
            'security': {
                'quarantine_suspicious': True,
                'scan_archives': True,
                'scan_network_drives': False,
                'auto_quarantine': False,
                'firewall_integration': True,
                'backup_enabled': True
            },
            'advanced': {
                'log_level': 'info',
                'debug_mode': False,
                'crash_reports': True,
                'telemetry': False
            }
        }
        
        # Load settings
        self.load_settings()
        
        # Create settings interface
        self.create_settings_interface()
    
    def load_settings(self):
        """Load settings from file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    saved_settings = json.load(f)
                    # Merge saved settings with defaults
                    for category, values in saved_settings.items():
                        if category in self.settings:
                            self.settings[category].update(values)
                print(f"[SETTINGS] Loaded settings from {self.settings_file}")
        except Exception as e:
            print(f"[SETTINGS] Error loading settings: {e}")
    
    def save_settings(self):
        """Save settings to file"""
        try:
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            print(f"[SETTINGS] Settings saved to {self.settings_file}")
            return True
        except Exception as e:
            print(f"[SETTINGS] Error saving settings: {e}")
            return False
    
    def create_settings_interface(self):
        """Create modern settings interface"""
        main_frame = tk.Frame(self.parent, bg=self.colors['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Settings sections in a scrollable frame
        self.create_settings_sections(main_frame)
        
        # Action buttons
        self.create_action_buttons(main_frame)
    
    def create_header(self, parent):
        """Create modern header section"""
        header_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Title with modern styling
        title_label = tk.Label(header_frame, text="⚙️ SETTINGS CONTROL CENTER",
                              bg=self.colors['bg_primary'], fg=self.colors['accent_primary'],
                              font=('Segoe UI', 22, 'bold'))
        title_label.pack(side='left')
        
        # Status indicator with glow effect
        status_frame = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        status_frame.pack(side='right')
        
        status_indicator = tk.Label(status_frame, text="●",
                                   bg=self.colors['bg_primary'], fg=self.colors['success'],
                                   font=('Segoe UI', 16))
        status_indicator.pack(side='right')
        
        status_text = tk.Label(status_frame, text="SYSTEM READY",
                              bg=self.colors['bg_primary'], fg=self.colors['success'],
                              font=('Segoe UI', 10, 'bold'))
        status_text.pack(side='right', padx=(0, 10))
    
    def create_settings_sections(self, parent):
        """Create organized settings sections"""
        sections_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        sections_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        # Create notebook for tabbed interface
        self.notebook = ttk.Notebook(sections_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Style the notebook
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=self.colors['bg_primary'])
        style.configure('TNotebook.Tab', background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'], padding=[20, 10])
        
        # Create tabs
        self.create_general_tab()
        self.create_performance_tab()
        self.create_interface_tab()
        self.create_security_tab()
        self.create_advanced_tab()
    
    def create_general_tab(self):
        """Create general settings tab"""
        tab_frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(tab_frame, text="🔧 General")
        
        # Auto start setting
        auto_start_card = HolographicCard(tab_frame, width=750, height=120,
                                         title="🚀 Startup Settings")
        auto_start_card.pack(pady=10, padx=20)
        
        self.auto_start_var = tk.BooleanVar(value=self.settings['general']['auto_start'])
        auto_start_check = tk.Checkbutton(auto_start_card, 
                                         text="Start DonTe Cleaner with Windows",
                                         variable=self.auto_start_var,
                                         bg=self.colors['bg_tertiary'],
                                         fg=self.colors['text_primary'],
                                         selectcolor=self.colors['bg_secondary'],
                                         font=('Segoe UI', 11))
        auto_start_check.place(x=20, y=60)
        
        # Notifications
        notifications_card = HolographicCard(tab_frame, width=750, height=180,
                                           title="🔔 Notification Settings")
        notifications_card.pack(pady=10, padx=20)
        
        self.notifications_var = tk.BooleanVar(value=self.settings['general']['notifications_enabled'])
        notifications_check = tk.Checkbutton(notifications_card,
                                            text="Enable system notifications",
                                            variable=self.notifications_var,
                                            bg=self.colors['bg_tertiary'],
                                            fg=self.colors['text_primary'],
                                            selectcolor=self.colors['bg_secondary'],
                                            font=('Segoe UI', 11))
        notifications_check.place(x=20, y=60)
        
        self.sound_var = tk.BooleanVar(value=self.settings['general']['sound_enabled'])
        sound_check = tk.Checkbutton(notifications_card,
                                    text="Enable sound effects",
                                    variable=self.sound_var,
                                    bg=self.colors['bg_tertiary'],
                                    fg=self.colors['text_primary'],
                                    selectcolor=self.colors['bg_secondary'],
                                    font=('Segoe UI', 11))
        sound_check.place(x=20, y=90)
        
        self.updates_var = tk.BooleanVar(value=self.settings['general']['check_updates'])
        updates_check = tk.Checkbutton(notifications_card,
                                      text="Check for updates automatically",
                                      variable=self.updates_var,
                                      bg=self.colors['bg_tertiary'],
                                      fg=self.colors['text_primary'],
                                      selectcolor=self.colors['bg_secondary'],
                                      font=('Segoe UI', 11))
        updates_check.place(x=20, y=120)
    
    def create_performance_tab(self):
        """Create performance settings tab"""
        tab_frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(tab_frame, text="⚡ Performance")
        
        # Optimization settings
        opt_card = HolographicCard(tab_frame, width=750, height=200,
                                  title="⚡ Optimization Settings")
        opt_card.pack(pady=10, padx=20)
        
        self.auto_opt_var = tk.BooleanVar(value=self.settings['general']['auto_optimization'])
        auto_opt_check = tk.Checkbutton(opt_card,
                                       text="Enable automatic optimization",
                                       variable=self.auto_opt_var,
                                       bg=self.colors['bg_tertiary'],
                                       fg=self.colors['text_primary'],
                                       selectcolor=self.colors['bg_secondary'],
                                       font=('Segoe UI', 11))
        auto_opt_check.place(x=20, y=60)
        
        # Scan frequency
        freq_label = tk.Label(opt_card, text="Scan Frequency:",
                             bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                             font=('Segoe UI', 11, 'bold'))
        freq_label.place(x=20, y=100)
        
        self.scan_freq_var = tk.StringVar(value=self.settings['performance']['scan_frequency'])
        freq_combo = ttk.Combobox(opt_card, textvariable=self.scan_freq_var,
                                 values=['daily', 'weekly', 'monthly', 'manual'],
                                 state='readonly', width=15, font=('Segoe UI', 10))
        freq_combo.place(x=150, y=100)
        
        # Gaming mode
        self.gaming_auto_var = tk.BooleanVar(value=self.settings['performance']['gaming_mode_auto'])
        gaming_check = tk.Checkbutton(opt_card,
                                     text="Auto-activate gaming mode for games",
                                     variable=self.gaming_auto_var,
                                     bg=self.colors['bg_tertiary'],
                                     fg=self.colors['text_primary'],
                                     selectcolor=self.colors['bg_secondary'],
                                     font=('Segoe UI', 11))
        gaming_check.place(x=20, y=140)
        
        # Memory settings
        memory_card = HolographicCard(tab_frame, width=750, height=150,
                                     title="💾 Memory & Storage")
        memory_card.pack(pady=10, padx=20)
        
        # Temp cleanup size
        size_label = tk.Label(memory_card, text="Temp cleanup threshold (MB):",
                             bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                             font=('Segoe UI', 11, 'bold'))
        size_label.place(x=20, y=60)
        
        self.temp_size_var = tk.StringVar(value=str(self.settings['performance']['temp_cleanup_size']))
        size_entry = tk.Entry(memory_card, textvariable=self.temp_size_var,
                             bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                             width=10, font=('Segoe UI', 10))
        size_entry.place(x=250, y=60)
        
        # Threads
        threads_label = tk.Label(memory_card, text="Scan threads:",
                                bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                font=('Segoe UI', 11, 'bold'))
        threads_label.place(x=20, y=100)
        
        self.threads_var = tk.StringVar(value=str(self.settings['performance']['scan_threads']))
        threads_entry = tk.Entry(memory_card, textvariable=self.threads_var,
                                bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                                width=5, font=('Segoe UI', 10))
        threads_entry.place(x=130, y=100)
    
    def create_interface_tab(self):
        """Create interface settings tab"""
        tab_frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(tab_frame, text="🎨 Interface")
        
        # Theme settings
        theme_card = HolographicCard(tab_frame, width=750, height=200,
                                    title="🎨 Theme & Appearance")
        theme_card.pack(pady=10, padx=20)
        
        # Theme selection
        theme_label = tk.Label(theme_card, text="Theme:",
                              bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                              font=('Segoe UI', 11, 'bold'))
        theme_label.place(x=20, y=60)
        
        self.theme_var = tk.StringVar(value=self.settings['interface']['theme'])
        theme_combo = ttk.Combobox(theme_card, textvariable=self.theme_var,
                                  values=['dark', 'light', 'auto', 'gaming'],
                                  state='readonly', width=15, font=('Segoe UI', 10))
        theme_combo.place(x=100, y=60)
        
        # Language
        lang_label = tk.Label(theme_card, text="Language:",
                             bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                             font=('Segoe UI', 11, 'bold'))
        lang_label.place(x=300, y=60)
        
        self.language_var = tk.StringVar(value=self.settings['interface']['language'])
        language_combo = ttk.Combobox(theme_card, textvariable=self.language_var,
                                     values=['turkish', 'english', 'german', 'french'],
                                     state='readonly', width=15, font=('Segoe UI', 10))
        language_combo.place(x=380, y=60)
        
        # Animations
        self.animations_var = tk.BooleanVar(value=self.settings['interface']['animations'])
        animations_check = tk.Checkbutton(theme_card,
                                         text="Enable UI animations",
                                         variable=self.animations_var,
                                         bg=self.colors['bg_tertiary'],
                                         fg=self.colors['text_primary'],
                                         selectcolor=self.colors['bg_secondary'],
                                         font=('Segoe UI', 11))
        animations_check.place(x=20, y=100)
        
        # Transparency
        transparency_label = tk.Label(theme_card, text="Window transparency:",
                                     bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                     font=('Segoe UI', 11, 'bold'))
        transparency_label.place(x=20, y=140)
        
        self.transparency_var = tk.DoubleVar(value=self.settings['interface']['transparency'])
        transparency_scale = tk.Scale(theme_card, variable=self.transparency_var,
                                     from_=0.5, to=1.0, resolution=0.05,
                                     orient='horizontal', length=200,
                                     bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                     font=('Segoe UI', 9))
        transparency_scale.place(x=200, y=120)
    
    def create_security_tab(self):
        """Create security settings tab"""
        tab_frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(tab_frame, text="🔒 Security")
        
        # Security settings
        security_card = HolographicCard(tab_frame, width=750, height=250,
                                       title="🔒 Security & Privacy")
        security_card.pack(pady=10, padx=20)
        
        self.backup_var = tk.BooleanVar(value=self.settings['security']['backup_enabled'])
        backup_check = tk.Checkbutton(security_card,
                                     text="Enable automatic backups",
                                     variable=self.backup_var,
                                     bg=self.colors['bg_tertiary'],
                                     fg=self.colors['text_primary'],
                                     selectcolor=self.colors['bg_secondary'],
                                     font=('Segoe UI', 11))
        backup_check.place(x=20, y=60)
        
        self.quarantine_var = tk.BooleanVar(value=self.settings['security']['quarantine_suspicious'])
        quarantine_check = tk.Checkbutton(security_card,
                                         text="Quarantine suspicious files",
                                         variable=self.quarantine_var,
                                         bg=self.colors['bg_tertiary'],
                                         fg=self.colors['text_primary'],
                                         selectcolor=self.colors['bg_secondary'],
                                         font=('Segoe UI', 11))
        quarantine_check.place(x=20, y=90)
        
        self.archives_var = tk.BooleanVar(value=self.settings['security']['scan_archives'])
        archives_check = tk.Checkbutton(security_card,
                                       text="Scan archive files (ZIP, RAR, etc.)",
                                       variable=self.archives_var,
                                       bg=self.colors['bg_tertiary'],
                                       fg=self.colors['text_primary'],
                                       selectcolor=self.colors['bg_secondary'],
                                       font=('Segoe UI', 11))
        archives_check.place(x=20, y=120)
        
        self.real_time_var = tk.BooleanVar(value=self.settings['performance']['real_time_protection'])
        real_time_check = tk.Checkbutton(security_card,
                                        text="Enable real-time protection",
                                        variable=self.real_time_var,
                                        bg=self.colors['bg_tertiary'],
                                        fg=self.colors['text_primary'],
                                        selectcolor=self.colors['bg_secondary'],
                                        font=('Segoe UI', 11))
        real_time_check.place(x=20, y=150)
    
    def create_advanced_tab(self):
        """Create advanced settings tab"""
        tab_frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(tab_frame, text="🔬 Advanced")
        
        # Advanced settings
        advanced_card = HolographicCard(tab_frame, width=750, height=200,
                                       title="🔬 Advanced Configuration")
        advanced_card.pack(pady=10, padx=20)
        
        # Log level
        log_label = tk.Label(advanced_card, text="Log level:",
                            bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                            font=('Segoe UI', 11, 'bold'))
        log_label.place(x=20, y=60)
        
        self.log_level_var = tk.StringVar(value=self.settings['advanced']['log_level'])
        log_combo = ttk.Combobox(advanced_card, textvariable=self.log_level_var,
                                values=['debug', 'info', 'warning', 'error'],
                                state='readonly', width=15, font=('Segoe UI', 10))
        log_combo.place(x=120, y=60)
        
        # Debug mode
        self.debug_var = tk.BooleanVar(value=self.settings['advanced']['debug_mode'])
        debug_check = tk.Checkbutton(advanced_card,
                                    text="Enable debug mode (for troubleshooting)",
                                    variable=self.debug_var,
                                    bg=self.colors['bg_tertiary'],
                                    fg=self.colors['text_primary'],
                                    selectcolor=self.colors['bg_secondary'],
                                    font=('Segoe UI', 11))
        debug_check.place(x=20, y=100)
        
        # Export/Import buttons
        export_btn = AnimatedButton(advanced_card, text="📤 Export Settings",
                                   width=150, height=35,
                                   bg_color=self.colors['accent_primary'],
                                   hover_color=self.colors['glow'],
                                   text_color='white',
                                   command=self.export_settings)
        export_btn.place(x=400, y=60)
        
        import_btn = AnimatedButton(advanced_card, text="📥 Import Settings",
                                   width=150, height=35,
                                   bg_color=self.colors['accent_secondary'],
                                   hover_color='#ff4081',
                                   text_color='white',
                                   command=self.import_settings)
        import_btn.place(x=570, y=60)
        
        reset_btn = AnimatedButton(advanced_card, text="🔄 Reset to Defaults",
                                  width=300, height=35,
                                  bg_color=self.colors['danger'],
                                  hover_color='#ff4444',
                                  text_color='white',
                                  command=self.reset_to_defaults)
        reset_btn.place(x=400, y=110)
    
    def create_action_buttons(self, parent):
        """Create action buttons"""
        action_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        action_frame.pack(fill='x', pady=20)
        
        # Save button
        save_btn = AnimatedButton(action_frame, text="💾 Save All Settings",
                                 width=180, height=45,
                                 bg_color=self.colors['success'],
                                 hover_color='#4caf50',
                                 text_color='white',
                                 command=self.save_all_settings)
        save_btn.pack(side='right', padx=(10, 0))
        
        # Apply button
        apply_btn = AnimatedButton(action_frame, text="✅ Apply Changes",
                                  width=150, height=45,
                                  bg_color=self.colors['accent_primary'],
                                  hover_color=self.colors['glow'],
                                  text_color='white',
                                  command=self.apply_settings)
        apply_btn.pack(side='right', padx=(10, 0))
        
        # Test button
        test_btn = AnimatedButton(action_frame, text="🧪 Test Settings",
                                 width=130, height=45,
                                 bg_color=self.colors['accent_gold'],
                                 hover_color='#ffed4a',
                                 text_color='black',
                                 command=self.test_settings)
        test_btn.pack(side='right', padx=(10, 0))
        
        # Cancel button
        cancel_btn = AnimatedButton(action_frame, text="❌ Reset",
                                   width=100, height=45,
                                   bg_color=self.colors['bg_secondary'],
                                   hover_color=self.colors['border'],
                                   text_color=self.colors['text_primary'],
                                   command=self.cancel_changes)
        cancel_btn.pack(side='right')
    
    def collect_settings_from_ui(self):
        """Collect all settings from UI elements"""
        try:
            # General settings
            self.settings['general']['auto_start'] = self.auto_start_var.get()
            self.settings['general']['notifications_enabled'] = self.notifications_var.get()
            self.settings['general']['sound_enabled'] = self.sound_var.get()
            self.settings['general']['check_updates'] = self.updates_var.get()
            self.settings['general']['auto_optimization'] = self.auto_opt_var.get()
            self.settings['general']['language'] = self.language_var.get()
            
            # Performance settings
            self.settings['performance']['scan_frequency'] = self.scan_freq_var.get()
            self.settings['performance']['gaming_mode_auto'] = self.gaming_auto_var.get()
            self.settings['performance']['real_time_protection'] = self.real_time_var.get()
            
            # Validate numeric values
            try:
                temp_size = int(self.temp_size_var.get())
                if temp_size > 0:
                    self.settings['performance']['temp_cleanup_size'] = temp_size
            except ValueError:
                self.settings['performance']['temp_cleanup_size'] = 100
            
            try:
                threads = int(self.threads_var.get())
                if 1 <= threads <= 16:
                    self.settings['performance']['scan_threads'] = threads
            except ValueError:
                self.settings['performance']['scan_threads'] = 4
            
            # Interface settings
            self.settings['interface']['theme'] = self.theme_var.get()
            self.settings['interface']['language'] = self.language_var.get()
            self.settings['interface']['animations'] = self.animations_var.get()
            self.settings['interface']['transparency'] = self.transparency_var.get()
            
            # Security settings
            self.settings['security']['backup_enabled'] = self.backup_var.get()
            self.settings['security']['quarantine_suspicious'] = self.quarantine_var.get()
            self.settings['security']['scan_archives'] = self.archives_var.get()
            
            # Advanced settings
            self.settings['advanced']['log_level'] = self.log_level_var.get()
            self.settings['advanced']['debug_mode'] = self.debug_var.get()
            
            print("[SETTINGS] All settings collected from UI successfully")
            return True
        except Exception as e:
            print(f"[SETTINGS] Error collecting settings: {e}")
            return False
    
    def apply_settings(self):
        """Apply current settings without saving"""
        if self.collect_settings_from_ui():
            # Apply theme changes
            if hasattr(self.main_window, 'apply_theme'):
                self.main_window.apply_theme(self.settings['interface']['theme'])
            
            # Apply transparency
            if hasattr(self.main_window, 'root'):
                try:
                    self.main_window.root.attributes('-alpha', self.settings['interface']['transparency'])
                except:
                    pass
            
            messagebox.showinfo("Settings Applied", 
                               "Settings have been applied successfully!\n"
                               "Note: Some changes require restart to take full effect.")
            print("[SETTINGS] Settings applied successfully")
        else:
            messagebox.showerror("Apply Error", "Failed to apply settings")
    
    def save_all_settings(self):
        """Save all settings to file"""
        if self.collect_settings_from_ui():
            if self.save_settings():
                # Also apply the settings
                self.apply_settings()
                messagebox.showinfo("Settings Saved", 
                                   "All settings have been saved successfully!")
                print("[SETTINGS] All settings saved successfully")
            else:
                messagebox.showerror("Save Error", "Failed to save settings to file")
        else:
            messagebox.showerror("Save Error", "Failed to collect settings from interface")
    
    def test_settings(self):
        """Test current settings"""
        try:
            # Test sound if enabled
            if self.sound_var.get() and hasattr(self.main_window, 'sound_effects'):
                self.main_window.sound_effects.play_sound('notification')
            
            # Test notification
            if self.notifications_var.get():
                messagebox.showinfo("Test Notification", 
                                   "✅ Settings test completed successfully!\n"
                                   f"Theme: {self.theme_var.get()}\n"
                                   f"Language: {self.language_var.get()}\n"
                                   f"Sound: {'Enabled' if self.sound_var.get() else 'Disabled'}")
            
            print("[SETTINGS] Settings test completed")
        except Exception as e:
            messagebox.showerror("Test Error", f"Settings test failed:\n{e}")
            print(f"[SETTINGS] Test error: {e}")
    
    def export_settings(self):
        """Export settings to file"""
        try:
            self.collect_settings_from_ui()
            
            file_path = filedialog.asksaveasfilename(
                title="Export Settings",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialfilename="donte_cleaner_settings.json"
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.settings, f, indent=2, ensure_ascii=False)
                
                messagebox.showinfo("Export Complete", 
                                   f"Settings exported successfully to:\n{file_path}")
                print(f"[SETTINGS] Settings exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export settings:\n{e}")
            print(f"[SETTINGS] Export error: {e}")
    
    def import_settings(self):
        """Import settings from file"""
        try:
            file_path = filedialog.askopenfilename(
                title="Import Settings",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as f:
                    imported_settings = json.load(f)
                
                # Validate and merge settings
                for category, values in imported_settings.items():
                    if category in self.settings and isinstance(values, dict):
                        self.settings[category].update(values)
                
                # Update UI from imported settings
                self.update_ui_from_settings()
                
                messagebox.showinfo("Import Complete", 
                                   f"Settings imported successfully from:\n{file_path}")
                print(f"[SETTINGS] Settings imported from {file_path}")
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import settings:\n{e}")
            print(f"[SETTINGS] Import error: {e}")
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        if messagebox.askyesno("Reset Settings", 
                              "Are you sure you want to reset ALL settings to defaults?\n\n"
                              "This will permanently delete your current configuration.\n"
                              "This action cannot be undone."):
            # Reset to default values
            self.settings = {
                'general': {
                    'auto_start': False,
                    'notifications_enabled': True,
                    'sound_enabled': True,
                    'startup_scan': True,
                    'minimize_to_tray': True,
                    'check_updates': True,
                    'send_statistics': False,
                    'auto_optimization': False,
                    'language': 'turkish'
                },
                'performance': {
                    'scan_threads': 4,
                    'memory_limit': 512,
                    'cleanup_schedule': 'weekly',
                    'deep_scan': False,
                    'real_time_protection': True,
                    'gaming_mode_auto': False,
                    'temp_cleanup_size': 100,
                    'scan_frequency': 'weekly'
                },
                'interface': {
                    'animations': True,
                    'sound_effects': True,
                    'transparency': 0.95,
                    'language': 'turkish',
                    'theme': 'dark',
                    'admin_mode_warning': True
                },
                'security': {
                    'quarantine_suspicious': True,
                    'scan_archives': True,
                    'scan_network_drives': False,
                    'auto_quarantine': False,
                    'firewall_integration': True,
                    'backup_enabled': True
                },
                'advanced': {
                    'log_level': 'info',
                    'debug_mode': False,
                    'crash_reports': True,
                    'telemetry': False
                }
            }
            
            # Update UI
            self.update_ui_from_settings()
            
            messagebox.showinfo("Reset Complete", 
                               "All settings have been reset to defaults.\n"
                               "Click 'Save All Settings' to make changes permanent.")
            print("[SETTINGS] Settings reset to defaults")
    
    def update_ui_from_settings(self):
        """Update all UI elements from current settings"""
        try:
            # General settings
            self.auto_start_var.set(self.settings['general']['auto_start'])
            self.notifications_var.set(self.settings['general']['notifications_enabled'])
            self.sound_var.set(self.settings['general']['sound_enabled'])
            self.updates_var.set(self.settings['general']['check_updates'])
            self.auto_opt_var.set(self.settings['general']['auto_optimization'])
            
            # Performance settings
            self.scan_freq_var.set(self.settings['performance']['scan_frequency'])
            self.gaming_auto_var.set(self.settings['performance']['gaming_mode_auto'])
            self.real_time_var.set(self.settings['performance']['real_time_protection'])
            self.temp_size_var.set(str(self.settings['performance']['temp_cleanup_size']))
            self.threads_var.set(str(self.settings['performance']['scan_threads']))
            
            # Interface settings
            self.theme_var.set(self.settings['interface']['theme'])
            self.language_var.set(self.settings['interface']['language'])
            self.animations_var.set(self.settings['interface']['animations'])
            self.transparency_var.set(self.settings['interface']['transparency'])
            
            # Security settings
            self.backup_var.set(self.settings['security']['backup_enabled'])
            self.quarantine_var.set(self.settings['security']['quarantine_suspicious'])
            self.archives_var.set(self.settings['security']['scan_archives'])
            
            # Advanced settings
            self.log_level_var.set(self.settings['advanced']['log_level'])
            self.debug_var.set(self.settings['advanced']['debug_mode'])
            
            print("[SETTINGS] UI updated from settings successfully")
        except Exception as e:
            print(f"[SETTINGS] Error updating UI from settings: {e}")
    
    def cancel_changes(self):
        """Cancel all changes and reload from file"""
        self.load_settings()
        self.update_ui_from_settings()
        messagebox.showinfo("Changes Cancelled", 
                           "All unsaved changes have been cancelled.\n"
                           "Settings restored to last saved state.")
        print("[SETTINGS] Changes cancelled, settings reloaded")
    
    def get_setting(self, category, key, default=None):
        """Get a specific setting value"""
        try:
            return self.settings.get(category, {}).get(key, default)
        except:
            return default
    
    def set_setting(self, category, key, value):
        """Set a specific setting value"""
        try:
            if category not in self.settings:
                self.settings[category] = {}
            self.settings[category][key] = value
            return True
        except:
            return False
    
    def create_settings_tabs(self, parent):
        """Create settings tabs"""
        tabs_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        tabs_frame.pack(fill='both', expand=True)
        
        # Tab buttons
        tab_frame = tk.Frame(tabs_frame, bg=self.colors['bg_secondary'], height=50)
        tab_frame.pack(fill='x', pady=(0, 20))
        tab_frame.pack_propagate(False)
        
        self.current_tab = tk.StringVar(value="general")
        
        tabs = [
            ("🔧 General", "general"),
            ("⚡ Performance", "performance"), 
            ("🎨 Interface", "interface"),
            ("🛡️ Security", "security")
        ]
        
        for text, tab_id in tabs:
            btn = AnimatedButton(tab_frame, text=text,
                                width=150, height=40,
                                bg_color=self.colors['bg_tertiary'],
                                hover_color=self.colors['accent_primary'],
                                text_color=self.colors['text_primary'],
                                command=lambda t=tab_id: self.switch_tab(t))
            btn.pack(side='left', padx=5, pady=5)
        
        # Content area
        self.content_frame = tk.Frame(tabs_frame, bg=self.colors['bg_primary'])
        self.content_frame.pack(fill='both', expand=True)
        
        # Create all tab contents
        self.tab_contents = {}
        self.create_general_tab()
        
        # Show initial tab
        self.switch_tab("general")
    
    def create_general_tab(self):
        """Create general settings tab"""
        frame = tk.Frame(self.content_frame, bg=self.colors['bg_primary'])
        self.tab_contents["general"] = frame
        
        # Settings card
        card = HolographicCard(frame, width=700, height=400, title="🔧 General Settings")
        card.pack(pady=30)
        
        # Settings options
        settings_options = [
            ("Run scan on startup", "startup_scan"),
            ("Minimize to system tray", "minimize_to_tray"),
            ("Check for updates automatically", "check_updates"),
            ("Send anonymous usage statistics", "send_statistics"),
            ("Enable automatic optimization", "auto_optimization")
        ]
        
        self.settings_vars = {}
        
        for i, (text, key) in enumerate(settings_options):
            var = tk.BooleanVar(value=self.settings['general'][key])
            self.settings_vars[key] = var
            
            check = tk.Checkbutton(card, text=text,
                                  variable=var,
                                  bg=self.colors['bg_tertiary'],
                                  fg=self.colors['text_primary'],
                                  selectcolor=self.colors['bg_secondary'],
                                  font=('Segoe UI', 12),
                                  command=lambda k=key: self.setting_changed(k))
            check.place(x=50, y=80 + i * 40)
        
        # Language selection
        lang_label = tk.Label(card, text="Language:",
                             bg=self.colors['bg_tertiary'],
                             fg=self.colors['text_primary'],
                             font=('Segoe UI', 12, 'bold'))
        lang_label.place(x=50, y=300)
        
        self.language_var = tk.StringVar(value="English")
        lang_menu = tk.OptionMenu(card, self.language_var,
                                 "English", "Türkçe", "Español", "Français")
        lang_menu.config(bg=self.colors['bg_secondary'], fg=self.colors['text_primary'])
        lang_menu.place(x=50, y=330)
        
        # Test notification button
        test_btn = AnimatedButton(card, text="🔔 Test Notifications",
                                 width=200, height=40,
                                 bg_color=self.colors['accent_primary'],
                                 hover_color=self.colors['accent_secondary'],
                                 text_color='black',
                                 command=self.test_notification_system)
        test_btn.place(x=400, y=300)
    
    def create_action_buttons(self, parent):
        """Create action buttons"""
        action_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        action_frame.pack(fill='x', pady=(20, 0))
        
        # Save button
        save_btn = AnimatedButton(action_frame, text="💾 Save Settings",
                                 width=150, height=40,
                                 bg_color=self.colors['success'],
                                 hover_color='#4caf50',
                                 text_color='white',
                                 command=self.save_settings)
        save_btn.pack(side='right', padx=(10, 0))
        
        # Reset button
        reset_btn = AnimatedButton(action_frame, text="🔄 Reset to Defaults",
                                  width=150, height=40,
                                  bg_color=self.colors['danger'],
                                  hover_color='#f44336',
                                  text_color='white',
                                  command=self.reset_settings)
        reset_btn.pack(side='right')
    
    def switch_tab(self, tab_id):
        """Switch between settings tabs"""
        # Hide all tabs
        for tab_frame in self.tab_contents.values():
            tab_frame.pack_forget()
        
        # Show selected tab
        if tab_id in self.tab_contents:
            self.tab_contents[tab_id].pack(fill='both', expand=True)
            self.current_tab.set(tab_id)
            
            # Show notification
            self.show_notification(f"📋 Switched to {tab_id.title()} settings", "info")
    
    def setting_changed(self, key):
        """Handle setting change"""
        if key in self.settings_vars:
            self.settings['general'][key] = self.settings_vars[key].get()
            
            # Show what changed with more specific feedback
            setting_names = {
                'startup_scan': 'Startup Scan',
                'minimize_to_tray': 'Minimize to Tray',
                'check_updates': 'Auto Updates',
                'send_statistics': 'Usage Statistics',
                'auto_optimization': 'Auto Optimization'
            }
            
            setting_name = setting_names.get(key, key.replace('_', ' ').title())
            new_value = "enabled" if self.settings_vars[key].get() else "disabled"
            
            self.show_notification(f"⚙️ {setting_name} {new_value}", "info")
            
            # Update status
            if hasattr(self, 'status_indicator'):
                self.status_indicator.update_status("Modified", self.colors['accent_gold'])
    
    def load_settings(self):
        """Load settings from file"""
        try:
            settings_file = "config/settings.json"
            if os.path.exists(settings_file):
                with open(settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    if 'general' in loaded_settings:
                        self.settings['general'].update(loaded_settings['general'])
        except Exception as e:
            print(f"Settings load error: {e}")
    
    def save_settings(self):
        """Save all settings"""
        try:
            # Create config directory if it doesn't exist
            os.makedirs("config", exist_ok=True)
            
            # Save to file
            settings_file = "config/settings.json"
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            
            # Update status
            if hasattr(self, 'status_indicator'):
                self.status_indicator.update_status("Saved", self.colors['success'])
            
            # Show success notification
            self.show_notification("✅ Settings saved successfully!", "success")
            
            # Play success sound
            if hasattr(self.main_window, 'sound_effects'):
                self.main_window.sound_effects.play_success()
            
        except Exception as e:
            self.show_notification(f"❌ Error saving settings: {str(e)}", "error")
    
    def reset_settings(self):
        """Reset settings to defaults"""
        if messagebox.askyesno("Reset Settings", "Reset all settings to defaults?\n\nThis cannot be undone!"):
            # Reset to defaults
            self.settings['general'] = {
                'startup_scan': True,
                'minimize_to_tray': True,
                'check_updates': True,
                'send_statistics': False,
                'auto_optimization': False
            }
            
            # Update UI
            for key, var in self.settings_vars.items():
                var.set(self.settings['general'][key])
            
            self.show_notification("🔄 All settings reset to defaults", "success")
    
    def test_notification_system(self):
        """Test the notification system"""
        import threading
        
        def test_sequence():
            self.show_notification("🧪 Testing notification system...", "info")
            self.main_window.root.after(1500, lambda: self.show_notification("⚠️ This is a warning notification", "warning"))
            self.main_window.root.after(3000, lambda: self.show_notification("❌ This is an error notification", "error"))
            self.main_window.root.after(4500, lambda: self.show_notification("✅ Notification system working perfectly!", "success"))
        
        test_sequence()
    
    def show_notification(self, message, type="info"):
        """Show notification to user with better visibility"""
        # Create a notification window
        notification = tk.Toplevel(self.main_window.root)
        notification.title("DonTe Cleaner")
        notification.geometry("400x100")
        notification.configure(bg=self.colors['bg_secondary'])
        notification.transient(self.main_window.root)
        notification.overrideredirect(True)  # Remove window decorations
        
        # Position in top right corner
        notification.update_idletasks()
        x = notification.winfo_screenwidth() - 420
        y = 50
        notification.geometry(f"400x100+{x}+{y}")
        
        # Make it stay on top
        notification.attributes('-topmost', True)
        
        # Notification content with border
        border_frame = tk.Frame(notification, bg=self.colors['accent_primary'], 
                               relief='raised', bd=2)
        border_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Content frame
        content_frame = tk.Frame(border_frame, bg=self.colors['bg_secondary'])
        content_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Icon and message based on type
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
        
        # Message label
        label = tk.Label(content_frame, text=f"{icon} {message}",
                        bg=bg_color, fg='white',
                        font=('Segoe UI', 11, 'bold'),
                        wraplength=350, justify='left')
        label.pack(expand=True, fill='both', padx=8, pady=8)
        
        # Close button
        close_btn = tk.Button(content_frame, text="×",
                             bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                             font=('Segoe UI', 12, 'bold'),
                             relief='flat', bd=0,
                             command=notification.destroy)
        close_btn.place(x=370, y=5, width=20, height=20)
        
        # Auto-close after 3 seconds
        notification.after(3000, notification.destroy)
        
        # Print to console for debugging
        print(f"[{type.upper()}] {message}")
        
        # Play sound if available
        if hasattr(self.main_window, 'sound_effects'):
            if type == "success":
                self.main_window.sound_effects.play_success()
            elif type == "warning":
                self.main_window.sound_effects.play_warning()
            elif type == "error":
                self.main_window.sound_effects.play_error()
            else:
                self.main_window.sound_effects.play_notification()
