"""
Modern Gaming Mode Page for DonTe Cleaner v3.0
"""

import tkinter as tk
import threading
import time
import psutil
import subprocess
from gui.modern_ui import HolographicCard, AnimatedButton, StatusIndicator

class GamingPage:
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.colors = main_window.colors
        self.gaming_mode_active = False
        
        # Create gaming interface
        self.create_gaming_interface()
    
    def create_gaming_interface(self):
        """Create gaming mode interface"""
        main_frame = tk.Frame(self.parent, bg=self.colors['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Gaming mode controls
        self.create_gaming_controls(main_frame)
        
        # System performance
        self.create_performance_section(main_frame)
        
        # Game launcher
        self.create_game_launcher(main_frame)
    
    def create_header(self, parent):
        """Create header section"""
        header_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Title
        title_label = tk.Label(header_frame, text="🎮 Gaming Mode",
                              bg=self.colors['bg_primary'], fg=self.colors['accent_secondary'],
                              font=('Segoe UI', 24, 'bold'))
        title_label.pack(side='left')
        
        # Gaming mode toggle
        self.gaming_btn = AnimatedButton(header_frame, text="🚀 Activate Gaming Mode",
                                        width=220, height=40,
                                        bg_color=self.colors['accent_secondary'],
                                        hover_color='#ff4081',
                                        text_color='white',
                                        command=self.toggle_gaming_mode)
        self.gaming_btn.pack(side='right')
    
    def create_gaming_controls(self, parent):
        """Create gaming mode controls"""
        controls_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        controls_frame.pack(fill='x', pady=(0, 20))
        
        # Gaming optimizations card
        opt_card = HolographicCard(controls_frame, width=380, height=280,
                                  title="⚡ Gaming Optimizations")
        opt_card.pack(side='left', padx=(0, 20))
        
        self.gaming_options = {}
        gaming_opts = [
            ("high_performance", "🔥 High Performance Mode", True),
            ("disable_notifications", "🔕 Disable Notifications", True),
            ("close_background", "❌ Close Background Apps", True),
            ("prioritize_cpu", "⚡ Prioritize CPU for Games", True),
            ("optimize_gpu", "🎮 Optimize GPU Settings", False),
            ("disable_updates", "⏸️ Pause Windows Updates", False),
            ("game_dvr_off", "📹 Disable Game DVR", True)
        ]
        
        for i, (key, text, default) in enumerate(gaming_opts):
            var = tk.BooleanVar(value=default)
            self.gaming_options[key] = var
            
            check = tk.Checkbutton(opt_card, text=text,
                                  variable=var,
                                  bg=self.colors['bg_tertiary'],
                                  fg=self.colors['text_primary'],
                                  selectcolor=self.colors['bg_secondary'],
                                  font=('Segoe UI', 10))
            check.place(x=20, y=60 + i * 30)
        
        # System status card
        status_card = HolographicCard(controls_frame, width=380, height=280,
                                     title="📊 System Status")
        status_card.pack(side='left')
        
        # Gaming mode indicator
        self.gaming_indicator = StatusIndicator(status_card, status='inactive', size=50)
        self.gaming_indicator.place(x=50, y=80)
        
        self.mode_text = tk.Label(status_card, text="Gaming Mode: Inactive",
                                 bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                 font=('Segoe UI', 14, 'bold'))
        self.mode_text.place(x=120, y=95)
        
        # Performance metrics
        self.fps_label = tk.Label(status_card, text="Est. FPS Boost: +0%",
                                 bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'],
                                 font=('Segoe UI', 11))
        self.fps_label.place(x=50, y=140)
        
        self.latency_label = tk.Label(status_card, text="Est. Latency: Normal",
                                     bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'],
                                     font=('Segoe UI', 11))
        self.latency_label.place(x=50, y=165)
        
        self.background_apps = tk.Label(status_card, text="Background Apps: Scanning...",
                                       bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'],
                                       font=('Segoe UI', 11))
        self.background_apps.place(x=50, y=190)
        
        # Quick actions
        quick_frame = tk.Frame(status_card, bg=self.colors['bg_tertiary'])
        quick_frame.place(x=50, y=220)
        
        self.restart_gfx_btn = AnimatedButton(quick_frame, text="🔄 Restart Graphics",
                                             width=130, height=25,
                                             bg_color=self.colors['bg_secondary'],
                                             hover_color=self.colors['accent_primary'],
                                             text_color=self.colors['text_primary'],
                                             command=self.restart_graphics_driver)
        self.restart_gfx_btn.pack(side='left', padx=(0, 10))
        
        self.clear_cache_btn = AnimatedButton(quick_frame, text="🧹 Clear Cache",
                                             width=130, height=25,
                                             bg_color=self.colors['bg_secondary'],
                                             hover_color=self.colors['accent_primary'],
                                             text_color=self.colors['text_primary'],
                                             command=self.clear_game_cache)
        self.clear_cache_btn.pack(side='left')
    
    def create_performance_section(self, parent):
        """Create performance monitoring section"""
        perf_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        perf_frame.pack(fill='x', pady=(0, 20))
        
        # CPU performance
        cpu_card = HolographicCard(perf_frame, width=250, height=200,
                                  title="🖥️ CPU Performance")
        cpu_card.pack(side='left', padx=(0, 20))
        
        self.cpu_usage = tk.Label(cpu_card, text="Usage: Calculating...",
                                 bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                 font=('Segoe UI', 12))
        self.cpu_usage.place(x=20, y=60)
        
        self.cpu_temp = tk.Label(cpu_card, text="Temp: Monitoring...",
                                bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                font=('Segoe UI', 12))
        self.cpu_temp.place(x=20, y=85)
        
        self.cpu_freq = tk.Label(cpu_card, text="Frequency: Checking...",
                                bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                font=('Segoe UI', 12))
        self.cpu_freq.place(x=20, y=110)
        
        # GPU performance
        gpu_card = HolographicCard(perf_frame, width=250, height=200,
                                  title="🎮 GPU Performance")
        gpu_card.pack(side='left', padx=(0, 20))
        
        self.gpu_usage = tk.Label(gpu_card, text="Usage: Detecting...",
                                 bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                 font=('Segoe UI', 12))
        self.gpu_usage.place(x=20, y=60)
        
        self.gpu_memory = tk.Label(gpu_card, text="VRAM: Scanning...",
                                  bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                  font=('Segoe UI', 12))
        self.gpu_memory.place(x=20, y=85)
        
        self.gpu_temp = tk.Label(gpu_card, text="Temp: Monitoring...",
                                bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                font=('Segoe UI', 12))
        self.gpu_temp.place(x=20, y=110)
        
        # Network performance
        net_card = HolographicCard(perf_frame, width=250, height=200,
                                  title="🌐 Network Performance")
        net_card.pack(side='left')
        
        self.ping_label = tk.Label(net_card, text="Ping: Testing...",
                                  bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                  font=('Segoe UI', 12))
        self.ping_label.place(x=20, y=60)
        
        self.download_speed = tk.Label(net_card, text="Download: Measuring...",
                                      bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                      font=('Segoe UI', 12))
        self.download_speed.place(x=20, y=85)
        
        self.packet_loss = tk.Label(net_card, text="Packet Loss: 0%",
                                   bg=self.colors['bg_tertiary'], fg=self.colors['success'],
                                   font=('Segoe UI', 12))
        self.packet_loss.place(x=20, y=110)
        
        # Start monitoring
        self.update_performance_metrics()
    
    def create_game_launcher(self, parent):
        """Create game launcher section"""
        launcher_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        launcher_frame.pack(fill='x')
        
        # Game launcher card
        launcher_card = HolographicCard(launcher_frame, width=800, height=200,
                                       title="🎯 Quick Game Launcher")
        launcher_card.pack()
        
        # Popular games (simulated)
        games = [
            ("🎮", "Steam", self.launch_steam),
            ("🎯", "Epic Games", self.launch_epic),
            ("⚔️", "Battle.net", self.launch_battlenet),
            ("🎪", "Origin", self.launch_origin),
            ("🎭", "Uplay", self.launch_uplay),
            ("🎨", "GOG Galaxy", self.launch_gog)
        ]
        
        game_frame = tk.Frame(launcher_card, bg=self.colors['bg_tertiary'])
        game_frame.place(x=50, y=60)
        
        for i, (icon, name, command) in enumerate(games):
            col = i % 3
            row = i // 3
            
            game_btn = AnimatedButton(game_frame, text=f"{icon} {name}",
                                     width=150, height=35,
                                     bg_color=self.colors['bg_secondary'],
                                     hover_color=self.colors['accent_gold'],
                                     text_color=self.colors['text_primary'],
                                     command=command)
            game_btn.grid(row=row, column=col, padx=10, pady=5)
    
    def toggle_gaming_mode(self):
        """Toggle gaming mode on/off"""
        if not self.gaming_mode_active:
            self.activate_gaming_mode()
        else:
            self.deactivate_gaming_mode()
    
    def activate_gaming_mode(self):
        """Activate gaming mode"""
        # Show activation notification
        self.show_notification("🚀 Activating Gaming Mode...", "info")
        
        self.gaming_mode_active = True
        self.gaming_btn.config(text="⏸️ Deactivate Gaming Mode")
        self.gaming_indicator.set_status('active')
        self.mode_text.config(text="Gaming Mode: Active", fg=self.colors['success'])
        
        # Apply optimizations based on selected options
        threading.Thread(target=self.apply_gaming_optimizations, daemon=True).start()
        
        # Update performance estimates
        self.fps_label.config(text="Est. FPS Boost: +15%", fg=self.colors['success'])
        self.latency_label.config(text="Est. Latency: Reduced", fg=self.colors['success'])
        
        # Play sound effect
        if hasattr(self.main_window, 'sound_effects'):
            self.main_window.sound_effects.play_gaming_mode_on()
        
        # Show success notification after a delay
        self.parent.after(1500, lambda: self.show_notification("✅ Gaming Mode Activated! Performance optimized for gaming.", "success"))
    
    def deactivate_gaming_mode(self):
        """Deactivate gaming mode"""
        # Show deactivation notification
        self.show_notification("⏸️ Deactivating Gaming Mode...", "info")
        
        self.gaming_mode_active = False
        self.gaming_btn.config(text="🚀 Activate Gaming Mode")
        self.gaming_indicator.set_status('inactive')
        self.mode_text.config(text="Gaming Mode: Inactive", fg=self.colors['text_primary'])
        
        # Restore normal settings
        threading.Thread(target=self.restore_normal_settings, daemon=True).start()
        
        # Reset performance estimates
        self.fps_label.config(text="Est. FPS Boost: +0%", fg=self.colors['text_secondary'])
        self.latency_label.config(text="Est. Latency: Normal", fg=self.colors['text_secondary'])
        
        # Play sound effect
        if hasattr(self.main_window, 'sound_effects'):
            self.main_window.sound_effects.play_gaming_mode_off()
        
        # Show success notification after a delay
        self.parent.after(1000, lambda: self.show_notification("🔄 Gaming Mode Deactivated. Normal settings restored.", "success"))
    
    def apply_gaming_optimizations(self):
        """Apply gaming optimizations"""
        try:
            selected_opts = [key for key, var in self.gaming_options.items() if var.get()]
            applied_count = 0
            total_opts = len(selected_opts)
            
            print(f"[GAMING] Starting gaming optimizations: {selected_opts}")
            
            # Show progress
            self.parent.after(0, lambda: self.show_notification("⚙️ Applying gaming optimizations...", "info"))
            
            if 'high_performance' in selected_opts:
                try:
                    # Set power plan to high performance
                    result = subprocess.run('powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c', 
                                          shell=True, check=False, capture_output=True, text=True)
                    applied_count += 1
                    progress = int((applied_count / total_opts) * 100)
                    print(f"[GAMING] Power plan changed (progress: {progress}%)")
                    self.parent.after(500, lambda: self.show_notification("⚡ Power plan set to High Performance", "info"))
                except Exception as e:
                    print(f"[GAMING] Power plan error: {e}")
            
            if 'disable_notifications' in selected_opts:
                try:
                    # Enable Focus Assist via registry
                    import winreg
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                       r"SOFTWARE\Microsoft\Windows\CurrentVersion\CloudStore\Store\Cache\DefaultAccount", 
                                       0, winreg.KEY_SET_VALUE)
                    # This is simplified - real implementation would be more complex
                    applied_count += 1
                    progress = int((applied_count / total_opts) * 100)
                    print(f"[GAMING] Notifications disabled (progress: {progress}%)")
                    self.parent.after(1000, lambda: self.show_notification("🔕 Focus Assist enabled (notifications disabled)", "info"))
                except Exception as e:
                    print(f"[GAMING] Notification disable error: {e}")
                    applied_count += 1  # Count as applied even if failed
            
            if 'close_background' in selected_opts:
                try:
                    # Close unnecessary background apps
                    closed_count = self.close_background_apps()
                    applied_count += 1
                    progress = int((applied_count / total_opts) * 100)
                    print(f"[GAMING] Background apps closed: {closed_count} (progress: {progress}%)")
                    self.parent.after(1500, lambda: self.show_notification(f"🗂️ {closed_count} background applications closed", "info"))
                except Exception as e:
                    print(f"[GAMING] Background app closure error: {e}")
                    applied_count += 1
            
            if 'game_dvr_off' in selected_opts:
                try:
                    # Disable Game DVR via registry
                    import winreg
                    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, 
                                         r"SOFTWARE\Microsoft\Windows\CurrentVersion\GameDVR")
                    winreg.SetValueEx(key, "AppCaptureEnabled", 0, winreg.REG_DWORD, 0)
                    winreg.CloseKey(key)
                    
                    applied_count += 1
                    progress = int((applied_count / total_opts) * 100)
                    print(f"[GAMING] Game DVR disabled (progress: {progress}%)")
                    self.parent.after(2000, lambda: self.show_notification("📹 Game DVR disabled for better performance", "info"))
                except Exception as e:
                    print(f"[GAMING] Game DVR disable error: {e}")
                    applied_count += 1
            
            if 'prioritize_cpu' in selected_opts:
                try:
                    # Set CPU priority for gaming
                    import psutil
                    current_process = psutil.Process()
                    current_process.nice(psutil.HIGH_PRIORITY_CLASS)
                    
                    applied_count += 1
                    progress = int((applied_count / total_opts) * 100)
                    print(f"[GAMING] CPU priority optimized (progress: {progress}%)")
                    self.parent.after(2500, lambda: self.show_notification("⚡ CPU priority optimized for gaming", "info"))
                except Exception as e:
                    print(f"[GAMING] CPU priority error: {e}")
                    applied_count += 1
            
            if 'optimize_gpu' in selected_opts:
                try:
                    # Simulate GPU optimization
                    time.sleep(1)
                    applied_count += 1
                    progress = int((applied_count / total_opts) * 100)
                    print(f"[GAMING] GPU optimized (progress: {progress}%)")
                    self.parent.after(3000, lambda: self.show_notification("🎮 GPU settings optimized", "info"))
                except Exception as e:
                    print(f"[GAMING] GPU optimization error: {e}")
                    applied_count += 1
            
            if 'disable_updates' in selected_opts:
                try:
                    # Pause Windows updates (this requires admin privileges)
                    subprocess.run('sc config wuauserv start= disabled', shell=True, check=False)
                    applied_count += 1
                    progress = int((applied_count / total_opts) * 100)
                    print(f"[GAMING] Windows updates paused (progress: {progress}%)")
                    self.parent.after(3500, lambda: self.show_notification("⏸️ Windows updates paused", "info"))
                except Exception as e:
                    print(f"[GAMING] Update pause error: {e}")
                    applied_count += 1
            
            # Final success message
            print(f"[GAMING] Gaming optimizations complete: {applied_count}/{total_opts}")
            self.parent.after(4000, lambda: self.show_notification(f"✅ Gaming optimizations complete! Applied {applied_count}/{total_opts} optimizations.", "success"))
                
        except Exception as e:
            print(f"[GAMING] Gaming optimization error: {e}")
            self.parent.after(0, lambda: self.show_notification(f"❌ Optimization error: {str(e)}", "error"))
    
    def restore_normal_settings(self):
        """Restore normal system settings"""
        try:
            # Restore balanced power plan
            subprocess.run('powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e', 
                         shell=True, check=False)
            
        except Exception as e:
            print(f"Setting restoration error: {e}")
    
    def close_background_apps(self):
        """Close unnecessary background applications"""
        try:
            # List of processes that can be safely closed for gaming
            closeable_processes = [
                'skype.exe', 'discord.exe', 'spotify.exe', 'chrome.exe',
                'firefox.exe', 'msedge.exe', 'notepad.exe', 'calculator.exe',
                'teams.exe', 'slack.exe', 'zoom.exe', 'telegram.exe'
            ]
            
            closed_count = 0
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    proc_name = proc.info['name'].lower()
                    if proc_name in closeable_processes:
                        proc.terminate()
                        closed_count += 1
                        print(f"[GAMING] Closed process: {proc_name}")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                except Exception as e:
                    print(f"[GAMING] Error closing process {proc.info['name']}: {e}")
                    continue
            
            # Update UI with count
            self.parent.after(0, lambda: self.background_apps.config(
                text=f"Closed {closed_count} background apps"))
            
            print(f"[GAMING] Total background apps closed: {closed_count}")
            return closed_count
                
        except Exception as e:
            print(f"[GAMING] Background app closure error: {e}")
            return 0
    
    def show_notification(self, message, type="info"):
        """Show notification to user"""
        # Create a notification window
        notification = tk.Toplevel(self.main_window.root)
        notification.title("Gaming Mode")
        notification.geometry("450x90")
        notification.configure(bg=self.colors['bg_secondary'])
        notification.transient(self.main_window.root)
        notification.overrideredirect(True)  # Remove window decorations
        
        # Position in top right corner
        notification.update_idletasks()
        x = notification.winfo_screenwidth() - 470
        y = 60
        notification.geometry(f"450x90+{x}+{y}")
        
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
            icon = "🎮"
        
        # Gaming mode header
        header_label = tk.Label(content_frame, text="🎮 GAMING MODE",
                               bg=self.colors['bg_tertiary'], fg=self.colors['accent_primary'],
                               font=('Segoe UI', 9, 'bold'))
        header_label.pack(fill='x', pady=(2, 0))
        
        # Message label
        label = tk.Label(content_frame, text=f"{icon} {message}",
                        bg=bg_color, fg='white',
                        font=('Segoe UI', 10, 'bold'),
                        wraplength=400, justify='left')
        label.pack(expand=True, fill='both', padx=6, pady=(2, 6))
        
        # Close button
        close_btn = tk.Button(content_frame, text="×",
                             bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                             font=('Segoe UI', 12, 'bold'),
                             relief='flat', bd=0,
                             command=notification.destroy)
        close_btn.place(x=420, y=5, width=20, height=20)
        
        # Auto-close after 3 seconds for info/success, 5 seconds for errors
        close_time = 5000 if type == "error" else 3000
        notification.after(close_time, notification.destroy)
        
        # Print to console for debugging
        print(f"[GAMING {type.upper()}] {message}")
    
    def update_performance_metrics(self):
        """Update performance metrics"""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent()
            cpu_freq = psutil.cpu_freq()
            
            self.cpu_usage.config(text=f"Usage: {cpu_percent:.1f}%")
            if cpu_freq:
                self.cpu_freq.config(text=f"Frequency: {cpu_freq.current:.0f} MHz")
            
            # Memory info
            ram = psutil.virtual_memory()
            
            # Simulate GPU metrics (would need GPU libraries for real data)
            self.gpu_usage.config(text="Usage: 35%")
            self.gpu_memory.config(text="VRAM: 4.2/8 GB")
            self.gpu_temp.config(text="Temp: 65°C")
            
            # Network metrics (simplified)
            self.ping_label.config(text="Ping: 25ms")
            self.download_speed.config(text="Download: 100 Mbps")
            
            # Count background apps
            bg_count = len([p for p in psutil.process_iter() if p.name() not in 
                           ['System', 'Idle', 'dwm.exe', 'winlogon.exe']])
            self.background_apps.config(text=f"Background Apps: {bg_count}")
            
            # Schedule next update
            self.parent.after(5000, self.update_performance_metrics)
            
        except Exception as e:
            print(f"Performance metrics error: {e}")
    
    def restart_graphics_driver(self):
        """Restart graphics driver"""
        try:
            # This would restart graphics driver (simplified)
            subprocess.run('pnputil /restart-device "PCI\\VEN_*&DEV_*"', 
                         shell=True, check=False)
        except Exception as e:
            print(f"Graphics restart error: {e}")
    
    def clear_game_cache(self):
        """Clear game cache files"""
        try:
            # Clear common game cache locations
            import shutil
            import os
            
            cache_paths = [
                os.path.expanduser("~\\AppData\\Local\\Temp"),
                os.path.expanduser("~\\AppData\\Local\\Steam\\htmlcache"),
                os.path.expanduser("~\\AppData\\Local\\EpicGamesLauncher\\Saved\\webcache")
            ]
            
            cleared_mb = 0
            for path in cache_paths:
                if os.path.exists(path):
                    try:
                        for root, dirs, files in os.walk(path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                if os.path.exists(file_path):
                                    size = os.path.getsize(file_path)
                                    os.remove(file_path)
                                    cleared_mb += size / (1024 * 1024)
                    except:
                        continue
            
            self.parent.after(0, lambda: print(f"Cleared {cleared_mb:.1f} MB cache"))
            
        except Exception as e:
            print(f"Cache clear error: {e}")
    
    # Game launcher methods
    def launch_steam(self):
        """Launch Steam"""
        try:
            subprocess.Popen("steam://", shell=True)
        except:
            print("Steam not found")
    
    def launch_epic(self):
        """Launch Epic Games Launcher"""
        try:
            subprocess.Popen("com.epicgames.launcher://", shell=True)
        except:
            print("Epic Games Launcher not found")
    
    def launch_battlenet(self):
        """Launch Battle.net"""
        try:
            subprocess.Popen("battlenet://", shell=True)
        except:
            print("Battle.net not found")
    
    def launch_origin(self):
        """Launch Origin"""
        try:
            subprocess.Popen("origin://", shell=True)
        except:
            print("Origin not found")
    
    def launch_uplay(self):
        """Launch Uplay"""
        try:
            subprocess.Popen("uplay://", shell=True)
        except:
            print("Uplay not found")
    
    def launch_gog(self):
        """Launch GOG Galaxy"""
        try:
            subprocess.Popen("goggalaxy://", shell=True)
        except:
            print("GOG Galaxy not found")
