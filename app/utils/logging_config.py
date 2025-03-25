import logging
import sys
import psutil
from pathlib import Path
from pythonjsonlogger import jsonlogger
from datetime import datetime
from typing import Dict, Any

# Create logs directory if it doesn't exist
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# Configure JSON formatter
class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record: Dict[str, Any], record: logging.LogRecord, message_dict: Dict[str, Any]) -> None:
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['timestamp'] = datetime.utcnow().isoformat()
        log_record['level'] = record.levelname
        log_record['module'] = record.module

def get_system_metrics() -> Dict[str, float]:
    """Get current system resource usage metrics."""
    return {
        'cpu_percent': psutil.cpu_percent(),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_usage_percent': psutil.disk_usage('/').percent
    }

def setup_logging():
    """Configure application logging."""
    # Create logger
    logger = logging.getLogger("credit_report_api")
    logger.setLevel(logging.INFO)

    # Create handlers
    console_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler(LOGS_DIR / "api.log")
    
    # Create formatter
    formatter = CustomJsonFormatter(
        '%(timestamp)s %(level)s %(name)s %(module)s %(message)s'
    )

    # Set formatter for handlers
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# Create monitoring logger
def setup_monitoring_logger():
    """Configure system monitoring logging."""
    logger = logging.getLogger("monitoring")
    logger.setLevel(logging.INFO)

    # Create handler for monitoring logs
    file_handler = logging.FileHandler(LOGS_DIR / "monitoring.log")
    
    # Create formatter
    formatter = CustomJsonFormatter(
        '%(timestamp)s %(level)s %(name)s %(message)s'
    )

    # Set formatter for handler
    file_handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(file_handler)

    return logger

# Initialize loggers
api_logger = setup_logging()
monitoring_logger = setup_monitoring_logger()

def log_system_metrics():
    """Log current system metrics."""
    metrics = get_system_metrics()
    monitoring_logger.info("System metrics", extra=metrics)
