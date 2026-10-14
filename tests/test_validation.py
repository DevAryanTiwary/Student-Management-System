import unittest
from utils.validators import (
    validate_student_id,
    validate_name,
    validate_age,
    validate_email,
    validate_phone,
    validate_marks,
    validate_attendance
)
from utils.exceptions import ValidationError

class TestValidationModule(unittest.TestCase):
    def test_valid_student_id(self):
        self.assertEqual(validate_student_id("stu001"), "STU001")
        self.assertEqual(validate_student_id("STU1234"), "STU1234")

    def test_invalid_student_id(self):
        with self.assertRaises(ValidationError):
            validate_student_id("ST12")
        with self.assertRaises(ValidationError):
            validate_student_id("STUDENT001")

    def test_name_validation(self):
        self.assertEqual(validate_name("  John Doe  "), "John Doe")
        with self.assertRaises(ValidationError):
            validate_name("J")
        with self.assertRaises(ValidationError):
            validate_name("John123")

    def test_age_validation(self):
        self.assertEqual(validate_age("20"), 20)
        with self.assertRaises(ValidationError):
            validate_age(12)
        with self.assertRaises(ValidationError):
            validate_age(120)

    def test_email_validation(self):
        self.assertEqual(validate_email("test.student@univ.edu"), "test.student@univ.edu")
        with self.assertRaises(ValidationError):
            validate_email("invalid_email.com")

    def test_phone_validation(self):
        self.assertEqual(validate_phone("+91-9876543210"), "+919876543210")
        with self.assertRaises(ValidationError):
            validate_phone("123")

    def test_marks_bounds(self):
        self.assertEqual(validate_marks("88.5"), 88.5)
        with self.assertRaises(ValidationError):
            validate_marks(105)
        with self.assertRaises(ValidationError):
            validate_marks(-5)

    def test_attendance_bounds(self):
        att, tot = validate_attendance(80, 100)
        self.assertEqual((att, tot), (80, 100))
        with self.assertRaises(ValidationError):
            validate_attendance(105, 100)