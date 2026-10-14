"""
Academic Marks & Subject Configuration Manager.
"""
import json
from typing import List, Dict
from config import SUBJECTS_JSON_FILE, DEFAULT_SUBJECTS
from storage.base_storage import BaseStorage
from utils.exceptions import SubjectError, StudentNotFoundError
from utils.validators import validate_marks
from utils.logger import log_activity

class MarksManager:
    def __init__(self, storage: BaseStorage, admin_username: str = "Admin"):
        self.storage = storage
        self.admin_username = admin_username
        self._ensure_subjects_file()

    def _ensure_subjects_file(self):
        if not SUBJECTS_JSON_FILE.exists():
            SUBJECTS_JSON_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(SUBJECTS_JSON_FILE, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_SUBJECTS, f, indent=4)

    def get_configured_subjects(self) -> List[str]:
        try:
            with open(SUBJECTS_JSON_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_SUBJECTS

    def add_configured_subject(self, subject_name: str):
        sub = subject_name.strip()
        if not sub:
            raise SubjectError("Subject name cannot be empty.")
        subjects = self.get_configured_subjects()
        if sub.lower() in [s.lower() for s in subjects]:
            raise SubjectError(f"Subject '{sub}' already exists.")
        subjects.append(sub)
        with open(SUBJECTS_JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(subjects, f, indent=4)
        log_activity(self.admin_username, "ADD_SUBJECT", f"Added configurable subject: {sub}")

    def update_student_marks(self, student_id: str, subject_marks: Dict[str, float]):
        student = self.storage.get_student(student_id)
        if not student:
            raise StudentNotFoundError(f"Student {student_id} not found.")

        valid_subjects = [s.lower() for s in self.get_configured_subjects()]

        for sub, score in subject_marks.items():
            if sub.lower() not in valid_subjects:
                raise SubjectError(f"Subject '{sub}' is not configured in the system.")
            validated_score = validate_marks(score)
            student.marks[sub] = validated_score

        self.storage.update_student(student)
        log_activity(
            self.admin_username,
            "UPDATE_MARKS",
            f"Updated marks for subjects: {list(subject_marks.keys())}",
            student_id
        )