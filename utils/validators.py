"""
Centralized validation suite. Pure functions ensuring data integrity.
"""
import re
from datetime import datetime
from utils.exceptions import ValidationError
from config import MIN_MARKS_PER_SUBJECT, MAX_MARKS_PER_SUBJECT

def validate_student_id(student_id: str) -> str:
    cleaned = student_id.strip().upper()
    if not re.match(r"^STU\d{3,}$", cleaned):
        raise ValidationError("Student ID must follow format 'STU' followed by at least 3 digits (e.g., STU001).")
    return cleaned

def validate_name(name: str) -> str:
    cleaned = name.strip()
    if not cleaned:
        raise ValidationError("Name cannot be empty.")
    if len(cleaned) < 2 or len(cleaned) > 70:
        raise ValidationError("Name must be between 2 and 70 characters long.")
    if not re.match(r"^[a-zA-Z\s.'-]+$", cleaned):
        raise ValidationError("Name contains invalid characters.")
    return " ".join(cleaned.split())

def validate_age(age_val) -> int:
    try:
        age = int(age_val)
    except (ValueError, TypeError):
        raise ValidationError("Age must be an integer.")
    if age < 14 or age > 100:
        raise ValidationError("Age must be between 14 and 100.")
    return age

def validate_gender(gender: str) -> str:
    cleaned = gender.strip().capitalize()
    allowed = ["Male", "Female", "Other", "Prefer not to say"]
    if cleaned not in allowed:
        raise ValidationError(f"Gender must be one of: {', '.join(allowed)}.")
    return cleaned

def validate_email(email: str) -> str:
    cleaned = email.strip().lower()
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_regex, cleaned):
        raise ValidationError("Invalid email address format.")
    return cleaned

def validate_phone(phone: str) -> str:
    cleaned = re.sub(r"[\s\-()]", "", phone.strip())
    if not re.match(r"^\+?\d{10,15}$", cleaned):
        raise ValidationError("Phone number must contain 10 to 15 digits, optionally prefixed with '+'.")
    return cleaned

def validate_date(date_str: str, field_name: str = "Date") -> str:
    cleaned = date_str.strip()
    try:
        parsed = datetime.strptime(cleaned, "%Y-%m-%d").date()
        if parsed > datetime.now().date():
            raise ValidationError(f"{field_name} cannot be in the future.")
        return cleaned
    except ValueError:
        raise ValidationError(f"{field_name} must be in YYYY-MM-DD format.")

def validate_marks(marks_val) -> float:
    try:
        marks = float(marks_val)
    except (ValueError, TypeError):
        raise ValidationError("Marks must be numeric.")
    if marks < MIN_MARKS_PER_SUBJECT or marks > MAX_MARKS_PER_SUBJECT:
        raise ValidationError(f"Marks must be between {MIN_MARKS_PER_SUBJECT} and {MAX_MARKS_PER_SUBJECT}.")
    return round(marks, 2)

def validate_attendance(attended, total) -> tuple[int, int]:
    try:
        att = int(attended)
        tot = int(total)
    except (ValueError, TypeError):
        raise ValidationError("Classes attended and total classes must be integers.")
    if tot < 0 or att < 0:
        raise ValidationError("Attendance counts cannot be negative.")
    if att > tot:
        raise ValidationError("Classes attended cannot exceed total classes.")
    return att, tot