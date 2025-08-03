"""
DonTe Cleaner Troubleshooting and Diagnostic Tool
"""

import sys
import os
import importlib
import subprocess
import traceback

def check_python_version():
    """Check Python version"""
    print("🐍 Python Version Check:")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("   ❌ Warning: Python 3.7+ recommended")
        return False
    else:
        print("   ✅ Python version OK")
        return True

def check_dependencies():
    """Check required dependencies"""
    print("\n📦 Dependency Check:")
    
    dependencies = {
        'tkinter': 'GUI framework',
        'psutil': 'System monitoring',
        'threading': 'Multithreading support',
        'time': 'Time operations',
        'os': 'Operating system interface',
        'subprocess': 'Process management',
        'PIL': 'Image processing (optional)',
        'pygame': 'Audio support (optional)',
        'numpy': 'Numerical operations (optional)',
        'wmi': 'Windows Management (optional)',
        'winreg': 'Windows Registry (Windows only)',
        'ctypes': 'Windows API calls'
    }
    
    missing = []
    optional_missing = []
    
    for module, description in dependencies.items():
        try:
            importlib.import_module(module)
            print(f"   ✅ {module} - {description}")
        except ImportError:
            if module in ['PIL', 'pygame', 'numpy', 'wmi']:
                optional_missing.append(module)
                print(f"   ⚠️ {module} - {description} (OPTIONAL - some features may be limited)")
            else:
                missing.append(module)
                print(f"   ❌ {module} - {description} (REQUIRED)")
    
    if missing:
        print(f"\n❌ Critical dependencies missing: {', '.join(missing)}")
        return False
    elif optional_missing:
        print(f"\n⚠️ Optional dependencies missing: {', '.join(optional_missing)}")
        print("   Application will work but some features may be limited.")
        return True
    else:
        print("\n✅ All dependencies found!")
        return True

def check_admin_privileges():
    """Check if running as administrator"""
    print("\n👑 Administrator Privileges Check:")
    
    try:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        if is_admin:
            print("   ✅ Running as Administrator")
            return True
        else:
            print("   ⚠️ Not running as Administrator")
            print("   Some optimization features may be limited.")
            return False
    except:
        print("   ❓ Unable to determine admin status")
        return False

def check_file_permissions():
    """Check file permissions"""
    print("\n📁 File Permissions Check:")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check read access
    if os.access(script_dir, os.R_OK):
        print("   ✅ Read access OK")
    else:
        print("   ❌ No read access to application directory")
        return False
    
    # Check write access for logs
    logs_dir = os.path.join(script_dir, 'logs')
    try:
        os.makedirs(logs_dir, exist_ok=True)
        test_file = os.path.join(logs_dir, 'test_write.tmp')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        print("   ✅ Write access OK")
        return True
    except:
        print("   ⚠️ Limited write access (logs may not work)")
        return False

def test_core_modules():
    """Test core modules"""
    print("\n🔧 Core Module Test:")
    
    try:
        # Test core imports
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        print("   Testing Windows Optimizer...")
        from core.windows_optimizer import WindowsOptimizer
        optimizer = WindowsOptimizer()
        print("   ✅ Windows Optimizer loaded")
        
        print("   Testing GUI components...")
        from gui.modern_ui import AnimatedButton, NeonProgressBar
        print("   ✅ Modern UI components loaded")
        
        print("   Testing main window...")
        from gui.modern_main_window import ModernMainWindow
        print("   ✅ Main window module loaded")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Core module error: {e}")
        print(f"   Details: {traceback.format_exc()}")
        return False

def check_system_resources():
    """Check system resources"""
    print("\n💻 System Resources Check:")
    
    try:
        import psutil
        
        # CPU
        cpu_count = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent(interval=1)
        print(f"   CPU: {cpu_count} cores, {cpu_percent}% usage")
        
        # Memory
        memory = psutil.virtual_memory()
        memory_gb = memory.total / (1024**3)
        memory_percent = memory.percent
        print(f"   RAM: {memory_gb:.1f} GB total, {memory_percent}% used")
        
        # Disk
        disk = psutil.disk_usage('/')
        disk_gb = disk.total / (1024**3)
        disk_percent = (disk.used / disk.total) * 100
        print(f"   Disk: {disk_gb:.1f} GB total, {disk_percent:.1f}% used")
        
        # Check if resources are sufficient
        if memory_gb < 2:
            print("   ⚠️ Warning: Low RAM (2GB+ recommended)")
        if cpu_percent > 80:
            print("   ⚠️ Warning: High CPU usage")
        if disk_percent > 90:
            print("   ⚠️ Warning: Low disk space")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Resource check failed: {e}")
        return False

def run_basic_test():
    """Run basic functionality test"""
    print("\n🧪 Basic Functionality Test:")
    
    try:
        # Test tkinter
        print("   Testing GUI framework...")
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Hide window
        root.destroy()
        print("   ✅ GUI framework working")
        
        # Test file operations
        print("   Testing file operations...")
        test_dir = "test_tmp"
        os.makedirs(test_dir, exist_ok=True)
        test_file = os.path.join(test_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        os.rmdir(test_dir)
        print("   ✅ File operations working")
        
        # Test threading
        print("   Testing threading...")
        import threading
        import time
        
        def test_thread():
            time.sleep(0.1)
        
        thread = threading.Thread(target=test_thread)
        thread.start()
        thread.join(timeout=1)
        print("   ✅ Threading working")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Basic test failed: {e}")
        return False

def provide_solutions():
    """Provide solutions for common issues"""
    print("\n💡 Common Solutions:")
    print("   1. Install missing packages:")
    print("      python -m pip install psutil pillow pygame numpy wmi pywin32")
    print("   2. Run as Administrator for full functionality")
    print("   3. Update Python to 3.7+ if needed")
    print("   4. Check Windows compatibility (Windows 10+ recommended)")
    print("   5. Ensure antivirus is not blocking the application")
    print("   6. Close other resource-intensive applications")

def main():
    """Main diagnostic function"""
    print("🔍 DonTe Cleaner Diagnostic Tool")
    print("=" * 50)
    
    results = []
    
    # Run all checks
    results.append(("Python Version", check_python_version()))
    results.append(("Dependencies", check_dependencies()))
    results.append(("Admin Privileges", check_admin_privileges()))
    results.append(("File Permissions", check_file_permissions()))
    results.append(("Core Modules", test_core_modules()))
    results.append(("System Resources", check_system_resources()))
    results.append(("Basic Functionality", run_basic_test()))
    
    # Summary
    print("\n📋 Diagnostic Summary:")
    print("=" * 30)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall Score: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! DonTe Cleaner should work properly.")
    elif passed >= len(results) * 0.7:
        print("\n⚠️ Most tests passed. Application should work with minor limitations.")
    else:
        print("\n❌ Multiple issues detected. Please follow the solutions below.")
    
    provide_solutions()
    
    print("\n" + "=" * 50)
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
