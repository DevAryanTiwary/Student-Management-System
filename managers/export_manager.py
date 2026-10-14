"""
Export system supporting TXT, CSV, JSON, and optional PDF via ReportLab.
"""
import json
import csv
from pathlib import Path
from config import REPORTS_DIR
from models.student import Student
from utils.logger import log_activity

class ExportManager:
    def __init__(self, admin_username: str = "Admin"):
        self.admin_username = admin_username

    def export_to_txt(self, filename: str, content: str) -> Path:
        out_path = REPORTS_DIR / f"{filename}.txt"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)
        log_activity(self.admin_username, "EXPORT_REPORT", f"Exported TXT: {out_path.name}")
        return out_path

    def export_to_json(self, filename: str, data: dict | list) -> Path:
        out_path = REPORTS_DIR / f"{filename}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        log_activity(self.admin_username, "EXPORT_REPORT", f"Exported JSON: {out_path.name}")
        return out_path

    def export_students_to_csv(self, filename: str, students: list[Student]) -> Path:
        out_path = REPORTS_DIR / f"{filename}.csv"
        headers = [
            "StudentID", "Name", "Class", "Course", "Email", "Phone",
            "AttendancePct", "TotalMarks", "Percentage", "Grade", "Status"
        ]
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for s in students:
                writer.writerow([
                    s.student_id, s.name, s.class_year, s.course, s.email, s.phone,
                    f"{s.attendance_percentage}%", s.total_marks, f"{s.percentage}%",
                    s.grade, s.pass_status
                ])
        log_activity(self.admin_username, "EXPORT_REPORT", f"Exported CSV: {out_path.name}")
        return out_path

    def export_to_pdf(self, filename: str, title: str, text_lines: list[str]) -> Path | None:
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
        except ImportError:
            return None

        out_path = REPORTS_DIR / f"{filename}.pdf"
        c = canvas.Canvas(str(out_path), pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, title)
        c.setLineWidth(1)
        c.line(50, height - 55, width - 50, height - 55)

        c.setFont("Courier", 10)
        y = height - 80
        for line in text_lines:
            c.drawString(50, y, line)
            y -= 14
            if y < 40:
                c.showPage()
                c.setFont("Courier", 10)
                y = height - 50

        c.save()
        log_activity(self.admin_username, "EXPORT_REPORT", f"Exported PDF: {out_path.name}")
        return out_path