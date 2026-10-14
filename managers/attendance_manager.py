"""
Attendance tracking, calculation, and constraint management.
"""
from storage.base_storage import BaseStorage
from utils.exceptions import StudentNotFoundError
from utils.validators import validate_attendance
from utils.logger import log_activity

class AttendanceManager:
    def __init__(self, storage: BaseStorage, admin_username: str = "Admin"):
        self.storage = storage
        self.admin_username = admin_username

    def record_attendance(self, student_id: str, attended: int, total: int):
        student = self.storage.get_student(student_id)
        if not student:
            raise StudentNotFoundError(f"Student {student_id} not found.")

        att, tot = validate_attendance(attended, total)
        student.classes_attended = att
        student.total_classes = tot

        self.storage.update_student(student)
        log_activity(
            self.admin_username,
            "UPDATE_ATTENDANCE",
            f"Attendance recorded: {att}/{tot} ({student.attendance_percentage}%)",
            student_id
        )