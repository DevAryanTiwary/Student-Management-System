from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QLabel, QMessageBox
)
from managers.marks_manager import MarksManager
from config import PASSING_MARKS, MIN_ATTENDANCE_PERCENT, DATA_STORAGE_FORMAT

class SettingsView(QWidget):
    def __init__(self, marks_mgr: MarksManager, parent=None):
        super().__init__(parent)
        self.marks_mgr = marks_mgr

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        lbl = QLabel("System Settings & Subject Catalog")
        lbl.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(lbl)

        form = QFormLayout()
        form.addRow("Active Storage Engine:", QLabel(DATA_STORAGE_FORMAT))
        form.addRow("Passing Score Threshold:", QLabel(f"{PASSING_MARKS}%"))
        form.addRow("Minimum Attendance Target:", QLabel(f"{MIN_ATTENDANCE_PERCENT}%"))

        self.txt_new_sub = QLineEdit()
        self.txt_new_sub.setPlaceholderText("e.g. Artificial Intelligence")
        btn_add_sub = QPushButton("+ Add Subject")
        btn_add_sub.clicked.connect(self.add_subject)

        form.addRow("New Subject:", self.txt_new_sub)
        form.addRow("", btn_add_sub)
        layout.addLayout(form)

        self.lbl_subs = QLabel()
        layout.addWidget(self.lbl_subs)
        self.render_subjects()

    def render_subjects(self):
        subs = self.marks_mgr.get_configured_subjects()
        self.lbl_subs.setText("Configured Subjects:\n" + "\n".join([f"  • {s}" for s in subs]))

    def add_subject(self):
        s = self.txt_new_sub.text().strip()
        try:
            self.marks_mgr.add_configured_subject(s)
            self.txt_new_sub.clear()
            self.render_subjects()
            QMessageBox.information(self, "Success", f"Subject '{s}' registered.")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))