"""
DonTe Cleaner v3.0 - Next-Generation Windows Optimization Tool
Ultra Modern Technological Interface
"""

import tkinter as tk
import sys
import os

# Hide console window on Windows (if running with python.exe instead of pythonw.exe)
if sys.platform == "win32":
    try:
        import ctypes
        # Hide console window
        console_window = ctypes.windll.kernel32.GetConsoleWindow()
        if console_window != 0:
            ctypes.windll.user32.ShowWindow(console_window, 0)
    except:
        pass  # If ctypes fails, continue without hiding console

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.modern_main_window import ModernMainWindow
from utils.admin_check import ensure_admin_privileges
from utils.logger import setup_logger

def main():
    """Main application entry point with modern interface"""
    try:
        # Setup logging
        setup_logger()
        
        # Ensure admin privileges with error handling
        try:
            if not ensure_admin_privileges():
                return
        except KeyboardInterrupt:
            print("User cancelled admin privileges dialog")
            # Continue without admin privileges
            pass
        except Exception as e:
            print(f"Error checking admin privileges: {e}")
            # Continue without admin privileges
            pass
        
        # Create and run modern application
        app = ModernMainWindow()
        app.run()
        
    except KeyboardInterrupt:
        # User pressed Ctrl+C
        print("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        # Show error message if GUI creation fails
        try:
            import tkinter.messagebox as mb
            mb.showerror("DonTe Cleaner - Critical Error", 
                        f"Application failed to start:\n\n{str(e)}\n\n"
                        f"Please ensure all dependencies are installed.")
        except:
            print(f"Critical error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
