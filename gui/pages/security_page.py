"""
Modern Security Page for DonTe Cleaner v3.0
"""

import tkinter as tk
import threading
import time
from gui.modern_ui import HolographicCard, AnimatedButton, NeonProgressBar, StatusIndicator

class SecurityPage:
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.colors = main_window.colors
        self.is_scanning = False
        
        # Create security interface
        self.create_security_interface()
    
    def create_security_interface(self):
        """Create security interface"""
        main_frame = tk.Frame(self.parent, bg=self.colors['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Security status
        self.create_security_status(main_frame)
        
        # Protection features
        self.create_protection_features(main_frame)
        
        # Scan controls
        self.create_scan_controls(main_frame)
    
    def create_header(self, parent):
        """Create header section"""
        header_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Title
        title_label = tk.Label(header_frame, text="🛡️ Security Center",
                              bg=self.colors['bg_primary'], fg=self.colors['success'],
                              font=('Segoe UI', 24, 'bold'))
        title_label.pack(side='left')
        
        # Quick scan button
        self.scan_btn = AnimatedButton(header_frame, text="🔍 Quick Scan",
                                      width=150, height=40,
                                      bg_color=self.colors['success'],
                                      hover_color='#4caf50',
                                      text_color='white',
                                      command=self.start_quick_scan)
        self.scan_btn.pack(side='right')
    
    def create_security_status(self, parent):
        """Create security status section"""
        status_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        status_frame.pack(fill='x', pady=(0, 20))
        
        # Overall status card
        status_card = HolographicCard(status_frame, width=250, height=200,
                                     title="📊 Security Status")
        status_card.pack(side='left', padx=(0, 20))
        
        # Security indicator
        self.security_indicator = StatusIndicator(status_card, status='active', size=60)
        self.security_indicator.place(x=95, y=80)
        
        self.status_text = tk.Label(status_card, text="PROTECTED",
                                   bg=self.colors['bg_tertiary'], fg=self.colors['success'],
                                   font=('Segoe UI', 16, 'bold'))
        self.status_text.place(x=85, y=150)
        
        # Threat statistics card  
        threats_card = HolographicCard(status_frame, width=250, height=200,
                                      title="🦠 Threats Blocked")
        threats_card.pack(side='left', padx=(0, 20))
        
        self.threats_today = tk.Label(threats_card, text="Today: 0",
                                     bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                     font=('Segoe UI', 14))
        self.threats_today.place(x=80, y=70)
        
        self.threats_week = tk.Label(threats_card, text="This Week: 0",
                                    bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                    font=('Segoe UI', 14))
        self.threats_week.place(x=60, y=100)
        
        self.threats_total = tk.Label(threats_card, text="Total: 0",
                                     bg=self.colors['bg_tertiary'], fg=self.colors['accent_primary'],
                                     font=('Segoe UI', 14, 'bold'))
        self.threats_total.place(x=80, y=130)
        
        # Last scan card
        scan_card = HolographicCard(status_frame, width=250, height=200,
                                   title="🔍 Last Scan")
        scan_card.pack(side='left')
        
        self.last_scan_date = tk.Label(scan_card, text="Never",
                                      bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                      font=('Segoe UI', 12))
        self.last_scan_date.place(x=90, y=70)
        
        self.scan_result = tk.Label(scan_card, text="No threats found",
                                   bg=self.colors['bg_tertiary'], fg=self.colors['success'],
                                   font=('Segoe UI', 11))
        self.scan_result.place(x=60, y=100)
        
        self.files_scanned = tk.Label(scan_card, text="Files: 0",
                                     bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'],
                                     font=('Segoe UI', 10))
        self.files_scanned.place(x=80, y=130)
    
    def create_protection_features(self, parent):
        """Create protection features section"""
        protection_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        protection_frame.pack(fill='x', pady=(0, 20))
        
        # Real-time protection card
        realtime_card = HolographicCard(protection_frame, width=380, height=250,
                                       title="🛡️ Real-time Protection")
        realtime_card.pack(side='left', padx=(0, 20))
        
        # Protection toggles
        self.realtime_protection = tk.BooleanVar(value=True)
        realtime_check = tk.Checkbutton(realtime_card, text="🔄 Real-time Scanning",
                                       variable=self.realtime_protection,
                                       bg=self.colors['bg_tertiary'],
                                       fg=self.colors['text_primary'],
                                       selectcolor=self.colors['bg_secondary'],
                                       font=('Segoe UI', 11))
        realtime_check.place(x=20, y=60)
        
        self.file_protection = tk.BooleanVar(value=True)
        file_check = tk.Checkbutton(realtime_card, text="📁 File System Protection",
                                   variable=self.file_protection,
                                   bg=self.colors['bg_tertiary'],
                                   fg=self.colors['text_primary'],
                                   selectcolor=self.colors['bg_secondary'],
                                   font=('Segoe UI', 11))
        file_check.place(x=20, y=90)
        
        self.web_protection = tk.BooleanVar(value=True)
        web_check = tk.Checkbutton(realtime_card, text="🌐 Web Protection",
                                  variable=self.web_protection,
                                  bg=self.colors['bg_tertiary'],
                                  fg=self.colors['text_primary'],
                                  selectcolor=self.colors['bg_secondary'],
                                  font=('Segoe UI', 11))
        web_check.place(x=20, y=120)
        
        self.email_protection = tk.BooleanVar(value=False)
        email_check = tk.Checkbutton(realtime_card, text="📧 Email Protection",
                                    variable=self.email_protection,
                                    bg=self.colors['bg_tertiary'],
                                    fg=self.colors['text_primary'],
                                    selectcolor=self.colors['bg_secondary'],
                                    font=('Segoe UI', 11))
        email_check.place(x=20, y=150)
        
        # Update button
        update_btn = AnimatedButton(realtime_card, text="🔄 Update Definitions",
                                   width=200, height=30,
                                   bg_color=self.colors['accent_primary'],
                                   hover_color='#00ff80',
                                   text_color='black',
                                   command=self.update_definitions)
        update_btn.place(x=20, y=190)
        
        # Firewall settings card
        firewall_card = HolographicCard(protection_frame, width=380, height=250,
                                       title="🔥 Firewall Settings")
        firewall_card.pack(side='left')
        
        # Firewall status
        self.firewall_status = StatusIndicator(firewall_card, status='active', size=40)
        self.firewall_status.place(x=50, y=80)
        
        self.firewall_text = tk.Label(firewall_card, text="Firewall: Active",
                                     bg=self.colors['bg_tertiary'], fg=self.colors['success'],
                                     font=('Segoe UI', 14, 'bold'))
        self.firewall_text.place(x=110, y=90)
        
        # Firewall controls
        self.block_incoming = tk.BooleanVar(value=True)
        incoming_check = tk.Checkbutton(firewall_card, text="🚫 Block Incoming",
                                       variable=self.block_incoming,
                                       bg=self.colors['bg_tertiary'],
                                       fg=self.colors['text_primary'],
                                       selectcolor=self.colors['bg_secondary'],
                                       font=('Segoe UI', 11))
        incoming_check.place(x=50, y=130)
        
        self.monitor_outgoing = tk.BooleanVar(value=False)
        outgoing_check = tk.Checkbutton(firewall_card, text="👁️ Monitor Outgoing",
                                       variable=self.monitor_outgoing,
                                       bg=self.colors['bg_tertiary'],
                                       fg=self.colors['text_primary'],
                                       selectcolor=self.colors['bg_secondary'],
                                       font=('Segoe UI', 11))
        outgoing_check.place(x=50, y=160)
        
        # Firewall config button
        config_btn = AnimatedButton(firewall_card, text="⚙️ Configure Rules",
                                   width=200, height=30,
                                   bg_color=self.colors['accent_secondary'],
                                   hover_color='#ff4081',
                                   text_color='white',
                                   command=self.configure_firewall)
        config_btn.place(x=50, y=190)
    
    def create_scan_controls(self, parent):
        """Create scan controls section"""
        scan_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        scan_frame.pack(fill='x')
        
        # Scan options card
        scan_card = HolographicCard(scan_frame, width=800, height=200,
                                   title="🔍 Scan Options")
        scan_card.pack()
        
        # Scan type buttons
        btn_frame = tk.Frame(scan_card, bg=self.colors['bg_tertiary'])
        btn_frame.place(x=50, y=60)
        
        quick_scan_btn = AnimatedButton(btn_frame, text="⚡ Quick Scan",
                                       width=150, height=35,
                                       bg_color=self.colors['accent_primary'],
                                       hover_color='#00ff80',
                                       text_color='black',
                                       command=self.start_quick_scan)
        quick_scan_btn.pack(side='left', padx=(0, 10))
        
        full_scan_btn = AnimatedButton(btn_frame, text="🔍 Full Scan",
                                      width=150, height=35,
                                      bg_color=self.colors['accent_secondary'],
                                      hover_color='#ff4081',
                                      text_color='white',
                                      command=self.start_full_scan)
        full_scan_btn.pack(side='left', padx=(0, 10))
        
        custom_scan_btn = AnimatedButton(btn_frame, text="⚙️ Custom Scan",
                                        width=150, height=35,
                                        bg_color=self.colors['accent_gold'],
                                        hover_color='#ffed4a',
                                        text_color='black',
                                        command=self.start_custom_scan)
        custom_scan_btn.pack(side='left')
        
        # Progress section
        self.progress_bar = NeonProgressBar(scan_card, width=600, height=25)
        self.progress_bar.place(x=100, y=120)
        
        self.scan_status = tk.Label(scan_card, text="Ready to scan",
                                   bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                   font=('Segoe UI', 12))
        self.scan_status.place(x=100, y=155)
    
    def start_quick_scan(self):
        """Start quick security scan"""
        if self.is_scanning:
            return
        
        self.is_scanning = True
        self.scan_btn.config(text="⏸️ Scanning...", state='disabled')
        
        threading.Thread(target=self.scan_worker, args=("quick",), daemon=True).start()
    
    def start_full_scan(self):
        """Start full system scan"""
        if self.is_scanning:
            return
        
        self.is_scanning = True
        threading.Thread(target=self.scan_worker, args=("full",), daemon=True).start()
    
    def start_custom_scan(self):
        """Start custom scan"""
        # Would open custom scan dialog
        if self.is_scanning:
            return
        
        self.is_scanning = True
        threading.Thread(target=self.scan_worker, args=("custom",), daemon=True).start()
    
    def scan_worker(self, scan_type):
        """Security scan worker thread"""
        try:
            scan_steps = {
                "quick": ["Scanning memory", "Checking startup items", "Scanning downloads"],
                "full": ["Scanning all files", "Checking registry", "Analyzing processes", 
                        "Scanning network connections", "Validating system files"],
                "custom": ["Custom scan", "Targeted analysis", "Deep inspection"]
            }
            
            steps = scan_steps.get(scan_type, scan_steps["quick"])
            
            for i, step in enumerate(steps):
                progress = int(((i + 1) / len(steps)) * 100)
                self.parent.after(0, lambda p=progress, s=step: self.update_scan_progress(p, s))
                time.sleep(2)  # Simulate scan time
            
            # Simulate scan completion
            self.parent.after(0, lambda: self.scan_complete(0))  # 0 threats found
            
        except Exception as e:
            self.parent.after(0, lambda: self.scan_error(str(e)))
    
    def update_scan_progress(self, progress, status):
        """Update scan progress"""
        self.progress_bar.set_progress(progress)
        self.scan_status.config(text=status)
    
    def scan_complete(self, threats_found):
        """Handle scan completion"""
        self.is_scanning = False
        self.scan_btn.config(text="🔍 Quick Scan", state='normal')
        self.progress_bar.set_progress(100)
        
        if threats_found == 0:
            self.scan_status.config(text="Scan complete - No threats found", 
                                   fg=self.colors['success'])
            self.scan_result.config(text="No threats found")
        else:
            self.scan_status.config(text=f"Scan complete - {threats_found} threats found",
                                   fg=self.colors['danger'])
            self.scan_result.config(text=f"{threats_found} threats found")
        
        # Update last scan info
        import datetime
        self.last_scan_date.config(text=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        
        # Reset progress after delay
        self.parent.after(3000, lambda: self.progress_bar.set_progress(0))
        self.parent.after(3000, lambda: self.scan_status.config(text="Ready to scan",
                                                               fg=self.colors['text_primary']))
    
    def scan_error(self, error):
        """Handle scan error"""
        self.is_scanning = False
        self.scan_btn.config(text="🔍 Quick Scan", state='normal')
        self.scan_status.config(text=f"Scan failed: {error}", fg=self.colors['danger'])
    
    def update_definitions(self):
        """Update security definitions"""
        self.scan_status.config(text="Updating definitions...")
        
        def update_worker():
            time.sleep(2)  # Simulate update
            self.parent.after(0, lambda: self.scan_status.config(
                text="Definitions updated successfully", fg=self.colors['success']))
            self.parent.after(3000, lambda: self.scan_status.config(
                text="Ready to scan", fg=self.colors['text_primary']))
        
        threading.Thread(target=update_worker, daemon=True).start()
    
    def configure_firewall(self):
        """Configure firewall rules"""
        self.scan_status.config(text="Opening firewall configuration...")
        # Would open firewall config dialog
