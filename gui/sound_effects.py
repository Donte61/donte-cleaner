"""
Sound Effects System for DonTe Cleaner
Provides audio feedback for user interactions and system events
"""

import winsound
import threading
import time
import os
import json
from pathlib import Path
import pygame

# Try to import numpy, use fallback if not available
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("NumPy not available, using fallback sound generation")

class SoundEffects:
    def __init__(self, main_window):
        self.main_window = main_window
        self.sounds_enabled = True
        self.volume = 0.7
        self.settings_file = "config/sound_settings.json"
        
        # Initialize pygame mixer for better sound control
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.pygame_available = True
        except Exception as e:
            print(f"Pygame mixer init failed: {e}")
            self.pygame_available = False
        
        # Sound categories
        self.sound_categories = {
            'ui': True,          # UI interactions
            'system': True,      # System events
            'alerts': True,      # Alerts and warnings
            'completion': True,  # Task completion
            'errors': True       # Error sounds
        }
        
        # Load settings
        self.load_settings()
        
        # Define sound effects
        self.sound_effects = {
            # UI Sounds
            'button_click': {'file': 'click.wav', 'category': 'ui', 'volume': 0.3},
            'button_hover': {'file': 'hover.wav', 'category': 'ui', 'volume': 0.2},
            'tab_switch': {'file': 'switch.wav', 'category': 'ui', 'volume': 0.4},
            'window_open': {'file': 'open.wav', 'category': 'ui', 'volume': 0.5},
            'window_close': {'file': 'close.wav', 'category': 'ui', 'volume': 0.4},
            
            # System Sounds
            'scan_start': {'file': 'scan_start.wav', 'category': 'system', 'volume': 0.6},
            'scan_progress': {'file': 'beep.wav', 'category': 'system', 'volume': 0.3},
            'optimization_start': {'file': 'power_up.wav', 'category': 'system', 'volume': 0.7},
            'cleanup_start': {'file': 'cleanup.wav', 'category': 'system', 'volume': 0.6},
            
            # Completion Sounds
            'task_complete': {'file': 'success.wav', 'category': 'completion', 'volume': 0.8},
            'scan_complete': {'file': 'scan_done.wav', 'category': 'completion', 'volume': 0.7},
            'optimization_complete': {'file': 'optimization_done.wav', 'category': 'completion', 'volume': 0.8},
            'cleanup_complete': {'file': 'cleanup_done.wav', 'category': 'completion', 'volume': 0.7},
            
            # Alert Sounds
            'warning': {'file': 'warning.wav', 'category': 'alerts', 'volume': 0.6},
            'critical_alert': {'file': 'alert.wav', 'category': 'alerts', 'volume': 0.9},
            'notification': {'file': 'notification.wav', 'category': 'alerts', 'volume': 0.5},
            'low_resource': {'file': 'low_resource.wav', 'category': 'alerts', 'volume': 0.7},
            
            # Error Sounds
            'error': {'file': 'error.wav', 'category': 'errors', 'volume': 0.6},
            'access_denied': {'file': 'denied.wav', 'category': 'errors', 'volume': 0.5},
            'operation_failed': {'file': 'failed.wav', 'category': 'errors', 'volume': 0.6},
            
            # Special Effects
            'startup': {'file': 'startup.wav', 'category': 'system', 'volume': 0.8},
            'shutdown': {'file': 'shutdown.wav', 'category': 'system', 'volume': 0.7},
            'gaming_mode_on': {'file': 'game_on.wav', 'category': 'system', 'volume': 0.8},
            'gaming_mode_off': {'file': 'game_off.wav', 'category': 'system', 'volume': 0.6},
            'theme_change': {'file': 'theme.wav', 'category': 'ui', 'volume': 0.5}
        }
        
        # Generate sounds folder
        self.sounds_folder = Path("sounds")
        self.ensure_sounds_folder()
        
        # Generate sound files if they don't exist
        self.generate_missing_sounds()
    
    def load_settings(self):
        """Load sound settings"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.sounds_enabled = settings.get('enabled', True)
                    self.volume = settings.get('volume', 0.7)
                    self.sound_categories.update(settings.get('categories', {}))
        except Exception as e:
            print(f"Sound settings load error: {e}")
    
    def save_settings(self):
        """Save sound settings"""
        try:
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            settings = {
                'enabled': self.sounds_enabled,
                'volume': self.volume,
                'categories': self.sound_categories
            }
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Sound settings save error: {e}")
    
    def ensure_sounds_folder(self):
        """Ensure sounds folder exists"""
        try:
            self.sounds_folder.mkdir(exist_ok=True)
        except Exception as e:
            print(f"Sounds folder creation error: {e}")
    
    def generate_missing_sounds(self):
        """Generate missing sound files"""
        for sound_name, sound_data in self.sound_effects.items():
            sound_path = self.sounds_folder / sound_data['file']
            if not sound_path.exists():
                self.generate_sound_file(sound_name, sound_path)
    
    def generate_sound_file(self, sound_name, sound_path):
        """Generate a sound file using synthesized audio"""
        try:
            if not self.pygame_available:
                return
            
            # Generate different tones for different sound types
            duration = 0.2  # 200ms default
            sample_rate = 22050
            
            # Define sound characteristics based on type
            sound_profiles = {
                'button_click': {'freq': 800, 'duration': 0.1, 'wave': 'sine'},
                'button_hover': {'freq': 600, 'duration': 0.05, 'wave': 'sine'},
                'tab_switch': {'freq': 1000, 'duration': 0.15, 'wave': 'square'},
                'window_open': {'freq': 440, 'duration': 0.3, 'wave': 'sine'},
                'window_close': {'freq': 330, 'duration': 0.25, 'wave': 'sine'},
                'scan_start': {'freq': 660, 'duration': 0.4, 'wave': 'sawtooth'},
                'scan_progress': {'freq': 880, 'duration': 0.1, 'wave': 'sine'},
                'optimization_start': {'freq': 523, 'duration': 0.5, 'wave': 'square'},
                'cleanup_start': {'freq': 440, 'duration': 0.4, 'wave': 'triangle'},
                'task_complete': {'freq': [523, 659, 784], 'duration': 0.6, 'wave': 'sine'},
                'scan_complete': {'freq': [440, 554, 659], 'duration': 0.8, 'wave': 'sine'},
                'optimization_complete': {'freq': [392, 494, 587, 698], 'duration': 1.0, 'wave': 'sine'},
                'cleanup_complete': {'freq': [330, 415, 494], 'duration': 0.7, 'wave': 'sine'},
                'warning': {'freq': 800, 'duration': 0.3, 'wave': 'square'},
                'critical_alert': {'freq': [800, 400, 800, 400], 'duration': 1.0, 'wave': 'square'},
                'notification': {'freq': 660, 'duration': 0.2, 'wave': 'sine'},
                'low_resource': {'freq': 220, 'duration': 0.5, 'wave': 'sawtooth'},
                'error': {'freq': 200, 'duration': 0.4, 'wave': 'square'},
                'access_denied': {'freq': 150, 'duration': 0.6, 'wave': 'square'},
                'operation_failed': {'freq': 100, 'duration': 0.5, 'wave': 'square'},
                'startup': {'freq': [262, 330, 392, 523], 'duration': 1.5, 'wave': 'sine'},
                'shutdown': {'freq': [523, 392, 330, 262], 'duration': 1.2, 'wave': 'sine'},
                'gaming_mode_on': {'freq': [440, 659, 880], 'duration': 0.8, 'wave': 'square'},
                'gaming_mode_off': {'freq': [880, 659, 440], 'duration': 0.6, 'wave': 'square'},
                'theme_change': {'freq': [523, 698, 523], 'duration': 0.5, 'wave': 'sine'}
            }
            
            profile = sound_profiles.get(sound_name, {'freq': 440, 'duration': 0.2, 'wave': 'sine'})
            
            # Generate sound data
            sound_data = self.synthesize_sound(
                profile['freq'], 
                profile['duration'], 
                sample_rate, 
                profile['wave']
            )
            
            # Save as WAV file
            self.save_wav_file(sound_data, sound_path, sample_rate)
            
        except Exception as e:
            print(f"Sound generation error for {sound_name}: {e}")
    
    def synthesize_sound(self, frequencies, duration, sample_rate, wave_type):
        """Synthesize sound with given parameters"""
        if not NUMPY_AVAILABLE:
            # Fallback: create simple beep sound
            return self.create_simple_beep(duration, sample_rate)
        
        if isinstance(frequencies, (int, float)):
            frequencies = [frequencies]
        
        total_samples = int(duration * sample_rate)
        sound_data = np.zeros(total_samples)
        
        # For multiple frequencies (chords), divide duration equally
        freq_duration = duration / len(frequencies)
        
        for i, freq in enumerate(frequencies):
            start_sample = int(i * freq_duration * sample_rate)
            end_sample = int((i + 1) * freq_duration * sample_rate)
            
            if end_sample > total_samples:
                end_sample = total_samples
            
            sample_count = end_sample - start_sample
            t = np.linspace(0, freq_duration, sample_count)
            
            # Generate wave based on type
            if wave_type == 'sine':
                wave = np.sin(2 * np.pi * freq * t)
            elif wave_type == 'square':
                wave = np.sign(np.sin(2 * np.pi * freq * t))
            elif wave_type == 'sawtooth':
                wave = 2 * (t * freq - np.floor(t * freq + 0.5))
            elif wave_type == 'triangle':
                wave = 2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1
            else:
                wave = np.sin(2 * np.pi * freq * t)  # Default to sine
            
            # Apply envelope (fade in/out)
            envelope = np.ones_like(wave)
            fade_samples = min(int(0.05 * sample_rate), sample_count // 4)  # 50ms fade or 1/4 of duration
            
            if fade_samples > 0:
                # Fade in
                envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
                # Fade out
                envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
            
            wave *= envelope
            sound_data[start_sample:end_sample] = wave
        
        # Normalize
        if np.max(np.abs(sound_data)) > 0:
            sound_data = sound_data / np.max(np.abs(sound_data))
        
        return sound_data
    
    def create_simple_beep(self, duration, sample_rate):
        """Create simple beep sound without numpy"""
        import math
        samples = int(duration * sample_rate)
        sound_data = []
        
        freq = 800  # Default frequency
        for i in range(samples):
            t = i / sample_rate
            sample = math.sin(2 * math.pi * freq * t) * 0.5
            sound_data.append(sample)
        
        return sound_data
    
    def save_wav_file(self, sound_data, file_path, sample_rate):
        """Save sound data as WAV file"""
        try:
            import wave
            import struct
            
            if NUMPY_AVAILABLE:
                # Convert to 16-bit integers
                sound_data_int = (sound_data * 32767).astype(np.int16)
            else:
                # Convert simple list to 16-bit integers
                sound_data_int = [int(sample * 32767) for sample in sound_data]
            
            with wave.open(str(file_path), 'w') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
                wav_file.setframerate(sample_rate)
                
                if NUMPY_AVAILABLE:
                    wav_file.writeframes(sound_data_int.tobytes())
                else:
                    # Pack simple list
                    packed_data = struct.pack('<' + 'h' * len(sound_data_int), *sound_data_int)
                    wav_file.writeframes(packed_data)
                
        except Exception as e:
            print(f"WAV file save error: {e}")
    
    def play_sound(self, sound_name, force=False):
        """Play a sound effect"""
        if not self.sounds_enabled and not force:
            return
        
        if sound_name not in self.sound_effects:
            print(f"Unknown sound: {sound_name}")
            return
        
        sound_data = self.sound_effects[sound_name]
        category = sound_data['category']
        
        # Check if category is enabled
        if not self.sound_categories.get(category, True) and not force:
            return
        
        # Play sound in background thread
        threading.Thread(target=self._play_sound_thread, 
                        args=(sound_name, sound_data), daemon=True).start()
    
    def _play_sound_thread(self, sound_name, sound_data):
        """Play sound in background thread"""
        try:
            sound_path = self.sounds_folder / sound_data['file']
            
            if self.pygame_available and sound_path.exists():
                # Use pygame for better control
                sound = pygame.mixer.Sound(str(sound_path))
                volume = sound_data['volume'] * self.volume
                sound.set_volume(volume)
                sound.play()
            else:
                # Fallback to system sounds
                self._play_system_sound(sound_name)
                
        except Exception as e:
            print(f"Sound playback error for {sound_name}: {e}")
            # Fallback to system beep
            try:
                winsound.MessageBeep(winsound.MB_OK)
            except:
                pass
    
    def _play_system_sound(self, sound_name):
        """Play system sound as fallback"""
        try:
            # Map to Windows system sounds
            system_sound_map = {
                'error': winsound.MB_ICONHAND,
                'warning': winsound.MB_ICONEXCLAMATION,
                'critical_alert': winsound.MB_ICONHAND,
                'access_denied': winsound.MB_ICONHAND,
                'operation_failed': winsound.MB_ICONHAND,
                'task_complete': winsound.MB_OK,
                'notification': winsound.MB_ICONASTERISK
            }
            
            system_sound = system_sound_map.get(sound_name, winsound.MB_OK)
            winsound.MessageBeep(system_sound)
            
        except Exception as e:
            print(f"System sound error: {e}")
    
    def show_sound_settings(self):
        """Show sound settings window"""
        import tkinter as tk
        from tkinter import ttk
        
        self.sound_window = tk.Toplevel(self.main_window.root)
        self.sound_window.title("🎵 Sound Settings")
        self.sound_window.geometry("600x500")
        self.sound_window.configure(bg=self.main_window.colors['bg_dark'])
        self.sound_window.transient(self.main_window.root)
        self.sound_window.grab_set()
        
        # Create sound settings interface
        self.create_sound_settings_interface()
        
        # Center window
        self.center_sound_window()
    
    def center_sound_window(self):
        """Center sound settings window"""
        self.sound_window.update_idletasks()
        width = self.sound_window.winfo_width()
        height = self.sound_window.winfo_height()
        x = (self.sound_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.sound_window.winfo_screenheight() // 2) - (height // 2)
        self.sound_window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_sound_settings_interface(self):
        """Create sound settings interface"""
        import tkinter as tk
        from tkinter import ttk
        
        main_frame = ttk.Frame(self.sound_window, style="Modern.TFrame", padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Header
        ttk.Label(main_frame, text="🎵 Sound Effects Settings", 
                 font=("Segoe UI", 16, "bold"),
                 background=self.main_window.colors['bg_dark'],
                 foreground=self.main_window.colors['text_white']).pack(pady=(0, 20))
        
        # General settings
        general_frame = ttk.LabelFrame(main_frame, text="🔧 General Settings", padding="15")
        general_frame.pack(fill="x", pady=(0, 20))
        
        # Enable/disable sounds
        self.sounds_var = tk.BooleanVar(value=self.sounds_enabled)
        ttk.Checkbutton(general_frame, text="Enable sound effects",
                       variable=self.sounds_var,
                       command=self.update_sound_settings).pack(anchor="w", pady=5)
        
        # Volume control
        volume_frame = ttk.Frame(general_frame, style="Modern.TFrame")
        volume_frame.pack(fill="x", pady=10)
        
        ttk.Label(volume_frame, text="Volume:",
                 background=self.main_window.colors['bg_light'],
                 foreground=self.main_window.colors['text_white']).pack(side="left")
        
        self.volume_var = tk.DoubleVar(value=self.volume)
        volume_scale = ttk.Scale(volume_frame, from_=0, to=1, variable=self.volume_var, 
                               orient="horizontal", command=self.update_volume)
        volume_scale.pack(side="right", fill="x", expand=True, padx=(10, 0))
        
        self.volume_label = ttk.Label(volume_frame, text=f"{int(self.volume * 100)}%",
                                     background=self.main_window.colors['bg_light'],
                                     foreground=self.main_window.colors['accent'])
        self.volume_label.pack(side="right", padx=(5, 10))
        
        # Sound categories
        categories_frame = ttk.LabelFrame(main_frame, text="🎯 Sound Categories", padding="15")
        categories_frame.pack(fill="x", pady=(0, 20))
        
        self.category_vars = {}
        category_labels = {
            'ui': 'UI Interactions (clicks, hovers)',
            'system': 'System Events (scans, optimizations)',
            'alerts': 'Alerts & Warnings',
            'completion': 'Task Completion',
            'errors': 'Error Sounds'
        }
        
        for category, label in category_labels.items():
            var = tk.BooleanVar(value=self.sound_categories[category])
            self.category_vars[category] = var
            
            ttk.Checkbutton(categories_frame, text=label,
                           variable=var,
                           command=self.update_sound_settings).pack(anchor="w", pady=3)
        
        # Test sounds
        test_frame = ttk.LabelFrame(main_frame, text="🧪 Test Sounds", padding="15")
        test_frame.pack(fill="x", pady=(0, 20))
        
        # Test buttons in grid
        test_buttons = [
            ("🖱️ Click", "button_click"),
            ("✅ Success", "task_complete"),
            ("⚠️ Warning", "warning"),
            ("❌ Error", "error"),
            ("🔍 Scan Start", "scan_start"),
            ("🎮 Gaming Mode", "gaming_mode_on")
        ]
        
        button_frame = ttk.Frame(test_frame, style="Modern.TFrame")
        button_frame.pack(fill="x")
        
        for i, (text, sound) in enumerate(test_buttons):
            row = i // 3
            col = i % 3
            
            ttk.Button(button_frame, text=text,
                      style="Modern.TButton",
                      command=lambda s=sound: self.test_sound(s)).grid(row=row, column=col, 
                                                                       padx=5, pady=5, sticky="ew")
        
        # Configure grid weights
        for i in range(3):
            button_frame.grid_columnconfigure(i, weight=1)
        
        # Action buttons
        action_frame = ttk.Frame(main_frame, style="Modern.TFrame")
        action_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Button(action_frame, text="💾 Save Settings",
                  style="Success.TButton",
                  command=self.save_sound_settings).pack(side="right", padx=(10, 0))
        
        ttk.Button(action_frame, text="🔄 Reset to Defaults",
                  style="Warning.TButton",
                  command=self.reset_sound_settings).pack(side="right", padx=(10, 0))
        
        ttk.Button(action_frame, text="❌ Close",
                  style="Modern.TButton",
                  command=self.sound_window.destroy).pack(side="right")
    
    def test_sound(self, sound_name):
        """Test a specific sound"""
        self.play_sound(sound_name, force=True)
    
    def update_sound_settings(self):
        """Update sound settings from UI"""
        self.sounds_enabled = self.sounds_var.get()
        
        for category, var in self.category_vars.items():
            self.sound_categories[category] = var.get()
    
    def update_volume(self, value):
        """Update volume setting"""
        self.volume = float(value)
        self.volume_label.config(text=f"{int(self.volume * 100)}%")
    
    def save_sound_settings(self):
        """Save sound settings"""
        self.update_sound_settings()
        self.save_settings()
        
        from tkinter import messagebox
        messagebox.showinfo("Settings Saved", "Sound settings have been saved successfully!")
        
        # Play confirmation sound
        self.play_sound("task_complete")
    
    def reset_sound_settings(self):
        """Reset sound settings to defaults"""
        from tkinter import messagebox
        
        if messagebox.askyesno("Reset Settings", "Reset all sound settings to defaults?"):
            self.sounds_enabled = True
            self.volume = 0.7
            self.sound_categories = {
                'ui': True,
                'system': True,
                'alerts': True,
                'completion': True,
                'errors': True
            }
            
            # Update UI
            self.sounds_var.set(self.sounds_enabled)
            self.volume_var.set(self.volume)
            for category, var in self.category_vars.items():
                var.set(self.sound_categories[category])
            
            self.save_settings()
            messagebox.showinfo("Reset Complete", "Sound settings reset to defaults!")
    
    # Convenience methods for common sounds
    def play_click(self):
        """Play button click sound"""
        self.play_sound("button_click")
    
    def play_hover(self):
        """Play button hover sound"""
        self.play_sound("button_hover")
    
    def play_success(self):
        """Play success sound"""
        self.play_sound("task_complete")
    
    def play_error(self):
        """Play error sound"""
        self.play_sound("error")
    
    def play_warning(self):
        """Play warning sound"""
        self.play_sound("warning")
    
    def play_notification(self):
        """Play notification sound"""
        self.play_sound("notification")
    
    def play_scan_start(self):
        """Play scan start sound"""
        self.play_sound("scan_start")
    
    def play_scan_complete(self):
        """Play scan complete sound"""
        self.play_sound("scan_complete")
    
    def play_optimization_start(self):
        """Play optimization start sound"""
        self.play_sound("optimization_start")
    
    def play_optimization_complete(self):
        """Play optimization complete sound"""
        self.play_sound("optimization_complete")
    
    def play_cleanup_start(self):
        """Play cleanup start sound"""
        self.play_sound("cleanup_start")
    
    def play_cleanup_complete(self):
        """Play cleanup complete sound"""
        self.play_sound("cleanup_complete")
    
    def play_startup(self):
        """Play startup sound"""
        self.play_sound("startup")
    
    def play_shutdown(self):
        """Play shutdown sound"""
        self.play_sound("shutdown")
    
    def play_gaming_mode_on(self):
        """Play gaming mode on sound"""
        self.play_sound("gaming_mode_on")
    
    def play_gaming_mode_off(self):
        """Play gaming mode off sound"""
        self.play_sound("gaming_mode_off")
    
    def play_theme_change(self):
        """Play theme change sound"""
        self.play_sound("theme_change")
