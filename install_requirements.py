"""
Install required packages for DonTe Cleaner
Run this script to install missing dependencies
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def main():
    """Install all required packages"""
    print("🚀 Installing DonTe Cleaner dependencies...")
    
    # Required packages
    packages = [
        "psutil",
        "pillow",
        "pygame", 
        "numpy",
        "wmi",
        "pywin32",
        "requests"
    ]
    
    installed_count = 0
    
    for package in packages:
        print(f"\n📦 Installing {package}...")
        if install_package(package):
            installed_count += 1
    
    print(f"\n🎉 Installation complete!")
    print(f"✅ Successfully installed: {installed_count}/{len(packages)} packages")
    
    if installed_count == len(packages):
        print("\n🚀 All dependencies installed! You can now run DonTe Cleaner.")
    else:
        print("\n⚠️ Some packages failed to install. You may experience limited functionality.")
    
    input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
