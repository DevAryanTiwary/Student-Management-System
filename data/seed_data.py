"""
Seed generator populating both JSON and CSV files with realistic sample records.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from storage.json_storage import JSONStorage
from storage.csv_storage import CSVStorage
from models.student import Student
from config import STUDENTS_JSON_FILE, STUDENTS_CSV_FILE

SAMPLE_STUDENTS = [
    Student("STU001", "Aarav Sharma", 20, "Male", "Year-2", "Computer Science", "aarav.sharma@example.com", "+919876543210", "2006-03-15", "Delhi, India", "2024-08-01", 85, 90, {"Python": 95.0, "DBMS": 88.0, "Java": 92.0, "Mathematics": 90.0, "Computer Networks": 89.0}),
    Student("STU002", "Diya Patel", 21, "Female", "Year-3", "Information Technology", "diya.patel@example.com", "+919876543211", "2005-07-22", "Ahmedabad, India", "2023-08-01", 88, 90, {"Python": 91.0, "DBMS": 94.0, "Java": 89.0, "Mathematics": 96.0, "Computer Networks": 92.0}),
    Student("STU003", "Rohan Verma", 20, "Male", "Year-2", "Computer Science", "rohan.verma@example.com", "+919876543212", "2006-11-10", "Lucknow, India", "2024-08-01", 60, 90, {"Python": 72.0, "DBMS": 68.0, "Java": 75.0, "Mathematics": 64.0, "Computer Networks": 70.0}),
    Student("STU004", "Ananya Iyer", 19, "Female", "Year-1", "Data Science", "ananya.iyer@example.com", "+919876543213", "2007-01-30", "Chennai, India", "2025-08-01", 89, 90, {"Python": 98.0, "DBMS": 92.0, "Java": 95.0, "Mathematics": 99.0, "Computer Networks": 94.0}),
    Student("STU005", "Kabir Singh", 22, "Male", "Year-4", "Computer Science", "kabir.singh@example.com", "+919876543214", "2004-05-18", "Chandigarh, India", "2022-08-01", 50, 90, {"Python": 35.0, "DBMS": 42.0, "Java": 38.0, "Mathematics": 45.0, "Computer Networks": 50.0}),
    Student("STU006", "Ishita Gupta", 20, "Female", "Year-2", "Information Technology", "ishita.gupta@example.com", "+919876543215", "2006-09-05", "Kolkata, India", "2024-08-01", 82, 90, {"Python": 84.0, "DBMS": 80.0, "Java": 86.0, "Mathematics": 78.0, "Computer Networks": 82.0}),
    Student("STU007", "Vikram Malhotra", 21, "Male", "Year-3", "Data Science", "vikram.m@example.com", "+919876543216", "2005-12-12", "Mumbai, India", "2023-08-01", 76, 90, {"Python": 78.0, "DBMS": 74.0, "Java": 80.0, "Mathematics": 82.0, "Computer Networks": 75.0}),
    Student("STU008", "Sneha Rao", 20, "Female", "Year-2", "Computer Science", "sneha.rao@example.com", "+919876543217", "2006-04-25", "Bengaluru, India", "2024-08-01", 84, 90, {"Python": 88.0, "DBMS": 85.0, "Java": 82.0, "Mathematics": 90.0, "Computer Networks": 87.0}),
    Student("STU009", "Rahul Nair", 22, "Male", "Year-4", "Information Technology", "rahul.nair@example.com", "+919876543218", "2004-02-14", "Kochi, India", "2022-08-01", 62, 90, {"Python": 55.0, "DBMS": 58.0, "Java": 60.0, "Mathematics": 52.0, "Computer Networks": 57.0}),
    Student("STU010", "Pooja Hegde", 19, "Female", "Year-1", "Computer Science", "pooja.h@example.com", "+919876543219", "2007-08-19", "Hyderabad, India", "2025-08-01", 79, 90, {"Python": 65.0, "DBMS": 70.0, "Java": 68.0, "Mathematics": 72.0, "Computer Networks": 66.0}),
]

def seed():
    j_storage = JSONStorage(STUDENTS_JSON_FILE)
    j_storage.save_students(SAMPLE_STUDENTS)

    c_storage = CSVStorage(STUDENTS_CSV_FILE)
    c_storage.save_students(SAMPLE_STUDENTS)

    print(f"Successfully seeded {len(SAMPLE_STUDENTS)} student records into JSON and CSV stores.")

if __name__ == "__main__":
    seed()