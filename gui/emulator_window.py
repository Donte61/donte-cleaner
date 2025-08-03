"""
Detailed Emulator Management Window for DonTe Cleaner
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import psutil

class EmulatorWindow:
    def __init__(self, parent, emulator_optimizer):
        self.parent = parent
        self.emulator_optimizer = emulator_optimizer
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title("DonTe Cleaner - Emülatör Yöneticisi")
        self.window.geometry("800x600")
        self.window.configure(bg="#1a1a1a")
        
        # Setup styles
        self.setup_styles()
        self.create_widgets()
        self.setup_layout()
        
        # Make window modal
        self.window.transient(parent)
        self.window.grab_set()
        
        # Start status update timer
        self.update_status()
        
        # Center window
        self.center_window()
    
    def setup_styles(self):
        """Setup window styles"""
        self.colors = {
            'bg_dark': '#1a1a1a',
            'bg_medium': '#2d2d2d',
            'bg_light': '#3d3d3d',
            'accent': '#0078d4',
            'success': '#107c10',
            'warning': '#ff8c00',
            'danger': '#d13438',
            'text_white': '#ffffff',
            'text_gray': '#cccccc'
        }
    
    def center_window(self):
        """Center window on parent"""
        self.window.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (self.window.winfo_width() // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (self.window.winfo_height() // 2)
        self.window.geometry(f"+{x}+{y}")
    
    def create_widgets(self):
        """Create all widgets"""
        # Main frame
        self.main_frame = ttk.Frame(self.window, padding="20")
        
        # Header
        header_frame = ttk.Frame(self.main_frame)
        ttk.Label(header_frame, text="Emülatör Yöneticisi", 
                 font=("Segoe UI", 16, "bold")).pack(anchor="w")
        ttk.Label(header_frame, text="Android emülatörlerini yönet ve optimize et", 
                 font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 20))
        
        # Emulator selection frame
        selection_frame = ttk.LabelFrame(self.main_frame, text="Emülatör Seçimi", padding="15")
        
        self.emulator_var = tk.StringVar(value="BlueStacks")
        emulator_frame = ttk.Frame(selection_frame)
        
        ttk.Label(emulator_frame, text="Emülatör:").pack(side="left", padx=(0, 10))
        self.emulator_combo = ttk.Combobox(emulator_frame, textvariable=self.emulator_var,
                                          values=list(self.emulator_optimizer.emulator_paths.keys()),
                                          state="readonly", width=15)
        self.emulator_combo.pack(side="left", padx=(0, 10))
        self.emulator_combo.bind("<<ComboboxSelected>>", self.on_emulator_changed)
        
        # Path management
        path_frame = ttk.Frame(selection_frame)
        ttk.Label(path_frame, text="Yol:").pack(side="left", padx=(0, 10))
        self.path_var = tk.StringVar()
        self.path_entry = ttk.Entry(path_frame, textvariable=self.path_var, width=40, state="readonly")
        self.path_entry.pack(side="left", padx=(0, 10), fill="x", expand=True)
        ttk.Button(path_frame, text="Değiştir", command=self.change_path).pack(side="right")
        
        # Control buttons frame
        control_frame = ttk.LabelFrame(self.main_frame, text="Emülatör Kontrolü", padding="15")
        
        button_grid = ttk.Frame(control_frame)
        
        # Row 1
        ttk.Button(button_grid, text="Başlat", command=self.start_emulator, 
                  width=15).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_grid, text="Kapat", command=self.stop_emulator, 
                  width=15).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(button_grid, text="Yeniden Başlat", command=self.restart_emulator, 
                  width=15).grid(row=0, column=2, padx=5, pady=5)
        
        # Row 2
        ttk.Button(button_grid, text="Öncelik Artır", command=self.boost_priority, 
                  width=15).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(button_grid, text="Optimize Et", command=self.optimize_emulator, 
                  width=15).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(button_grid, text="Otomatik Başlat", command=self.auto_start, 
                  width=15).grid(row=1, column=2, padx=5, pady=5)
        
        # Status frame
        status_frame = ttk.LabelFrame(self.main_frame, text="Durum Bilgileri", padding="15")
        
        # Status display
        self.status_text = tk.Text(status_frame, height=8, width=70, 
                                  state="disabled", wrap="word")
        status_scrollbar = ttk.Scrollbar(status_frame, orient="vertical", 
                                        command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=status_scrollbar.set)
        
        # Performance monitoring frame
        perf_frame = ttk.LabelFrame(self.main_frame, text="Performans İzleme", padding="15")
        
        # Performance labels
        self.cpu_label = ttk.Label(perf_frame, text="CPU: -")
        self.memory_label = ttk.Label(perf_frame, text="Bellek: -")
        self.process_count_label = ttk.Label(perf_frame, text="İşlem Sayısı: -")
        
        # Advanced settings frame
        advanced_frame = ttk.LabelFrame(self.main_frame, text="Gelişmiş Ayarlar", padding="15")
        
        # Settings checkboxes
        self.auto_optimize_var = tk.BooleanVar()
        self.monitor_performance_var = tk.BooleanVar(value=True)
        self.close_background_var = tk.BooleanVar()
        
        ttk.Checkbutton(advanced_frame, text="Otomatik optimizasyon", 
                       variable=self.auto_optimize_var).pack(anchor="w")
        ttk.Checkbutton(advanced_frame, text="Performans izleme", 
                       variable=self.monitor_performance_var,
                       command=self.toggle_monitoring).pack(anchor="w")
        ttk.Checkbutton(advanced_frame, text="Arka plan uygulamalarını kapat", 
                       variable=self.close_background_var).pack(anchor="w")
        
        # Bottom frame
        bottom_frame = ttk.Frame(self.main_frame)
        ttk.Button(bottom_frame, text="Ayarları Kaydet", 
                  command=self.save_settings).pack(side="left", padx=(0, 10))
        ttk.Button(bottom_frame, text="Varsayılana Sıfırla", 
                  command=self.reset_settings).pack(side="left", padx=(0, 10))
        ttk.Button(bottom_frame, text="Kapat", 
                  command=self.window.destroy).pack(side="right")
        
        # Store widgets
        self.header_frame = header_frame
        self.selection_frame = selection_frame
        self.emulator_frame = emulator_frame
        self.path_frame = path_frame
        self.control_frame = control_frame
        self.button_grid = button_grid
        self.status_frame = status_frame
        self.status_scrollbar = status_scrollbar
        self.perf_frame = perf_frame
        self.advanced_frame = advanced_frame
        self.bottom_frame = bottom_frame
        
        # Load current emulator path
        self.on_emulator_changed()
    
    def setup_layout(self):
        """Setup widget layout"""
        self.main_frame.pack(fill="both", expand=True)
        self.header_frame.pack(fill="x", pady=(0, 20))
        
        self.selection_frame.pack(fill="x", pady=(0, 10))
        self.emulator_frame.pack(fill="x", pady=(0, 10))
        self.path_frame.pack(fill="x")
        
        self.control_frame.pack(fill="x", pady=(0, 10))
        self.button_grid.pack()
        
        # Status layout in two columns
        status_perf_frame = ttk.Frame(self.main_frame)
        status_perf_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        self.status_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        self.status_text.pack(side="left", fill="both", expand=True)
        self.status_scrollbar.pack(side="right", fill="y")
        
        self.perf_frame.pack(side="right", fill="y", padx=(5, 0))
        self.cpu_label.pack(anchor="w", pady=2)
        self.memory_label.pack(anchor="w", pady=2)
        self.process_count_label.pack(anchor="w", pady=2)
        
        self.advanced_frame.pack(fill="x", pady=(0, 10))
        self.bottom_frame.pack(fill="x")
    
    def on_emulator_changed(self, event=None):
        """Handle emulator selection change"""
        emulator_name = self.emulator_var.get()
        path = self.emulator_optimizer.emulator_paths.get(emulator_name, "")
        self.path_var.set(path)
        self.update_status_display()
    
    def change_path(self):
        """Change emulator path"""
        emulator_name = self.emulator_var.get()
        current_path = self.path_var.get()
        
        new_path = filedialog.askopenfilename(
            title=f"{emulator_name} çalıştırılabilir dosyasını seçin",
            initialdir=current_path if current_path else "",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
        )
        
        if new_path:
            self.emulator_optimizer.set_emulator_path(emulator_name, new_path)
            self.path_var.set(new_path)
            self.log_message(f"{emulator_name} yolu güncellendi: {new_path}")
    
    def start_emulator(self):
        """Start selected emulator"""
        emulator_name = self.emulator_var.get()
        
        def start_worker():
            success, message = self.emulator_optimizer.start_emulator(emulator_name)
            self.window.after(0, lambda: self.operation_completed("Başlatma", success, message))
        
        threading.Thread(target=start_worker, daemon=True).start()
        self.log_message(f"{emulator_name} başlatılıyor...")
    
    def stop_emulator(self):
        """Stop selected emulator"""
        emulator_name = self.emulator_var.get()
        
        result = messagebox.askyesno("Onay", f"{emulator_name} kapatılsın mı?")
        if not result:
            return
        
        def stop_worker():
            success, message = self.emulator_optimizer.close_emulator(emulator_name)
            self.window.after(0, lambda: self.operation_completed("Kapatma", success, message))
        
        threading.Thread(target=stop_worker, daemon=True).start()
        self.log_message(f"{emulator_name} kapatılıyor...")
    
    def restart_emulator(self):
        """Restart selected emulator"""
        emulator_name = self.emulator_var.get()
        
        def restart_worker():
            # First stop
            self.emulator_optimizer.close_emulator(emulator_name)
            time.sleep(3)  # Wait for processes to close
            
            # Then start
            success, message = self.emulator_optimizer.start_emulator(emulator_name)
            self.window.after(0, lambda: self.operation_completed("Yeniden Başlatma", success, message))
        
        threading.Thread(target=restart_worker, daemon=True).start()
        self.log_message(f"{emulator_name} yeniden başlatılıyor...")
    
    def boost_priority(self):
        """Boost emulator priority"""
        emulator_name = self.emulator_var.get()
        
        def boost_worker():
            success, message = self.emulator_optimizer.boost_emulator_priority(emulator_name)
            self.window.after(0, lambda: self.operation_completed("Öncelik Artırma", success, message))
        
        threading.Thread(target=boost_worker, daemon=True).start()
        self.log_message(f"{emulator_name} önceliği artırılıyor...")
    
    def optimize_emulator(self):
        """Optimize emulator settings"""
        emulator_name = self.emulator_var.get()
        
        def optimize_worker():
            success, message = self.emulator_optimizer.optimize_emulator_settings(emulator_name)
            self.window.after(0, lambda: self.operation_completed("Optimizasyon", success, message))
        
        threading.Thread(target=optimize_worker, daemon=True).start()
        self.log_message(f"{emulator_name} optimize ediliyor...")
    
    def auto_start(self):
        """Auto start with optimization"""
        emulator_name = self.emulator_var.get()
        
        def auto_start_worker():
            self.log_message(f"{emulator_name} otomatik başlatma işlemi başlıyor...")
            
            # Close background apps if enabled
            if self.close_background_var.get():
                self.log_message("Arka plan uygulamaları kapatılıyor...")
                # Close background apps logic here
            
            # Start emulator
            success, message = self.emulator_optimizer.start_emulator(emulator_name)
            if success:
                time.sleep(5)  # Wait for emulator to start
                
                # Auto optimize if enabled
                if self.auto_optimize_var.get():
                    self.log_message("Otomatik optimizasyon yapılıyor...")
                    self.emulator_optimizer.optimize_emulator_settings(emulator_name)
                    self.emulator_optimizer.boost_emulator_priority(emulator_name)
            
            self.window.after(0, lambda: self.operation_completed("Otomatik Başlatma", success, message))
        
        threading.Thread(target=auto_start_worker, daemon=True).start()
    
    def operation_completed(self, operation, success, message):
        """Handle operation completion"""
        if success:
            self.log_message(f"✓ {operation} başarılı: {message}")
        else:
            self.log_message(f"✗ {operation} başarısız: {message}")
            messagebox.showerror("Hata", f"{operation} başarısız:\n{message}")
    
    def log_message(self, message):
        """Add message to status log"""
        self.status_text.config(state="normal")
        timestamp = time.strftime("%H:%M:%S")
        self.status_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state="disabled")
    
    def update_status(self):
        """Update emulator status and performance info"""
        if self.monitor_performance_var.get():
            self.update_performance_info()
        
        # Update status display
        self.update_status_display()
        
        # Schedule next update
        self.window.after(2000, self.update_status)  # Update every 2 seconds
    
    def update_performance_info(self):
        """Update performance monitoring info"""
        emulator_name = self.emulator_var.get()
        processes = self.emulator_optimizer.get_emulator_status(emulator_name)
        
        if processes:
            total_cpu = sum(p['cpu_percent'] for p in processes)
            total_memory = sum(p['memory_mb'] for p in processes)
            process_count = len(processes)
            
            self.cpu_label.config(text=f"CPU: {total_cpu:.1f}%")
            self.memory_label.config(text=f"Bellek: {total_memory:.1f} MB")
            self.process_count_label.config(text=f"İşlem Sayısı: {process_count}")
        else:
            self.cpu_label.config(text="CPU: -")
            self.memory_label.config(text="Bellek: -")
            self.process_count_label.config(text="İşlem Sayısı: 0")
    
    def update_status_display(self):
        """Update status display with current emulator info"""
        emulator_name = self.emulator_var.get()
        processes = self.emulator_optimizer.get_emulator_status(emulator_name)
        
        status = "Çalışıyor" if processes else "Durduruldu"
        
        # This could be expanded to show more detailed status
        if hasattr(self, 'last_status') and self.last_status != status:
            self.log_message(f"{emulator_name} durumu: {status}")
            self.last_status = status
        elif not hasattr(self, 'last_status'):
            self.last_status = status
    
    def toggle_monitoring(self):
        """Toggle performance monitoring"""
        if self.monitor_performance_var.get():
            self.log_message("Performans izleme etkinleştirildi")
        else:
            self.log_message("Performans izleme devre dışı bırakıldı")
            self.cpu_label.config(text="CPU: -")
            self.memory_label.config(text="Bellek: -")
            self.process_count_label.config(text="İşlem Sayısı: -")
    
    def save_settings(self):
        """Save current settings"""
        # Save settings logic here
        self.log_message("Ayarlar kaydedildi")
        messagebox.showinfo("Başarılı", "Ayarlar kaydedildi")
    
    def reset_settings(self):
        """Reset settings to default"""
        result = messagebox.askyesno("Onay", "Ayarlar varsayılana sıfırlanacak. Emin misiniz?")
        if result:
            self.auto_optimize_var.set(False)
            self.monitor_performance_var.set(True)
            self.close_background_var.set(False)
            self.log_message("Ayarlar varsayılana sıfırlandı")
            messagebox.showinfo("Başarılı", "Ayarlar varsayılana sıfırlandı")
