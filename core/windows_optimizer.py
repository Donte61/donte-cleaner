"""
Windows System Optimizer Core Module
"""

import winreg
import subprocess
import psutil
import wmi
import os
import shutil
import ctypes
from utils.logger import get_logger

class WindowsOptimizer:
    def __init__(self):
        self.logger = get_logger("WindowsOptimizer")
        self.disabled_services = []
        self.removed_startup_items = []
        self.original_visual_effects = None
        self.registry_backup_path = None
        
    def disable_services(self):
        """Disable unnecessary Windows services"""
        try:
            c = wmi.WMI()
            services = ["Spooler", "WSearch", "SysMain", "Fax", "TabletInputService"]
            
            for service_name in services:
                try:
                    service_list = c.Win32_Service(Name=service_name)
                    if service_list:
                        for service in service_list:
                            if service.State == "Running":
                                result = service.StopService()
                                if result[0] == 0:
                                    self.logger.info(f"Service stopped: {service_name}")
                            
                            if service.StartMode != "Disabled":
                                result = service.ChangeStartMode("Disabled")
                                if result[0] == 0:
                                    self.disabled_services.append(service_name)
                                    self.logger.info(f"Service disabled: {service_name}")
                except Exception as e:
                    self.logger.error(f"Error handling service {service_name}: {str(e)}")
            
            return True, f"{len(self.disabled_services)} hizmet devre dışı bırakıldı"
        except Exception as e:
            self.logger.error(f"Service disable operation failed: {str(e)}")
            return False, f"Hizmet kapatma başarısız: {str(e)}"
    
    def clean_startup_programs(self):
        """Clean unnecessary startup programs"""
        try:
            startup_locations = [
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
                (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            ]
            
            removed_count = 0
            for hive, key_path in startup_locations:
                try:
                    key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_ALL_ACCESS)
                    
                    # List of potentially unnecessary startup programs
                    unnecessary_programs = [
                        "Adobe", "Spotify", "Steam", "Discord", "Skype",
                        "Teams", "OneDrive", "Dropbox", "GoogleUpdate"
                    ]
                    
                    i = 0
                    while True:
                        try:
                            value_name, value_data, value_type = winreg.EnumValue(key, i)
                            
                            # Check if this is an unnecessary program
                            for prog in unnecessary_programs:
                                if prog.lower() in value_name.lower() or prog.lower() in value_data.lower():
                                    try:
                                        winreg.DeleteValue(key, value_name)
                                        self.removed_startup_items.append((hive, key_path, value_name, value_data))
                                        removed_count += 1
                                        self.logger.info(f"Removed startup item: {value_name}")
                                        break
                                    except:
                                        pass
                            else:
                                i += 1
                        except OSError:
                            break
                    
                    winreg.CloseKey(key)
                except Exception as e:
                    self.logger.error(f"Error accessing registry key {key_path}: {str(e)}")
            
            return True, f"{removed_count} başlangıç programı kaldırıldı"
        except Exception as e:
            self.logger.error(f"Startup cleanup failed: {str(e)}")
            return False, f"Başlangıç temizleme başarısız: {str(e)}"
    
    def disable_visual_effects(self):
        """Disable Windows visual effects for better performance"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, 
                r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects", 
                0, 
                winreg.KEY_ALL_ACCESS
            )
            
            try:
                self.original_visual_effects = winreg.QueryValueEx(key, "VisualFXSetting")[0]
            except:
                self.original_visual_effects = None
            
            # Set to "Adjust for best performance" (value 2)
            winreg.SetValueEx(key, "VisualFXSetting", 0, winreg.REG_DWORD, 2)
            winreg.CloseKey(key)
            
            self.logger.info("Visual effects disabled")
            return True, "Görsel efektler kapatıldı"
        except Exception as e:
            self.logger.error(f"Visual effects disable failed: {str(e)}")
            return False, f"Görsel efekt kapatma başarısız: {str(e)}"
    
    def set_high_performance_power_plan(self):
        """Set Windows power plan to high performance"""
        try:
            # High Performance GUID
            result = subprocess.run(
                "powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c", 
                shell=True, 
                capture_output=True, 
                text=True
            )
            
            if result.returncode == 0:
                self.logger.info("Power plan set to high performance")
                return True, "Güç planı yüksek performansa ayarlandı"
            else:
                return False, "Güç planı değiştirilemedi"
        except Exception as e:
            self.logger.error(f"Power plan change failed: {str(e)}")
            return False, f"Güç planı ayarı başarısız: {str(e)}"
    
    def clean_temp_files(self):
        """Clean temporary files and system cache"""
        try:
            cleaned_size = 0
            temp_paths = [
                os.environ.get('TEMP', ''),
                os.environ.get('TMP', ''),
                r'C:\Windows\Temp',
                os.path.expanduser(r'~\AppData\Local\Temp')
            ]
            
            for temp_path in temp_paths:
                if os.path.exists(temp_path):
                    try:
                        for root, dirs, files in os.walk(temp_path):
                            for file in files:
                                try:
                                    file_path = os.path.join(root, file)
                                    file_size = os.path.getsize(file_path)
                                    os.remove(file_path)
                                    cleaned_size += file_size
                                except:
                                    pass
                    except:
                        pass
            
            # Run disk cleanup
            try:
                subprocess.run("cleanmgr /sagerun:1", shell=True, check=False)
            except:
                pass
            
            cleaned_mb = cleaned_size / (1024 * 1024)
            self.logger.info(f"Temp files cleaned: {cleaned_mb:.2f} MB")
            return True, f"{cleaned_mb:.2f} MB geçici dosya temizlendi"
        except Exception as e:
            self.logger.error(f"Temp file cleanup failed: {str(e)}")
            return False, f"Geçici dosya temizleme başarısız: {str(e)}"
    
    def optimize_memory(self):
        """Optimize system memory usage"""
        try:
            # Clear working set of current process
            ctypes.windll.kernel32.SetProcessWorkingSetSize(-1, -1, -1)
            
            # Get memory info
            memory = psutil.virtual_memory()
            self.logger.info(f"Memory optimization completed. Available: {memory.available / (1024**3):.2f} GB")
            
            return True, f"Bellek optimize edildi. Kullanılabilir: {memory.available / (1024**3):.2f} GB"
        except Exception as e:
            self.logger.error(f"Memory optimization failed: {str(e)}")
            return False, f"Bellek optimizasyonu başarısız: {str(e)}"
    
    def undo_all_changes(self):
        """Undo all optimization changes"""
        try:
            # Restore services
            if self.disabled_services:
                c = wmi.WMI()
                for service_name in self.disabled_services:
                    try:
                        service_list = c.Win32_Service(Name=service_name)
                        if service_list:
                            for service in service_list:
                                service.ChangeStartMode("Automatic")
                                service.StartService()
                                self.logger.info(f"Service restored: {service_name}")
                    except:
                        pass
                self.disabled_services = []
            
            # Restore startup items
            for hive, key_path, value_name, value_data in self.removed_startup_items:
                try:
                    key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_SET_VALUE)
                    winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, value_data)
                    winreg.CloseKey(key)
                    self.logger.info(f"Startup item restored: {value_name}")
                except:
                    pass
            self.removed_startup_items = []
            
            # Restore visual effects
            if self.original_visual_effects is not None:
                try:
                    key = winreg.OpenKey(
                        winreg.HKEY_CURRENT_USER, 
                        r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects", 
                        0, 
                        winreg.KEY_SET_VALUE
                    )
                    winreg.SetValueEx(key, "VisualFXSetting", 0, winreg.REG_DWORD, self.original_visual_effects)
                    winreg.CloseKey(key)
                    self.logger.info("Visual effects restored")
                except:
                    pass
                self.original_visual_effects = None
            
            # Restore balanced power plan
            try:
                subprocess.run("powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e", shell=True, check=True)
                self.logger.info("Power plan restored to balanced")
            except:
                pass
            
            return True, "Tüm değişiklikler geri alındı"
        except Exception as e:
            self.logger.error(f"Undo operation failed: {str(e)}")
            return False, f"Geri alma işlemi başarısız: {str(e)}"
