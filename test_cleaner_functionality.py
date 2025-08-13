#!/usr/bin/env python3
"""
Test DonTe Cleaner Functionality
Test all core functions to ensure they work properly
"""

import sys
import os
import time

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_core_modules():
    """Test core optimization modules"""
    print("🔧 Testing Core Modules...")
    print("=" * 50)
    
    # Test Windows Optimizer
    try:
        from core.windows_optimizer import WindowsOptimizer
        optimizer = WindowsOptimizer()
        print("✅ WindowsOptimizer: OK")
        
        # Test temp file cleanup
        success, message = optimizer.clean_temp_files()
        print(f"🧹 Temp Cleanup: {'✅' if success else '❌'} {message}")
        
        # Test memory optimization
        success, message = optimizer.optimize_memory()
        print(f"💾 Memory Optimization: {'✅' if success else '❌'} {message}")
        
    except Exception as e:
        print(f"❌ WindowsOptimizer error: {e}")
    
    print()
    
    # Test Enhanced Optimizer
    try:
        from core.enhanced_optimizer import EnhancedWindowsOptimizer
        enhanced = EnhancedWindowsOptimizer()
        print("✅ EnhancedWindowsOptimizer: OK")
        
        # Test user temp cleanup
        success, message = enhanced.clear_user_temp_files()
        print(f"🗑️ User Temp Cleanup: {'✅' if success else '❌'} {message}")
        
        # Test DNS cache clear
        success, message = enhanced.clear_dns_cache()
        print(f"🌐 DNS Cache Clear: {'✅' if success else '❌'} {message}")
        
        # Test memory optimization
        success, message = enhanced.optimize_system_memory()
        print(f"⚡ Enhanced Memory: {'✅' if success else '❌'} {message}")
        
    except Exception as e:
        print(f"❌ EnhancedWindowsOptimizer error: {e}")
    
    print()

def test_antivirus_scanner():
    """Test antivirus scanner"""
    print("🛡️ Testing Antivirus Scanner...")
    print("=" * 50)
    
    try:
        from core.antivirus_scanner import AntivirusScanner
        scanner = AntivirusScanner()
        print("✅ AntivirusScanner: OK")
        
        # Test quick scan
        threats = scanner.quick_scan()
        print(f"🔍 Quick Scan: ✅ Found {len(threats)} threats")
        
    except Exception as e:
        print(f"❌ AntivirusScanner error: {e}")
    
    print()

def test_system_info():
    """Test system information gathering"""
    print("📊 Testing System Information...")
    print("=" * 50)
    
    try:
        import psutil
        
        # CPU info
        cpu_percent = psutil.cpu_percent(interval=1)
        print(f"🖥️ CPU Usage: {cpu_percent:.1f}%")
        
        # Memory info
        memory = psutil.virtual_memory()
        print(f"💾 Memory Usage: {memory.percent:.1f}% ({memory.used // (1024**3)} GB / {memory.total // (1024**3)} GB)")
        
        # Disk info
        disk = psutil.disk_usage('C:\\')
        disk_percent = (disk.used / disk.total) * 100
        print(f"💿 Disk Usage: {disk_percent:.1f}% ({disk.free // (1024**3)} GB free)")
        
        # Process count
        process_count = len(psutil.pids())
        print(f"⚙️ Running Processes: {process_count}")
        
        print("✅ System information gathering: OK")
        
    except Exception as e:
        print(f"❌ System information error: {e}")
    
    print()

def test_gui_components():
    """Test GUI components without opening window"""
    print("🎨 Testing GUI Components...")
    print("=" * 50)
    
    try:
        # Test imports
        from gui.modern_ui import AnimatedButton, NeonProgressBar, HolographicCard
        print("✅ Modern UI components: OK")
        
        from gui.modern_main_window import ModernMainWindow
        print("✅ Main window class: OK")
        
        from gui.pages.dashboard_page import DashboardPage
        print("✅ Dashboard page: OK")
        
        from gui.pages.optimizer_page import OptimizerPage
        print("✅ Optimizer page: OK")
        
    except Exception as e:
        print(f"❌ GUI components error: {e}")
    
    print()

def test_one_click_fix():
    """Test one-click fix functionality"""
    print("🚀 Testing One-Click Fix...")
    print("=" * 50)
    
    try:
        # Initialize optimizers
        from core.windows_optimizer import WindowsOptimizer
        from core.enhanced_optimizer import EnhancedWindowsOptimizer
        
        optimizer = WindowsOptimizer()
        enhanced = EnhancedWindowsOptimizer()
        
        print("🔄 Running one-click optimization...")
        
        # Step 1: Clean temp files
        print("1️⃣ Cleaning temporary files...")
        success, msg = enhanced.clear_user_temp_files()
        print(f"   {'✅' if success else '❌'} {msg}")
        
        # Step 2: Optimize memory
        print("2️⃣ Optimizing memory...")
        success, msg = enhanced.optimize_system_memory()
        print(f"   {'✅' if success else '❌'} {msg}")
        
        # Step 3: Clear DNS cache
        print("3️⃣ Clearing DNS cache...")
        success, msg = enhanced.clear_dns_cache()
        print(f"   {'✅' if success else '❌'} {msg}")
        
        # Step 4: Network optimization
        print("4️⃣ Optimizing network...")
        success, msg = enhanced.optimize_network_settings()
        print(f"   {'✅' if success else '❌'} {msg}")
        
        print("✅ One-click fix completed!")
        
    except Exception as e:
        print(f"❌ One-click fix error: {e}")
    
    print()

def test_quick_clean():
    """Test quick clean functionality"""
    print("🧹 Testing Quick Clean...")
    print("=" * 50)
    
    try:
        from core.enhanced_optimizer import EnhancedWindowsOptimizer
        enhanced = EnhancedWindowsOptimizer()
        
        print("🔄 Running quick clean...")
        
        # Clean user temp files
        success, msg = enhanced.clear_user_temp_files()
        print(f"🗑️ Temp files: {'✅' if success else '❌'} {msg}")
        
        # Clear network cache
        success, msg = enhanced.optimize_network_settings()
        print(f"🌐 Network cache: {'✅' if success else '❌'} {msg}")
        
        print("✅ Quick clean completed!")
        
    except Exception as e:
        print(f"❌ Quick clean error: {e}")
    
    print()

def main():
    """Main test function"""
    print("🔧 DonTe Cleaner v3.0 - Functionality Test")
    print("=" * 60)
    print()
    
    # Test all components
    test_system_info()
    test_core_modules()
    test_antivirus_scanner()
    test_gui_components()
    test_one_click_fix()
    test_quick_clean()
    
    print("🏁 Test completed!")
    print("=" * 60)
    
    # Show final system status
    try:
        import psutil
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        print(f"📊 Final System Status:")
        print(f"   CPU: {cpu:.1f}%")
        print(f"   Memory: {memory.percent:.1f}%")
        print(f"   Available RAM: {memory.available // (1024**3)} GB")
    except:
        pass

if __name__ == "__main__":
    main()
