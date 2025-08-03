"""
Network Optimizer for DonTe Cleaner
Advanced network optimization and monitoring tools
"""

import subprocess
import winreg
import psutil
import socket
import threading
import time
import json
import os
from tkinter import messagebox
import requests
import speedtest

class NetworkOptimizer:
    def __init__(self, main_window):
        self.main_window = main_window
        self.settings_file = "config/network_settings.json"
        self.monitoring_active = False
        
        # Network settings
        self.dns_servers = {
            'cloudflare': {'primary': '1.1.1.1', 'secondary': '1.0.0.1', 'name': 'Cloudflare DNS'},
            'google': {'primary': '8.8.8.8', 'secondary': '8.8.4.4', 'name': 'Google DNS'},
            'opendns': {'primary': '208.67.222.222', 'secondary': '208.67.220.220', 'name': 'OpenDNS'},
            'quad9': {'primary': '9.9.9.9', 'secondary': '149.112.112.112', 'name': 'Quad9 DNS'},
            'automatic': {'primary': 'auto', 'secondary': 'auto', 'name': 'Automatic (ISP)'}
        }
        
        # TCP optimization settings
        self.tcp_settings = {
            'tcp_window_scaling': 1,
            'tcp_timestamps': 1,
            'tcp_chimney_offload': 'enabled',
            'receive_side_scaling': 'enabled',
            'netdma': 'enabled',
            'tcp_global_autotuninglevel': 'normal'
        }
        
        # Network monitoring data
        self.network_stats = {
            'download_speed': 0,
            'upload_speed': 0,
            'ping': 0,
            'packet_loss': 0,
            'active_connections': 0,
            'bandwidth_usage': 0
        }
        
        # Load settings
        self.load_settings()
    
    def load_settings(self):
        """Load network settings"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.tcp_settings.update(settings.get('tcp_settings', {}))
        except Exception as e:
            print(f"Network settings load error: {e}")
    
    def save_settings(self):
        """Save network settings"""
        try:
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            settings = {
                'tcp_settings': self.tcp_settings
            }
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Network settings save error: {e}")
    
    def show_network_optimizer(self):
        """Show network optimizer window"""
        import tkinter as tk
        from tkinter import ttk
        
        self.network_window = tk.Toplevel(self.main_window.root)
        self.network_window.title("🌐 Network Optimizer")
        self.network_window.geometry("900x700")
        self.network_window.configure(bg=self.main_window.colors['bg_dark'])
        self.network_window.transient(self.main_window.root)
        self.network_window.grab_set()
        
        # Create network optimizer interface
        self.create_network_interface()
        
        # Start monitoring
        self.start_network_monitoring()
        
        # Handle window close
        self.network_window.protocol("WM_DELETE_WINDOW", self.on_network_window_close)
        
        # Center window
        self.center_network_window()
    
    def center_network_window(self):
        """Center network window"""
        self.network_window.update_idletasks()
        width = self.network_window.winfo_width()
        height = self.network_window.winfo_height()
        x = (self.network_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.network_window.winfo_screenheight() // 2) - (height // 2)
        self.network_window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_network_interface(self):
        """Create network optimizer interface"""
        import tkinter as tk
        from tkinter import ttk
        
        main_frame = ttk.Frame(self.network_window, style="Modern.TFrame", padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Header
        self.create_network_header(main_frame)
        
        # Notebook for different sections
        notebook = ttk.Notebook(main_frame, style="Modern.TNotebook")
        notebook.pack(fill="both", expand=True, pady=(10, 0))
        
        # Network status tab
        self.create_network_status_tab(notebook)
        
        # Speed test tab
        self.create_speed_test_tab(notebook)
        
        # DNS optimizer tab
        self.create_dns_optimizer_tab(notebook)
        
        # TCP optimization tab
        self.create_tcp_optimizer_tab(notebook)
        
        # Network tools tab
        self.create_network_tools_tab(notebook)
    
    def create_network_header(self, parent):
        """Create network header"""
        import tkinter as tk
        from tkinter import ttk
        
        header_frame = ttk.Frame(parent, style="Modern.TFrame")
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Title
        ttk.Label(header_frame, text="🌐 Network Optimizer", 
                 font=("Segoe UI", 18, "bold"),
                 background=self.main_window.colors['bg_dark'],
                 foreground=self.main_window.colors['text_white']).pack(side="left")
        
        # Controls
        controls_frame = ttk.Frame(header_frame, style="Modern.TFrame")
        controls_frame.pack(side="right")
        
        # Quick optimize button
        ttk.Button(controls_frame, text="⚡ Quick Optimize",
                  style="Success.TButton",
                  command=self.quick_network_optimize).pack(side="right", padx=(10, 0))
        
        # Refresh button
        ttk.Button(controls_frame, text="🔄 Refresh",
                  style="Modern.TButton",
                  command=self.refresh_network_info).pack(side="right", padx=(10, 0))
    
    def create_network_status_tab(self, parent):
        """Create network status tab"""
        import tkinter as tk
        from tkinter import ttk
        
        status_frame = ttk.Frame(parent, style="Modern.TFrame", padding="20")
        parent.add(status_frame, text="📊 Network Status")
        
        # Current status
        current_frame = ttk.LabelFrame(status_frame, text="🔗 Current Connection", padding="15")
        current_frame.pack(fill="x", pady=(0, 20))
        
        # Connection info
        self.connection_info_frame = ttk.Frame(current_frame, style="Card.TFrame")
        self.connection_info_frame.pack(fill="x")
        
        # Real-time stats
        stats_frame = ttk.LabelFrame(status_frame, text="📈 Real-time Statistics", padding="15")
        stats_frame.pack(fill="x", pady=(0, 20))
        
        # Create stats grid
        stats_grid = ttk.Frame(stats_frame, style="Card.TFrame")
        stats_grid.pack(fill="x")
        
        # Stats cards
        self.create_network_stat_card(stats_grid, "📥 Download", "0 Mbps", "download", row=0, col=0)
        self.create_network_stat_card(stats_grid, "📤 Upload", "0 Mbps", "upload", row=0, col=1)
        self.create_network_stat_card(stats_grid, "⚡ Ping", "0 ms", "ping", row=1, col=0)
        self.create_network_stat_card(stats_grid, "📡 Connections", "0", "connections", row=1, col=1)
        
        # Configure grid
        for i in range(2):
            stats_grid.grid_rowconfigure(i, weight=1)
            stats_grid.grid_columnconfigure(i, weight=1)
        
        # Active connections
        connections_frame = ttk.LabelFrame(status_frame, text="🔌 Active Connections", padding="15")
        connections_frame.pack(fill="both", expand=True)
        
        # Connections treeview
        self.create_connections_treeview(connections_frame)
        
        # Update network info
        self.update_network_status()
    
    def create_network_stat_card(self, parent, title, value, stat_type, row, col):
        """Create network stat card"""
        import tkinter as tk
        from tkinter import ttk
        
        card = ttk.Frame(parent, style="Card.TFrame", padding="15")
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        ttk.Label(card, text=title,
                 font=("Segoe UI", 10),
                 background=self.main_window.colors['bg_light'],
                 foreground=self.main_window.colors['text_gray']).pack()
        
        value_label = ttk.Label(card, text=value,
                               font=("Segoe UI", 16, "bold"),
                               background=self.main_window.colors['bg_light'],
                               foreground=self.main_window.colors['accent'])
        value_label.pack()
        
        # Store reference
        setattr(self, f"{stat_type}_stat_label", value_label)
    
    def create_connections_treeview(self, parent):
        """Create connections treeview"""
        import tkinter as tk
        from tkinter import ttk
        
        # Treeview for connections
        columns = ("Process", "Local Address", "Remote Address", "Status", "PID")
        self.connections_tree = ttk.Treeview(parent, columns=columns, show="headings", height=8)
        
        # Configure columns
        for col in columns:
            self.connections_tree.heading(col, text=col)
            self.connections_tree.column(col, width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.connections_tree.yview)
        self.connections_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack
        self.connections_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_speed_test_tab(self, parent):
        """Create speed test tab"""
        import tkinter as tk
        from tkinter import ttk
        
        speed_frame = ttk.Frame(parent, style="Modern.TFrame", padding="20")
        parent.add(speed_frame, text="🚀 Speed Test")
        
        # Speed test controls
        controls_frame = ttk.LabelFrame(speed_frame, text="⚡ Internet Speed Test", padding="15")
        controls_frame.pack(fill="x", pady=(0, 20))
        
        # Test button
        self.speed_test_btn = ttk.Button(controls_frame, text="🚀 Start Speed Test",
                                        style="Success.TButton",
                                        command=self.run_speed_test)
        self.speed_test_btn.pack(pady=10)
        
        # Progress bar
        self.speed_test_progress = ttk.Progressbar(controls_frame, mode='indeterminate')
        self.speed_test_progress.pack(fill="x", pady=5)
        
        # Status label
        self.speed_test_status = ttk.Label(controls_frame, text="Ready to test",
                                          background=self.main_window.colors['bg_light'],
                                          foreground=self.main_window.colors['text_white'])
        self.speed_test_status.pack(pady=5)
        
        # Results frame
        results_frame = ttk.LabelFrame(speed_frame, text="📊 Speed Test Results", padding="15")
        results_frame.pack(fill="x", pady=(0, 20))
        
        # Results grid
        results_grid = ttk.Frame(results_frame, style="Card.TFrame")
        results_grid.pack(fill="x")
        
        # Result cards
        self.create_result_card(results_grid, "📥 Download Speed", "--- Mbps", "download_result", row=0, col=0)
        self.create_result_card(results_grid, "📤 Upload Speed", "--- Mbps", "upload_result", row=0, col=1)
        self.create_result_card(results_grid, "⚡ Ping", "--- ms", "ping_result", row=1, col=0)
        self.create_result_card(results_grid, "🌍 Server", "---", "server_result", row=1, col=1)
        
        # Configure grid
        for i in range(2):
            results_grid.grid_rowconfigure(i, weight=1)
            results_grid.grid_columnconfigure(i, weight=1)
        
        # Speed history
        history_frame = ttk.LabelFrame(speed_frame, text="📈 Speed History", padding="15")
        history_frame.pack(fill="both", expand=True)
        
        # History treeview
        self.create_speed_history_treeview(history_frame)
    
    def create_result_card(self, parent, title, value, result_type, row, col):
        """Create speed test result card"""
        import tkinter as tk
        from tkinter import ttk
        
        card = ttk.Frame(parent, style="Card.TFrame", padding="15")
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        ttk.Label(card, text=title,
                 font=("Segoe UI", 10),
                 background=self.main_window.colors['bg_light'],
                 foreground=self.main_window.colors['text_gray']).pack()
        
        value_label = ttk.Label(card, text=value,
                               font=("Segoe UI", 14, "bold"),
                               background=self.main_window.colors['bg_light'],
                               foreground=self.main_window.colors['accent'])
        value_label.pack()
        
        # Store reference
        setattr(self, f"{result_type}_label", value_label)
    
    def create_speed_history_treeview(self, parent):
        """Create speed history treeview"""
        import tkinter as tk
        from tkinter import ttk
        
        columns = ("Date", "Time", "Download", "Upload", "Ping", "Server")
        self.speed_history_tree = ttk.Treeview(parent, columns=columns, show="headings", height=6)
        
        # Configure columns
        for col in columns:
            self.speed_history_tree.heading(col, text=col)
            self.speed_history_tree.column(col, width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.speed_history_tree.yview)
        self.speed_history_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack
        self.speed_history_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_dns_optimizer_tab(self, parent):
        """Create DNS optimizer tab"""
        import tkinter as tk
        from tkinter import ttk
        
        dns_frame = ttk.Frame(parent, style="Modern.TFrame", padding="20")
        parent.add(dns_frame, text="🔍 DNS Optimizer")
        
        # Current DNS
        current_dns_frame = ttk.LabelFrame(dns_frame, text="🔗 Current DNS Settings", padding="15")
        current_dns_frame.pack(fill="x", pady=(0, 20))
        
        self.current_dns_label = ttk.Label(current_dns_frame, text="Loading DNS info...",
                                          background=self.main_window.colors['bg_light'],
                                          foreground=self.main_window.colors['text_white'])
        self.current_dns_label.pack()
        
        # DNS options
        dns_options_frame = ttk.LabelFrame(dns_frame, text="🚀 DNS Providers", padding="15")
        dns_options_frame.pack(fill="x", pady=(0, 20))
        
        # DNS selection
        self.dns_var = tk.StringVar(value="automatic")
        
        for dns_id, dns_info in self.dns_servers.items():
            dns_frame_widget = ttk.Frame(dns_options_frame, style="Card.TFrame")
            dns_frame_widget.pack(fill="x", pady=5)
            
            ttk.Radiobutton(dns_frame_widget, text=dns_info['name'],
                           variable=self.dns_var, value=dns_id).pack(side="left")
            
            if dns_info['primary'] != 'auto':
                ttk.Label(dns_frame_widget, text=f"({dns_info['primary']}, {dns_info['secondary']})",
                         background=self.main_window.colors['bg_light'],
                         foreground=self.main_window.colors['text_gray']).pack(side="right")
        
        # DNS actions
        dns_actions_frame = ttk.Frame(dns_options_frame, style="Modern.TFrame")
        dns_actions_frame.pack(fill="x", pady=(15, 0))
        
        ttk.Button(dns_actions_frame, text="✅ Apply DNS Settings",
                  style="Success.TButton",
                  command=self.apply_dns_settings).pack(side="left")
        
        ttk.Button(dns_actions_frame, text="🧪 Test DNS Speed",
                  style="Modern.TButton",
                  command=self.test_dns_speed).pack(side="left", padx=(10, 0))
        
        # DNS cache
        dns_cache_frame = ttk.LabelFrame(dns_frame, text="🗂️ DNS Cache Management", padding="15")
        dns_cache_frame.pack(fill="x")
        
        cache_actions = [
            ("🔄 Flush DNS Cache", self.flush_dns_cache),
            ("📊 View DNS Cache", self.view_dns_cache),
            ("⚡ Optimize DNS Cache", self.optimize_dns_cache)
        ]
        
        for text, command in cache_actions:
            ttk.Button(dns_cache_frame, text=text,
                      style="Modern.TButton",
                      command=command).pack(side="left", padx=(0, 10))
    
    def create_tcp_optimizer_tab(self, parent):
        """Create TCP optimizer tab"""
        import tkinter as tk
        from tkinter import ttk
        
        tcp_frame = ttk.Frame(parent, style="Modern.TFrame", padding="20")
        parent.add(tcp_frame, text="⚙️ TCP Optimization")
        
        # TCP settings
        tcp_settings_frame = ttk.LabelFrame(tcp_frame, text="🔧 TCP/IP Settings", padding="15")
        tcp_settings_frame.pack(fill="x", pady=(0, 20))
        
        # TCP optimizations
        optimizations = [
            ("Enable TCP Window Scaling", "tcp_window_scaling"),
            ("Enable TCP Timestamps", "tcp_timestamps"),
            ("Enable Receive Side Scaling", "receive_side_scaling"),
            ("Enable NetDMA", "netdma")
        ]
        
        self.tcp_vars = {}
        for text, setting in optimizations:
            var = tk.BooleanVar(value=self.tcp_settings.get(setting, False))
            self.tcp_vars[setting] = var
            
            ttk.Checkbutton(tcp_settings_frame, text=text,
                           variable=var).pack(anchor="w", pady=3)
        
        # Auto-tuning level
        autotune_frame = ttk.Frame(tcp_settings_frame, style="Modern.TFrame")
        autotune_frame.pack(fill="x", pady=(15, 0))
        
        ttk.Label(autotune_frame, text="Auto-tuning Level:",
                 background=self.main_window.colors['bg_light'],
                 foreground=self.main_window.colors['text_white']).pack(side="left")
        
        self.autotune_var = tk.StringVar(value=self.tcp_settings.get('tcp_global_autotuninglevel', 'normal'))
        autotune_combo = ttk.Combobox(autotune_frame, textvariable=self.autotune_var,
                                     values=['disabled', 'highlyrestricted', 'restricted', 'normal', 'experimental'],
                                     state='readonly')
        autotune_combo.pack(side="right")
        
        # TCP actions
        tcp_actions_frame = ttk.Frame(tcp_settings_frame, style="Modern.TFrame")
        tcp_actions_frame.pack(fill="x", pady=(15, 0))
        
        ttk.Button(tcp_actions_frame, text="✅ Apply TCP Settings",
                  style="Success.TButton",
                  command=self.apply_tcp_settings).pack(side="left")
        
        ttk.Button(tcp_actions_frame, text="🔄 Reset to Defaults",
                  style="Warning.TButton",
                  command=self.reset_tcp_settings).pack(side="left", padx=(10, 0))
        
        # Network adapter settings
        adapter_frame = ttk.LabelFrame(tcp_frame, text="🖧 Network Adapter Optimization", padding="15")
        adapter_frame.pack(fill="x", pady=(0, 20))
        
        adapter_optimizations = [
            ("🚀 Optimize Adapter Settings", self.optimize_network_adapter),
            ("⚡ Disable Power Management", self.disable_adapter_power_management),
            ("📊 Show Adapter Properties", self.show_adapter_properties)
        ]
        
        for text, command in adapter_optimizations:
            ttk.Button(adapter_frame, text=text,
                      style="Modern.TButton",
                      command=command).pack(side="left", padx=(0, 10))
        
        # Firewall optimization
        firewall_frame = ttk.LabelFrame(tcp_frame, text="🔥 Firewall Optimization", padding="15")
        firewall_frame.pack(fill="x")
        
        firewall_actions = [
            ("🔧 Optimize Firewall Rules", self.optimize_firewall),
            ("📊 Check Firewall Status", self.check_firewall_status),
            ("⚡ Gaming Mode Firewall", self.gaming_firewall_mode)
        ]
        
        for text, command in firewall_actions:
            ttk.Button(firewall_frame, text=text,
                      style="Modern.TButton",
                      command=command).pack(side="left", padx=(0, 10))
    
    def create_network_tools_tab(self, parent):
        """Create network tools tab"""
        import tkinter as tk
        from tkinter import ttk
        
        tools_frame = ttk.Frame(parent, style="Modern.TFrame", padding="20")
        parent.add(tools_frame, text="🛠️ Network Tools")
        
        # Diagnostic tools
        diagnostic_frame = ttk.LabelFrame(tools_frame, text="🔍 Diagnostic Tools", padding="15")
        diagnostic_frame.pack(fill="x", pady=(0, 20))
        
        diagnostic_tools = [
            ("🏓 Ping Test", self.ping_test),
            ("🗺️ Traceroute", self.traceroute_test),
            ("🔌 Port Scanner", self.port_scanner),
            ("📡 Network Discovery", self.network_discovery)
        ]
        
        diagnostic_grid = ttk.Frame(diagnostic_frame, style="Modern.TFrame")
        diagnostic_grid.pack(fill="x")
        
        for i, (text, command) in enumerate(diagnostic_tools):
            row = i // 2
            col = i % 2
            ttk.Button(diagnostic_grid, text=text,
                      style="Modern.TButton",
                      command=command).grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        
        # Configure grid
        diagnostic_grid.grid_columnconfigure(0, weight=1)
        diagnostic_grid.grid_columnconfigure(1, weight=1)
        
        # Bandwidth tools
        bandwidth_frame = ttk.LabelFrame(tools_frame, text="📊 Bandwidth Tools", padding="15")
        bandwidth_frame.pack(fill="x", pady=(0, 20))
        
        bandwidth_tools = [
            ("📈 Bandwidth Monitor", self.bandwidth_monitor),
            ("🎯 QoS Configuration", self.qos_configuration),
            ("⚖️ Traffic Shaping", self.traffic_shaping),
            ("📊 Usage Statistics", self.usage_statistics)
        ]
        
        bandwidth_grid = ttk.Frame(bandwidth_frame, style="Modern.TFrame")
        bandwidth_grid.pack(fill="x")
        
        for i, (text, command) in enumerate(bandwidth_tools):
            row = i // 2
            col = i % 2
            ttk.Button(bandwidth_grid, text=text,
                      style="Modern.TButton",
                      command=command).grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        
        # Configure grid
        bandwidth_grid.grid_columnconfigure(0, weight=1)
        bandwidth_grid.grid_columnconfigure(1, weight=1)
        
        # Security tools
        security_frame = ttk.LabelFrame(tools_frame, text="🛡️ Security Tools", padding="15")
        security_frame.pack(fill="x")
        
        security_tools = [
            ("🔒 WiFi Security Scan", self.wifi_security_scan),
            ("🌐 Open Port Check", self.open_port_check),
            ("🔍 Network Vulnerability Scan", self.vulnerability_scan),
            ("🛡️ Intrusion Detection", self.intrusion_detection)
        ]
        
        security_grid = ttk.Frame(security_frame, style="Modern.TFrame")
        security_grid.pack(fill="x")
        
        for i, (text, command) in enumerate(security_tools):
            row = i // 2
            col = i % 2
            ttk.Button(security_grid, text=text,
                      style="Modern.TButton",
                      command=command).grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        
        # Configure grid
        security_grid.grid_columnconfigure(0, weight=1)
        security_grid.grid_columnconfigure(1, weight=1)
    
    def start_network_monitoring(self):
        """Start network monitoring"""
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self.monitoring_loop, daemon=True)
        self.monitoring_thread.start()
    
    def monitoring_loop(self):
        """Network monitoring loop"""
        while self.monitoring_active:
            try:
                # Update network statistics
                self.update_network_stats()
                
                # Update UI
                self.network_window.after(0, self.update_network_status)
                
                time.sleep(5)  # Update every 5 seconds
                
            except Exception as e:
                print(f"Network monitoring error: {e}")
                time.sleep(5)
    
    def update_network_stats(self):
        """Update network statistics"""
        try:
            # Get network I/O stats
            net_io = psutil.net_io_counters()
            
            # Get active connections
            connections = psutil.net_connections()
            self.network_stats['active_connections'] = len(connections)
            
            # Calculate bandwidth usage (simplified)
            self.network_stats['bandwidth_usage'] = (net_io.bytes_sent + net_io.bytes_recv) / (1024 * 1024)  # MB
            
        except Exception as e:
            print(f"Network stats update error: {e}")
    
    def update_network_status(self):
        """Update network status display"""
        try:
            # Update stat labels
            if hasattr(self, 'connections_stat_label'):
                self.connections_stat_label.config(text=str(self.network_stats['active_connections']))
            
            # Update connections treeview
            self.update_connections_display()
            
        except Exception as e:
            print(f"Network status update error: {e}")
    
    def update_connections_display(self):
        """Update connections display"""
        try:
            # Clear existing items
            for item in self.connections_tree.get_children():
                self.connections_tree.delete(item)
            
            # Get current connections
            connections = psutil.net_connections()
            
            for conn in connections[:50]:  # Limit to 50 connections
                try:
                    # Get process name
                    process_name = "Unknown"
                    if conn.pid:
                        try:
                            process = psutil.Process(conn.pid)
                            process_name = process.name()
                        except:
                            pass
                    
                    local_addr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
                    remote_addr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                    status = conn.status
                    pid = str(conn.pid) if conn.pid else "N/A"
                    
                    self.connections_tree.insert('', 'end', values=(
                        process_name, local_addr, remote_addr, status, pid
                    ))
                    
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"Connections display update error: {e}")
    
    def refresh_network_info(self):
        """Refresh network information"""
        try:
            self.update_network_stats()
            self.update_network_status()
            self.get_current_dns_info()
            
            if hasattr(self.main_window, 'add_activity'):
                self.main_window.add_activity("Network information refreshed", "Bilgi")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh network info:\n{str(e)}")
    
    def quick_network_optimize(self):
        """Quick network optimization"""
        try:
            optimizations = []
            
            # Flush DNS cache
            result = subprocess.run(['ipconfig', '/flushdns'], capture_output=True, text=True)
            if result.returncode == 0:
                optimizations.append("DNS cache flushed")
            
            # Reset network stack
            subprocess.run(['netsh', 'winsock', 'reset'], capture_output=True)
            optimizations.append("Winsock reset")
            
            # Reset TCP/IP stack
            subprocess.run(['netsh', 'int', 'ip', 'reset'], capture_output=True)
            optimizations.append("TCP/IP stack reset")
            
            # Optimize TCP settings
            self.apply_tcp_optimizations()
            optimizations.append("TCP settings optimized")
            
            message = "Quick network optimization completed:\n\n" + "\n".join(f"✅ {opt}" for opt in optimizations)
            message += "\n\n⚠️ Restart required for some changes to take effect."
            
            messagebox.showinfo("Optimization Complete", message)
            
            if hasattr(self.main_window, 'add_activity'):
                self.main_window.add_activity("Quick network optimization completed", "Başarılı")
            
        except Exception as e:
            messagebox.showerror("Error", f"Network optimization failed:\n{str(e)}")
    
    def run_speed_test(self):
        """Run internet speed test"""
        def speed_test_worker():
            try:
                self.speed_test_btn.config(state='disabled', text="🔄 Testing...")
                self.speed_test_progress.start()
                self.speed_test_status.config(text="Initializing speed test...")
                
                # Initialize speedtest
                st = speedtest.Speedtest()
                
                self.speed_test_status.config(text="Finding best server...")
                st.get_best_server()
                
                self.speed_test_status.config(text="Testing download speed...")
                download_speed = st.download() / 1_000_000  # Convert to Mbps
                
                self.speed_test_status.config(text="Testing upload speed...")
                upload_speed = st.upload() / 1_000_000  # Convert to Mbps
                
                self.speed_test_status.config(text="Testing ping...")
                ping = st.results.ping
                
                server_info = st.results.server
                server_name = f"{server_info['sponsor']} ({server_info['name']})"
                
                # Update UI
                self.network_window.after(0, lambda: self.update_speed_test_results(
                    download_speed, upload_speed, ping, server_name
                ))
                
            except Exception as e:
                self.network_window.after(0, lambda: self.speed_test_error(str(e)))
        
        threading.Thread(target=speed_test_worker, daemon=True).start()
    
    def update_speed_test_results(self, download, upload, ping, server):
        """Update speed test results"""
        try:
            self.download_result_label.config(text=f"{download:.1f} Mbps")
            self.upload_result_label.config(text=f"{upload:.1f} Mbps")
            self.ping_result_label.config(text=f"{ping:.0f} ms")
            self.server_result_label.config(text=server[:20] + "..." if len(server) > 20 else server)
            
            self.speed_test_progress.stop()
            self.speed_test_btn.config(state='normal', text="🚀 Start Speed Test")
            self.speed_test_status.config(text="Speed test completed!")
            
            # Add to history
            from datetime import datetime
            now = datetime.now()
            self.speed_history_tree.insert('', 0, values=(
                now.strftime("%Y-%m-%d"),
                now.strftime("%H:%M:%S"),
                f"{download:.1f} Mbps",
                f"{upload:.1f} Mbps",
                f"{ping:.0f} ms",
                server[:15] + "..." if len(server) > 15 else server
            ))
            
            if hasattr(self.main_window, 'add_activity'):
                self.main_window.add_activity(f"Speed test: {download:.1f}/{upload:.1f} Mbps", "Başarılı")
            
        except Exception as e:
            print(f"Speed test results update error: {e}")
    
    def speed_test_error(self, error_msg):
        """Handle speed test error"""
        self.speed_test_progress.stop()
        self.speed_test_btn.config(state='normal', text="🚀 Start Speed Test")
        self.speed_test_status.config(text=f"Speed test failed: {error_msg}")
        
        messagebox.showerror("Speed Test Error", f"Speed test failed:\n{error_msg}")
    
    def get_current_dns_info(self):
        """Get current DNS information"""
        try:
            # Get DNS servers from registry
            result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True)
            
            dns_servers = []
            lines = result.stdout.split('\n')
            
            for line in lines:
                if 'DNS Servers' in line:
                    dns_server = line.split(':')[-1].strip()
                    if dns_server:
                        dns_servers.append(dns_server)
            
            if dns_servers:
                dns_text = f"Current DNS: {', '.join(dns_servers)}"
            else:
                dns_text = "DNS: Automatic (DHCP)"
            
            self.current_dns_label.config(text=dns_text)
            
        except Exception as e:
            self.current_dns_label.config(text=f"DNS info error: {e}")
    
    def apply_dns_settings(self):
        """Apply selected DNS settings"""
        try:
            selected_dns = self.dns_var.get()
            
            if selected_dns == 'automatic':
                # Set to automatic (DHCP)
                subprocess.run(['netsh', 'interface', 'ip', 'set', 'dns', 'name="Local Area Connection"', 'source=dhcp'], 
                              capture_output=True)
                messagebox.showinfo("DNS Applied", "DNS set to automatic (DHCP)")
            else:
                dns_info = self.dns_servers[selected_dns]
                
                # Set primary DNS
                subprocess.run(['netsh', 'interface', 'ip', 'set', 'dns', 'name="Local Area Connection"', 
                               f'static', dns_info['primary']], capture_output=True)
                
                # Set secondary DNS
                subprocess.run(['netsh', 'interface', 'ip', 'add', 'dns', 'name="Local Area Connection"', 
                               dns_info['secondary'], 'index=2'], capture_output=True)
                
                messagebox.showinfo("DNS Applied", f"{dns_info['name']} DNS servers applied successfully!")
            
            # Flush DNS cache
            subprocess.run(['ipconfig', '/flushdns'], capture_output=True)
            
            # Update current DNS info
            self.get_current_dns_info()
            
            if hasattr(self.main_window, 'add_activity'):
                self.main_window.add_activity(f"DNS changed to {selected_dns}", "Başarılı")
            
        except Exception as e:
            messagebox.showerror("DNS Error", f"Failed to apply DNS settings:\n{str(e)}")
    
    def test_dns_speed(self):
        """Test DNS server speeds"""
        messagebox.showinfo("DNS Speed Test", "DNS speed testing feature will be implemented here.\n\nThis will test response times for different DNS servers.")
    
    def flush_dns_cache(self):
        """Flush DNS cache"""
        try:
            result = subprocess.run(['ipconfig', '/flushdns'], capture_output=True, text=True)
            if result.returncode == 0:
                messagebox.showinfo("DNS Cache", "DNS cache flushed successfully!")
                if hasattr(self.main_window, 'add_activity'):
                    self.main_window.add_activity("DNS cache flushed", "Başarılı")
            else:
                messagebox.showerror("Error", "Failed to flush DNS cache")
        except Exception as e:
            messagebox.showerror("Error", f"DNS cache flush failed:\n{str(e)}")
    
    def view_dns_cache(self):
        """View DNS cache"""
        import tkinter as tk
        from tkinter import ttk
        try:
            result = subprocess.run(['ipconfig', '/displaydns'], capture_output=True, text=True)
            
            # Create window to display DNS cache
            cache_window = tk.Toplevel(self.network_window)
            cache_window.title("DNS Cache")
            cache_window.geometry("600x400")
            
            text_widget = tk.Text(cache_window, wrap=tk.WORD)
            scrollbar = ttk.Scrollbar(cache_window, orient="vertical", command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            text_widget.insert("1.0", result.stdout)
            text_widget.config(state=tk.DISABLED)
            
            text_widget.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to view DNS cache:\n{str(e)}")
    
    def optimize_dns_cache(self):
        """Optimize DNS cache"""
        messagebox.showinfo("DNS Optimization", "DNS cache optimization feature will be implemented here.")
    
    def apply_tcp_settings(self):
        """Apply TCP optimization settings"""
        try:
            self.apply_tcp_optimizations()
            messagebox.showinfo("TCP Settings", "TCP optimization settings applied!\n\nRestart required for changes to take effect.")
            
            if hasattr(self.main_window, 'add_activity'):
                self.main_window.add_activity("TCP settings optimized", "Başarılı")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply TCP settings:\n{str(e)}")
    
    def apply_tcp_optimizations(self):
        """Apply TCP optimizations"""
        try:
            # Enable TCP window scaling
            subprocess.run(['netsh', 'int', 'tcp', 'set', 'global', 'autotuninglevel=normal'], capture_output=True)
            
            # Enable receive side scaling
            subprocess.run(['netsh', 'int', 'tcp', 'set', 'global', 'rss=enabled'], capture_output=True)
            
            # Enable chimney offload
            subprocess.run(['netsh', 'int', 'tcp', 'set', 'global', 'chimney=enabled'], capture_output=True)
            
            # Optimize network throttling
            subprocess.run(['netsh', 'int', 'tcp', 'set', 'global', 'netdma=enabled'], capture_output=True)
            
        except Exception as e:
            print(f"TCP optimization error: {e}")
    
    def reset_tcp_settings(self):
        """Reset TCP settings to defaults"""
        try:
            if messagebox.askyesno("Reset TCP Settings", "Reset all TCP settings to Windows defaults?"):
                subprocess.run(['netsh', 'int', 'tcp', 'reset'], capture_output=True)
                messagebox.showinfo("TCP Reset", "TCP settings reset to defaults!\n\nRestart required.")
                
                if hasattr(self.main_window, 'add_activity'):
                    self.main_window.add_activity("TCP settings reset", "Bilgi")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reset TCP settings:\n{str(e)}")
    
    def optimize_network_adapter(self):
        """Optimize network adapter settings"""
        messagebox.showinfo("Adapter Optimization", "Network adapter optimization feature will be implemented here.")
    
    def disable_adapter_power_management(self):
        """Disable adapter power management"""
        messagebox.showinfo("Power Management", "Adapter power management optimization will be implemented here.")
    
    def show_adapter_properties(self):
        """Show adapter properties"""
        messagebox.showinfo("Adapter Properties", "Adapter properties display will be implemented here.")
    
    def optimize_firewall(self):
        """Optimize firewall settings"""
        messagebox.showinfo("Firewall Optimization", "Firewall optimization feature will be implemented here.")
    
    def check_firewall_status(self):
        """Check firewall status"""
        import tkinter as tk
        from tkinter import ttk
        try:
            result = subprocess.run(['netsh', 'advfirewall', 'show', 'allprofiles'], capture_output=True, text=True)
            
            # Show firewall status
            status_window = tk.Toplevel(self.network_window)
            status_window.title("Firewall Status")
            status_window.geometry("500x300")
            
            text_widget = tk.Text(status_window, wrap=tk.WORD)
            scrollbar = ttk.Scrollbar(status_window, orient="vertical", command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            text_widget.insert("1.0", result.stdout)
            text_widget.config(state=tk.DISABLED)
            
            text_widget.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to check firewall status:\n{str(e)}")
    
    def gaming_firewall_mode(self):
        """Configure gaming mode firewall"""
        messagebox.showinfo("Gaming Firewall", "Gaming mode firewall configuration will be implemented here.")
    
    # Network tool methods (placeholders)
    def ping_test(self):
        """Ping test tool"""
        messagebox.showinfo("Ping Test", "Ping test tool will be implemented here.")
    
    def traceroute_test(self):
        """Traceroute test tool"""
        messagebox.showinfo("Traceroute", "Traceroute tool will be implemented here.")
    
    def port_scanner(self):
        """Port scanner tool"""
        messagebox.showinfo("Port Scanner", "Port scanner tool will be implemented here.")
    
    def network_discovery(self):
        """Network discovery tool"""
        messagebox.showinfo("Network Discovery", "Network discovery tool will be implemented here.")
    
    def bandwidth_monitor(self):
        """Bandwidth monitor tool"""
        messagebox.showinfo("Bandwidth Monitor", "Bandwidth monitor will be implemented here.")
    
    def qos_configuration(self):
        """QoS configuration tool"""
        messagebox.showinfo("QoS Configuration", "QoS configuration will be implemented here.")
    
    def traffic_shaping(self):
        """Traffic shaping tool"""
        messagebox.showinfo("Traffic Shaping", "Traffic shaping will be implemented here.")
    
    def usage_statistics(self):
        """Usage statistics tool"""
        messagebox.showinfo("Usage Statistics", "Usage statistics will be implemented here.")
    
    def wifi_security_scan(self):
        """WiFi security scan"""
        messagebox.showinfo("WiFi Security", "WiFi security scan will be implemented here.")
    
    def open_port_check(self):
        """Open port check"""
        messagebox.showinfo("Port Check", "Open port check will be implemented here.")
    
    def vulnerability_scan(self):
        """Network vulnerability scan"""
        messagebox.showinfo("Vulnerability Scan", "Network vulnerability scan will be implemented here.")
    
    def intrusion_detection(self):
        """Intrusion detection"""
        messagebox.showinfo("Intrusion Detection", "Intrusion detection will be implemented here.")
    
    def on_network_window_close(self):
        """Handle network window close"""
        self.monitoring_active = False
        self.network_window.destroy()
