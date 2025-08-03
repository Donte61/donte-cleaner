"""
Modern Dashboard Page for DonTe Cleaner v3.0
Real-time system overview with holographic design
"""

import tkinter as tk
from tkinter import ttk
import psutil
import time
import threading
from gui.modern_ui import HolographicCard, NeonProgressBar, StatusIndicator

class DashboardPage:
    """Modern dashboard with real-time system monitoring"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.colors = main_window.colors
        
        self.create_dashboard()
        self.start_monitoring()
    
    def create_dashboard(self):
        """Create dashboard layout"""
        # Main dashboard container
        dashboard_frame = tk.Frame(self.parent, bg=self.colors['bg_primary'])
        dashboard_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Top row - System overview cards
        self.create_system_overview(dashboard_frame)
        
        # Middle row - Quick stats and actions
        self.create_quick_stats(dashboard_frame)
        
        # Bottom row - Recent activities and alerts
        self.create_activity_section(dashboard_frame)
    
    def create_system_overview(self, parent):
        """Create system overview cards"""
        overview_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        overview_frame.pack(fill='x', pady=(0, 20))
        
        # CPU Card
        self.cpu_card = HolographicCard(overview_frame, width=280, height=160, 
                                       title="🖥️ CPU Status")
        self.cpu_card.pack(side='left', padx=(0, 15))
        
        self.cpu_usage_bar = NeonProgressBar(self.cpu_card, width=220, height=25)
        self.cpu_usage_bar.place(x=30, y=80)
        
        self.cpu_text = tk.Label(self.cpu_card, text="CPU: 0%", 
                                bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                font=('Segoe UI', 12, 'bold'))
        self.cpu_text.place(x=30, y=55)
        
        self.cpu_temp_text = tk.Label(self.cpu_card, text="Temp: N/A", 
                                     bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'],
                                     font=('Segoe UI', 10))
        self.cpu_temp_text.place(x=30, y=120)
        
        # Memory Card
        self.memory_card = HolographicCard(overview_frame, width=280, height=160,
                                          title="💾 Memory Status")
        self.memory_card.pack(side='left', padx=(0, 15))
        
        self.memory_usage_bar = NeonProgressBar(self.memory_card, width=220, height=25)
        self.memory_usage_bar.place(x=30, y=80)
        
        self.memory_text = tk.Label(self.memory_card, text="RAM: 0%",
                                   bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                   font=('Segoe UI', 12, 'bold'))
        self.memory_text.place(x=30, y=55)
        
        self.memory_available_text = tk.Label(self.memory_card, text="Available: 0 GB",
                                             bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'],
                                             font=('Segoe UI', 10))
        self.memory_available_text.place(x=30, y=120)
        
        # Disk Card
        self.disk_card = HolographicCard(overview_frame, width=280, height=160,
                                        title="💿 Disk Status")
        self.disk_card.pack(side='left', padx=(0, 15))
        
        self.disk_usage_bar = NeonProgressBar(self.disk_card, width=220, height=25)
        self.disk_usage_bar.place(x=30, y=80)
        
        self.disk_text = tk.Label(self.disk_card, text="Disk C: 0%",
                                 bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                 font=('Segoe UI', 12, 'bold'))
        self.disk_text.place(x=30, y=55)
        
        self.disk_free_text = tk.Label(self.disk_card, text="Free: 0 GB",
                                      bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'],
                                      font=('Segoe UI', 10))
        self.disk_free_text.place(x=30, y=120)
        
        # Network Card
        self.network_card = HolographicCard(overview_frame, width=280, height=160,
                                           title="🌐 Network Status")
        self.network_card.pack(side='left')
        
        self.network_status = StatusIndicator(self.network_card, status='active', size=25)
        self.network_status.place(x=30, y=55)
        
        self.network_text = tk.Label(self.network_card, text="Connected",
                                    bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                    font=('Segoe UI', 12, 'bold'))
        self.network_text.place(x=65, y=55)
        
        self.network_speed_text = tk.Label(self.network_card, text="Speed: Checking...",
                                          bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'],
                                          font=('Segoe UI', 10))
        self.network_speed_text.place(x=30, y=90)
    
    def create_quick_stats(self, parent):
        """Create quick statistics section"""
        stats_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        stats_frame.pack(fill='x', pady=(0, 20))
        
        # System health score
        health_card = HolographicCard(stats_frame, width=350, height=200,
                                     title="🏥 System Health Score")
        health_card.pack(side='left', padx=(0, 15))
        
        self.health_score = tk.Label(health_card, text="95",
                                    bg=self.colors['bg_tertiary'], fg=self.colors['accent_primary'],
                                    font=('Segoe UI', 48, 'bold'))
        self.health_score.place(x=150, y=80)
        
        health_suffix = tk.Label(health_card, text="/100",
                                bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'],
                                font=('Segoe UI', 16))
        health_suffix.place(x=220, y=110)
        
        self.health_status = tk.Label(health_card, text="Excellent",
                                     bg=self.colors['bg_tertiary'], fg=self.colors['success'],
                                     font=('Segoe UI', 12, 'bold'))
        self.health_status.place(x=140, y=140)
        
        # Active processes
        processes_card = HolographicCard(stats_frame, width=350, height=200,
                                        title="⚙️ Active Processes")
        processes_card.pack(side='left', padx=(0, 15))
        
        self.process_count = tk.Label(processes_card, text="0",
                                     bg=self.colors['bg_tertiary'], fg=self.colors['accent_secondary'],
                                     font=('Segoe UI', 36, 'bold'))
        self.process_count.place(x=150, y=80)
        
        process_label = tk.Label(processes_card, text="Running",
                                bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'],
                                font=('Segoe UI', 12))
        process_label.place(x=140, y=130)
        
        # Security status
        security_card = HolographicCard(stats_frame, width=350, height=200,
                                       title="🛡️ Security Status")
        security_card.pack(side='left')
        
        self.security_status = StatusIndicator(security_card, status='active', size=40)
        self.security_status.place(x=155, y=80)
        
        self.security_text = tk.Label(security_card, text="Protected",
                                     bg=self.colors['bg_tertiary'], fg=self.colors['success'],
                                     font=('Segoe UI', 16, 'bold'))
        self.security_text.place(x=130, y=130)
        
        self.last_scan_text = tk.Label(security_card, text="Last scan: Today",
                                      bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'],
                                      font=('Segoe UI', 10))
        self.last_scan_text.place(x=120, y=155)
    
    def create_activity_section(self, parent):
        """Create recent activities section"""
        activity_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        activity_frame.pack(fill='both', expand=True)
        
        # Recent activities card
        activities_card = HolographicCard(activity_frame, width=600, height=250,
                                         title="📋 Recent Activities")
        activities_card.pack(side='left', padx=(0, 15), fill='y')
        
        # Activity list
        self.activity_listbox = tk.Listbox(activities_card, 
                                          bg=self.colors['bg_secondary'],
                                          fg=self.colors['text_primary'],
                                          font=('Segoe UI', 10),
                                          borderwidth=0,
                                          highlightthickness=0,
                                          selectbackground=self.colors['accent_primary'])
        self.activity_listbox.place(x=20, y=50, width=560, height=180)
        
        # System alerts card
        alerts_card = HolographicCard(activity_frame, width=480, height=250,
                                     title="⚠️ System Alerts")
        alerts_card.pack(side='left', fill='y')
        
        # Alerts list
        self.alerts_listbox = tk.Listbox(alerts_card,
                                        bg=self.colors['bg_secondary'],
                                        fg=self.colors['text_primary'],
                                        font=('Segoe UI', 10),
                                        borderwidth=0,
                                        highlightthickness=0,
                                        selectbackground=self.colors['warning'])
        self.alerts_listbox.place(x=20, y=50, width=440, height=180)
        
        # Add some sample activities and alerts
        self.add_sample_data()
    
    def add_sample_data(self):
        """Add sample activities and alerts"""
        activities = [
            "🔍 System scan completed - No threats found",
            "🧹 Temporary files cleaned - 2.5 GB freed",
            "⚡ System optimization completed",
            "🛡️ Real-time protection enabled",
            "🎮 Gaming mode activated",
            "📊 Performance monitoring started"
        ]
        
        for activity in activities:
            self.activity_listbox.insert(tk.END, activity)
        
        alerts = [
            "💾 Low disk space on C: drive (15% remaining)",
            "🔥 CPU temperature high (78°C)",
            "🔄 Windows updates available",
            "🛡️ Antivirus definitions need update"
        ]
        
        for alert in alerts:
            self.alerts_listbox.insert(tk.END, alert)
    
    def start_monitoring(self):
        """Start real-time system monitoring"""
        def monitor_worker():
            while True:
                try:
                    # Update CPU usage
                    cpu_percent = psutil.cpu_percent(interval=1)
                    self.main_window.root.after(0, lambda: self.update_cpu(cpu_percent))
                    
                    # Update memory usage
                    memory = psutil.virtual_memory()
                    self.main_window.root.after(0, lambda: self.update_memory(memory))
                    
                    # Update disk usage
                    disk = psutil.disk_usage('C:\\')
                    self.main_window.root.after(0, lambda: self.update_disk(disk))
                    
                    # Update process count
                    process_count = len(psutil.pids())
                    self.main_window.root.after(0, lambda: self.update_processes(process_count))
                    
                    # Update health score
                    health_score = self.calculate_health_score(cpu_percent, memory.percent, 
                                                             disk.percent)
                    self.main_window.root.after(0, lambda: self.update_health(health_score))
                    
                except Exception as e:
                    print(f"Monitoring error: {e}")
                
                time.sleep(5)  # Update every 5 seconds
        
        # Start monitoring in background thread
        threading.Thread(target=monitor_worker, daemon=True).start()
    
    def update_cpu(self, cpu_percent):
        """Update CPU display"""
        self.cpu_usage_bar.set_progress(cpu_percent)
        self.cpu_text.config(text=f"CPU: {cpu_percent:.1f}%")
        
        # Try to get CPU temperature (if available)
        try:
            temps = psutil.sensors_temperatures()
            if 'coretemp' in temps:
                temp = temps['coretemp'][0].current
                self.cpu_temp_text.config(text=f"Temp: {temp:.1f}°C")
        except:
            self.cpu_temp_text.config(text="Temp: N/A")
    
    def update_memory(self, memory):
        """Update memory display"""
        self.memory_usage_bar.set_progress(memory.percent)
        self.memory_text.config(text=f"RAM: {memory.percent:.1f}%")
        
        available_gb = memory.available / (1024**3)
        self.memory_available_text.config(text=f"Available: {available_gb:.1f} GB")
    
    def update_disk(self, disk):
        """Update disk display"""
        used_percent = (disk.used / disk.total) * 100
        self.disk_usage_bar.set_progress(used_percent)
        self.disk_text.config(text=f"Disk C: {used_percent:.1f}%")
        
        free_gb = disk.free / (1024**3)
        self.disk_free_text.config(text=f"Free: {free_gb:.1f} GB")
    
    def update_processes(self, count):
        """Update process count"""
        self.process_count.config(text=str(count))
    
    def update_health(self, score):
        """Update system health score"""
        self.health_score.config(text=str(score))
        
        if score >= 90:
            status_text = "Excellent"
            status_color = self.colors['success']
        elif score >= 70:
            status_text = "Good"
            status_color = self.colors['accent_primary']
        elif score >= 50:
            status_text = "Fair"
            status_color = self.colors['warning']
        else:
            status_text = "Poor"
            status_color = self.colors['danger']
        
        self.health_status.config(text=status_text, fg=status_color)
    
    def calculate_health_score(self, cpu_percent, memory_percent, disk_percent):
        """Calculate overall system health score"""
        score = 100
        
        # Penalize high CPU usage
        if cpu_percent > 80:
            score -= (cpu_percent - 80) * 2
        elif cpu_percent > 60:
            score -= (cpu_percent - 60) * 1
        
        # Penalize high memory usage
        if memory_percent > 85:
            score -= (memory_percent - 85) * 2
        elif memory_percent > 70:
            score -= (memory_percent - 70) * 1
        
        # Penalize high disk usage
        if disk_percent > 90:
            score -= (disk_percent - 90) * 3
        elif disk_percent > 80:
            score -= (disk_percent - 80) * 1.5
        
        return max(0, min(100, int(score)))
