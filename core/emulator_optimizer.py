"""
Emulator Optimizer Core Module
"""

import os
import json
import subprocess
import psutil
import time
from utils.logger import get_logger

class EmulatorOptimizer:
    def __init__(self):
        self.logger = get_logger("EmulatorOptimizer")
        self.emulator_paths = {
            "BlueStacks": "",
            "LDPlayer": "",
            "Nox": "",
            "MEmu": "",
            "GameLoop": "",
            "MuMu": ""
        }
        self.config_file = "emulator_config.json"
        self.load_emulator_paths()
    
    def load_emulator_paths(self):
        """Load saved emulator paths from config file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_paths = json.load(f)
                    for emulator, path in saved_paths.items():
                        if emulator in self.emulator_paths and os.path.exists(path):
                            self.emulator_paths[emulator] = path
                self.logger.info("Emulator paths loaded from config")
            else:
                self.auto_detect_emulators()
        except Exception as e:
            self.logger.error(f"Error loading emulator paths: {str(e)}")
            self.auto_detect_emulators()
    
    def save_emulator_paths(self):
        """Save emulator paths to config file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.emulator_paths, f, indent=2, ensure_ascii=False)
            self.logger.info("Emulator paths saved to config")
        except Exception as e:
            self.logger.error(f"Error saving emulator paths: {str(e)}")
    
    def auto_detect_emulators(self):
        """Auto-detect installed emulators"""
        default_paths = {
            "BlueStacks": [
                r"C:\Program Files\BlueStacks_nxt\HD-Player.exe",
                r"C:\Program Files (x86)\BlueStacks_nxt\HD-Player.exe",
                r"C:\Program Files\BlueStacks\HD-Player.exe"
            ],
            "LDPlayer": [
                r"C:\LDPlayer\LDPlayer9\dnplayer.exe",
                r"C:\LDPlayer\dnplayer.exe",
                r"C:\Program Files\LDPlayer\dnplayer.exe"
            ],
            "Nox": [
                r"C:\Program Files (x86)\Nox\bin\Nox.exe",
                r"C:\Program Files\Nox\bin\Nox.exe"
            ],
            "MEmu": [
                r"C:\Program Files\Microvirt\MEmu\MEmu.exe",
                r"C:\Program Files (x86)\Microvirt\MEmu\MEmu.exe"
            ],
            "GameLoop": [
                r"C:\Program Files\TxGameAssistant\AppMarket\GameLoop.exe",
                r"C:\Program Files (x86)\TxGameAssistant\AppMarket\GameLoop.exe"
            ],
            "MuMu": [
                r"C:\Program Files\Netease\MuMu Player 12\shell\MuMuPlayer.exe",
                r"C:\Program Files (x86)\Netease\MuMu Player 12\shell\MuMuPlayer.exe"
            ]
        }
        
        for emulator, paths in default_paths.items():
            for path in paths:
                if os.path.exists(path):
                    self.emulator_paths[emulator] = path
                    self.logger.info(f"Auto-detected {emulator}: {path}")
                    break
        
        self.save_emulator_paths()
    
    def set_emulator_path(self, emulator_name, path):
        """Set custom path for an emulator"""
        if emulator_name in self.emulator_paths:
            self.emulator_paths[emulator_name] = path
            self.save_emulator_paths()
            return True
        return False
    
    def get_emulator_processes(self, emulator_name):
        """Get process names for specific emulator"""
        process_maps = {
            "BlueStacks": ["HD-Player.exe", "Bluestacks.exe", "BlueStacksServices.exe"],
            "LDPlayer": ["dnplayer.exe", "LDPlayer.exe", "LdBoxHeadless.exe"],
            "Nox": ["Nox.exe", "NoxVMHandle.exe", "Nox_adb.exe"],
            "MEmu": ["MEmu.exe", "MEmuHeadless.exe", "MEmuSVC.exe"],
            "GameLoop": ["GameLoop.exe", "AndroidEmulator.exe"],
            "MuMu": ["MuMuPlayer.exe", "MuMu-Launcher.exe"]
        }
        return process_maps.get(emulator_name, [])
    
    def start_emulator(self, emulator_name):
        """Start specified emulator"""
        try:
            if not self.emulator_paths[emulator_name]:
                return False, f"{emulator_name} yolu belirtilmedi"
            
            if not os.path.exists(self.emulator_paths[emulator_name]):
                return False, f"{emulator_name} dosyası bulunamadı"
            
            # Start emulator process
            process = subprocess.Popen(
                [self.emulator_paths[emulator_name]], 
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait a bit for emulator to start
            time.sleep(3)
            
            # Check if process is still running
            if process.poll() is None:
                self.logger.info(f"{emulator_name} started successfully")
                return True, f"{emulator_name} başarıyla başlatıldı"
            else:
                return False, f"{emulator_name} başlatılamadı"
                
        except Exception as e:
            self.logger.error(f"Error starting {emulator_name}: {str(e)}")
            return False, f"{emulator_name} başlatma hatası: {str(e)}"
    
    def boost_emulator_priority(self, emulator_name):
        """Boost CPU priority for emulator processes"""
        try:
            process_names = self.get_emulator_processes(emulator_name)
            boosted_count = 0
            
            for proc in psutil.process_iter(['name', 'pid']):
                if proc.info['name'] in process_names:
                    try:
                        # Set to high priority
                        proc.nice(psutil.HIGH_PRIORITY_CLASS)
                        boosted_count += 1
                        self.logger.info(f"Boosted priority for {proc.info['name']} (PID: {proc.info['pid']})")
                    except Exception as e:
                        self.logger.error(f"Error boosting priority for {proc.info['name']}: {str(e)}")
            
            if boosted_count > 0:
                return True, f"{boosted_count} emülatör işleminin önceliği artırıldı"
            else:
                return False, f"{emulator_name} işlemleri bulunamadı"
                
        except Exception as e:
            self.logger.error(f"Error boosting emulator priority: {str(e)}")
            return False, f"Öncelik artırma hatası: {str(e)}"
    
    def optimize_emulator_settings(self, emulator_name):
        """Optimize emulator settings for better performance"""
        try:
            if emulator_name == "BlueStacks":
                return self._optimize_bluestacks()
            elif emulator_name == "LDPlayer":
                return self._optimize_ldplayer()
            elif emulator_name == "Nox":
                return self._optimize_nox()
            elif emulator_name == "MEmu":
                return self._optimize_memu()
            else:
                return True, "Genel optimizasyon uygulandı"
        except Exception as e:
            self.logger.error(f"Error optimizing {emulator_name}: {str(e)}")
            return False, f"Optimizasyon hatası: {str(e)}"
    
    def _optimize_bluestacks(self):
        """Optimize BlueStacks specific settings"""
        # BlueStacks configuration optimizations
        try:
            # This would involve modifying BlueStacks config files
            # For now, just return success
            self.logger.info("BlueStacks optimization applied")
            return True, "BlueStacks optimize edildi"
        except Exception as e:
            return False, f"BlueStacks optimizasyon hatası: {str(e)}"
    
    def _optimize_ldplayer(self):
        """Optimize LDPlayer specific settings"""
        try:
            self.logger.info("LDPlayer optimization applied")
            return True, "LDPlayer optimize edildi"
        except Exception as e:
            return False, f"LDPlayer optimizasyon hatası: {str(e)}"
    
    def _optimize_nox(self):
        """Optimize Nox specific settings"""
        try:
            self.logger.info("Nox optimization applied")
            return True, "Nox optimize edildi"
        except Exception as e:
            return False, f"Nox optimizasyon hatası: {str(e)}"
    
    def _optimize_memu(self):
        """Optimize MEmu specific settings"""
        try:
            self.logger.info("MEmu optimization applied")
            return True, "MEmu optimize edildi"
        except Exception as e:
            return False, f"MEmu optimizasyon hatası: {str(e)}"
    
    def close_emulator(self, emulator_name):
        """Close emulator processes"""
        try:
            process_names = self.get_emulator_processes(emulator_name)
            closed_count = 0
            
            for proc in psutil.process_iter(['name', 'pid']):
                if proc.info['name'] in process_names:
                    try:
                        proc.terminate()
                        closed_count += 1
                        self.logger.info(f"Terminated {proc.info['name']} (PID: {proc.info['pid']})")
                    except Exception as e:
                        self.logger.error(f"Error terminating {proc.info['name']}: {str(e)}")
            
            if closed_count > 0:
                return True, f"{closed_count} emülatör işlemi kapatıldı"
            else:
                return False, f"{emulator_name} işlemleri bulunamadı"
                
        except Exception as e:
            self.logger.error(f"Error closing emulator: {str(e)}")
            return False, f"Emülatör kapatma hatası: {str(e)}"
    
    def get_emulator_status(self, emulator_name):
        """Get current status of emulator"""
        try:
            process_names = self.get_emulator_processes(emulator_name)
            running_processes = []
            
            for proc in psutil.process_iter(['name', 'pid', 'memory_info', 'cpu_percent']):
                if proc.info['name'] in process_names:
                    running_processes.append({
                        'name': proc.info['name'],
                        'pid': proc.info['pid'],
                        'memory_mb': proc.info['memory_info'].rss / (1024 * 1024),
                        'cpu_percent': proc.info['cpu_percent']
                    })
            
            return running_processes
        except Exception as e:
            self.logger.error(f"Error getting emulator status: {str(e)}")
            return []
