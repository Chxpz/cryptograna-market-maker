"""
Logging configuration for the market making bot.
"""
import os
import logging
from pythonjsonlogger import jsonlogger
from datetime import datetime

def setup_logger(name: str) -> logging.Logger:
    """
    Set up a logger with JSON formatting.
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))
        
        # Create console handler
        handler = logging.StreamHandler()
        
        # Create formatter
        formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Add formatter to handler
        handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(handler)
    
    return logger 