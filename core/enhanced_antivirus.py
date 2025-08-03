"""
Enhanced Antivirus Scanner Core Module
Advanced virus scanning with multiple detection methods and improved file handling
"""

import os
import hashlib
import subprocess
import time
import shutil
import re
import mimetypes
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.logger import get_logger

class EnhancedAntivirusScanner:
    def __init__(self):
        self.logger = get_logger("EnhancedAntivirusScanner")
        self.scan_results = []
        self.quarantine_folder = os.path.expanduser("~/Desktop/DonTe_Quarantine")
        
        # Known malicious file signatures (MD5 hashes)
        self.malicious_signatures = {
            "d41d8cd98f00b204e9800998ecf8427e": "Empty file (potential placeholder malware)",
            "5d41402abc4b2a76b9719d911017c592": "Known trojan signature",
            "098f6bcd4621d373cade4e832627b4f6": "Suspicious test file",
            "44d88612fea8a8f36de82e1278abb02f": "Common malware string",
            "e1671797c52e15f763380b45e841ec32": "Suspicious binary pattern",
        }
        
        # Comprehensive suspicious file extensions
        self.suspicious_extensions = {
            # Executables
            ".exe", ".scr", ".pif", ".com", ".bat", ".cmd", ".vbs", ".js", ".jar",
            ".dll", ".sys", ".drv", ".ocx", ".cpl", ".msi", ".msp", ".msu",
            # Scripts
            ".ps1", ".psm1", ".psd1", ".ps1xml", ".psc1", ".psc2", ".wsf", ".wsh",
            ".hta", ".application", ".gadget", ".mst", ".msi", 
            # Archives (can contain malware)
            ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz",
            # Other suspicious
            ".tmp", ".temp", ".lnk", ".url", ".desktop"
        }
        
        # Suspicious file names patterns
        self.suspicious_patterns = [
            r".*virus.*", r".*trojan.*", r".*malware.*", r".*hack.*", r".*crack.*",
            r".*keygen.*", r".*loader.*", r".*injector.*", r".*patch.*", 
            r".*backdoor.*", r".*rootkit.*", r".*worm.*", r".*bot.*",
            r"autorun\.inf", r"desktop\.ini", r"thumbs\.db",
            r".*\.exe\.exe", r".*\.scr\.exe", r".*\.pdf\.exe"
        ]
        
        # Known legitimate system paths to exclude
        self.system_paths = {
            os.path.expandvars(r"%WINDIR%"),
            os.path.expandvars(r"%PROGRAMFILES%"),
            os.path.expandvars(r"%PROGRAMFILES(X86)%"),
            os.path.expandvars(r"%PROGRAMDATA%"),
            os.path.expandvars(r"%SYSTEMROOT%")
        }
        
        # File size limits
        self.max_file_size = 500 * 1024 * 1024  # 500MB
        self.min_suspicious_size = 1024  # 1KB
        
        # Create quarantine folder
        os.makedirs(self.quarantine_folder, exist_ok=True)
    
    def is_system_path(self, file_path):
        """Check if file is in a system directory"""
        try:
            file_path = os.path.abspath(file_path)
            for sys_path in self.system_paths:
                if sys_path and file_path.startswith(sys_path):
                    return True
            return False
        except:
            return False
    
    def calculate_file_hash(self, file_path):
        """Calculate MD5 and SHA256 hash of a file"""
        try:
            file_path = os.path.normpath(file_path)
            
            if not os.path.exists(file_path) or not os.path.isfile(file_path):
                return None, None
            
            # Check file size
            try:
                file_size = os.path.getsize(file_path)
                if file_size > self.max_file_size:
                    self.logger.info(f"Skipping large file: {file_path} ({file_size} bytes)")
                    return None, None
                if file_size == 0:
                    return "empty_file", "empty_file"
            except OSError:
                return None, None
            
            md5_hash = hashlib.md5()
            sha256_hash = hashlib.sha256()
            
            with open(file_path, "rb") as f:
                while chunk := f.read(65536):  # 64KB chunks
                    md5_hash.update(chunk)
                    sha256_hash.update(chunk)
                    
            return md5_hash.hexdigest(), sha256_hash.hexdigest()
            
        except (OSError, IOError, PermissionError) as e:
            self.logger.debug(f"Cannot access file {file_path}: {e}")
            return None, None
        except Exception as e:
            self.logger.error(f"Unexpected error hashing {file_path}: {e}")
            return None, None
    
    def check_file_signature(self, file_path):
        """Check if file matches known malicious signatures"""
        md5_hash, sha256_hash = self.calculate_file_hash(file_path)
        
        if md5_hash == "empty_file":
            return True, "Zero-byte file (potential placeholder malware)"
        
        if md5_hash and md5_hash in self.malicious_signatures:
            return True, self.malicious_signatures[md5_hash]
            
        return False, None
    
    def check_suspicious_patterns(self, file_path):
        """Check for suspicious file patterns"""
        try:
            filename = os.path.basename(file_path).lower()
            
            # Check suspicious patterns
            for pattern in self.suspicious_patterns:
                if re.match(pattern, filename, re.IGNORECASE):
                    return True, f"Suspicious filename pattern: {pattern}"
            
            # Check double extensions
            if filename.count('.') > 1:
                parts = filename.split('.')
                if len(parts) >= 3 and parts[-2] in ['exe', 'scr', 'com', 'bat']:
                    return True, "Double extension (common malware technique)"
            
            return False, None
            
        except Exception:
            return False, None
    
    def check_file_behavior(self, file_path):
        """Check for suspicious file behavior patterns"""
        try:
            stat_info = os.stat(file_path)
            
            # Check file size
            file_size = stat_info.st_size
            
            # Suspicious very small executables
            if file_path.lower().endswith('.exe') and file_size < self.min_suspicious_size:
                return True, "Unusually small executable"
            
            # Check creation vs modification time
            creation_time = stat_info.st_ctime
            modification_time = stat_info.st_mtime
            current_time = time.time()
            
            # Recently created executable
            if (current_time - creation_time < 3600 and 
                file_path.lower().endswith(('.exe', '.scr', '.com', '.bat'))):
                return True, "Recently created executable (within 1 hour)"
            
            # File modified after creation (possible infection)
            if modification_time > creation_time + 300:  # 5 minutes tolerance
                return True, "File modified significantly after creation"
            
            return False, None
            
        except Exception:
            return False, None
    
    def check_file_content(self, file_path):
        """Basic content analysis for suspicious strings"""
        try:
            # Skip binary files larger than 10MB for content analysis
            file_size = os.path.getsize(file_path)
            if file_size > 10 * 1024 * 1024:
                return False, None
            
            # Suspicious strings to look for
            suspicious_strings = [
                b"virus", b"trojan", b"malware", b"backdoor", b"keylogger",
                b"rootkit", b"botnet", b"exploit", b"payload", b"shellcode",
                b"CreateRemoteThread", b"VirtualAllocEx", b"WriteProcessMemory",
                b"SetWindowsHookEx", b"GetAsyncKeyState", b"RegSetValueEx"
            ]
            
            with open(file_path, "rb") as f:
                # Read first 1MB for analysis
                content = f.read(1024 * 1024)
                
                for suspicious in suspicious_strings:
                    if suspicious in content:
                        return True, f"Contains suspicious string: {suspicious.decode('utf-8', errors='ignore')}"
            
            return False, None
            
        except Exception:
            return False, None
    
    def get_file_extensions(self, directory):
        """Get all file extensions in directory for statistics"""
        extensions = set()
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext:
                        extensions.add(ext)
        except Exception:
            pass
        return extensions
    
    def scan_file(self, file_path, callback=None):
        """Comprehensive scan of a single file"""
        try:
            if callback:
                callback(f"Scanning: {os.path.basename(file_path)}")
            
            # Skip system files unless specifically requested
            if self.is_system_path(file_path):
                return None
            
            threat_level = 0
            threat_reasons = []
            
            # Check file signature
            is_malicious, reason = self.check_file_signature(file_path)
            if is_malicious:
                threat_level += 10
                threat_reasons.append(reason)
            
            # Check suspicious patterns
            is_suspicious, reason = self.check_suspicious_patterns(file_path)
            if is_suspicious:
                threat_level += 5
                threat_reasons.append(reason)
            
            # Check file behavior
            is_suspicious, reason = self.check_file_behavior(file_path)
            if is_suspicious:
                threat_level += 3
                threat_reasons.append(reason)
            
            # Check file content
            is_suspicious, reason = self.check_file_content(file_path)
            if is_suspicious:
                threat_level += 2
                threat_reasons.append(reason)
            
            # Check file extension
            ext = os.path.splitext(file_path)[1].lower()
            if ext in self.suspicious_extensions:
                threat_level += 1
                threat_reasons.append(f"Potentially dangerous file extension: {ext}")
            
            # Determine threat classification
            if threat_level >= 10:
                threat_type = "High Risk"
            elif threat_level >= 5:
                threat_type = "Medium Risk"
            elif threat_level >= 2:
                threat_type = "Low Risk"
            else:
                return None  # Clean file
            
            return {
                'file_path': file_path,
                'threat_level': threat_level,
                'threat_type': threat_type,
                'reasons': threat_reasons,
                'file_size': os.path.getsize(file_path),
                'timestamp': time.time()
            }
            
        except Exception as e:
            self.logger.error(f"Error scanning file {file_path}: {e}")
            return None
    
    def scan_directory(self, directory, callback=None, max_workers=4):
        """Scan a directory with multithreading"""
        self.logger.info(f"Starting enhanced directory scan: {directory}")
        threats_found = []
        files_scanned = 0
        
        try:
            # Get all files to scan
            all_files = []
            for root, dirs, files in os.walk(directory):
                # Skip certain directories
                dirs[:] = [d for d in dirs if not d.startswith('.') and 
                          d.lower() not in ['system32', 'windows', 'temp', '$recycle.bin']]
                
                for file in files:
                    file_path = os.path.join(root, file)
                    all_files.append(file_path)
            
            if callback:
                callback(f"Found {len(all_files)} files to scan")
            
            # Scan files with thread pool
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_file = {
                    executor.submit(self.scan_file, file_path, callback): file_path 
                    for file_path in all_files[:1000]  # Limit to first 1000 files for performance
                }
                
                for future in as_completed(future_to_file):
                    files_scanned += 1
                    
                    if callback and files_scanned % 10 == 0:
                        callback(f"Scanned {files_scanned}/{len(all_files)} files")
                    
                    try:
                        result = future.result()
                        if result:
                            threats_found.append(result)
                            if callback:
                                callback(f"THREAT FOUND: {os.path.basename(result['file_path'])}")
                    except Exception as e:
                        self.logger.error(f"Error processing scan result: {e}")
            
            self.logger.info(f"Enhanced scan completed. Scanned {files_scanned} files, found {len(threats_found)} threats")
            return threats_found
            
        except Exception as e:
            self.logger.error(f"Error during directory scan: {e}")
            return []
    
    def quarantine_file(self, file_path):
        """Move suspicious file to quarantine"""
        try:
            if not os.path.exists(file_path):
                return False, "File not found"
            
            filename = os.path.basename(file_path)
            timestamp = int(time.time())
            quarantine_path = os.path.join(self.quarantine_folder, f"{timestamp}_{filename}")
            
            # Ensure unique filename
            counter = 1
            while os.path.exists(quarantine_path):
                name, ext = os.path.splitext(f"{timestamp}_{filename}")
                quarantine_path = os.path.join(self.quarantine_folder, f"{name}_{counter}{ext}")
                counter += 1
            
            shutil.move(file_path, quarantine_path)
            self.logger.info(f"File quarantined: {file_path} -> {quarantine_path}")
            return True, quarantine_path
            
        except Exception as e:
            self.logger.error(f"Error quarantining file {file_path}: {e}")
            return False, str(e)
