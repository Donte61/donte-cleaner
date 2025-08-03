"""
Privacy Cleaner for DonTe Cleaner
Advanced privacy cleaning with browser data, tracking files, and privacy protection
"""

import os
import sqlite3
import json
import shutil
import winreg
import glob
import threading
from pathlib import Path
from tkinter import messagebox
import psutil

class PrivacyCleaner:
    def __init__(self, main_window):
        self.main_window = main_window
        self.settings_file = "config/privacy_settings.json"
        self.scanning = False
        
        # Privacy categories
        self.privacy_categories = {
            'browser_data': {
                'enabled': True,
                'name': 'Browser Data',
                'description': 'Cookies, cache, history, downloads'
            },
            'tracking_files': {
                'enabled': True,
                'name': 'Tracking Files',
                'description': 'Tracking cookies, beacons, analytics'
            },
            'recent_documents': {
                'enabled': True,
                'name': 'Recent Documents',
                'description': 'Recent files, jump lists, shortcuts'
            },
            'system_traces': {
                'enabled': True,
                'name': 'System Traces',
                'description': 'Prefetch, temp files, logs'
            },
            'registry_traces': {
                'enabled': False,
                'name': 'Registry Traces',
                'description': 'Registry entries, MRU lists'
            },
            'network_traces': {
                'enabled': True,
                'name': 'Network Traces',
                'description': 'DNS cache, network logs'
            }
        }
        
        # Browser paths
        self.browser_paths = {
            'chrome': {
                'name': 'Google Chrome',
                'paths': {
                    'cache': os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache'),
                    'cookies': os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cookies'),
                    'history': os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History'),
                    'downloads': os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History'),
                    'form_data': os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Web Data'),
                    'sessions': os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Sessions'),
                    'bookmarks': os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks')
                }
            },
            'firefox': {
                'name': 'Mozilla Firefox',
                'paths': {
                    'cache': os.path.expanduser('~\\AppData\\Local\\Mozilla\\Firefox\\Profiles'),
                    'cookies': os.path.expanduser('~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles'),
                    'history': os.path.expanduser('~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles'),
                    'downloads': os.path.expanduser('~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles'),
                    'form_data': os.path.expanduser('~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles'),
                    'sessions': os.path.expanduser('~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles')
                }
            },
            'edge': {
                'name': 'Microsoft Edge',
                'paths': {
                    'cache': os.path.expanduser('~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cache'),
                    'cookies': os.path.expanduser('~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cookies'),
                    'history': os.path.expanduser('~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\History'),
                    'downloads': os.path.expanduser('~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\History'),
                    'form_data': os.path.expanduser('~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Web Data'),
                    'sessions': os.path.expanduser('~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Sessions')
                }
            },
            'opera': {
                'name': 'Opera',
                'paths': {
                    'cache': os.path.expanduser('~\\AppData\\Local\\Opera Software\\Opera Stable\\Cache'),
                    'cookies': os.path.expanduser('~\\AppData\\Roaming\\Opera Software\\Opera Stable\\Cookies'),
                    'history': os.path.expanduser('~\\AppData\\Roaming\\Opera Software\\Opera Stable\\History'),
                    'downloads': os.path.expanduser('~\\AppData\\Roaming\\Opera Software\\Opera Stable\\History'),
                    'form_data': os.path.expanduser('~\\AppData\\Roaming\\Opera Software\\Opera Stable\\Web Data')
                }
            }
        }
        
        # System trace paths
        self.system_paths = {
            'temp': [
                os.path.expanduser('~\\AppData\\Local\\Temp'),
                'C:\\Windows\\Temp',
                'C:\\Temp'
            ],
            'prefetch': 'C:\\Windows\\Prefetch',
            'recent': os.path.expanduser('~\\AppData\\Roaming\\Microsoft\\Windows\\Recent'),
            'jumplists': os.path.expanduser('~\\AppData\\Roaming\\Microsoft\\Windows\\Recent\\AutomaticDestinations'),
            'thumbnail_cache': os.path.expanduser('~\\AppData\\Local\\Microsoft\\Windows\\Explorer'),
            'icon_cache': os.path.expanduser('~\\AppData\\Local\\IconCache.db'),
            'font_cache': 'C:\\Windows\\System32\\FNTCACHE.DAT'
        }
        
        # Registry paths for privacy cleaning
        self.registry_paths = {
            'run_mru': r'HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RunMRU',
            'typed_urls': r'HKEY_CURRENT_USER\\Software\\Microsoft\\Internet Explorer\\TypedURLs',
            'recent_docs': r'HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RecentDocs',
            'user_assist': r'HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist'
        }
        
        # Scan results
        self.scan_results = {
            'browser_data': {},
            'tracking_files': [],
            'recent_documents': [],
            'system_traces': [],
            'registry_traces': [],
            'network_traces': []
        }
        
        # Load settings
        self.load_settings()
    
    def load_settings(self):
        """Load privacy settings"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    for category, data in settings.get('categories', {}).items():
                        if category in self.privacy_categories:
                            self.privacy_categories[category].update(data)
        except Exception as e:
            print(f"Privacy settings load error: {e}")
    
    def save_settings(self):
        """Save privacy settings"""
        try:
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            settings = {
                'categories': self.privacy_categories
            }
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Privacy settings save error: {e}")
    
    def show_privacy_cleaner(self):
        """Show privacy cleaner window"""
        import tkinter as tk
        from tkinter import ttk
        
        self.privacy_window = tk.Toplevel(self.main_window.root)
        self.privacy_window.title("🔐 Privacy Cleaner")
        self.privacy_window.geometry("1000x700")
        self.privacy_window.configure(bg=self.main_window.colors['bg_dark'])
        self.privacy_window.transient(self.main_window.root)
        self.privacy_window.grab_set()
        
        # Create privacy cleaner interface
        self.create_privacy_interface()
        
        # Center window
        self.center_privacy_window()
    
    def center_privacy_window(self):
        """Center privacy window"""
        self.privacy_window.update_idletasks()
        width = self.privacy_window.winfo_width()
        height = self.privacy_window.winfo_height()
        x = (self.privacy_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.privacy_window.winfo_screenheight() // 2) - (height // 2)
        self.privacy_window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_privacy_interface(self):
        """Create privacy cleaner interface"""
        import tkinter as tk
        from tkinter import ttk
        
        main_frame = ttk.Frame(self.privacy_window, style="Modern.TFrame", padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Header
        self.create_privacy_header(main_frame)
        
        # Content area
        content_frame = ttk.Frame(main_frame, style="Modern.TFrame")
        content_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # Left panel - Categories
        left_panel = ttk.Frame(content_frame, style="Card.TFrame", padding="15")
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.configure(width=300)
        left_panel.pack_propagate(False)
        
        # Right panel - Results
        right_panel = ttk.Frame(content_frame, style="Modern.TFrame")
        right_panel.pack(side="right", fill="both", expand=True)
        
        # Create left panel content
        self.create_categories_panel(left_panel)
        
        # Create right panel content
        self.create_results_panel(right_panel)
    
    def create_privacy_header(self, parent):
        """Create privacy header"""
        import tkinter as tk
        from tkinter import ttk
        
        header_frame = ttk.Frame(parent, style="Modern.TFrame")
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Title
        ttk.Label(header_frame, text="🔐 Privacy Cleaner", 
                 font=("Segoe UI", 18, "bold"),
                 background=self.main_window.colors['bg_dark'],
                 foreground=self.main_window.colors['text_white']).pack(side="left")
        
        # Controls
        controls_frame = ttk.Frame(header_frame, style="Modern.TFrame")
        controls_frame.pack(side="right")
        
        # Scan button
        self.scan_btn = ttk.Button(controls_frame, text="🔍 Privacy Scan",
                                  style="Success.TButton",
                                  command=self.start_privacy_scan)
        self.scan_btn.pack(side="right", padx=(10, 0))
        
        # Clean button
        self.clean_btn = ttk.Button(controls_frame, text="🧹 Clean Selected",
                                   style="Warning.TButton",
                                   command=self.clean_selected_items,
                                   state='disabled')
        self.clean_btn.pack(side="right", padx=(10, 0))
        
        # Settings button
        ttk.Button(controls_frame, text="⚙️ Settings",
                  style="Modern.TButton",
                  command=self.show_privacy_settings).pack(side="right", padx=(10, 0))
    
    def create_categories_panel(self, parent):
        """Create privacy categories panel"""
        import tkinter as tk
        from tkinter import ttk
        
        # Categories title
        ttk.Label(parent, text="🎯 Privacy Categories",
                 font=("Segoe UI", 14, "bold"),
                 background=self.main_window.colors['bg_light'],
                 foreground=self.main_window.colors['text_white']).pack(pady=(0, 15))
        
        # Category checkboxes
        self.category_vars = {}
        
        for category_id, category_data in self.privacy_categories.items():
            var = tk.BooleanVar(value=category_data['enabled'])
            self.category_vars[category_id] = var
            
            # Category frame
            cat_frame = ttk.Frame(parent, style="Card.TFrame", padding="10")
            cat_frame.pack(fill="x", pady=5)
            
            # Checkbox and name
            checkbox = ttk.Checkbutton(cat_frame, text=category_data['name'],
                                      variable=var,
                                      command=self.update_category_settings)
            checkbox.pack(anchor="w")
            
            # Description
            ttk.Label(cat_frame, text=category_data['description'],
                     font=("Segoe UI", 8),
                     background=self.main_window.colors['bg_light'],
                     foreground=self.main_window.colors['text_gray'],
                     wraplength=250).pack(anchor="w", padx=(20, 0))
        
        # Select all/none buttons
        button_frame = ttk.Frame(parent, style="Card.TFrame")
        button_frame.pack(fill="x", pady=(15, 0))
        
        ttk.Button(button_frame, text="Select All",
                  style="Modern.TButton",
                  command=self.select_all_categories).pack(side="left")
        
        ttk.Button(button_frame, text="Select None",
                  style="Modern.TButton",
                  command=self.select_no_categories).pack(side="right")
        
        # Scan progress
        progress_frame = ttk.Frame(parent, style="Card.TFrame")
        progress_frame.pack(fill="x", pady=(20, 0))
        
        ttk.Label(progress_frame, text="Scan Progress:",
                 background=self.main_window.colors['bg_light'],
                 foreground=self.main_window.colors['text_white']).pack(anchor="w")
        
        self.scan_progress = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.scan_progress.pack(fill="x", pady=5)
        
        self.scan_status_label = ttk.Label(progress_frame, text="Ready to scan",
                                          background=self.main_window.colors['bg_light'],
                                          foreground=self.main_window.colors['text_gray'])
        self.scan_status_label.pack(anchor="w")
    
    def create_results_panel(self, parent):
        """Create scan results panel"""
        import tkinter as tk
        from tkinter import ttk
        
        # Results notebook
        self.results_notebook = ttk.Notebook(parent, style="Modern.TNotebook")
        self.results_notebook.pack(fill="both", expand=True)
        
        # Create tabs for each category
        self.create_browser_results_tab()
        self.create_tracking_results_tab()
        self.create_documents_results_tab()
        self.create_system_results_tab()
        self.create_registry_results_tab()
        self.create_network_results_tab()
        
        # Summary tab
        self.create_summary_tab()
    
    def create_browser_results_tab(self):
        """Create browser data results tab"""
        import tkinter as tk
        from tkinter import ttk
        
        browser_frame = ttk.Frame(self.results_notebook, style="Modern.TFrame", padding="10")
        self.results_notebook.add(browser_frame, text="🌐 Browser Data")
        
        # Browser treeview
        columns = ("Browser", "Data Type", "Items", "Size", "Path")
        self.browser_tree = ttk.Treeview(browser_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.browser_tree.heading(col, text=col)
            self.browser_tree.column(col, width=150)
        
        # Scrollbar
        browser_scrollbar = ttk.Scrollbar(browser_frame, orient="vertical", command=self.browser_tree.yview)
        self.browser_tree.configure(yscrollcommand=browser_scrollbar.set)
        
        self.browser_tree.pack(side="left", fill="both", expand=True)
        browser_scrollbar.pack(side="right", fill="y")
    
    def create_tracking_results_tab(self):
        """Create tracking files results tab"""
        import tkinter as tk
        from tkinter import ttk
        
        tracking_frame = ttk.Frame(self.results_notebook, style="Modern.TFrame", padding="10")
        self.results_notebook.add(tracking_frame, text="👁️ Tracking Files")
        
        # Tracking treeview
        columns = ("File Type", "Location", "Size", "Last Modified")
        self.tracking_tree = ttk.Treeview(tracking_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tracking_tree.heading(col, text=col)
            self.tracking_tree.column(col, width=180)
        
        # Scrollbar
        tracking_scrollbar = ttk.Scrollbar(tracking_frame, orient="vertical", command=self.tracking_tree.yview)
        self.tracking_tree.configure(yscrollcommand=tracking_scrollbar.set)
        
        self.tracking_tree.pack(side="left", fill="both", expand=True)
        tracking_scrollbar.pack(side="right", fill="y")
    
    def create_documents_results_tab(self):
        """Create recent documents results tab"""
        import tkinter as tk
        from tkinter import ttk
        
        docs_frame = ttk.Frame(self.results_notebook, style="Modern.TFrame", padding="10")
        self.results_notebook.add(docs_frame, text="📄 Recent Documents")
        
        # Documents treeview
        columns = ("Document", "Type", "Last Accessed", "Location")
        self.docs_tree = ttk.Treeview(docs_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.docs_tree.heading(col, text=col)
            self.docs_tree.column(col, width=180)
        
        # Scrollbar
        docs_scrollbar = ttk.Scrollbar(docs_frame, orient="vertical", command=self.docs_tree.yview)
        self.docs_tree.configure(yscrollcommand=docs_scrollbar.set)
        
        self.docs_tree.pack(side="left", fill="both", expand=True)
        docs_scrollbar.pack(side="right", fill="y")
    
    def create_system_results_tab(self):
        """Create system traces results tab"""
        import tkinter as tk
        from tkinter import ttk
        
        system_frame = ttk.Frame(self.results_notebook, style="Modern.TFrame", padding="10")
        self.results_notebook.add(system_frame, text="🖥️ System Traces")
        
        # System treeview
        columns = ("Trace Type", "Files", "Total Size", "Location")
        self.system_tree = ttk.Treeview(system_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.system_tree.heading(col, text=col)
            self.system_tree.column(col, width=180)
        
        # Scrollbar
        system_scrollbar = ttk.Scrollbar(system_frame, orient="vertical", command=self.system_tree.yview)
        self.system_tree.configure(yscrollcommand=system_scrollbar.set)
        
        self.system_tree.pack(side="left", fill="both", expand=True)
        system_scrollbar.pack(side="right", fill="y")
    
    def create_registry_results_tab(self):
        """Create registry traces results tab"""
        import tkinter as tk
        from tkinter import ttk
        
        registry_frame = ttk.Frame(self.results_notebook, style="Modern.TFrame", padding="10")
        self.results_notebook.add(registry_frame, text="📋 Registry Traces")
        
        # Registry treeview
        columns = ("Registry Key", "Entries", "Type", "Description")
        self.registry_tree = ttk.Treeview(registry_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.registry_tree.heading(col, text=col)
            self.registry_tree.column(col, width=180)
        
        # Scrollbar
        registry_scrollbar = ttk.Scrollbar(registry_frame, orient="vertical", command=self.registry_tree.yview)
        self.registry_tree.configure(yscrollcommand=registry_scrollbar.set)
        
        self.registry_tree.pack(side="left", fill="both", expand=True)
        registry_scrollbar.pack(side="right", fill="y")
    
    def create_network_results_tab(self):
        """Create network traces results tab"""
        import tkinter as tk
        from tkinter import ttk
        
        network_frame = ttk.Frame(self.results_notebook, style="Modern.TFrame", padding="10")
        self.results_notebook.add(network_frame, text="🌐 Network Traces")
        
        # Network treeview
        columns = ("Trace Type", "Entries", "Size", "Description")
        self.network_tree = ttk.Treeview(network_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.network_tree.heading(col, text=col)
            self.network_tree.column(col, width=180)
        
        # Scrollbar
        network_scrollbar = ttk.Scrollbar(network_frame, orient="vertical", command=self.network_tree.yview)
        self.network_tree.configure(yscrollcommand=network_scrollbar.set)
        
        self.network_tree.pack(side="left", fill="both", expand=True)
        network_scrollbar.pack(side="right", fill="y")
    
    def create_summary_tab(self):
        """Create scan summary tab"""
        import tkinter as tk
        from tkinter import ttk
        
        summary_frame = ttk.Frame(self.results_notebook, style="Modern.TFrame", padding="20")
        self.results_notebook.add(summary_frame, text="📊 Summary")
        
        # Summary cards
        self.create_summary_cards(summary_frame)
    
    def create_summary_cards(self, parent):
        """Create summary cards"""
        import tkinter as tk
        from tkinter import ttk
        
        # Summary grid
        summary_grid = ttk.Frame(parent, style="Modern.TFrame")
        summary_grid.pack(fill="x", pady=(0, 20))
        
        # Create summary cards
        self.create_summary_card(summary_grid, "🌐 Browser Data", "0 items", "browser_summary", row=0, col=0)
        self.create_summary_card(summary_grid, "👁️ Tracking Files", "0 files", "tracking_summary", row=0, col=1)
        self.create_summary_card(summary_grid, "📄 Recent Docs", "0 documents", "docs_summary", row=1, col=0)
        self.create_summary_card(summary_grid, "🖥️ System Traces", "0 MB", "system_summary", row=1, col=1)
        
        # Configure grid
        for i in range(2):
            summary_grid.grid_rowconfigure(i, weight=1)
            summary_grid.grid_columnconfigure(i, weight=1)
        
        # Privacy score
        score_frame = ttk.LabelFrame(parent, text="🛡️ Privacy Score", padding="15")
        score_frame.pack(fill="x", pady=(0, 20))
        
        self.privacy_score_label = ttk.Label(score_frame, text="Privacy Score: Calculating...",
                                            font=("Segoe UI", 16, "bold"),
                                            background=self.main_window.colors['bg_light'],
                                            foreground=self.main_window.colors['accent'])
        self.privacy_score_label.pack()
        
        self.privacy_score_desc = ttk.Label(score_frame, text="Run a privacy scan to see your privacy score",
                                           background=self.main_window.colors['bg_light'],
                                           foreground=self.main_window.colors['text_gray'])
        self.privacy_score_desc.pack(pady=(5, 0))
        
        # Recommendations
        recommendations_frame = ttk.LabelFrame(parent, text="💡 Recommendations", padding="15")
        recommendations_frame.pack(fill="both", expand=True)
        
        self.recommendations_text = tk.Text(recommendations_frame, height=10, wrap=tk.WORD,
                                           bg=self.main_window.colors['bg_light'],
                                           fg=self.main_window.colors['text_white'],
                                           font=("Segoe UI", 10))
        recommendations_scrollbar = ttk.Scrollbar(recommendations_frame, orient="vertical", 
                                                 command=self.recommendations_text.yview)
        self.recommendations_text.configure(yscrollcommand=recommendations_scrollbar.set)
        
        self.recommendations_text.pack(side="left", fill="both", expand=True)
        recommendations_scrollbar.pack(side="right", fill="y")
        
        # Initial recommendations
        self.update_recommendations()
    
    def create_summary_card(self, parent, title, value, card_type, row, col):
        """Create summary card"""
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
        setattr(self, f"{card_type}_label", value_label)
    
    def start_privacy_scan(self):
        """Start privacy scan"""
        if self.scanning:
            return
        
        self.scanning = True
        self.scan_btn.config(state='disabled', text="🔄 Scanning...")
        self.clean_btn.config(state='disabled')
        self.scan_progress.start()
        self.scan_status_label.config(text="Starting privacy scan...")
        
        # Start scan in background thread
        scan_thread = threading.Thread(target=self.privacy_scan_worker, daemon=True)
        scan_thread.start()
    
    def privacy_scan_worker(self):
        """Privacy scan worker thread"""
        try:
            # Clear previous results
            self.scan_results = {category: {} if category == 'browser_data' else [] 
                               for category in self.scan_results.keys()}
            
            # Scan enabled categories
            for category_id, category_data in self.privacy_categories.items():
                if not category_data['enabled']:
                    continue
                
                self.privacy_window.after(0, lambda cat=category_data['name']: 
                                        self.scan_status_label.config(text=f"Scanning {cat}..."))
                
                if category_id == 'browser_data':
                    self.scan_browser_data()
                elif category_id == 'tracking_files':
                    self.scan_tracking_files()
                elif category_id == 'recent_documents':
                    self.scan_recent_documents()
                elif category_id == 'system_traces':
                    self.scan_system_traces()
                elif category_id == 'registry_traces':
                    self.scan_registry_traces()
                elif category_id == 'network_traces':
                    self.scan_network_traces()
            
            # Update UI with results
            self.privacy_window.after(0, self.update_scan_results)
            
        except Exception as e:
            self.privacy_window.after(0, lambda: self.scan_error(str(e)))
    
    def scan_browser_data(self):
        """Scan browser data"""
        for browser_id, browser_info in self.browser_paths.items():
            browser_results = {}
            
            for data_type, path in browser_info['paths'].items():
                if not os.path.exists(path):
                    continue
                
                try:
                    if data_type == 'cookies':
                        items, size = self.scan_cookies(path)
                    elif data_type == 'cache':
                        items, size = self.scan_cache(path)
                    elif data_type == 'history':
                        items, size = self.scan_history(path)
                    else:
                        items, size = self.scan_generic_browser_data(path)
                    
                    if items > 0:
                        browser_results[data_type] = {
                            'items': items,
                            'size': size,
                            'path': path
                        }
                        
                except Exception as e:
                    print(f"Browser scan error ({browser_id}, {data_type}): {e}")
            
            if browser_results:
                self.scan_results['browser_data'][browser_id] = {
                    'name': browser_info['name'],
                    'data': browser_results
                }
    
    def scan_cookies(self, cookies_path):
        """Scan browser cookies"""
        try:
            if not os.path.exists(cookies_path):
                return 0, 0
            
            # For Chrome/Edge cookies (SQLite database)
            if cookies_path.endswith('Cookies'):
                try:
                    conn = sqlite3.connect(cookies_path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM cookies")
                    count = cursor.fetchone()[0]
                    conn.close()
                    size = os.path.getsize(cookies_path)
                    return count, size
                except:
                    return 0, 0
            
            # For Firefox (multiple files in profile)
            elif 'Firefox' in cookies_path:
                count = 0
                size = 0
                for profile_dir in glob.glob(os.path.join(cookies_path, '*.default*')):
                    cookies_file = os.path.join(profile_dir, 'cookies.sqlite')
                    if os.path.exists(cookies_file):
                        try:
                            conn = sqlite3.connect(cookies_file)
                            cursor = conn.cursor()
                            cursor.execute("SELECT COUNT(*) FROM moz_cookies")
                            count += cursor.fetchone()[0]
                            conn.close()
                            size += os.path.getsize(cookies_file)
                        except:
                            pass
                return count, size
            
        except Exception as e:
            print(f"Cookie scan error: {e}")
        
        return 0, 0
    
    def scan_cache(self, cache_path):
        """Scan browser cache"""
        try:
            if not os.path.exists(cache_path):
                return 0, 0
            
            total_files = 0
            total_size = 0
            
            for root, dirs, files in os.walk(cache_path):
                total_files += len(files)
                for file in files:
                    try:
                        file_path = os.path.join(root, file)
                        total_size += os.path.getsize(file_path)
                    except:
                        pass
            
            return total_files, total_size
            
        except Exception as e:
            print(f"Cache scan error: {e}")
            return 0, 0
    
    def scan_history(self, history_path):
        """Scan browser history"""
        try:
            if not os.path.exists(history_path):
                return 0, 0
            
            # Chrome/Edge history
            if history_path.endswith('History'):
                try:
                    # Make a copy to avoid locking issues
                    temp_history = history_path + '_temp'
                    shutil.copy2(history_path, temp_history)
                    
                    conn = sqlite3.connect(temp_history)
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM urls")
                    count = cursor.fetchone()[0]
                    conn.close()
                    
                    # Clean up temp file
                    try:
                        os.remove(temp_history)
                    except:
                        pass
                    
                    size = os.path.getsize(history_path)
                    return count, size
                except Exception as e:
                    print(f"History scan error: {e}")
                    return 0, 0
            
            # Firefox history
            elif 'Firefox' in history_path:
                count = 0
                size = 0
                for profile_dir in glob.glob(os.path.join(history_path, '*.default*')):
                    places_file = os.path.join(profile_dir, 'places.sqlite')
                    if os.path.exists(places_file):
                        try:
                            temp_places = places_file + '_temp'
                            shutil.copy2(places_file, temp_places)
                            
                            conn = sqlite3.connect(temp_places)
                            cursor = conn.cursor()
                            cursor.execute("SELECT COUNT(*) FROM moz_places")
                            count += cursor.fetchone()[0]
                            conn.close()
                            
                            # Clean up
                            try:
                                os.remove(temp_places)
                            except:
                                pass
                            
                            size += os.path.getsize(places_file)
                        except:
                            pass
                return count, size
            
        except Exception as e:
            print(f"History scan error: {e}")
        
        return 0, 0
    
    def scan_generic_browser_data(self, path):
        """Scan generic browser data"""
        try:
            if os.path.isfile(path):
                return 1, os.path.getsize(path)
            elif os.path.isdir(path):
                total_files = 0
                total_size = 0
                
                for root, dirs, files in os.walk(path):
                    total_files += len(files)
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            total_size += os.path.getsize(file_path)
                        except:
                            pass
                
                return total_files, total_size
        except:
            pass
        
        return 0, 0
    
    def scan_tracking_files(self):
        """Scan tracking files"""
        tracking_patterns = [
            '*tracking*',
            '*analytics*',
            '*beacon*',
            '*telemetry*',
            '*metrics*'
        ]
        
        search_paths = [
            os.path.expanduser('~\\AppData\\Local'),
            os.path.expanduser('~\\AppData\\Roaming'),
            'C:\\ProgramData'
        ]
        
        for search_path in search_paths:
            if not os.path.exists(search_path):
                continue
            
            for pattern in tracking_patterns:
                try:
                    for file_path in glob.glob(os.path.join(search_path, '**', pattern), recursive=True):
                        if os.path.isfile(file_path):
                            try:
                                stat = os.stat(file_path)
                                self.scan_results['tracking_files'].append({
                                    'path': file_path,
                                    'size': stat.st_size,
                                    'modified': stat.st_mtime,
                                    'type': 'Tracking File'
                                })
                            except:
                                pass
                except:
                    pass
    
    def scan_recent_documents(self):
        """Scan recent documents"""
        try:
            # Windows Recent folder
            recent_path = self.system_paths['recent']
            if os.path.exists(recent_path):
                for file in os.listdir(recent_path):
                    file_path = os.path.join(recent_path, file)
                    if os.path.isfile(file_path):
                        try:
                            stat = os.stat(file_path)
                            self.scan_results['recent_documents'].append({
                                'name': file,
                                'path': file_path,
                                'size': stat.st_size,
                                'accessed': stat.st_atime,
                                'type': 'Recent Document'
                            })
                        except:
                            pass
            
            # Jump lists
            jumplists_path = self.system_paths['jumplists']
            if os.path.exists(jumplists_path):
                for file in os.listdir(jumplists_path):
                    file_path = os.path.join(jumplists_path, file)
                    if os.path.isfile(file_path):
                        try:
                            stat = os.stat(file_path)
                            self.scan_results['recent_documents'].append({
                                'name': file,
                                'path': file_path,
                                'size': stat.st_size,
                                'accessed': stat.st_atime,
                                'type': 'Jump List'
                            })
                        except:
                            pass
                            
        except Exception as e:
            print(f"Recent documents scan error: {e}")
    
    def scan_system_traces(self):
        """Scan system traces"""
        try:
            # Temporary files
            for temp_path in self.system_paths['temp']:
                if os.path.exists(temp_path):
                    total_files, total_size = self.count_files_in_directory(temp_path)
                    if total_files > 0:
                        self.scan_results['system_traces'].append({
                            'type': 'Temporary Files',
                            'path': temp_path,
                            'files': total_files,
                            'size': total_size
                        })
            
            # Prefetch files
            prefetch_path = self.system_paths['prefetch']
            if os.path.exists(prefetch_path):
                total_files, total_size = self.count_files_in_directory(prefetch_path)
                if total_files > 0:
                    self.scan_results['system_traces'].append({
                        'type': 'Prefetch Files',
                        'path': prefetch_path,
                        'files': total_files,
                        'size': total_size
                    })
            
            # Thumbnail cache
            thumbnail_path = self.system_paths['thumbnail_cache']
            if os.path.exists(thumbnail_path):
                total_files, total_size = self.count_files_in_directory(thumbnail_path, '*.db')
                if total_files > 0:
                    self.scan_results['system_traces'].append({
                        'type': 'Thumbnail Cache',
                        'path': thumbnail_path,
                        'files': total_files,
                        'size': total_size
                    })
                    
        except Exception as e:
            print(f"System traces scan error: {e}")
    
    def count_files_in_directory(self, directory, pattern='*'):
        """Count files in directory"""
        try:
            total_files = 0
            total_size = 0
            
            if pattern == '*':
                for root, dirs, files in os.walk(directory):
                    total_files += len(files)
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            total_size += os.path.getsize(file_path)
                        except:
                            pass
            else:
                for file_path in glob.glob(os.path.join(directory, pattern)):
                    if os.path.isfile(file_path):
                        total_files += 1
                        try:
                            total_size += os.path.getsize(file_path)
                        except:
                            pass
            
            return total_files, total_size
            
        except Exception as e:
            print(f"File count error: {e}")
            return 0, 0
    
    def scan_registry_traces(self):
        """Scan registry traces"""
        try:
            for reg_key, reg_path in self.registry_paths.items():
                try:
                    # Split registry path
                    hive, subkey = reg_path.split('\\\\', 1)
                    
                    # Map hive names
                    hive_map = {
                        'HKEY_CURRENT_USER': winreg.HKEY_CURRENT_USER,
                        'HKEY_LOCAL_MACHINE': winreg.HKEY_LOCAL_MACHINE
                    }
                    
                    if hive in hive_map:
                        try:
                            key = winreg.OpenKey(hive_map[hive], subkey)
                            
                            # Count values
                            value_count = 0
                            try:
                                while True:
                                    winreg.EnumValue(key, value_count)
                                    value_count += 1
                            except WindowsError:
                                pass
                            
                            winreg.CloseKey(key)
                            
                            if value_count > 0:
                                self.scan_results['registry_traces'].append({
                                    'key': reg_key,
                                    'path': reg_path,
                                    'entries': value_count,
                                    'type': 'Privacy Trace'
                                })
                                
                        except WindowsError:
                            pass
                            
                except Exception as e:
                    print(f"Registry scan error ({reg_key}): {e}")
                    
        except Exception as e:
            print(f"Registry traces scan error: {e}")
    
    def scan_network_traces(self):
        """Scan network traces"""
        try:
            # DNS cache
            try:
                import subprocess
                result = subprocess.run(['ipconfig', '/displaydns'], capture_output=True, text=True)
                if result.returncode == 0 and result.stdout:
                    dns_entries = len([line for line in result.stdout.split('\n') if 'Record Name' in line])
                    self.scan_results['network_traces'].append({
                        'type': 'DNS Cache',
                        'entries': dns_entries,
                        'size': len(result.stdout),
                        'description': 'Cached DNS queries'
                    })
            except:
                pass
            
            # Network logs (if accessible)
            network_log_paths = [
                'C:\\Windows\\System32\\LogFiles\\WMI',
                'C:\\Windows\\System32\\winevt\\Logs'
            ]
            
            for log_path in network_log_paths:
                if os.path.exists(log_path):
                    try:
                        files, size = self.count_files_in_directory(log_path, '*.etl')
                        if files > 0:
                            self.scan_results['network_traces'].append({
                                'type': 'Network Logs',
                                'entries': files,
                                'size': size,
                                'description': 'Network activity logs'
                            })
                    except:
                        pass
                        
        except Exception as e:
            print(f"Network traces scan error: {e}")
    
    def update_scan_results(self):
        """Update scan results in UI"""
        try:
            # Update browser results
            self.update_browser_results()
            
            # Update tracking results
            self.update_tracking_results()
            
            # Update documents results
            self.update_documents_results()
            
            # Update system results
            self.update_system_results()
            
            # Update registry results
            self.update_registry_results()
            
            # Update network results
            self.update_network_results()
            
            # Update summary
            self.update_summary()
            
            # Calculate privacy score
            self.calculate_privacy_score()
            
            # Finish scan
            self.scanning = False
            self.scan_btn.config(state='normal', text="🔍 Privacy Scan")
            self.clean_btn.config(state='normal')
            self.scan_progress.stop()
            self.scan_status_label.config(text="Scan completed successfully!")
            
        except Exception as e:
            self.scan_error(str(e))
    
    def update_browser_results(self):
        """Update browser results display"""
        # Clear existing items
        for item in self.browser_tree.get_children():
            self.browser_tree.delete(item)
        
        for browser_id, browser_results in self.scan_results['browser_data'].items():
            browser_name = browser_results['name']
            
            for data_type, data_info in browser_results['data'].items():
                self.browser_tree.insert('', 'end', values=(
                    browser_name,
                    data_type.replace('_', ' ').title(),
                    f"{data_info['items']:,}",
                    f"{data_info['size'] / (1024*1024):.1f} MB",
                    data_info['path']
                ))
    
    def update_tracking_results(self):
        """Update tracking results display"""
        # Clear existing items
        for item in self.tracking_tree.get_children():
            self.tracking_tree.delete(item)
        
        for tracking_file in self.scan_results['tracking_files']:
            import time
            modified_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(tracking_file['modified']))
            
            self.tracking_tree.insert('', 'end', values=(
                tracking_file['type'],
                tracking_file['path'],
                f"{tracking_file['size'] / 1024:.1f} KB",
                modified_time
            ))
    
    def update_documents_results(self):
        """Update documents results display"""
        # Clear existing items
        for item in self.docs_tree.get_children():
            self.docs_tree.delete(item)
        
        for doc in self.scan_results['recent_documents']:
            import time
            accessed_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(doc['accessed']))
            
            self.docs_tree.insert('', 'end', values=(
                doc['name'],
                doc['type'],
                accessed_time,
                doc['path']
            ))
    
    def update_system_results(self):
        """Update system results display"""
        # Clear existing items
        for item in self.system_tree.get_children():
            self.system_tree.delete(item)
        
        for trace in self.scan_results['system_traces']:
            self.system_tree.insert('', 'end', values=(
                trace['type'],
                f"{trace['files']:,}",
                f"{trace['size'] / (1024*1024):.1f} MB",
                trace['path']
            ))
    
    def update_registry_results(self):
        """Update registry results display"""
        # Clear existing items
        for item in self.registry_tree.get_children():
            self.registry_tree.delete(item)
        
        for trace in self.scan_results['registry_traces']:
            self.registry_tree.insert('', 'end', values=(
                trace['key'].replace('_', ' ').title(),
                f"{trace['entries']:,}",
                trace['type'],
                trace['path']
            ))
    
    def update_network_results(self):
        """Update network results display"""
        # Clear existing items
        for item in self.network_tree.get_children():
            self.network_tree.delete(item)
        
        for trace in self.scan_results['network_traces']:
            self.network_tree.insert('', 'end', values=(
                trace['type'],
                f"{trace['entries']:,}",
                f"{trace['size'] / 1024:.1f} KB",
                trace['description']
            ))
    
    def update_summary(self):
        """Update summary display"""
        # Count totals
        browser_count = sum(len(browser['data']) for browser in self.scan_results['browser_data'].values())
        tracking_count = len(self.scan_results['tracking_files'])
        docs_count = len(self.scan_results['recent_documents'])
        system_size = sum(trace['size'] for trace in self.scan_results['system_traces'])
        
        # Update summary cards
        self.browser_summary_label.config(text=f"{browser_count} items")
        self.tracking_summary_label.config(text=f"{tracking_count} files")
        self.docs_summary_label.config(text=f"{docs_count} documents")
        self.system_summary_label.config(text=f"{system_size / (1024*1024):.1f} MB")
    
    def calculate_privacy_score(self):
        """Calculate privacy score"""
        try:
            score = 100  # Start with perfect score
            
            # Deduct points based on findings
            browser_items = sum(len(browser['data']) for browser in self.scan_results['browser_data'].values())
            tracking_files = len(self.scan_results['tracking_files'])
            recent_docs = len(self.scan_results['recent_documents'])
            system_traces = len(self.scan_results['system_traces'])
            registry_traces = len(self.scan_results['registry_traces'])
            network_traces = len(self.scan_results['network_traces'])
            
            # Scoring algorithm
            score -= min(browser_items * 2, 30)  # Max 30 points for browser data
            score -= min(tracking_files * 3, 25)  # Max 25 points for tracking files
            score -= min(recent_docs * 1, 15)    # Max 15 points for recent docs
            score -= min(system_traces * 2, 20)  # Max 20 points for system traces
            score -= min(registry_traces * 2, 10) # Max 10 points for registry traces
            score -= min(network_traces * 1, 10)  # Max 10 points for network traces
            
            score = max(0, score)  # Don't go below 0
            
            # Update UI
            color = self.get_score_color(score)
            status = self.get_score_status(score)
            
            self.privacy_score_label.config(text=f"Privacy Score: {score}/100", foreground=color)
            self.privacy_score_desc.config(text=f"Status: {status}")
            
        except Exception as e:
            print(f"Privacy score calculation error: {e}")
            self.privacy_score_label.config(text="Privacy Score: Error")
            self.privacy_score_desc.config(text="Unable to calculate score")
    
    def get_score_color(self, score):
        """Get color based on privacy score"""
        if score >= 80:
            return self.main_window.colors['success']
        elif score >= 60:
            return self.main_window.colors['warning']
        else:
            return self.main_window.colors['danger']
    
    def get_score_status(self, score):
        """Get status text based on privacy score"""
        if score >= 90:
            return "Excellent Privacy Protection"
        elif score >= 80:
            return "Good Privacy Protection"
        elif score >= 60:
            return "Fair Privacy Protection"
        elif score >= 40:
            return "Poor Privacy Protection"
        else:
            return "Critical Privacy Issues"
    
    def update_recommendations(self):
        """Update privacy recommendations"""
        recommendations = [
            "🔍 Run a privacy scan to identify potential privacy risks",
            "🌐 Clear browser data regularly (cookies, cache, history)",
            "👁️ Remove tracking files and analytics data",
            "📄 Clean recent documents and jump lists",
            "🖥️ Clear system traces and temporary files",
            "📋 Clean registry traces (advanced users)",
            "🌐 Flush DNS cache and clear network traces",
            "🔒 Use private browsing mode when possible",
            "🛡️ Install privacy-focused browser extensions",
            "⚙️ Review and adjust privacy settings in applications"
        ]
        
        self.recommendations_text.delete(1.0, 'end')
        for recommendation in recommendations:
            self.recommendations_text.insert('end', f"{recommendation}\n\n")
        
        self.recommendations_text.config(state='disabled')
    
    def scan_error(self, error_msg):
        """Handle scan error"""
        self.scanning = False
        self.scan_btn.config(state='normal', text="🔍 Privacy Scan")
        self.scan_progress.stop()
        self.scan_status_label.config(text=f"Scan failed: {error_msg}")
        
        messagebox.showerror("Privacy Scan Error", f"Privacy scan failed:\n{error_msg}")
    
    def clean_selected_items(self):
        """Clean selected privacy items"""
        if messagebox.askyesno("Confirm Cleanup", 
                              "This will permanently delete selected privacy data.\n\nContinue?",
                              icon='warning'):
            self.start_privacy_cleanup()
    
    def start_privacy_cleanup(self):
        """Start privacy cleanup"""
        cleanup_thread = threading.Thread(target=self.privacy_cleanup_worker, daemon=True)
        cleanup_thread.start()
    
    def privacy_cleanup_worker(self):
        """Privacy cleanup worker thread"""
        try:
            cleaned_items = []
            
            # Clean browser data
            for browser_id, browser_results in self.scan_results['browser_data'].items():
                for data_type, data_info in browser_results['data'].items():
                    if self.clean_browser_data(data_info['path'], data_type):
                        cleaned_items.append(f"{browser_results['name']} {data_type}")
            
            # Clean tracking files
            for tracking_file in self.scan_results['tracking_files']:
                if self.clean_file(tracking_file['path']):
                    cleaned_items.append(f"Tracking file: {os.path.basename(tracking_file['path'])}")
            
            # Clean recent documents
            for doc in self.scan_results['recent_documents']:
                if self.clean_file(doc['path']):
                    cleaned_items.append(f"Recent document: {doc['name']}")
            
            # Clean system traces
            for trace in self.scan_results['system_traces']:
                if self.clean_directory(trace['path']):
                    cleaned_items.append(f"System trace: {trace['type']}")
            
            # Show results
            self.privacy_window.after(0, lambda: self.cleanup_completed(cleaned_items))
            
        except Exception as e:
            self.privacy_window.after(0, lambda: self.cleanup_error(str(e)))
    
    def clean_browser_data(self, path, data_type):
        """Clean specific browser data"""
        try:
            if data_type in ['cookies', 'history', 'form_data']:
                # For SQLite databases, clear tables instead of deleting files
                if path.endswith(('Cookies', 'History', 'Web Data')):
                    try:
                        # Make backup first
                        backup_path = path + '.backup'
                        shutil.copy2(path, backup_path)
                        
                        conn = sqlite3.connect(path)
                        cursor = conn.cursor()
                        
                        if data_type == 'cookies':
                            cursor.execute("DELETE FROM cookies")
                        elif data_type == 'history':
                            cursor.execute("DELETE FROM urls")
                            cursor.execute("DELETE FROM visits")
                        elif data_type == 'form_data':
                            cursor.execute("DELETE FROM autofill")
                        
                        conn.commit()
                        conn.close()
                        
                        # Remove backup if successful
                        os.remove(backup_path)
                        return True
                        
                    except Exception as e:
                        # Restore backup on error
                        if os.path.exists(backup_path):
                            shutil.copy2(backup_path, path)
                            os.remove(backup_path)
                        return False
            
            elif data_type == 'cache':
                return self.clean_directory(path)
            
            else:
                return self.clean_file(path)
                
        except Exception as e:
            print(f"Browser data cleanup error: {e}")
            return False
    
    def clean_file(self, file_path):
        """Clean a single file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
        except Exception as e:
            print(f"File cleanup error ({file_path}): {e}")
        return False
    
    def clean_directory(self, dir_path):
        """Clean directory contents"""
        try:
            if os.path.exists(dir_path):
                for root, dirs, files in os.walk(dir_path):
                    for file in files:
                        try:
                            os.remove(os.path.join(root, file))
                        except:
                            pass
                    
                    # Remove empty directories
                    for dir in dirs:
                        try:
                            dir_full_path = os.path.join(root, dir)
                            if not os.listdir(dir_full_path):
                                os.rmdir(dir_full_path)
                        except:
                            pass
                return True
        except Exception as e:
            print(f"Directory cleanup error ({dir_path}): {e}")
        return False
    
    def cleanup_completed(self, cleaned_items):
        """Handle cleanup completion"""
        if cleaned_items:
            message = f"Privacy cleanup completed!\n\nCleaned {len(cleaned_items)} items:\n\n"
            message += "\n".join(f"✅ {item}" for item in cleaned_items[:10])
            if len(cleaned_items) > 10:
                message += f"\n... and {len(cleaned_items) - 10} more items"
        else:
            message = "No items were cleaned. Some files may be in use."
        
        messagebox.showinfo("Cleanup Complete", message)
        
        if hasattr(self.main_window, 'add_activity'):
            self.main_window.add_activity(f"Privacy cleanup: {len(cleaned_items)} items cleaned", "Başarılı")
        
        # Refresh scan results
        self.start_privacy_scan()
    
    def cleanup_error(self, error_msg):
        """Handle cleanup error"""
        messagebox.showerror("Cleanup Error", f"Privacy cleanup failed:\n{error_msg}")
    
    def update_category_settings(self):
        """Update category settings"""
        for category_id, var in self.category_vars.items():
            self.privacy_categories[category_id]['enabled'] = var.get()
        
        self.save_settings()
    
    def select_all_categories(self):
        """Select all categories"""
        for var in self.category_vars.values():
            var.set(True)
        self.update_category_settings()
    
    def select_no_categories(self):
        """Select no categories"""
        for var in self.category_vars.values():
            var.set(False)
        self.update_category_settings()
    
    def show_privacy_settings(self):
        """Show privacy settings window"""
        messagebox.showinfo("Privacy Settings", "Advanced privacy settings will be implemented here.\n\nPlanned features:\n• Custom scan locations\n• Exclusion lists\n• Scheduled scans\n• Privacy profiles")
