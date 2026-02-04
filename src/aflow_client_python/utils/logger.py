# Logger utilities

import logging
import os
from typing import Optional

# Default logger configuration
DEFAULT_LOG_LEVEL = logging.INFO #TODO: Change to INFO
DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Create logger cache
_loggers = {}


def get_logger(name: str = __name__, log_file: Optional[str] = None) -> logging.Logger:
    """
    Get a logger with the given name
    
    Args:
        name: Logger name
        log_file: Optional log file path
        
    Returns:
        Logger instance
    """
    if name in _loggers:
        return _loggers[name]

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(DEFAULT_LOG_LEVEL)

    # Check if logger already has handlers
    if not logger.handlers:
        # Create formatter
        formatter = logging.Formatter(DEFAULT_LOG_FORMAT)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Create file handler if log_file is provided
        if log_file:
            # Ensure directory exists
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)

            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    # Cache logger
    _loggers[name] = logger

    return logger


def set_log_level(level: int):
    """
    Set log level for all loggers
    
    Args:
        level: Log level
    """
    for logger in _loggers.values():
        logger.setLevel(level)
