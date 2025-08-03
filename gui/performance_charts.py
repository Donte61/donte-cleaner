"""
Performance Charts Module for DonTe Cleaner
Beautiful real-time performance monitoring with charts
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
import psutil
import time
from collections import deque
import threading
import numpy as np

class PerformanceCharts:
    def __init__(self, main_window):
        self.main_window = main_window
        self.is_monitoring = False
        self.animation = None
        
        # Data storage (keep last 60 points = 1 minute if updated every second)
        self.cpu_data = deque(maxlen=60)
        self.ram_data = deque(maxlen=60)
        self.disk_data = deque(maxlen=60)
        self.network_data = deque(maxlen=60)
        self.gpu_data = deque(maxlen=60)
        self.time_data = deque(maxlen=60)
        
        # Initialize with zeros
        for _ in range(60):
            self.cpu_data.append(0)
            self.ram_data.append(0)
            self.disk_data.append(0)
            self.network_data.append(0)
            self.gpu_data.append(0)
            self.time_data.append(0)
        
        # Network monitoring
        self.last_net_io = psutil.net_io_counters()
        self.last_net_time = time.time()
        
        # Chart styles
        plt.style.use('dark_background')
        self.setup_chart_colors()
    
    def setup_chart_colors(self):
        """Setup chart color scheme"""
        self.colors = {
            'bg': self.main_window.colors['bg_dark'],
            'fg': self.main_window.colors['text_white'],
            'cpu': '#ff6b6b',      # Red
            'ram': '#4ecdc4',      # Teal
            'disk': '#45b7d1',     # Blue
            'network': '#96ceb4',  # Green
            'gpu': '#feca57',      # Yellow
            'grid': '#404040'
        }
    
    def show_performance_charts(self):
        """Show performance charts window"""
        self.chart_window = tk.Toplevel(self.main_window.root)
        self.chart_window.title("📊 Performance Charts - Real-time Monitoring")
        self.chart_window.geometry("1200x800")
        self.chart_window.configure(bg=self.main_window.colors['bg_dark'])
        self.chart_window.transient(self.main_window.root)
        
        # Create charts interface
        self.create_charts_interface()
        
        # Start monitoring
        self.start_monitoring()
        
        # Handle window close
        self.chart_window.protocol("WM_DELETE_WINDOW", self.on_chart_window_close)
        
        # Center window
        self.center_chart_window()
    
    def center_chart_window(self):
        """Center chart window"""
        self.chart_window.update_idletasks()
        width = self.chart_window.winfo_width()
        height = self.chart_window.winfo_height()
        x = (self.chart_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.chart_window.winfo_screenheight() // 2) - (height // 2)
        self.chart_window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_charts_interface(self):
        """Create charts interface"""
        main_frame = ttk.Frame(self.chart_window, style="Modern.TFrame", padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Header with controls
        self.create_chart_header(main_frame)
        
        # Charts notebook
        self.create_charts_notebook(main_frame)
    
    def create_chart_header(self, parent):
        """Create chart header with controls"""
        header_frame = ttk.Frame(parent, style="Modern.TFrame")
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Title
        ttk.Label(header_frame, text="📊 Real-time Performance Monitor", 
                 font=("Segoe UI", 18, "bold"),
                 background=self.main_window.colors['bg_dark'],
                 foreground=self.main_window.colors['text_white']).pack(side="left")
        
        # Controls
        controls_frame = ttk.Frame(header_frame, style="Modern.TFrame")
        controls_frame.pack(side="right")
        
        # Monitoring toggle
        self.monitor_btn = ttk.Button(controls_frame, text="⏸️ Duraklat",
                                     style="Warning.TButton",
                                     command=self.toggle_monitoring)
        self.monitor_btn.pack(side="right", padx=(10, 0))
        
        # Export data
        ttk.Button(controls_frame, text="💾 Veri Kaydet",
                  style="Modern.TButton",
                  command=self.export_chart_data).pack(side="right", padx=(10, 0))
        
        # Settings
        ttk.Button(controls_frame, text="⚙️ Ayarlar",
                  style="Modern.TButton",
                  command=self.show_chart_settings).pack(side="right", padx=(10, 0))
    
    def create_charts_notebook(self, parent):
        """Create charts notebook with different views"""
        self.charts_notebook = ttk.Notebook(parent, style="Modern.TNotebook")
        self.charts_notebook.pack(fill="both", expand=True)
        
        # Overview tab (all charts)
        self.create_overview_charts()
        
        # Individual metric tabs
        self.create_cpu_chart_tab()
        self.create_memory_chart_tab()
        self.create_disk_chart_tab()
        self.create_network_chart_tab()
        self.create_comparison_tab()
    
    def create_overview_charts(self):
        """Create overview tab with all charts"""
        overview_frame = ttk.Frame(self.charts_notebook, style="Modern.TFrame")
        self.charts_notebook.add(overview_frame, text="🔍 Overview")
        
        # Create matplotlib figure with subplots
        self.overview_fig = Figure(figsize=(12, 8), dpi=100, facecolor=self.colors['bg'])
        self.overview_fig.suptitle('System Performance Overview', color=self.colors['fg'], fontsize=16)
        
        # Create subplots (2x2 grid)
        self.cpu_ax = self.overview_fig.add_subplot(2, 2, 1)
        self.ram_ax = self.overview_fig.add_subplot(2, 2, 2)
        self.disk_ax = self.overview_fig.add_subplot(2, 2, 3)
        self.network_ax = self.overview_fig.add_subplot(2, 2, 4)
        
        # Style subplots
        for ax, title, color in [(self.cpu_ax, 'CPU Usage (%)', self.colors['cpu']),
                                (self.ram_ax, 'RAM Usage (%)', self.colors['ram']),
                                (self.disk_ax, 'Disk Usage (%)', self.colors['disk']),
                                (self.network_ax, 'Network (MB/s)', self.colors['network'])]:
            ax.set_title(title, color=color, fontweight='bold')
            ax.set_facecolor(self.colors['bg'])
            ax.tick_params(colors=self.colors['fg'])
            ax.spines['bottom'].set_color(self.colors['fg'])
            ax.spines['top'].set_color(self.colors['fg'])
            ax.spines['right'].set_color(self.colors['fg'])
            ax.spines['left'].set_color(self.colors['fg'])
            ax.grid(True, alpha=0.3, color=self.colors['grid'])
            ax.set_ylim(0, 100)
            ax.set_xlim(0, 60)
        
        # Network chart has different y-limit
        self.network_ax.set_ylim(0, 10)  # Will adjust dynamically
        
        # Create canvas
        self.overview_canvas = FigureCanvasTkAgg(self.overview_fig, overview_frame)
        self.overview_canvas.draw()
        self.overview_canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Tight layout
        self.overview_fig.tight_layout()
    
    def create_cpu_chart_tab(self):
        """Create detailed CPU chart tab"""
        cpu_frame = ttk.Frame(self.charts_notebook, style="Modern.TFrame")
        self.charts_notebook.add(cpu_frame, text="💻 CPU")
        
        # CPU figure
        self.cpu_fig = Figure(figsize=(12, 6), dpi=100, facecolor=self.colors['bg'])
        self.cpu_detailed_ax = self.cpu_fig.add_subplot(1, 1, 1)
        
        self.cpu_detailed_ax.set_title('CPU Usage - Detailed View', color=self.colors['cpu'], fontsize=14, fontweight='bold')
        self.cpu_detailed_ax.set_facecolor(self.colors['bg'])
        self.cpu_detailed_ax.tick_params(colors=self.colors['fg'])
        self.cpu_detailed_ax.spines['bottom'].set_color(self.colors['fg'])
        self.cpu_detailed_ax.spines['top'].set_color(self.colors['fg'])
        self.cpu_detailed_ax.spines['right'].set_color(self.colors['fg'])
        self.cpu_detailed_ax.spines['left'].set_color(self.colors['fg'])
        self.cpu_detailed_ax.grid(True, alpha=0.3, color=self.colors['grid'])
        self.cpu_detailed_ax.set_ylim(0, 100)
        self.cpu_detailed_ax.set_ylabel('Usage (%)', color=self.colors['fg'])
        self.cpu_detailed_ax.set_xlabel('Time (seconds)', color=self.colors['fg'])
        
        # Stats frame
        stats_frame = ttk.Frame(cpu_frame, style="Card.TFrame", padding="10")
        stats_frame.pack(fill="x", padx=10, pady=5)
        
        self.cpu_stats_label = ttk.Label(stats_frame, text="CPU Stats Loading...",
                                        font=("Segoe UI", 10),
                                        background=self.main_window.colors['bg_light'],
                                        foreground=self.main_window.colors['text_white'])
        self.cpu_stats_label.pack()
        
        # Canvas
        self.cpu_canvas = FigureCanvasTkAgg(self.cpu_fig, cpu_frame)
        self.cpu_canvas.draw()
        self.cpu_canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=5)
        
        self.cpu_fig.tight_layout()
    
    def create_memory_chart_tab(self):
        """Create detailed memory chart tab"""
        memory_frame = ttk.Frame(self.charts_notebook, style="Modern.TFrame")
        self.charts_notebook.add(memory_frame, text="🧠 Memory")
        
        # Memory figure
        self.memory_fig = Figure(figsize=(12, 6), dpi=100, facecolor=self.colors['bg'])
        self.memory_detailed_ax = self.memory_fig.add_subplot(1, 1, 1)
        
        self.memory_detailed_ax.set_title('Memory Usage - Detailed View', color=self.colors['ram'], fontsize=14, fontweight='bold')
        self.memory_detailed_ax.set_facecolor(self.colors['bg'])
        self.memory_detailed_ax.tick_params(colors=self.colors['fg'])
        self.memory_detailed_ax.spines['bottom'].set_color(self.colors['fg'])
        self.memory_detailed_ax.spines['top'].set_color(self.colors['fg'])
        self.memory_detailed_ax.spines['right'].set_color(self.colors['fg'])
        self.memory_detailed_ax.spines['left'].set_color(self.colors['fg'])
        self.memory_detailed_ax.grid(True, alpha=0.3, color=self.colors['grid'])
        self.memory_detailed_ax.set_ylim(0, 100)
        self.memory_detailed_ax.set_ylabel('Usage (%)', color=self.colors['fg'])
        self.memory_detailed_ax.set_xlabel('Time (seconds)', color=self.colors['fg'])
        
        # Stats frame
        stats_frame = ttk.Frame(memory_frame, style="Card.TFrame", padding="10")
        stats_frame.pack(fill="x", padx=10, pady=5)
        
        self.memory_stats_label = ttk.Label(stats_frame, text="Memory Stats Loading...",
                                           font=("Segoe UI", 10),
                                           background=self.main_window.colors['bg_light'],
                                           foreground=self.main_window.colors['text_white'])
        self.memory_stats_label.pack()
        
        # Canvas
        self.memory_canvas = FigureCanvasTkAgg(self.memory_fig, memory_frame)
        self.memory_canvas.draw()
        self.memory_canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=5)
        
        self.memory_fig.tight_layout()
    
    def create_disk_chart_tab(self):
        """Create detailed disk chart tab"""
        disk_frame = ttk.Frame(self.charts_notebook, style="Modern.TFrame")
        self.charts_notebook.add(disk_frame, text="💾 Disk")
        
        # Create disk charts (usage + I/O)
        self.disk_fig = Figure(figsize=(12, 8), dpi=100, facecolor=self.colors['bg'])
        
        # Disk usage chart
        self.disk_usage_ax = self.disk_fig.add_subplot(2, 1, 1)
        self.disk_usage_ax.set_title('Disk Usage', color=self.colors['disk'], fontsize=12, fontweight='bold')
        self.disk_usage_ax.set_facecolor(self.colors['bg'])
        self.disk_usage_ax.tick_params(colors=self.colors['fg'])
        for spine in self.disk_usage_ax.spines.values():
            spine.set_color(self.colors['fg'])
        self.disk_usage_ax.grid(True, alpha=0.3, color=self.colors['grid'])
        self.disk_usage_ax.set_ylim(0, 100)
        self.disk_usage_ax.set_ylabel('Usage (%)', color=self.colors['fg'])
        
        # Disk I/O chart
        self.disk_io_ax = self.disk_fig.add_subplot(2, 1, 2)
        self.disk_io_ax.set_title('Disk I/O Activity', color=self.colors['disk'], fontsize=12, fontweight='bold')
        self.disk_io_ax.set_facecolor(self.colors['bg'])
        self.disk_io_ax.tick_params(colors=self.colors['fg'])
        for spine in self.disk_io_ax.spines.values():
            spine.set_color(self.colors['fg'])
        self.disk_io_ax.grid(True, alpha=0.3, color=self.colors['grid'])
        self.disk_io_ax.set_ylabel('I/O (MB/s)', color=self.colors['fg'])
        self.disk_io_ax.set_xlabel('Time (seconds)', color=self.colors['fg'])
        
        # Canvas
        self.disk_canvas = FigureCanvasTkAgg(self.disk_fig, disk_frame)
        self.disk_canvas.draw()
        self.disk_canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        self.disk_fig.tight_layout()
    
    def create_network_chart_tab(self):
        """Create detailed network chart tab"""
        network_frame = ttk.Frame(self.charts_notebook, style="Modern.TFrame")
        self.charts_notebook.add(network_frame, text="🌐 Network")
        
        # Network figure with upload/download
        self.network_fig = Figure(figsize=(12, 8), dpi=100, facecolor=self.colors['bg'])
        
        # Combined upload/download chart
        self.network_combined_ax = self.network_fig.add_subplot(2, 1, 1)
        self.network_combined_ax.set_title('Network Traffic', color=self.colors['network'], fontsize=12, fontweight='bold')
        self.network_combined_ax.set_facecolor(self.colors['bg'])
        self.network_combined_ax.tick_params(colors=self.colors['fg'])
        for spine in self.network_combined_ax.spines.values():
            spine.set_color(self.colors['fg'])
        self.network_combined_ax.grid(True, alpha=0.3, color=self.colors['grid'])
        self.network_combined_ax.set_ylabel('Speed (MB/s)', color=self.colors['fg'])
        
        # Network usage percentage
        self.network_usage_ax = self.network_fig.add_subplot(2, 1, 2)
        self.network_usage_ax.set_title('Network Utilization', color=self.colors['network'], fontsize=12, fontweight='bold')
        self.network_usage_ax.set_facecolor(self.colors['bg'])
        self.network_usage_ax.tick_params(colors=self.colors['fg'])
        for spine in self.network_usage_ax.spines.values():
            spine.set_color(self.colors['fg'])
        self.network_usage_ax.grid(True, alpha=0.3, color=self.colors['grid'])
        self.network_usage_ax.set_ylabel('Utilization (%)', color=self.colors['fg'])
        self.network_usage_ax.set_xlabel('Time (seconds)', color=self.colors['fg'])
        self.network_usage_ax.set_ylim(0, 100)
        
        # Canvas
        self.network_canvas = FigureCanvasTkAgg(self.network_fig, network_frame)
        self.network_canvas.draw()
        self.network_canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        self.network_fig.tight_layout()
    
    def create_comparison_tab(self):
        """Create comparison charts tab"""
        comparison_frame = ttk.Frame(self.charts_notebook, style="Modern.TFrame")
        self.charts_notebook.add(comparison_frame, text="📊 Comparison")
        
        # Comparison figure
        self.comparison_fig = Figure(figsize=(12, 8), dpi=100, facecolor=self.colors['bg'])
        
        # All metrics on one chart
        self.comparison_ax = self.comparison_fig.add_subplot(1, 1, 1)
        self.comparison_ax.set_title('All Metrics Comparison', color=self.colors['fg'], fontsize=14, fontweight='bold')
        self.comparison_ax.set_facecolor(self.colors['bg'])
        self.comparison_ax.tick_params(colors=self.colors['fg'])
        for spine in self.comparison_ax.spines.values():
            spine.set_color(self.colors['fg'])
        self.comparison_ax.grid(True, alpha=0.3, color=self.colors['grid'])
        self.comparison_ax.set_ylim(0, 100)
        self.comparison_ax.set_ylabel('Usage (%)', color=self.colors['fg'])
        self.comparison_ax.set_xlabel('Time (seconds)', color=self.colors['fg'])
        
        # Legend will be added dynamically
        
        # Canvas
        self.comparison_canvas = FigureCanvasTkAgg(self.comparison_fig, comparison_frame)
        self.comparison_canvas.draw()
        self.comparison_canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        self.comparison_fig.tight_layout()
    
    def start_monitoring(self):
        """Start performance monitoring"""
        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(target=self.monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        # Start chart animation
        self.animation = animation.FuncAnimation(
            self.overview_fig, self.update_charts, interval=1000, blit=False, cache_frame_data=False
        )
    
    def monitoring_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                # Get system metrics
                cpu_percent = psutil.cpu_percent(interval=0.1)
                memory = psutil.virtual_memory()
                disk_usage = psutil.disk_usage('C:')
                disk_percent = (disk_usage.used / disk_usage.total) * 100
                
                # Get network speed
                network_speed = self.get_network_speed()
                
                # Get GPU usage (if available)
                gpu_percent = self.get_gpu_usage()
                
                # Add to data queues
                current_time = time.time()
                self.cpu_data.append(cpu_percent)
                self.ram_data.append(memory.percent)
                self.disk_data.append(disk_percent)
                self.network_data.append(network_speed)
                self.gpu_data.append(gpu_percent)
                self.time_data.append(current_time)
                
                # Update stats labels
                self.chart_window.after(0, self.update_stats_labels)
                
                time.sleep(1)  # Update every second
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(1)
    
    def get_network_speed(self):
        """Calculate network speed in MB/s"""
        try:
            current_net_io = psutil.net_io_counters()
            current_time = time.time()
            
            # Calculate bytes per second
            time_delta = current_time - self.last_net_time
            bytes_sent = current_net_io.bytes_sent - self.last_net_io.bytes_sent
            bytes_recv = current_net_io.bytes_recv - self.last_net_io.bytes_recv
            
            # Convert to MB/s
            if time_delta > 0:
                speed_mbps = (bytes_sent + bytes_recv) / time_delta / (1024 * 1024)
            else:
                speed_mbps = 0
            
            # Update for next calculation
            self.last_net_io = current_net_io
            self.last_net_time = current_time
            
            return min(speed_mbps, 100)  # Cap at 100 MB/s for chart scaling
            
        except Exception:
            return 0
    
    def get_gpu_usage(self):
        """Get GPU usage percentage (if available)"""
        try:
            # Try to get GPU usage using nvidia-ml-py or similar
            # For now, return 0 as placeholder
            return 0
        except Exception:
            return 0
    
    def update_charts(self, frame):
        """Update all charts"""
        try:
            if not self.is_monitoring or len(self.cpu_data) == 0:
                return
            
            # Create time axis (last 60 seconds)
            x_data = list(range(len(self.cpu_data)))
            
            # Overview charts
            self.cpu_ax.clear()
            self.ram_ax.clear()
            self.disk_ax.clear()
            self.network_ax.clear()
            
            # Style and plot each chart
            charts_data = [
                (self.cpu_ax, self.cpu_data, 'CPU Usage (%)', self.colors['cpu']),
                (self.ram_ax, self.ram_data, 'RAM Usage (%)', self.colors['ram']),
                (self.disk_ax, self.disk_data, 'Disk Usage (%)', self.colors['disk']),
                (self.network_ax, self.network_data, 'Network (MB/s)', self.colors['network'])
            ]
            
            for ax, data, title, color in charts_data:
                ax.plot(x_data, list(data), color=color, linewidth=2, alpha=0.8)
                ax.fill_between(x_data, list(data), alpha=0.3, color=color)
                ax.set_title(title, color=color, fontweight='bold')
                ax.set_facecolor(self.colors['bg'])
                ax.tick_params(colors=self.colors['fg'])
                for spine in ax.spines.values():
                    spine.set_color(self.colors['fg'])
                ax.grid(True, alpha=0.3, color=self.colors['grid'])
                ax.set_xlim(0, 60)
                
                if 'Network' in title:
                    ax.set_ylim(0, max(10, max(data) * 1.2))
                else:
                    ax.set_ylim(0, 100)
            
            # Update detailed charts if they exist
            self.update_detailed_charts(x_data)
            
            # Update comparison chart
            self.update_comparison_chart(x_data)
            
        except Exception as e:
            print(f"Chart update error: {e}")
    
    def update_detailed_charts(self, x_data):
        """Update detailed individual charts"""
        try:
            # CPU detailed chart
            if hasattr(self, 'cpu_detailed_ax'):
                self.cpu_detailed_ax.clear()
                self.cpu_detailed_ax.plot(x_data, list(self.cpu_data), color=self.colors['cpu'], linewidth=3)
                self.cpu_detailed_ax.fill_between(x_data, list(self.cpu_data), alpha=0.3, color=self.colors['cpu'])
                self.cpu_detailed_ax.set_title('CPU Usage - Detailed View', color=self.colors['cpu'], fontsize=14, fontweight='bold')
                self.cpu_detailed_ax.set_facecolor(self.colors['bg'])
                self.cpu_detailed_ax.tick_params(colors=self.colors['fg'])
                for spine in self.cpu_detailed_ax.spines.values():
                    spine.set_color(self.colors['fg'])
                self.cpu_detailed_ax.grid(True, alpha=0.3, color=self.colors['grid'])
                self.cpu_detailed_ax.set_ylim(0, 100)
                self.cpu_detailed_ax.set_ylabel('Usage (%)', color=self.colors['fg'])
                self.cpu_detailed_ax.set_xlabel('Time (seconds)', color=self.colors['fg'])
                self.cpu_canvas.draw()
            
            # Memory detailed chart
            if hasattr(self, 'memory_detailed_ax'):
                self.memory_detailed_ax.clear()
                self.memory_detailed_ax.plot(x_data, list(self.ram_data), color=self.colors['ram'], linewidth=3)
                self.memory_detailed_ax.fill_between(x_data, list(self.ram_data), alpha=0.3, color=self.colors['ram'])
                self.memory_detailed_ax.set_title('Memory Usage - Detailed View', color=self.colors['ram'], fontsize=14, fontweight='bold')
                self.memory_detailed_ax.set_facecolor(self.colors['bg'])
                self.memory_detailed_ax.tick_params(colors=self.colors['fg'])
                for spine in self.memory_detailed_ax.spines.values():
                    spine.set_color(self.colors['fg'])
                self.memory_detailed_ax.grid(True, alpha=0.3, color=self.colors['grid'])
                self.memory_detailed_ax.set_ylim(0, 100)
                self.memory_detailed_ax.set_ylabel('Usage (%)', color=self.colors['fg'])
                self.memory_detailed_ax.set_xlabel('Time (seconds)', color=self.colors['fg'])
                self.memory_canvas.draw()
            
        except Exception as e:
            print(f"Detailed charts update error: {e}")
    
    def update_comparison_chart(self, x_data):
        """Update comparison chart with all metrics"""
        try:
            if hasattr(self, 'comparison_ax'):
                self.comparison_ax.clear()
                
                # Plot all metrics
                self.comparison_ax.plot(x_data, list(self.cpu_data), color=self.colors['cpu'], 
                                      linewidth=2, label='CPU', alpha=0.8)
                self.comparison_ax.plot(x_data, list(self.ram_data), color=self.colors['ram'], 
                                      linewidth=2, label='RAM', alpha=0.8)
                self.comparison_ax.plot(x_data, list(self.disk_data), color=self.colors['disk'], 
                                      linewidth=2, label='Disk', alpha=0.8)
                
                # Scale network data to percentage for comparison
                network_scaled = [min(x * 10, 100) for x in self.network_data]  # Scale network speed
                self.comparison_ax.plot(x_data, network_scaled, color=self.colors['network'], 
                                      linewidth=2, label='Network (scaled)', alpha=0.8)
                
                self.comparison_ax.set_title('All Metrics Comparison', color=self.colors['fg'], 
                                           fontsize=14, fontweight='bold')
                self.comparison_ax.set_facecolor(self.colors['bg'])
                self.comparison_ax.tick_params(colors=self.colors['fg'])
                for spine in self.comparison_ax.spines.values():
                    spine.set_color(self.colors['fg'])
                self.comparison_ax.grid(True, alpha=0.3, color=self.colors['grid'])
                self.comparison_ax.set_ylim(0, 100)
                self.comparison_ax.set_ylabel('Usage (%)', color=self.colors['fg'])
                self.comparison_ax.set_xlabel('Time (seconds)', color=self.colors['fg'])
                self.comparison_ax.legend(facecolor=self.colors['bg'], edgecolor=self.colors['fg'], 
                                        labelcolor=self.colors['fg'])
                
                self.comparison_canvas.draw()
                
        except Exception as e:
            print(f"Comparison chart update error: {e}")
    
    def update_stats_labels(self):
        """Update statistics labels"""
        try:
            if len(self.cpu_data) > 0:
                # CPU stats
                if hasattr(self, 'cpu_stats_label'):
                    cpu_current = self.cpu_data[-1]
                    cpu_avg = sum(self.cpu_data) / len(self.cpu_data)
                    cpu_max = max(self.cpu_data)
                    cpu_stats = f"Current: {cpu_current:.1f}% | Average: {cpu_avg:.1f}% | Peak: {cpu_max:.1f}%"
                    self.cpu_stats_label.config(text=cpu_stats)
                
                # Memory stats
                if hasattr(self, 'memory_stats_label'):
                    ram_current = self.ram_data[-1]
                    ram_avg = sum(self.ram_data) / len(self.ram_data)
                    ram_max = max(self.ram_data)
                    memory_stats = f"Current: {ram_current:.1f}% | Average: {ram_avg:.1f}% | Peak: {ram_max:.1f}%"
                    self.memory_stats_label.config(text=memory_stats)
        
        except Exception as e:
            print(f"Stats update error: {e}")
    
    def toggle_monitoring(self):
        """Toggle monitoring on/off"""
        if self.is_monitoring:
            self.is_monitoring = False
            self.monitor_btn.config(text="▶️ Başlat")
            if self.animation:
                self.animation.event_source.stop()
        else:
            self.is_monitoring = True
            self.monitor_btn.config(text="⏸️ Duraklat")
            self.start_monitoring()
    
    def export_chart_data(self):
        """Export chart data to CSV"""
        try:
            from tkinter import filedialog
            import csv
            
            file_path = filedialog.asksaveasfilename(
                title="Performance Data Kaydet",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Time', 'CPU (%)', 'RAM (%)', 'Disk (%)', 'Network (MB/s)'])
                    
                    for i in range(len(self.cpu_data)):
                        writer.writerow([
                            i,
                            self.cpu_data[i],
                            self.ram_data[i],
                            self.disk_data[i],
                            self.network_data[i]
                        ])
                
                from tkinter import messagebox
                messagebox.showinfo("Başarılı", f"Performance data saved to {file_path}")
                
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Hata", f"Data export error:\n{str(e)}")
    
    def show_chart_settings(self):
        """Show chart settings dialog"""
        # Placeholder for chart settings
        from tkinter import messagebox
        messagebox.showinfo("Chart Settings", "Chart settings will be implemented here.\n\nPlanned features:\n• Update interval\n• Chart colors\n• Data retention time\n• Export formats")
    
    def on_chart_window_close(self):
        """Handle chart window close"""
        self.is_monitoring = False
        if self.animation:
            self.animation.event_source.stop()
        self.chart_window.destroy()
