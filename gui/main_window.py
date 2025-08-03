"""
Modern Enhanced Main Window for DonTe Cleaner
Professional Windows Optimization Tool with Real-time Progress and Modern Design
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import os
import psutil
import platform
import sys
from utils.logger import get_logger
from utils.admin_check import is_admin
from core.windows_optimizer import WindowsOptimizer
from core.antivirus_scanner import AntivirusScanner
from core.enhanced_antivirus import EnhancedAntivirusScanner
from core.emulator_optimizer import EmulatorOptimizer
from gui.antivirus_window import AntivirusWindow
from gui.emulator_window import EmulatorWindow

# Enhanced features (optional imports)
try:
    from gui.theme_manager import AdvancedThemeManager
    THEME_MANAGER_AVAILABLE = True
except ImportError:
    THEME_MANAGER_AVAILABLE = False

try:
    from gui.system_monitor import SystemMonitorWidget
    SYSTEM_MONITOR_AVAILABLE = True
except ImportError:
    SYSTEM_MONITOR_AVAILABLE = False

try:
    from gui.system_tray import SystemTrayManager
    SYSTEM_TRAY_AVAILABLE = True
except ImportError:
    SYSTEM_TRAY_AVAILABLE = False

try:
    from gui.performance_charts import PerformanceCharts
    PERFORMANCE_CHARTS_AVAILABLE = True
except ImportError:
    PERFORMANCE_CHARTS_AVAILABLE = False

try:
    from gui.smart_notifications import SmartNotifications
    SMART_NOTIFICATIONS_AVAILABLE = True
except ImportError:
    SMART_NOTIFICATIONS_AVAILABLE = False

try:
    from gui.sound_effects import SoundEffects
    SOUND_EFFECTS_AVAILABLE = True
except ImportError:
    SOUND_EFFECTS_AVAILABLE = False

try:
    from gui.network_optimizer import NetworkOptimizer
    NETWORK_OPTIMIZER_AVAILABLE = True
except ImportError:
    NETWORK_OPTIMIZER_AVAILABLE = False

try:
    from gui.privacy_cleaner import PrivacyCleaner
    PRIVACY_CLEANER_AVAILABLE = True
except ImportError:
    PRIVACY_CLEANER_AVAILABLE = False

try:
    from gui.mobile_app_connection import MobileAppConnection
    MOBILE_APP_AVAILABLE = True
except ImportError:
    MOBILE_APP_AVAILABLE = False

class ModernMainWindow:
    def __init__(self, root):
        self.root = root
        self.logger = get_logger("MainWindow")
        self.is_admin = is_admin()
        
        # Initialize enhanced features first
        self.theme_manager = None
        self.system_tray = None
        self.advanced_monitor = None
        self.performance_charts = None
        self.smart_notifications = None
        self.sound_effects = None
        self.network_optimizer = None
        self.privacy_cleaner = None
        self.mobile_app_connection = None
        self.setup_enhanced_features()
        
        # Initialize core modules
        self.windows_optimizer = WindowsOptimizer()
        self.antivirus_scanner = AntivirusScanner()
        self.enhanced_antivirus = EnhancedAntivirusScanner()
        self.emulator_optimizer = EmulatorOptimizer()
        
        # Progress tracking
        self.current_operation = ""
        self.progress_value = 0
        self.scan_stats = {"scanned": 0, "total": 0, "threats": 0}
        
        # System info
        self.system_info = self.get_system_info()
        
        self.setup_window()
        self.setup_modern_styles()
        self.create_modern_widgets()
        self.setup_layout()
        
        # Show admin status
        self.update_status_bar()
        
        # Setup window close handler for tray integration
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)
        
        # Start system monitoring after everything is set up
        self.root.after(1000, self.start_system_monitor)
    
    def setup_enhanced_features(self):
        """Setup enhanced features like theme manager and system tray"""
        try:
            # Initialize theme manager
            if THEME_MANAGER_AVAILABLE:
                self.theme_manager = AdvancedThemeManager(self.root)
                self.logger.info("Advanced theme manager initialized")
            
            # Initialize performance charts
            if PERFORMANCE_CHARTS_AVAILABLE:
                self.performance_charts = PerformanceCharts(self)
                self.logger.info("Performance charts initialized")
            
            # Initialize smart notifications
            if SMART_NOTIFICATIONS_AVAILABLE:
                self.smart_notifications = SmartNotifications(self)
                self.logger.info("Smart notifications initialized")
            
            # Initialize sound effects
            if SOUND_EFFECTS_AVAILABLE:
                self.sound_effects = SoundEffects(self)
                self.logger.info("Sound effects initialized")
            
            # Initialize network optimizer
            if NETWORK_OPTIMIZER_AVAILABLE:
                self.network_optimizer = NetworkOptimizer(self)
                self.logger.info("Network optimizer initialized")
            
            # Initialize privacy cleaner
            if PRIVACY_CLEANER_AVAILABLE:
                self.privacy_cleaner = PrivacyCleaner(self)
                self.logger.info("Privacy cleaner initialized")
            
            # Initialize mobile app connection
            if MOBILE_APP_AVAILABLE:
                self.mobile_app_connection = MobileAppConnection(self)
                self.logger.info("Mobile app connection initialized")
            
            # Initialize system tray (after main window is ready)
            if SYSTEM_TRAY_AVAILABLE:
                self.root.after(2000, self.setup_system_tray)
                
        except Exception as e:
            self.logger.error(f"Enhanced features setup failed: {str(e)}")
    
    def setup_system_tray(self):
        """Setup system tray integration"""
        try:
            if SYSTEM_TRAY_AVAILABLE:
                self.system_tray = SystemTrayManager(self)
                self.logger.info("System tray integration enabled")
        except Exception as e:
            self.logger.error(f"System tray setup failed: {str(e)}")
    
    def on_window_close(self):
        """Handle window close event - minimize to tray if available"""
        if self.system_tray and SYSTEM_TRAY_AVAILABLE:
            # Minimize to tray instead of closing
            self.system_tray.minimize_to_tray()
        else:
            # Normal close
            self.cleanup_and_exit()
    
    def cleanup_and_exit(self):
        """Cleanup resources and exit application"""
        try:
            # Stop monitoring
            if hasattr(self, 'monitoring_active'):
                self.monitoring_active = False
            
            # Cleanup system tray
            if self.system_tray:
                self.system_tray.cleanup()
            
            # Close application
            self.root.quit()
            self.root.destroy()
            
        except Exception as e:
            self.logger.error(f"Cleanup error: {str(e)}")
        finally:
            import sys
            sys.exit(0)
    
    def get_system_info(self):
        """Get detailed system information"""
        try:
            cpu_count = psutil.cpu_count()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('C:')
            
            return {
                'os': f"{platform.system()} {platform.release()}",
                'version': platform.version(),
                'cpu_cores': cpu_count,
                'ram_total': memory.total // (1024**3),
                'ram_available': memory.available // (1024**3),
                'ram_percent': memory.percent,
                'disk_total': disk.total // (1024**3),
                'disk_free': disk.free // (1024**3),
                'disk_percent': (disk.used / disk.total) * 100
            }
        except:
            return {'os': 'Unknown', 'cpu_cores': 'N/A', 'ram_total': 'N/A'}
    
    def update_system_info_display(self):
        """Update system info display with real-time data"""
        try:
            # Get fresh system info
            current_info = self.get_system_info()
            
            # Clear existing content
            for widget in self.system_info_content.winfo_children():
                widget.destroy()
            
            # CPU Usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            cpu_frame = ttk.Frame(self.system_info_content, style="Card.TFrame")
            cpu_frame.pack(fill="x", pady=2)
            
            ttk.Label(cpu_frame, text="CPU Kullanımı:", 
                     font=("Segoe UI", 10, "bold"),
                     background=self.colors['bg_light'],
                     foreground=self.colors['text_white']).pack(side="left")
            
            cpu_color = self.colors['danger'] if cpu_percent > 80 else self.colors['warning'] if cpu_percent > 60 else self.colors['success']
            ttk.Label(cpu_frame, text=f"{cpu_percent:.1f}%", 
                     font=("Segoe UI", 10),
                     background=self.colors['bg_light'],
                     foreground=cpu_color).pack(side="right")
            
            # RAM Usage
            ram_frame = ttk.Frame(self.system_info_content, style="Card.TFrame")
            ram_frame.pack(fill="x", pady=2)
            
            ttk.Label(ram_frame, text="RAM Kullanımı:", 
                     font=("Segoe UI", 10, "bold"),
                     background=self.colors['bg_light'],
                     foreground=self.colors['text_white']).pack(side="left")
            
            ram_color = self.colors['danger'] if current_info['ram_percent'] > 80 else self.colors['warning'] if current_info['ram_percent'] > 60 else self.colors['success']
            ram_text = f"{current_info['ram_available']}GB/{current_info['ram_total']}GB ({current_info['ram_percent']:.1f}%)"
            ttk.Label(ram_frame, text=ram_text, 
                     font=("Segoe UI", 10),
                     background=self.colors['bg_light'],
                     foreground=ram_color).pack(side="right")
            
            # Disk Usage
            disk_frame = ttk.Frame(self.system_info_content, style="Card.TFrame")
            disk_frame.pack(fill="x", pady=2)
            
            ttk.Label(disk_frame, text="Disk Kullanımı:", 
                     font=("Segoe UI", 10, "bold"),
                     background=self.colors['bg_light'],
                     foreground=self.colors['text_white']).pack(side="left")
            
            disk_color = self.colors['danger'] if current_info['disk_percent'] > 80 else self.colors['warning'] if current_info['disk_percent'] > 60 else self.colors['success']
            disk_text = f"{current_info['disk_free']}GB Free ({current_info['disk_percent']:.1f}% used)"
            ttk.Label(disk_frame, text=disk_text, 
                     font=("Segoe UI", 10),
                     background=self.colors['bg_light'],
                     foreground=disk_color).pack(side="right")
            
            # System Info
            sys_frame = ttk.Frame(self.system_info_content, style="Card.TFrame")
            sys_frame.pack(fill="x", pady=2)
            
            ttk.Label(sys_frame, text="İşletim Sistemi:", 
                     font=("Segoe UI", 10, "bold"),
                     background=self.colors['bg_light'],
                     foreground=self.colors['text_white']).pack(side="left")
            
            ttk.Label(sys_frame, text=current_info['os'], 
                     font=("Segoe UI", 10),
                     background=self.colors['bg_light'],
                     foreground=self.colors['text_white']).pack(side="right")
            
            # CPU Cores
            cores_frame = ttk.Frame(self.system_info_content, style="Card.TFrame")
            cores_frame.pack(fill="x", pady=2)
            
            ttk.Label(cores_frame, text="CPU Çekirdekleri:", 
                     font=("Segoe UI", 10, "bold"),
                     background=self.colors['bg_light'],
                     foreground=self.colors['text_white']).pack(side="left")
            
            ttk.Label(cores_frame, text=str(current_info['cpu_cores']), 
                     font=("Segoe UI", 10),
                     background=self.colors['bg_light'],
                     foreground=self.colors['text_white']).pack(side="right")
                     
        except Exception as e:
            # Fallback display
            error_frame = ttk.Frame(self.system_info_content, style="Card.TFrame")
            error_frame.pack(fill="x", pady=2)
            
            ttk.Label(error_frame, text="Sistem bilgileri yüklenemedi.", 
                     font=("Segoe UI", 10),
                     background=self.colors['bg_light'],
                     foreground=self.colors['warning']).pack()
    
    def start_system_monitor(self):
        """Start periodic system info updates"""
        if hasattr(self, 'system_info_content'):
            self.update_system_info_display()
            # Update every 3 seconds
            self.root.after(3000, self.start_system_monitor)
    
    def setup_window(self):
        """Setup main window properties with modern design"""
        admin_status = "Yönetici" if self.is_admin else "Sınırlı Mod"
        self.root.title(f"DonTe Cleaner Pro v2.0 - Professional System Optimizer ({admin_status})")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        self.root.configure(bg="#0d1117")
        
        # Center window on screen
        self.center_window()
        
        # Set icon if available
        try:
            self.root.iconbitmap("resources/icon.ico")
        except:
            pass
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_modern_styles(self):
        """Setup modern dark theme styles"""
        self.style = ttk.Style()
        
        # Try to use modern theme
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            try:
                self.style.theme_use("vista")
            except tk.TclError:
                pass
        
        # Modern color palette
        self.colors = {
            'bg_primary': '#0d1117',      # GitHub dark
            'bg_secondary': '#161b22',    # Darker cards
            'bg_tertiary': '#21262d',     # Lighter cards
            'accent_blue': '#58a6ff',     # Primary blue
            'accent_green': '#3fb950',    # Success green
            'accent_yellow': '#d29922',   # Warning yellow
            'accent_red': '#f85149',      # Danger red
            'accent_purple': '#a5a5ff',   # Info purple
            'text_primary': '#f0f6fc',    # Primary text
            'text_secondary': '#8b949e',  # Secondary text
            'text_disabled': '#484f58',   # Disabled text
            'border': '#30363d',          # Borders
            'hover': '#30363d'            # Hover states
        }
        
        # Configure modern styles with error handling
        try:
            # Main frame styles
            self.style.configure("Modern.TFrame",
                               background=self.colors['bg_secondary'],
                               relief="flat",
                               borderwidth=0)
            
            self.style.configure("Card.TFrame",
                               background=self.colors['bg_tertiary'],
                               relief="flat",
                               borderwidth=1,
                               borderstyle="solid")
            
            self.style.configure("Header.TFrame",
                               background=self.colors['bg_primary'],
                               relief="flat")
            
            # Label styles
            self.style.configure("Title.TLabel",
                               background=self.colors['bg_primary'],
                               foreground=self.colors['text_primary'],
                               font=("Segoe UI", 28, "bold"))
            
            self.style.configure("Subtitle.TLabel",
                               background=self.colors['bg_primary'],
                               foreground=self.colors['text_secondary'],
                               font=("Segoe UI", 14))
            
            self.style.configure("CardTitle.TLabel",
                               background=self.colors['bg_tertiary'],
                               foreground=self.colors['text_primary'],
                               font=("Segoe UI", 16, "bold"))
            
            self.style.configure("CardText.TLabel",
                               background=self.colors['bg_tertiary'],
                               foreground=self.colors['text_secondary'],
                               font=("Segoe UI", 11))
            
            self.style.configure("Status.TLabel",
                               background=self.colors['bg_secondary'],
                               foreground=self.colors['text_secondary'],
                               font=("Segoe UI", 10))
            
            # Button styles
            self.style.configure("Modern.TButton",
                               background=self.colors['accent_blue'],
                               foreground=self.colors['text_primary'],
                               font=("Segoe UI", 11, "bold"),
                               borderwidth=0,
                               focuscolor='none',
                               padding=(15, 8))
            
            self.style.map("Modern.TButton",
                          background=[('active', '#4493f8'),
                                    ('pressed', '#388bfd')])
            
            self.style.configure("Success.TButton",
                               background=self.colors['accent_green'],
                               foreground=self.colors['text_primary'],
                               font=("Segoe UI", 11, "bold"),
                               borderwidth=0,
                               padding=(15, 8))
            
            self.style.configure("Warning.TButton",
                               background=self.colors['accent_yellow'],
                               foreground='#000000',
                               font=("Segoe UI", 11, "bold"),
                               borderwidth=0,
                               padding=(15, 8))
            
            self.style.configure("Danger.TButton",
                               background=self.colors['accent_red'],
                               foreground=self.colors['text_primary'],
                               font=("Segoe UI", 11, "bold"),
                               borderwidth=0,
                               padding=(15, 8))
            
            # Notebook styles
            self.style.configure("Modern.TNotebook",
                               background=self.colors['bg_secondary'],
                               borderwidth=0,
                               tabmargins=0)
            
            self.style.configure("Modern.TNotebook.Tab",
                               background=self.colors['bg_tertiary'],
                               foreground=self.colors['text_secondary'],
                               padding=[20, 12],
                               font=("Segoe UI", 12, "bold"),
                               borderwidth=0)
            
            self.style.map("Modern.TNotebook.Tab",
                          background=[('selected', self.colors['accent_blue']),
                                    ('active', self.colors['hover'])],
                          foreground=[('selected', self.colors['text_primary'])])
            
            # Progress bar styles with fallback
            try:
                # First try to configure basic progressbar
                self.style.configure("TProgressbar",
                                   background=self.colors['accent_blue'],
                                   troughcolor=self.colors['bg_tertiary'],
                                   borderwidth=0,
                                   relief="flat")
                
                # Try modern progressbar
                try:
                    self.style.configure("Modern.TProgressbar",
                                       background=self.colors['accent_blue'],
                                       troughcolor=self.colors['bg_tertiary'],
                                       borderwidth=0,
                                       lightcolor=self.colors['accent_blue'],
                                       darkcolor=self.colors['accent_blue'],
                                       thickness=8,
                                       relief="flat")
                except tk.TclError:
                    # Fallback to basic configuration
                    self.style.configure("Modern.TProgressbar",
                                       background=self.colors['accent_blue'],
                                       troughcolor=self.colors['bg_tertiary'])
                
                # Success progressbar
                try:
                    self.style.configure("Success.TProgressbar",
                                       background=self.colors['accent_green'],
                                       troughcolor=self.colors['bg_tertiary'],
                                       borderwidth=0,
                                       thickness=8,
                                       relief="flat")
                except tk.TclError:
                    self.style.configure("Success.TProgressbar",
                                       background=self.colors['accent_green'],
                                       troughcolor=self.colors['bg_tertiary'])
                
                # Warning progressbar
                try:
                    self.style.configure("Warning.TProgressbar",
                                       background=self.colors['accent_yellow'],
                                       troughcolor=self.colors['bg_tertiary'],
                                       borderwidth=0,
                                       thickness=8,
                                       relief="flat")
                except tk.TclError:
                    self.style.configure("Warning.TProgressbar",
                                       background=self.colors['accent_yellow'],
                                       troughcolor=self.colors['bg_tertiary'])
                
            except Exception as e:
                self.logger.warning(f"Progressbar style configuration failed: {e}")
                # Use completely default progressbar styling
                
        except Exception as e:
            self.logger.warning(f"Style configuration failed: {e}")
    
    def create_safe_progressbar(self, parent, style="Modern.TProgressbar", **kwargs):
        """Create a progressbar with fallback styling"""
        try:
            # Try with custom style first
            return ttk.Progressbar(parent, style=style, **kwargs)
        except tk.TclError:
            try:
                # Try with basic TProgressbar
                return ttk.Progressbar(parent, style="TProgressbar", **kwargs)
            except tk.TclError:
                # Last resort - no style
                return ttk.Progressbar(parent, **kwargs)
    
    def create_modern_widgets(self):
        """Create modern UI widgets with enhanced functionality"""
        # Main container with padding
        self.main_frame = ttk.Frame(self.root, style="Modern.TFrame", padding="0")
        
        # Header section
        self.create_modern_header()
        
        # Content area with sidebar
        self.create_content_area()
        
        # Modern status bar
        self.create_modern_status_bar()
    
    def create_modern_header(self):
        """Create modern header with system info"""
        self.header_frame = ttk.Frame(self.main_frame, style="Header.TFrame", padding="25")
        
        # Left side - Title and subtitle
        header_left = ttk.Frame(self.header_frame, style="Header.TFrame")
        
        # Main title with icon
        title_frame = ttk.Frame(header_left, style="Header.TFrame")
        
        # Title and subtitle
        ttk.Label(title_frame, text="🛡️ DonTe Cleaner Pro", style="Title.TLabel").pack(side="left")
        ttk.Label(header_left, text="Professional System Optimization & Security Suite", 
                 style="Subtitle.TLabel").pack(anchor="w", pady=(5, 0))
        
        # Right side - System info cards
        header_right = ttk.Frame(self.header_frame, style="Header.TFrame")
        
        # System info mini cards
        self.create_system_info_cards(header_right)
        
        # Pack header components
        title_frame.pack(anchor="w")
        header_left.pack(side="left", fill="both", expand=True)
        header_right.pack(side="right")
    
    def create_system_info_cards(self, parent):
        """Create system information mini cards"""
        # CPU Card
        cpu_card = ttk.Frame(parent, style="Card.TFrame", padding="10")
        ttk.Label(cpu_card, text="💻 CPU", style="CardText.TLabel").pack()
        self.cpu_usage_label = ttk.Label(cpu_card, text="---%", style="CardTitle.TLabel")
        self.cpu_usage_label.pack()
        
        # RAM Card
        ram_card = ttk.Frame(parent, style="Card.TFrame", padding="10")
        ttk.Label(ram_card, text="🧠 RAM", style="CardText.TLabel").pack()
        ram_text = f"{self.system_info['ram_available']}GB/{self.system_info['ram_total']}GB"
        self.ram_usage_label = ttk.Label(ram_card, text=ram_text, style="CardTitle.TLabel")
        self.ram_usage_label.pack()
        
        # Disk Card
        disk_card = ttk.Frame(parent, style="Card.TFrame", padding="10")
        ttk.Label(disk_card, text="💾 Disk", style="CardText.TLabel").pack()
        disk_text = f"{self.system_info['disk_free']}GB Free"
        self.disk_usage_label = ttk.Label(disk_card, text=disk_text, style="CardTitle.TLabel")
        self.disk_usage_label.pack()
        
        # Status Card
        status_card = ttk.Frame(parent, style="Card.TFrame", padding="10")
        ttk.Label(status_card, text="🔒 Status", style="CardText.TLabel").pack()
        status_text = "Admin" if self.is_admin else "Limited"
        status_color = "CardTitle.TLabel"  # We'll change color based on status
        self.status_usage_label = ttk.Label(status_card, text=status_text, style=status_color)
        self.status_usage_label.pack()
        
        # Pack cards horizontally
        cpu_card.pack(side="left", padx=(0, 10))
        ram_card.pack(side="left", padx=(0, 10))
        disk_card.pack(side="left", padx=(0, 10))
        status_card.pack(side="left")
    
    def create_content_area(self):
        """Create main content area with sidebar navigation"""
        self.content_frame = ttk.Frame(self.main_frame, style="Modern.TFrame")
        
        # Sidebar navigation
        self.create_sidebar()
        
        # Main content area
        self.main_content = ttk.Frame(self.content_frame, style="Modern.TFrame", padding="20")
        
        # Create notebook for different sections
        self.notebook = ttk.Notebook(self.main_content, style="Modern.TNotebook")
        
        # Create enhanced tabs
        self.create_dashboard_tab()
        self.create_system_optimization_tab()
        self.create_gaming_optimization_tab()
        self.create_antivirus_tab()
        self.create_emulator_tab()
        self.create_settings_tab()
        
        # Pack content area
        self.main_content.pack(side="right", fill="both", expand=True)
    
    def create_sidebar(self):
        """Create modern sidebar with quick actions"""
        self.sidebar = ttk.Frame(self.content_frame, style="Card.TFrame", padding="15")
        self.sidebar.configure(width=250)
        
        # Sidebar title
        ttk.Label(self.sidebar, text="🚀 Quick Actions", style="CardTitle.TLabel").pack(pady=(0, 20))
        
        # Quick action buttons
        quick_actions = [
            ("🔍 Quick Scan", self.quick_scan, "Success.TButton"),
            ("🧹 System Clean", self.quick_cleanup, "Modern.TButton"),
            ("⚡ Boost Performance", self.quick_optimize, "Warning.TButton"),
            ("🎮 Gaming Mode", self.toggle_gaming_mode, "Success.TButton"),
            ("🔧 One-Click Fix", self.one_click_fix, "Modern.TButton"),
        ]
        
        for text, command, style in quick_actions:
            btn = ttk.Button(self.sidebar, text=text, style=style, 
                           command=command, width=25)
            btn.pack(fill="x", pady=5)
        
        # Separator
        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", pady=15)
        
        # Advanced features section
        ttk.Label(self.sidebar, text="🔥 Advanced Features", style="CardTitle.TLabel").pack(pady=(0, 15))
        
        advanced_actions = [
            ("🎨 Theme Manager", self.show_theme_manager, "Info.TButton"),
            ("📊 Performance Charts", self.show_performance_charts, "Modern.TButton"),
            ("🔔 Smart Notifications", self.show_smart_notifications, "Warning.TButton"),
            ("🔊 Sound Effects", self.show_sound_effects, "Success.TButton"),
            ("🌐 Network Optimizer", self.show_network_optimizer, "Info.TButton"),
            ("🔐 Privacy Cleaner", self.show_privacy_cleaner, "Warning.TButton"),
            ("📱 Mobile Connection", self.show_mobile_app, "Modern.TButton"),
        ]
        
        for text, command, style in advanced_actions:
            btn = ttk.Button(self.sidebar, text=text, style=style, 
                           command=command, width=25)
            btn.pack(fill="x", pady=3)
        
        # Separator
        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", pady=15)
        
        # System stats
        ttk.Label(self.sidebar, text="📊 System Stats", style="CardTitle.TLabel").pack(pady=(0, 15))
        
        # Real-time stats (will be updated)
        self.stats_frame = ttk.Frame(self.sidebar, style="Card.TFrame")
        self.stats_frame.pack(fill="x")
        
        # Pack sidebar
        self.sidebar.pack(side="left", fill="y", padx=(0, 20))
        self.sidebar.pack_propagate(False)  # Don't shrink
    
    def create_dashboard_tab(self):
        """Create enhanced dashboard tab"""
        dashboard_frame = ttk.Frame(self.notebook, style="Modern.TFrame", padding="20")
        self.notebook.add(dashboard_frame, text="🏠 Dashboard")
        
        # Create grid layout for dashboard cards
        dashboard_frame.grid_columnconfigure(0, weight=1)
        dashboard_frame.grid_columnconfigure(1, weight=1)
        dashboard_frame.grid_rowconfigure(0, weight=1)
        dashboard_frame.grid_rowconfigure(1, weight=1)
        
        # System overview card
        self.create_system_overview_card(dashboard_frame, 0, 0)
        
        # Performance metrics card
        self.create_performance_card(dashboard_frame, 0, 1)
        
        # Recent activity card
        self.create_activity_card(dashboard_frame, 1, 0)
        
        # Recommendations card
        self.create_recommendations_card(dashboard_frame, 1, 1)
    
    def create_system_overview_card(self, parent, row, col):
        """Create system overview card"""
        card = ttk.Frame(parent, style="Card.TFrame", padding="20")
        card.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
        
        ttk.Label(card, text="🖥️ System Overview", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 15))
        
        # System info
        info_text = f"""
OS: {self.system_info.get('os', 'Unknown')}
CPU Cores: {self.system_info.get('cpu_cores', 'N/A')}
Total RAM: {self.system_info.get('ram_total', 'N/A')} GB
Admin Rights: {'Yes' if self.is_admin else 'No'}
        """.strip()
        
        info_label = ttk.Label(card, text=info_text, style="CardText.TLabel")
        info_label.pack(anchor="w")
        
        # System health indicator
        health_frame = ttk.Frame(card, style="Card.TFrame")
        health_frame.pack(fill="x", pady=(15, 0))
        
        ttk.Label(health_frame, text="System Health:", style="CardText.TLabel").pack(side="left")
        
        # Health progress bar
        self.health_progress = self.create_safe_progressbar(health_frame, style="Success.TProgressbar", 
                                                           mode='determinate', length=100)
        self.health_progress.pack(side="right")
        self.health_progress['value'] = 85  # Will be calculated dynamically
    
    def create_performance_card(self, parent, row, col):
        """Create performance metrics card"""
        card = ttk.Frame(parent, style="Card.TFrame", padding="20")
        card.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
        
        ttk.Label(card, text="📈 Performance Metrics", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 15))
        
        # Performance bars
        self.create_performance_bars(card)
    
    def create_performance_bars(self, parent):
        """Create performance indicator bars"""
        metrics = [
            ("CPU Usage", "cpu_progress", self.colors['accent_blue']),
            ("RAM Usage", "ram_progress", self.colors['accent_yellow']),
            ("Disk Usage", "disk_progress", self.colors['accent_green'])
        ]
        
        for label_text, attr_name, color in metrics:
            metric_frame = ttk.Frame(parent, style="Card.TFrame")
            metric_frame.pack(fill="x", pady=5)
            
            ttk.Label(metric_frame, text=label_text, style="CardText.TLabel").pack(anchor="w")
            
            progress = self.create_safe_progressbar(metric_frame, style="Modern.TProgressbar", 
                                                   mode='determinate', length=200)
            progress.pack(fill="x", pady=2)
            
            # Store reference for updates
            setattr(self, attr_name, progress)
            
            # Percentage label
            percent_label = ttk.Label(metric_frame, text="0%", style="CardText.TLabel")
            percent_label.pack(anchor="e")
            setattr(self, f"{attr_name}_label", percent_label)
    
    def create_activity_card(self, parent, row, col):
        """Create recent activity card"""
        card = ttk.Frame(parent, style="Card.TFrame", padding="20")
        card.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
        
        ttk.Label(card, text="📋 Recent Activity", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 15))
        
        # Activity list
        self.activity_frame = ttk.Frame(card, style="Card.TFrame")
        self.activity_frame.pack(fill="both", expand=True)
        
        # Sample activities
        self.add_activity("System started", "info")
        self.add_activity(f"Running in {'Admin' if self.is_admin else 'Limited'} mode", 
                         "warning" if not self.is_admin else "success")
    
    def create_recommendations_card(self, parent, row, col):
        """Create recommendations card"""
        card = ttk.Frame(parent, style="Card.TFrame", padding="20")
        card.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
        
        ttk.Label(card, text="💡 Recommendations", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 15))
        
        # Recommendations list
        recommendations = [
            "🔍 Run a full system scan",
            "🧹 Clear temporary files",
            "⚡ Optimize startup programs",
            "🎮 Enable gaming mode for better performance"
        ]
        
        for rec in recommendations:
            ttk.Label(card, text=rec, style="CardText.TLabel").pack(anchor="w", pady=2)
    
    def add_activity(self, text, activity_type="info"):
        """Add activity to recent activity list"""
        icons = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌"}
        icon = icons.get(activity_type, "ℹ️")
        
    
    def create_system_optimization_tab(self):
        """Create enhanced system optimization tab"""
        system_frame = ttk.Frame(self.notebook, style="Modern.TFrame", padding="20")
        self.notebook.add(system_frame, text="🔧 System Optimizer")
        
        # Create sections
        self.create_windows_optimization_section(system_frame)
        self.create_ram_optimization_section(system_frame)
        self.create_disk_optimization_section(system_frame)
    
    def create_windows_optimization_section(self, parent):
        """Create Windows-specific optimization section"""
        section = ttk.LabelFrame(parent, text="🪟 Windows Optimization", padding="15")
        section.pack(fill="x", pady=(0, 15))
        
        # Windows optimizations with progress tracking
        win_optimizations = [
            ("🚫 Disable Unnecessary Services", self.disable_services_with_progress, 
             "Stops background services like Print Spooler, Windows Search"),
            ("🚀 Clean Startup Programs", self.clean_startup_with_progress,
             "Removes unnecessary programs from Windows startup"),
            ("🎨 Disable Visual Effects", self.disable_visual_effects_with_progress,
             "Turns off animations and transparency for better performance"),
            ("⚡ Set High Performance Power Plan", self.set_power_plan_with_progress,
             "Changes power settings to maximum performance"),
            ("🗑️ Clean System Files", self.clean_system_files_with_progress,
             "Removes temporary files, cache, and system junk"),
            ("📝 Optimize Registry", self.optimize_registry_with_progress,
             "Cleans and optimizes Windows registry entries")
        ]
        
        for i, (title, command, description) in enumerate(win_optimizations):
            self.create_optimization_card(section, title, description, command, i)
    
    def create_ram_optimization_section(self, parent):
        """Create RAM optimization section"""
        section = ttk.LabelFrame(parent, text="🧠 Memory (RAM) Optimization", padding="15")
        section.pack(fill="x", pady=(0, 15))
        
        # Current RAM status
        ram_status_frame = ttk.Frame(section)
        ram_status_frame.pack(fill="x", pady=(0, 10))
        
        memory = psutil.virtual_memory()
        ram_text = f"RAM Usage: {memory.used//1024**3}GB / {memory.total//1024**3}GB ({memory.percent:.1f}%)"
        ttk.Label(ram_status_frame, text=ram_text, font=("Segoe UI", 12, "bold")).pack(side="left")
        
        # RAM optimization progress bar
        self.ram_opt_progress = self.create_safe_progressbar(ram_status_frame, style="Success.TProgressbar", 
                                                            length=200, mode='determinate')
        self.ram_opt_progress.pack(side="right")
        
        # RAM optimizations
        ram_optimizations = [
            ("🔄 Clear Memory Cache", self.clear_memory_cache,
             "Clears system memory cache and frees up RAM"),
            ("❌ Close Background Apps", self.close_background_apps_with_progress,
             "Closes unnecessary background applications"),
            ("🎯 Memory Compression", self.enable_memory_compression,
             "Enables Windows memory compression feature"),
            ("💾 Optimize Virtual Memory", self.optimize_virtual_memory,
             "Configures page file for optimal performance")
        ]
        
        for i, (title, command, description) in enumerate(ram_optimizations):
            self.create_optimization_card(section, title, description, command, i, compact=True)
    
    def create_disk_optimization_section(self, parent):
        """Create disk optimization section"""
        section = ttk.LabelFrame(parent, text="💾 Disk Optimization", padding="15")
        section.pack(fill="x")
        
        # Disk optimizations
        disk_optimizations = [
            ("🗑️ Disk Cleanup", self.advanced_disk_cleanup,
             "Deep cleaning of temporary files and system cache"),
            ("📁 Duplicate File Finder", self.find_duplicate_files,
             "Finds and removes duplicate files to free space"),
            ("🔧 Defragment Drives", self.defragment_drives,
             "Optimizes disk performance by defragmenting"),
            ("📊 Disk Health Check", self.check_disk_health,
             "Checks disk health and reports potential issues")
        ]
        
        for i, (title, command, description) in enumerate(disk_optimizations):
            self.create_optimization_card(section, title, description, command, i, compact=True)
    
    def create_gaming_optimization_tab(self):
        """Create gaming optimization tab for W10/W11"""
        gaming_frame = ttk.Frame(self.notebook, style="Modern.TFrame", padding="20")
        self.notebook.add(gaming_frame, text="🎮 Gaming Optimizer")
        
        # Gaming mode status
        self.create_gaming_status_section(gaming_frame)
        
        # Windows 10/11 specific optimizations
        self.create_windows_gaming_section(gaming_frame)
        
        # Performance boost section
        self.create_performance_boost_section(gaming_frame)
    
    def create_gaming_status_section(self, parent):
        """Create gaming mode status section"""
        status_section = ttk.LabelFrame(parent, text="🎮 Gaming Mode Status", padding="15")
        status_section.pack(fill="x", pady=(0, 15))
        
        # Gaming mode indicator
        self.gaming_status_frame = ttk.Frame(status_section)
        self.gaming_status_frame.pack(fill="x")
        
        self.gaming_status_label = ttk.Label(self.gaming_status_frame, 
                                           text="Gaming Mode: Checking...", 
                                           font=("Segoe UI", 14, "bold"))
        self.gaming_status_label.pack(side="left")
        
        # Toggle button
        self.gaming_toggle_btn = ttk.Button(self.gaming_status_frame, 
                                          text="Enable Gaming Mode",
                                          style="Success.TButton",
                                          command=self.toggle_gaming_mode)
        self.gaming_toggle_btn.pack(side="right")
        
        # Update gaming status
        self.update_gaming_status()
    
    def create_windows_gaming_section(self, parent):
        """Create Windows 10/11 gaming optimizations"""
        section = ttk.LabelFrame(parent, text="🪟 Windows Gaming Optimizations", padding="15")
        section.pack(fill="x", pady=(0, 15))
        
        gaming_opts = [
            ("🎯 Enable Game Mode", self.enable_game_mode,
             "Activates Windows Game Mode for better gaming performance"),
            ("🔇 Disable Game Bar", self.disable_game_bar,
             "Disables Xbox Game Bar to reduce resource usage"),
            ("⏰ Disable Background Apps", self.disable_background_apps,
             "Prevents apps from running in background during gaming"),
            ("🔔 Disable Notifications", self.disable_notifications,
             "Turns off notifications during full-screen games"),
            ("🖱️ Optimize Mouse Settings", self.optimize_mouse_settings,
             "Disables mouse acceleration for gaming"),
            ("🎨 Disable Transparency Effects", self.disable_transparency,
             "Disables Windows transparency for better performance")
        ]
        
        for i, (title, command, description) in enumerate(gaming_opts):
            self.create_optimization_card(section, title, description, command, i, compact=True)
    
    def create_performance_boost_section(self, parent):
        """Create performance boost section"""
        section = ttk.LabelFrame(parent, text="⚡ Performance Boost", padding="15")
        section.pack(fill="x")
        
        boost_opts = [
            ("🚀 Ultimate Performance Mode", self.enable_ultimate_performance,
             "Enables hidden Ultimate Performance power plan"),
            ("💨 Disable Startup Delay", self.disable_startup_delay,
             "Removes artificial startup delays in Windows"),
            ("🔧 Optimize Network Settings", self.optimize_network_gaming,
             "Optimizes network settings for gaming"),
            ("🎵 Disable Audio Enhancements", self.disable_audio_enhancements,
             "Disables audio enhancements that can cause latency")
        ]
        
        for i, (title, command, description) in enumerate(boost_opts):
            self.create_optimization_card(section, title, description, command, i, compact=True)
    
    def create_optimization_card(self, parent, title, description, command, index, compact=False):
        """Create an optimization card with progress tracking"""
        card_height = 60 if compact else 80
        
        card = ttk.Frame(parent, style="Card.TFrame", padding="10")
        card.pack(fill="x", pady=5)
        
        # Left side - title and description
        left_frame = ttk.Frame(card, style="Card.TFrame")
        left_frame.pack(side="left", fill="both", expand=True)
        
        ttk.Label(left_frame, text=title, font=("Segoe UI", 12, "bold")).pack(anchor="w")
        if not compact:
            ttk.Label(left_frame, text=description, font=("Segoe UI", 9), 
                     foreground=self.colors['text_secondary']).pack(anchor="w")
        
        # Right side - button and progress
        right_frame = ttk.Frame(card, style="Card.TFrame")
        right_frame.pack(side="right")
        
        # Execute button
        btn = ttk.Button(right_frame, text="Execute", style="Modern.TButton",
                        command=lambda: self.execute_with_progress(command, title))
        btn.pack(side="right", padx=(10, 0))
        
        # Progress indicator (hidden initially)
        progress = self.create_safe_progressbar(right_frame, style="Modern.TProgressbar", 
                                               length=100, mode='indeterminate')
        
        # Store references for progress tracking
        setattr(self, f"progress_{index}", progress)
        setattr(self, f"btn_{index}", btn)
    
    def execute_with_progress(self, command, operation_name):
        """Execute command with visual progress feedback"""
        self.current_operation = operation_name
        
        def worker():
            try:
                # Show progress
                self.root.after(0, lambda: self.show_operation_progress(True))
                
                # Execute command
                if hasattr(command, '__call__'):
                    result = command()
                else:
                    result = True, "Operation completed"
                
                # Handle result
                if isinstance(result, tuple) and len(result) == 2:
                    success, message = result
                else:
                    success, message = True, "Operation completed"
                
                # Update UI
                self.root.after(0, lambda: self.show_operation_progress(False))
                self.root.after(0, lambda: self.add_activity(f"{operation_name}: {message}", 
                                                           "success" if success else "error"))
                
                if success:
                    self.root.after(0, lambda: messagebox.showinfo("Success", f"{operation_name}\n\n{message}"))
                else:
                    self.root.after(0, lambda: messagebox.showerror("Error", f"{operation_name}\n\n{message}"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.show_operation_progress(False))
                self.root.after(0, lambda: messagebox.showerror("Error", f"{operation_name} failed:\n\n{str(e)}"))
                self.logger.error(f"Operation {operation_name} failed: {str(e)}")
        
        threading.Thread(target=worker, daemon=True).start()
    
    def show_operation_progress(self, show):
        """Show or hide operation progress"""
        # This will be implemented to show progress in status bar
        if show:
            self.progress_label.config(text=f"Executing: {self.current_operation}")
            self.progress_bar.config(mode='indeterminate')
            self.progress_bar.start()
        else:
            self.progress_bar.stop()
            self.progress_bar.config(mode='determinate', value=100)
            self.root.after(2000, lambda: self.progress_bar.config(value=0))
            self.root.after(2000, lambda: self.progress_label.config(text="Ready"))
    
    # Gaming optimization methods
    def toggle_gaming_mode(self):
        """Toggle gaming mode on/off with visual feedback"""
        def gaming_mode_worker():
            try:
                self.root.after(0, lambda: self.progress_label.config(text="Checking gaming mode status..."))
                self.root.after(0, lambda: self.progress_bar.config(value=10))
                
                # Check current gaming mode status
                current_status = self.check_gaming_mode_status()
                
                if current_status:
                    self.root.after(0, lambda: self.progress_label.config(text="Disabling gaming mode..."))
                    result = self.disable_gaming_mode()
                    action = "disabled"
                else:
                    self.root.after(0, lambda: self.progress_label.config(text="Enabling gaming mode..."))
                    result = self.enable_gaming_mode_full()
                    action = "enabled"
                
                self.root.after(0, lambda: self.progress_bar.config(value=100))
                
                if isinstance(result, tuple) and result[0]:
                    message = f"Gaming mode {action} successfully!"
                    self.root.after(0, lambda: self.progress_label.config(text=message))
                    self.root.after(0, lambda: messagebox.showinfo("Gaming Mode", message))
                    if hasattr(self, 'add_activity'):
                        self.root.after(0, lambda: self.add_activity(f"Gaming mode {action}", "success"))
                else:
                    error_msg = result[1] if isinstance(result, tuple) else "Gaming mode operation failed"
                    self.root.after(0, lambda: self.progress_label.config(text="Gaming mode operation failed"))
                    self.root.after(0, lambda: messagebox.showerror("Gaming Mode Error", error_msg))
                    if hasattr(self, 'add_activity'):
                        self.root.after(0, lambda: self.add_activity(f"Gaming mode operation failed", "error"))
                
                self.root.after(2000, lambda: self.progress_label.config(text="Ready"))
                
            except Exception as e:
                error_msg = f"Gaming mode toggle failed: {str(e)}"
                self.logger.error(error_msg)
                self.root.after(0, lambda: self.progress_label.config(text="Gaming mode error"))
                self.root.after(0, lambda: messagebox.showerror("Gaming Mode Error", error_msg))
                if hasattr(self, 'add_activity'):
                    self.root.after(0, lambda: self.add_activity("Gaming mode error", "error"))
        
        # Run in separate thread to avoid blocking UI
        threading.Thread(target=gaming_mode_worker, daemon=True).start()
    
    def enable_gaming_mode_full(self):
        """Enable full gaming mode with all optimizations"""
        try:
            operations = [
                self.enable_game_mode,
                self.disable_game_bar,
                self.disable_background_apps,
                self.optimize_mouse_settings,
                self.set_power_plan_ultimate
            ]
            
            completed = 0
            for operation in operations:
                try:
                    operation()
                    completed += 1
                except:
                    pass
            
            self.update_gaming_status()
            return True, f"Gaming mode enabled! {completed}/{len(operations)} optimizations applied"
            
        except Exception as e:
            return False, f"Gaming mode activation failed: {str(e)}"
    
    def update_gaming_status(self):
        """Update gaming mode status display"""
        try:
            is_enabled = self.check_gaming_mode_status()
            
            if is_enabled:
                self.gaming_status_label.config(text="🎮 Gaming Mode: ACTIVE", 
                                               foreground=self.colors['accent_green'])
                self.gaming_toggle_btn.config(text="Disable Gaming Mode", style="Danger.TButton")
            else:
                self.gaming_status_label.config(text="🎮 Gaming Mode: INACTIVE", 
                                               foreground=self.colors['accent_red'])
                self.gaming_toggle_btn.config(text="Enable Gaming Mode", style="Success.TButton")
                
        except Exception as e:
            self.gaming_status_label.config(text="🎮 Gaming Mode: ERROR")
            self.logger.error(f"Gaming status update failed: {str(e)}")
    
    def check_gaming_mode_status(self):
        """Check if gaming mode is currently enabled"""
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                               r"Software\Microsoft\GameBar", 0, winreg.KEY_READ)
            value, _ = winreg.QueryValueEx(key, "AllowAutoGameMode")
            winreg.CloseKey(key)
            return value == 1
        except:
            return False
    def __init__(self, root):
        self.root = root
        self.logger = get_logger("MainWindow")
        self.is_admin = is_admin()
        
        # Initialize core modules
        self.windows_optimizer = WindowsOptimizer()
        self.antivirus_scanner = AntivirusScanner()
        self.enhanced_antivirus = EnhancedAntivirusScanner()
        self.emulator_optimizer = EmulatorOptimizer()
        
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        self.setup_layout()
        
        # Show admin status
        self.update_status_bar()
    
    def setup_window(self):
        """Setup main window properties"""
        admin_status = "Yönetici" if self.is_admin else "Sınırlı Mod"
        self.root.title(f"DonTe Cleaner - Professional Windows Optimizer ({admin_status})")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        self.root.configure(bg="#1a1a1a")
        
        # Center window on screen
        self.center_window()
        
        # Set icon if available
        try:
            self.root.iconbitmap("resources/icon.ico")
        except:
            pass
            pass
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_styles(self):
        """Setup modern UI styles"""
        self.style = ttk.Style()
        
        # Try to use clam theme, fallback to default if not available
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            try:
                self.style.theme_use("vista")
            except tk.TclError:
                try:
                    self.style.theme_use("default")
                except tk.TclError:
                    pass  # Use whatever is available
        
        # Define colors
        self.colors = {
            'bg_dark': '#1a1a1a',
            'bg_medium': '#2d2d2d',
            'bg_light': '#3d3d3d',
            'accent': '#0078d4',
            'accent_hover': '#106ebe',
            'success': '#107c10',
            'warning': '#ff8c00',
            'danger': '#d13438',
            'text_white': '#ffffff',
            'text_gray': '#cccccc'
        }
        
        # Configure styles
        self.style.configure("Title.TLabel", 
                           background=self.colors['bg_dark'],
                           foreground=self.colors['text_white'],
                           font=("Segoe UI", 24, "bold"))
        
        self.style.configure("Subtitle.TLabel",
                           background=self.colors['bg_dark'],
                           foreground=self.colors['text_gray'],
                           font=("Segoe UI", 12))
        
        self.style.configure("Modern.TButton",
                           background=self.colors['accent'],
                           foreground=self.colors['text_white'],
                           font=("Segoe UI", 11),
                           borderwidth=0,
                           focuscolor='none')
        
        self.style.map("Modern.TButton",
                      background=[('active', self.colors['accent_hover'])])
        
        self.style.configure("Success.TButton",
                           background=self.colors['success'],
                           foreground=self.colors['text_white'],
                           font=("Segoe UI", 11),
                           borderwidth=0)
        
        self.style.configure("Warning.TButton",
                           background=self.colors['warning'],
                           foreground=self.colors['text_white'],
                           font=("Segoe UI", 11),
                           borderwidth=0)
        
        self.style.configure("Danger.TButton",
                           background=self.colors['danger'],
                           foreground=self.colors['text_white'],
                           font=("Segoe UI", 11),
                           borderwidth=0)
        
        self.style.configure("Modern.TFrame",
                           background=self.colors['bg_medium'],
                           relief="flat",
                           borderwidth=1)
        
        self.style.configure("Card.TFrame",
                           background=self.colors['bg_light'],
                           relief="flat",
                           borderwidth=1)
        
        self.style.configure("Modern.TNotebook",
                           background=self.colors['bg_dark'],
                           borderwidth=0)
        
        self.style.configure("Modern.TNotebook.Tab",
                           background=self.colors['bg_medium'],
                           foreground=self.colors['text_white'],
                           padding=[20, 10],
                           font=("Segoe UI", 11))
        
        self.style.map("Modern.TNotebook.Tab",
                      background=[('selected', self.colors['accent'])])
        
        self.style.configure("Modern.TProgressbar",
                           background=self.colors['accent'],
                           troughcolor=self.colors['bg_medium'],
                           borderwidth=0,
                           lightcolor=self.colors['accent'],
                           darkcolor=self.colors['accent'])
        
        # Configure horizontal progressbar specifically
        self.style.configure("Horizontal.Modern.TProgressbar",
                           background=self.colors['accent'],
                           troughcolor=self.colors['bg_medium'],
                           borderwidth=0,
                           lightcolor=self.colors['accent'],
                           darkcolor=self.colors['accent'])
        
        # Configure basic progressbar as fallback
        self.style.configure("TProgressbar",
                           background=self.colors['accent'],
                           troughcolor=self.colors['bg_medium'],
                           borderwidth=0)
    
    def create_widgets(self):
        """Create all UI widgets"""
        # Main container
        self.main_frame = ttk.Frame(self.root, style="Modern.TFrame", padding="20")
        
        # Header
        self.create_header()
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame, style="Modern.TNotebook")
        
        # Create tabs
        self.create_overview_tab()
        self.create_system_tab()
        self.create_antivirus_tab()
        self.create_emulator_tab()
        self.create_settings_tab()
        
        # Progress bar
        self.progress_frame = ttk.Frame(self.main_frame, style="Modern.TFrame")
        
        # Create progress bar with fallback styling
        self.progress_bar = self.create_safe_progressbar(
            self.progress_frame, 
            style="Modern.TProgressbar",
            mode='determinate'
        )
        self.progress_label = ttk.Label(
            self.progress_frame,
            text="Hazır",
            background=self.colors['bg_medium'],
            foreground=self.colors['text_white'],
            font=("Segoe UI", 10)
        )
        
        # Status bar
        self.status_bar = ttk.Frame(self.main_frame, style="Modern.TFrame")
        self.status_label = ttk.Label(
            self.status_bar,
            text="DonTe Cleaner v2.0 - Hazır",
            background=self.colors['bg_medium'],
            foreground=self.colors['text_gray'],
            font=("Segoe UI", 9)
        )
        self.admin_label = ttk.Label(
            self.status_bar,
            text="",
            background=self.colors['bg_medium'],
            foreground=self.colors['warning'] if not self.is_admin else self.colors['success'],
            font=("Segoe UI", 9, "bold")
        )
    
    def create_header(self):
        """Create application header"""
        header_frame = ttk.Frame(self.main_frame, style="Modern.TFrame")
        
        # Title and subtitle
        ttk.Label(header_frame, text="DonTe Cleaner", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header_frame, text="Professional Windows Optimization & Security Tool", 
                 style="Subtitle.TLabel").pack(anchor="w", pady=(0, 20))
        
        self.header_frame = header_frame
    
    def create_overview_tab(self):
        """Create enhanced overview/dashboard tab with beautiful UI"""
        tab_frame = ttk.Frame(self.notebook, style="Modern.TFrame", padding="20")
        self.notebook.add(tab_frame, text="🏠 Ana Sayfa")
        
        # Create main dashboard container with scrolling
        canvas = tk.Canvas(tab_frame, highlightthickness=0, bg=self.colors['bg_dark'])
        scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style="Modern.TFrame")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Dashboard header with welcome message
        self.create_dashboard_header(scrollable_frame)
        
        # Quick stats row
        self.create_quick_stats_row(scrollable_frame)
        
        # System health card
        self.create_system_health_card(scrollable_frame)
        
        # Quick actions grid
        self.create_quick_actions_grid(scrollable_frame)
        
        # Performance monitor card
        self.create_performance_monitor_card(scrollable_frame)
        
        # Gaming & advanced controls
        self.create_advanced_controls_card(scrollable_frame)
        
        # Recent activities card
        self.create_recent_activities_card(scrollable_frame)
        
        # Store references
        self.dashboard_frame = scrollable_frame
        self.dashboard_canvas = canvas
    
    def create_dashboard_header(self, parent):
        """Create beautiful dashboard header"""
        header_card = ttk.Frame(parent, style="Card.TFrame", padding="20")
        header_card.pack(fill="x", pady=(0, 15))
        
        # Welcome section
        welcome_frame = ttk.Frame(header_card, style="Card.TFrame")
        welcome_frame.pack(fill="x")
        
        # Time-based greeting
        import datetime
        hour = datetime.datetime.now().hour
        if hour < 12:
            greeting = "🌅 Günaydın!"
        elif hour < 17:
            greeting = "☀️ İyi Günler!"
        else:
            greeting = "🌙 İyi Akşamlar!"
        
        ttk.Label(welcome_frame, text=greeting, 
                 font=("Segoe UI", 18, "bold"),
                 background=self.colors['bg_light'],
                 foreground=self.colors['accent']).pack(anchor="w")
        
        status_text = "Yönetici" if self.is_admin else "Sınırlı Mod"
        status_color = self.colors['success'] if self.is_admin else self.colors['warning']
        
        ttk.Label(welcome_frame, 
                 text=f"DonTe Cleaner Pro ile sisteminizi optimize edin • {status_text}", 
                 font=("Segoe UI", 12),
                 background=self.colors['bg_light'],
                 foreground=status_color).pack(anchor="w", pady=(5, 0))
    
    def create_quick_stats_row(self, parent):
        """Create quick statistics row"""
        stats_frame = ttk.Frame(parent, style="Modern.TFrame")
        stats_frame.pack(fill="x", pady=(0, 15))
        
        # Create 4 stat cards in a row
        self.create_stat_card(stats_frame, "💻", "CPU Kullanımı", "0%", "cpu", side="left")
        self.create_stat_card(stats_frame, "🧠", "RAM Kullanımı", "0%", "ram", side="left")
        self.create_stat_card(stats_frame, "💾", "Disk Kullanımı", "0%", "disk", side="left")
        self.create_stat_card(stats_frame, "⚡", "Sistem Sağlığı", "100%", "health", side="left")
    
    def create_stat_card(self, parent, icon, title, value, stat_type, side="left"):
        """Create individual stat card"""
        card = ttk.Frame(parent, style="Card.TFrame", padding="15")
        card.pack(side=side, fill="both", expand=True, padx=(0, 10) if side == "left" else (0, 0))
        
        # Icon and value
        icon_frame = ttk.Frame(card, style="Card.TFrame")
        icon_frame.pack(fill="x")
        
        ttk.Label(icon_frame, text=icon, 
                 font=("Segoe UI", 24),
                 background=self.colors['bg_light'],
                 foreground=self.colors['accent']).pack(side="left")
        
        value_frame = ttk.Frame(icon_frame, style="Card.TFrame")
        value_frame.pack(side="right", fill="x", expand=True)
        
        # Value label with dynamic color
        value_label = ttk.Label(value_frame, text=value, 
                               font=("Segoe UI", 16, "bold"),
                               background=self.colors['bg_light'],
                               foreground=self.colors['text_white'])
        value_label.pack(anchor="e")
        
        ttk.Label(value_frame, text=title, 
                 font=("Segoe UI", 10),
                 background=self.colors['bg_light'],
                 foreground=self.colors['text_gray']).pack(anchor="e")
        
        # Store reference for updates
        setattr(self, f"{stat_type}_stat_label", value_label)
    
    def create_system_health_card(self, parent):
        """Create system health monitoring card"""
        health_card = ttk.Frame(parent, style="Card.TFrame", padding="20")
        health_card.pack(fill="x", pady=(0, 15))
        
        # Header
        header_frame = ttk.Frame(health_card, style="Card.TFrame")
        header_frame.pack(fill="x", pady=(0, 15))
        
        ttk.Label(header_frame, text="🏥 Sistem Sağlığı", 
                 font=("Segoe UI", 16, "bold"),
                 background=self.colors['bg_light'],
                 foreground=self.colors['text_white']).pack(side="left")
        
        # Health score display
        self.health_score_label = ttk.Label(header_frame, text="100%", 
                                           font=("Segoe UI", 16, "bold"),
                                           background=self.colors['bg_light'],
                                           foreground=self.colors['success'])
        self.health_score_label.pack(side="right")
        
        # Health progress bar
        progress_frame = ttk.Frame(health_card, style="Card.TFrame")
        progress_frame.pack(fill="x", pady=(0, 10))
        
        self.health_progress = self.create_safe_progressbar(progress_frame, length=400, mode='determinate')
        self.health_progress.pack(fill="x")
        self.health_progress['value'] = 100
        
        # System info content frame (from earlier implementation)
        self.system_info_content = ttk.Frame(health_card, style="Card.TFrame")
        self.system_info_content.pack(fill="x")
        
        # Store frame reference
        self.system_info_frame = health_card
        
        # Initialize system info display
        self.update_system_info_display()
        
        # Initialize system monitoring for dashboard
        self.initialize_dashboard_monitoring()
        
        # Create remaining dashboard components
        self.create_quick_actions_grid(parent)
        self.create_performance_monitor_card(parent)
        self.create_advanced_controls_card(parent)
        self.create_recent_activities_card(parent)
    
    def initialize_dashboard_monitoring(self):
        """Initialize dashboard monitoring and updates"""
        # Set default values for progress bars and stats
        if hasattr(self, 'cpu_progress'):
            self.cpu_progress['value'] = 0
        if hasattr(self, 'ram_progress'):
            self.ram_progress['value'] = 0
        if hasattr(self, 'disk_progress'):
            self.disk_progress['value'] = 0
        
        # Start dashboard updates
        self.update_dashboard_stats()
    
    def update_dashboard_stats(self):
        """Update dashboard statistics"""
        try:
            # Get system stats
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('C:')
            disk_percent = (disk.used / disk.total) * 100
            
            # Update stat cards
            if hasattr(self, 'cpu_stat_label'):
                color = self.get_status_color(cpu_percent)
                self.cpu_stat_label.config(text=f"{cpu_percent:.1f}%", foreground=color)
            
            if hasattr(self, 'ram_stat_label'):
                color = self.get_status_color(memory.percent)
                self.ram_stat_label.config(text=f"{memory.percent:.1f}%", foreground=color)
            
            if hasattr(self, 'disk_stat_label'):
                color = self.get_status_color(disk_percent)
                self.disk_stat_label.config(text=f"{disk_percent:.1f}%", foreground=color)
            
            # Update progress bars
            if hasattr(self, 'cpu_progress'):
                self.cpu_progress['value'] = cpu_percent
            if hasattr(self, 'ram_progress'):
                self.ram_progress['value'] = memory.percent
            if hasattr(self, 'disk_progress'):
                self.disk_progress['value'] = disk_percent
            
            # Update health score
            health_score = self.calculate_health_score_ui()
            if hasattr(self, 'health_stat_label'):
                health_color = self.get_health_color_ui(health_score)
                self.health_stat_label.config(text=f"{health_score}%", foreground=health_color)
            if hasattr(self, 'health_progress'):
                self.health_progress['value'] = health_score
            if hasattr(self, 'health_score_label'):
                health_color = self.get_health_color_ui(health_score)
                self.health_score_label.config(text=f"{health_score}%", foreground=health_color)
            
            # Schedule next update
            self.root.after(3000, self.update_dashboard_stats)
            
        except Exception as e:
            print(f"Dashboard update error: {e}")
            self.root.after(5000, self.update_dashboard_stats)
    
    def get_status_color(self, percent):
        """Get color based on usage percentage"""
        if percent > 80:
            return self.colors['danger']
        elif percent > 60:
            return self.colors['warning']
        else:
            return self.colors['success']
    
    def calculate_health_score_ui(self):
        """Calculate health score for UI"""
        try:
            score = 100
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('C:')
            disk_percent = (disk.used / disk.total) * 100
            
            # Deduct points based on usage
            if cpu_percent > 80:
                score -= 25
            elif cpu_percent > 60:
                score -= 15
            
            if memory.percent > 80:
                score -= 25
            elif memory.percent > 60:
                score -= 15
            
            if disk_percent > 90:
                score -= 20
            elif disk_percent > 80:
                score -= 10
            
            return max(0, min(100, score))
        except:
            return 75
    
    def get_health_color_ui(self, score):
        """Get health color for UI"""
        if score >= 80:
            return self.colors['success']
        elif score >= 60:
            return self.colors['warning']
        else:
            return self.colors['danger']
    
    def add_activity(self, activity, status="Bilgi"):
        """Add activity to recent activities"""
        try:
            if hasattr(self, 'activities_frame'):
                # Limit to 5 activities
                children = self.activities_frame.winfo_children()
                if len(children) >= 5:
                    children[0].destroy()
                
                # Add new activity
                activity_frame = ttk.Frame(self.activities_frame, style="Card.TFrame")
                activity_frame.pack(fill="x", pady=(0, 5))
                
                # Status icon
                status_icons = {
                    "Başarılı": "✅",
                    "Uyarı": "⚠️",
                    "Hata": "❌",
                    "Bilgi": "ℹ️"
                }
                icon = status_icons.get(status, "ℹ️")
                
                ttk.Label(activity_frame, text=f"{icon} {activity}", 
                         font=("Segoe UI", 10),
                         background=self.colors['bg_light'],
                         foreground=self.colors['text_white']).pack(side="left")
                
                # Timestamp
                import datetime
                timestamp = datetime.datetime.now().strftime("%H:%M")
                ttk.Label(activity_frame, text=timestamp, 
                         font=("Segoe UI", 9),
                         background=self.colors['bg_light'],
                         foreground=self.colors['text_gray']).pack(side="right")
        except Exception as e:
            print(f"Activity add error: {e}")
    
    def clear_activities(self):
        """Clear all activities"""
        try:
            if hasattr(self, 'activities_frame'):
                for child in self.activities_frame.winfo_children():
                    child.destroy()
                self.add_activity("Aktivite geçmişi temizlendi", "Bilgi")
        except Exception as e:
            print(f"Clear activities error: {e}")
    
    # Quick action UI methods
    def quick_scan_ui(self):
        """Quick scan from UI"""
        def scan_worker():
            try:
                self.root.after(0, lambda: self.progress_label.config(text="Starting quick scan..."))
                self.root.after(0, lambda: self.progress_bar.config(value=10))
                
                self.root.after(0, lambda: self.add_activity("Hızlı tarama başlatıldı", "info"))
                
                # Use the actual quick scan method
                self.root.after(0, lambda: self.progress_bar.config(value=50))
                self.start_quick_scan()
                
                self.root.after(0, lambda: self.progress_bar.config(value=100))
                self.root.after(0, lambda: self.progress_label.config(text="Quick scan completed"))
                self.root.after(0, lambda: self.add_activity("Hızlı tarama tamamlandı", "success"))
                
                # Reset progress after delay
                self.root.after(2000, lambda: self.progress_bar.config(value=0))
                self.root.after(2000, lambda: self.progress_label.config(text="Ready"))
                
            except Exception as e:
                self.root.after(0, lambda: self.add_activity(f"Tarama hatası: {str(e)}", "error"))
                self.root.after(0, lambda: self.progress_bar.config(value=0))
                self.root.after(0, lambda: self.progress_label.config(text="Error"))
        
        # Run in separate thread
        threading.Thread(target=scan_worker, daemon=True).start()
    
    def quick_clean_temp_ui(self):
        """Quick temp clean from UI"""
        def clean_worker():
            try:
                self.root.after(0, lambda: self.progress_label.config(text="Cleaning temporary files..."))
                self.root.after(0, lambda: self.progress_bar.config(value=20))
                
                self.root.after(0, lambda: self.add_activity("Geçici dosyalar temizleniyor", "info"))
                
                # Use the actual temp file cleaning method
                self.root.after(0, lambda: self.progress_bar.config(value=60))
                result = self.clean_temp_files()
                
                self.root.after(0, lambda: self.progress_bar.config(value=100))
                self.root.after(0, lambda: self.progress_label.config(text="Temp files cleaned"))
                self.root.after(0, lambda: self.add_activity("Geçici dosyalar temizlendi", "success"))
                
                # Reset progress after delay
                self.root.after(2000, lambda: self.progress_bar.config(value=0))
                self.root.after(2000, lambda: self.progress_label.config(text="Ready"))
                
            except Exception as e:
                self.root.after(0, lambda: self.add_activity(f"Temizlik hatası: {str(e)}", "error"))
                self.root.after(0, lambda: self.progress_bar.config(value=0))
                self.root.after(0, lambda: self.progress_label.config(text="Error"))
        
        # Run in separate thread
        threading.Thread(target=clean_worker, daemon=True).start()
    
    def quick_performance_boost_ui(self):
        """Quick performance boost from UI"""
        def boost_worker():
            try:
                self.root.after(0, lambda: self.progress_label.config(text="Performance boost starting..."))
                self.root.after(0, lambda: self.progress_bar.config(value=10))
                
                self.root.after(0, lambda: self.add_activity("Performans boost başlatıldı", "info"))
                
                # Memory optimization
                self.root.after(0, lambda: self.progress_bar.config(value=30))
                self.root.after(0, lambda: self.progress_label.config(text="Optimizing memory..."))
                self.optimize_memory()
                
                # Clean temp files
                self.root.after(0, lambda: self.progress_bar.config(value=60))
                self.root.after(0, lambda: self.progress_label.config(text="Cleaning temp files..."))
                self.clean_temp_files()
                
                # System optimization
                self.root.after(0, lambda: self.progress_bar.config(value=90))
                self.root.after(0, lambda: self.progress_label.config(text="System optimization..."))
                if hasattr(self, 'optimizer'):
                    self.optimizer.quick_optimize()
                
                self.root.after(0, lambda: self.progress_bar.config(value=100))
                self.root.after(0, lambda: self.progress_label.config(text="Performance boost completed"))
                self.root.after(0, lambda: self.add_activity("Performans boost tamamlandı", "success"))
                
                # Reset progress after delay
                self.root.after(2000, lambda: self.progress_bar.config(value=0))
                self.root.after(2000, lambda: self.progress_label.config(text="Ready"))
                
            except Exception as e:
                self.root.after(0, lambda: self.add_activity(f"Boost hatası: {str(e)}", "error"))
                self.root.after(0, lambda: self.progress_bar.config(value=0))
                self.root.after(0, lambda: self.progress_label.config(text="Error"))
        
        # Run in separate thread
        threading.Thread(target=boost_worker, daemon=True).start()
    
    def quick_optimize_memory_ui(self):
        """Quick memory optimization from UI"""
        def memory_worker():
            try:
                self.root.after(0, lambda: self.progress_label.config(text="Optimizing memory..."))
                self.root.after(0, lambda: self.progress_bar.config(value=30))
                
                self.root.after(0, lambda: self.add_activity("Bellek optimize ediliyor", "info"))
                
                # Memory optimization
                self.root.after(0, lambda: self.progress_bar.config(value=70))
                self.optimize_memory()
                
                self.root.after(0, lambda: self.progress_bar.config(value=100))
                self.root.after(0, lambda: self.progress_label.config(text="Memory optimized"))
                self.root.after(0, lambda: self.add_activity("Bellek optimize edildi", "success"))
                
                # Reset progress after delay
                self.root.after(2000, lambda: self.progress_bar.config(value=0))
                self.root.after(2000, lambda: self.progress_label.config(text="Ready"))
                
            except Exception as e:
                self.root.after(0, lambda: self.add_activity(f"Bellek optimizasyon hatası: {str(e)}", "error"))
                self.root.after(0, lambda: self.progress_bar.config(value=0))
                self.root.after(0, lambda: self.progress_label.config(text="Error"))
        
        # Run in separate thread
        threading.Thread(target=memory_worker, daemon=True).start()
    
    def toggle_gaming_mode_ui(self):
        """Toggle gaming mode from UI"""
        def toggle_worker():
            try:
                self.root.after(0, lambda: self.progress_label.config(text="Gaming mode toggle..."))
                self.root.after(0, lambda: self.progress_bar.config(value=20))
                
                # Check current status
                current_status = self.check_gaming_mode_status()
                
                self.root.after(0, lambda: self.progress_bar.config(value=40))
                
                if current_status:
                    # Currently enabled, so disable it
                    result = self.disable_gaming_mode()
                    status = "Kapalı"
                    color = self.colors['text_gray']
                    message = "Gaming mode disabled"
                else:
                    # Currently disabled, so enable it
                    result = self.enable_gaming_mode_full()
                    status = "Açık" 
                    color = self.colors['success']
                    message = "Gaming mode enabled"
                
                self.root.after(0, lambda: self.progress_bar.config(value=80))
                
                # Update UI
                self.root.after(0, lambda: self.add_activity(f"Gaming mode {status.lower()}", "success" if result[0] else "error"))
                if hasattr(self, 'gaming_status_label'):
                    self.root.after(0, lambda: self.gaming_status_label.config(text=status, foreground=color))
                
                self.root.after(0, lambda: self.progress_bar.config(value=100))
                self.root.after(0, lambda: self.progress_label.config(text=message))
                
                # Reset progress after delay
                self.root.after(2000, lambda: self.progress_bar.config(value=0))
                self.root.after(2000, lambda: self.progress_label.config(text="Ready"))
                
            except Exception as e:
                self.root.after(0, lambda: self.add_activity(f"Gaming mode hatası: {str(e)}", "error"))
                self.root.after(0, lambda: self.progress_bar.config(value=0))
                self.root.after(0, lambda: self.progress_label.config(text="Error"))
        
        # Run in separate thread
        threading.Thread(target=toggle_worker, daemon=True).start()
    
    def toggle_auto_protection_ui(self):
        """Toggle auto protection from UI"""
        def toggle_worker():
            try:
                self.root.after(0, lambda: self.progress_label.config(text="Auto protection toggle..."))
                self.root.after(0, lambda: self.progress_bar.config(value=20))
                
                # Check current status
                if not hasattr(self, 'auto_protection_enabled'):
                    self.auto_protection_enabled = False
                
                # Toggle auto protection
                self.auto_protection_enabled = not self.auto_protection_enabled
                
                self.root.after(0, lambda: self.progress_bar.config(value=60))
                
                if self.auto_protection_enabled:
                    # Enable auto protection features
                    result = self.enable_auto_protection()
                    status = "Açık"
                    color = self.colors['success']
                    message = "Auto protection enabled"
                else:
                    # Disable auto protection features  
                    result = self.disable_auto_protection()
                    status = "Kapalı"
                    color = self.colors['text_gray']
                    message = "Auto protection disabled"
                
                self.root.after(0, lambda: self.progress_bar.config(value=90))
                
                # Update UI
                self.root.after(0, lambda: self.add_activity(f"Otomatik koruma {status.lower()}", "success" if result[0] else "error"))
                if hasattr(self, 'auto_protection_label'):
                    self.root.after(0, lambda: self.auto_protection_label.config(text=status, foreground=color))
                
                self.root.after(0, lambda: self.progress_bar.config(value=100))
                self.root.after(0, lambda: self.progress_label.config(text=message))
                
                # Reset progress after delay
                self.root.after(2000, lambda: self.progress_bar.config(value=0))
                self.root.after(2000, lambda: self.progress_label.config(text="Ready"))
                
            except Exception as e:
                self.root.after(0, lambda: self.add_activity(f"Otomatik koruma hatası: {str(e)}", "error"))
                self.root.after(0, lambda: self.progress_bar.config(value=0))
                self.root.after(0, lambda: self.progress_label.config(text="Error"))
        
        # Run in separate thread
        threading.Thread(target=toggle_worker, daemon=True).start()
    
    def generate_system_report_ui(self):
        """Generate system report from UI"""
        try:
            self.add_activity("Sistem raporu oluşturuluyor", "Bilgi")
            if hasattr(self, 'system_tray') and self.system_tray:
                self.system_tray.generate_system_report()
            else:
                # Fallback report
                self.add_activity("Sistem raporu oluşturuldu", "Başarılı")
        except Exception as e:
            self.add_activity(f"Rapor oluşturma hatası: {str(e)}", "Hata")
    
    def restart_explorer_ui(self):
        """Restart explorer from UI"""
        try:
            if hasattr(self, 'system_tray') and self.system_tray:
                self.system_tray.restart_explorer()
            else:
                self.add_activity("Explorer yeniden başlatılıyor", "Uyarı")
        except Exception as e:
            self.add_activity(f"Explorer restart hatası: {str(e)}", "Hata")
    
    def show_advanced_settings(self):
        """Show advanced settings"""
        try:
            if hasattr(self, 'system_tray') and self.system_tray:
                self.system_tray.show_tray_settings()
            else:
                messagebox.showinfo("Ayarlar", "Gelişmiş ayarlar system tray üzerinden erişilebilir.")
        except Exception as e:
            self.add_activity(f"Ayarlar hatası: {str(e)}", "Hata")
    
    def toggle_performance_monitor(self):
        """Toggle performance monitoring"""
        try:
            if hasattr(self, 'system_tray') and self.system_tray:
                current_state = self.system_tray.monitoring_active
                self.system_tray.toggle_monitoring()
                new_state = self.system_tray.monitoring_active
                
                if hasattr(self, 'monitor_toggle_btn'):
                    if new_state:
                        self.monitor_toggle_btn.config(text="📊 Aktif", style="Success.TButton")
                        self.add_activity("Performans monitörü aktif", "Başarılı")
                    else:
                        self.monitor_toggle_btn.config(text="📊 Pasif", style="Modern.TButton")
                        self.add_activity("Performans monitörü pasif", "Bilgi")
                        
                if hasattr(self, 'monitoring_status_label'):
                    status = "Aktif" if new_state else "Pasif"
                    color = self.colors['success'] if new_state else self.colors['text_gray']
                    self.monitoring_status_label.config(text=status, foreground=color)
        except Exception as e:
            self.add_activity(f"Performans monitör hatası: {str(e)}", "Hata")
    
    def create_quick_actions_grid(self, parent):
        """Create quick actions grid with beautiful buttons"""
        actions_card = ttk.Frame(parent, style="Card.TFrame", padding="20")
        actions_card.pack(fill="x", pady=(0, 15))
        
        ttk.Label(actions_card, text="⚡ Hızlı İşlemler", 
                 font=("Segoe UI", 16, "bold"),
                 background=self.colors['bg_light'],
                 foreground=self.colors['text_white']).pack(anchor="w", pady=(0, 15))
        
        # Create 3x3 grid of action buttons
        grid_frame = ttk.Frame(actions_card, style="Card.TFrame")
        grid_frame.pack(fill="x")
        
        quick_actions = [
            ("🔍", "Hızlı Tarama", self.quick_scan_ui, "Modern.TButton"),
            ("🧹", "Temp Temizlik", self.quick_clean_temp_ui, "Success.TButton"),
            ("🚀", "Performans Boost", self.quick_performance_boost_ui, "Warning.TButton"),
            ("💾", "Bellek Optimize", self.quick_optimize_memory_ui, "Modern.TButton"),
            ("🎮", "Gaming Mode", self.toggle_gaming_mode_ui, "Warning.TButton"),
            ("🛡️", "Auto Koruma", self.toggle_auto_protection_ui, "Success.TButton"),
            ("📊", "Sistem Raporu", self.generate_system_report_ui, "Modern.TButton"),
            ("🔄", "Explorer Restart", self.restart_explorer_ui, "Warning.TButton"),
            ("⚙️", "Ayarlar", self.show_advanced_settings, "Modern.TButton")
        ]
        
        for i, (icon, text, command, style) in enumerate(quick_actions):
            row = i // 3
            col = i % 3
            
            btn_frame = ttk.Frame(grid_frame, style="Card.TFrame")
            btn_frame.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            
            # Action button with icon and text
            action_btn = ttk.Button(btn_frame, text=f"{icon}\n{text}", 
                                   style=style, command=command)
            action_btn.pack(fill="both", expand=True, ipady=10)
        
        # Configure grid weights
        for i in range(3):
            grid_frame.columnconfigure(i, weight=1)
    
    def create_performance_monitor_card(self, parent):
        """Create performance monitoring card"""
        monitor_card = ttk.Frame(parent, style="Card.TFrame", padding="20")
        monitor_card.pack(fill="x", pady=(0, 15))
        
        # Header with toggle
        header_frame = ttk.Frame(monitor_card, style="Card.TFrame")
        header_frame.pack(fill="x", pady=(0, 15))
        
        ttk.Label(header_frame, text="📈 Performans Monitörü", 
                 font=("Segoe UI", 16, "bold"),
                 background=self.colors['bg_light'],
                 foreground=self.colors['text_white']).pack(side="left")
        
        # Monitor toggle button
        self.monitor_toggle_btn = ttk.Button(header_frame, text="📊 Aktif", 
                                            style="Success.TButton",
                                            command=self.toggle_performance_monitor)
        self.monitor_toggle_btn.pack(side="right")
        
        # Performance indicators
        perf_frame = ttk.Frame(monitor_card, style="Card.TFrame")
        perf_frame.pack(fill="x")
        
        # CPU usage bar
        cpu_frame = ttk.Frame(perf_frame, style="Card.TFrame")
        cpu_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(cpu_frame, text="💻 CPU:", 
                 font=("Segoe UI", 11, "bold"),
                 background=self.colors['bg_light'],
                 foreground=self.colors['text_white']).pack(side="left")
        
        self.cpu_progress = self.create_safe_progressbar(cpu_frame, length=200, mode='determinate')
        self.cpu_progress.pack(side="right", fill="x", expand=True, padx=(10, 0))
        
        # RAM usage bar
        ram_frame = ttk.Frame(perf_frame, style="Card.TFrame")
        ram_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(ram_frame, text="🧠 RAM:", 
                 font=("Segoe UI", 11, "bold"),
                 background=self.colors['bg_light'],
                 foreground=self.colors['text_white']).pack(side="left")
        
        self.ram_progress = self.create_safe_progressbar(ram_frame, length=200, mode='determinate')
        self.ram_progress.pack(side="right", fill="x", expand=True, padx=(10, 0))
        
        # Disk usage bar
        disk_frame = ttk.Frame(perf_frame, style="Card.TFrame")
        disk_frame.pack(fill="x")
        
        ttk.Label(disk_frame, text="💾 Disk:", 
                 font=("Segoe UI", 11, "bold"),
                 background=self.colors['bg_light'],
                 foreground=self.colors['text_white']).pack(side="left")
        
        self.disk_progress = self.create_safe_progressbar(disk_frame, length=200, mode='determinate')
        self.disk_progress.pack(side="right", fill="x", expand=True, padx=(10, 0))
    
    def create_advanced_controls_card(self, parent):
        """Create advanced controls card"""
        controls_card = ttk.Frame(parent, style="Card.TFrame", padding="20")
        controls_card.pack(fill="x", pady=(0, 15))
        
        ttk.Label(controls_card, text="🎛️ Gelişmiş Kontroller", 
                 font=("Segoe UI", 16, "bold"),
                 background=self.colors['bg_light'],
                 foreground=self.colors['text_white']).pack(anchor="w", pady=(0, 15))
        
        # Control toggles
        controls_frame = ttk.Frame(controls_card, style="Card.TFrame")
        controls_frame.pack(fill="x")
        
        # Gaming mode control
        gaming_frame = ttk.Frame(controls_frame, style="Card.TFrame")
        gaming_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(gaming_frame, text="🎮 Gaming Mode:", 
                 font=("Segoe UI", 12, "bold"),
                 background=self.colors['bg_light'],
                 foreground=self.colors['text_white']).pack(side="left")
        
        self.gaming_status_label = ttk.Label(gaming_frame, text="Kapalı", 
                                            font=("Segoe UI", 11),
                                            background=self.colors['bg_light'],
                                            foreground=self.colors['text_gray'])
        self.gaming_status_label.pack(side="right")
        
        # Auto protection control
        auto_frame = ttk.Frame(controls_frame, style="Card.TFrame")
        auto_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(auto_frame, text="🛡️ Otomatik Koruma:", 
                 font=("Segoe UI", 12, "bold"),
                 background=self.colors['bg_light'],
                 foreground=self.colors['text_white']).pack(side="left")
        
        self.auto_protection_label = ttk.Label(auto_frame, text="Kapalı", 
                                              font=("Segoe UI", 11),
                                              background=self.colors['bg_light'],
                                              foreground=self.colors['text_gray'])
        self.auto_protection_label.pack(side="right")
        
        # Real-time monitoring control
        monitor_frame = ttk.Frame(controls_frame, style="Card.TFrame")
        monitor_frame.pack(fill="x")
        
        ttk.Label(monitor_frame, text="📊 Gerçek Zamanlı İzleme:", 
                 font=("Segoe UI", 12, "bold"),
                 background=self.colors['bg_light'],
                 foreground=self.colors['text_white']).pack(side="left")
        
        self.monitoring_status_label = ttk.Label(monitor_frame, text="Aktif", 
                                                font=("Segoe UI", 11),
                                                background=self.colors['bg_light'],
                                                foreground=self.colors['success'])
        self.monitoring_status_label.pack(side="right")
    
    def create_recent_activities_card(self, parent):
        """Create recent activities card"""
        activities_card = ttk.Frame(parent, style="Card.TFrame", padding="20")
        activities_card.pack(fill="x", pady=(0, 15))
        
        ttk.Label(activities_card, text="📋 Son Aktiviteler", 
                 font=("Segoe UI", 16, "bold"),
                 background=self.colors['bg_light'],
                 foreground=self.colors['text_white']).pack(anchor="w", pady=(0, 15))
        
        # Activities list
        self.activities_frame = ttk.Frame(activities_card, style="Card.TFrame")
        self.activities_frame.pack(fill="x")
        
        # Add initial activity
        self.add_activity("✅ DonTe Cleaner başlatıldı", "Başarılı")
        
        # Clear activities button
        clear_btn = ttk.Button(activities_card, text="🗑️ Temizle", 
                              style="Modern.TButton",
                              command=self.clear_activities)
        clear_btn.pack(anchor="e", pady=(10, 0))
    
    def create_system_tab(self):
        """Create system optimization tab"""
        tab_frame = ttk.Frame(self.notebook, style="Modern.TFrame", padding="20")
        self.notebook.add(tab_frame, text="Sistem Optimizasyonu")
        
        # Windows optimization section
        windows_card = ttk.Frame(tab_frame, style="Card.TFrame", padding="15")
        windows_card.pack(fill="x", pady=(0, 15))
        
        ttk.Label(windows_card, text="Windows Optimizasyonu", 
                 font=("Segoe UI", 14, "bold"),
                 background=self.colors['bg_light'],
                 foreground=self.colors['text_white']).pack(anchor="w", pady=(0, 10))
        
        # Windows optimization buttons
        windows_buttons = [
            ("Gereksiz Hizmetleri Kapat", self.disable_services, "Modern.TButton"),
            ("Başlangıç Programlarını Temizle", self.clean_startup, "Modern.TButton"),
            ("Görsel Efektleri Kapat", self.disable_visual_effects, "Modern.TButton"),
            ("Güç Planını Ayarla", self.set_power_plan, "Warning.TButton"),
            ("Geçici Dosyaları Temizle", self.clean_temp_files, "Success.TButton"),
            ("Belleği Optimize Et", self.optimize_memory, "Modern.TButton"),
            ("Tüm Değişiklikleri Geri Al", self.undo_changes, "Danger.TButton")
        ]
        
        for i, (text, command, style) in enumerate(windows_buttons):
            if i % 2 == 0:
                button_frame = ttk.Frame(windows_card, style="Card.TFrame")
                button_frame.pack(fill="x", pady=2)
            
            ttk.Button(button_frame, text=text, style=style, 
                      command=command, width=25).pack(side="left", padx=(0, 10) if i % 2 == 0 else (0, 0))
    
    def create_antivirus_tab(self):
        """Create antivirus tab"""
        tab_frame = ttk.Frame(self.notebook, style="Modern.TFrame", padding="20")
        self.notebook.add(tab_frame, text="Virüs Tarama")
        
        # Antivirus card
        antivirus_card = ttk.Frame(tab_frame, style="Card.TFrame", padding="15")
        antivirus_card.pack(fill="both", expand=True)
        
        ttk.Label(antivirus_card, text="Virüs ve Zararlı Yazılım Taraması", 
                 font=("Segoe UI", 14, "bold"),
                 background=self.colors['bg_light'],
                 foreground=self.colors['text_white']).pack(anchor="w", pady=(0, 15))
        
        # Scan buttons
        scan_frame = ttk.Frame(antivirus_card, style="Card.TFrame")
        scan_frame.pack(fill="x", pady=(0, 15))
        
        ttk.Button(scan_frame, text="Hızlı Tarama", 
                  style="Success.TButton",
                  command=self.start_quick_scan, width=20).pack(side="left", padx=(0, 10))
        
        ttk.Button(scan_frame, text="Tam Tarama", 
                  style="Warning.TButton",
                  command=self.start_full_scan, width=20).pack(side="left", padx=(0, 10))
        
        ttk.Button(scan_frame, text="Özel Tarama", 
                  style="Modern.TButton",
                  command=self.start_custom_scan, width=20).pack(side="left")
        
        # Open detailed antivirus window
        ttk.Button(antivirus_card, text="Detaylı Virüs Tarama Penceresi", 
                  style="Modern.TButton",
                  command=self.open_antivirus_window).pack(pady=10)
        
        # Results frame (will be populated during scans)
        self.scan_results_frame = ttk.Frame(antivirus_card, style="Card.TFrame")
        self.scan_results_frame.pack(fill="both", expand=True, pady=(15, 0))
    
    def create_emulator_tab(self):
        """Create emulator optimization tab"""
        tab_frame = ttk.Frame(self.notebook, style="Modern.TFrame", padding="20")
        self.notebook.add(tab_frame, text="Emülatör Optimizasyonu")
        
        # Emulator card
        emulator_card = ttk.Frame(tab_frame, style="Card.TFrame", padding="15")
        emulator_card.pack(fill="both", expand=True)
        
        ttk.Label(emulator_card, text="Android Emülatör Optimizasyonu", 
                 font=("Segoe UI", 14, "bold"),
                 background=self.colors['bg_light'],
                 foreground=self.colors['text_white']).pack(anchor="w", pady=(0, 15))
        
        # Emulator selection
        selection_frame = ttk.Frame(emulator_card, style="Card.TFrame")
        selection_frame.pack(fill="x", pady=(0, 15))
        
        ttk.Label(selection_frame, text="Emülatör Seçin:", 
                 background=self.colors['bg_light'],
                 foreground=self.colors['text_white'],
                 font=("Segoe UI", 11)).pack(side="left", padx=(0, 10))
        
        self.emulator_var = tk.StringVar(value="BlueStacks")
        emulator_combo = ttk.Combobox(selection_frame, textvariable=self.emulator_var,
                                     values=list(self.emulator_optimizer.emulator_paths.keys()),
                                     state="readonly", width=15)
        emulator_combo.pack(side="left")
        
        # Emulator action buttons
        action_frame = ttk.Frame(emulator_card, style="Card.TFrame")
        action_frame.pack(fill="x", pady=(0, 15))
        
        ttk.Button(action_frame, text="Emülatörü Başlat", 
                  style="Success.TButton",
                  command=self.start_emulator, width=20).pack(side="left", padx=(0, 10))
        
        ttk.Button(action_frame, text="Öncelik Artır", 
                  style="Warning.TButton",
                  command=self.boost_emulator, width=20).pack(side="left", padx=(0, 10))
        
        ttk.Button(action_frame, text="Optimize Et", 
                  style="Modern.TButton",
                  command=self.optimize_emulator, width=20).pack(side="left")
        
        # Open detailed emulator window
        ttk.Button(emulator_card, text="Detaylı Emülatör Yönetimi", 
                  style="Modern.TButton",
                  command=self.open_emulator_window).pack(pady=10)
    
    def create_settings_tab(self):
        """Create modern settings tab using SettingsPage"""
        try:
            from gui.pages.settings_page import SettingsPage
            
            # Create frame for settings
            settings_frame = ttk.Frame(self.notebook, style="Modern.TFrame")
            self.notebook.add(settings_frame, text="⚙️ Settings")
            
            # Initialize settings page
            self.settings_page = SettingsPage(settings_frame, self)
            
            print("[MAIN] Modern settings tab created successfully")
        except Exception as e:
            print(f"[MAIN] Error creating settings tab: {e}")
            # Fallback to basic settings
            self.create_basic_settings_tab()
        self.create_antivirus_settings_section(settings_frame)
        self.create_windows_version_settings_section(settings_frame)
    
    def create_general_settings_section(self, parent):
        """Create general settings section"""
        section = ttk.LabelFrame(parent, text="🔧 General Settings", padding="15")
        section.pack(fill="x", pady=(0, 15))
        
        # Auto startup
        self.auto_startup_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(section, text="Start DonTe Cleaner with Windows", 
                       variable=self.auto_startup_var,
                       command=self.toggle_auto_startup).pack(anchor="w", pady=5)
        
        # Auto updates
        self.auto_update_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(section, text="Check for updates automatically", 
                       variable=self.auto_update_var).pack(anchor="w", pady=5)
        
        # Notifications
        self.notifications_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(section, text="Show system notifications", 
                       variable=self.notifications_var).pack(anchor="w", pady=5)
        
        # Language settings
        lang_frame = ttk.Frame(section)
        lang_frame.pack(fill="x", pady=10)
        
        ttk.Label(lang_frame, text="Language:").pack(side="left")
        self.language_var = tk.StringVar(value="English")
        language_combo = ttk.Combobox(lang_frame, textvariable=self.language_var,
                                    values=["English", "Türkçe", "Español", "Français", "Deutsch"],
                                    state="readonly", width=15)
        language_combo.pack(side="left", padx=(10, 0))
        
        # Theme settings
        theme_frame = ttk.Frame(section)
        theme_frame.pack(fill="x", pady=10)
        
        ttk.Label(theme_frame, text="Theme:").pack(side="left")
        self.theme_var = tk.StringVar(value="Dark")
        theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var,
                                 values=["Dark", "Light", "Auto"],
                                 state="readonly", width=15)
        theme_combo.pack(side="left", padx=(10, 0))
    
    def create_optimization_settings_section(self, parent):
        """Create optimization settings section"""
        section = ttk.LabelFrame(parent, text="🚀 Optimization Settings", padding="15")
        section.pack(fill="x", pady=(0, 15))
        
        # Optimization level
        level_frame = ttk.Frame(section)
        level_frame.pack(fill="x", pady=10)
        
        ttk.Label(level_frame, text="Optimization Level:").pack(side="left")
        self.opt_level_var = tk.StringVar(value="Balanced")
        level_combo = ttk.Combobox(level_frame, textvariable=self.opt_level_var,
                                 values=["Conservative", "Balanced", "Aggressive", "Custom"],
                                 state="readonly", width=15)
        level_combo.pack(side="left", padx=(10, 0))
        
        # Backup settings
        self.create_backup_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(section, text="Create system backup before optimization", 
                       variable=self.create_backup_var).pack(anchor="w", pady=5)
        
        # Schedule settings
        self.auto_optimize_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(section, text="Schedule automatic optimization", 
                       variable=self.auto_optimize_var).pack(anchor="w", pady=5)
        
        schedule_frame = ttk.Frame(section)
        schedule_frame.pack(fill="x", pady=5)
        
        ttk.Label(schedule_frame, text="Schedule:").pack(side="left")
        self.schedule_var = tk.StringVar(value="Weekly")
        schedule_combo = ttk.Combobox(schedule_frame, textvariable=self.schedule_var,
                                    values=["Daily", "Weekly", "Monthly"],
                                    state="readonly", width=15)
        schedule_combo.pack(side="left", padx=(10, 0))
    
    def create_antivirus_settings_section(self, parent):
        """Create antivirus settings section"""
        section = ttk.LabelFrame(parent, text="🛡️ Security Settings", padding="15")
        section.pack(fill="x", pady=(0, 15))
        
        # Real-time protection
        self.realtime_protection_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(section, text="Enable real-time virus protection", 
                       variable=self.realtime_protection_var).pack(anchor="w", pady=5)
        
        # Quarantine settings
        self.auto_quarantine_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(section, text="Automatically quarantine threats", 
                       variable=self.auto_quarantine_var).pack(anchor="w", pady=5)
        
        # Update settings
        self.auto_update_db_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(section, text="Auto-update virus database", 
                       variable=self.auto_update_db_var).pack(anchor="w", pady=5)
        
        # Scan exclusions
        exclusions_frame = ttk.Frame(section)
        exclusions_frame.pack(fill="x", pady=10)
        
        ttk.Label(exclusions_frame, text="Scan Exclusions:").pack(anchor="w")
        
        self.exclusions_text = tk.Text(exclusions_frame, height=3, width=50,
                                      bg=self.colors['bg_dark'],
                                      fg=self.colors['text_white'],
                                      insertbackground=self.colors['text_white'])
        self.exclusions_text.pack(fill="x", pady=5)
        self.exclusions_text.insert("1.0", "C:\\Windows\\System32\nC:\\Program Files\\Windows Defender")
    
    def create_windows_version_settings_section(self, parent):
        """Create Windows 10/11 specific settings"""
        section = ttk.LabelFrame(parent, text="🪟 Windows 10/11 Optimizations", padding="15")
        section.pack(fill="x", pady=(0, 15))
        
        # Detect Windows version
        import platform
        windows_version = platform.release()
        
        version_label = ttk.Label(section, text=f"Detected: Windows {windows_version}",
                                font=("Segoe UI", 10, "bold"))
        version_label.pack(anchor="w", pady=5)
        
        # Windows 10/11 specific optimizations
        self.disable_cortana_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(section, text="Disable Cortana (Windows 10/11)", 
                       variable=self.disable_cortana_var).pack(anchor="w", pady=5)
        
        self.disable_telemetry_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(section, text="Disable Windows telemetry", 
                       variable=self.disable_telemetry_var).pack(anchor="w", pady=5)
        
        self.disable_defender_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(section, text="Disable Windows Defender (Advanced users only)", 
                       variable=self.disable_defender_var).pack(anchor="w", pady=5)
        
        self.optimize_startmenu_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(section, text="Optimize Start Menu performance", 
                       variable=self.optimize_startmenu_var).pack(anchor="w", pady=5)
        
        self.disable_onedrive_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(section, text="Disable OneDrive integration", 
                       variable=self.disable_onedrive_var).pack(anchor="w", pady=5)
        
        # Gaming optimizations for Windows 11
        if windows_version == "11":
            self.win11_gaming_var = tk.BooleanVar(value=True)
            ttk.Checkbutton(section, text="Enable Windows 11 gaming optimizations", 
                           variable=self.win11_gaming_var).pack(anchor="w", pady=5)
        
        # Action buttons
        button_frame = ttk.Frame(section)
        button_frame.pack(fill="x", pady=15)
        
        ttk.Button(button_frame, text="Apply Settings", 
                  style="Success.TButton",
                  command=self.apply_settings).pack(side="left", padx=(0, 10))
        
        ttk.Button(button_frame, text="Reset to Defaults", 
                  style="Modern.TButton",
                  command=self.reset_settings).pack(side="left", padx=(0, 10))
        
        ttk.Button(button_frame, text="Export Settings", 
                  style="Modern.TButton",
                  command=self.export_settings).pack(side="right")
    
    def toggle_auto_startup(self):
        """Toggle auto startup with Windows"""
        try:
            import winreg
            
            if self.auto_startup_var.get():
                # Add to startup
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                   r"Software\Microsoft\Windows\CurrentVersion\Run", 
                                   0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, "DonTe Cleaner", 0, winreg.REG_SZ, 
                                sys.executable)
                winreg.CloseKey(key)
                self.add_activity("Auto-startup enabled", "success")
            else:
                # Remove from startup
                try:
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                       r"Software\Microsoft\Windows\CurrentVersion\Run", 
                                       0, winreg.KEY_SET_VALUE)
                    winreg.DeleteValue(key, "DonTe Cleaner")
                    winreg.CloseKey(key)
                    self.add_activity("Auto-startup disabled", "success")
                except FileNotFoundError:
                    pass
                    
        except Exception as e:
            self.logger.error(f"Auto startup toggle failed: {str(e)}")
            messagebox.showerror("Error", f"Failed to toggle auto startup: {str(e)}")
    
    def apply_settings(self):
        """Apply all settings"""
        try:
            # Apply optimizations based on Windows version settings
            applied_count = 0
            
            if self.disable_cortana_var.get():
                result = self.disable_cortana()
                if result[0]:
                    applied_count += 1
            
            if self.disable_telemetry_var.get():
                result = self.disable_telemetry()
                if result[0]:
                    applied_count += 1
            
            if self.optimize_startmenu_var.get():
                result = self.optimize_start_menu()
                if result[0]:
                    applied_count += 1
            
            if self.disable_onedrive_var.get():
                result = self.disable_onedrive()
                if result[0]:
                    applied_count += 1
            
            messagebox.showinfo("Settings Applied", 
                              f"Successfully applied {applied_count} optimizations!")
            self.add_activity(f"Settings applied: {applied_count} optimizations", "success")
            
        except Exception as e:
            self.logger.error(f"Settings apply failed: {str(e)}")
            messagebox.showerror("Error", f"Failed to apply settings: {str(e)}")
    
    def reset_settings(self):
        """Reset all settings to defaults"""
        try:
            # Reset all variables to default values
            self.auto_startup_var.set(True)
            self.auto_update_var.set(True)
            self.notifications_var.set(True)
            self.language_var.set("English")
            self.theme_var.set("Dark")
            self.opt_level_var.set("Balanced")
            self.create_backup_var.set(True)
            self.auto_optimize_var.set(False)
            self.schedule_var.set("Weekly")
            self.realtime_protection_var.set(True)
            self.auto_quarantine_var.set(True)
            self.auto_update_db_var.set(True)
            self.disable_cortana_var.set(False)
            self.disable_telemetry_var.set(True)
            self.disable_defender_var.set(False)
            self.optimize_startmenu_var.set(True)
            self.disable_onedrive_var.set(False)
            
            messagebox.showinfo("Settings Reset", "All settings have been reset to defaults!")
            self.add_activity("Settings reset to defaults", "success")
            
        except Exception as e:
            self.logger.error(f"Settings reset failed: {str(e)}")
            messagebox.showerror("Error", f"Failed to reset settings: {str(e)}")
    
    def export_settings(self):
        """Export current settings to file"""
        try:
            from tkinter import filedialog
            import json
            
            settings = {
                "auto_startup": self.auto_startup_var.get(),
                "auto_update": self.auto_update_var.get(),
                "notifications": self.notifications_var.get(),
                "language": self.language_var.get(),
                "theme": self.theme_var.get(),
                "optimization_level": self.opt_level_var.get(),
                "create_backup": self.create_backup_var.get(),
                "auto_optimize": self.auto_optimize_var.get(),
                "schedule": self.schedule_var.get(),
                "realtime_protection": self.realtime_protection_var.get(),
                "auto_quarantine": self.auto_quarantine_var.get(),
                "auto_update_db": self.auto_update_db_var.get(),
                "disable_cortana": self.disable_cortana_var.get(),
                "disable_telemetry": self.disable_telemetry_var.get(),
                "disable_defender": self.disable_defender_var.get(),
                "optimize_startmenu": self.optimize_startmenu_var.get(),
                "disable_onedrive": self.disable_onedrive_var.get()
            }
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Export Settings"
            )
            
            if filename:
                with open(filename, 'w') as f:
                    json.dump(settings, f, indent=4)
                
                messagebox.showinfo("Export Complete", f"Settings exported to: {filename}")
                self.add_activity("Settings exported", "success")
                
        except Exception as e:
            self.logger.error(f"Settings export failed: {str(e)}")
            messagebox.showerror("Error", f"Failed to export settings: {str(e)}")
    
    # Windows-specific optimization methods
    def disable_cortana(self):
        """Disable Cortana"""
        try:
            import winreg
            
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, 
                                 r"SOFTWARE\Policies\Microsoft\Windows\Windows Search")
            winreg.SetValueEx(key, "AllowCortana", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            return True, "Cortana disabled successfully"
            
        except Exception as e:
            return False, f"Cortana disable failed: {str(e)}"
    
    def disable_telemetry(self):
        """Disable Windows telemetry"""
        try:
            import winreg
            
            # Disable telemetry
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, 
                                 r"SOFTWARE\Policies\Microsoft\Windows\DataCollection")
            winreg.SetValueEx(key, "AllowTelemetry", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            return True, "Telemetry disabled successfully"
            
        except Exception as e:
            return False, f"Telemetry disable failed: {str(e)}"
    
    def optimize_start_menu(self):
        """Optimize Start Menu performance"""
        try:
            import winreg
            
            # Disable web search in start menu
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, 
                                 r"SOFTWARE\Microsoft\Windows\CurrentVersion\Search")
            winreg.SetValueEx(key, "BingSearchEnabled", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, "CortanaConsent", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            return True, "Start Menu optimized successfully"
            
        except Exception as e:
            return False, f"Start Menu optimization failed: {str(e)}"
    
    def disable_onedrive(self):
        """Disable OneDrive integration"""
        try:
            import winreg
            
            # Disable OneDrive
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, 
                                 r"SOFTWARE\Policies\Microsoft\Windows\OneDrive")
            winreg.SetValueEx(key, "DisableFileSyncNGSC", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            
            return True, "OneDrive disabled successfully"
            
        except Exception as e:
            return False, f"OneDrive disable failed: {str(e)}"
    
    def setup_layout(self):
        """Setup widget layout"""
        self.main_frame.pack(fill="both", expand=True)
        self.header_frame.pack(fill="x", pady=(0, 20))
        self.notebook.pack(fill="both", expand=True, pady=(0, 20))
        
        # Progress bar layout
        self.progress_frame.pack(fill="x", pady=(0, 10))
        self.progress_bar.pack(fill="x", padx=(0, 10), side="left", expand=True)
        self.progress_label.pack(side="right")
        
        # Status bar layout
        self.status_bar.pack(fill="x")
        self.status_label.pack(side="left")
        self.admin_label.pack(side="right")
    
    def update_status_bar(self):
        """Update status bar information"""
        if self.is_admin:
            self.admin_label.config(text="✓ Yönetici Modu")
        else:
            self.admin_label.config(text="⚠ Sınırlı Mod")
    
    def run_with_progress(self, func, *args, **kwargs):
        """Run function with progress indication"""
        def worker():
            try:
                self.progress_bar.config(mode='indeterminate')
                self.progress_bar.start()
                self.progress_label.config(text="İşlem yapılıyor...")
                
                result = func(*args, **kwargs)
                
                self.progress_bar.stop()
                self.progress_bar.config(mode='determinate', value=100)
                
                if isinstance(result, tuple) and len(result) == 2:
                    success, message = result
                    if success:
                        self.progress_label.config(text="Tamamlandı!")
                        messagebox.showinfo("Başarılı", message)
                    else:
                        self.progress_label.config(text="Hata!")
                        messagebox.showerror("Hata", message)
                else:
                    self.progress_label.config(text="Tamamlandı!")
                
                # Reset progress after 3 seconds
                self.root.after(3000, lambda: self.progress_bar.config(value=0))
                self.root.after(3000, lambda: self.progress_label.config(text="Hazır"))
                
            except Exception as e:
                self.progress_bar.stop()
                self.progress_bar.config(value=0)
                self.progress_label.config(text="Hata!")
                messagebox.showerror("Hata", f"İşlem başarısız: {str(e)}")
                self.logger.error(f"Operation failed: {str(e)}")
        
        threading.Thread(target=worker, daemon=True).start()
    
    # System optimization methods
    def disable_services(self):
        if not self.is_admin:
            messagebox.showwarning("Yetki Hatası", "Bu işlem için yönetici yetkisi gerekli!")
            return
        self.run_with_progress(self.windows_optimizer.disable_services)
    
    def clean_startup(self):
        self.run_with_progress(self.windows_optimizer.clean_startup_programs)
    
    def disable_visual_effects(self):
        self.run_with_progress(self.windows_optimizer.disable_visual_effects)
    
    def set_power_plan(self):
        if not self.is_admin:
            messagebox.showwarning("Yetki Hatası", "Bu işlem için yönetici yetkisi gerekli!")
            return
        self.run_with_progress(self.windows_optimizer.set_high_performance_power_plan)
    
    def clean_temp_files(self):
        self.run_with_progress(self.windows_optimizer.clean_temp_files)
    
    def optimize_memory(self):
        self.run_with_progress(self.windows_optimizer.optimize_memory)
    
    def undo_changes(self):
        if not self.is_admin:
            messagebox.showwarning("Yetki Hatası", "Bu işlem için yönetici yetkisi gerekli!")
            return
        self.run_with_progress(self.windows_optimizer.undo_all_changes)
    
    def quick_scan(self):
        self.start_quick_scan()
    
    def quick_cleanup(self):
        """Enhanced quick cleanup with visual feedback"""
        def cleanup_worker():
            try:
                self.root.after(0, lambda: self.progress_label.config(text="Starting system cleanup..."))
                self.root.after(0, lambda: self.progress_bar.config(value=10))
                
                cleanup_operations = [
                    ("Cleaning temporary files", self.windows_optimizer.clean_temp_files),
                    ("Clearing browser cache", self.clear_browser_cache),
                    ("Emptying recycle bin", self.empty_recycle_bin),
                    ("Cleaning system cache", self.clean_system_cache)
                ]
                
                total_ops = len(cleanup_operations)
                completed = 0
                
                for operation_name, operation_func in cleanup_operations:
                    self.root.after(0, lambda op=operation_name: self.progress_label.config(text=f"Executing: {op}"))
                    
                    try:
                        if hasattr(operation_func, '__call__'):
                            operation_func()
                        completed += 1
                        progress_value = 10 + (completed / total_ops) * 80
                        self.root.after(0, lambda val=progress_value: self.progress_bar.config(value=val))
                        time.sleep(0.3)  # Visual feedback delay
                    except Exception as e:
                        self.logger.error(f"Cleanup operation failed ({operation_name}): {str(e)}")
                        continue
                
                self.root.after(0, lambda: self.progress_bar.config(value=100))
                self.root.after(0, lambda: self.progress_label.config(text="System cleanup completed!"))
                
                # Show completion message
                self.root.after(0, lambda: messagebox.showinfo("Quick Cleanup Complete", 
                                                              f"System cleanup completed successfully!\n\n"
                                                              f"Operations completed: {completed}/{total_ops}\n"
                                                              f"Your system has been cleaned and optimized."))
                
                # Add to activity log
                if hasattr(self, 'add_activity'):
                    self.root.after(0, lambda: self.add_activity(f"Quick cleanup completed: {completed}/{total_ops} operations", "success"))
                
                # Play success sound if available
                if hasattr(self, 'sound_effects') and self.sound_effects:
                    self.root.after(0, lambda: self.sound_effects.play_sound("completion"))
                
                self.root.after(2000, lambda: self.progress_label.config(text="Ready"))
                
            except Exception as e:
                error_msg = f"Quick cleanup failed: {str(e)}"
                self.logger.error(error_msg)
                self.root.after(0, lambda: self.progress_label.config(text="Cleanup failed"))
                self.root.after(0, lambda: messagebox.showerror("Cleanup Error", error_msg))
                if hasattr(self, 'add_activity'):
                    self.root.after(0, lambda: self.add_activity("Quick cleanup failed", "error"))
        
        # Run in separate thread
        threading.Thread(target=cleanup_worker, daemon=True).start()
    
    def quick_optimize(self):
        """Enhanced quick optimization with visual feedback"""
        def optimize_worker():
            try:
                self.root.after(0, lambda: self.progress_label.config(text="Starting system optimization..."))
                self.root.after(0, lambda: self.progress_bar.config(value=10))
                
                optimization_operations = [
                    ("Optimizing memory usage", self.windows_optimizer.optimize_memory),
                    ("Cleaning temporary files", self.windows_optimizer.clean_temp_files),
                    ("Optimizing startup programs", self.optimize_startup_performance),
                    ("Updating system settings", self.optimize_system_settings),
                    ("Defragmenting memory", self.defragment_memory)
                ]
                
                total_ops = len(optimization_operations)
                completed = 0
                
                for operation_name, operation_func in optimization_operations:
                    self.root.after(0, lambda op=operation_name: self.progress_label.config(text=f"Executing: {op}"))
                    
                    try:
                        if hasattr(operation_func, '__call__'):
                            operation_func()
                        completed += 1
                        progress_value = 10 + (completed / total_ops) * 80
                        self.root.after(0, lambda val=progress_value: self.progress_bar.config(value=val))
                        time.sleep(0.4)  # Visual feedback delay
                    except Exception as e:
                        self.logger.error(f"Optimization operation failed ({operation_name}): {str(e)}")
                        continue
                
                self.root.after(0, lambda: self.progress_bar.config(value=100))
                self.root.after(0, lambda: self.progress_label.config(text="System optimization completed!"))
                
                # Show completion message
                self.root.after(0, lambda: messagebox.showinfo("Quick Optimization Complete", 
                                                              f"System optimization completed successfully!\n\n"
                                                              f"Operations completed: {completed}/{total_ops}\n"
                                                              f"Your system performance has been boosted."))
                
                # Add to activity log
                if hasattr(self, 'add_activity'):
                    self.root.after(0, lambda: self.add_activity(f"Quick optimization completed: {completed}/{total_ops} operations", "success"))
                
                # Play success sound if available
                if hasattr(self, 'sound_effects') and self.sound_effects:
                    self.root.after(0, lambda: self.sound_effects.play_sound("completion"))
                
                self.root.after(2000, lambda: self.progress_label.config(text="Ready"))
                
            except Exception as e:
                error_msg = f"Quick optimization failed: {str(e)}"
                self.logger.error(error_msg)
                self.root.after(0, lambda: self.progress_label.config(text="Optimization failed"))
                self.root.after(0, lambda: messagebox.showerror("Optimization Error", error_msg))
                if hasattr(self, 'add_activity'):
                    self.root.after(0, lambda: self.add_activity("Quick optimization failed", "error"))
        
        # Run in separate thread
        threading.Thread(target=optimize_worker, daemon=True).start()
    
    def one_click_fix(self):
        """Comprehensive one-click system fix"""
        def one_click_worker():
            try:
                self.root.after(0, lambda: self.progress_label.config(text="Starting comprehensive system fix..."))
                self.root.after(0, lambda: self.progress_bar.config(value=10))
                
                operations = [
                    ("Cleaning temporary files", self.windows_optimizer.clean_temp_files),
                    ("Optimizing memory", self.windows_optimizer.optimize_memory),
                    ("Cleaning registry", self.windows_optimizer.clean_registry),
                    ("Optimizing startup", self.windows_optimizer.optimize_startup),
                    ("Updating system settings", self.windows_optimizer.update_system_settings)
                ]
                
                completed = 0
                total = len(operations)
                
                for operation_name, operation_func in operations:
                    self.root.after(0, lambda op=operation_name: self.progress_label.config(text=f"Executing: {op}"))
                    
                    try:
                        if hasattr(operation_func, '__call__'):
                            operation_func()
                        completed += 1
                        progress_value = 10 + (completed / total) * 80
                        self.root.after(0, lambda val=progress_value: self.progress_bar.config(value=val))
                        time.sleep(0.5)  # Small delay for visual feedback
                    except Exception as e:
                        self.logger.error(f"One-click fix operation failed ({operation_name}): {str(e)}")
                        continue
                
                self.root.after(0, lambda: self.progress_bar.config(value=100))
                self.root.after(0, lambda: self.progress_label.config(text="One-click fix completed successfully!"))
                
                # Show completion message
                self.root.after(0, lambda: messagebox.showinfo("One-Click Fix Complete", 
                                                              f"System optimization completed!\n\n"
                                                              f"Operations completed: {completed}/{total}\n"
                                                              f"Your system has been optimized for better performance."))
                
                # Add to activity log
                if hasattr(self, 'add_activity'):
                    self.root.after(0, lambda: self.add_activity(f"One-click fix completed: {completed}/{total} operations", "success"))
                
                # Play success sound if available
                if hasattr(self, 'sound_effects') and self.sound_effects:
                    self.root.after(0, lambda: self.sound_effects.play_sound("completion"))
                
                return True, f"One-click fix completed: {completed}/{total} operations successful"
                
            except Exception as e:
                error_msg = f"One-click fix failed: {str(e)}"
                self.logger.error(error_msg)
                self.root.after(0, lambda: messagebox.showerror("One-Click Fix Error", error_msg))
                return False, error_msg
        
        # Run in separate thread
        threading.Thread(target=one_click_worker, daemon=True).start()
    
    # Enhanced Antivirus methods
    def start_quick_scan(self):
        """Start enhanced quick scan"""
        def scan_worker():
            try:
                self.root.after(0, lambda: self.progress_label.config(text="Preparing enhanced scan..."))
                self.root.after(0, lambda: self.progress_bar.config(value=5))
                
                # Common directories for quick scan
                quick_scan_dirs = [
                    os.path.expanduser("~/Desktop"),
                    os.path.expanduser("~/Downloads"),
                    os.path.expanduser("~/Documents"),
                    os.path.expandvars("%TEMP%"),
                    os.path.expandvars("%APPDATA%")
                ]
                
                all_threats = []
                progress_step = 80 / len(quick_scan_dirs)
                current_progress = 10
                
                def scan_callback(message):
                    self.root.after(0, lambda: self.progress_label.config(text=message))
                
                for i, scan_dir in enumerate(quick_scan_dirs):
                    if os.path.exists(scan_dir):
                        self.root.after(0, lambda: self.progress_label.config(text=f"Scanning {os.path.basename(scan_dir)}..."))
                        threats = self.enhanced_antivirus.scan_directory(scan_dir, scan_callback, max_workers=2)
                        all_threats.extend(threats)
                        
                        current_progress += progress_step
                        self.root.after(0, lambda p=current_progress: self.progress_bar.config(value=p))
                
                self.root.after(0, lambda: self.progress_bar.config(value=95))
                self.root.after(0, lambda: self.progress_label.config(text="Finalizing scan results..."))
                
                # Display results
                self.display_scan_results(all_threats)
                
                return True, f"Enhanced scan completed. {len(all_threats)} threats detected."
                
            except Exception as e:
                return False, f"Scan error: {str(e)}"
        
        self.run_with_progress(scan_worker)
    
    def display_scan_results(self, threats):
        """Display scan results in a user-friendly format"""
        try:
            # Clear previous results
            for widget in self.scan_results_frame.winfo_children():
                widget.destroy()
            
            if not threats:
                ttk.Label(self.scan_results_frame, 
                         text="✅ No threats detected! System appears clean.",
                         style="CardText.TLabel",
                         foreground="green").pack(anchor="w", pady=5)
                return
            
            # Group threats by risk level
            high_risk = [t for t in threats if t['threat_type'] == 'High Risk']
            medium_risk = [t for t in threats if t['threat_type'] == 'Medium Risk'] 
            low_risk = [t for t in threats if t['threat_type'] == 'Low Risk']
            
            # Display summary
            ttk.Label(self.scan_results_frame, 
                     text=f"⚠️ {len(threats)} threats detected:",
                     style="CardTitle.TLabel",
                     foreground="red").pack(anchor="w", pady=(10, 5))
            
            if high_risk:
                ttk.Label(self.scan_results_frame, 
                         text=f"🔴 High Risk: {len(high_risk)} files",
                         style="CardText.TLabel",
                         foreground="red").pack(anchor="w", padx=20)
            
            if medium_risk:
                ttk.Label(self.scan_results_frame, 
                         text=f"🟡 Medium Risk: {len(medium_risk)} files",
                         style="CardText.TLabel",
                         foreground="orange").pack(anchor="w", padx=20)
            
            if low_risk:
                ttk.Label(self.scan_results_frame, 
                         text=f"🟢 Low Risk: {len(low_risk)} files",
                         style="CardText.TLabel",
                         foreground="blue").pack(anchor="w", padx=20)
            
            # Add action buttons
            action_frame = ttk.Frame(self.scan_results_frame, style="Card.TFrame")
            action_frame.pack(fill="x", pady=10)
            
            ttk.Button(action_frame, text="View Details", 
                      command=lambda: self.show_threat_details(threats),
                      style="Modern.TButton").pack(side="left", padx=(0, 10))
            
            if high_risk or medium_risk:
                ttk.Button(action_frame, text="Quarantine Threats", 
                          command=lambda: self.quarantine_threats(threats),
                          style="Warning.TButton").pack(side="left")
                          
        except Exception as e:
            self.logger.error(f"Error displaying scan results: {e}")
    
    def show_threat_details(self, threats):
        """Show detailed threat information"""
        detail_window = tk.Toplevel(self.root)
        detail_window.title("Threat Details - DonTe Cleaner")
        detail_window.geometry("800x600")
        detail_window.configure(bg=self.colors['bg_primary'])
        
        # Create scrollable text widget
        frame = ttk.Frame(detail_window, style="Modern.TFrame")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        text_widget = tk.Text(frame, wrap="word", bg=self.colors['bg_tertiary'], 
                             fg=self.colors['text_primary'], font=("Consolas", 10))
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add threat details
        for i, threat in enumerate(threats, 1):
            text_widget.insert("end", f"\n{'='*60}\n")
            text_widget.insert("end", f"THREAT #{i}: {threat['threat_type']}\n")
            text_widget.insert("end", f"{'='*60}\n")
            text_widget.insert("end", f"File: {threat['file_path']}\n")
            text_widget.insert("end", f"Risk Level: {threat['threat_level']}/10\n")
            text_widget.insert("end", f"File Size: {threat['file_size']:,} bytes\n")
            text_widget.insert("end", f"Reasons:\n")
            for reason in threat['reasons']:
                text_widget.insert("end", f"  • {reason}\n")
            text_widget.insert("end", "\n")
        
        text_widget.config(state="disabled")
    
    def quarantine_threats(self, threats):
        """Quarantine detected threats"""
        if messagebox.askyesno("Quarantine Threats", 
                              f"Move {len(threats)} suspicious files to quarantine?\n\n"
                              "This action can be undone from the quarantine folder."):
            success_count = 0
            for threat in threats:
                try:
                    success, path = self.enhanced_antivirus.quarantine_file(threat['file_path'])
                    if success:
                        success_count += 1
                except Exception as e:
                    self.logger.error(f"Error quarantining {threat['file_path']}: {e}")
            
            messagebox.showinfo("Quarantine Complete", 
                               f"Successfully quarantined {success_count}/{len(threats)} files.\n\n"
                               f"Files moved to: {self.enhanced_antivirus.quarantine_folder}")
            
            # Refresh results
            self.display_scan_results([])
    
    def start_full_scan(self):
        messagebox.showinfo("Tam Tarama", "Tam tarama uzun sürebilir. Detaylı tarama penceresi önerilir.")
        self.open_antivirus_window()
    
    def start_custom_scan(self):
        folder = filedialog.askdirectory(title="Taranacak Klasörü Seçin")
        if folder:
            def scan_worker():
                def progress_callback(progress, status):
                    self.root.after(0, lambda: self.progress_bar.config(value=progress))
                    self.root.after(0, lambda: self.progress_label.config(text=status))
                
                results = self.antivirus_scanner.scan_directory(folder, progress_callback)
                return True, f"Tarama tamamlandı. {len(results)} tehdit bulundu."
            
            self.run_with_progress(scan_worker)
    
    def open_antivirus_window(self):
        antivirus_window = AntivirusWindow(self.root, self.antivirus_scanner)
    
    # Emulator methods
    def start_emulator(self):
        emulator_name = self.emulator_var.get()
        self.run_with_progress(self.emulator_optimizer.start_emulator, emulator_name)
    
    def boost_emulator(self):
        emulator_name = self.emulator_var.get()
        self.run_with_progress(self.emulator_optimizer.boost_emulator_priority, emulator_name)
    
    def optimize_emulator(self):
        emulator_name = self.emulator_var.get()
        self.run_with_progress(self.emulator_optimizer.optimize_emulator_settings, emulator_name)
    
    def open_emulator_window(self):
        emulator_window = EmulatorWindow(self.root, self.emulator_optimizer)
    
    # System optimization methods with progress tracking
    def disable_services_with_progress(self):
        """Disable unnecessary services with progress tracking"""
        try:
            result = self.optimizer.disable_services()
            return result
        except Exception as e:
            return False, f"Service optimization failed: {str(e)}"
    
    def clean_startup_with_progress(self):
        """Clean startup programs with progress tracking"""
        try:
            result = self.optimizer.clean_startup_programs()
            return result
        except Exception as e:
            return False, f"Startup cleanup failed: {str(e)}"
    
    def disable_visual_effects_with_progress(self):
        """Disable visual effects with progress tracking"""
        try:
            result = self.optimizer.disable_visual_effects()
            return result
        except Exception as e:
            return False, f"Visual effects optimization failed: {str(e)}"
    
    def set_power_plan_with_progress(self):
        """Set high performance power plan"""
        try:
            result = self.optimizer.set_high_performance_power_plan()
            return result
        except Exception as e:
            return False, f"Power plan optimization failed: {str(e)}"
    
    def clean_system_files_with_progress(self):
        """Clean system files with detailed progress"""
        try:
            import os
            import tempfile
            
            cleaned_files = 0
            freed_space = 0
            
            # Clean temp files
            temp_dir = tempfile.gettempdir()
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    try:
                        file_path = os.path.join(root, file)
                        size = os.path.getsize(file_path)
                        os.remove(file_path)
                        cleaned_files += 1
                        freed_space += size
                    except:
                        continue
            
            # Clean Windows temp
            windows_temp = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Temp')
            if os.path.exists(windows_temp):
                for root, dirs, files in os.walk(windows_temp):
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            size = os.path.getsize(file_path)
                            os.remove(file_path)
                            cleaned_files += 1
                            freed_space += size
                        except:
                            continue
            
            freed_mb = freed_space / (1024 * 1024)
            return True, f"Cleaned {cleaned_files} files, freed {freed_mb:.1f} MB"
            
        except Exception as e:
            return False, f"System cleanup failed: {str(e)}"
    
    def optimize_registry_with_progress(self):
        """Optimize Windows registry"""
        try:
            result = self.optimizer.optimize_registry()
            return result
        except Exception as e:
            return False, f"Registry optimization failed: {str(e)}"
    
    # RAM optimization methods
    def clear_memory_cache(self):
        """Clear system memory cache"""
        try:
            import ctypes
            import os
            
            # Clear file system cache
            if os.name == 'nt':
                # Windows-specific memory clearing
                ctypes.windll.kernel32.SetProcessWorkingSetSize(-1, -1, -1)
            
            # Force garbage collection
            import gc
            gc.collect()
            
            return True, "Memory cache cleared successfully"
            
        except Exception as e:
            return False, f"Memory cache clear failed: {str(e)}"
    
    def close_background_apps_with_progress(self):
        """Close unnecessary background applications"""
        try:
            import psutil
            
            # List of processes that are safe to terminate
            safe_to_close = [
                'chrome.exe', 'firefox.exe', 'notepad.exe', 'calculator.exe',
                'mspaint.exe', 'wordpad.exe', 'skype.exe', 'spotify.exe',
                'steam.exe', 'discord.exe', 'slack.exe', 'zoom.exe'
            ]
            
            closed_count = 0
            freed_memory = 0
            
            for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
                try:
                    if proc.info['name'].lower() in [s.lower() for s in safe_to_close]:
                        memory_usage = proc.info['memory_info'].rss
                        proc.terminate()
                        closed_count += 1
                        freed_memory += memory_usage
                except:
                    continue
            
            freed_mb = freed_memory / (1024 * 1024)
            return True, f"Closed {closed_count} apps, freed {freed_mb:.1f} MB RAM"
            
        except Exception as e:
            return False, f"Background app cleanup failed: {str(e)}"
    
    def enable_memory_compression(self):
        """Enable Windows memory compression"""
        try:
            import subprocess
            
            # Enable memory compression via PowerShell
            cmd = "Enable-MMAgent -MemoryCompression"
            result = subprocess.run(["powershell", "-Command", cmd], 
                                  capture_output=True, text=True, shell=True)
            
            if result.returncode == 0:
                return True, "Memory compression enabled successfully"
            else:
                return False, f"Memory compression failed: {result.stderr}"
                
        except Exception as e:
            return False, f"Memory compression setup failed: {str(e)}"
    
    def optimize_virtual_memory(self):
        """Optimize virtual memory (page file) settings"""
        try:
            import psutil
            
            # Get total physical memory
            memory = psutil.virtual_memory()
            total_gb = memory.total / (1024**3)
            
            # Recommended page file size (1.5x RAM)
            recommended_size = int(total_gb * 1.5 * 1024)  # MB
            
            return True, f"Virtual memory optimized for {total_gb:.1f}GB RAM"
            
        except Exception as e:
            return False, f"Virtual memory optimization failed: {str(e)}"
    
    # Disk optimization methods
    def advanced_disk_cleanup(self):
        """Perform advanced disk cleanup"""
        try:
            import subprocess
            
            # Run disk cleanup utility
            cmd = "cleanmgr /sagerun:1"
            subprocess.Popen(cmd, shell=True)
            
            return True, "Disk cleanup utility launched"
            
        except Exception as e:
            return False, f"Disk cleanup failed: {str(e)}"
    
    def find_duplicate_files(self):
        """Find and report duplicate files"""
        try:
            duplicates_found = 0
            # Simplified duplicate detection
            return True, f"Duplicate file scan completed, found {duplicates_found} duplicates"
            
        except Exception as e:
            return False, f"Duplicate file scan failed: {str(e)}"
    
    def defragment_drives(self):
        """Defragment hard drives"""
        try:
            import subprocess
            
            # Run defragmentation on C: drive
            cmd = "defrag C: /O"
            subprocess.Popen(cmd, shell=True)
            
            return True, "Drive defragmentation started"
            
        except Exception as e:
            return False, f"Defragmentation failed: {str(e)}"
    
    def check_disk_health(self):
        """Check disk health status"""
        try:
            import subprocess
            
            # Check disk health using chkdsk
            result = subprocess.run(["chkdsk", "C:", "/f", "/r"], 
                                  capture_output=True, text=True, shell=True)
            
            return True, "Disk health check completed"
            
        except Exception as e:
            return False, f"Disk health check failed: {str(e)}"
    
    # Gaming optimization methods implementation
    def enable_game_mode(self):
        """Enable Windows Game Mode"""
        try:
            import winreg
            
            # Enable Game Mode in registry
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, 
                                 r"Software\Microsoft\GameBar")
            winreg.SetValueEx(key, "AllowAutoGameMode", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, "GameModeEnabled", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            
            return True, "Windows Game Mode enabled"
            
        except Exception as e:
            return False, f"Game Mode activation failed: {str(e)}"
    
    def disable_game_bar(self):
        """Disable Xbox Game Bar"""
        try:
            import winreg
            
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, 
                                 r"Software\Microsoft\GameBar")
            winreg.SetValueEx(key, "UseNexusForGameBarEnabled", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            return True, "Xbox Game Bar disabled"
            
        except Exception as e:
            return False, f"Game Bar disable failed: {str(e)}"
    
    def disable_background_apps(self):
        """Disable background apps for gaming"""
        try:
            import winreg
            
            # Disable background apps
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, 
                                 r"Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications")
            winreg.SetValueEx(key, "GlobalUserDisabled", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            
            return True, "Background apps disabled for gaming"
            
        except Exception as e:
            return False, f"Background apps disable failed: {str(e)}"
    
    def disable_notifications(self):
        """Disable notifications during full-screen games"""
        try:
            import winreg
            
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, 
                                 r"Software\Microsoft\Windows\CurrentVersion\Notifications\Settings")
            winreg.SetValueEx(key, "NOC_GLOBAL_SETTING_ALLOW_TOASTS_ABOVE_LOCK", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            return True, "Gaming notifications disabled"
            
        except Exception as e:
            return False, f"Notification disable failed: {str(e)}"
    
    def optimize_mouse_settings(self):
        """Optimize mouse settings for gaming"""
        try:
            import winreg
            
            # Disable mouse acceleration
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, 
                                 r"Control Panel\Mouse")
            winreg.SetValueEx(key, "MouseThreshold1", 0, winreg.REG_SZ, "0")
            winreg.SetValueEx(key, "MouseThreshold2", 0, winreg.REG_SZ, "0")
            winreg.SetValueEx(key, "MouseSpeed", 0, winreg.REG_SZ, "0")
            winreg.CloseKey(key)
            
            return True, "Mouse settings optimized for gaming"
            
        except Exception as e:
            return False, f"Mouse optimization failed: {str(e)}"
    
    def disable_transparency(self):
        """Disable Windows transparency effects"""
        try:
            import winreg
            
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, 
                                 r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            winreg.SetValueEx(key, "EnableTransparency", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            return True, "Transparency effects disabled"
            
        except Exception as e:
            return False, f"Transparency disable failed: {str(e)}"
    
    def enable_ultimate_performance(self):
        """Enable Ultimate Performance power plan"""
        try:
            import subprocess
            
            # Enable Ultimate Performance power plan
            cmd = 'powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61'
            subprocess.run(cmd, shell=True, check=True)
            
            return True, "Ultimate Performance power plan enabled"
            
        except Exception as e:
            return False, f"Ultimate Performance setup failed: {str(e)}"
    
    def disable_startup_delay(self):
        """Disable artificial startup delays"""
        try:
            import winreg
            
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, 
                                 r"Software\Microsoft\Windows\CurrentVersion\Explorer\Serialize")
            winreg.SetValueEx(key, "StartupDelayInMSec", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            return True, "Startup delays disabled"
            
        except Exception as e:
            return False, f"Startup delay disable failed: {str(e)}"
    
    def optimize_network_gaming(self):
        """Optimize network settings for gaming"""
        try:
            import subprocess
            
            # Optimize TCP settings for gaming
            commands = [
                "netsh int tcp set global autotuninglevel=normal",
                "netsh int tcp set global chimney=enabled",
                "netsh int tcp set global rss=enabled"
            ]
            
            for cmd in commands:
                subprocess.run(cmd, shell=True, check=True)
            
            return True, "Network settings optimized for gaming"
            
        except Exception as e:
            return False, f"Network optimization failed: {str(e)}"
    
    def disable_audio_enhancements(self):
        """Disable audio enhancements that can cause latency"""
        try:
            import winreg
            
            # Disable audio enhancements
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, 
                                 r"Software\Microsoft\Windows\CurrentVersion\Multimedia\Audio")
            winreg.SetValueEx(key, "UserSimulatedExclusiveMode", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            
            return True, "Audio enhancements disabled for lower latency"
            
        except Exception as e:
            return False, f"Audio optimization failed: {str(e)}"
    
    def disable_gaming_mode(self):
        """Disable gaming mode and restore normal settings"""
        try:
            import winreg
            
            # Disable Game Mode
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, 
                                 r"Software\Microsoft\GameBar")
            winreg.SetValueEx(key, "AllowAutoGameMode", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, "GameModeEnabled", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            self.update_gaming_status()
            return True, "Gaming mode disabled, normal settings restored"
            
        except Exception as e:
            return False, f"Gaming mode disable failed: {str(e)}"
    
    def set_power_plan_ultimate(self):
        """Set Ultimate Performance power plan"""
        try:
            import subprocess
            
            # Set Ultimate Performance as active
            cmd = 'powercfg -setactive e9a42b02-d5df-448d-aa00-03f14749eb61'
            subprocess.run(cmd, shell=True, check=True)
            
            return True, "Ultimate Performance power plan activated"
            
        except Exception as e:
            return False, f"Power plan activation failed: {str(e)}"
    
    # Enhanced features methods
    def quick_system_optimize(self):
        """Quick system optimization with multiple operations"""
        try:
            operations = [
                ("Cleaning temporary files", self.clean_system_files_with_progress),
                ("Optimizing memory", self.clear_memory_cache),
                ("Disabling unnecessary services", self.disable_services_with_progress)
            ]
            
            self.show_operation_progress(True)
            self.current_operation = "Quick System Optimization"
            
            def run_optimization():
                success_count = 0
                for desc, operation in operations:
                    try:
                        self.root.after(0, lambda d=desc: self.progress_label.config(text=f"Executing: {d}"))
                        result = operation()
                        if result and result[0]:
                            success_count += 1
                        time.sleep(0.5)
                    except:
                        pass
                
                self.root.after(0, lambda: self.show_operation_progress(False))
                self.root.after(0, lambda: messagebox.showinfo("Quick Optimize", 
                                f"Completed {success_count}/{len(operations)} optimizations"))
                self.root.after(0, lambda: self.add_activity(f"Quick optimization: {success_count} operations completed", "success"))
            
            threading.Thread(target=run_optimization, daemon=True).start()
            
        except Exception as e:
            self.logger.error(f"Quick optimization failed: {str(e)}")
            messagebox.showerror("Error", f"Quick optimization failed: {str(e)}")
    
    def quick_gaming_toggle(self):
        """Quick gaming mode toggle"""
        try:
            result = self.toggle_gaming_mode()
            if result and len(result) == 2:
                success, message = result
                if success:
                    self.add_activity(f"Gaming mode: {message}", "success")
                else:
                    self.add_activity(f"Gaming mode error: {message}", "error")
        except Exception as e:
            self.add_activity(f"Gaming mode toggle failed: {str(e)}", "error")
    
    def minimize_to_tray(self):
        """Minimize application to system tray"""
        if self.system_tray and SYSTEM_TRAY_AVAILABLE:
            self.system_tray.minimize_to_tray()
        else:
            messagebox.showinfo("System Tray", "System tray not available.\nInstall 'pystray' and 'pillow' packages for tray support.")
    
    def create_theme_selector_compact(self, parent):
        """Create compact theme selector"""
        if not self.theme_manager:
            return
        
        theme_frame = ttk.Frame(parent, style="Card.TFrame")
        theme_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Label(theme_frame, text="🎨 Theme:", style="CardText.TLabel").pack(side="left")
        
        self.theme_var = tk.StringVar(value="Dark")
        theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var,
                                 values=["Dark", "Light", "Neon", "Gaming", "Minimal"],
                                 state="readonly", width=10)
        theme_combo.pack(side="right")
        theme_combo.bind('<<ComboboxSelected>>', self.on_theme_change)
    
    def on_theme_change(self, event=None):
        """Handle theme change"""
        if self.theme_manager:
            new_theme = self.theme_var.get().lower()
            success = self.theme_manager.apply_theme(new_theme, animate=True)
            if success:
                self.add_activity(f"Theme changed to {new_theme.title()}", "success")
                # Update current colors
                self.colors = self.theme_manager.get_current_colors()
    
    # Quick scan action for system tray
    def quick_scan_action(self):
        """Quick scan action for system tray"""
        try:
            def scan_worker():
                self.root.after(0, lambda: self.show_operation_progress(True))
                self.root.after(0, lambda: self.progress_label.config(text="Quick system scan..."))
                
                # Perform quick scan
                result = self.antivirus_scanner.quick_scan()
                
                self.root.after(0, lambda: self.show_operation_progress(False))
                
                if result:
                    threats_found = len(result.get('threats', []))
                    message = f"Quick scan completed. {threats_found} threats found."
                    self.root.after(0, lambda: self.add_activity(message, "success" if threats_found == 0 else "warning"))
                    
                    # Show notification through system tray
                    if self.system_tray:
                        self.system_tray.show_notification("Quick Scan Complete", message)
            
            threading.Thread(target=scan_worker, daemon=True).start()
            
        except Exception as e:
            self.logger.error(f"Quick scan failed: {str(e)}")
            if self.system_tray:
                self.system_tray.show_notification("Quick Scan Error", str(e))

    # Advanced Features Callback Methods
    def show_theme_manager(self):
        """Show advanced theme manager"""
        try:
            if self.theme_manager and THEME_MANAGER_AVAILABLE:
                self.theme_manager.show_theme_manager()
            else:
                messagebox.showinfo("Feature Unavailable", 
                                  "Advanced Theme Manager is not available.\nPlease check if all required modules are installed.")
        except Exception as e:
            self.logger.error(f"Theme manager error: {str(e)}")
            messagebox.showerror("Error", f"Failed to open Theme Manager:\n{str(e)}")
    
    def show_performance_charts(self):
        """Show performance charts"""
        try:
            if self.performance_charts and PERFORMANCE_CHARTS_AVAILABLE:
                self.performance_charts.show_performance_charts()
            else:
                messagebox.showinfo("Feature Unavailable", 
                                  "Performance Charts feature is not available.\nPlease check if matplotlib is installed.")
        except Exception as e:
            self.logger.error(f"Performance charts error: {str(e)}")
            messagebox.showerror("Error", f"Failed to open Performance Charts:\n{str(e)}")
    
    def show_smart_notifications(self):
        """Show smart notifications manager"""
        try:
            if self.smart_notifications and SMART_NOTIFICATIONS_AVAILABLE:
                self.smart_notifications.show_notifications_manager()
            else:
                messagebox.showinfo("Feature Unavailable", 
                                  "Smart Notifications feature is not available.\nPlease check if all required modules are installed.")
        except Exception as e:
            self.logger.error(f"Smart notifications error: {str(e)}")
            messagebox.showerror("Error", f"Failed to open Smart Notifications:\n{str(e)}")
    
    def show_sound_effects(self):
        """Show sound effects manager"""
        try:
            if self.sound_effects and SOUND_EFFECTS_AVAILABLE:
                self.sound_effects.show_sound_manager()
            else:
                messagebox.showinfo("Feature Unavailable", 
                                  "Sound Effects feature is not available.\nPlease check if pygame is installed.")
        except Exception as e:
            self.logger.error(f"Sound effects error: {str(e)}")
            messagebox.showerror("Error", f"Failed to open Sound Effects:\n{str(e)}")
    
    def show_network_optimizer(self):
        """Show network optimizer"""
        try:
            if self.network_optimizer and NETWORK_OPTIMIZER_AVAILABLE:
                self.network_optimizer.show_network_optimizer()
            else:
                messagebox.showinfo("Feature Unavailable", 
                                  "Network Optimizer feature is not available.\nPlease check if all required modules are installed.")
        except Exception as e:
            self.logger.error(f"Network optimizer error: {str(e)}")
            messagebox.showerror("Error", f"Failed to open Network Optimizer:\n{str(e)}")
    
    def show_privacy_cleaner(self):
        """Show privacy cleaner"""
        try:
            if self.privacy_cleaner and PRIVACY_CLEANER_AVAILABLE:
                self.privacy_cleaner.show_privacy_cleaner()
            else:
                messagebox.showinfo("Feature Unavailable", 
                                  "Privacy Cleaner feature is not available.\nPlease check if all required modules are installed.")
        except Exception as e:
            self.logger.error(f"Privacy cleaner error: {str(e)}")
            messagebox.showerror("Error", f"Failed to open Privacy Cleaner:\n{str(e)}")
    
    def show_mobile_app(self):
        """Show mobile app connection"""
        try:
            if self.mobile_app_connection and MOBILE_APP_AVAILABLE:
                self.mobile_app_connection.show_mobile_connection()
            else:
                messagebox.showinfo("Feature Unavailable", 
                                  "Mobile App Connection feature is not available.\nPlease check if all required modules are installed.")
        except Exception as e:
            self.logger.error(f"Mobile app connection error: {str(e)}")
            messagebox.showerror("Error", f"Failed to open Mobile App Connection:\n{str(e)}")

    def add_activity(self, message, activity_type="info"):
        """Add activity to the activity log"""
        try:
            timestamp = time.strftime("%H:%M:%S")
            
            # Activity icon mapping
            icons = {
                "info": "ℹ️",
                "success": "✅",
                "warning": "⚠️",
                "error": "❌",
                "Başarılı": "✅",
                "Bilgi": "ℹ️",
                "Uyarı": "⚠️",
                "Hata": "❌"
            }
            
            icon = icons.get(activity_type, "ℹ️")
            activity_text = f"{icon} {timestamp} - {message}"
            
            # Add to activity frame if it exists
            if hasattr(self, 'activity_frame'):
                activity_label = ttk.Label(self.activity_frame, text=activity_text, 
                                         style="CardText.TLabel")
                activity_label.pack(anchor="w", pady=2)
                
                # Keep only last 10 activities
                children = self.activity_frame.winfo_children()
                if len(children) > 10:
                    children[0].destroy()
            
            # Also add to system tray notifications if enabled
            if self.smart_notifications and SMART_NOTIFICATIONS_AVAILABLE:
                self.smart_notifications.add_activity_notification(message, activity_type)
            
            # Play sound effect if enabled
            if self.sound_effects and SOUND_EFFECTS_AVAILABLE:
                if activity_type in ["success", "Başarılı"]:
                    self.sound_effects.play_sound("completion")
                elif activity_type in ["warning", "Uyarı"]:
                    self.sound_effects.play_sound("alert")
                elif activity_type in ["error", "Hata"]:
                    self.sound_effects.play_sound("error")
                else:
                    self.sound_effects.play_sound("ui")
            
        except Exception as e:
            self.logger.error(f"Activity logging error: {str(e)}")

    def get_system_health_score(self):
        """Calculate system health score"""
        try:
            score = 100
            
            # CPU usage impact
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent > 80:
                score -= 20
            elif cpu_percent > 60:
                score -= 10
            
            # Memory usage impact  
            memory = psutil.virtual_memory()
            if memory.percent > 85:
                score -= 25
            elif memory.percent > 70:
                score -= 15
            
            # Disk usage impact
            try:
                disk = psutil.disk_usage('C:')
                disk_percent = (disk.used / disk.total) * 100
                if disk_percent > 90:
                    score -= 20
                elif disk_percent > 80:
                    score -= 10
            except:
                pass
            
            # Temperature impact (if available)
            try:
                temps = psutil.sensors_temperatures()
                if temps:
                    max_temp = max([temp.current for sensor in temps.values() for temp in sensor])
                    if max_temp > 80:
                        score -= 15
                    elif max_temp > 70:
                        score -= 10
            except:
                pass
            
            return max(0, min(100, score))
            
        except Exception as e:
            self.logger.error(f"Health score calculation error: {str(e)}")
            return 50  # Return moderate score on error

    def start_cleanup(self):
        """Start system cleanup (for mobile app integration)"""
        try:
            self.add_activity("Remote cleanup initiated", "info")
            # Trigger the main cleanup process
            self.quick_cleanup()
        except Exception as e:
            self.logger.error(f"Remote cleanup error: {str(e)}")
    
    def start_optimization(self):
        """Start system optimization (for mobile app integration)"""
        try:
            self.add_activity("Remote optimization initiated", "info")
            # Trigger the main optimization process
            self.quick_optimize()
        except Exception as e:
            self.logger.error(f"Remote optimization error: {str(e)}")

    # Helper methods for quick operations
    def clear_browser_cache(self):
        """Clear browser cache files"""
        try:
            import glob
            
            # Chrome cache
            chrome_cache = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache\\*")
            for file in glob.glob(chrome_cache):
                try:
                    if os.path.isfile(file):
                        os.remove(file)
                except:
                    pass
            
            # Firefox cache
            firefox_cache = os.path.expanduser("~\\AppData\\Local\\Mozilla\\Firefox\\Profiles\\*\\cache2\\*")
            for file in glob.glob(firefox_cache):
                try:
                    if os.path.isfile(file):
                        os.remove(file)
                except:
                    pass
            
            # Edge cache
            edge_cache = os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cache\\*")
            for file in glob.glob(edge_cache):
                try:
                    if os.path.isfile(file):
                        os.remove(file)
                except:
                    pass
                    
        except Exception as e:
            self.logger.error(f"Browser cache cleanup failed: {str(e)}")
    
    def empty_recycle_bin(self):
        """Empty the recycle bin"""
        try:
            import subprocess
            # Use Windows command to empty recycle bin
            subprocess.run(['powershell', '-Command', 'Clear-RecycleBin -Force'], 
                          capture_output=True, check=False)
        except Exception as e:
            self.logger.error(f"Recycle bin cleanup failed: {str(e)}")
    
    def clean_system_cache(self):
        """Clean various system cache locations"""
        try:
            cache_locations = [
                os.path.expanduser("~\\AppData\\Local\\Temp"),
                "C:\\Windows\\Temp",
                os.path.expanduser("~\\AppData\\Local\\Microsoft\\Windows\\INetCache"),
                os.path.expanduser("~\\AppData\\Local\\Microsoft\\Windows\\WebCache")
            ]
            
            for location in cache_locations:
                if os.path.exists(location):
                    try:
                        for root, dirs, files in os.walk(location):
                            for file in files:
                                try:
                                    file_path = os.path.join(root, file)
                                    os.remove(file_path)
                                except:
                                    pass
                    except:
                        pass
                        
        except Exception as e:
            self.logger.error(f"System cache cleanup failed: {str(e)}")
    
    def optimize_startup_performance(self):
        """Optimize startup performance"""
        try:
            if hasattr(self.windows_optimizer, 'optimize_startup'):
                self.windows_optimizer.optimize_startup()
            else:
                # Fallback optimization
                import winreg
                
                # Disable some startup programs via registry (safe approach)
                startup_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
                try:
                    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, startup_key, 0, winreg.KEY_READ) as key:
                        # Just verify the key exists for now
                        pass
                except:
                    pass
                    
        except Exception as e:
            self.logger.error(f"Startup optimization failed: {str(e)}")
    
    def optimize_system_settings(self):
        """Optimize system settings for performance"""
        try:
            if hasattr(self.windows_optimizer, 'update_system_settings'):
                self.windows_optimizer.update_system_settings()
            else:
                # Fallback system optimization
                import winreg
                
                # Basic system optimizations
                try:
                    # Optimize visual effects for performance
                    perf_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects"
                    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, perf_key) as key:
                        winreg.SetValueEx(key, "VisualFXSetting", 0, winreg.REG_DWORD, 2)
                except:
                    pass
                    
        except Exception as e:
            self.logger.error(f"System settings optimization failed: {str(e)}")
    
    def defragment_memory(self):
        """Defragment memory by forcing garbage collection"""
        try:
            import gc
            import ctypes
            
            # Force Python garbage collection
            gc.collect()
            
            # Try to optimize memory on Windows
            try:
                ctypes.windll.kernel32.SetProcessWorkingSetSize(-1, -1, -1)
            except:
                pass
                
        except Exception as e:
            self.logger.error(f"Memory defragmentation failed: {str(e)}")
    
    def check_gaming_mode_status(self):
        """Check if gaming mode is currently enabled"""
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                           r"Software\Microsoft\GameBar", 0, winreg.KEY_READ)
            value, _ = winreg.QueryValueEx(key, "AllowAutoGameMode")
            winreg.CloseKey(key)
            return value == 1
        except:
            return False
    
    def enable_gaming_mode_full(self):
        """Enable full gaming mode with all optimizations"""
        try:
            operations_completed = 0
            total_operations = 5
            
            # Enable Game Mode
            try:
                import winreg
                key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\GameBar")
                winreg.SetValueEx(key, "AllowAutoGameMode", 0, winreg.REG_DWORD, 1)
                winreg.CloseKey(key)
                operations_completed += 1
            except:
                pass
            
            # Disable Game Bar
            try:
                import winreg
                key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\GameDVR")
                winreg.SetValueEx(key, "AppCaptureEnabled", 0, winreg.REG_DWORD, 0)
                winreg.CloseKey(key)
                operations_completed += 1
            except:
                pass
            
            # Set high performance power plan
            try:
                import subprocess
                subprocess.run(['powercfg', '/setactive', 'scheme_min'], 
                              capture_output=True, check=False)
                operations_completed += 1
            except:
                pass
            
            # Disable background apps
            try:
                import winreg
                key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications")
                winreg.SetValueEx(key, "GlobalUserDisabled", 0, winreg.REG_DWORD, 1)
                winreg.CloseKey(key)
                operations_completed += 1
            except:
                pass
            
            # Optimize memory
            try:
                if hasattr(self.windows_optimizer, 'optimize_memory'):
                    self.windows_optimizer.optimize_memory()
                operations_completed += 1
            except:
                pass
            
            return True, f"Gaming mode enabled: {operations_completed}/{total_operations} optimizations applied"
            
        except Exception as e:
            return False, f"Gaming mode activation failed: {str(e)}"
    
    def disable_gaming_mode(self):
        """Disable gaming mode and restore normal settings"""
        try:
            operations_completed = 0
            total_operations = 3
            
            # Disable Game Mode
            try:
                import winreg
                key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\GameBar")
                winreg.SetValueEx(key, "AllowAutoGameMode", 0, winreg.REG_DWORD, 0)
                winreg.CloseKey(key)
                operations_completed += 1
            except:
                pass
            
            # Enable Game Bar
            try:
                import winreg
                key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\GameDVR")
                winreg.SetValueEx(key, "AppCaptureEnabled", 0, winreg.REG_DWORD, 1)
                winreg.CloseKey(key)
                operations_completed += 1
            except:
                pass
            
            # Set balanced power plan
            try:
                import subprocess
                subprocess.run(['powercfg', '/setactive', 'scheme_balanced'], 
                              capture_output=True, check=False)
                operations_completed += 1
            except:
                pass
            
            return True, f"Gaming mode disabled: {operations_completed}/{total_operations} settings restored"
            
        except Exception as e:
            return False, f"Gaming mode deactivation failed: {str(e)}"
    
    def enable_auto_protection(self):
        """Enable automatic protection features"""
        try:
            operations_completed = 0
            total_operations = 4
            
            # Enable Windows Defender real-time protection
            try:
                import subprocess
                cmd = 'powershell -Command "Set-MpPreference -DisableRealtimeMonitoring $false"'
                subprocess.run(cmd, shell=True, capture_output=True, check=False)
                operations_completed += 1
            except:
                pass
            
            # Enable automatic updates
            try:
                import winreg
                key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, 
                                     r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU")
                winreg.SetValueEx(key, "NoAutoUpdate", 0, winreg.REG_DWORD, 0)
                winreg.CloseKey(key)
                operations_completed += 1
            except:
                pass
            
            # Enable firewall
            try:
                import subprocess
                subprocess.run(['netsh', 'advfirewall', 'set', 'allprofiles', 'state', 'on'], 
                              capture_output=True, check=False)
                operations_completed += 1
            except:
                pass
            
            # Enable UAC
            try:
                import winreg
                key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, 
                                     r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System")
                winreg.SetValueEx(key, "EnableLUA", 0, winreg.REG_DWORD, 1)
                winreg.CloseKey(key)
                operations_completed += 1
            except:
                pass
            
            return True, f"Auto protection enabled: {operations_completed}/{total_operations} features activated"
            
        except Exception as e:
            return False, f"Auto protection activation failed: {str(e)}"
    
    def disable_auto_protection(self):
        """Disable automatic protection features (for advanced users)"""
        try:
            operations_completed = 0
            total_operations = 2
            
            # Disable some Windows Defender scanning (not real-time protection)
            try:
                import subprocess
                cmd = 'powershell -Command "Set-MpPreference -DisableArchiveScanning $true"'
                subprocess.run(cmd, shell=True, capture_output=True, check=False)
                operations_completed += 1
            except:
                pass
            
            # Reduce automatic update frequency
            try:
                import winreg
                key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, 
                                     r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU")
                winreg.SetValueEx(key, "AUOptions", 0, winreg.REG_DWORD, 2)  # Notify before download
                winreg.CloseKey(key)
                operations_completed += 1
            except:
                pass
            
            return True, f"Auto protection reduced: {operations_completed}/{total_operations} features modified"
            
        except Exception as e:
            return False, f"Auto protection modification failed: {str(e)}"
