"""
DonTe Cleaner - Simple Test Version
Minimal styling for compatibility testing
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.admin_check import is_admin, ensure_admin_privileges
from utils.logger import setup_logger

class SimpleMainWindow:
    def __init__(self, root):
        self.root = root
        self.is_admin = is_admin()
        
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        """Setup main window properties"""
        admin_status = "Yönetici" if self.is_admin else "Sınırlı Mod"
        self.root.title(f"DonTe Cleaner - Simple Test ({admin_status})")
        self.root.geometry("600x400")
        self.root.configure(bg="#2d2d2d")
        
    def create_widgets(self):
        """Create simple UI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="DonTe Cleaner - Test Sürümü", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Status
        status_text = "Yönetici Modu" if self.is_admin else "Sınırlı Mod"
        status_color = "green" if self.is_admin else "orange"
        
        status_label = ttk.Label(main_frame, text=f"Durum: {status_text}", 
                                font=("Arial", 12))
        status_label.pack(pady=(0, 20))
        
        # Simple progress bar test
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(progress_frame, text="İlerleme Test:").pack()
        
        # Simple progressbar without custom styling
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_bar.pack(fill="x", pady=5)
        
        # Test button
        test_button = ttk.Button(main_frame, text="İlerleme Testini Başlat", 
                                command=self.test_progress)
        test_button.pack(pady=10)
        
        # Info text
        info_text = tk.Text(main_frame, height=10, width=60, wrap="word")
        info_text.pack(fill="both", expand=True, pady=(0, 10))
        
        info_content = f"""DonTe Cleaner Test Sürümü

Durum: {status_text}
Admin İzni: {'Evet' if self.is_admin else 'Hayır'}

Bu basit test sürümü, ana programın çalışıp çalışmadığını kontrol etmek için oluşturulmuştur.

Eğer bu pencere sorunsuz açılıyorsa, ana program da çalışması gerekir.

Test özellikler:
- Temel pencere oluşturma ✓
- TTK widget'ları ✓
- İlerleme çubuğu ✓
- Yönetici izni kontrolü ✓

Ana programı çalıştırmak için: python main.py
"""
        
        info_text.insert("1.0", info_content)
        info_text.config(state="disabled")
        
        # Close button
        close_button = ttk.Button(main_frame, text="Kapat", command=self.root.quit)
        close_button.pack()
    
    def test_progress(self):
        """Test progress bar"""
        import threading
        
        def progress_worker():
            for i in range(101):
                self.root.after(0, lambda v=i: self.progress_bar.config(value=v))
                import time
                time.sleep(0.05)
            
            self.root.after(0, lambda: messagebox.showinfo("Test", "İlerleme testi tamamlandı!"))
            self.root.after(0, lambda: self.progress_bar.config(value=0))
        
        threading.Thread(target=progress_worker, daemon=True).start()

def main():
    """Main function for simple test"""
    try:
        # Setup logging
        setup_logger()
        
        # Check admin privileges but don't force restart
        if not is_admin():
            print("Uyarı: Yönetici izni yok, test sınırlı modda çalışacak")
        
        # Create and run the simple test application
        root = tk.Tk()
        app = SimpleMainWindow(root)
        root.mainloop()
        
    except Exception as e:
        # Show error message if GUI creation fails
        try:
            import tkinter.messagebox as mb
            mb.showerror("Test Hatası", 
                        f"Basit test bile başlatılamadı:\n\n{str(e)}\n\n"
                        f"Bu durumda sistem TTK desteği eksik olabilir.")
        except:
            print(f"Kritik hata: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
