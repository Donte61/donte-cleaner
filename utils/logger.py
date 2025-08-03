"""
Logger utility for DonTe Cleaner
"""

import logging
import os
from datetime import datetime

def setup_logger():
    """Setup application logging"""
    # Create logs directory if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    # Create log filename with timestamp
    log_filename = f"logs/donte_cleaner_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger("DonTe Cleaner")
    logger.info("DonTe Cleaner başlatıldı")
    return logger

def get_logger(name=None):
    """Get a logger instance"""
    return logging.getLogger(name or "DonTe Cleaner")
