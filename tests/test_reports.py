import unittest
from models.student import Student
from managers.report_manager import ReportManager

class TestReports(unittest.TestCase):
    def setUp(self):
        self.s1 = Student("STU001", "High Scorer", 20, "Male", "Year-1", "CS", "h@test.com", "1234567890", "2006-01-01", "City", "2024-01-01", 90, 100, {"Python": 95.0})
        self.s2 = Student("STU002", "Mid Scorer", 20, "Female", "Year-1", "CS", "m@test.com", "1234567891", "2006-01-01", "City", "2024-01-01", 70, 100, {"Python": 75.0})
        self.s3 = Student("STU003", "Low Scorer", 20, "Male", "Year-1", "CS", "l@test.com", "1234567892", "2006-01-01", "City", "2024-01-01", 50, 100, {"Python": 35.0})
        self.students = [self.s1, self.s2, self.s3]
        self.rm = ReportManager(self.students)

    def test_toppers(self):
        toppers = self.rm.get_toppers(1)
        self.assertEqual(toppers[0].student_id, "STU001")

    def test_pass_fail(self):
        pf = self.rm.generate_pass_fail_summary()
        self.assertEqual(pf["passed"], 2)
        self.assertEqual(pf["failed"], 1)

    def test_rank(self):
        rank = self.rm.get_student_rank("STU002")
        self.assertEqual(rank, 2)