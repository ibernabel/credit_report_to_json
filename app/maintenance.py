#!/usr/bin/env python3
import asyncio
import schedule
import time
from app.utils.backup import BackupManager
from app.utils.logging_config import api_logger

class MaintenanceScheduler:
    def __init__(self):
        self.backup_manager = BackupManager()

    def run_daily_maintenance(self):
        """Run daily maintenance tasks."""
        try:
            # Create backup
            self.backup_manager.create_backup()
            
            # Cleanup old backups (keep last 7 days)
            self.backup_manager.cleanup_old_backups(keep_days=7)
            
            # Rotate logs if needed
            self.backup_manager.rotate_logs(max_size_mb=100)
            
            api_logger.info("Daily maintenance tasks completed successfully")
            
        except Exception as e:
            api_logger.error(
                "Daily maintenance tasks failed",
                extra={'error': str(e)}
            )

def main():
    """Main function to schedule and run maintenance tasks."""
    scheduler = MaintenanceScheduler()
    
    # Schedule daily maintenance at 2 AM
    schedule.every().day.at("02:00").do(scheduler.run_daily_maintenance)
    
    # Log startup
    api_logger.info("Maintenance scheduler started")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
    except KeyboardInterrupt:
        api_logger.info("Maintenance scheduler stopped")
        
    except Exception as e:
        api_logger.error(
            "Maintenance scheduler error",
            extra={'error': str(e)}
        )
        raise

if __name__ == "__main__":
    main()
