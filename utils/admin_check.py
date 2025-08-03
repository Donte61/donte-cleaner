"""
Admin privileges utility for DonTe Cleaner
"""

import ctypes
import sys
import os
from tkinter import messagebox

def is_admin():
    """Check if running with administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def ensure_admin_privileges():
    """Ensure the application is running with admin privileges"""
    # Check if limited mode is requested
    if os.environ.get('DONTE_LIMITED_MODE') == '1':
        print("Running in limited mode (admin check skipped)")
        return True
    
    if not is_admin():
        try:
            # Try to restart as admin
            result = messagebox.askyesno(
                "DonTe Cleaner - Yönetici İzni",
                "Bu program tam işlevsellik için yönetici izinleri gerektirir.\n\n"
                "Yönetici olarak yeniden başlatmak istiyor musunuz?\n\n"
                "Not: Mevcut pencere kapanacak ve yeni pencere açılacak.\n\n"
                "İptal ederseniz program sınırlı modda çalışacaktır."
            )
            
            if result:
                try:
                    # Get the current script path
                    script_path = os.path.abspath(sys.argv[0])
                    
                    # Restart as admin
                    ctypes.windll.shell32.ShellExecuteW(
                        None, 
                        "runas", 
                        sys.executable, 
                        f'"{script_path}"', 
                        os.path.dirname(script_path), 
                        1
                    )
                    # Exit current instance
                    sys.exit(0)
                except Exception as restart_error:
                    messagebox.showerror(
                        "Yeniden Başlatma Hatası",
                        f"Yönetici olarak yeniden başlatılamadı: {str(restart_error)}\n\n"
                        "Program sınırlı modda devam edecek."
                    )
                    return True  # Continue in limited mode
            else:
                # User chose not to restart as admin
                messagebox.showinfo(
                    "Sınırlı Mod",
                    "Program sınırlı modda çalışacak.\n\n"
                    "Bazı özellikler (hizmet yönetimi, kayıt defteri değişiklikleri) "
                    "kullanılamayacak."
                )
                return True  # Continue in limited mode
        except KeyboardInterrupt:
            # User pressed Ctrl+C or closed dialog abruptly
            print("Admin privileges dialog was cancelled by user")
            messagebox.showinfo(
                "Sınırlı Mod",
                "Program sınırlı modda çalışacak.\n\n"
                "Bazı özellikler (hizmet yönetimi, kayıt defteri değişiklikleri) "
                "kullanılamayacak."
            )
            return True  # Continue in limited mode
        except Exception as e:
            messagebox.showerror(
                "Hata",
                f"Yönetici izni kontrolü başarısız: {str(e)}\n\n"
                "Program sınırlı modda çalışacak."
            )
            return True  # Continue in limited mode
    return True
