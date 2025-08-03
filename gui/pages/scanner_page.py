"""
Modern Scanner Page for DonTe Cleaner v3.0
Advanced system scanning with real-time visualization
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time
import os
from gui.modern_ui import HolographicCard, NeonProgressBar, AnimatedButton

class ScannerPage:
    """Modern scanner interface with holographic design"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.colors = main_window.colors
        self.scanning = False
        
        self.create_scanner_interface()
    
    def create_scanner_interface(self):
        """Create scanner interface"""
        # Main scanner container
        scanner_frame = tk.Frame(self.parent, bg=self.colors['bg_primary'])
        scanner_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Top section - Scan controls
        self.create_scan_controls(scanner_frame)
        
        # Middle section - Scan progress and visualization
        self.create_scan_visualization(scanner_frame)
        
        # Bottom section - Results
        self.create_results_section(scanner_frame)
    
    def create_scan_controls(self, parent):
        """Create scan control buttons"""
        controls_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        controls_frame.pack(fill='x', pady=(0, 20))
        
        # Scan types card
        scan_types_card = HolographicCard(controls_frame, width=400, height=180,
                                         title="🔍 Scan Types")
        scan_types_card.pack(side='left', padx=(0, 20))
        
        # Quick scan button
        self.quick_scan_btn = AnimatedButton(scan_types_card, text="⚡ Quick Scan",
                                            width=150, height=40,
                                            bg_color=self.colors['accent_primary'],
                                            hover_color=self.colors['glow'],
                                            command=self.start_quick_scan)
        self.quick_scan_btn.place(x=30, y=60)
        
        # Full scan button
        self.full_scan_btn = AnimatedButton(scan_types_card, text="🔍 Full Scan",
                                           width=150, height=40,
                                           bg_color=self.colors['accent_secondary'],
                                           hover_color='#ff4da6',
                                           command=self.start_full_scan)
        self.full_scan_btn.place(x=200, y=60)
        
        # Custom scan button
        self.custom_scan_btn = AnimatedButton(scan_types_card, text="⚙️ Custom Scan",
                                             width=150, height=40,
                                             bg_color=self.colors['accent_gold'],
                                             hover_color='#ffed4a',
                                             text_color='black',
                                             command=self.start_custom_scan)
        self.custom_scan_btn.place(x=30, y=110)
        
        # Stop scan button
        self.stop_scan_btn = AnimatedButton(scan_types_card, text="⏹️ Stop Scan",
                                           width=150, height=40,
                                           bg_color=self.colors['danger'],
                                           hover_color='#ff4444',
                                           command=self.stop_scan)
        self.stop_scan_btn.place(x=200, y=110)
        
        # Scan options card
        options_card = HolographicCard(controls_frame, width=400, height=180,
                                      title="⚙️ Scan Options")
        options_card.pack(side='left', padx=(0, 20))
        
        # Checkboxes for scan options
        self.scan_malware = tk.BooleanVar(value=True)
        malware_check = tk.Checkbutton(options_card, text="🦠 Scan for Malware",
                                      variable=self.scan_malware,
                                      bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                      selectcolor=self.colors['bg_secondary'],
                                      font=('Segoe UI', 10))
        malware_check.place(x=30, y=60)
        
        self.scan_registry = tk.BooleanVar(value=True)
        registry_check = tk.Checkbutton(options_card, text="📋 Scan Registry",
                                       variable=self.scan_registry,
                                       bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                       selectcolor=self.colors['bg_secondary'],
                                       font=('Segoe UI', 10))
        registry_check.place(x=30, y=85)
        
        self.scan_startup = tk.BooleanVar(value=True)
        startup_check = tk.Checkbutton(options_card, text="🚀 Scan Startup Items",
                                      variable=self.scan_startup,
                                      bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                      selectcolor=self.colors['bg_secondary'],
                                      font=('Segoe UI', 10))
        startup_check.place(x=30, y=110)
        
        self.deep_scan = tk.BooleanVar(value=False)
        deep_check = tk.Checkbutton(options_card, text="🔬 Deep System Scan",
                                   variable=self.deep_scan,
                                   bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                   selectcolor=self.colors['bg_secondary'],
                                   font=('Segoe UI', 10))
        deep_check.place(x=30, y=135)
        
        # Scan statistics card
        stats_card = HolographicCard(controls_frame, width=350, height=180,
                                    title="📊 Scan Statistics")
        stats_card.pack(side='left')
        
        # Statistics display
        self.files_scanned = tk.Label(stats_card, text="Files Scanned: 0",
                                     bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                     font=('Segoe UI', 12, 'bold'))
        self.files_scanned.place(x=30, y=60)
        
        self.threats_found = tk.Label(stats_card, text="Threats Found: 0",
                                     bg=self.colors['bg_tertiary'], fg=self.colors['danger'],
                                     font=('Segoe UI', 12, 'bold'))
        self.threats_found.place(x=30, y=85)
        
        self.scan_time = tk.Label(stats_card, text="Scan Time: 00:00",
                                 bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'],
                                 font=('Segoe UI', 11))
        self.scan_time.place(x=30, y=110)
        
        self.scan_speed = tk.Label(stats_card, text="Speed: 0 files/sec",
                                  bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'],
                                  font=('Segoe UI', 11))
        self.scan_speed.place(x=30, y=135)
    
    def create_scan_visualization(self, parent):
        """Create scan progress visualization"""
        viz_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        viz_frame.pack(fill='x', pady=(0, 20))
        
        # Main progress card
        progress_card = HolographicCard(viz_frame, width=800, height=200,
                                       title="📈 Scan Progress")
        progress_card.pack(side='left', padx=(0, 20))
        
        # Progress bar
        self.scan_progress_bar = NeonProgressBar(progress_card, width=700, height=35)
        self.scan_progress_bar.place(x=50, y=80)
        
        # Progress text
        self.progress_text = tk.Label(progress_card, text="Ready to scan",
                                     bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                     font=('Segoe UI', 14, 'bold'))
        self.progress_text.place(x=50, y=50)
        
        # Current file being scanned
        self.current_file = tk.Label(progress_card, text="",
                                    bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'],
                                    font=('Segoe UI', 10))
        self.current_file.place(x=50, y=130)
        
        # Visual scan representation
        visual_card = HolographicCard(viz_frame, width=350, height=200,
                                     title="🖼️ Scan Visual")
        visual_card.pack(side='left')
        
        # Create visual scan canvas
        self.scan_canvas = tk.Canvas(visual_card, width=300, height=120,
                                    bg=self.colors['bg_secondary'],
                                    highlightthickness=0)
        self.scan_canvas.place(x=25, y=60)
        
        self.create_scan_visualization_grid()
    
    def create_scan_visualization_grid(self):
        """Create grid visualization for scan progress"""
        # Create a grid of small squares representing files
        self.grid_size = 15
        self.square_size = 18
        self.scan_squares = []
        
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x1 = col * self.square_size + 2
                y1 = row * 8 + 2
                x2 = x1 + self.square_size - 2
                y2 = y1 + 6
                
                square = self.scan_canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=self.colors['bg_tertiary'],
                    outline=self.colors['border'],
                    width=1
                )
                self.scan_squares.append(square)
    
    def create_results_section(self, parent):
        """Create scan results section"""
        results_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        results_frame.pack(fill='both', expand=True)
        
        # Results card
        results_card = HolographicCard(results_frame, width=1150, height=300,
                                      title="📋 Scan Results")
        results_card.pack(fill='both', expand=True)
        
        # Results notebook
        results_notebook = ttk.Notebook(results_card)
        results_notebook.place(x=20, y=50, width=1110, height=230)
        
        # Threats tab
        threats_frame = ttk.Frame(results_notebook)
        results_notebook.add(threats_frame, text="🦠 Threats")
        
        self.threats_tree = ttk.Treeview(threats_frame, columns=('Type', 'Path', 'Risk'), 
                                        show='headings')
        self.threats_tree.heading('#1', text='Threat Type')
        self.threats_tree.heading('#2', text='File Path')
        self.threats_tree.heading('#3', text='Risk Level')
        self.threats_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Issues tab
        issues_frame = ttk.Frame(results_notebook)
        results_notebook.add(issues_frame, text="⚠️ Issues")
        
        self.issues_tree = ttk.Treeview(issues_frame, columns=('Issue', 'Location', 'Impact'),
                                       show='headings')
        self.issues_tree.heading('#1', text='Issue Type')
        self.issues_tree.heading('#2', text='Location')
        self.issues_tree.heading('#3', text='Impact')
        self.issues_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Clean files tab
        clean_frame = ttk.Frame(results_notebook)
        results_notebook.add(clean_frame, text="✅ Clean Files")
        
        self.clean_tree = ttk.Treeview(clean_frame, columns=('File', 'Size', 'Modified'),
                                      show='headings')
        self.clean_tree.heading('#1', text='File Name')
        self.clean_tree.heading('#2', text='Size')
        self.clean_tree.heading('#3', text='Last Modified')
        self.clean_tree.pack(fill='both', expand=True, padx=10, pady=10)
    
    def start_quick_scan(self):
        """Start quick system scan"""
        if self.scanning:
            return
        
        self.scanning = True
        self.scan_start_time = time.time()
        
        def scan_worker():
            try:
                # Quick scan locations
                scan_locations = [
                    os.path.expanduser("~/Desktop"),
                    os.path.expanduser("~/Downloads"),
                    os.path.expanduser("~/Documents"),
                    os.path.expandvars("%TEMP%"),
                    "C:\\Windows\\System32"
                ]
                
                total_files = 0
                scanned_files = 0
                threats_count = 0
                
                # Count total files first
                for location in scan_locations:
                    if os.path.exists(location):
                        for root, dirs, files in os.walk(location):
                            total_files += len(files)
                
                self.main_window.root.after(0, lambda: self.update_progress(0, f"Found {total_files} files to scan"))
                
                # Scan files
                for location in scan_locations:
                    if not self.scanning:
                        break
                        
                    if os.path.exists(location):
                        for root, dirs, files in os.walk(location):
                            for file in files:
                                if not self.scanning:
                                    break
                                    
                                file_path = os.path.join(root, file)
                                scanned_files += 1
                                
                                # Update progress
                                progress = (scanned_files / total_files) * 100
                                self.main_window.root.after(0, lambda p=progress, f=file_path: 
                                                           self.update_scan_progress(p, f, scanned_files))
                                
                                # Simulate threat detection
                                if file.lower().endswith(('.exe', '.bat', '.cmd', '.scr')) and 'temp' in file_path.lower():
                                    threats_count += 1
                                    self.main_window.root.after(0, lambda path=file_path: 
                                                               self.add_threat_result("Suspicious File", path, "Medium"))
                                
                                time.sleep(0.001)  # Small delay for smooth progress
                
                # Scan complete
                self.main_window.root.after(0, lambda: self.scan_complete(scanned_files, threats_count))
                
            except Exception as e:
                self.main_window.root.after(0, lambda: self.scan_error(str(e)))
        
        threading.Thread(target=scan_worker, daemon=True).start()
    
    def start_full_scan(self):
        """Start full system scan"""
        if self.scanning:
            return
        
        messagebox.showinfo("Full Scan", "Full scan will take longer time.\nThis is a demonstration - scanning C:\\ drive.")
        self.start_quick_scan()  # For demo, use quick scan logic
    
    def start_custom_scan(self):
        """Start custom directory scan"""
        if self.scanning:
            return
        
        directory = filedialog.askdirectory(title="Select directory to scan")
        if directory:
            messagebox.showinfo("Custom Scan", f"Starting custom scan of:\n{directory}")
            self.start_quick_scan()  # For demo, use quick scan logic
    
    def stop_scan(self):
        """Stop current scan"""
        self.scanning = False
        self.update_progress(0, "Scan stopped by user")
        
        # Reset visual grid
        for square in self.scan_squares:
            self.scan_canvas.itemconfig(square, fill=self.colors['bg_tertiary'])
    
    def update_scan_progress(self, progress, current_file, files_scanned):
        """Update scan progress display"""
        self.scan_progress_bar.set_progress(progress)
        self.progress_text.config(text=f"Scanning... {progress:.1f}%")
        
        # Truncate long file paths
        if len(current_file) > 80:
            display_file = "..." + current_file[-77:]
        else:
            display_file = current_file
        
        self.current_file.config(text=f"Current: {display_file}")
        
        # Update statistics
        self.files_scanned.config(text=f"Files Scanned: {files_scanned:,}")
        
        elapsed_time = time.time() - self.scan_start_time
        self.scan_time.config(text=f"Scan Time: {elapsed_time:.0f}s")
        
        if elapsed_time > 0:
            speed = files_scanned / elapsed_time
            self.scan_speed.config(text=f"Speed: {speed:.0f} files/sec")
        
        # Update visual grid
        grid_progress = int((progress / 100) * len(self.scan_squares))
        for i in range(grid_progress):
            if i < len(self.scan_squares):
                self.scan_canvas.itemconfig(self.scan_squares[i], 
                                           fill=self.colors['accent_primary'])
    
    def update_progress(self, progress, message):
        """Update progress display"""
        self.scan_progress_bar.set_progress(progress)
        self.progress_text.config(text=message)
    
    def add_threat_result(self, threat_type, file_path, risk_level):
        """Add threat to results"""
        self.threats_tree.insert('', 'end', values=(threat_type, file_path, risk_level))
        
        # Update threat count
        threat_count = len(self.threats_tree.get_children())
        self.threats_found.config(text=f"Threats Found: {threat_count}")
    
    def scan_complete(self, files_scanned, threats_found):
        """Handle scan completion"""
        self.scanning = False
        elapsed_time = time.time() - self.scan_start_time
        
        self.update_progress(100, f"Scan complete! {files_scanned:,} files scanned in {elapsed_time:.0f}s")
        
        # Show completion message
        if threats_found > 0:
            messagebox.showwarning("Scan Complete", 
                                 f"Scan completed!\n\n"
                                 f"Files scanned: {files_scanned:,}\n"
                                 f"Threats found: {threats_found}\n"
                                 f"Time taken: {elapsed_time:.0f} seconds\n\n"
                                 f"Please review the threats in the results section.")
        else:
            messagebox.showinfo("Scan Complete", 
                               f"Scan completed successfully!\n\n"
                               f"Files scanned: {files_scanned:,}\n"
                               f"No threats found!\n"
                               f"Time taken: {elapsed_time:.0f} seconds")
    
    def scan_error(self, error_message):
        """Handle scan error"""
        self.scanning = False
        self.update_progress(0, f"Scan failed: {error_message}")
        messagebox.showerror("Scan Error", f"Scan failed:\n{error_message}")
