"""
Detailed Antivirus Window for DonTe Cleaner
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import json
import os
from datetime import datetime

class AntivirusWindow:
    def __init__(self, parent, antivirus_scanner):
        self.parent = parent
        self.antivirus_scanner = antivirus_scanner
        self.scan_results = []
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title("DonTe Cleaner - Detaylı Virüs Tarama")
        self.window.geometry("900x600")
        self.window.configure(bg="#1a1a1a")
        
        # Setup styles
        self.setup_styles()
        self.create_widgets()
        self.setup_layout()
        
        # Make window modal
        self.window.transient(parent)
        self.window.grab_set()
        
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
        ttk.Label(header_frame, text="Virüs ve Zararlı Yazılım Taraması", 
                 font=("Segoe UI", 16, "bold")).pack(anchor="w")
        ttk.Label(header_frame, text="Gelişmiş tarama seçenekleri ve detaylı sonuçlar", 
                 font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 20))
        
        # Scan options frame
        options_frame = ttk.LabelFrame(self.main_frame, text="Tarama Seçenekleri", padding="15")
        
        # Scan type selection
        scan_type_frame = ttk.Frame(options_frame)
        ttk.Label(scan_type_frame, text="Tarama Türü:").pack(side="left", padx=(0, 10))
        
        self.scan_type_var = tk.StringVar(value="quick")
        ttk.Radiobutton(scan_type_frame, text="Hızlı Tarama", variable=self.scan_type_var, 
                       value="quick").pack(side="left", padx=(0, 10))
        ttk.Radiobutton(scan_type_frame, text="Tam Tarama", variable=self.scan_type_var, 
                       value="full").pack(side="left", padx=(0, 10))
        ttk.Radiobutton(scan_type_frame, text="Özel Tarama", variable=self.scan_type_var, 
                       value="custom").pack(side="left")
        
        # Custom scan path
        path_frame = ttk.Frame(options_frame)
        ttk.Label(path_frame, text="Özel Yol:").pack(side="left", padx=(0, 10))
        self.custom_path_var = tk.StringVar()
        self.path_entry = ttk.Entry(path_frame, textvariable=self.custom_path_var, width=40)
        self.path_entry.pack(side="left", padx=(0, 10), fill="x", expand=True)
        ttk.Button(path_frame, text="Gözat", command=self.browse_path).pack(side="right")
        
        # Action buttons
        button_frame = ttk.Frame(self.main_frame)
        ttk.Button(button_frame, text="Taramayı Başlat", 
                  command=self.start_scan).pack(side="left", padx=(0, 10))
        ttk.Button(button_frame, text="Taramayı Durdur", 
                  command=self.stop_scan).pack(side="left", padx=(0, 10))
        ttk.Button(button_frame, text="Sonuçları Temizle", 
                  command=self.clear_results).pack(side="left")
        
        # Progress frame
        progress_frame = ttk.Frame(self.main_frame)
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_label = ttk.Label(progress_frame, text="Hazır")
        
        # Results frame
        results_frame = ttk.LabelFrame(self.main_frame, text="Tarama Sonuçları", padding="10")
        
        # Results treeview
        columns = ("Dosya", "Tehdit Türü", "Açıklama", "Önem Derecesi")
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=200)
        
        # Scrollbars for treeview
        v_scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_tree.yview)
        h_scrollbar = ttk.Scrollbar(results_frame, orient="horizontal", command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Results action buttons
        results_button_frame = ttk.Frame(results_frame)
        ttk.Button(results_button_frame, text="Karantinaya Al", 
                  command=self.quarantine_selected).pack(side="left", padx=(0, 10))
        ttk.Button(results_button_frame, text="Sil", 
                  command=self.delete_selected).pack(side="left", padx=(0, 10))
        ttk.Button(results_button_frame, text="Rapor Kaydet", 
                  command=self.save_report).pack(side="left", padx=(0, 10))
        ttk.Button(results_button_frame, text="Karantina Yöneticisi", 
                  command=self.open_quarantine_manager).pack(side="left")
        
        # Bottom frame
        bottom_frame = ttk.Frame(self.main_frame)
        ttk.Button(bottom_frame, text="Kapat", command=self.window.destroy).pack(side="right")
        
        # Store widgets
        self.header_frame = header_frame
        self.options_frame = options_frame
        self.scan_type_frame = scan_type_frame
        self.path_frame = path_frame
        self.button_frame = button_frame
        self.progress_frame = progress_frame
        self.results_frame = results_frame
        self.results_button_frame = results_button_frame
        self.bottom_frame = bottom_frame
        self.v_scrollbar = v_scrollbar
        self.h_scrollbar = h_scrollbar
        
        self.scan_thread = None
        self.scan_running = False
    
    def setup_layout(self):
        """Setup widget layout"""
        self.main_frame.pack(fill="both", expand=True)
        self.header_frame.pack(fill="x", pady=(0, 20))
        self.options_frame.pack(fill="x", pady=(0, 10))
        self.scan_type_frame.pack(fill="x", pady=(0, 10))
        self.path_frame.pack(fill="x", pady=(0, 10))
        self.button_frame.pack(fill="x", pady=(0, 10))
        self.progress_frame.pack(fill="x", pady=(0, 10))
        self.progress_bar.pack(fill="x", pady=(0, 5))
        self.progress_label.pack()
        self.results_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Treeview layout
        self.results_tree.grid(row=0, column=0, sticky="nsew")
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        self.results_frame.grid_rowconfigure(0, weight=1)
        self.results_frame.grid_columnconfigure(0, weight=1)
        
        self.results_button_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        self.bottom_frame.pack(fill="x")
    
    def browse_path(self):
        """Browse for custom scan path"""
        path = filedialog.askdirectory(title="Taranacak Klasörü Seçin")
        if path:
            self.custom_path_var.set(path)
    
    def start_scan(self):
        """Start virus scan"""
        if self.scan_running:
            messagebox.showwarning("Uyarı", "Bir tarama zaten çalışıyor!")
            return
        
        scan_type = self.scan_type_var.get()
        
        if scan_type == "custom" and not self.custom_path_var.get():
            messagebox.showerror("Hata", "Özel tarama için bir yol seçin!")
            return
        
        self.scan_running = True
        self.progress_bar.config(mode='indeterminate')
        self.progress_bar.start()
        
        def scan_worker():
            try:
                def progress_callback(progress, status):
                    self.window.after(0, lambda: self.update_progress(progress, status))
                
                if scan_type == "quick":
                    results = self.antivirus_scanner.quick_scan(progress_callback)
                elif scan_type == "full":
                    results = self.antivirus_scanner.full_scan(progress_callback)
                else:  # custom
                    results = self.antivirus_scanner.scan_directory(
                        self.custom_path_var.get(), progress_callback)
                
                self.window.after(0, lambda: self.scan_completed(results))
                
            except Exception as e:
                self.window.after(0, lambda: self.scan_error(str(e)))
        
        self.scan_thread = threading.Thread(target=scan_worker, daemon=True)
        self.scan_thread.start()
    
    def stop_scan(self):
        """Stop current scan"""
        if self.scan_running:
            self.scan_running = False
            self.progress_bar.stop()
            self.progress_bar.config(mode='determinate', value=0)
            self.progress_label.config(text="Tarama durduruldu")
    
    def update_progress(self, progress, status):
        """Update progress bar and label"""
        if self.scan_running:
            self.progress_bar.config(mode='determinate', value=progress)
            self.progress_label.config(text=status)
    
    def scan_completed(self, results):
        """Handle scan completion"""
        self.scan_running = False
        self.progress_bar.stop()
        self.progress_bar.config(value=100)
        self.progress_label.config(text=f"Tarama tamamlandı - {len(results)} tehdit bulundu")
        
        self.scan_results = results
        self.display_results(results)
        
        if results:
            messagebox.showwarning("Tehdit Bulundu", 
                                 f"{len(results)} adet tehdit tespit edildi!")
        else:
            messagebox.showinfo("Temiz", "Hiçbir tehdit bulunamadı.")
    
    def scan_error(self, error_message):
        """Handle scan error"""
        self.scan_running = False
        self.progress_bar.stop()
        self.progress_bar.config(value=0)
        self.progress_label.config(text="Tarama hatası")
        messagebox.showerror("Tarama Hatası", f"Tarama sırasında hata oluştu:\n{error_message}")
    
    def display_results(self, results):
        """Display scan results in treeview"""
        # Clear existing results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Add new results
        for result in results:
            self.results_tree.insert("", "end", values=(
                result['path'],
                result['threat_type'],
                result['description'],
                result['severity']
            ))
    
    def clear_results(self):
        """Clear scan results"""
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        self.scan_results = []
        self.progress_label.config(text="Sonuçlar temizlendi")
    
    def quarantine_selected(self):
        """Quarantine selected files"""
        selected_items = self.results_tree.selection()
        if not selected_items:
            messagebox.showwarning("Uyarı", "Karantinaya alınacak dosyaları seçin!")
            return
        
        quarantined_count = 0
        for item in selected_items:
            values = self.results_tree.item(item)['values']
            file_path = values[0]
            
            success, message = self.antivirus_scanner.quarantine_file(file_path)
            if success:
                quarantined_count += 1
                self.results_tree.delete(item)
        
        messagebox.showinfo("Karantina", f"{quarantined_count} dosya karantinaya alındı.")
    
    def delete_selected(self):
        """Delete selected files"""
        selected_items = self.results_tree.selection()
        if not selected_items:
            messagebox.showwarning("Uyarı", "Silinecek dosyaları seçin!")
            return
        
        result = messagebox.askyesno("Onay", 
                                   "Seçili dosyalar kalıcı olarak silinecek. Emin misiniz?")
        if not result:
            return
        
        deleted_count = 0
        for item in selected_items:
            values = self.results_tree.item(item)['values']
            file_path = values[0]
            
            success, message = self.antivirus_scanner.delete_file(file_path)
            if success:
                deleted_count += 1
                self.results_tree.delete(item)
        
        messagebox.showinfo("Silme", f"{deleted_count} dosya silindi.")
    
    def save_report(self):
        """Save scan report to file"""
        if not self.scan_results:
            messagebox.showwarning("Uyarı", "Kaydedilecek tarama sonucu yok!")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Raporu Kaydet",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt")]
        )
        
        if file_path:
            report = self.antivirus_scanner.get_scan_report()
            
            if file_path.endswith('.json'):
                success = self.antivirus_scanner.save_report(report, file_path)
            else:
                # Save as text
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(f"DonTe Cleaner Tarama Raporu\n")
                        f.write(f"Tarih: {report['scan_date']}\n")
                        f.write(f"Toplam Tehdit: {report['total_threats']}\n\n")
                        
                        for threat in report['threats']:
                            f.write(f"Dosya: {threat['path']}\n")
                            f.write(f"Tehdit: {threat['threat_type']}\n")
                            f.write(f"Açıklama: {threat['description']}\n")
                            f.write(f"Önem: {threat['severity']}\n")
                            f.write("-" * 50 + "\n")
                    success = True
                except:
                    success = False
            
            if success:
                messagebox.showinfo("Başarılı", "Rapor kaydedildi.")
            else:
                messagebox.showerror("Hata", "Rapor kaydedilemedi.")
    
    def open_quarantine_manager(self):
        """Open quarantine manager window"""
        quarantine_window = QuarantineManager(self.window, self.antivirus_scanner)


class QuarantineManager:
    def __init__(self, parent, antivirus_scanner):
        self.parent = parent
        self.antivirus_scanner = antivirus_scanner
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title("Karantina Yöneticisi")
        self.window.geometry("600x400")
        self.window.configure(bg="#1a1a1a")
        
        self.create_widgets()
        self.setup_layout()
        self.load_quarantine_files()
        
        # Make window modal
        self.window.transient(parent)
        self.window.grab_set()
    
    def create_widgets(self):
        """Create quarantine manager widgets"""
        self.main_frame = ttk.Frame(self.window, padding="20")
        
        # Header
        ttk.Label(self.main_frame, text="Karantina Yöneticisi", 
                 font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0, 20))
        
        # File list
        list_frame = ttk.Frame(self.main_frame)
        
        self.file_listbox = tk.Listbox(list_frame, height=15)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Buttons
        button_frame = ttk.Frame(self.main_frame)
        ttk.Button(button_frame, text="Geri Yükle", 
                  command=self.restore_file).pack(side="left", padx=(0, 10))
        ttk.Button(button_frame, text="Kalıcı Sil", 
                  command=self.delete_file).pack(side="left", padx=(0, 10))
        ttk.Button(button_frame, text="Yenile", 
                  command=self.load_quarantine_files).pack(side="left", padx=(0, 10))
        ttk.Button(button_frame, text="Kapat", 
                  command=self.window.destroy).pack(side="right")
        
        self.list_frame = list_frame
        self.button_frame = button_frame
        self.scrollbar = scrollbar
    
    def setup_layout(self):
        """Setup layout"""
        self.main_frame.pack(fill="both", expand=True)
        self.list_frame.pack(fill="both", expand=True, pady=(0, 20))
        self.file_listbox.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.button_frame.pack(fill="x")
    
    def load_quarantine_files(self):
        """Load files from quarantine folder"""
        self.file_listbox.delete(0, tk.END)
        
        quarantine_folder = self.antivirus_scanner.quarantine_folder
        if os.path.exists(quarantine_folder):
            files = os.listdir(quarantine_folder)
            for file in files:
                self.file_listbox.insert(tk.END, file)
    
    def restore_file(self):
        """Restore selected file from quarantine"""
        selection = self.file_listbox.curselection()
        if not selection:
            messagebox.showwarning("Uyarı", "Geri yüklenecek dosyayı seçin!")
            return
        
        file_name = self.file_listbox.get(selection[0])
        quarantine_path = os.path.join(self.antivirus_scanner.quarantine_folder, file_name)
        
        # Ask for restore location
        restore_path = filedialog.askdirectory(title="Geri Yükleme Konumunu Seçin")
        if restore_path:
            original_path = os.path.join(restore_path, file_name)
            success, message = self.antivirus_scanner.restore_from_quarantine(quarantine_path, original_path)
            
            if success:
                messagebox.showinfo("Başarılı", "Dosya geri yüklendi.")
                self.load_quarantine_files()
            else:
                messagebox.showerror("Hata", f"Geri yükleme başarısız: {message}")
    
    def delete_file(self):
        """Permanently delete file from quarantine"""
        selection = self.file_listbox.curselection()
        if not selection:
            messagebox.showwarning("Uyarı", "Silinecek dosyayı seçin!")
            return
        
        result = messagebox.askyesno("Onay", 
                                   "Dosya kalıcı olarak silinecek. Emin misiniz?")
        if not result:
            return
        
        file_name = self.file_listbox.get(selection[0])
        quarantine_path = os.path.join(self.antivirus_scanner.quarantine_folder, file_name)
        
        success, message = self.antivirus_scanner.delete_file(quarantine_path)
        if success:
            messagebox.showinfo("Başarılı", "Dosya silindi.")
            self.load_quarantine_files()
        else:
            messagebox.showerror("Hata", f"Silme başarısız: {message}")
