"""
DonTe Cleaner - Professional Windows Optimization Tool
Main Application Entry Point without Console Window
"""

import tkinter as tk
import sys
import os

# Hide console window on Windows
if sys.platform == "win32":
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import ModernMainWindow
from gui.splash_screen import show_splash_screen
from utils.admin_check import ensure_admin_privileges
from utils.logger import setup_logger

def main():
    """Main application entry point with splash screen"""
    try:
        # Setup logging
        setup_logger()
        
        # Create root window (hidden initially)
        root = tk.Tk()
        root.withdraw()  # Hide main window initially
        
        # Show splash screen
        splash = show_splash_screen(root, duration=3000)
        
        # Ensure admin privileges
        if not ensure_admin_privileges():
            return
        
        # Wait for splash screen to finish
        root.after(3200, lambda: create_main_application(root))
        
        # Start the application
        root.mainloop()
        
    except Exception as e:
        # Show error message if GUI creation fails
        try:
            import tkinter.messagebox as mb
            mb.showerror("DonTe Cleaner - Kritik Hata", 
                        f"Program başlatılamadı:\n\n{str(e)}\n\n"
                        f"Lütfen gerekli bağımlılıkların yüklü olduğundan emin olun.")
        except:
            print(f"Kritik hata: {str(e)}")
        sys.exit(1)

def create_main_application(root):
    """Create main application after splash screen"""
    try:
        # Show main window
        root.deiconify()
        
        # Create main application
        app = ModernMainWindow(root)
        
        # Center window on screen
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
        y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
        root.geometry(f"+{x}+{y}")
        
        # Bring to front
        root.lift()
        root.attributes("-topmost", True)
        root.attributes("-topmost", False)
        root.focus_force()
        
    except Exception as e:
        import tkinter.messagebox as mb
        mb.showerror("Başlatma Hatası", f"Ana uygulama başlatılamadı:\n\n{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
