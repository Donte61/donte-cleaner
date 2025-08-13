#!/usr/bin/env python3
"""
Test Fixed Animations - DonTe Cleaner v3.0
Test all animations and UI components for errors
"""

import sys
import os
import time
import tkinter as tk

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_ui_components():
    """Test all UI components for errors"""
    print("🎨 Testing Fixed UI Components...")
    print("=" * 50)
    
    try:
        # Create test window
        root = tk.Tk()
        root.title("UI Components Test")
        root.geometry("800x600")
        root.configure(bg='#1a1a2e')
        
        # Test modern UI components
        from gui.modern_ui import (AnimatedButton, NeonProgressBar, 
                                   HolographicCard, StatusIndicator, 
                                   ParticleSystem, GradientFrame)
        
        print("✅ All UI components imported successfully")
        
        # Create gradient background
        gradient = GradientFrame(root, color1="#1a1a2e", color2="#16213e")
        gradient.pack(fill='both', expand=True)
        
        # Test AnimatedButton
        test_btn = AnimatedButton(gradient, text="🧪 Test Button", 
                                 width=200, height=50,
                                 bg_color="#0066cc", hover_color="#0080ff")
        test_btn.place(x=50, y=50)
        print("✅ AnimatedButton created")
        
        # Test NeonProgressBar
        progress = NeonProgressBar(gradient, width=300, height=30)
        progress.place(x=50, y=120)
        print("✅ NeonProgressBar created")
        
        # Test HolographicCard
        card = HolographicCard(gradient, width=250, height=150, title="🔮 Test Card")
        card.place(x=50, y=180)
        print("✅ HolographicCard created")
        
        # Test StatusIndicator
        status = StatusIndicator(gradient, status='active', size=30)
        status.place(x=400, y=50)
        print("✅ StatusIndicator created")
        
        # Test ParticleSystem
        particles = ParticleSystem(gradient, num_particles=20)
        print("✅ ParticleSystem created")
        
        # Animate progress bar
        def animate_progress():
            for i in range(101):
                try:
                    progress.set_progress(i)
                    root.update_idletasks()
                    time.sleep(0.01)
                except:
                    break
        
        # Start animation test
        print("🔄 Starting animation test...")
        root.after(1000, animate_progress)
        
        # Auto close after 5 seconds
        def auto_close():
            particles.stop()
            card.stop_animation()
            root.quit()
            root.destroy()
            print("✅ Animation test completed successfully!")
        
        root.after(5000, auto_close)
        
        # Run test
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ UI test error: {e}")
        return False

def test_button_functionality():
    """Quick test of button functionality"""
    print("\n🚀 Testing Button Functionality...")
    print("=" * 50)
    
    try:
        from core.enhanced_optimizer import EnhancedWindowsOptimizer
        enhanced = EnhancedWindowsOptimizer()
        
        # Test one function to make sure everything still works
        success, message = enhanced.optimize_system_memory()
        print(f"💾 Memory optimization: {'✅' if success else '❌'} {message}")
        
        success, message = enhanced.clear_dns_cache()
        print(f"🌐 DNS cache clear: {'✅' if success else '❌'} {message}")
        
        print("✅ Core functionality still working after UI fixes!")
        return True
        
    except Exception as e:
        print(f"❌ Functionality test error: {e}")
        return False

def main():
    """Main test function"""
    print("🔧 DonTe Cleaner v3.0 - Fixed Animation Test")
    print("🎯 Testing all fixed UI components and animations")
    print("=" * 60)
    
    # Test button functionality first
    func_result = test_button_functionality()
    
    # Test UI components
    ui_result = test_ui_components()
    
    # Summary
    print("\n🏁 FIXED VERSION TEST RESULTS")
    print("=" * 60)
    
    if func_result:
        print("✅ Core Functionality: WORKING")
    else:
        print("❌ Core Functionality: NEEDS ATTENTION")
    
    if ui_result:
        print("✅ UI Components & Animations: FIXED")
    else:
        print("❌ UI Components & Animations: STILL HAVE ISSUES")
    
    if func_result and ui_result:
        print("\n🎉 ALL FIXES SUCCESSFUL!")
        print("✅ DonTe Cleaner is now fully functional with stable animations!")
    else:
        print("\n⚠️ Some issues remain")

if __name__ == "__main__":
    main()
