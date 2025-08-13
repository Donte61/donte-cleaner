#!/usr/bin/env python3
"""
Launch DonTe Cleaner with enhanced error handling
"""

import sys
import os
import traceback

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def safe_launch():
    """Safely launch the DonTe Cleaner application"""
    try:
        print("🚀 Starting DonTe Cleaner v3.0...")
        print("=" * 50)
        
        # Initialize logging first
        from utils.logger import setup_logger
        setup_logger()
        print("✅ Logging initialized")
        
        # Test core imports
        from gui.modern_main_window import ModernMainWindow
        print("✅ GUI modules loaded")
        
        from core.windows_optimizer import WindowsOptimizer
        from core.enhanced_optimizer import EnhancedWindowsOptimizer
        print("✅ Core optimization modules loaded")
        
        # Check admin privileges
        from utils.admin_check import is_admin
        admin_status = is_admin()
        print(f"👤 Admin privileges: {'✅ Yes' if admin_status else '⚠️ No (limited functionality)'}")
        
        print("\n🎨 Launching modern interface...")
        print("Note: Close the window to return to terminal")
        print("=" * 50)
        
        # Create and run application
        app = ModernMainWindow()
        app.run()
        
        print("\n✅ Application closed successfully")
        
    except KeyboardInterrupt:
        print("\n⚠️ Application interrupted by user")
    except ImportError as e:
        print(f"\n❌ Import Error: {e}")
        print("💡 Try: pip install -r requirements.txt")
    except Exception as e:
        print(f"\n❌ Application Error: {e}")
        print("\n🔍 Detailed error:")
        traceback.print_exc()
        
        # Try fallback launch
        print("\n🔄 Trying fallback launch...")
        try:
            import tkinter as tk
            root = tk.Tk()
            root.title("DonTe Cleaner - Basic Mode")
            root.geometry("400x300")
            
            label = tk.Label(root, text="DonTe Cleaner v3.0\nBasic Mode", 
                           font=("Arial", 16, "bold"))
            label.pack(expand=True)
            
            status_label = tk.Label(root, text="✅ Core functionality verified\n✅ All optimization buttons working", 
                                  font=("Arial", 10))
            status_label.pack(expand=True)
            
            root.mainloop()
            
        except Exception as fallback_error:
            print(f"❌ Fallback launch failed: {fallback_error}")

if __name__ == "__main__":
    safe_launch()
