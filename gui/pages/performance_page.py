"""
Modern Performance Page for DonTe Cleaner v3.0
"""

import tkinter as tk
import threading
import time
import psutil
from gui.modern_ui import HolographicCard, AnimatedButton, NeonProgressBar

class PerformancePage:
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.colors = main_window.colors
        
        # Create performance interface
        self.create_performance_interface()
        
        # Start real-time monitoring
        self.start_monitoring()
    
    def create_performance_interface(self):
        """Create performance monitoring interface"""
        main_frame = tk.Frame(self.parent, bg=self.colors['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Real-time metrics
        self.create_metrics_section(main_frame)
        
        # Performance tools
        self.create_tools_section(main_frame)
        
        # System resources
        self.create_resources_section(main_frame)
    
    def create_header(self, parent):
        """Create header section"""
        header_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Title
        title_label = tk.Label(header_frame, text="📊 Performance Monitor",
                              bg=self.colors['bg_primary'], fg=self.colors['accent_gold'],
                              font=('Segoe UI', 24, 'bold'))
        title_label.pack(side='left')
        
        # Performance boost button
        self.boost_btn = AnimatedButton(header_frame, text="🚀 Boost Performance",
                                       width=200, height=40,
                                       bg_color=self.colors['accent_gold'],
                                       hover_color='#ffed4a',
                                       text_color='black',
                                       command=self.boost_performance)
        self.boost_btn.pack(side='right')
    
    def create_metrics_section(self, parent):
        """Create real-time metrics section"""
        metrics_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        metrics_frame.pack(fill='x', pady=(0, 20))
        
        # CPU card
        cpu_card = HolographicCard(metrics_frame, width=250, height=200,
                                  title="🖥️ CPU Usage")
        cpu_card.pack(side='left', padx=(0, 20))
        
        self.cpu_percent = tk.Label(cpu_card, text="0%",
                                   bg=self.colors['bg_tertiary'], fg=self.colors['accent_primary'],
                                   font=('Segoe UI', 36, 'bold'))
        self.cpu_percent.place(x=90, y=80)
        
        self.cpu_cores = tk.Label(cpu_card, text="Cores: Detecting...",
                                 bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'],
                                 font=('Segoe UI', 10))
        self.cpu_cores.place(x=20, y=140)
        
        self.cpu_freq = tk.Label(cpu_card, text="Freq: Calculating...",
                                bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'],
                                font=('Segoe UI', 10))
        self.cpu_freq.place(x=20, y=160)
        
        # Memory card
        memory_card = HolographicCard(metrics_frame, width=250, height=200,
                                     title="🧠 Memory Usage")
        memory_card.pack(side='left', padx=(0, 20))
        
        self.memory_percent = tk.Label(memory_card, text="0%",
                                      bg=self.colors['bg_tertiary'], fg=self.colors['accent_secondary'],
                                      font=('Segoe UI', 36, 'bold'))
        self.memory_percent.place(x=90, y=80)
        
        self.memory_used = tk.Label(memory_card, text="Used: 0 GB",
                                   bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'],
                                   font=('Segoe UI', 10))
        self.memory_used.place(x=20, y=140)
        
        self.memory_total = tk.Label(memory_card, text="Total: 0 GB",
                                    bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'],
                                    font=('Segoe UI', 10))
        self.memory_total.place(x=20, y=160)
        
        # Disk card
        disk_card = HolographicCard(metrics_frame, width=250, height=200,
                                   title="💾 Disk Usage")
        disk_card.pack(side='left')
        
        self.disk_percent = tk.Label(disk_card, text="0%",
                                    bg=self.colors['bg_tertiary'], fg=self.colors['accent_gold'],
                                    font=('Segoe UI', 36, 'bold'))
        self.disk_percent.place(x=90, y=80)
        
        self.disk_used = tk.Label(disk_card, text="Used: 0 GB",
                                 bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'],
                                 font=('Segoe UI', 10))
        self.disk_used.place(x=20, y=140)
        
        self.disk_free = tk.Label(disk_card, text="Free: 0 GB",
                                 bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'],
                                 font=('Segoe UI', 10))
        self.disk_free.place(x=20, y=160)
    
    def create_tools_section(self, parent):
        """Create performance tools section"""
        tools_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        tools_frame.pack(fill='x', pady=(0, 20))
        
        # Quick tools card
        tools_card = HolographicCard(tools_frame, width=380, height=250,
                                    title="🛠️ Performance Tools")
        tools_card.pack(side='left', padx=(0, 20))
        
        # Tool buttons
        btn_frame = tk.Frame(tools_card, bg=self.colors['bg_tertiary'])
        btn_frame.place(x=30, y=60)
        
        memory_btn = AnimatedButton(btn_frame, text="🧹 Clear Memory",
                                   width=150, height=35,
                                   bg_color=self.colors['accent_primary'],
                                   hover_color='#00ff80',
                                   text_color='black',
                                   command=self.clear_memory)
        memory_btn.pack(pady=5)
        
        startup_btn = AnimatedButton(btn_frame, text="🚀 Manage Startup",
                                    width=150, height=35,
                                    bg_color=self.colors['accent_secondary'],
                                    hover_color='#ff4081',
                                    text_color='white',
                                    command=self.manage_startup)
        startup_btn.pack(pady=5)
        
        services_btn = AnimatedButton(btn_frame, text="⚙️ Optimize Services",
                                     width=150, height=35,
                                     bg_color=self.colors['accent_gold'],
                                     hover_color='#ffed4a',
                                     text_color='black',
                                     command=self.optimize_services)
        services_btn.pack(pady=5)
        
        defrag_btn = AnimatedButton(btn_frame, text="🔧 Defrag Registry",
                                   width=150, height=35,
                                   bg_color=self.colors['bg_secondary'],
                                   hover_color=self.colors['accent_primary'],
                                   text_color=self.colors['text_primary'],
                                   command=self.defrag_registry)
        defrag_btn.pack(pady=5)
        
        # System health card
        health_card = HolographicCard(tools_frame, width=380, height=250,
                                     title="❤️ System Health")
        health_card.pack(side='left')
        
        # Health score
        self.health_score = tk.Label(health_card, text="95",
                                    bg=self.colors['bg_tertiary'], fg=self.colors['success'],
                                    font=('Segoe UI', 48, 'bold'))
        self.health_score.place(x=140, y=80)
        
        health_suffix = tk.Label(health_card, text="/100",
                                bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'],
                                font=('Segoe UI', 16))
        health_suffix.place(x=210, y=110)
        
        # Health details
        self.health_status = tk.Label(health_card, text="Excellent",
                                     bg=self.colors['bg_tertiary'], fg=self.colors['success'],
                                     font=('Segoe UI', 14, 'bold'))
        self.health_status.place(x=130, y=150)
        
        # Health recommendations
        rec_text = tk.Text(health_card, width=35, height=3,
                          bg=self.colors['bg_secondary'], fg=self.colors['text_secondary'],
                          font=('Segoe UI', 9), wrap=tk.WORD)
        rec_text.place(x=30, y=180)
        rec_text.insert(tk.END, "• System running optimally\n• No immediate action needed\n• Next scan: Today")
        rec_text.config(state=tk.DISABLED)
    
    def create_resources_section(self, parent):
        """Create system resources section"""
        resources_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        resources_frame.pack(fill='x')
        
        # Processes card
        processes_card = HolographicCard(resources_frame, width=380, height=200,
                                        title="⚙️ Top Processes")
        processes_card.pack(side='left', padx=(0, 20))
        
        # Process list (simplified)
        self.process_list = tk.Text(processes_card, width=35, height=8,
                                   bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                                   font=('Consolas', 9))
        self.process_list.place(x=30, y=60)
        
        # Network card
        network_card = HolographicCard(resources_frame, width=380, height=200,
                                      title="🌐 Network Activity")
        network_card.pack(side='left')
        
        self.network_up = tk.Label(network_card, text="Upload: 0 KB/s",
                                  bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                  font=('Segoe UI', 12))
        self.network_up.place(x=30, y=70)
        
        self.network_down = tk.Label(network_card, text="Download: 0 KB/s",
                                    bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                    font=('Segoe UI', 12))
        self.network_down.place(x=30, y=100)
        
        self.network_total = tk.Label(network_card, text="Total: 0 MB",
                                     bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'],
                                     font=('Segoe UI', 11))
        self.network_total.place(x=30, y=130)
        
        self.connections = tk.Label(network_card, text="Connections: 0",
                                   bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'],
                                   font=('Segoe UI', 11))
        self.connections.place(x=30, y=155)
    
    def start_monitoring(self):
        """Start real-time performance monitoring"""
        self.update_metrics()
    
    def update_metrics(self):
        """Update performance metrics"""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent()
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            self.cpu_percent.config(text=f"{cpu_percent:.0f}%")
            self.cpu_cores.config(text=f"Cores: {cpu_count}")
            if cpu_freq:
                self.cpu_freq.config(text=f"Freq: {cpu_freq.current:.0f} MHz")
            
            # Memory metrics
            memory = psutil.virtual_memory()
            self.memory_percent.config(text=f"{memory.percent:.0f}%")
            self.memory_used.config(text=f"Used: {memory.used // (1024**3):.1f} GB")
            self.memory_total.config(text=f"Total: {memory.total // (1024**3):.1f} GB")
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            self.disk_percent.config(text=f"{disk_percent:.0f}%")
            self.disk_used.config(text=f"Used: {disk.used // (1024**3):.0f} GB")
            self.disk_free.config(text=f"Free: {disk.free // (1024**3):.0f} GB")
            
            # Network metrics (simplified)
            net_io = psutil.net_io_counters()
            self.network_up.config(text="Upload: 12 KB/s")
            self.network_down.config(text="Download: 156 KB/s")
            self.network_total.config(text=f"Total: {(net_io.bytes_sent + net_io.bytes_recv) // (1024**2):.0f} MB")
            
            # Connection count
            connections = len(psutil.net_connections())
            self.connections.config(text=f"Connections: {connections}")
            
            # Update process list
            self.update_process_list()
            
            # Calculate health score
            health = 100 - max(0, min(100, cpu_percent + memory.percent - 100))
            self.health_score.config(text=f"{health:.0f}")
            
            if health >= 90:
                self.health_status.config(text="Excellent", fg=self.colors['success'])
            elif health >= 70:
                self.health_status.config(text="Good", fg=self.colors['accent_primary'])
            elif health >= 50:
                self.health_status.config(text="Fair", fg=self.colors['accent_gold'])
            else:
                self.health_status.config(text="Poor", fg=self.colors['danger'])
            
            # Schedule next update
            self.parent.after(2000, self.update_metrics)
            
        except Exception as e:
            print(f"Metrics update error: {e}")
            self.parent.after(5000, self.update_metrics)
    
    def update_process_list(self):
        """Update top processes list"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    processes.append((proc.info['name'], proc.info['cpu_percent']))
                except:
                    continue
            
            # Sort by CPU usage and get top 5
            processes.sort(key=lambda x: x[1] if x[1] else 0, reverse=True)
            top_processes = processes[:5]
            
            # Update display
            self.process_list.config(state=tk.NORMAL)
            self.process_list.delete(1.0, tk.END)
            
            for name, cpu in top_processes:
                cpu_val = cpu if cpu else 0
                self.process_list.insert(tk.END, f"{name[:20]:<20} {cpu_val:>6.1f}%\n")
            
            self.process_list.config(state=tk.DISABLED)
            
        except Exception as e:
            print(f"Process list update error: {e}")
    
    def boost_performance(self):
        """Boost system performance"""
        self.boost_btn.config(text="🔄 Boosting...", state='disabled')
        
        def boost_worker():
            try:
                # Simulate performance boost tasks
                tasks = [
                    "Clearing memory cache...",
                    "Optimizing processes...", 
                    "Cleaning temporary files...",
                    "Adjusting system priorities...",
                    "Finalizing optimizations..."
                ]
                
                for task in tasks:
                    self.parent.after(0, lambda t=task: print(f"Performance boost: {t}"))
                    time.sleep(1)
                
                self.parent.after(0, self.boost_complete)
                
            except Exception as e:
                self.parent.after(0, lambda: print(f"Performance boost error: {e}"))
        
        threading.Thread(target=boost_worker, daemon=True).start()
    
    def boost_complete(self):
        """Handle boost completion"""
        self.boost_btn.config(text="🚀 Boost Performance", state='normal')
        # Would show success message
        print("Performance boost completed!")
    
    def clear_memory(self):
        """Clear system memory"""
        # Simulate memory clearing
        print("Clearing system memory...")
        
    def manage_startup(self):
        """Manage startup programs"""
        # Would open startup manager
        print("Opening startup manager...")
        
    def optimize_services(self):
        """Optimize system services"""
        # Would optimize services
        print("Optimizing system services...")
        
    def defrag_registry(self):
        """Defragment registry"""
        # Would defrag registry
        print("Defragmenting registry...")
