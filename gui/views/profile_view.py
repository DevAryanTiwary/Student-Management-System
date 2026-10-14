from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton,
    QHeaderView, QMessageBox
)
from managers.student_manager import StudentManager
from managers.report_manager import ReportManager
from gui.widgets.stat_card import StatCard

class StudentProfileView(QWidget):
    def __init__(self, student_mgr: StudentManager, on_back, parent=None):
        super().__init__(parent)
        self.student_mgr = student_mgr
        self.on_back = on_back
        self.active_student_id = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        top_bar = QHBoxLayout()
        btn_back = QPushButton("◀ Back to Directory")
        btn_back.setObjectName("SecondaryButton")
        btn_back.clicked.connect(self.on_back)

        self.lbl_name = QLabel("Student Dossier")
        self.lbl_name.setStyleSheet("font-size: 20px; font-weight: bold;")

        top_bar.addWidget(btn_back)
        top_bar.addWidget(self.lbl_name)
        top_bar.addStretch()

        self.btn_archive = QPushButton("Archive Student")
        self.btn_archive.setObjectName("DangerButton")
        self.btn_archive.clicked.connect(self.archive_student)
        top_bar.addWidget(self.btn_archive)
        layout.addLayout(top_bar)

        kpis = QHBoxLayout()
        self.kpi_pct = StatCard("Percentage", "0.0%", "Overall Score")
        self.kpi_grade = StatCard("Grade", "-", "Academic Scale")
        self.kpi_rank = StatCard("Class Rank", "#-", "Cohort Standing")
        self.kpi_att = StatCard("Attendance", "0%", "Present")

        kpis.addWidget(self.kpi_pct)
        kpis.addWidget(self.kpi_grade)
        kpis.addWidget(self.kpi_rank)
        kpis.addWidget(self.kpi_att)
        layout.addLayout(kpis)

        lbl_tbl = QLabel("Subject-wise Performance Breakdown:")
        lbl_tbl.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(lbl_tbl)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Subject", "Score Obtained", "Maximum Marks"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

    def load_student(self, student_id: str):
        self.active_student_id = student_id
        student = self.student_mgr.get_student(student_id)
        if not student:
            return

        rm = ReportManager(self.student_mgr.get_all_students())
        rank = rm.get_student_rank(student_id)

        self.lbl_name.setText(f"{student.name} ({student.student_id}) — {student.course}")
        self.kpi_pct.update_value(f"{student.percentage}%", f"{student.total_marks}/{student.max_possible_marks}")
        self.kpi_grade.update_value(student.grade, student.pass_status)
        self.kpi_rank.update_value(f"#{rank}" if rank > 0 else "N/A", "Active Cohort")
        self.kpi_att.update_value(f"{student.attendance_percentage}%", f"{student.classes_attended}/{student.total_classes} Classes")

        self.table.setRowCount(len(student.marks))
        for r, (subj, score) in enumerate(student.marks.items()):
            self.table.setItem(r, 0, QTableWidgetItem(subj))
            self.table.setItem(r, 1, QTableWidgetItem(f"{score:.2f}"))
            self.table.setItem(r, 2, QTableWidgetItem("100.00"))

    def archive_student(self):
        if not self.active_student_id:
            return
        conf = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to soft-delete / archive student {self.active_student_id}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if conf == QMessageBox.Yes:
            self.student_mgr.delete_student(self.active_student_id, soft_delete=True)
            self.on_back()