"""
Student Management Controller: CRUD, ID generator, and transaction orchestrator.
"""
from typing import List
from models.student import Student
from storage.base_storage import BaseStorage
from utils.exceptions import DuplicateStudentError, StudentNotFoundError
from utils.logger import log_activity
from utils.validators import (
    validate_student_id,
    validate_name,
    validate_age,
    validate_gender,
    validate_email,
    validate_phone,
    validate_date
)

class StudentManager:
    def __init__(self, storage: BaseStorage, admin_username: str = "Admin"):
        self.storage = storage
        self.admin_username = admin_username

    def generate_next_student_id(self) -> str:
        students = self.storage.load_students()
        max_id = 0
        for s in students:
            if s.student_id.startswith("STU"):
                suffix = s.student_id[3:]
                if suffix.isdigit():
                    max_id = max(max_id, int(suffix))
        return f"STU{max_id + 1:03d}"

    def add_student(self, student_data: dict) -> Student:
        sid = validate_student_id(student_data["student_id"])
        if self.storage.get_student(sid):
            raise DuplicateStudentError(f"Student with ID '{sid}' already exists.")

        student = Student(
            student_id=sid,
            name=validate_name(student_data["name"]),
            age=validate_age(student_data["age"]),
            gender=validate_gender(student_data["gender"]),
            class_year=student_data["class_year"].strip(),
            course=student_data["course"].strip(),
            email=validate_email(student_data["email"]),
            phone=validate_phone(student_data["phone"]),
            dob=validate_date(student_data["dob"], "Date of Birth"),
            address=student_data.get("address", "").strip(),
            admission_date=validate_date(student_data["admission_date"], "Admission Date"),
            classes_attended=student_data.get("classes_attended", 0),
            total_classes=student_data.get("total_classes", 0),
            marks=student_data.get("marks", {})
        )

        self.storage.add_student(student)
        log_activity(self.admin_username, "ADD_STUDENT", f"Added student: {student.name}", student.student_id)
        return student

    def get_all_students(self) -> List[Student]:
        return self.storage.load_students()

    def get_student(self, student_id: str) -> Student:
        student = self.storage.get_student(student_id)
        if not student:
            raise StudentNotFoundError(f"Student with ID '{student_id}' does not exist.")
        return student

    def update_student(self, student_id: str, updates: dict) -> Student:
        student = self.get_student(student_id)

        if "name" in updates and updates["name"]:
            student.name = validate_name(updates["name"])
        if "age" in updates and updates["age"]:
            student.age = validate_age(updates["age"])
        if "gender" in updates and updates["gender"]:
            student.gender = validate_gender(updates["gender"])
        if "class_year" in updates and updates["class_year"]:
            student.class_year = updates["class_year"].strip()
        if "course" in updates and updates["course"]:
            student.course = updates["course"].strip()
        if "email" in updates and updates["email"]:
            student.email = validate_email(updates["email"])
        if "phone" in updates and updates["phone"]:
            student.phone = validate_phone(updates["phone"])
        if "dob" in updates and updates["dob"]:
            student.dob = validate_date(updates["dob"], "Date of Birth")
        if "address" in updates and updates["address"]:
            student.address = updates["address"].strip()

        self.storage.update_student(student)
        log_activity(self.admin_username, "UPDATE_STUDENT", "Updated basic demographic fields", student.student_id)
        return student

    def delete_student(self, student_id: str, soft_delete: bool = True) -> bool:
        _ = self.get_student(student_id)
        success = self.storage.delete_student(student_id, soft_delete=soft_delete)
        if success:
            log_activity(self.admin_username, "DELETE_STUDENT", f"Deleted student (soft={soft_delete})", student_id)
        return success