"""
Smart Notifications System for DonTe Cleaner
Advanced notification system with customizable alerts and smart suggestions
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import json
import os
from datetime import datetime, timedelta
import psutil
import winsound
from plyer import notification
import schedule

class SmartNotifications:
    def __init__(self, main_window):
        self.main_window = main_window
        self.notifications_enabled = True
        self.sound_enabled = True
        self.desktop_notifications = True
        self.monitoring_active = False
        
        # Notification settings
        self.settings_file = "config/notifications.json"
        self.load_settings()
        
        # Notification history
        self.notification_history = []
        self.max_history = 100
        
        # Monitoring thresholds
        self.thresholds = {
            'cpu_warning': 80,
            'cpu_critical': 95,
            'ram_warning': 80,
            'ram_critical': 95,
            'disk_warning': 85,
            'disk_critical': 95,
            'temp_warning': 70,
            'temp_critical': 85
        }
        
        # Smart suggestions
        self.suggestions = {
            'high_cpu': [
                "Close unnecessary applications",
                "Check for background processes",
                "Consider restarting your computer",
                "Run antivirus scan for malware"
            ],
            'high_ram': [
                "Close unused browser tabs",
                "Restart memory-intensive applications",
                "Clear system cache",
                "Check for memory leaks"
            ],
            'high_disk': [
                "Clean temporary files",
                "Empty recycle bin",
                "Remove old downloads",
                "Move files to external storage"
            ],
            'low_disk_space': [
                "Run disk cleanup utility",
                "Uninstall unused programs",
                "Move large files to cloud storage",
                "Consider upgrading storage"
            ]
        }
        
        # Notification types
        self.notification_types = {
            'info': {'icon': 'ℹ️', 'color': '#17a2b8'},
            'success': {'icon': '✅', 'color': '#28a745'},
            'warning': {'icon': '⚠️', 'color': '#ffc107'},
            'error': {'icon': '❌', 'color': '#dc3545'},
            'critical': {'icon': '🚨', 'color': '#d4edda'}
        }
        
        # Auto-suggestions based on system state
        self.auto_suggestions = []
        self.last_suggestion_time = {}
        
        # Schedule notifications
        self.setup_scheduled_notifications()
        
        # Start monitoring
        self.start_smart_monitoring()
    
    def load_settings(self):
        """Load notification settings"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.notifications_enabled = settings.get('enabled', True)
                    self.sound_enabled = settings.get('sound', True)
                    self.desktop_notifications = settings.get('desktop', True)
                    self.thresholds.update(settings.get('thresholds', {}))
        except Exception as e:
            print(f"Settings load error: {e}")
    
    def save_settings(self):
        """Save notification settings"""
        try:
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            settings = {
                'enabled': self.notifications_enabled,
                'sound': self.sound_enabled,
                'desktop': self.desktop_notifications,
                'thresholds': self.thresholds
            }
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Settings save error: {e}")
    
    def show_notification_center(self):
        """Show notification center window"""
        self.notification_window = tk.Toplevel(self.main_window.root)
        self.notification_window.title("🔔 Smart Notification Center")
        self.notification_window.geometry("800x600")
        self.notification_window.configure(bg=self.main_window.colors['bg_dark'])
        self.notification_window.transient(self.main_window.root)
        self.notification_window.grab_set()
        
        # Create notification interface
        self.create_notification_interface()
        
        # Center window
        self.center_notification_window()
    
    def center_notification_window(self):
        """Center notification window"""
        self.notification_window.update_idletasks()
        width = self.notification_window.winfo_width()
        height = self.notification_window.winfo_height()
        x = (self.notification_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.notification_window.winfo_screenheight() // 2) - (height // 2)
        self.notification_window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_notification_interface(self):
        """Create notification center interface"""
        main_frame = ttk.Frame(self.notification_window, style="Modern.TFrame", padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Header
        self.create_notification_header(main_frame)
        
        # Notebook for different sections
        notebook = ttk.Notebook(main_frame, style="Modern.TNotebook")
        notebook.pack(fill="both", expand=True, pady=(10, 0))
        
        # Recent notifications tab
        self.create_recent_notifications_tab(notebook)
        
        # Smart suggestions tab
        self.create_suggestions_tab(notebook)
        
        # Settings tab
        self.create_notification_settings_tab(notebook)
        
        # System alerts tab
        self.create_system_alerts_tab(notebook)
    
    def create_notification_header(self, parent):
        """Create notification header"""
        header_frame = ttk.Frame(parent, style="Modern.TFrame")
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Title
        ttk.Label(header_frame, text="🔔 Smart Notification Center", 
                 font=("Segoe UI", 18, "bold"),
                 background=self.main_window.colors['bg_dark'],
                 foreground=self.main_window.colors['text_white']).pack(side="left")
        
        # Controls
        controls_frame = ttk.Frame(header_frame, style="Modern.TFrame")
        controls_frame.pack(side="right")
        
        # Clear all notifications
        ttk.Button(controls_frame, text="🗑️ Tümünü Temizle",
                  style="Danger.TButton",
                  command=self.clear_all_notifications).pack(side="right", padx=(10, 0))
        
        # Toggle notifications
        status_text = "🔕 Kapat" if self.notifications_enabled else "🔔 Aç"
        self.toggle_btn = ttk.Button(controls_frame, text=status_text,
                                    style="Warning.TButton" if self.notifications_enabled else "Success.TButton",
                                    command=self.toggle_notifications)
        self.toggle_btn.pack(side="right", padx=(10, 0))
        
        # Test notification
        ttk.Button(controls_frame, text="🧪 Test Bildirim",
                  style="Modern.TButton",
                  command=self.send_test_notification).pack(side="right", padx=(10, 0))
    
    def create_recent_notifications_tab(self, parent):
        """Create recent notifications tab"""
        notifications_frame = ttk.Frame(parent, style="Modern.TFrame")
        parent.add(notifications_frame, text="📨 Recent Notifications")
        
        # Create scrollable notification list
        canvas = tk.Canvas(notifications_frame, highlightthickness=0,
                          bg=self.main_window.colors['bg_dark'])
        scrollbar = ttk.Scrollbar(notifications_frame, orient="vertical", command=canvas.yview)
        self.notifications_list_frame = ttk.Frame(canvas, style="Modern.TFrame")
        
        self.notifications_list_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.notifications_list_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Populate notifications
        self.populate_notification_history()
        
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
    
    def create_suggestions_tab(self, parent):
        """Create smart suggestions tab"""
        suggestions_frame = ttk.Frame(parent, style="Modern.TFrame", padding="20")
        parent.add(suggestions_frame, text="💡 Smart Suggestions")
        
        # Current system status
        status_frame = ttk.LabelFrame(suggestions_frame, text="🖥️ Current System Status", padding="15")
        status_frame.pack(fill="x", pady=(0, 20))
        
        self.system_status_label = ttk.Label(status_frame, text="Analyzing system...",
                                            font=("Segoe UI", 11),
                                            background=self.main_window.colors['bg_light'],
                                            foreground=self.main_window.colors['text_white'])
        self.system_status_label.pack(anchor="w")
        
        # Smart suggestions list
        suggestions_list_frame = ttk.LabelFrame(suggestions_frame, text="🧠 AI Recommendations", padding="15")
        suggestions_list_frame.pack(fill="both", expand=True)
        
        # Suggestions canvas
        suggestions_canvas = tk.Canvas(suggestions_list_frame, highlightthickness=0,
                                     bg=self.main_window.colors['bg_light'])
        suggestions_scrollbar = ttk.Scrollbar(suggestions_list_frame, orient="vertical", 
                                            command=suggestions_canvas.yview)
        self.suggestions_content_frame = ttk.Frame(suggestions_canvas, style="Card.TFrame")
        
        self.suggestions_content_frame.bind(
            "<Configure>",
            lambda e: suggestions_canvas.configure(scrollregion=suggestions_canvas.bbox("all"))
        )
        
        suggestions_canvas.create_window((0, 0), window=self.suggestions_content_frame, anchor="nw")
        suggestions_canvas.configure(yscrollcommand=suggestions_scrollbar.set)
        
        # Populate suggestions
        self.populate_suggestions()
        
        suggestions_canvas.pack(side="left", fill="both", expand=True)
        suggestions_scrollbar.pack(side="right", fill="y")
        
        # Auto-refresh button
        ttk.Button(suggestions_frame, text="🔄 Önerileri Yenile",
                  style="Modern.TButton",
                  command=self.refresh_suggestions).pack(pady=(10, 0))
    
    def create_notification_settings_tab(self, parent):
        """Create notification settings tab"""
        settings_frame = ttk.Frame(parent, style="Modern.TFrame", padding="20")
        parent.add(settings_frame, text="⚙️ Settings")
        
        # General settings
        general_frame = ttk.LabelFrame(settings_frame, text="🔧 General Settings", padding="15")
        general_frame.pack(fill="x", pady=(0, 20))
        
        # Enable/disable notifications
        self.notifications_var = tk.BooleanVar(value=self.notifications_enabled)
        ttk.Checkbutton(general_frame, text="Enable notifications",
                       variable=self.notifications_var,
                       command=self.update_notification_settings).pack(anchor="w", pady=5)
        
        # Sound notifications
        self.sound_var = tk.BooleanVar(value=self.sound_enabled)
        ttk.Checkbutton(general_frame, text="Sound alerts",
                       variable=self.sound_var,
                       command=self.update_notification_settings).pack(anchor="w", pady=5)
        
        # Desktop notifications
        self.desktop_var = tk.BooleanVar(value=self.desktop_notifications)
        ttk.Checkbutton(general_frame, text="Desktop notifications",
                       variable=self.desktop_var,
                       command=self.update_notification_settings).pack(anchor="w", pady=5)
        
        # Threshold settings
        thresholds_frame = ttk.LabelFrame(settings_frame, text="🎯 Alert Thresholds", padding="15")
        thresholds_frame.pack(fill="x", pady=(0, 20))
        
        # Create threshold sliders
        self.threshold_vars = {}
        threshold_labels = {
            'cpu_warning': 'CPU Warning (%)',
            'cpu_critical': 'CPU Critical (%)',
            'ram_warning': 'RAM Warning (%)',
            'ram_critical': 'RAM Critical (%)',
            'disk_warning': 'Disk Warning (%)',
            'disk_critical': 'Disk Critical (%)'
        }
        
        for key, label in threshold_labels.items():
            frame = ttk.Frame(thresholds_frame, style="Modern.TFrame")
            frame.pack(fill="x", pady=5)
            
            ttk.Label(frame, text=f"{label}:",
                     background=self.main_window.colors['bg_light'],
                     foreground=self.main_window.colors['text_white']).pack(side="left")
            
            var = tk.IntVar(value=self.thresholds[key])
            self.threshold_vars[key] = var
            
            scale = ttk.Scale(frame, from_=50, to=100, variable=var, orient="horizontal",
                            command=lambda v, k=key: self.update_threshold(k, v))
            scale.pack(side="right", fill="x", expand=True, padx=(10, 0))
            
            value_label = ttk.Label(frame, text=f"{var.get()}%",
                                   background=self.main_window.colors['bg_light'],
                                   foreground=self.main_window.colors['accent'])
            value_label.pack(side="right", padx=(5, 10))
            
            # Update label when scale changes
            var.trace('w', lambda *args, lbl=value_label, v=var: lbl.config(text=f"{v.get()}%"))
    
    def create_system_alerts_tab(self, parent):
        """Create system alerts tab"""
        alerts_frame = ttk.Frame(parent, style="Modern.TFrame", padding="20")
        parent.add(alerts_frame, text="🚨 System Alerts")
        
        # Active alerts
        active_frame = ttk.LabelFrame(alerts_frame, text="🔥 Active Alerts", padding="15")
        active_frame.pack(fill="x", pady=(0, 20))
        
        self.active_alerts_frame = ttk.Frame(active_frame, style="Card.TFrame")
        self.active_alerts_frame.pack(fill="x")
        
        # Alert history
        history_frame = ttk.LabelFrame(alerts_frame, text="📜 Alert History", padding="15")
        history_frame.pack(fill="both", expand=True)
        
        # History canvas
        history_canvas = tk.Canvas(history_frame, highlightthickness=0,
                                  bg=self.main_window.colors['bg_light'])
        history_scrollbar = ttk.Scrollbar(history_frame, orient="vertical", 
                                         command=history_canvas.yview)
        self.alert_history_frame = ttk.Frame(history_canvas, style="Card.TFrame")
        
        self.alert_history_frame.bind(
            "<Configure>",
            lambda e: history_canvas.configure(scrollregion=history_canvas.bbox("all"))
        )
        
        history_canvas.create_window((0, 0), window=self.alert_history_frame, anchor="nw")
        history_canvas.configure(yscrollcommand=history_scrollbar.set)
        
        history_canvas.pack(side="left", fill="both", expand=True)
        history_scrollbar.pack(side="right", fill="y")
        
        # Update alerts
        self.update_system_alerts()
    
    def start_smart_monitoring(self):
        """Start smart monitoring system"""
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self.monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        # Setup scheduled notifications
        self.schedule_thread = threading.Thread(target=self.schedule_runner, daemon=True)
        self.schedule_thread.start()
    
    def monitoring_loop(self):
        """Main monitoring loop for smart notifications"""
        while self.monitoring_active:
            try:
                # Check system metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk_usage = psutil.disk_usage('C:')
                disk_percent = (disk_usage.used / disk_usage.total) * 100
                
                # Check thresholds and send notifications
                self.check_cpu_threshold(cpu_percent)
                self.check_memory_threshold(memory.percent)
                self.check_disk_threshold(disk_percent)
                
                # Generate smart suggestions
                self.generate_smart_suggestions(cpu_percent, memory.percent, disk_percent)
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(30)
    
    def check_cpu_threshold(self, cpu_percent):
        """Check CPU usage thresholds"""
        if cpu_percent >= self.thresholds['cpu_critical']:
            self.send_notification(
                "🚨 Critical CPU Usage!",
                f"CPU usage is {cpu_percent:.1f}% - System may be unresponsive",
                "critical",
                suggestions=self.suggestions['high_cpu']
            )
        elif cpu_percent >= self.thresholds['cpu_warning']:
            self.send_notification(
                "⚠️ High CPU Usage",
                f"CPU usage is {cpu_percent:.1f}% - Consider closing applications",
                "warning",
                suggestions=self.suggestions['high_cpu'][:2]
            )
    
    def check_memory_threshold(self, memory_percent):
        """Check memory usage thresholds"""
        if memory_percent >= self.thresholds['ram_critical']:
            self.send_notification(
                "🚨 Critical Memory Usage!",
                f"RAM usage is {memory_percent:.1f}% - System may slow down",
                "critical",
                suggestions=self.suggestions['high_ram']
            )
        elif memory_percent >= self.thresholds['ram_warning']:
            self.send_notification(
                "⚠️ High Memory Usage",
                f"RAM usage is {memory_percent:.1f}% - Consider freeing memory",
                "warning",
                suggestions=self.suggestions['high_ram'][:2]
            )
    
    def check_disk_threshold(self, disk_percent):
        """Check disk usage thresholds"""
        if disk_percent >= self.thresholds['disk_critical']:
            self.send_notification(
                "🚨 Critical Disk Space!",
                f"Disk usage is {disk_percent:.1f}% - Immediate cleanup needed",
                "critical",
                suggestions=self.suggestions['high_disk']
            )
        elif disk_percent >= self.thresholds['disk_warning']:
            self.send_notification(
                "⚠️ Low Disk Space",
                f"Disk usage is {disk_percent:.1f}% - Consider cleanup",
                "warning",
                suggestions=self.suggestions['high_disk'][:2]
            )
    
    def send_notification(self, title, message, notification_type="info", suggestions=None):
        """Send smart notification"""
        if not self.notifications_enabled:
            return
        
        # Avoid spam - don't send same notification too frequently
        notification_key = f"{title}_{notification_type}"
        current_time = time.time()
        
        if notification_key in self.last_suggestion_time:
            if current_time - self.last_suggestion_time[notification_key] < 300:  # 5 minutes
                return
        
        self.last_suggestion_time[notification_key] = current_time
        
        # Create notification object
        notification_obj = {
            'id': len(self.notification_history),
            'title': title,
            'message': message,
            'type': notification_type,
            'timestamp': datetime.now(),
            'suggestions': suggestions or [],
            'read': False
        }
        
        # Add to history
        self.notification_history.insert(0, notification_obj)
        if len(self.notification_history) > self.max_history:
            self.notification_history.pop()
        
        # Show desktop notification
        if self.desktop_notifications:
            try:
                icon_path = self.get_notification_icon(notification_type)
                notification.notify(
                    title=title,
                    message=message,
                    app_name="DonTe Cleaner",
                    timeout=10
                )
            except Exception as e:
                print(f"Desktop notification error: {e}")
        
        # Play sound
        if self.sound_enabled:
            self.play_notification_sound(notification_type)
        
        # Show in-app notification popup
        self.show_notification_popup(notification_obj)
        
        # Update notification count in main window
        if hasattr(self.main_window, 'add_activity'):
            self.main_window.add_activity(f"{title}: {message}", 
                                        self.get_activity_type(notification_type))
    
    def show_notification_popup(self, notification_obj):
        """Show in-app notification popup"""
        try:
            popup = tk.Toplevel(self.main_window.root)
            popup.title("Notification")
            popup.geometry("400x300")
            popup.configure(bg=self.main_window.colors['bg_dark'])
            popup.attributes('-topmost', True)
            popup.transient(self.main_window.root)
            
            # Position in bottom right
            popup.update_idletasks()
            x = popup.winfo_screenwidth() - 420
            y = popup.winfo_screenheight() - 350
            popup.geometry(f"400x300+{x}+{y}")
            
            main_frame = ttk.Frame(popup, style="Card.TFrame", padding="20")
            main_frame.pack(fill="both", expand=True)
            
            # Header
            header_frame = ttk.Frame(main_frame, style="Card.TFrame")
            header_frame.pack(fill="x", pady=(0, 10))
            
            # Icon and title
            icon = self.notification_types[notification_obj['type']]['icon']
            color = self.notification_types[notification_obj['type']]['color']
            
            ttk.Label(header_frame, text=f"{icon} {notification_obj['title']}", 
                     font=("Segoe UI", 12, "bold"),
                     background=self.main_window.colors['bg_light'],
                     foreground=color).pack(side="left")
            
            # Close button
            ttk.Button(header_frame, text="✕",
                      command=popup.destroy).pack(side="right")
            
            # Message
            ttk.Label(main_frame, text=notification_obj['message'],
                     font=("Segoe UI", 10),
                     background=self.main_window.colors['bg_light'],
                     foreground=self.main_window.colors['text_white'],
                     wraplength=350).pack(fill="x", pady=(0, 10))
            
            # Suggestions
            if notification_obj['suggestions']:
                ttk.Label(main_frame, text="💡 Suggestions:",
                         font=("Segoe UI", 10, "bold"),
                         background=self.main_window.colors['bg_light'],
                         foreground=self.main_window.colors['accent']).pack(anchor="w", pady=(5, 0))
                
                for suggestion in notification_obj['suggestions'][:3]:  # Show max 3
                    ttk.Label(main_frame, text=f"• {suggestion}",
                             font=("Segoe UI", 9),
                             background=self.main_window.colors['bg_light'],
                             foreground=self.main_window.colors['text_gray'],
                             wraplength=350).pack(anchor="w", padx=(10, 0))
            
            # Auto-close after 10 seconds
            popup.after(10000, popup.destroy)
            
        except Exception as e:
            print(f"Popup notification error: {e}")
    
    def play_notification_sound(self, notification_type):
        """Play notification sound"""
        try:
            if notification_type == "critical":
                winsound.MessageBeep(winsound.MB_ICONHAND)
            elif notification_type == "warning":
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            elif notification_type == "error":
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
            else:
                winsound.MessageBeep(winsound.MB_OK)
        except Exception as e:
            print(f"Sound notification error: {e}")
    
    def get_notification_icon(self, notification_type):
        """Get notification icon path"""
        # Placeholder - would return actual icon paths
        return None
    
    def get_activity_type(self, notification_type):
        """Convert notification type to activity type"""
        type_mapping = {
            'info': 'Bilgi',
            'success': 'Başarılı',
            'warning': 'Uyarı',
            'error': 'Hata',
            'critical': 'Hata'
        }
        return type_mapping.get(notification_type, 'Bilgi')
    
    def generate_smart_suggestions(self, cpu_percent, memory_percent, disk_percent):
        """Generate smart suggestions based on system state"""
        suggestions = []
        
        # CPU suggestions
        if cpu_percent > 70:
            suggestions.extend(self.suggestions['high_cpu'][:2])
        
        # Memory suggestions
        if memory_percent > 70:
            suggestions.extend(self.suggestions['high_ram'][:2])
        
        # Disk suggestions
        if disk_percent > 80:
            suggestions.extend(self.suggestions['high_disk'][:2])
        
        # Update suggestions
        self.auto_suggestions = list(set(suggestions))  # Remove duplicates
    
    def populate_notification_history(self):
        """Populate notification history list"""
        # Clear existing notifications
        for widget in self.notifications_list_frame.winfo_children():
            widget.destroy()
        
        if not self.notification_history:
            ttk.Label(self.notifications_list_frame, text="No notifications yet",
                     font=("Segoe UI", 12),
                     background=self.main_window.colors['bg_dark'],
                     foreground=self.main_window.colors['text_gray']).pack(pady=20)
            return
        
        for notification in self.notification_history[:20]:  # Show last 20
            self.create_notification_item(self.notifications_list_frame, notification)
    
    def create_notification_item(self, parent, notification):
        """Create notification history item"""
        item_frame = ttk.Frame(parent, style="Card.TFrame", padding="10")
        item_frame.pack(fill="x", pady=5, padx=10)
        
        # Header
        header_frame = ttk.Frame(item_frame, style="Card.TFrame")
        header_frame.pack(fill="x")
        
        # Icon and title
        icon = self.notification_types[notification['type']]['icon']
        color = self.notification_types[notification['type']]['color']
        
        ttk.Label(header_frame, text=f"{icon} {notification['title']}", 
                 font=("Segoe UI", 11, "bold"),
                 background=self.main_window.colors['bg_light'],
                 foreground=color).pack(side="left")
        
        # Timestamp
        time_str = notification['timestamp'].strftime("%H:%M")
        ttk.Label(header_frame, text=time_str,
                 font=("Segoe UI", 9),
                 background=self.main_window.colors['bg_light'],
                 foreground=self.main_window.colors['text_gray']).pack(side="right")
        
        # Message
        ttk.Label(item_frame, text=notification['message'],
                 font=("Segoe UI", 9),
                 background=self.main_window.colors['bg_light'],
                 foreground=self.main_window.colors['text_white'],
                 wraplength=600).pack(anchor="w", pady=(5, 0))
    
    def populate_suggestions(self):
        """Populate smart suggestions"""
        # Clear existing suggestions
        for widget in self.suggestions_content_frame.winfo_children():
            widget.destroy()
        
        # Update system status
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk_usage = psutil.disk_usage('C:')
            disk_percent = (disk_usage.used / disk_usage.total) * 100
            
            status_text = f"CPU: {cpu_percent:.1f}% | RAM: {memory.percent:.1f}% | Disk: {disk_percent:.1f}%"
            self.system_status_label.config(text=status_text)
            
            # Generate suggestions
            self.generate_smart_suggestions(cpu_percent, memory.percent, disk_percent)
            
        except Exception as e:
            self.system_status_label.config(text=f"Status check error: {e}")
        
        # Show suggestions
        if not self.auto_suggestions:
            ttk.Label(self.suggestions_content_frame, text="✅ System is running optimally!",
                     font=("Segoe UI", 12),
                     background=self.main_window.colors['bg_light'],
                     foreground=self.main_window.colors['success']).pack(pady=20)
        else:
            for i, suggestion in enumerate(self.auto_suggestions[:10]):  # Show max 10
                self.create_suggestion_item(self.suggestions_content_frame, suggestion, i)
    
    def create_suggestion_item(self, parent, suggestion, index):
        """Create suggestion item"""
        item_frame = ttk.Frame(parent, style="Card.TFrame", padding="10")
        item_frame.pack(fill="x", pady=5)
        
        ttk.Label(item_frame, text=f"💡 {suggestion}",
                 font=("Segoe UI", 10),
                 background=self.main_window.colors['bg_light'],
                 foreground=self.main_window.colors['text_white']).pack(side="left")
        
        ttk.Button(item_frame, text="Apply",
                  style="Modern.TButton",
                  command=lambda: self.apply_suggestion(suggestion)).pack(side="right")
    
    def apply_suggestion(self, suggestion):
        """Apply a suggestion"""
        # This would implement the actual suggestion
        self.send_notification("✅ Suggestion Applied", f"Applied: {suggestion}", "success")
    
    def refresh_suggestions(self):
        """Refresh suggestions"""
        self.populate_suggestions()
    
    def update_notification_settings(self):
        """Update notification settings"""
        self.notifications_enabled = self.notifications_var.get()
        self.sound_enabled = self.sound_var.get()
        self.desktop_notifications = self.desktop_var.get()
        self.save_settings()
        
        # Update toggle button
        if hasattr(self, 'toggle_btn'):
            status_text = "🔕 Kapat" if self.notifications_enabled else "🔔 Aç"
            style = "Warning.TButton" if self.notifications_enabled else "Success.TButton"
            self.toggle_btn.config(text=status_text, style=style)
    
    def update_threshold(self, key, value):
        """Update threshold value"""
        self.thresholds[key] = int(float(value))
        self.save_settings()
    
    def toggle_notifications(self):
        """Toggle notifications on/off"""
        self.notifications_enabled = not self.notifications_enabled
        self.notifications_var.set(self.notifications_enabled)
        self.update_notification_settings()
    
    def clear_all_notifications(self):
        """Clear all notifications"""
        self.notification_history.clear()
        self.populate_notification_history()
        self.send_notification("🗑️ Cleared", "All notifications cleared", "info")
    
    def send_test_notification(self):
        """Send test notification"""
        self.send_notification(
            "🧪 Test Notification",
            "This is a test notification with suggestions",
            "info",
            suggestions=["This is a test suggestion", "Another test suggestion"]
        )
    
    def update_system_alerts(self):
        """Update system alerts display"""
        # This would show current system alerts
        pass
    
    def setup_scheduled_notifications(self):
        """Setup scheduled notifications"""
        # Daily system health check
        schedule.every().day.at("09:00").do(self.daily_health_check)
        
        # Weekly maintenance reminder
        schedule.every().monday.at("10:00").do(self.weekly_maintenance_reminder)
        
        # Monthly security scan reminder
        schedule.every(30).days.do(self.monthly_security_reminder)
    
    def schedule_runner(self):
        """Run scheduled notifications"""
        while self.monitoring_active:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except Exception as e:
                print(f"Schedule error: {e}")
                time.sleep(60)
    
    def daily_health_check(self):
        """Daily health check notification"""
        self.send_notification(
            "🏥 Daily Health Check",
            "Daily system health check completed",
            "info",
            suggestions=["Run system optimization", "Check for updates"]
        )
    
    def weekly_maintenance_reminder(self):
        """Weekly maintenance reminder"""
        self.send_notification(
            "🔧 Weekly Maintenance",
            "Time for weekly system maintenance",
            "info",
            suggestions=["Clean temporary files", "Defragment drives", "Update software"]
        )
    
    def monthly_security_reminder(self):
        """Monthly security scan reminder"""
        self.send_notification(
            "🛡️ Security Scan",
            "Monthly security scan recommended",
            "warning",
            suggestions=["Run full antivirus scan", "Update security definitions", "Check firewall settings"]
        )
