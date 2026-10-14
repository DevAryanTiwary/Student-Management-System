import unittest
import tempfile
from pathlib import Path
from models.student import Student
from storage.json_storage import JSONStorage
from storage.csv_storage import CSVStorage

class TestStorageEngines(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.json_file = Path(self.temp_dir.name) / "test_students.json"
        self.csv_file = Path(self.temp_dir.name) / "test_students.csv"

        self.student = Student(
            student_id="STU001",
            name="Bob Brown",
            age=22,
            gender="Male",
            class_year="Year-3",
            course="IT",
            email="bob@example.com",
            phone="+919876543210",
            dob="2004-02-14",
            address="Pune",
            admission_date="2023-08-01",
            classes_attended=40,
            total_classes=50,
            marks={"Python": 85.0}
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_json_persistence(self):
        storage = JSONStorage(self.json_file)
        storage.add_student(self.student)
        loaded = storage.load_students()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].name, "Bob Brown")
        self.assertEqual(loaded[0].marks["Python"], 85.0)

    def test_csv_persistence(self):
        storage = CSVStorage(self.csv_file)
        storage.add_student(self.student)
        loaded = storage.load_students()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].name, "Bob Brown")
        self.assertEqual(loaded[0].marks["Python"], 85.0)