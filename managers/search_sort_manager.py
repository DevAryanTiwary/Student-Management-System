"""
High-performance searching, multi-criteria filtering, and sorting algorithms.
"""
from typing import List
from models.student import Student

class SearchSortManager:
    @staticmethod
    def search(students: List[Student], query: str, field: str = "all") -> List[Student]:
        q = query.strip().lower()
        if not q:
            return students

        results = []
        for s in students:
            if field == "id" and q in s.student_id.lower():
                results.append(s)
            elif field == "name" and q in s.name.lower():
                results.append(s)
            elif field == "class" and q in s.class_year.lower():
                results.append(s)
            elif field == "course" and q in s.course.lower():
                results.append(s)
            elif field == "email" and q in s.email.lower():
                results.append(s)
            elif field == "phone" and q in s.phone.lower():
                results.append(s)
            elif field == "grade" and q == s.grade.lower():
                results.append(s)
            elif field == "all":
                if (q in s.student_id.lower() or
                    q in s.name.lower() or
                    q in s.course.lower() or
                    q in s.class_year.lower() or
                    q in s.email.lower() or
                    q in s.phone.lower()):
                    results.append(s)
        return results

    @staticmethod
    def filter_students(
        students: List[Student],
        grade: str = None,
        pass_status: str = None,
        min_attendance: float = None,
        max_attendance: float = None,
        min_pct: float = None,
        max_pct: float = None,
        course: str = None,
        class_year: str = None
    ) -> List[Student]:
        filtered = students
        if grade:
            filtered = [s for s in filtered if s.grade.upper() == grade.strip().upper()]
        if pass_status:
            is_pass = pass_status.strip().lower() == "pass"
            filtered = [s for s in filtered if s.is_passed == is_pass]
        if min_attendance is not None:
            filtered = [s for s in filtered if s.attendance_percentage >= min_attendance]
        if max_attendance is not None:
            filtered = [s for s in filtered if s.attendance_percentage <= max_attendance]
        if min_pct is not None:
            filtered = [s for s in filtered if s.percentage >= min_pct]
        if max_pct is not None:
            filtered = [s for s in filtered if s.percentage <= max_pct]
        if course:
            filtered = [s for s in filtered if s.course.lower() == course.strip().lower()]
        if class_year:
            filtered = [s for s in filtered if s.class_year.lower() == class_year.strip().lower()]
        return filtered

    @staticmethod
    def sort_students(students: List[Student], criterion: str, reverse: bool = False) -> List[Student]:
        key_funcs = {
            "id": lambda s: s.student_id,
            "name": lambda s: s.name.lower(),
            "age": lambda s: s.age,
            "marks": lambda s: s.total_marks,
            "percentage": lambda s: s.percentage,
            "grade": lambda s: s.percentage,
            "attendance": lambda s: s.attendance_percentage,
            "admission_date": lambda s: s.admission_date
        }
        func = key_funcs.get(criterion.lower(), lambda s: s.student_id)
        return sorted(students, key=func, reverse=reverse)