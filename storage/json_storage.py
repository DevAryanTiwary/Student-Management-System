"""
JSON Storage Provider using atomic writes to prevent corruption.
"""
import json
import os
import tempfile
from pathlib import Path
from typing import List, Optional
from storage.base_storage import BaseStorage
from models.student import Student
from utils.exceptions import StorageError

class JSONStorage(BaseStorage):
    def __init__(self, file_path: Path):
        self.file_path = Path(file_path)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            self._atomic_write([])

    def _atomic_write(self, data: list):
        dir_name = self.file_path.parent
        try:
            with tempfile.NamedTemporaryFile("w", dir=dir_name, delete=False, encoding="utf-8") as tf:
                json.dump(data, tf, indent=4)
                temp_name = tf.name
            os.replace(temp_name, self.file_path)
        except Exception as e:
            if 'temp_name' in locals() and os.path.exists(temp_name):
                os.remove(temp_name)
            raise StorageError(f"Failed to write JSON atomically: {e}")

    def load_students(self) -> List[Student]:
        try:
            if os.path.getsize(self.file_path) == 0:
                return []
            with open(self.file_path, "r", encoding="utf-8") as f:
                records = json.load(f)
            return [Student.from_dict(r) for r in records if r.get("is_active", True)]
        except json.JSONDecodeError as err:
            raise StorageError(f"Corrupt JSON file detected in {self.file_path}: {err}")
        except Exception as err:
            raise StorageError(f"Failed reading student records: {err}")

    def save_students(self, students: List[Student]) -> None:
        raw_data = [s.to_dict() for s in students]
        self._atomic_write(raw_data)

    def add_student(self, student: Student) -> None:
        all_students = self.load_students()
        all_students.append(student)
        self.save_students(all_students)

    def get_student(self, student_id: str) -> Optional[Student]:
        for s in self.load_students():
            if s.student_id.upper() == student_id.upper():
                return s
        return None

    def update_student(self, student: Student) -> None:
        students = self.load_students()
        updated = False
        for idx, s in enumerate(students):
            if s.student_id.upper() == student.student_id.upper():
                students[idx] = student
                updated = True
                break
        if not updated:
            raise StorageError(f"Student {student.student_id} not found to update.")
        self.save_students(students)

    def delete_student(self, student_id: str, soft_delete: bool = True) -> bool:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                raw_records = json.load(f)
        except Exception:
            raw_records = []

        found = False
        new_records = []
        for r in raw_records:
            if r.get("student_id", "").upper() == student_id.upper():
                found = True
                if soft_delete:
                    r["is_active"] = False
                    new_records.append(r)
            else:
                new_records.append(r)

        if found:
            self._atomic_write(new_records)
        return found