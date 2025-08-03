"""
Antivirus Scanner Core Module
Modern virus scanning with multiple detect                  return None
    
    def check_suspicious_behavior(self, file_path): Exception as e:
            self.logger.error(f"Unexpected error calculating hash for {file_path}: {e}")
            return None
    
    def check_suspicious_behavior(self, file_path):s
"""

import os
import hashlib
import requests
import json
import subprocess
import time
import shutil
from pathlib import Path
from utils.logger import get_logger

class AntivirusScanner:
    def __init__(self):
        self.logger = get_logger("AntivirusScanner")
        self.scan_results = []
        self.quarantine_folder = os.path.expanduser("~/Desktop/DonTe_Quarantine")
        
        # Known malicious file signatures (MD5 hashes)
        self.malicious_signatures = {
            "d41d8cd98f00b204e9800998ecf8427e": "Empty file (potential placeholder malware)",
            "5d41402abc4b2a76b9719d911017c592": "Known trojan signature",
            "098f6bcd4621d373cade4e832627b4f6": "Suspicious test file",
            # Add more known malicious signatures here
        }
        
        # Suspicious file extensions
        self.suspicious_extensions = [
            ".exe", ".scr", ".pif", ".com", ".bat", ".cmd", ".vbs", ".js",
            ".jar", ".dll", ".sys", ".drv", ".tmp", ".temp"
        ]
        
        # Suspicious file names
        self.suspicious_names = [
            "autorun.inf", "desktop.ini", "thumbs.db", "virus", "trojan",
            "malware", "hack", "crack", "keygen", "loader", "injector"
        ]
        
        # Create quarantine folder
        os.makedirs(self.quarantine_folder, exist_ok=True)
    
    def calculate_file_hash(self, file_path):
        """Calculate MD5 hash of a file"""
        try:
            # Normalize path separators
            file_path = os.path.normpath(file_path)
            
            # Check if file exists and is accessible
            if not os.path.exists(file_path):
                return None
                
            if not os.path.isfile(file_path):
                return None
            
            # Skip very large files (>100MB) for performance
            try:
                file_size = os.path.getsize(file_path)
                if file_size > 100 * 1024 * 1024:  # 100MB
                    self.logger.info(f"Skipping large file: {file_path} ({file_size} bytes)")
                    return None
            except OSError:
                return None
            
            hash_md5 = hashlib.md5()
            
            with open(file_path, "rb") as f:
                # Read in chunks to handle large files efficiently
                while chunk := f.read(8192):
                    hash_md5.update(chunk)
                    
            return hash_md5.hexdigest()
            
        except (OSError, IOError, PermissionError) as e:
            self.logger.error(f"Error calculating hash for {file_path}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error calculating hash for {file_path}: {e}")
            return None
    
    def check_file_signature(self, file_path):
        """Check if file matches known malicious signatures"""
        file_hash = self.calculate_file_hash(file_path)
        if file_hash and file_hash in self.malicious_signatures:
            return True, self.malicious_signatures[file_hash]
        return False, None
    
    def check_suspicious_patterns(self, file_path):
        """Check for suspicious file patterns"""
        file_name = os.path.basename(file_path).lower()
        file_ext = os.path.splitext(file_name)[1].lower()
        
        # Check suspicious extensions
        if file_ext in self.suspicious_extensions:
            # Additional checks for executable files
            if file_ext in [".exe", ".scr", ".com", ".pif"]:
                return self.analyze_executable(file_path)
        
        # Check suspicious names
        for suspicious_name in self.suspicious_names:
            if suspicious_name in file_name:
                return True, f"Suspicious file name pattern: {suspicious_name}"
        
        return False, None
    
    def analyze_executable(self, file_path):
        """Analyze executable files for suspicious behavior"""
        try:
            file_size = os.path.getsize(file_path)
            
            # Very small or very large executables can be suspicious
            if file_size < 1024:  # Less than 1KB
                return True, "Unusually small executable file"
            elif file_size > 100 * 1024 * 1024:  # Larger than 100MB
                return True, "Unusually large executable file"
            
            # Check file creation time
            creation_time = os.path.getctime(file_path)
            current_time = time.time()
            
            # Files created very recently might be suspicious
            if current_time - creation_time < 3600:  # Created in last hour
                return True, "Recently created executable (potential malware)"
            
            # Check for hidden attributes
            if os.name == 'nt':  # Windows
                import stat
                if os.stat(file_path).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN:
                    return True, "Hidden executable file"
            
            return False, None
        except Exception as e:
            self.logger.error(f"Error analyzing executable {file_path}: {str(e)}")
            return False, None
    
    def scan_directory(self, directory_path, callback=None):
        """Scan a directory for malicious files"""
        scan_results = []
        scanned_files = 0
        total_files = sum([len(files) for r, d, files in os.walk(directory_path)])
        
        self.logger.info(f"Starting directory scan: {directory_path}")
        
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                scanned_files += 1
                
                if callback:
                    progress = (scanned_files / total_files) * 100
                    callback(progress, f"Taranıyor: {file}")
                
                try:
                    # Check file signature
                    is_malicious, reason = self.check_file_signature(file_path)
                    if is_malicious:
                        scan_results.append({
                            'path': file_path,
                            'threat_type': 'Known Malware',
                            'description': reason,
                            'severity': 'High'
                        })
                        continue
                    
                    # Check suspicious patterns
                    is_suspicious, reason = self.check_suspicious_patterns(file_path)
                    if is_suspicious:
                        scan_results.append({
                            'path': file_path,
                            'threat_type': 'Suspicious File',
                            'description': reason,
                            'severity': 'Medium'
                        })
                
                except Exception as e:
                    self.logger.error(f"Error scanning file {file_path}: {str(e)}")
        
        self.scan_results.extend(scan_results)
        self.logger.info(f"Directory scan completed. Found {len(scan_results)} threats")
        return scan_results
    
    def quick_scan(self, callback=None):
        """Perform a quick system scan"""
        quick_scan_paths = [
            os.path.expanduser("~/Desktop"),
            os.path.expanduser("~/Downloads"),
            os.path.expanduser("~/Documents"),
            os.path.expanduser("~/AppData/Local/Temp"),
            "C:/Windows/Temp",
            "C:/Temp"
        ]
        
        all_results = []
        for i, path in enumerate(quick_scan_paths):
            if os.path.exists(path):
                if callback:
                    callback((i / len(quick_scan_paths)) * 100, f"Taranıyor: {path}")
                results = self.scan_directory(path)
                all_results.extend(results)
        
        return all_results
    
    def full_scan(self, callback=None):
        """Perform a full system scan"""
        drives = []
        if os.name == 'nt':  # Windows
            import string
            for letter in string.ascii_uppercase:
                if os.path.exists(f"{letter}:\\"):
                    drives.append(f"{letter}:\\")
        else:
            drives = ["/"]
        
        all_results = []
        for i, drive in enumerate(drives):
            if callback:
                callback((i / len(drives)) * 100, f"Taranıyor: {drive}")
            try:
                results = self.scan_directory(drive)
                all_results.extend(results)
            except Exception as e:
                self.logger.error(f"Error scanning drive {drive}: {str(e)}")
        
        return all_results
    
    def quarantine_file(self, file_path):
        """Move suspicious file to quarantine"""
        try:
            file_name = os.path.basename(file_path)
            quarantine_path = os.path.join(self.quarantine_folder, file_name)
            
            # If file already exists in quarantine, add timestamp
            if os.path.exists(quarantine_path):
                timestamp = int(time.time())
                name, ext = os.path.splitext(file_name)
                quarantine_path = os.path.join(self.quarantine_folder, f"{name}_{timestamp}{ext}")
            
            # Move file to quarantine
            shutil.move(file_path, quarantine_path)
            self.logger.info(f"File quarantined: {file_path} -> {quarantine_path}")
            return True, quarantine_path
        except Exception as e:
            self.logger.error(f"Error quarantining file {file_path}: {str(e)}")
            return False, str(e)
    
    def delete_file(self, file_path):
        """Permanently delete a file"""
        try:
            os.remove(file_path)
            self.logger.info(f"File deleted: {file_path}")
            return True, "File deleted successfully"
        except Exception as e:
            self.logger.error(f"Error deleting file {file_path}: {str(e)}")
            return False, str(e)
    
    def restore_from_quarantine(self, quarantine_path, original_path):
        """Restore a file from quarantine"""
        try:
            shutil.move(quarantine_path, original_path)
            self.logger.info(f"File restored: {quarantine_path} -> {original_path}")
            return True, "File restored successfully"
        except Exception as e:
            self.logger.error(f"Error restoring file {quarantine_path}: {str(e)}")
            return False, str(e)
    
    def get_scan_report(self):
        """Generate a detailed scan report"""
        report = {
            'scan_date': time.strftime("%Y-%m-%d %H:%M:%S"),
            'total_threats': len(self.scan_results),
            'high_severity': len([r for r in self.scan_results if r['severity'] == 'High']),
            'medium_severity': len([r for r in self.scan_results if r['severity'] == 'Medium']),
            'low_severity': len([r for r in self.scan_results if r['severity'] == 'Low']),
            'threats': self.scan_results
        }
        return report
    
    def save_report(self, report, file_path):
        """Save scan report to file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            self.logger.error(f"Error saving report: {str(e)}")
            return False
