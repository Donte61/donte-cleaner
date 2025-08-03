"""
Enhanced Windows Optimizer - Works with limited privileges
"""

import winreg
import subprocess
import psutil
import os
import shutil
import ctypes
import tempfile
import time
from utils.logger import get_logger

class EnhancedWindowsOptimizer:
    def __init__(self):
        self.logger = get_logger("EnhancedOptimizer")
        self.is_admin = self.check_admin_privileges()
        self.optimized_processes = []
        self.cleared_caches = []
        
    def check_admin_privileges(self):
        """Check if running with admin privileges"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def optimize_current_process(self):
        """Optimize current process performance"""
        try:
            current_process = psutil.Process()
            
            # Set high priority if possible
            try:
                current_process.nice(psutil.HIGH_PRIORITY_CLASS)
                self.logger.info("Process priority set to high")
                return True, "Process priority optimized"
            except psutil.AccessDenied:
                self.logger.warning("Cannot set high priority - limited privileges")
                return False, "Priority optimization requires admin privileges"
                
        except Exception as e:
            self.logger.error(f"Process optimization failed: {e}")
            return False, f"Process optimization failed: {e}"
    
    def clear_user_temp_files(self):
        """Clear user temporary files (no admin required)"""
        try:
            cleaned_size = 0
            temp_paths = [
                tempfile.gettempdir(),
                os.path.expanduser("~\\AppData\\Local\\Temp"),
                os.path.expanduser("~\\AppData\\Local\\Microsoft\\Windows\\INetCache"),
                os.path.expanduser("~\\AppData\\Roaming\\Microsoft\\Teams\\tmp"),
                os.path.expanduser("~\\AppData\\Local\\Discord\\Cache"),
                os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache"),
                os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cache")
            ]
            
            cleaned_files = 0
            for temp_path in temp_paths:
                if os.path.exists(temp_path):
                    try:
                        for root, dirs, files in os.walk(temp_path):
                            for file in files:
                                try:
                                    file_path = os.path.join(root, file)
                                    if os.path.isfile(file_path):
                                        file_size = os.path.getsize(file_path)
                                        os.remove(file_path)
                                        cleaned_size += file_size
                                        cleaned_files += 1
                                except (PermissionError, FileNotFoundError):
                                    continue
                                except Exception:
                                    continue
                    except Exception:
                        continue
            
            cleaned_mb = cleaned_size / (1024 * 1024)
            self.logger.info(f"User temp files cleaned: {cleaned_mb:.2f} MB, {cleaned_files} files")
            return True, f"{cleaned_mb:.2f} MB temp files cleaned ({cleaned_files} files)"
            
        except Exception as e:
            self.logger.error(f"Temp file cleanup failed: {e}")
            return False, f"Temp file cleanup failed: {e}"
    
    def optimize_user_startup(self):
        """Optimize user startup programs (current user only)"""
        try:
            startup_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
            
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, startup_key, 0, 
                                   winreg.KEY_READ | winreg.KEY_WRITE)
                
                # Get list of startup items
                startup_items = []
                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        startup_items.append((name, value))
                        i += 1
                    except OSError:
                        break
                
                # Identify non-essential startup items
                non_essential = []
                non_essential_keywords = [
                    'spotify', 'steam', 'discord', 'skype', 'adobe', 'java', 
                    'quicktime', 'realplayer', 'winrar', 'torrent'
                ]
                
                for name, value in startup_items:
                    for keyword in non_essential_keywords:
                        if keyword.lower() in name.lower() or keyword.lower() in value.lower():
                            non_essential.append(name)
                            break
                
                # Remove non-essential items
                removed_count = 0
                for item_name in non_essential:
                    try:
                        winreg.DeleteValue(key, item_name)
                        removed_count += 1
                        self.logger.info(f"Removed startup item: {item_name}")
                    except Exception:
                        continue
                
                winreg.CloseKey(key)
                
                return True, f"{removed_count} non-essential startup items disabled"
                
            except PermissionError:
                return False, "Startup optimization requires admin privileges"
                
        except Exception as e:
            self.logger.error(f"Startup optimization failed: {e}")
            return False, f"Startup optimization failed: {e}"
    
    def optimize_user_services(self):
        """Optimize user-level services and processes"""
        try:
            # Target user processes that can be safely optimized
            target_processes = [
                'notepad.exe', 'calculator.exe', 'mspaint.exe', 
                'wordpad.exe', 'write.exe', 'charmap.exe'
            ]
            
            optimized_count = 0
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'].lower() in target_processes:
                        # Lower priority for non-essential processes
                        proc.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
                        optimized_count += 1
                        self.optimized_processes.append(proc.info['name'])
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                except Exception:
                    continue
            
            self.logger.info(f"Optimized {optimized_count} user processes")
            return True, f"{optimized_count} user processes optimized"
            
        except Exception as e:
            self.logger.error(f"Service optimization failed: {e}")
            return False, f"Service optimization failed: {e}"
    
    def clear_dns_cache(self):
        """Clear DNS cache"""
        try:
            result = subprocess.run("ipconfig /flushdns", shell=True, 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info("DNS cache cleared")
                return True, "DNS cache cleared successfully"
            else:
                return False, "DNS cache clear failed"
                
        except Exception as e:
            self.logger.error(f"DNS cache clear failed: {e}")
            return False, f"DNS cache clear failed: {e}"
    
    def optimize_network_settings(self):
        """Optimize network settings (user-level)"""
        try:
            # Clear network cache files
            network_cache_paths = [
                os.path.expanduser("~\\AppData\\Local\\Microsoft\\Windows\\INetCache"),
                os.path.expanduser("~\\AppData\\Local\\Microsoft\\Windows\\WebCache"),
                os.path.expanduser("~\\AppData\\Roaming\\Microsoft\\Windows\\Cookies")
            ]
            
            cleared_size = 0
            for cache_path in network_cache_paths:
                if os.path.exists(cache_path):
                    try:
                        for root, dirs, files in os.walk(cache_path):
                            for file in files:
                                try:
                                    file_path = os.path.join(root, file)
                                    file_size = os.path.getsize(file_path)
                                    os.remove(file_path)
                                    cleared_size += file_size
                                except:
                                    continue
                    except:
                        continue
            
            cleared_mb = cleared_size / (1024 * 1024)
            self.logger.info(f"Network cache cleared: {cleared_mb:.2f} MB")
            return True, f"Network cache cleared: {cleared_mb:.2f} MB"
            
        except Exception as e:
            self.logger.error(f"Network optimization failed: {e}")
            return False, f"Network optimization failed: {e}"
    
    def optimize_system_memory(self):
        """Optimize system memory usage"""
        try:
            # Force garbage collection
            import gc
            gc.collect()
            
            # Clear working set of current process
            try:
                ctypes.windll.kernel32.SetProcessWorkingSetSize(-1, -1, -1)
            except:
                pass
            
            # Get memory info
            memory = psutil.virtual_memory()
            available_gb = memory.available / (1024**3)
            
            self.logger.info(f"Memory optimization completed. Available: {available_gb:.2f} GB")
            return True, f"Memory optimized. Available: {available_gb:.2f} GB"
            
        except Exception as e:
            self.logger.error(f"Memory optimization failed: {e}")
            return False, f"Memory optimization failed: {e}"
    
    def set_power_plan_balanced(self):
        """Set power plan to balanced (safer for non-admin)"""
        try:
            # Balanced power plan GUID
            result = subprocess.run(
                "powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e", 
                shell=True, capture_output=True, text=True
            )
            
            if result.returncode == 0:
                self.logger.info("Power plan set to balanced")
                return True, "Power plan set to balanced"
            else:
                return False, "Power plan change requires admin privileges"
                
        except Exception as e:
            self.logger.error(f"Power plan change failed: {e}")
            return False, f"Power plan change failed: {e}"
    
    def perform_full_optimization(self, selected_options=None):
        """Perform full optimization with selected options"""
        results = []
        
        try:
            if not selected_options:
                selected_options = [
                    'clean_temp', 'optimize_startup', 'optimize_memory', 
                    'clear_dns', 'optimize_network'
                ]
            
            optimization_functions = {
                'clean_temp': self.clear_user_temp_files,
                'optimize_startup': self.optimize_user_startup,
                'optimize_memory': self.optimize_system_memory,
                'clear_dns': self.clear_dns_cache,
                'optimize_network': self.optimize_network_settings,
                'optimize_processes': self.optimize_user_services,
                'optimize_current': self.optimize_current_process
            }
            
            for option in selected_options:
                if option in optimization_functions:
                    try:
                        success, message = optimization_functions[option]()
                        results.append((option, success, message))
                        time.sleep(0.5)  # Small delay between operations
                    except Exception as e:
                        results.append((option, False, f"Error: {e}"))
            
            # Summary
            successful = [r for r in results if r[1]]
            total = len(results)
            success_count = len(successful)
            
            self.logger.info(f"Optimization complete: {success_count}/{total} operations successful")
            return results, f"Optimization complete: {success_count}/{total} operations successful"
            
        except Exception as e:
            self.logger.error(f"Full optimization failed: {e}")
            return [], f"Full optimization failed: {e}"
    
    def get_optimization_report(self):
        """Get optimization report"""
        try:
            # System info
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            report = {
                'admin_privileges': self.is_admin,
                'cpu_usage': cpu_percent,
                'memory_usage': memory.percent,
                'memory_available': memory.available / (1024**3),
                'disk_usage': (disk.used / disk.total) * 100,
                'optimized_processes': len(self.optimized_processes),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Report generation failed: {e}")
            return {}
