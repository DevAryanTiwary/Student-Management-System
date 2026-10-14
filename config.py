"""
Central configuration settings for the Student Management System.
Extended for Professional Desktop GUI while preserving all original configurations.
"""
from pathlib import Path

# Base Paths (Preserved)
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
BACKUPS_DIR = BASE_DIR / "backups"
REPORTS_DIR = BASE_DIR / "reports" / "generated"

# Ensure runtime directories exist
for directory in [DATA_DIR, LOGS_DIR, BACKUPS_DIR, REPORTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Storage Configuration (Preserved)
# Options: "CSV" or "JSON"
DATA_STORAGE_FORMAT = "JSON"

STUDENTS_CSV_FILE = DATA_DIR / "students.csv"
STUDENTS_JSON_FILE = DATA_DIR / "students.json"
ADMINS_JSON_FILE = DATA_DIR / "admins.json"
SUBJECTS_JSON_FILE = DATA_DIR / "subjects.json"
ACTIVITY_LOG_FILE = LOGS_DIR / "activity.log"

# Academic & Grading Rules (Preserved)
MAX_MARKS_PER_SUBJECT = 100.0
MIN_MARKS_PER_SUBJECT = 0.0
PASSING_MARKS = 40.0
MIN_ATTENDANCE_PERCENT = 75.0

# Configurable Grade Scale: (min_percentage, grade_label) (Preserved)
GRADE_SCALE = [
    (90.0, "A+"),
    (80.0, "A"),
    (70.0, "B+"),
    (60.0, "B"),
    (50.0, "C"),
    (40.0, "D"),
    (0.0, "F"),
]

# Security Configuration (Preserved)
MAX_LOGIN_ATTEMPTS = 3
PASSWORD_SALT_BYTES = 16
PBKDF2_ITERATIONS = 100_000

# Default Initial Administrator (Preserved)
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "AdminPassword@123"

# Default Subjects (Preserved)
DEFAULT_SUBJECTS = ["Python", "DBMS", "Java", "Mathematics", "Computer Networks"]

# --- Extensions for Professional Edition ---
APP_VERSION = "2.0.0"
APP_NAME = "Student Management System — Professional Edition"

# Role Definitions
ROLE_SUPER_ADMIN = "Super Admin"
ROLE_ADMIN = "Administrator"
ROLE_TEACHER = "Teacher"
ROLE_VIEWER = "Viewer"

ALL_ROLES = [ROLE_SUPER_ADMIN, ROLE_ADMIN, ROLE_TEACHER, ROLE_VIEWER]

# Session Security
SESSION_TIMEOUT_MINUTES = 15

# Theme Preferences: "dark" or "light"
DEFAULT_THEME = "dark"

# Academic Terms & Sessions
CURRENT_ACADEMIC_YEAR = "2026-27"
CURRENT_SEMESTER = "Semester 1"