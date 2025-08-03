"""
DonTe Cleaner Functionality Test
Test all major components to ensure they work properly
"""

import sys
import os
import time
import threading
import traceback

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_core_modules():
    """Test core modules"""
    print("\n🔧 Testing Core Modules:")
    
    try:
        print("   Testing Windows Optimizer...")
        from core.windows_optimizer import WindowsOptimizer
        optimizer = WindowsOptimizer()
        print("   ✅ Windows Optimizer OK")
        
        print("   Testing Enhanced Optimizer...")
        from core.enhanced_optimizer import EnhancedWindowsOptimizer
        enhanced_optimizer = EnhancedWindowsOptimizer()
        report = enhanced_optimizer.get_optimization_report()
        print(f"   ✅ Enhanced Optimizer OK (Admin: {report.get('admin_privileges', False)})")
        
        return True, optimizer, enhanced_optimizer
        
    except Exception as e:
        print(f"   ❌ Core module error: {e}")
        return False, None, None

def test_gui_components():
    """Test GUI components"""
    print("\n🎨 Testing GUI Components:")
    
    try:
        print("   Testing Modern UI components...")
        from gui.modern_ui import AnimatedButton, NeonProgressBar, HolographicCard
        print("   ✅ Modern UI components OK")
        
        print("   Testing Main Window...")
        from gui.modern_main_window import ModernMainWindow
        print("   ✅ Main Window module OK")
        
        print("   Testing Optimizer Page...")
        from gui.pages.optimizer_page import OptimizerPage
        print("   ✅ Optimizer Page OK")
        
        print("   Testing Gaming Page...")
        from gui.pages.gaming_page import GamingPage
        print("   ✅ Gaming Page OK")
        
        return True
        
    except Exception as e:
        print(f"   ❌ GUI component error: {e}")
        print(f"   Details: {traceback.format_exc()}")
        return False

def test_optimization_functions(enhanced_optimizer):
    """Test optimization functions"""
    print("\n⚡ Testing Optimization Functions:")
    
    if not enhanced_optimizer:
        print("   ⚠️ No enhanced optimizer available")
        return False
    
    try:
        print("   Testing memory optimization...")
        success, message = enhanced_optimizer.optimize_system_memory()
        print(f"   {'✅' if success else '⚠️'} Memory optimization: {message}")
        
        print("   Testing DNS cache clear...")
        success, message = enhanced_optimizer.clear_dns_cache()
        print(f"   {'✅' if success else '⚠️'} DNS cache: {message}")
        
        print("   Testing network optimization...")
        success, message = enhanced_optimizer.optimize_network_settings()
        print(f"   {'✅' if success else '⚠️'} Network optimization: {message}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Optimization test error: {e}")
        return False

def test_progress_bars():
    """Test progress bar functionality"""
    print("\n📊 Testing Progress Bars:")
    
    try:
        import tkinter as tk
        from gui.modern_ui import NeonProgressBar
        
        # Create a test window
        root = tk.Tk()
        root.title("Progress Bar Test")
        root.geometry("400x100")
        root.withdraw()  # Hide initially
        
        # Create progress bar
        progress = NeonProgressBar(root, width=350, height=30)
        progress.pack(pady=20)
        
        # Test progress updates
        def test_progress():
            for i in range(0, 101, 10):
                progress.set_progress(i)
                root.update()
                time.sleep(0.1)
            
            print("   ✅ Progress bar animation working")
            root.after(1000, root.destroy)
        
        root.deiconify()  # Show window
        root.after(100, test_progress)
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"   ❌ Progress bar test error: {e}")
        return False

def test_threading():
    """Test threading functionality"""
    print("\n🧵 Testing Threading:")
    
    try:
        results = []
        
        def worker_thread(thread_id):
            time.sleep(0.5)
            results.append(f"Thread {thread_id} completed")
        
        # Create multiple threads
        threads = []
        for i in range(3):
            thread = threading.Thread(target=worker_thread, args=(i,), daemon=True)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads
        for thread in threads:
            thread.join(timeout=2)
        
        if len(results) == 3:
            print("   ✅ Threading working correctly")
            return True
        else:
            print(f"   ⚠️ Threading partial success: {len(results)}/3 threads completed")
            return False
            
    except Exception as e:
        print(f"   ❌ Threading test error: {e}")
        return False

def test_system_monitoring():
    """Test system monitoring"""
    print("\n💻 Testing System Monitoring:")
    
    try:
        import psutil
        
        # Test CPU monitoring
        cpu_percent = psutil.cpu_percent(interval=1)
        print(f"   ✅ CPU monitoring: {cpu_percent}%")
        
        # Test memory monitoring
        memory = psutil.virtual_memory()
        print(f"   ✅ Memory monitoring: {memory.percent}% used")
        
        # Test disk monitoring
        disk = psutil.disk_usage('/')
        disk_percent = (disk.used / disk.total) * 100
        print(f"   ✅ Disk monitoring: {disk_percent:.1f}% used")
        
        # Test process monitoring
        process_count = len(list(psutil.process_iter()))
        print(f"   ✅ Process monitoring: {process_count} processes")
        
        return True
        
    except Exception as e:
        print(f"   ❌ System monitoring error: {e}")
        return False

def test_file_operations():
    """Test file operations"""
    print("\n📁 Testing File Operations:")
    
    try:
        # Test directory creation
        test_dir = "test_optimization_tmp"
        os.makedirs(test_dir, exist_ok=True)
        print("   ✅ Directory creation OK")
        
        # Test file creation
        test_file = os.path.join(test_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("Test optimization content")
        print("   ✅ File creation OK")
        
        # Test file deletion
        os.remove(test_file)
        os.rmdir(test_dir)
        print("   ✅ File cleanup OK")
        
        return True
        
    except Exception as e:
        print(f"   ❌ File operations error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 DonTe Cleaner Functionality Test")
    print("=" * 50)
    
    test_results = []
    
    # Run all tests
    print("Starting comprehensive functionality test...")
    
    # Test core modules
    core_success, optimizer, enhanced_optimizer = test_core_modules()
    test_results.append(("Core Modules", core_success))
    
    # Test GUI components
    gui_success = test_gui_components()
    test_results.append(("GUI Components", gui_success))
    
    # Test system monitoring
    monitoring_success = test_system_monitoring()
    test_results.append(("System Monitoring", monitoring_success))
    
    # Test file operations
    file_success = test_file_operations()
    test_results.append(("File Operations", file_success))
    
    # Test threading
    threading_success = test_threading()
    test_results.append(("Threading", threading_success))
    
    # Test optimization functions
    if enhanced_optimizer:
        opt_success = test_optimization_functions(enhanced_optimizer)
        test_results.append(("Optimization Functions", opt_success))
    
    # Test progress bars (optional, requires GUI)
    try:
        progress_success = test_progress_bars()
        test_results.append(("Progress Bars", progress_success))
    except:
        print("\n📊 Progress bar test skipped (GUI not available)")
    
    # Results summary
    print("\n" + "=" * 50)
    print("🎯 Test Results Summary:")
    print("=" * 30)
    
    passed = 0
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    success_rate = (passed / len(test_results)) * 100
    print(f"\n📊 Overall Success Rate: {passed}/{len(test_results)} ({success_rate:.1f}%)")
    
    if success_rate >= 90:
        print("\n🎉 Excellent! All major components are working properly.")
        print("   DonTe Cleaner should function perfectly.")
    elif success_rate >= 70:
        print("\n✅ Good! Most components are working.")
        print("   DonTe Cleaner should work with minor limitations.")
    elif success_rate >= 50:
        print("\n⚠️ Partial success. Some components have issues.")
        print("   DonTe Cleaner may have limited functionality.")
    else:
        print("\n❌ Multiple critical issues detected.")
        print("   Please run diagnostic_tool.py for detailed analysis.")
    
    print("\n💡 Next Steps:")
    if success_rate >= 80:
        print("   • You can start using DonTe Cleaner normally")
        print("   • Run as Administrator for full optimization features")
        print("   • Use 'start_donte_cleaner.bat' for easy launching")
    else:
        print("   • Run 'python diagnostic_tool.py' for detailed diagnostics")
        print("   • Install missing dependencies with 'python install_requirements.py'")
        print("   • Check the troubleshooting guide in README.md")
    
    print("\n" + "=" * 50)
    input("Press Enter to exit test...")

if __name__ == "__main__":
    main()
