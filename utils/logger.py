"""
Centralized audit and application activity logger.
Writes structured audit events to file and provides formatted display hooks.
"""
import logging
from config import ACTIVITY_LOG_FILE

logger = logging.getLogger("SMS_Audit")
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler(ACTIVITY_LOG_FILE, encoding="utf-8")
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] [%(user)s] [%(action)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

def log_activity(username: str, action: str, description: str, student_id: str = "N/A") -> None:
    extra = {
        "user": username or "ANONYMOUS",
        "action": action
    }
    msg = f"StudentID: {student_id} | {description}"
    logger.info(msg, extra=extra)

def read_recent_logs(lines: int = 50) -> list[str]:
    if not ACTIVITY_LOG_FILE.exists():
        return []
    with open(ACTIVITY_LOG_FILE, "r", encoding="utf-8") as f:
        all_lines = f.readlines()
        return all_lines[-lines:]