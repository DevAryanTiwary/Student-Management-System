"""
Backup and Restoration system with timestamped directories.
"""
import shutil
from datetime import datetime
from typing import List
from config import BACKUPS_DIR, DATA_DIR
from utils.exceptions import StorageError
from utils.logger import log_activity

class BackupManager:
    def __init__(self, admin_username: str = "Admin"):
        self.admin_username = admin_username

    def create_backup(self) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        target_dir = BACKUPS_DIR / f"backup_{timestamp}"
        try:
            target_dir.mkdir(parents=True, exist_ok=False)
            for item in DATA_DIR.glob("*.*"):
                if item.is_file():
                    shutil.copy2(item, target_dir / item.name)

            log_activity(self.admin_username, "CREATE_BACKUP", f"Created backup: {target_dir.name}")
            return target_dir.name
        except Exception as e:
            raise StorageError(f"Backup creation failed: {e}")

    def list_backups(self) -> List[str]:
        if not BACKUPS_DIR.exists():
            return []
        dirs = [d.name for d in BACKUPS_DIR.iterdir() if d.is_dir() and d.name.startswith("backup_")]
        return sorted(dirs, reverse=True)

    def restore_backup(self, backup_name: str) -> bool:
        target_dir = BACKUPS_DIR / backup_name
        if not target_dir.exists() or not target_dir.is_dir():
            raise StorageError(f"Backup folder '{backup_name}' does not exist.")

        try:
            for item in target_dir.glob("*.*"):
                if item.is_file():
                    shutil.copy2(item, DATA_DIR / item.name)

            log_activity(self.admin_username, "RESTORE_BACKUP", f"Restored backup from {backup_name}")
            return True
        except Exception as e:
            raise StorageError(f"Backup restoration failed: {e}")