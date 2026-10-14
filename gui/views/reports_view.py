from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTextEdit, QMessageBox
)
from managers.student_manager import StudentManager
from managers.report_manager import ReportManager
from managers.export_manager import ExportManager

class ReportsView(QWidget):
    def __init__(self, student_mgr: StudentManager, export_mgr: ExportManager, parent=None):
        super().__init__(parent)
        self.student_mgr = student_mgr
        self.export_mgr = export_mgr

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        lbl = QLabel("Report & Analytics Generation Center")
        lbl.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(lbl)

        btn_bar = QHBoxLayout()
        btn_summary = QPushButton("Class Performance Summary")
        btn_summary.clicked.connect(self.generate_class_summary)

        btn_toppers = QPushButton("Top 5 Toppers")
        btn_toppers.clicked.connect(self.generate_toppers)

        btn_export_csv = QPushButton("Export Roster (CSV)")
        btn_export_csv.setObjectName("SecondaryButton")
        btn_export_csv.clicked.connect(self.export_csv)

        btn_export_pdf = QPushButton("Export Summary (PDF)")
        btn_export_pdf.setObjectName("SecondaryButton")
        btn_export_pdf.clicked.connect(self.export_pdf)

        btn_bar.addWidget(btn_summary)
        btn_bar.addWidget(btn_toppers)
        btn_bar.addWidget(btn_export_csv)
        btn_bar.addWidget(btn_export_pdf)
        btn_bar.addStretch()
        layout.addLayout(btn_bar)

        self.txt_display = QTextEdit()
        self.txt_display.setReadOnly(True)
        layout.addWidget(self.txt_display)

        self.generate_class_summary()

    def generate_class_summary(self):
        students = self.student_mgr.get_all_students()
        rm = ReportManager(students)
        summary = rm.get_class_performance_summary()

        lines = [
            "=" * 60,
            "COHORT ACADEMIC & ATTENDANCE SUMMARY REPORT".center(60),
            "=" * 60,
            f"Total Assessed Students : {summary.get('total_students', 0)}",
            f"Overall Cohort Average  : {summary.get('average_percentage', 0.0)}%",
            f"Highest Percentage      : {summary.get('highest_percentage', 0.0)}%",
            f"Lowest Percentage       : {summary.get('lowest_percentage', 0.0)}%",
            f"Cohort Topper           : {summary.get('topper', 'N/A')}",
            f"Overall Pass Rate       : {summary.get('pass_fail', {}).get('pass_pct', 0.0)}%",
            f"Average Attendance Rate : {summary.get('attendance', {}).get('avg_att', 0.0)}%",
            "=" * 60
        ]
        self.txt_display.setText("\n".join(lines))

    def generate_toppers(self):
        students = self.student_mgr.get_all_students()
        rm = ReportManager(students)
        toppers = rm.get_toppers(5)

        lines = [
            "=" * 60,
            "TOP 5 ACADEMIC ACHIEVERS".center(60),
            "=" * 60
        ]
        for idx, t in enumerate(toppers):
            lines.append(f"Rank #{idx + 1:<2} | {t.student_id} | {t.name:<25} | {t.percentage:>6.2f}% | Grade {t.grade}")
        lines.append("=" * 60)
        self.txt_display.setText("\n".join(lines))

    def export_csv(self):
        students = self.student_mgr.get_all_students()
        p = self.export_mgr.export_students_to_csv("students_report", students)
        QMessageBox.information(self, "Exported", f"CSV file exported to:\n{p.resolve()}")

    def export_pdf(self):
        students = self.student_mgr.get_all_students()
        rm = ReportManager(students)
        summary = rm.get_class_performance_summary()
        lines = [
            f"Total Students: {summary.get('total_students', 0)}",
            f"Cohort Average: {summary.get('average_percentage', 0.0)}%",
            f"Topper: {summary.get('topper', 'N/A')}",
            f"Pass Rate: {summary.get('pass_fail', {}).get('pass_pct', 0.0)}%"
        ]
        p = self.export_mgr.export_to_pdf("class_performance", "Cohort Performance Summary", lines)
        if p:
            QMessageBox.information(self, "Exported", f"PDF exported to:\n{p.resolve()}")
        else:
            QMessageBox.warning(self, "Missing Dependency", "ReportLab is required for PDF output. Install via pip install reportlab")