import unittest
from models.student import Student

class TestStudentModel(unittest.TestCase):
    def setUp(self):
        self.student = Student(
            student_id="STU001",
            name="Alice Walker",
            age=20,
            gender="Female",
            class_year="Year-2",
            course="Computer Science",
            email="alice@example.com",
            phone="+919876543210",
            dob="2006-05-10",
            address="Delhi",
            admission_date="2024-08-01",
            classes_attended=80,
            total_classes=100,
            marks={"Python": 90.0, "DBMS": 80.0, "Java": 100.0}
        )

    def test_academic_computations(self):
        self.assertEqual(self.student.total_marks, 270.0)
        self.assertEqual(self.student.percentage, 90.0)
        self.assertEqual(self.student.grade, "A+")
        self.assertTrue(self.student.is_passed)

    def test_attendance_computations(self):
        self.assertEqual(self.student.attendance_percentage, 80.0)
        self.assertEqual(self.student.attendance_status, "Adequate")

    def test_failing_student(self):
        self.student.marks["Python"] = 30.0
        self.assertFalse(self.student.is_passed)
        self.assertEqual(self.student.pass_status, "Fail")