"""
Data Integrity and System Diagnostics Service.
Audits datasets for anomalies and verifies system prerequisites on startup.
"""
from typing import Dict, Any
from storage.base_storage import BaseStorage
from config import (
    ADMINS_JSON_FILE,
    SUBJECTS_JSON_FILE,
    ACTIVITY_LOG_FILE,
    DATA_STORAGE_FORMAT
)

class IntegrityService:
    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def perform_system_health_check(self) -> Dict[str, Any]:
        report = {
            "status": "HEALTHY",
            "storage_format": DATA_STORAGE_FORMAT,
            "checks": {},
            "issues": []
        }

        report["checks"]["admins_file"] = ADMINS_JSON_FILE.exists()
        report["checks"]["subjects_file"] = SUBJECTS_JSON_FILE.exists()
        report["checks"]["activity_log"] = ACTIVITY_LOG_FILE.exists()

        try:
            students = self.storage.load_students()
            report["checks"]["storage_accessible"] = True
            report["student_count"] = len(students)
        except Exception as e:
            report["checks"]["storage_accessible"] = False
            report["status"] = "CRITICAL"
            report["issues"].append(f"Storage access failure: {e}")
            return report

        seen_ids = set()
        duplicate_ids = []
        invalid_marks = []
        invalid_attendance = []

        for s in students:
            if s.student_id in seen_ids:
                duplicate_ids.append(s.student_id)
            seen_ids.add(s.student_id)

            if s.classes_attended > s.total_classes or s.classes_attended < 0:
                invalid_attendance.append(s.student_id)

            for subj, mark in s.marks.items():
                if mark < 0 or mark > 100:
                    invalid_marks.append(f"{s.student_id} ({subj}={mark})")

        report["checks"]["no_duplicate_ids"] = len(duplicate_ids) == 0
        report["checks"]["valid_attendance"] = len(invalid_attendance) == 0
        report["checks"]["valid_marks"] = len(invalid_marks) == 0

        if duplicate_ids:
            report["status"] = "WARNING"
            report["issues"].append(f"Duplicate IDs detected: {', '.join(duplicate_ids)}")
        if invalid_attendance:
            report["status"] = "WARNING"
            report["issues"].append(f"Invalid attendance in IDs: {', '.join(invalid_attendance)}")
        if invalid_marks:
            report["status"] = "WARNING"
            report["issues"].append(f"Invalid marks in: {', '.join(invalid_marks)}")

        return report