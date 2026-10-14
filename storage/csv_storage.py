"""
CSV Storage Provider handling serializing nested structures (Marks) into delimiters.
"""
import csv
import os
import tempfile
from pathlib import Path
from typing import List, Optional
from storage.base_storage import BaseStorage
from models.student import Student
from utils.exceptions import StorageError

CSV_HEADERS = [
    "student_id", "name", "age", "gender", "class_year", "course",
    "email", "phone", "dob", "address", "admission_date",
    "classes_attended", "total_classes", "marks_serialized", "is_active"
]

class CSVStorage(BaseStorage):
    def __init__(self, file_path: Path):
        self.file_path = Path(file_path)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(CSV_HEADERS)

    def _serialize_marks(self, marks_dict: dict) -> str:
        return "|".join([f"{k}={v}" for k, v in marks_dict.items()])

    def _deserialize_marks(self, serialized: str) -> dict:
        if not serialized or serialized.strip() == "":
            return {}
        marks = {}
        for item in serialized.split("|"):
            if "=" in item:
                subj, val = item.split("=", 1)
                try:
                    marks[subj.strip()] = float(val)
                except ValueError:
                    continue
        return marks

    def _atomic_write(self, rows: list):
        dir_name = self.file_path.parent
        try:
            with tempfile.NamedTemporaryFile("w", dir=dir_name, delete=False, newline="", encoding="utf-8") as tf:
                writer = csv.writer(tf)
                writer.writerow(CSV_HEADERS)
                writer.writerows(rows)
                temp_name = tf.name
            os.replace(temp_name, self.file_path)
        except Exception as e:
            if 'temp_name' in locals() and os.path.exists(temp_name):
                os.remove(temp_name)
            raise StorageError(f"Failed atomic write to CSV: {e}")

    def load_students(self) -> List[Student]:
        students = []
        if not self.file_path.exists():
            return []
        try:
            with open(self.file_path, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if not row or not row.get("student_id"):
                        continue
                    is_active = str(row.get("is_active", "True")).lower() == "true"
                    if not is_active:
                        continue
                    student = Student(
                        student_id=row["student_id"],
                        name=row["name"],
                        age=int(row["age"]),
                        gender=row["gender"],
                        class_year=row["class_year"],
                        course=row["course"],
                        email=row["email"],
                        phone=row["phone"],
                        dob=row["dob"],
                        address=row["address"],
                        admission_date=row["admission_date"],
                        classes_attended=int(row["classes_attended"]),
                        total_classes=int(row["total_classes"]),
                        marks=self._deserialize_marks(row.get("marks_serialized", "")),
                        is_active=is_active
                    )
                    students.append(student)
            return students
        except Exception as e:
            raise StorageError(f"Failed parsing CSV records: {e}")

    def save_students(self, students: List[Student]) -> None:
        rows = []
        for s in students:
            rows.append([
                s.student_id,
                s.name,
                s.age,
                s.gender,
                s.class_year,
                s.course,
                s.email,
                s.phone,
                s.dob,
                s.address,
                s.admission_date,
                s.classes_attended,
                s.total_classes,
                self._serialize_marks(s.marks),
                str(s.is_active)
            ])
        self._atomic_write(rows)

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
        if not self.file_path.exists():
            return False

        updated_rows = []
        found = False
        with open(self.file_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("student_id", "").upper() == student_id.upper():
                    found = True
                    if soft_delete:
                        row["is_active"] = "False"
                        updated_rows.append([row[h] for h in CSV_HEADERS])
                else:
                    updated_rows.append([row[h] for h in CSV_HEADERS])

        if found:
            self._atomic_write(updated_rows)
        return found