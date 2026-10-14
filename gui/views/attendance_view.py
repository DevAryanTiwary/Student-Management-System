from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLabel, QHeaderView,
    QSpinBox, QMessageBox
)
from managers.student_manager import StudentManager
from managers.attendance_manager import AttendanceManager
from config import MIN_ATTENDANCE_PERCENT

class AttendanceView(QWidget):
    def __init__(self, student_mgr: StudentManager, att_mgr: AttendanceManager, parent=None):
        super().__init__(parent)
        self.student_mgr = student_mgr
        self.att_mgr = att_mgr

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        lbl = QLabel(f"Cohort Attendance Ledger (Threshold: {MIN_ATTENDANCE_PERCENT}%)")
        lbl.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(lbl)

        self.table = QTableWidget()
        self.headers = ["ID", "Name", "Attended", "Total Classes", "Attendance %", "Risk Status", "Update"]
        self.table.setColumnCount(len(self.headers))
        self.table.setHorizontalHeaderLabels(self.headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.load_data()

    def load_data(self):
        students = self.student_mgr.get_all_students()
        self.table.setRowCount(len(students))

        for r, s in enumerate(students):
            self.table.setItem(r, 0, QTableWidgetItem(s.student_id))
            self.table.setItem(r, 1, QTableWidgetItem(s.name))

            spn_att = QSpinBox()
            spn_att.setRange(0, 1000)
            spn_att.setValue(s.classes_attended)

            spn_tot = QSpinBox()
            spn_tot.setRange(0, 1000)
            spn_tot.setValue(s.total_classes)

            self.table.setCellWidget(r, 2, spn_att)
            self.table.setCellWidget(r, 3, spn_tot)
            self.table.setItem(r, 4, QTableWidgetItem(f"{s.attendance_percentage}%"))
            self.table.setItem(r, 5, QTableWidgetItem("⚠️ Shortage" if s.attendance_percentage < MIN_ATTENDANCE_PERCENT else "OK"))

            btn_save = QPushButton("Save")
            btn_save.clicked.connect(lambda _, sid=s.student_id, sa=spn_att, st=spn_tot: self.save_record(sid, sa.value(), st.value()))
            self.table.setCellWidget(r, 6, btn_save)

    def save_record(self, student_id: str, attended: int, total: int):
        try:
            self.att_mgr.record_attendance(student_id, attended, total)
            self.load_data()
        except Exception as e:
            QMessageBox.warning(self, "Invalid Entry", str(e))