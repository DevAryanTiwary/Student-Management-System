from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLabel, QHeaderView, QMessageBox
)
from managers.student_manager import StudentManager
from managers.marks_manager import MarksManager
from gui.dialogs.marks_dialog import MarksDialog

class AcademicsView(QWidget):
    def __init__(self, student_mgr: StudentManager, marks_mgr: MarksManager, parent=None):
        super().__init__(parent)
        self.student_mgr = student_mgr
        self.marks_mgr = marks_mgr

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        lbl = QLabel("Academic Marks & Subject Performance Ledger")
        lbl.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(lbl)

        self.table = QTableWidget()
        self.headers = ["ID", "Name", "Total Marks", "Average", "Percentage", "Grade", "Status", "Action"]
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
            self.table.setItem(r, 2, QTableWidgetItem(f"{s.total_marks}/{s.max_possible_marks}"))
            self.table.setItem(r, 3, QTableWidgetItem(f"{s.average_marks}"))
            self.table.setItem(r, 4, QTableWidgetItem(f"{s.percentage}%"))
            self.table.setItem(r, 5, QTableWidgetItem(s.grade))
            self.table.setItem(r, 6, QTableWidgetItem(s.pass_status))

            btn_edit = QPushButton("Manage Marks")
            btn_edit.clicked.connect(lambda _, st=s: self.open_marks_dialog(st))
            self.table.setCellWidget(r, 7, btn_edit)

    def open_marks_dialog(self, student):
        dlg = MarksDialog(student, self.marks_mgr, self)
        if dlg.exec() == MarksDialog.Accepted:
            self.load_data()