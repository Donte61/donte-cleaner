"""
Build script for DonTe Cleaner
Creates standalone executable using PyInstaller
"""

import os
import subprocess
import sys
import shutil

def main():
    """Main build function"""
    print("🚀 DonTe Cleaner Build Script")
    print("=" * 40)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✅ PyInstaller found")
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Build command
    build_cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=DonTe_Cleaner",
        "--icon=resources/icon.ico",
        "--add-data=resources;resources",
        "--hidden-import=tkinter",
        "--hidden-import=wmi",
        "--hidden-import=psutil",
        "main.py"
    ]
    
    print("🔨 Building executable...")
    try:
        subprocess.run(build_cmd, check=True)
        print("✅ Build completed successfully!")
        
        # Create release folder
        release_dir = "release"
        if os.path.exists(release_dir):
            shutil.rmtree(release_dir)
        os.makedirs(release_dir)
        
        # Copy executable
        shutil.copy("dist/DonTe_Cleaner.exe", release_dir)
        
        # Copy additional files
        additional_files = [
            "README.md",
            "requirements.txt"
        ]
        
        for file in additional_files:
            if os.path.exists(file):
                shutil.copy(file, release_dir)
        
        print(f"📦 Release package created in '{release_dir}' folder")
        print("🎉 Build process completed!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
