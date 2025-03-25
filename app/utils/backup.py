import shutil
from pathlib import Path
from datetime import datetime
import tarfile
import os
from app.utils.logging_config import api_logger

class BackupManager:
    def __init__(self):
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)
        
        # Directories to backup
        self.dirs_to_backup = [
            Path("logs"),
            Path("credit_reports"),
            Path("output_text")
        ]

    def create_backup(self) -> Path:
        """
        Create a backup of important directories and files.
        
        Returns:
            Path: Path to the created backup file
        """
        try:
            # Create timestamp for backup name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{timestamp}.tar.gz"
            backup_path = self.backup_dir / backup_name

            # Create tar archive
            with tarfile.open(backup_path, "w:gz") as tar:
                # Add each directory to backup
                for dir_path in self.dirs_to_backup:
                    if dir_path.exists():
                        tar.add(dir_path, arcname=dir_path.name)

            # Log successful backup
            api_logger.info(
                "Backup created successfully",
                extra={
                    'backup_file': str(backup_path),
                    'size': os.path.getsize(backup_path)
                }
            )

            return backup_path

        except Exception as e:
            # Log backup failure
            api_logger.error(
                "Backup creation failed",
                extra={'error': str(e)}
            )
            raise

    def cleanup_old_backups(self, keep_days: int = 7):
        """
        Remove backups older than specified days.
        
        Args:
            keep_days (int): Number of days to keep backups for
        """
        try:
            current_time = datetime.now().timestamp()
            
            # Check each file in backup directory
            for backup_file in self.backup_dir.glob("backup_*.tar.gz"):
                file_age = current_time - os.path.getctime(backup_file)
                if file_age > (keep_days * 24 * 3600):  # Convert days to seconds
                    backup_file.unlink()
                    api_logger.info(
                        "Removed old backup file",
                        extra={'file': str(backup_file)}
                    )

        except Exception as e:
            api_logger.error(
                "Backup cleanup failed",
                extra={'error': str(e)}
            )
            raise

    def rotate_logs(self, max_size_mb: int = 100):
        """
        Rotate log files if they exceed maximum size.
        
        Args:
            max_size_mb (int): Maximum size of log files in megabytes
        """
        try:
            log_dir = Path("logs")
            if not log_dir.exists():
                return

            for log_file in log_dir.glob("*.log"):
                # Check if file exceeds max size
                if os.path.getsize(log_file) > (max_size_mb * 1024 * 1024):
                    # Create new filename with timestamp
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    new_name = log_file.with_name(f"{log_file.stem}_{timestamp}.log")
                    
                    # Rename current log file
                    shutil.move(log_file, new_name)
                    
                    # Create new empty log file
                    log_file.touch()
                    
                    api_logger.info(
                        "Log file rotated",
                        extra={
                            'old_file': str(log_file),
                            'new_file': str(new_name)
                        }
                    )

        except Exception as e:
            api_logger.error(
                "Log rotation failed",
                extra={'error': str(e)}
            )
            raise
