"""
Student Domain Model encapsulating student state, marks, and attendance metrics.
Backward-compatible upgrade supporting academic sessions and soft-deletion metadata.
"""
from typing import Dict, Any
from config import GRADE_SCALE, PASSING_MARKS, MIN_ATTENDANCE_PERCENT, CURRENT_ACADEMIC_YEAR, CURRENT_SEMESTER

class Student:
    def __init__(
        self,
        student_id: str,
        name: str,
        age: int,
        gender: str,
        class_year: str,
        course: str,
        email: str,
        phone: str,
        dob: str,
        address: str,
        admission_date: str,
        classes_attended: int = 0,
        total_classes: int = 0,
        marks: Dict[str, float] = None,
        is_active: bool = True,
        academic_year: str = CURRENT_ACADEMIC_YEAR,
        semester: str = CURRENT_SEMESTER
    ):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.gender = gender
        self.class_year = class_year
        self.course = course
        self.email = email
        self.phone = phone
        self.dob = dob
        self.address = address
        self.admission_date = admission_date
        self.classes_attended = classes_attended
        self.total_classes = total_classes
        self.marks = marks if marks is not None else {}
        self.is_active = is_active
        self.academic_year = academic_year
        self.semester = semester

    # --- Computed Academic Properties ---

    @property
    def total_marks(self) -> float:
        return round(sum(self.marks.values()), 2)

    @property
    def max_possible_marks(self) -> float:
        return float(len(self.marks) * 100)

    @property
    def percentage(self) -> float:
        if not self.marks:
            return 0.0
        return round((self.total_marks / self.max_possible_marks) * 100, 2)

    @property
    def average_marks(self) -> float:
        if not self.marks:
            return 0.0
        return round(self.total_marks / len(self.marks), 2)

    @property
    def grade(self) -> str:
        if not self.marks:
            return "N/A"
        pct = self.percentage
        for min_pct, grade_symbol in GRADE_SCALE:
            if pct >= min_pct:
                return grade_symbol
        return "F"

    @property
    def is_passed(self) -> bool:
        if not self.marks:
            return False
        return all(m >= PASSING_MARKS for m in self.marks.values())

    @property
    def pass_status(self) -> str:
        return "Pass" if self.is_passed else "Fail"

    # --- Attendance Computations ---

    @property
    def attendance_percentage(self) -> float:
        if self.total_classes == 0:
            return 0.0
        return round((self.classes_attended / self.total_classes) * 100, 2)

    @property
    def attendance_status(self) -> str:
        return "Adequate" if self.attendance_percentage >= MIN_ATTENDANCE_PERCENT else "Shortage"

    # --- Serialization Handlers ---

    def to_dict(self) -> Dict[str, Any]:
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "class_year": self.class_year,
            "course": self.course,
            "email": self.email,
            "phone": self.phone,
            "dob": self.dob,
            "address": self.address,
            "admission_date": self.admission_date,
            "classes_attended": self.classes_attended,
            "total_classes": self.total_classes,
            "marks": self.marks,
            "is_active": self.is_active,
            "academic_year": self.academic_year,
            "semester": self.semester
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Student":
        return cls(
            student_id=str(data.get("student_id", "")),
            name=str(data.get("name", "")),
            age=int(data.get("age", 0)),
            gender=str(data.get("gender", "")),
            class_year=str(data.get("class_year", "")),
            course=str(data.get("course", "")),
            email=str(data.get("email", "")),
            phone=str(data.get("phone", "")),
            dob=str(data.get("dob", "")),
            address=str(data.get("address", "")),
            admission_date=str(data.get("admission_date", "")),
            classes_attended=int(data.get("classes_attended", 0)),
            total_classes=int(data.get("total_classes", 0)),
            marks={k: float(v) for k, v in data.get("marks", {}).items()},
            is_active=bool(data.get("is_active", True)),
            academic_year=str(data.get("academic_year", CURRENT_ACADEMIC_YEAR)),
            semester=str(data.get("semester", CURRENT_SEMESTER))
        )