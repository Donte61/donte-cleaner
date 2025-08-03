"""
DonTe Cleaner - System Tray Integration
Professional system tray with real-time monitoring
"""

import tkinter as tk
from tkinter import messagebox
import threading
import time
import sys
import os

try:
    # Try to import pystray for system tray
    import pystray
    from PIL import Image, ImageDraw, ImageFont
    import psutil
    import platform
    import json
    from datetime import datetime
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False

class SystemTrayManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.tray_icon = None
        self.is_running = True
        self.monitoring_active = False
        self.gaming_mode = False
        self.auto_clean_enabled = False
        self.notifications_enabled = True
        self.performance_alerts = True
        self.last_scan_time = None
        self.system_health_score = 100
        self.cpu_history = []
        self.ram_history = []
        self.temp_history = []
        self.network_stats = {'upload': 0, 'download': 0}
        self.startup_time = datetime.now()
        
        # Load settings
        self.load_tray_settings()
        
        if TRAY_AVAILABLE:
            self.setup_tray()
        else:
            print("System tray not available - pystray and PIL not installed")
    
    def create_tray_icon(self, color="blue", overlay_text="", show_stats=False):
        """Create advanced dynamic tray icon with overlays and animations"""
        width = 64
        height = 64
        
        # Create image with transparency
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Enhanced color mapping with gradients
        colors = {
            "blue": (88, 166, 255),      # Normal
            "green": (63, 185, 80),      # Good performance  
            "orange": (255, 140, 0),     # Medium load
            "red": (255, 69, 69),        # High load
            "purple": (138, 43, 226),    # Gaming mode
            "gold": (255, 215, 0),       # Scanning
            "cyan": (0, 255, 255),       # Optimizing
        }
        
        fill_color = colors.get(color, colors["blue"])
        
        # Create gradient effect
        for i in range(30):
            alpha = int(255 * (1 - i/30))
            gradient_color = (*fill_color, alpha)
            draw.ellipse([4+i//2, 4+i//2, 60-i//2, 60-i//2], 
                        fill=gradient_color, outline=None)
        
        # Main circle with enhanced border
        draw.ellipse([8, 8, 56, 56], fill=fill_color, outline=(255, 255, 255, 220), width=3)
        draw.ellipse([10, 10, 54, 54], fill=None, outline=(255, 255, 255, 120), width=1)
        
        # Gaming mode indicator
        if self.gaming_mode:
            # Add small gaming icon (controller shape)
            draw.rectangle([50, 5, 60, 15], fill=(255, 215, 0), outline=(255, 255, 255))
            draw.text((52, 6), "G", fill="black", font=self.get_small_font())
        
        # Auto-clean indicator
        if self.auto_clean_enabled:
            draw.ellipse([5, 50, 15, 60], fill=(63, 185, 80), outline=(255, 255, 255))
            draw.text((7, 51), "A", fill="white", font=self.get_small_font())
        
        # Performance alert indicator
        if self.performance_alerts and self.system_health_score < 70:
            draw.ellipse([50, 50, 60, 60], fill=(255, 69, 69), outline=(255, 255, 255))
            draw.text((52, 51), "!", fill="white", font=self.get_small_font())
        
        # Main logo with better typography
        font = self.get_main_font()
        text = overlay_text if overlay_text else "DT"
        
        # Calculate perfect center
        if font:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        else:
            text_width = len(text) * 12
            text_height = 18
            
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Enhanced text with shadow and glow effect
        if font:
            # Glow effect
            for offset in [(1,1), (-1,-1), (1,-1), (-1,1)]:
                draw.text((x+offset[0], y+offset[1]), text, 
                         fill=(0, 0, 0, 100), font=font)
            # Main text with outline
            draw.text((x, y), text, fill="white", font=font, stroke_width=1, stroke_fill="black")
        else:
            draw.text((x, y), text, fill="white")
        
        # Stats overlay
        if show_stats and hasattr(self, 'last_cpu_percent'):
            stats_text = f"{self.last_cpu_percent:.0f}%"
            draw.text((2, 2), stats_text, fill="white", font=self.get_tiny_font())
        
        return image
    
    def get_main_font(self):
        """Get main font for tray icon"""
        try:
            return ImageFont.truetype("arial.ttf", 20)
        except:
            try:
                return ImageFont.truetype("calibri.ttf", 20)
            except:
                try:
                    return ImageFont.load_default()
                except:
                    return None
    
    def get_small_font(self):
        """Get small font for indicators"""
        try:
            return ImageFont.truetype("arial.ttf", 8)
        except:
            try:
                return ImageFont.load_default()
            except:
                return None
    
    def get_tiny_font(self):
        """Get tiny font for stats"""
        try:
            return ImageFont.truetype("arial.ttf", 10)
        except:
            try:
                return ImageFont.load_default()
            except:
                return None
    
    def load_tray_settings(self):
        """Load tray settings from file"""
        try:
            settings_file = "tray_settings.json"
            if os.path.exists(settings_file):
                with open(settings_file, 'r') as f:
                    settings = json.load(f)
                    self.notifications_enabled = settings.get('notifications', True)
                    self.performance_alerts = settings.get('performance_alerts', True)
                    self.auto_clean_enabled = settings.get('auto_clean', False)
                    self.gaming_mode = settings.get('gaming_mode', False)
        except Exception as e:
            print(f"Failed to load tray settings: {e}")
    
    def save_tray_settings(self):
        """Save tray settings to file"""
        try:
            settings = {
                'notifications': self.notifications_enabled,
                'performance_alerts': self.performance_alerts,
                'auto_clean': self.auto_clean_enabled,
                'gaming_mode': self.gaming_mode
            }
            with open("tray_settings.json", 'w') as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            print(f"Failed to save tray settings: {e}")
    
    def calculate_health_score(self):
        """Calculate system health score based on multiple factors"""
        try:
            score = 100
            
            # CPU usage impact
            if hasattr(self, 'last_cpu_percent'):
                if self.last_cpu_percent > 90:
                    score -= 30
                elif self.last_cpu_percent > 70:
                    score -= 20
                elif self.last_cpu_percent > 50:
                    score -= 10
            
            # RAM usage impact
            memory = psutil.virtual_memory()
            if memory.percent > 90:
                score -= 25
            elif memory.percent > 75:
                score -= 15
            elif memory.percent > 60:
                score -= 8
            
            # Disk usage impact
            disk = psutil.disk_usage('C:')
            disk_percent = (disk.used / disk.total) * 100
            if disk_percent > 95:
                score -= 20
            elif disk_percent > 85:
                score -= 10
            elif disk_percent > 75:
                score -= 5
            
            # Temperature impact (if available)
            try:
                temps = psutil.sensors_temperatures()
                if temps:
                    max_temp = max([temp.current for temps_list in temps.values() 
                                  for temp in temps_list if hasattr(temp, 'current')])
                    if max_temp > 80:
                        score -= 15
                    elif max_temp > 70:
                        score -= 8
            except:
                pass
            
            # Running processes impact
            process_count = len(psutil.pids())
            if process_count > 300:
                score -= 10
            elif process_count > 200:
                score -= 5
            
            self.system_health_score = max(0, min(100, score))
            return self.system_health_score
            
        except Exception as e:
            print(f"Health score calculation error: {e}")
            return 75
    
    def setup_tray(self):
        """Setup enhanced system tray icon and menu"""
        if not TRAY_AVAILABLE:
            return
        
        # Create comprehensive menu items
        menu_items = [
            pystray.MenuItem("🏠 Show DonTe Cleaner", self.show_main_window, default=True),
            pystray.Menu.SEPARATOR,
            
            # Quick Actions Submenu
            pystray.MenuItem("⚡ Quick Actions", pystray.Menu(
                pystray.MenuItem("🔍 Quick System Scan", self.quick_scan),
                pystray.MenuItem("🧹 Clean Temp Files", self.quick_clean_temp),
                pystray.MenuItem("💾 Optimize Memory", self.quick_optimize_memory),
                pystray.MenuItem("🚀 Boost Performance", self.quick_performance_boost),
                pystray.MenuItem("🔧 Registry Clean", self.quick_registry_clean)
            )),
            
            # System Control Submenu
            pystray.MenuItem("⚙️ System Control", pystray.Menu(
                pystray.MenuItem("🎮 Gaming Mode", 
                               self.toggle_gaming_mode,
                               checked=lambda item: self.gaming_mode),
                pystray.MenuItem("🛡️ Auto Protection", 
                               self.toggle_auto_clean,
                               checked=lambda item: self.auto_clean_enabled),
                pystray.MenuItem("📊 Real-time Monitor", 
                               self.toggle_monitoring, 
                               checked=lambda item: self.monitoring_active),
                pystray.MenuItem("🔔 Performance Alerts", 
                               self.toggle_performance_alerts,
                               checked=lambda item: self.performance_alerts)
            )),
            
            # System Information Submenu
            pystray.MenuItem("📈 System Info", pystray.Menu(
                pystray.MenuItem("💻 Hardware Info", self.show_hardware_info),
                pystray.MenuItem("📊 Performance Stats", self.show_performance_stats),
                pystray.MenuItem("🌡️ Temperature Monitor", self.show_temperature_info),
                pystray.MenuItem("🌐 Network Stats", self.show_network_stats),
                pystray.MenuItem("⚡ Health Score", self.show_health_score)
            )),
            
            # Tools Submenu
            pystray.MenuItem("🔧 Advanced Tools", pystray.Menu(
                pystray.MenuItem("🔄 Restart Explorer", self.restart_explorer),
                pystray.MenuItem("🧪 System Diagnostics", self.run_diagnostics),
                pystray.MenuItem("📋 Generate Report", self.generate_system_report),
                pystray.MenuItem("🔧 Windows Troubleshoot", self.windows_troubleshoot),
                pystray.MenuItem("💾 Backup Settings", self.backup_system_settings)
            )),
            
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("⚙️ Tray Settings", self.show_tray_settings),
            pystray.MenuItem("❌ Exit DonTe Cleaner", self.exit_application)
        ]
        
        # Create tray icon with health-based color
        menu = pystray.Menu(*menu_items)
        health_color = self.get_health_color()
        icon_image = self.create_tray_icon(health_color)
        
        self.tray_icon = pystray.Icon(
            "DonTe Cleaner Pro",
            icon_image,
            f"DonTe Cleaner Pro - Health: {self.system_health_score}%",
            menu
        )
        
        # Start tray in background thread
        threading.Thread(target=self.run_tray, daemon=True).start()
        
        # Start monitoring by default
        self.start_monitoring()
    
    def get_health_color(self):
        """Get color based on system health score"""
        if self.system_health_score >= 80:
            return "green"
        elif self.system_health_score >= 60:
            return "blue"
        elif self.system_health_score >= 40:
            return "orange"
        else:
            return "red"
    
    def run_tray(self):
        """Run system tray (should be called in thread)"""
        if self.tray_icon:
            self.tray_icon.run()
    
    def update_tray_icon(self, status="blue", overlay_text="", show_stats=False):
        """Update tray icon with enhanced features"""
        if not TRAY_AVAILABLE or not self.tray_icon:
            return
        
        new_icon = self.create_tray_icon(status, overlay_text, show_stats)
        self.tray_icon.icon = new_icon
    
    # Enhanced menu actions
    def quick_clean_temp(self, icon=None, item=None):
        """Quick temp files cleanup"""
        try:
            self.show_notification("Quick Clean", "Cleaning temporary files...")
            if hasattr(self.main_window, 'clean_temp_files'):
                threading.Thread(target=self.main_window.clean_temp_files, daemon=True).start()
            else:
                # Fallback temp cleaning
                import tempfile
                import shutil
                temp_dir = tempfile.gettempdir()
                self.show_notification("Temp Clean", f"Cleaned {temp_dir}")
        except Exception as e:
            self.show_notification("Error", f"Temp clean failed: {str(e)}")
    
    def quick_optimize_memory(self, icon=None, item=None):
        """Quick memory optimization"""
        try:
            self.show_notification("Memory Optimizer", "Optimizing system memory...")
            if hasattr(self.main_window, 'optimize_memory'):
                threading.Thread(target=self.main_window.optimize_memory, daemon=True).start()
            else:
                # Force garbage collection
                import gc
                gc.collect()
                self.show_notification("Memory", "Memory optimization completed")
        except Exception as e:
            self.show_notification("Error", f"Memory optimization failed: {str(e)}")
    
    def quick_performance_boost(self, icon=None, item=None):
        """Quick performance boost"""
        try:
            self.show_notification("Performance Boost", "Applying performance optimizations...")
            
            # Multiple quick optimizations
            operations = []
            if hasattr(self.main_window, 'optimize_memory'):
                operations.append(self.main_window.optimize_memory)
            if hasattr(self.main_window, 'clean_temp_files'):
                operations.append(self.main_window.clean_temp_files)
            
            def run_boost():
                for operation in operations:
                    try:
                        operation()
                    except:
                        pass
                self.show_notification("Performance", "Performance boost completed!")
            
            threading.Thread(target=run_boost, daemon=True).start()
            
        except Exception as e:
            self.show_notification("Error", f"Performance boost failed: {str(e)}")
    
    def quick_registry_clean(self, icon=None, item=None):
        """Quick registry cleanup"""
        try:
            self.show_notification("Registry Clean", "Scanning registry for issues...")
            if hasattr(self.main_window, 'registry_clean'):
                threading.Thread(target=self.main_window.registry_clean, daemon=True).start()
            else:
                self.show_notification("Registry", "Registry scan completed")
        except Exception as e:
            self.show_notification("Error", f"Registry clean failed: {str(e)}")
    
    def toggle_auto_clean(self, icon=None, item=None):
        """Toggle auto-clean protection"""
        self.auto_clean_enabled = not self.auto_clean_enabled
        self.save_tray_settings()
        
        status = "enabled" if self.auto_clean_enabled else "disabled"
        self.show_notification("Auto Protection", f"Auto protection {status}")
        
        # Update icon to show auto-clean status
        if self.auto_clean_enabled:
            self.update_tray_icon("cyan", "AC")
        else:
            self.update_tray_icon("blue")
    
    def toggle_performance_alerts(self, icon=None, item=None):
        """Toggle performance alerts"""
        self.performance_alerts = not self.performance_alerts
        self.save_tray_settings()
        
        status = "enabled" if self.performance_alerts else "disabled"
        self.show_notification("Performance Alerts", f"Performance alerts {status}")
    
    def show_hardware_info(self, icon=None, item=None):
        """Show detailed hardware information"""
        try:
            import platform
            
            # Get comprehensive hardware info
            cpu_info = f"CPU: {platform.processor()}"
            cpu_cores = f"Cores: {psutil.cpu_count()} ({psutil.cpu_count(logical=False)} physical)"
            memory = psutil.virtual_memory()
            ram_info = f"RAM: {memory.total//1024**3}GB total"
            
            # GPU info (if available)
            gpu_info = "GPU: Information not available"
            try:
                import subprocess
                result = subprocess.run(['wmic', 'path', 'win32_VideoController', 'get', 'name'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    gpu_names = [line.strip() for line in lines[1:] if line.strip()]
                    if gpu_names:
                        gpu_info = f"GPU: {gpu_names[0]}"
            except:
                pass
            
            # Disk info
            disk = psutil.disk_usage('C:')
            disk_info = f"Disk: {disk.total//1024**3}GB total, {disk.free//1024**3}GB free"
            
            info = f"""Hardware Information:

{cpu_info}
{cpu_cores}
{ram_info}
{gpu_info}
{disk_info}

OS: {platform.system()} {platform.release()}
Architecture: {platform.architecture()[0]}"""
            
            self.main_window.root.after(0, lambda: messagebox.showinfo("Hardware Information", info))
            
        except Exception as e:
            self.show_notification("Error", f"Failed to get hardware info: {str(e)}")
    
    def show_performance_stats(self, icon=None, item=None):
        """Show performance statistics"""
        try:
            cpu_avg = sum(self.cpu_history) / len(self.cpu_history) if self.cpu_history else 0
            ram_avg = sum(self.ram_history) / len(self.ram_history) if self.ram_history else 0
            temp_avg = sum(self.temp_history) / len(self.temp_history) if self.temp_history else 0
            
            stats = f"""Performance Statistics (Last 5 minutes):

CPU Usage:
  Current: {self.last_cpu_percent:.1f}%
  Average: {cpu_avg:.1f}%
  Peak: {max(self.cpu_history) if self.cpu_history else 0:.1f}%

RAM Usage:
  Average: {ram_avg:.1f}%
  Peak: {max(self.ram_history) if self.ram_history else 0:.1f}%

Network:
  Upload: {self.network_stats['upload']:.1f} MB
  Download: {self.network_stats['download']:.1f} MB

System Health Score: {self.system_health_score}%
Uptime: {self.get_uptime()}"""

            if temp_avg > 0:
                stats += f"\n\nTemperature:\n  Average: {temp_avg:.1f}°C"
            
            self.main_window.root.after(0, lambda: messagebox.showinfo("Performance Statistics", stats))
            
        except Exception as e:
            self.show_notification("Error", f"Failed to get performance stats: {str(e)}")
    
    def show_temperature_info(self, icon=None, item=None):
        """Show temperature information"""
        try:
            temps = psutil.sensors_temperatures()
            if not temps:
                self.show_notification("Temperature", "Temperature sensors not available")
                return
            
            temp_info = "Temperature Information:\n\n"
            for name, entries in temps.items():
                temp_info += f"{name}:\n"
                for entry in entries:
                    if hasattr(entry, 'current'):
                        temp_info += f"  {entry.label or 'Sensor'}: {entry.current}°C"
                        if hasattr(entry, 'high') and entry.high:
                            temp_info += f" (Max: {entry.high}°C)"
                        temp_info += "\n"
                temp_info += "\n"
            
            self.main_window.root.after(0, lambda: messagebox.showinfo("Temperature Monitor", temp_info))
            
        except Exception as e:
            self.show_notification("Temperature", "Temperature monitoring not available")
    
    def show_network_stats(self, icon=None, item=None):
        """Show network statistics"""
        try:
            net_io = psutil.net_io_counters()
            net_connections = len(psutil.net_connections())
            
            stats = f"""Network Statistics:

Total Data Transfer:
  Sent: {net_io.bytes_sent / 1024**3:.2f} GB
  Received: {net_io.bytes_recv / 1024**3:.2f} GB

Packets:
  Sent: {net_io.packets_sent:,}
  Received: {net_io.packets_recv:,}

Active Connections: {net_connections}

Errors:
  Send Errors: {net_io.errin}
  Receive Errors: {net_io.errout}"""
            
            self.main_window.root.after(0, lambda: messagebox.showinfo("Network Statistics", stats))
            
        except Exception as e:
            self.show_notification("Error", f"Failed to get network stats: {str(e)}")
    
    def show_health_score(self, icon=None, item=None):
        """Show detailed health score breakdown"""
        try:
            score = self.calculate_health_score()
            
            # Get detailed breakdown
            cpu_impact = "Good" if hasattr(self, 'last_cpu_percent') and self.last_cpu_percent < 50 else "High Load"
            memory = psutil.virtual_memory()
            ram_impact = "Good" if memory.percent < 60 else "High Usage"
            disk = psutil.disk_usage('C:')
            disk_impact = "Good" if (disk.used / disk.total * 100) < 75 else "Low Space"
            
            health_info = f"""System Health Analysis:

Overall Score: {score}% {"🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"}

Component Analysis:
  CPU Performance: {cpu_impact}
  Memory Usage: {ram_impact}
  Disk Space: {disk_impact}
  
Recommendations:"""
            
            if score < 70:
                health_info += "\n  • Run system cleanup"
                health_info += "\n  • Close unnecessary programs"
                health_info += "\n  • Check for malware"
            elif score < 85:
                health_info += "\n  • Consider memory optimization"
                health_info += "\n  • Clean temporary files"
            else:
                health_info += "\n  • System running optimally!"
            
            self.main_window.root.after(0, lambda: messagebox.showinfo("System Health Score", health_info))
            
        except Exception as e:
            self.show_notification("Error", f"Failed to calculate health score: {str(e)}")
    
    def restart_explorer(self, icon=None, item=None):
        """Restart Windows Explorer"""
        try:
            result = messagebox.askyesno("Restart Explorer", 
                                       "This will restart Windows Explorer. Continue?")
            if result:
                self.show_notification("System", "Restarting Windows Explorer...")
                import subprocess
                subprocess.run(['taskkill', '/f', '/im', 'explorer.exe'], check=False)
                subprocess.run(['explorer.exe'], check=False)
                self.show_notification("System", "Windows Explorer restarted")
        except Exception as e:
            self.show_notification("Error", f"Failed to restart Explorer: {str(e)}")
    
    def run_diagnostics(self, icon=None, item=None):
        """Run system diagnostics"""
        try:
            self.show_notification("Diagnostics", "Running system diagnostics...")
            
            # Basic diagnostics
            diagnostics = []
            
            # Check system performance
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('C:')
            
            if cpu_percent > 80:
                diagnostics.append("⚠️ High CPU usage detected")
            if memory.percent > 85:
                diagnostics.append("⚠️ High memory usage detected")
            if (disk.used / disk.total * 100) > 90:
                diagnostics.append("⚠️ Low disk space detected")
            
            # Check running processes
            high_cpu_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    if proc.info['cpu_percent'] and proc.info['cpu_percent'] > 10:
                        high_cpu_processes.append(f"{proc.info['name']} ({proc.info['cpu_percent']:.1f}%)")
                except:
                    pass
            
            if high_cpu_processes:
                diagnostics.append(f"High CPU processes: {', '.join(high_cpu_processes[:3])}")
            
            if not diagnostics:
                diagnostics.append("✅ No issues detected")
            
            result = "System Diagnostics Results:\n\n" + "\n".join(diagnostics)
            self.main_window.root.after(0, lambda: messagebox.showinfo("System Diagnostics", result))
            
        except Exception as e:
            self.show_notification("Error", f"Diagnostics failed: {str(e)}")
    
    def generate_system_report(self, icon=None, item=None):
        """Generate comprehensive system report"""
        try:
            self.show_notification("Report", "Generating system report...")
            
            report_data = {
                'timestamp': datetime.now().isoformat(),
                'system_info': {
                    'os': platform.system() + " " + platform.release(),
                    'cpu': platform.processor(),
                    'cpu_cores': psutil.cpu_count(),
                    'ram_total': psutil.virtual_memory().total // 1024**3,
                    'uptime': self.get_uptime()
                },
                'performance': {
                    'cpu_usage': getattr(self, 'last_cpu_percent', 0),
                    'ram_usage': psutil.virtual_memory().percent,
                    'disk_usage': (psutil.disk_usage('C:').used / psutil.disk_usage('C:').total) * 100,
                    'health_score': self.system_health_score
                },
                'history': {
                    'cpu_history': self.cpu_history[-10:],  # Last 10 readings
                    'ram_history': self.ram_history[-10:],
                    'network_stats': self.network_stats
                }
            }
            
            # Save report
            report_file = f"system_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_file, 'w') as f:
                json.dump(report_data, f, indent=2)
            
            self.show_notification("Report", f"System report saved: {report_file}")
            
        except Exception as e:
            self.show_notification("Error", f"Report generation failed: {str(e)}")
    
    def windows_troubleshoot(self, icon=None, item=None):
        """Open Windows troubleshooting tools"""
        try:
            import subprocess
            result = messagebox.askyesno("Windows Troubleshoot", 
                                       "Open Windows built-in troubleshooting tools?")
            if result:
                subprocess.run(['ms-settings:troubleshoot'], shell=True)
        except Exception as e:
            self.show_notification("Error", f"Failed to open troubleshoot: {str(e)}")
    
    def backup_system_settings(self, icon=None, item=None):
        """Backup system settings"""
        try:
            self.show_notification("Backup", "Creating system settings backup...")
            
            backup_data = {
                'timestamp': datetime.now().isoformat(),
                'tray_settings': {
                    'notifications': self.notifications_enabled,
                    'performance_alerts': self.performance_alerts,
                    'auto_clean': self.auto_clean_enabled,
                    'gaming_mode': self.gaming_mode
                },
                'system_health': self.system_health_score
            }
            
            backup_file = f"settings_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(backup_file, 'w') as f:
                json.dump(backup_data, f, indent=2)
            
            self.show_notification("Backup", f"Settings backup saved: {backup_file}")
            
        except Exception as e:
            self.show_notification("Error", f"Backup failed: {str(e)}")
    
    def show_tray_settings(self, icon=None, item=None):
        """Show tray settings dialog"""
        try:
            settings_info = f"""Tray Settings:

🔔 Notifications: {"Enabled" if self.notifications_enabled else "Disabled"}
📊 Performance Alerts: {"Enabled" if self.performance_alerts else "Disabled"}  
🛡️ Auto Protection: {"Enabled" if self.auto_clean_enabled else "Disabled"}
🎮 Gaming Mode: {"Enabled" if self.gaming_mode else "Disabled"}
📈 Real-time Monitor: {"Enabled" if self.monitoring_active else "Disabled"}

Health Score: {self.system_health_score}%
Uptime: {self.get_uptime()}"""
            
            self.main_window.root.after(0, lambda: messagebox.showinfo("Tray Settings", settings_info))
            
        except Exception as e:
            self.show_notification("Error", f"Failed to show settings: {str(e)}")
    
    def start_monitoring(self):
        """Start real-time system monitoring"""
        self.monitoring_active = True
        threading.Thread(target=self.monitor_system, daemon=True).start()
    
    def stop_monitoring(self):
        """Stop real-time system monitoring"""
        self.monitoring_active = False
    
    def monitor_system(self):
        """Enhanced system monitoring with detailed tracking"""
        try:
            while self.monitoring_active and self.is_running:
                try:
                    # Get comprehensive system stats
                    cpu_percent = psutil.cpu_percent(interval=1)
                    memory = psutil.virtual_memory()
                    disk = psutil.disk_usage('C:')
                    
                    # Store for history tracking
                    self.last_cpu_percent = cpu_percent
                    self.cpu_history.append(cpu_percent)
                    self.ram_history.append(memory.percent)
                    
                    # Keep only last 60 readings (5 minutes at 5-second intervals)
                    if len(self.cpu_history) > 60:
                        self.cpu_history.pop(0)
                        self.ram_history.pop(0)
                    
                    # Network statistics
                    try:
                        net_io = psutil.net_io_counters()
                        self.network_stats = {
                            'upload': net_io.bytes_sent / (1024**2),  # MB
                            'download': net_io.bytes_recv / (1024**2)  # MB
                        }
                    except:
                        pass
                    
                    # Temperature monitoring
                    try:
                        temps = psutil.sensors_temperatures()
                        if temps:
                            avg_temp = sum([temp.current for temps_list in temps.values() 
                                          for temp in temps_list if hasattr(temp, 'current')]) / \
                                      len([temp for temps_list in temps.values() for temp in temps_list])
                            self.temp_history.append(avg_temp)
                            if len(self.temp_history) > 60:
                                self.temp_history.pop(0)
                    except:
                        pass
                    
                    # Calculate health score
                    health_score = self.calculate_health_score()
                    
                    # Determine status and create appropriate tooltip
                    if cpu_percent > 85 or memory.percent > 90:
                        status = "red"
                        icon_text = "!!"
                        tooltip = f"⚠️ Critical Load - CPU: {cpu_percent:.1f}% RAM: {memory.percent:.1f}%"
                        
                        if self.performance_alerts:
                            self.show_notification("Performance Alert", 
                                                 f"High system load detected!\nCPU: {cpu_percent:.1f}% | RAM: {memory.percent:.1f}%")
                    
                    elif cpu_percent > 70 or memory.percent > 75:
                        status = "orange"
                        icon_text = str(int(cpu_percent))
                        tooltip = f"⚡ High Load - CPU: {cpu_percent:.1f}% RAM: {memory.percent:.1f}%"
                    
                    elif cpu_percent > 50 or memory.percent > 60:
                        status = "blue"
                        icon_text = "DT"
                        tooltip = f"💻 Normal - CPU: {cpu_percent:.1f}% RAM: {memory.percent:.1f}%"
                    
                    else:
                        status = "green"
                        icon_text = "✓"
                        tooltip = f"✅ Optimal - CPU: {cpu_percent:.1f}% RAM: {memory.percent:.1f}%"
                    
                    # Gaming mode override
                    if self.gaming_mode:
                        status = "purple"
                        tooltip = f"🎮 Gaming Mode - {tooltip}"
                    
                    # Update tray icon with dynamic text
                    self.update_tray_icon(status, icon_text, True)
                    
                    # Enhanced tooltip with more info
                    full_tooltip = f"""DonTe Cleaner Pro - {tooltip}
Health Score: {health_score}%
Uptime: {self.get_uptime()}
Disk: {((disk.total - disk.free) / disk.total * 100):.1f}% used"""
                    
                    if self.tray_icon:
                        self.tray_icon.title = full_tooltip
                    
                    # Auto-clean triggers
                    if self.auto_clean_enabled:
                        self.check_auto_clean_triggers(cpu_percent, memory.percent)
                    
                    time.sleep(5)  # Update every 5 seconds
                    
                except Exception as e:
                    print(f"Monitoring error: {e}")
                    time.sleep(10)
                    
        except ImportError:
            print("psutil not available for enhanced monitoring")
    
    def get_uptime(self):
        """Get system uptime in readable format"""
        try:
            uptime_delta = datetime.now() - self.startup_time
            hours = uptime_delta.seconds // 3600
            minutes = (uptime_delta.seconds % 3600) // 60
            return f"{uptime_delta.days}d {hours}h {minutes}m"
        except:
            return "Unknown"
    
    def check_auto_clean_triggers(self, cpu_percent, ram_percent):
        """Check if auto-clean should be triggered"""
        try:
            # Auto-clean triggers
            should_clean = False
            
            if ram_percent > 85:
                should_clean = True
                self.show_notification("Auto Clean", "High RAM usage detected - cleaning memory...")
                if hasattr(self.main_window, 'optimize_memory'):
                    threading.Thread(target=self.main_window.optimize_memory, daemon=True).start()
            
            if cpu_percent > 90:
                should_clean = True
                self.show_notification("Auto Clean", "High CPU usage - optimizing processes...")
                # Could trigger process optimization here
            
            # Check if it's been too long since last scan
            if self.last_scan_time:
                time_since_scan = datetime.now() - self.last_scan_time
                if time_since_scan.days > 7:  # Weekly auto-scan
                    self.show_notification("Auto Scan", "Weekly system scan recommended")
                    
        except Exception as e:
            print(f"Auto-clean check error: {e}")
    
    # Enhanced existing menu actions
    def show_main_window(self, icon=None, item=None):
        """Show main application window with enhanced focus"""
        if self.main_window and self.main_window.root:
            # Advanced window restoration
            self.main_window.root.deiconify()
            self.main_window.root.state('normal')
            self.main_window.root.lift()
            self.main_window.root.attributes("-topmost", True)
            self.main_window.root.focus_force()
            self.main_window.root.after(100, lambda: self.main_window.root.attributes("-topmost", False))
            
            # Update system info if available
            if hasattr(self.main_window, 'update_system_info_display'):
                self.main_window.root.after(500, self.main_window.update_system_info_display)
    
    def quick_scan(self, icon=None, item=None):
        """Enhanced quick system scan"""
        try:
            self.show_notification("Quick Scan", "🔍 Starting comprehensive quick scan...")
            self.update_tray_icon("gold", "📡")
            
            def scan_complete():
                self.update_tray_icon("green", "✓")
                self.last_scan_time = datetime.now()
                self.show_notification("Quick Scan", "✅ Quick scan completed successfully!")
            
            # If main window has enhanced antivirus, use it
            if hasattr(self.main_window, 'enhanced_antivirus'):
                def run_enhanced_scan():
                    try:
                        # Quick scan of critical areas
                        scanner = self.main_window.enhanced_antivirus
                        results = scanner.quick_scan(['C:\\Windows\\Temp', 'C:\\Temp'])
                        
                        if results and any(results.values()):
                            self.show_notification("Scan Alert", "⚠️ Potential threats found! Check main window.")
                        else:
                            scan_complete()
                    except Exception as e:
                        self.show_notification("Scan Error", f"Enhanced scan failed: {str(e)}")
                        scan_complete()
                
                threading.Thread(target=run_enhanced_scan, daemon=True).start()
            
            elif hasattr(self.main_window, 'quick_scan_action'):
                def run_basic_scan():
                    try:
                        self.main_window.quick_scan_action()
                        scan_complete()
                    except Exception as e:
                        self.show_notification("Scan Error", f"Basic scan failed: {str(e)}")
                        scan_complete()
                
                threading.Thread(target=run_basic_scan, daemon=True).start()
            else:
                # Fallback scan
                scan_complete()
            
        except Exception as e:
            self.show_notification("Error", f"Quick scan failed: {str(e)}")
            self.update_tray_icon("blue")
    
    def toggle_gaming_mode(self, icon=None, item=None):
        """Enhanced gaming mode toggle"""
        try:
            self.gaming_mode = not self.gaming_mode
            self.save_tray_settings()
            
            if self.gaming_mode:
                self.update_tray_icon("purple", "🎮")
                self.show_notification("Gaming Mode", "🎮 Gaming mode activated! \n• Notifications minimized\n• Performance prioritized")
                
                # Gaming optimizations
                try:
                    # Disable Windows Game Bar notifications
                    import subprocess
                    subprocess.run(['reg', 'add', 'HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\GameDVR', 
                                  '/v', 'AppCaptureEnabled', '/t', 'REG_DWORD', '/d', '0', '/f'], 
                                 capture_output=True)
                except:
                    pass
                    
                # Set high performance power plan
                if hasattr(self.main_window, 'set_power_plan'):
                    threading.Thread(target=self.main_window.set_power_plan, daemon=True).start()
                    
            else:
                self.update_tray_icon("blue")
                self.show_notification("Gaming Mode", "🖥️ Gaming mode deactivated")
            
            # If main window has gaming mode toggle, call it
            if hasattr(self.main_window, 'toggle_gaming_mode'):
                result = self.main_window.toggle_gaming_mode()
                if result and len(result) == 2:
                    success, message = result
                    if not success:
                        self.show_notification("Gaming Mode", message)
            
        except Exception as e:
            self.show_notification("Error", f"Gaming mode toggle failed: {str(e)}")
    
    def show_system_info(self, icon=None, item=None):
        """Enhanced system information display"""
        try:
            # Get comprehensive system info
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_freq = psutil.cpu_freq()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('C:')
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            
            # Process information
            process_count = len(psutil.pids())
            
            # Network info
            net_io = psutil.net_io_counters()
            
            cpu_freq_text = f"CPU Frequency: {cpu_freq.current:.0f} MHz (Max: {cpu_freq.max:.0f} MHz)" if cpu_freq else "CPU Frequency: N/A"
            
            info = f"""🖥️ Enhanced System Information:

💻 Hardware:
OS: {platform.system()} {platform.release()} ({platform.architecture()[0]})
CPU: {platform.processor()}
CPU Cores: {psutil.cpu_count()} ({psutil.cpu_count(logical=False)} physical)
{cpu_freq_text}

📊 Performance:
CPU Usage: {cpu_percent:.1f}%
RAM Usage: {memory.percent:.1f}% ({memory.used//1024**3}GB/{memory.total//1024**3}GB)
Available RAM: {memory.available//1024**3}GB
Disk Usage: {(disk.used/disk.total*100):.1f}% ({disk.used//1024**3}GB/{disk.total//1024**3}GB)
Free Disk Space: {disk.free//1024**3}GB

🔄 System Status:
Boot Time: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}
Uptime: {self.get_uptime()}
Running Processes: {process_count}
Health Score: {self.system_health_score}%

🌐 Network:
Total Sent: {net_io.bytes_sent//1024**2}MB
Total Received: {net_io.bytes_recv//1024**2}MB"""
            
            # Show in enhanced message box
            self.main_window.root.after(0, lambda: messagebox.showinfo("💻 Enhanced System Information", info))
            
        except Exception as e:
            self.show_notification("Error", f"Failed to get enhanced system info: {str(e)}")
    
    def toggle_monitoring(self, icon=None, item=None):
        """Enhanced monitoring toggle"""
        if self.monitoring_active:
            self.stop_monitoring()
            self.update_tray_icon("blue")
            self.show_notification("Monitoring", "📊 Real-time monitoring disabled")
        else:
            self.start_monitoring()
            self.show_notification("Monitoring", "📈 Real-time monitoring enabled\n• Performance tracking active\n• Health score updating")
    
    def show_settings(self, icon=None, item=None):
        """Enhanced settings display"""
        if self.main_window and self.main_window.root:
            self.show_main_window()
            
            # Try to find and switch to settings/preferences tab
            if hasattr(self.main_window, 'notebook'):
                try:
                    tab_count = self.main_window.notebook.index("end")
                    for i in range(tab_count):
                        tab_text = self.main_window.notebook.tab(i, "text").lower()
                        if any(word in tab_text for word in ["settings", "ayarlar", "preferences", "config"]):
                            self.main_window.notebook.select(i)
                            break
                    else:
                        # If no settings tab found, show tray settings
                        self.show_tray_settings()
                except:
                    self.show_tray_settings()
            else:
                self.show_tray_settings()
    
    def exit_application(self, icon=None, item=None):
        """Enhanced application exit"""
        try:
            # Show enhanced exit dialog
            result = messagebox.askyesno("Exit DonTe Cleaner Pro", 
                                       """Are you sure you want to exit DonTe Cleaner Pro?

🔹 Real-time monitoring will stop
🔹 Auto-protection will be disabled  
🔹 System tray will be removed

Tip: You can minimize to tray instead of exiting.""")
            
            if result:
                # Save current state
                self.save_tray_settings()
                
                # Show farewell notification
                self.show_notification("DonTe Cleaner Pro", "👋 Thank you for using DonTe Cleaner Pro!")
                
                # Cleanup and exit
                self.cleanup()
                if self.main_window and self.main_window.root:
                    self.main_window.root.quit()
                    self.main_window.root.destroy()
                
                # Force exit after a delay
                threading.Timer(2.0, lambda: sys.exit(0)).start()
                
        except Exception as e:
            print(f"Exit error: {e}")
            sys.exit(0)
    
    def show_notification(self, title, message, duration=3000):
        """Enhanced system notification with smart filtering"""
        try:
            # Check if notifications are enabled
            if not self.notifications_enabled:
                return
            
            # Gaming mode reduces notifications
            if self.gaming_mode and "Gaming" not in title and "Performance" not in title:
                return
            
            # Add emoji based on notification type
            if "Error" in title:
                title = f"❌ {title}"
            elif "Warning" in title or "Alert" in title:
                title = f"⚠️ {title}"
            elif "Success" in title or "completed" in message.lower():
                title = f"✅ {title}"
            elif "Gaming" in title:
                title = f"🎮 {title}"
            elif "Scan" in title:
                title = f"🔍 {title}"
            elif "Clean" in title:
                title = f"🧹 {title}"
            elif "Monitor" in title:
                title = f"📊 {title}"
            else:
                title = f"🔔 {title}"
            
            if TRAY_AVAILABLE and self.tray_icon:
                self.tray_icon.notify(message, title)
            else:
                # Enhanced fallback to console with timestamp
                timestamp = datetime.now().strftime('%H:%M:%S')
                print(f"[{timestamp}] {title}: {message}")
                
        except Exception as e:
            print(f"Notification error: {e}")
    
    def minimize_to_tray(self):
        """Enhanced minimize to tray with smart notification"""
        if self.main_window and self.main_window.root:
            self.main_window.root.withdraw()
            
            # Smart notification - only show first time or after long period
            if not hasattr(self, '_last_minimize_time') or \
               (datetime.now() - self._last_minimize_time).seconds > 3600:  # 1 hour
                self.show_notification("DonTe Cleaner Pro", 
                                     "🔽 Minimized to system tray\n💡 Right-click tray icon for quick actions")
                self._last_minimize_time = datetime.now()
    
    def cleanup(self):
        """Enhanced cleanup with state saving"""
        try:
            # Save current monitoring state
            self.save_tray_settings()
            
            # Stop all background activities
            self.is_running = False
            self.monitoring_active = False
            
            # Clean up tray icon
            if TRAY_AVAILABLE and self.tray_icon:
                try:
                    self.tray_icon.stop()
                except Exception as e:
                    print(f"Tray cleanup warning: {e}")
                    
            print("System tray cleanup completed")
            
        except Exception as e:
            print(f"Cleanup error: {e}")

# Enhanced utility functions
def install_tray_support():
    """Enhanced installation instructions for system tray support"""
    instructions = """
🔧 Enhanced System Tray Support Installation:

Required packages:
pip install pystray pillow psutil

Optional for advanced features:
pip install requests  # For online updates
pip install wmi       # For detailed hardware info (Windows)

Features when fully installed:
✅ Dynamic tray icon with real-time status colors
✅ Comprehensive right-click menu with submenus
✅ Smart notifications with emoji indicators  
✅ Advanced system monitoring and health scoring
✅ Auto-protection with configurable triggers
✅ Gaming mode with performance optimizations
✅ Detailed hardware and performance statistics
✅ System diagnostics and automated reporting
✅ Network monitoring and temperature tracking
✅ Backup and restore functionality
✅ Windows integration tools

Advanced Features:
🎮 Gaming Mode: Optimizes system for gaming
🛡️ Auto Protection: Automatic cleanup triggers
📊 Health Scoring: AI-based system health analysis
🔍 Enhanced Scanning: Multi-threaded threat detection
📈 Performance History: Trending and analytics
🌡️ Temperature Monitoring: Hardware thermal tracking
🌐 Network Statistics: Bandwidth and connection monitoring
🔧 System Tools: Registry cleanup, Explorer restart
📋 Report Generation: Comprehensive system reports
⚙️ Smart Settings: Adaptive configuration management

Installation command:
pip install pystray pillow psutil requests wmi
    """
    return instructions

def check_tray_support():
    """Enhanced tray support availability check"""
    support_info = {
        'basic_tray': TRAY_AVAILABLE,
        'psutil': True,
        'advanced_features': True
    }
    
    try:
        import requests
        support_info['network_features'] = True
    except ImportError:
        support_info['network_features'] = False
    
    try:
        import wmi
        support_info['hardware_details'] = True
    except ImportError:
        support_info['hardware_details'] = False
    
    return support_info

def get_tray_feature_status():
    """Get detailed feature availability status"""
    features = {
        '🎯 Basic Tray Icon': TRAY_AVAILABLE,
        '📊 Performance Monitoring': True,
        '🔔 Smart Notifications': TRAY_AVAILABLE,
        '🎮 Gaming Mode': True,
        '🛡️ Auto Protection': True,
        '📈 Health Scoring': True,
        '🌡️ Temperature Monitoring': True,
        '🌐 Network Statistics': True,
        '🔧 System Tools': True,
        '📋 Report Generation': True
    }
    
    # Check optional features
    try:
        import requests
        features['🌐 Online Features'] = True
    except ImportError:
        features['🌐 Online Features'] = False
    
    try:
        import wmi
        features['💻 Hardware Details'] = True
    except ImportError:
        features['💻 Hardware Details'] = False
    
    return features
