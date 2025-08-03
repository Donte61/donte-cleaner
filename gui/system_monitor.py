"""
DonTe Cleaner - Advanced System Monitor Widget
Real-time system monitoring with beautiful charts and graphs
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import math
from collections import deque

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

class SystemMonitorWidget:
    def __init__(self, parent, width=300, height=200, update_interval=1000):
        self.parent = parent
        self.width = width
        self.height = height
        self.update_interval = update_interval
        self.is_running = False
        
        # Data storage for graphs
        self.cpu_data = deque(maxlen=60)  # Last 60 readings
        self.ram_data = deque(maxlen=60)
        self.disk_data = deque(maxlen=60)
        self.network_data = deque(maxlen=60)
        
        # Colors for different metrics
        self.colors = {
            'cpu': '#58a6ff',      # Blue
            'ram': '#3fb950',      # Green  
            'disk': '#d29922',     # Orange
            'network': '#a5a5ff',  # Purple
            'bg': '#0d1117',       # Dark background
            'grid': '#30363d',     # Grid lines
            'text': '#f0f6fc'      # Text color
        }
        
        self.create_widget()
        
        if PSUTIL_AVAILABLE:
            self.start_monitoring()
        else:
            self.show_no_data_message()
    
    def create_widget(self):
        """Create the monitoring widget"""
        # Main container
        self.container = ttk.Frame(self.parent, style="Card.TFrame")
        self.container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Title
        title_frame = ttk.Frame(self.container, style="Card.TFrame")
        title_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        ttk.Label(title_frame, text="📊 System Monitor", 
                 style="CardTitle.TLabel").pack(side="left")
        
        # Toggle button
        self.toggle_btn = ttk.Button(title_frame, text="●", 
                                   style="Success.TButton",
                                   width=3,
                                   command=self.toggle_monitoring)
        self.toggle_btn.pack(side="right")
        
        # Create notebook for different views
        self.notebook = ttk.Notebook(self.container, style="Modern.TNotebook")
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Real-time tab
        self.create_realtime_tab()
        
        # Graphs tab
        self.create_graphs_tab()
        
        # Details tab
        self.create_details_tab()
    
    def create_realtime_tab(self):
        """Create real-time monitoring tab"""
        self.realtime_frame = ttk.Frame(self.notebook, style="Modern.TFrame")
        self.notebook.add(self.realtime_frame, text="📈 Live")
        
        # Create circular progress indicators
        self.create_circular_indicators()
        
        # System info labels
        info_frame = ttk.Frame(self.realtime_frame, style="Modern.TFrame")
        info_frame.pack(fill="x", padx=10, pady=5)
        
        self.cpu_temp_label = ttk.Label(info_frame, text="CPU Temp: --°C", 
                                       style="CardText.TLabel")
        self.cpu_temp_label.pack(anchor="w")
        
        self.uptime_label = ttk.Label(info_frame, text="Uptime: --", 
                                     style="CardText.TLabel")
        self.uptime_label.pack(anchor="w")
        
        self.processes_label = ttk.Label(info_frame, text="Processes: --", 
                                        style="CardText.TLabel")
        self.processes_label.pack(anchor="w")
    
    def create_circular_indicators(self):
        """Create circular progress indicators"""
        indicators_frame = ttk.Frame(self.realtime_frame, style="Modern.TFrame")
        indicators_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create canvas for circular indicators
        canvas_frame = ttk.Frame(indicators_frame, style="Modern.TFrame")
        canvas_frame.pack(fill="both", expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg=self.colors['bg'], 
                               height=120, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Initialize circular indicators
        self.init_circular_indicators()
    
    def init_circular_indicators(self):
        """Initialize circular progress indicators"""
        self.canvas.delete("all")
        
        # Calculate positions for 4 circles
        canvas_width = self.canvas.winfo_width() or 280
        canvas_height = self.canvas.winfo_height() or 120
        
        if canvas_width < 10:  # Canvas not ready
            self.parent.after(100, self.init_circular_indicators)
            return
        
        circle_radius = 30
        spacing = 70
        start_x = (canvas_width - (4 * spacing - spacing//2)) // 2
        center_y = canvas_height // 2
        
        # Create circles for CPU, RAM, Disk, Network
        metrics = [
            ("CPU", self.colors['cpu']),
            ("RAM", self.colors['ram']),
            ("Disk", self.colors['disk']),
            ("Net", self.colors['network'])
        ]
        
        self.circles = []
        for i, (label, color) in enumerate(metrics):
            x = start_x + i * spacing
            
            # Background circle
            self.canvas.create_oval(x - circle_radius, center_y - circle_radius,
                                  x + circle_radius, center_y + circle_radius,
                                  outline=self.colors['grid'], width=2, fill="")
            
            # Progress arc (will be updated)
            arc_id = self.canvas.create_arc(x - circle_radius, center_y - circle_radius,
                                          x + circle_radius, center_y + circle_radius,
                                          start=90, extent=0, outline=color, 
                                          width=3, style="arc")
            
            # Center text
            text_id = self.canvas.create_text(x, center_y - 5, text="0%", 
                                            fill=self.colors['text'], 
                                            font=("Segoe UI", 8, "bold"))
            
            label_id = self.canvas.create_text(x, center_y + 10, text=label, 
                                             fill=self.colors['text'], 
                                             font=("Segoe UI", 7))
            
            self.circles.append({
                'arc': arc_id,
                'text': text_id,
                'label': label_id,
                'color': color
            })
    
    def create_graphs_tab(self):
        """Create historical graphs tab"""
        self.graphs_frame = ttk.Frame(self.notebook, style="Modern.TFrame")
        self.notebook.add(self.graphs_frame, text="📊 History")
        
        # Graph canvas
        self.graph_canvas = tk.Canvas(self.graphs_frame, bg=self.colors['bg'], 
                                    height=150, highlightthickness=0)
        self.graph_canvas.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Legend
        legend_frame = ttk.Frame(self.graphs_frame, style="Modern.TFrame")
        legend_frame.pack(fill="x", padx=10, pady=5)
        
        metrics = [("CPU", self.colors['cpu']), ("RAM", self.colors['ram']), 
                  ("Disk", self.colors['disk']), ("Network", self.colors['network'])]
        
        for label, color in metrics:
            legend_item = ttk.Frame(legend_frame, style="Modern.TFrame")
            legend_item.pack(side="left", padx=10)
            
            # Color indicator
            color_box = tk.Frame(legend_item, bg=color, width=12, height=12)
            color_box.pack(side="left", padx=(0, 5))
            
            ttk.Label(legend_item, text=label, style="CardText.TLabel").pack(side="left")
    
    def create_details_tab(self):
        """Create detailed system information tab"""
        self.details_frame = ttk.Frame(self.notebook, style="Modern.TFrame")
        self.notebook.add(self.details_frame, text="🔍 Details")
        
        # Scrollable text widget
        text_frame = ttk.Frame(self.details_frame, style="Modern.TFrame")
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.details_text = tk.Text(text_frame, bg=self.colors['bg'], 
                                  fg=self.colors['text'], font=("Consolas", 9),
                                  wrap="word", height=8)
        
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", 
                                command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=scrollbar.set)
        
        self.details_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def start_monitoring(self):
        """Start system monitoring"""
        if not PSUTIL_AVAILABLE:
            return
        
        self.is_running = True
        self.toggle_btn.configure(text="●", style="Success.TButton")
        
        # Start monitoring thread
        threading.Thread(target=self.monitor_loop, daemon=True).start()
        
        # Start UI update loop
        self.update_ui()
    
    def stop_monitoring(self):
        """Stop system monitoring"""
        self.is_running = False
        self.toggle_btn.configure(text="○", style="Modern.TButton")
    
    def toggle_monitoring(self):
        """Toggle monitoring on/off"""
        if self.is_running:
            self.stop_monitoring()
        else:
            self.start_monitoring()
    
    def monitor_loop(self):
        """Main monitoring loop"""
        while self.is_running:
            try:
                if PSUTIL_AVAILABLE:
                    # Get system metrics
                    cpu_percent = psutil.cpu_percent(interval=1)
                    memory = psutil.virtual_memory()
                    disk = psutil.disk_usage('/')
                    
                    # Network (simplified)
                    network_io = psutil.net_io_counters()
                    network_percent = min(100, (network_io.bytes_sent + network_io.bytes_recv) / 1024 / 1024 % 100)
                    
                    # Store data
                    self.cpu_data.append(cpu_percent)
                    self.ram_data.append(memory.percent)
                    self.disk_data.append(disk.percent)
                    self.network_data.append(network_percent)
                
                time.sleep(1)
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(5)
    
    def update_ui(self):
        """Update UI with latest data"""
        if not self.is_running:
            return
        
        try:
            if self.cpu_data and PSUTIL_AVAILABLE:
                # Update circular indicators
                self.update_circular_indicators()
                
                # Update graphs
                self.update_graphs()
                
                # Update details
                self.update_details()
                
                # Update system info
                self.update_system_info()
        
        except Exception as e:
            print(f"UI update error: {e}")
        
        # Schedule next update
        if self.is_running:
            self.parent.after(self.update_interval, self.update_ui)
    
    def update_circular_indicators(self):
        """Update circular progress indicators"""
        if not self.circles or not self.cpu_data:
            return
        
        try:
            # Get latest values
            values = [
                self.cpu_data[-1] if self.cpu_data else 0,
                self.ram_data[-1] if self.ram_data else 0,
                self.disk_data[-1] if self.disk_data else 0,
                self.network_data[-1] if self.network_data else 0
            ]
            
            # Update each circle
            for i, (circle, value) in enumerate(zip(self.circles, values)):
                # Calculate arc extent (0-360 degrees)
                extent = -int((value / 100) * 360)
                
                # Update arc
                self.canvas.itemconfig(circle['arc'], extent=extent)
                
                # Update text
                self.canvas.itemconfig(circle['text'], text=f"{value:.0f}%")
        
        except Exception as e:
            print(f"Circular indicator update error: {e}")
    
    def update_graphs(self):
        """Update historical graphs"""
        try:
            self.graph_canvas.delete("all")
            
            canvas_width = self.graph_canvas.winfo_width() or 260
            canvas_height = self.graph_canvas.winfo_height() or 150
            
            if canvas_width < 10:
                return
            
            # Draw grid
            self.draw_grid(canvas_width, canvas_height)
            
            # Draw data lines
            datasets = [
                (self.cpu_data, self.colors['cpu']),
                (self.ram_data, self.colors['ram']),
                (self.disk_data, self.colors['disk']),
                (self.network_data, self.colors['network'])
            ]
            
            for data, color in datasets:
                if len(data) > 1:
                    self.draw_line_graph(data, color, canvas_width, canvas_height)
        
        except Exception as e:
            print(f"Graph update error: {e}")
    
    def draw_grid(self, width, height):
        """Draw graph grid"""
        # Horizontal lines (percentage markers)
        for i in range(0, 101, 25):
            y = height - (i / 100 * height)
            self.graph_canvas.create_line(0, y, width, y, 
                                        fill=self.colors['grid'], width=1)
            
            # Labels
            self.graph_canvas.create_text(5, y - 5, text=f"{i}%", 
                                        fill=self.colors['text'], 
                                        font=("Segoe UI", 7), anchor="w")
        
        # Vertical lines (time markers)
        for i in range(0, 61, 15):
            x = (i / 60) * width
            self.graph_canvas.create_line(x, 0, x, height, 
                                        fill=self.colors['grid'], width=1)
    
    def draw_line_graph(self, data, color, width, height):
        """Draw line graph for data"""
        if len(data) < 2:
            return
        
        points = []
        data_list = list(data)
        
        for i, value in enumerate(data_list):
            x = (i / (len(data_list) - 1)) * width
            y = height - (value / 100 * height)
            points.extend([x, y])
        
        if len(points) >= 4:
            self.graph_canvas.create_line(points, fill=color, width=2, smooth=True)
    
    def update_details(self):
        """Update detailed system information"""
        if not PSUTIL_AVAILABLE:
            return
        
        try:
            # Get detailed system info
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            boot_time = psutil.boot_time()
            
            # Format uptime
            uptime_seconds = time.time() - boot_time
            uptime_hours = int(uptime_seconds // 3600)
            uptime_minutes = int((uptime_seconds % 3600) // 60)
            
            details = f"""SYSTEM INFORMATION
            
CPU:
  Cores: {cpu_count}
  Current Usage: {self.cpu_data[-1] if self.cpu_data else 0:.1f}%
  Frequency: {cpu_freq.current:.0f} MHz (max: {cpu_freq.max:.0f} MHz)

MEMORY:
  Total: {memory.total / 1024**3:.1f} GB
  Used: {memory.used / 1024**3:.1f} GB ({memory.percent:.1f}%)
  Available: {memory.available / 1024**3:.1f} GB
  
DISK:
  Total: {disk.total / 1024**3:.1f} GB
  Used: {disk.used / 1024**3:.1f} GB ({disk.percent:.1f}%)
  Free: {disk.free / 1024**3:.1f} GB

SYSTEM:
  Uptime: {uptime_hours}h {uptime_minutes}m
  Processes: {len(psutil.pids())}
  
PERFORMANCE SUMMARY:
  CPU Avg (1min): {sum(list(self.cpu_data)[-10:]) / min(10, len(self.cpu_data)):.1f}%
  RAM Avg (1min): {sum(list(self.ram_data)[-10:]) / min(10, len(self.ram_data)):.1f}%
            """
            
            self.details_text.delete("1.0", tk.END)
            self.details_text.insert("1.0", details)
        
        except Exception as e:
            print(f"Details update error: {e}")
    
    def update_system_info(self):
        """Update system info labels"""
        try:
            if PSUTIL_AVAILABLE:
                # CPU temperature (if available)
                try:
                    temps = psutil.sensors_temperatures()
                    if temps:
                        cpu_temp = list(temps.values())[0][0].current
                        self.cpu_temp_label.config(text=f"CPU Temp: {cpu_temp:.1f}°C")
                    else:
                        self.cpu_temp_label.config(text="CPU Temp: N/A")
                except:
                    self.cpu_temp_label.config(text="CPU Temp: N/A")
                
                # Uptime
                boot_time = psutil.boot_time()
                uptime_seconds = time.time() - boot_time
                uptime_hours = int(uptime_seconds // 3600)
                uptime_minutes = int((uptime_seconds % 3600) // 60)
                self.uptime_label.config(text=f"Uptime: {uptime_hours}h {uptime_minutes}m")
                
                # Process count
                self.processes_label.config(text=f"Processes: {len(psutil.pids())}")
        
        except Exception as e:
            print(f"System info update error: {e}")
    
    def show_no_data_message(self):
        """Show message when psutil is not available"""
        no_data_frame = ttk.Frame(self.container, style="Card.TFrame")
        no_data_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ttk.Label(no_data_frame, 
                 text="📊 System monitoring requires 'psutil' package", 
                 style="CardText.TLabel").pack(pady=20)
        
        ttk.Label(no_data_frame, 
                 text="Install with: pip install psutil", 
                 style="CardText.TLabel").pack(pady=5)

def create_system_monitor(parent, **kwargs):
    """Create and return system monitor widget"""
    return SystemMonitorWidget(parent, **kwargs)
