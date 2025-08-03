"""
Mobile App Connection for DonTe Cleaner
Mobile app connectivity with QR code pairing, remote monitoring, and mobile notifications
"""

import json
import socket
import threading
import qrcode
import base64
import hashlib
import time
import uuid
import os
from io import BytesIO
from tkinter import messagebox
import requests
import psutil

class MobileAppConnection:
    def __init__(self, main_window):
        self.main_window = main_window
        self.settings_file = "config/mobile_settings.json"
        
        # Connection settings
        self.connection_settings = {
            'enabled': False,
            'port': 8765,
            'password': '',
            'auto_connect': False,
            'notifications_enabled': True,
            'remote_monitoring': True,
            'secure_connection': True
        }
        
        # Server state
        self.server = None
        self.server_thread = None
        self.connected_devices = {}
        self.is_running = False
        
        # API endpoints
        self.api_endpoints = {
            'status': '/api/status',
            'system_info': '/api/system',
            'cleanup': '/api/cleanup',
            'optimize': '/api/optimize',
            'notifications': '/api/notifications',
            'settings': '/api/settings'
        }
        
        # Mobile features
        self.mobile_features = {
            'remote_cleanup': {
                'enabled': True,
                'name': 'Remote Cleanup',
                'description': 'Start system cleanup from mobile device'
            },
            'system_monitoring': {
                'enabled': True,
                'name': 'System Monitoring',
                'description': 'Real-time system stats on mobile'
            },
            'notifications': {
                'enabled': True,
                'name': 'Push Notifications',
                'description': 'Receive alerts on mobile device'
            },
            'remote_optimize': {
                'enabled': True,
                'name': 'Remote Optimization',
                'description': 'Optimize system from mobile'
            },
            'file_manager': {
                'enabled': False,
                'name': 'File Manager',
                'description': 'Basic file operations via mobile'
            },
            'screenshot': {
                'enabled': False,
                'name': 'Remote Screenshots',
                'description': 'View desktop screenshots'
            }
        }
        
        # Load settings
        self.load_settings()
        
        # Generate device ID
        self.device_id = self.get_device_id()
        
        # Connection security
        self.auth_tokens = {}
        self.session_timeout = 3600  # 1 hour
    
    def load_settings(self):
        """Load mobile settings"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.connection_settings.update(settings.get('connection', {}))
                    
                    # Load mobile features
                    for feature_id, feature_data in settings.get('features', {}).items():
                        if feature_id in self.mobile_features:
                            self.mobile_features[feature_id].update(feature_data)
        except Exception as e:
            print(f"Mobile settings load error: {e}")
    
    def save_settings(self):
        """Save mobile settings"""
        try:
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            settings = {
                'connection': self.connection_settings,
                'features': self.mobile_features
            }
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Mobile settings save error: {e}")
    
    def get_device_id(self):
        """Get unique device ID"""
        try:
            # Use MAC address for device ID
            import uuid
            mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                           for elements in range(0, 2*6, 2)][::-1])
            device_id = hashlib.md5(mac.encode()).hexdigest()[:16]
            return device_id
        except:
            return "unknown_device"
    
    def show_mobile_connection(self):
        """Show mobile connection window"""
        import tkinter as tk
        from tkinter import ttk
        
        self.mobile_window = tk.Toplevel(self.main_window.root)
        self.mobile_window.title("📱 Mobile App Connection")
        self.mobile_window.geometry("1000x700")
        self.mobile_window.configure(bg=self.main_window.colors['bg_dark'])
        self.mobile_window.transient(self.main_window.root)
        self.mobile_window.grab_set()
        
        # Create mobile interface
        self.create_mobile_interface()
        
        # Center window
        self.center_mobile_window()
    
    def center_mobile_window(self):
        """Center mobile window"""
        self.mobile_window.update_idletasks()
        width = self.mobile_window.winfo_width()
        height = self.mobile_window.winfo_height()
        x = (self.mobile_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.mobile_window.winfo_screenheight() // 2) - (height // 2)
        self.mobile_window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_mobile_interface(self):
        """Create mobile connection interface"""
        import tkinter as tk
        from tkinter import ttk
        
        main_frame = ttk.Frame(self.mobile_window, style="Modern.TFrame", padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Header
        self.create_mobile_header(main_frame)
        
        # Content notebook
        self.mobile_notebook = ttk.Notebook(main_frame, style="Modern.TNotebook")
        self.mobile_notebook.pack(fill="both", expand=True, pady=(10, 0))
        
        # Create tabs
        self.create_connection_tab()
        self.create_devices_tab()
        self.create_features_tab()
        self.create_logs_tab()
    
    def create_mobile_header(self, parent):
        """Create mobile header"""
        import tkinter as tk
        from tkinter import ttk
        
        header_frame = ttk.Frame(parent, style="Modern.TFrame")
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Title and status
        left_frame = ttk.Frame(header_frame, style="Modern.TFrame")
        left_frame.pack(side="left", fill="x", expand=True)
        
        ttk.Label(left_frame, text="📱 Mobile App Connection", 
                 font=("Segoe UI", 18, "bold"),
                 background=self.main_window.colors['bg_dark'],
                 foreground=self.main_window.colors['text_white']).pack(anchor="w")
        
        # Connection status
        self.connection_status_label = ttk.Label(left_frame, text="🔴 Disconnected",
                                                font=("Segoe UI", 12),
                                                background=self.main_window.colors['bg_dark'],
                                                foreground=self.main_window.colors['danger'])
        self.connection_status_label.pack(anchor="w")
        
        # Controls
        controls_frame = ttk.Frame(header_frame, style="Modern.TFrame")
        controls_frame.pack(side="right")
        
        # Start/Stop server button
        self.server_btn = ttk.Button(controls_frame, text="🚀 Start Server",
                                    style="Success.TButton",
                                    command=self.toggle_server)
        self.server_btn.pack(side="right", padx=(10, 0))
        
        # Generate QR button
        self.qr_btn = ttk.Button(controls_frame, text="📋 Show QR Code",
                                style="Info.TButton",
                                command=self.show_qr_code,
                                state='disabled')
        self.qr_btn.pack(side="right", padx=(10, 0))
        
        # Settings button
        ttk.Button(controls_frame, text="⚙️ Settings",
                  style="Modern.TButton",
                  command=self.show_mobile_settings).pack(side="right", padx=(10, 0))
    
    def create_connection_tab(self):
        """Create connection tab"""
        import tkinter as tk
        from tkinter import ttk
        
        connection_frame = ttk.Frame(self.mobile_notebook, style="Modern.TFrame", padding="20")
        self.mobile_notebook.add(connection_frame, text="🔗 Connection")
        
        # Connection info
        info_frame = ttk.LabelFrame(connection_frame, text="📡 Connection Information", padding="15")
        info_frame.pack(fill="x", pady=(0, 20))
        
        # Server status
        status_frame = ttk.Frame(info_frame, style="Modern.TFrame")
        status_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(status_frame, text="Server Status:",
                 background=self.main_window.colors['bg_light'],
                 foreground=self.main_window.colors['text_white']).pack(side="left")
        
        self.server_status_label = ttk.Label(status_frame, text="Stopped",
                                            background=self.main_window.colors['bg_light'],
                                            foreground=self.main_window.colors['danger'])
        self.server_status_label.pack(side="right")
        
        # IP address
        ip_frame = ttk.Frame(info_frame, style="Modern.TFrame")
        ip_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(ip_frame, text="IP Address:",
                 background=self.main_window.colors['bg_light'],
                 foreground=self.main_window.colors['text_white']).pack(side="left")
        
        self.ip_label = ttk.Label(ip_frame, text=self.get_local_ip(),
                                 background=self.main_window.colors['bg_light'],
                                 foreground=self.main_window.colors['accent'])
        self.ip_label.pack(side="right")
        
        # Port
        port_frame = ttk.Frame(info_frame, style="Modern.TFrame")
        port_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(port_frame, text="Port:",
                 background=self.main_window.colors['bg_light'],
                 foreground=self.main_window.colors['text_white']).pack(side="left")
        
        self.port_label = ttk.Label(port_frame, text=str(self.connection_settings['port']),
                                   background=self.main_window.colors['bg_light'],
                                   foreground=self.main_window.colors['accent'])
        self.port_label.pack(side="right")
        
        # Device ID
        device_frame = ttk.Frame(info_frame, style="Modern.TFrame")
        device_frame.pack(fill="x")
        
        ttk.Label(device_frame, text="Device ID:",
                 background=self.main_window.colors['bg_light'],
                 foreground=self.main_window.colors['text_white']).pack(side="left")
        
        ttk.Label(device_frame, text=self.device_id,
                 background=self.main_window.colors['bg_light'],
                 foreground=self.main_window.colors['text_gray']).pack(side="right")
        
        # QR Code frame
        qr_frame = ttk.LabelFrame(connection_frame, text="📋 QR Code for Mobile App", padding="15")
        qr_frame.pack(fill="both", expand=True)
        
        # QR Code display
        self.qr_label = ttk.Label(qr_frame, text="Start server to generate QR code",
                                 background=self.main_window.colors['bg_light'],
                                 foreground=self.main_window.colors['text_gray'],
                                 anchor="center")
        self.qr_label.pack(expand=True, fill="both")
        
        # Connection instructions
        instructions_frame = ttk.Frame(connection_frame, style="Modern.TFrame")
        instructions_frame.pack(fill="x", pady=(20, 0))
        
        instructions_text = """
📱 How to connect your mobile device:

1. Start the server by clicking 'Start Server'
2. Download the DonTe Cleaner mobile app
3. Scan the QR code with the mobile app
4. Enter the connection password if prompted
5. Start monitoring and controlling your PC remotely!

📋 Connection URL will be displayed after starting the server.
        """
        
        ttk.Label(instructions_frame, text=instructions_text,
                 background=self.main_window.colors['bg_light'],
                 foreground=self.main_window.colors['text_white'],
                 justify="left").pack(anchor="w")
    
    def create_devices_tab(self):
        """Create connected devices tab"""
        import tkinter as tk
        from tkinter import ttk
        
        devices_frame = ttk.Frame(self.mobile_notebook, style="Modern.TFrame", padding="20")
        self.mobile_notebook.add(devices_frame, text="📱 Connected Devices")
        
        # Devices list
        devices_list_frame = ttk.LabelFrame(devices_frame, text="📱 Connected Mobile Devices", padding="15")
        devices_list_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Devices treeview
        columns = ("Device Name", "IP Address", "Connected Since", "Last Activity", "Status")
        self.devices_tree = ttk.Treeview(devices_list_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.devices_tree.heading(col, text=col)
            self.devices_tree.column(col, width=150)
        
        # Scrollbar
        devices_scrollbar = ttk.Scrollbar(devices_list_frame, orient="vertical", command=self.devices_tree.yview)
        self.devices_tree.configure(yscrollcommand=devices_scrollbar.set)
        
        self.devices_tree.pack(side="left", fill="both", expand=True)
        devices_scrollbar.pack(side="right", fill="y")
        
        # Device controls
        controls_frame = ttk.Frame(devices_frame, style="Modern.TFrame")
        controls_frame.pack(fill="x")
        
        ttk.Button(controls_frame, text="🔄 Refresh",
                  style="Modern.TButton",
                  command=self.refresh_devices).pack(side="left")
        
        ttk.Button(controls_frame, text="❌ Disconnect Selected",
                  style="Warning.TButton",
                  command=self.disconnect_selected_device).pack(side="left", padx=(10, 0))
        
        ttk.Button(controls_frame, text="📤 Send Notification",
                  style="Info.TButton",
                  command=self.send_test_notification).pack(side="left", padx=(10, 0))
        
        # Connection statistics
        stats_frame = ttk.LabelFrame(devices_frame, text="📊 Connection Statistics", padding="15")
        stats_frame.pack(fill="x", pady=(20, 0))
        
        stats_grid = ttk.Frame(stats_frame, style="Modern.TFrame")
        stats_grid.pack(fill="x")
        
        # Stats labels
        self.create_stat_item(stats_grid, "Total Connections:", "0", "total_connections", row=0, col=0)
        self.create_stat_item(stats_grid, "Active Devices:", "0", "active_devices", row=0, col=1)
        self.create_stat_item(stats_grid, "Data Transferred:", "0 MB", "data_transferred", row=1, col=0)
        self.create_stat_item(stats_grid, "Uptime:", "00:00:00", "server_uptime", row=1, col=1)
        
        # Configure grid
        for i in range(2):
            stats_grid.grid_rowconfigure(i, weight=1)
            stats_grid.grid_columnconfigure(i, weight=1)
    
    def create_features_tab(self):
        """Create mobile features tab"""
        import tkinter as tk
        from tkinter import ttk
        
        features_frame = ttk.Frame(self.mobile_notebook, style="Modern.TFrame", padding="20")
        self.mobile_notebook.add(features_frame, text="⚡ Features")
        
        # Features list
        features_list_frame = ttk.LabelFrame(features_frame, text="📱 Mobile App Features", padding="15")
        features_list_frame.pack(fill="both", expand=True)
        
        # Feature checkboxes
        self.feature_vars = {}
        
        for feature_id, feature_data in self.mobile_features.items():
            var = tk.BooleanVar(value=feature_data['enabled'])
            self.feature_vars[feature_id] = var
            
            # Feature frame
            feature_item_frame = ttk.Frame(features_list_frame, style="Card.TFrame", padding="15")
            feature_item_frame.pack(fill="x", pady=5)
            
            # Checkbox and name
            checkbox_frame = ttk.Frame(feature_item_frame, style="Card.TFrame")
            checkbox_frame.pack(fill="x")
            
            checkbox = ttk.Checkbutton(checkbox_frame, text=feature_data['name'],
                                      variable=var,
                                      command=self.update_feature_settings)
            checkbox.pack(side="left")
            
            # Feature status
            status_text = "🟢 Enabled" if feature_data['enabled'] else "🔴 Disabled"
            status_label = ttk.Label(checkbox_frame, text=status_text,
                                    background=self.main_window.colors['bg_light'],
                                    foreground=self.main_window.colors['success'] if feature_data['enabled'] else self.main_window.colors['danger'])
            status_label.pack(side="right")
            
            # Description
            ttk.Label(feature_item_frame, text=feature_data['description'],
                     font=("Segoe UI", 9),
                     background=self.main_window.colors['bg_light'],
                     foreground=self.main_window.colors['text_gray'],
                     wraplength=600).pack(anchor="w", padx=(20, 0), pady=(5, 0))
    
    def create_logs_tab(self):
        """Create connection logs tab"""
        import tkinter as tk
        from tkinter import ttk
        
        logs_frame = ttk.Frame(self.mobile_notebook, style="Modern.TFrame", padding="20")
        self.mobile_notebook.add(logs_frame, text="📄 Logs")
        
        # Logs display
        logs_display_frame = ttk.LabelFrame(logs_frame, text="📄 Connection Logs", padding="15")
        logs_display_frame.pack(fill="both", expand=True)
        
        # Logs text widget
        self.logs_text = tk.Text(logs_display_frame, height=20, wrap=tk.WORD,
                                bg=self.main_window.colors['bg_light'],
                                fg=self.main_window.colors['text_white'],
                                font=("Consolas", 9))
        logs_scrollbar = ttk.Scrollbar(logs_display_frame, orient="vertical", command=self.logs_text.yview)
        self.logs_text.configure(yscrollcommand=logs_scrollbar.set)
        
        self.logs_text.pack(side="left", fill="both", expand=True)
        logs_scrollbar.pack(side="right", fill="y")
        
        # Logs controls
        logs_controls_frame = ttk.Frame(logs_frame, style="Modern.TFrame")
        logs_controls_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Button(logs_controls_frame, text="🔄 Refresh",
                  style="Modern.TButton",
                  command=self.refresh_logs).pack(side="left")
        
        ttk.Button(logs_controls_frame, text="🗑️ Clear Logs",
                  style="Warning.TButton",
                  command=self.clear_logs).pack(side="left", padx=(10, 0))
        
        ttk.Button(logs_controls_frame, text="💾 Export Logs",
                  style="Info.TButton",
                  command=self.export_logs).pack(side="left", padx=(10, 0))
        
        # Add initial log entry
        self.add_log("Mobile App Connection initialized")
    
    def create_stat_item(self, parent, label, value, stat_type, row, col):
        """Create statistics item"""
        import tkinter as tk
        from tkinter import ttk
        
        stat_frame = ttk.Frame(parent, style="Card.TFrame", padding="10")
        stat_frame.grid(row=row, column=col, padx=10, pady=5, sticky="nsew")
        
        ttk.Label(stat_frame, text=label,
                 background=self.main_window.colors['bg_light'],
                 foreground=self.main_window.colors['text_gray']).pack()
        
        value_label = ttk.Label(stat_frame, text=value,
                               font=("Segoe UI", 14, "bold"),
                               background=self.main_window.colors['bg_light'],
                               foreground=self.main_window.colors['accent'])
        value_label.pack()
        
        # Store reference
        setattr(self, f"{stat_type}_label", value_label)
    
    def get_local_ip(self):
        """Get local IP address"""
        try:
            # Connect to a remote server to get local IP
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except:
            return "127.0.0.1"
    
    def toggle_server(self):
        """Toggle mobile server on/off"""
        if self.is_running:
            self.stop_server()
        else:
            self.start_server()
    
    def start_server(self):
        """Start mobile server"""
        try:
            if self.is_running:
                return
            
            self.is_running = True
            self.server_thread = threading.Thread(target=self.server_worker, daemon=True)
            self.server_thread.start()
            
            # Update UI
            self.server_btn.config(text="🛑 Stop Server", style="Warning.TButton")
            self.qr_btn.config(state='normal')
            self.connection_status_label.config(text="🟢 Server Running", 
                                              foreground=self.main_window.colors['success'])
            self.server_status_label.config(text="Running", 
                                           foreground=self.main_window.colors['success'])
            
            # Generate and display QR code
            self.generate_qr_code()
            
            self.add_log(f"Mobile server started on {self.get_local_ip()}:{self.connection_settings['port']}")
            
            if hasattr(self.main_window, 'add_activity'):
                self.main_window.add_activity("Mobile server started", "Başarılı")
            
        except Exception as e:
            self.add_log(f"Failed to start server: {e}")
            messagebox.showerror("Server Error", f"Failed to start mobile server:\n{e}")
    
    def stop_server(self):
        """Stop mobile server"""
        try:
            self.is_running = False
            
            # Close server socket
            if self.server:
                self.server.close()
                self.server = None
            
            # Update UI
            self.server_btn.config(text="🚀 Start Server", style="Success.TButton")
            self.qr_btn.config(state='disabled')
            self.connection_status_label.config(text="🔴 Disconnected", 
                                              foreground=self.main_window.colors['danger'])
            self.server_status_label.config(text="Stopped", 
                                           foreground=self.main_window.colors['danger'])
            
            # Clear QR code
            self.qr_label.config(text="Start server to generate QR code", image="")
            
            # Disconnect all devices
            self.connected_devices.clear()
            self.refresh_devices()
            
            self.add_log("Mobile server stopped")
            
            if hasattr(self.main_window, 'add_activity'):
                self.main_window.add_activity("Mobile server stopped", "Bilgi")
            
        except Exception as e:
            self.add_log(f"Error stopping server: {e}")
    
    def server_worker(self):
        """Mobile server worker thread"""
        try:
            import http.server
            import socketserver
            from urllib.parse import urlparse, parse_qs
            
            class MobileRequestHandler(http.server.BaseHTTPRequestHandler):
                def __init__(self, mobile_connection, *args, **kwargs):
                    self.mobile_connection = mobile_connection
                    super().__init__(*args, **kwargs)
                
                def do_GET(self):
                    self.handle_request()
                
                def do_POST(self):
                    self.handle_request()
                
                def handle_request(self):
                    try:
                        # Parse URL
                        parsed_path = urlparse(self.path)
                        
                        # Handle API endpoints
                        if parsed_path.path == '/api/status':
                            self.handle_status()
                        elif parsed_path.path == '/api/system':
                            self.handle_system_info()
                        elif parsed_path.path == '/api/cleanup':
                            self.handle_cleanup()
                        elif parsed_path.path == '/api/optimize':
                            self.handle_optimize()
                        elif parsed_path.path == '/api/notifications':
                            self.handle_notifications()
                        elif parsed_path.path == '/':
                            self.handle_root()
                        else:
                            self.send_error(404)
                    
                    except Exception as e:
                        self.mobile_connection.add_log(f"Request error: {e}")
                        self.send_error(500)
                
                def handle_status(self):
                    """Handle status request"""
                    response = {
                        'status': 'online',
                        'device_id': self.mobile_connection.device_id,
                        'version': '2.0',
                        'features': [k for k, v in self.mobile_connection.mobile_features.items() if v['enabled']]
                    }
                    self.send_json_response(response)
                
                def handle_system_info(self):
                    """Handle system info request"""
                    try:
                        cpu_percent = psutil.cpu_percent()
                        memory = psutil.virtual_memory()
                        disk = psutil.disk_usage('/')
                        
                        response = {
                            'cpu': {
                                'percent': cpu_percent,
                                'cores': psutil.cpu_count()
                            },
                            'memory': {
                                'total': memory.total,
                                'used': memory.used,
                                'percent': memory.percent
                            },
                            'disk': {
                                'total': disk.total,
                                'used': disk.used,
                                'percent': (disk.used / disk.total) * 100
                            },
                            'timestamp': time.time()
                        }
                        self.send_json_response(response)
                    except Exception as e:
                        self.send_error_response(f"Failed to get system info: {e}")
                
                def handle_cleanup(self):
                    """Handle cleanup request"""
                    if not self.mobile_connection.mobile_features['remote_cleanup']['enabled']:
                        self.send_error_response("Remote cleanup is disabled")
                        return
                    
                    try:
                        # Simulate cleanup (integrate with actual cleanup functions)
                        response = {
                            'status': 'started',
                            'message': 'Cleanup started successfully',
                            'job_id': str(uuid.uuid4())
                        }
                        
                        self.mobile_connection.add_log("Remote cleanup initiated from mobile device")
                        self.send_json_response(response)
                        
                        # Trigger actual cleanup (if available)
                        if hasattr(self.mobile_connection.main_window, 'start_cleanup'):
                            threading.Thread(target=self.mobile_connection.main_window.start_cleanup, daemon=True).start()
                    
                    except Exception as e:
                        self.send_error_response(f"Cleanup failed: {e}")
                
                def handle_optimize(self):
                    """Handle optimize request"""
                    if not self.mobile_connection.mobile_features['remote_optimize']['enabled']:
                        self.send_error_response("Remote optimization is disabled")
                        return
                    
                    try:
                        response = {
                            'status': 'started',
                            'message': 'Optimization started successfully',
                            'job_id': str(uuid.uuid4())
                        }
                        
                        self.mobile_connection.add_log("Remote optimization initiated from mobile device")
                        self.send_json_response(response)
                        
                        # Trigger actual optimization (if available)
                        if hasattr(self.mobile_connection.main_window, 'start_optimization'):
                            threading.Thread(target=self.mobile_connection.main_window.start_optimization, daemon=True).start()
                    
                    except Exception as e:
                        self.send_error_response(f"Optimization failed: {e}")
                
                def handle_notifications(self):
                    """Handle notifications request"""
                    response = {
                        'notifications': [],
                        'count': 0
                    }
                    self.send_json_response(response)
                
                def handle_root(self):
                    """Handle root request - return mobile app info"""
                    html = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>DonTe Cleaner Mobile</title>
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                        <style>
                            body {{ font-family: Arial, sans-serif; margin: 20px; background: #1a1a1a; color: white; }}
                            .container {{ max-width: 400px; margin: 0 auto; text-align: center; }}
                            .logo {{ font-size: 2em; margin-bottom: 20px; }}
                            .info {{ background: #2a2a2a; padding: 20px; border-radius: 10px; margin: 10px 0; }}
                            .status {{ color: #4CAF50; }}
                            button {{ background: #007acc; color: white; border: none; padding: 10px 20px; margin: 5px; border-radius: 5px; cursor: pointer; }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <div class="logo">🧹 DonTe Cleaner</div>
                            <div class="info">
                                <h3>Mobile Connection Active</h3>
                                <p class="status">✅ Connected to PC</p>
                                <p>Device ID: {self.mobile_connection.device_id}</p>
                                <p>Server Version: 2.0</p>
                            </div>
                            <div class="info">
                                <h3>Quick Actions</h3>
                                <button onclick="startCleanup()">🧹 Start Cleanup</button>
                                <button onclick="optimizeSystem()">⚡ Optimize</button>
                                <button onclick="getSystemInfo()">📊 System Info</button>
                            </div>
                            <div class="info" id="systemInfo" style="display: none;">
                                <h3>System Information</h3>
                                <div id="systemData"></div>
                            </div>
                        </div>
                        
                        <script>
                            function startCleanup() {{
                                fetch('/api/cleanup', {{method: 'POST'}})
                                    .then(response => response.json())
                                    .then(data => alert('Cleanup started: ' + data.message))
                                    .catch(error => alert('Error: ' + error));
                            }}
                            
                            function optimizeSystem() {{
                                fetch('/api/optimize', {{method: 'POST'}})
                                    .then(response => response.json())
                                    .then(data => alert('Optimization started: ' + data.message))
                                    .catch(error => alert('Error: ' + error));
                            }}
                            
                            function getSystemInfo() {{
                                fetch('/api/system')
                                    .then(response => response.json())
                                    .then(data => {{
                                        document.getElementById('systemInfo').style.display = 'block';
                                        document.getElementById('systemData').innerHTML = 
                                            '<p>CPU: ' + data.cpu.percent + '%</p>' +
                                            '<p>Memory: ' + data.memory.percent + '%</p>' +
                                            '<p>Disk: ' + data.disk.percent.toFixed(1) + '%</p>';
                                    }})
                                    .catch(error => alert('Error: ' + error));
                            }}
                        </script>
                    </body>
                    </html>
                    """
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(html.encode())
                
                def send_json_response(self, data):
                    """Send JSON response"""
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(data).encode())
                
                def send_error_response(self, message):
                    """Send error response"""
                    response = {'error': message}
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode())
                
                def log_message(self, format, *args):
                    """Override log message to add to our logs"""
                    self.mobile_connection.add_log(f"{self.address_string()} - {format % args}")
            
            # Create server with custom handler
            handler = lambda *args, **kwargs: MobileRequestHandler(self, *args, **kwargs)
            
            with socketserver.TCPServer(("", self.connection_settings['port']), handler) as httpd:
                self.server = httpd
                self.add_log(f"Server listening on port {self.connection_settings['port']}")
                
                while self.is_running:
                    httpd.handle_request()
                    
        except Exception as e:
            self.add_log(f"Server error: {e}")
            self.mobile_window.after(0, lambda: self.stop_server())
    
    def generate_qr_code(self):
        """Generate QR code for mobile connection"""
        try:
            # Connection data
            connection_data = {
                'ip': self.get_local_ip(),
                'port': self.connection_settings['port'],
                'device_id': self.device_id,
                'name': 'DonTe Cleaner PC',
                'version': '2.0'
            }
            
            # Create QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(json.dumps(connection_data))
            qr.make(fit=True)
            
            # Generate QR code image
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to PhotoImage for Tkinter
            from PIL import ImageTk
            
            # Resize for display
            qr_image = qr_image.resize((200, 200))
            qr_photo = ImageTk.PhotoImage(qr_image)
            
            # Update QR label
            self.qr_label.config(image=qr_photo, text="")
            self.qr_label.image = qr_photo  # Keep a reference
            
        except Exception as e:
            self.add_log(f"QR code generation error: {e}")
            self.qr_label.config(text="QR code generation failed")
    
    def show_qr_code(self):
        """Show QR code in popup"""
        try:
            import tkinter as tk
            from tkinter import ttk
            
            qr_popup = tk.Toplevel(self.mobile_window)
            qr_popup.title("📋 QR Code for Mobile Connection")
            qr_popup.geometry("350x450")
            qr_popup.configure(bg=self.main_window.colors['bg_dark'])
            qr_popup.transient(self.mobile_window)
            qr_popup.grab_set()
            
            # Center popup
            qr_popup.update_idletasks()
            x = (qr_popup.winfo_screenwidth() // 2) - (350 // 2)
            y = (qr_popup.winfo_screenheight() // 2) - (450 // 2)
            qr_popup.geometry(f"350x450+{x}+{y}")
            
            # Title
            ttk.Label(qr_popup, text="📱 Scan with Mobile App",
                     font=("Segoe UI", 14, "bold"),
                     background=self.main_window.colors['bg_dark'],
                     foreground=self.main_window.colors['text_white']).pack(pady=20)
            
            # QR Code
            qr_frame = ttk.Frame(qr_popup, style="Card.TFrame", padding="20")
            qr_frame.pack(padx=20, pady=10)
            
            # Generate larger QR code for popup
            connection_data = {
                'ip': self.get_local_ip(),
                'port': self.connection_settings['port'],
                'device_id': self.device_id,
                'name': 'DonTe Cleaner PC',
                'version': '2.0'
            }
            
            qr = qrcode.QRCode(version=1, box_size=8, border=5)
            qr.add_data(json.dumps(connection_data))
            qr.make(fit=True)
            
            qr_image = qr.make_image(fill_color="black", back_color="white")
            qr_image = qr_image.resize((250, 250))
            
            from PIL import ImageTk
            qr_photo = ImageTk.PhotoImage(qr_image)
            
            qr_label = ttk.Label(qr_frame, image=qr_photo)
            qr_label.image = qr_photo
            qr_label.pack()
            
            # Connection info
            info_text = f"""
Connection URL:
http://{self.get_local_ip()}:{self.connection_settings['port']}

Device ID: {self.device_id}
            """
            
            ttk.Label(qr_popup, text=info_text,
                     background=self.main_window.colors['bg_dark'],
                     foreground=self.main_window.colors['text_gray'],
                     justify="center").pack(pady=10)
            
            # Close button
            ttk.Button(qr_popup, text="Close",
                      style="Modern.TButton",
                      command=qr_popup.destroy).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("QR Code Error", f"Failed to show QR code:\n{e}")
    
    def refresh_devices(self):
        """Refresh connected devices list"""
        # Clear existing items
        for item in self.devices_tree.get_children():
            self.devices_tree.delete(item)
        
        # Add connected devices
        for device_id, device_info in self.connected_devices.items():
            self.devices_tree.insert('', 'end', values=(
                device_info.get('name', 'Unknown Device'),
                device_info.get('ip', 'Unknown'),
                device_info.get('connected_since', 'Unknown'),
                device_info.get('last_activity', 'Unknown'),
                device_info.get('status', 'Connected')
            ))
        
        # Update statistics
        self.total_connections_label.config(text=str(len(self.connected_devices)))
        active_count = sum(1 for device in self.connected_devices.values() 
                          if device.get('status') == 'Connected')
        self.active_devices_label.config(text=str(active_count))
    
    def disconnect_selected_device(self):
        """Disconnect selected device"""
        selected = self.devices_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a device to disconnect.")
            return
        
        if messagebox.askyesno("Disconnect Device", "Disconnect selected device?"):
            # Remove from connected devices (simplified)
            self.refresh_devices()
            self.add_log("Device disconnected by user")
    
    def send_test_notification(self):
        """Send test notification to mobile devices"""
        if not self.connected_devices:
            messagebox.showwarning("No Devices", "No mobile devices are connected.")
            return
        
        # Simulate sending notification
        messagebox.showinfo("Notification Sent", "Test notification sent to all connected devices.")
        self.add_log("Test notification sent to mobile devices")
    
    def update_feature_settings(self):
        """Update mobile feature settings"""
        for feature_id, var in self.feature_vars.items():
            self.mobile_features[feature_id]['enabled'] = var.get()
        
        self.save_settings()
        self.add_log("Mobile features updated")
    
    def add_log(self, message):
        """Add log entry"""
        try:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] {message}\n"
            
            if hasattr(self, 'logs_text'):
                self.logs_text.insert('end', log_entry)
                self.logs_text.see('end')
        except:
            pass
    
    def refresh_logs(self):
        """Refresh logs display"""
        self.add_log("Logs refreshed")
    
    def clear_logs(self):
        """Clear all logs"""
        if hasattr(self, 'logs_text'):
            self.logs_text.delete(1.0, 'end')
            self.add_log("Logs cleared")
    
    def export_logs(self):
        """Export logs to file"""
        try:
            from tkinter import filedialog
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Export Mobile Connection Logs"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    if hasattr(self, 'logs_text'):
                        f.write(self.logs_text.get(1.0, 'end'))
                
                messagebox.showinfo("Export Complete", f"Logs exported to:\n{filename}")
                self.add_log(f"Logs exported to {filename}")
        
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export logs:\n{e}")
    
    def show_mobile_settings(self):
        """Show mobile settings window"""
        import tkinter as tk
        from tkinter import ttk
        
        settings_window = tk.Toplevel(self.mobile_window)
        settings_window.title("⚙️ Mobile Settings")
        settings_window.geometry("500x400")
        settings_window.configure(bg=self.main_window.colors['bg_dark'])
        settings_window.transient(self.mobile_window)
        settings_window.grab_set()
        
        # Center window
        settings_window.update_idletasks()
        x = (settings_window.winfo_screenwidth() // 2) - (250)
        y = (settings_window.winfo_screenheight() // 2) - (200)
        settings_window.geometry(f"500x400+{x}+{y}")
        
        # Settings content
        main_frame = ttk.Frame(settings_window, style="Modern.TFrame", padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Title
        ttk.Label(main_frame, text="⚙️ Mobile Connection Settings",
                 font=("Segoe UI", 16, "bold"),
                 background=self.main_window.colors['bg_dark'],
                 foreground=self.main_window.colors['text_white']).pack(pady=(0, 20))
        
        # Port setting
        port_frame = ttk.Frame(main_frame, style="Modern.TFrame")
        port_frame.pack(fill="x", pady=5)
        
        ttk.Label(port_frame, text="Server Port:",
                 background=self.main_window.colors['bg_dark'],
                 foreground=self.main_window.colors['text_white']).pack(side="left")
        
        port_var = tk.StringVar(value=str(self.connection_settings['port']))
        port_entry = ttk.Entry(port_frame, textvariable=port_var, width=10)
        port_entry.pack(side="right")
        
        # Auto-connect setting
        auto_var = tk.BooleanVar(value=self.connection_settings['auto_connect'])
        ttk.Checkbutton(main_frame, text="Auto-start server on app launch",
                       variable=auto_var).pack(anchor="w", pady=5)
        
        # Notifications setting
        notif_var = tk.BooleanVar(value=self.connection_settings['notifications_enabled'])
        ttk.Checkbutton(main_frame, text="Enable mobile notifications",
                       variable=notif_var).pack(anchor="w", pady=5)
        
        # Remote monitoring setting
        monitor_var = tk.BooleanVar(value=self.connection_settings['remote_monitoring'])
        ttk.Checkbutton(main_frame, text="Allow remote monitoring",
                       variable=monitor_var).pack(anchor="w", pady=5)
        
        # Secure connection setting
        secure_var = tk.BooleanVar(value=self.connection_settings['secure_connection'])
        ttk.Checkbutton(main_frame, text="Use secure connection (HTTPS)",
                       variable=secure_var).pack(anchor="w", pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame, style="Modern.TFrame")
        button_frame.pack(fill="x", pady=(20, 0))
        
        def save_settings():
            try:
                self.connection_settings['port'] = int(port_var.get())
                self.connection_settings['auto_connect'] = auto_var.get()
                self.connection_settings['notifications_enabled'] = notif_var.get()
                self.connection_settings['remote_monitoring'] = monitor_var.get()
                self.connection_settings['secure_connection'] = secure_var.get()
                
                self.save_settings()
                messagebox.showinfo("Settings Saved", "Mobile settings saved successfully!")
                settings_window.destroy()
                
                # Update port label
                self.port_label.config(text=str(self.connection_settings['port']))
                
            except ValueError:
                messagebox.showerror("Invalid Port", "Please enter a valid port number.")
        
        ttk.Button(button_frame, text="Save Settings",
                  style="Success.TButton",
                  command=save_settings).pack(side="right")
        
        ttk.Button(button_frame, text="Cancel",
                  style="Modern.TButton",
                  command=settings_window.destroy).pack(side="right", padx=(0, 10))
