from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QLabel, QMessageBox, QHBoxLayout
)
from managers.marks_manager import MarksManager
from models.student import Student

class MarksDialog(QDialog):
    def __init__(self, student: Student, marks_mgr: MarksManager, parent=None):
        super().__init__(parent)
        self.student = student
        self.marks_mgr = marks_mgr
        self.setWindowTitle(f"Manage Marks — {student.name} ({student.student_id})")
        self.setFixedSize(400, 360)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        lbl = QLabel(f"Enter Subject Marks (0 - 100):")
        lbl.setStyleSheet("font-weight: bold; font-size: 14px; color: #63B3ED;")
        layout.addWidget(lbl)

        form = QFormLayout()
        self.inputs = {}
        for sub in self.marks_mgr.get_configured_subjects():
            cur = str(self.student.marks.get(sub, 0.0))
            inp = QLineEdit(cur)
            self.inputs[sub] = inp
            form.addRow(f"{sub}:", inp)
        layout.addLayout(form)

        btn_box = QHBoxLayout()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.setObjectName("SecondaryButton")
        btn_cancel.clicked.connect(self.reject)

        btn_save = QPushButton("Save Marks")
        btn_save.clicked.connect(self.save_marks)

        btn_box.addWidget(btn_cancel)
        btn_box.addWidget(btn_save)
        layout.addLayout(btn_box)

    def save_marks(self):
        payload = {}
        try:
            for sub, inp in self.inputs.items():
                payload[sub] = float(inp.text().strip())
            self.marks_mgr.update_student_marks(self.student.student_id, payload)
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Validation Error", str(e))