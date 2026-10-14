from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QStackedWidget,
    QWidget, QLabel, QLineEdit, QComboBox, QSpinBox,
    QPushButton, QMessageBox, QFormLayout, QTextEdit
)
from managers.student_manager import StudentManager
from managers.marks_manager import MarksManager
from utils.validators import (
    validate_student_id, validate_name, validate_age,
    validate_gender, validate_email, validate_phone,
    validate_date, validate_marks, validate_attendance
)
from utils.exceptions import ValidationError, DuplicateStudentError

class StudentWizardDialog(QDialog):
    def __init__(self, student_mgr: StudentManager, marks_mgr: MarksManager, parent=None):
        super().__init__(parent)
        self.student_mgr = student_mgr
        self.marks_mgr = marks_mgr
        self.setWindowTitle("Enroll New Student — Step-by-Step Wizard")
        self.setFixedSize(540, 500)

        main_layout = QVBoxLayout(self)
        self.step_label = QLabel("Step 1 of 5: Personal Profile")
        self.step_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #63B3ED;")
        main_layout.addWidget(self.step_label)

        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        self._build_step_1_personal()
        self._build_step_2_contact()
        self._build_step_3_academic()
        self._build_step_4_marks()
        self._build_step_5_review()

        nav_layout = QHBoxLayout()
        self.btn_prev = QPushButton("Previous")
        self.btn_prev.setObjectName("SecondaryButton")
        self.btn_prev.clicked.connect(self.prev_step)
        self.btn_prev.setEnabled(False)

        self.btn_next = QPushButton("Next")
        self.btn_next.clicked.connect(self.next_step)

        nav_layout.addWidget(self.btn_prev)
        nav_layout.addStretch()
        nav_layout.addWidget(self.btn_next)
        main_layout.addLayout(nav_layout)

    def _build_step_1_personal(self):
        w = QWidget()
        form = QFormLayout(w)
        self.txt_id = QLineEdit(self.student_mgr.generate_next_student_id())
        self.txt_name = QLineEdit()
        self.spn_age = QSpinBox()
        self.spn_age.setRange(14, 100)
        self.spn_age.setValue(20)
        self.cmb_gender = QComboBox()
        self.cmb_gender.addItems(["Male", "Female", "Other", "Prefer not to say"])
        self.txt_dob = QLineEdit("2006-01-15")

        form.addRow("Student ID*:", self.txt_id)
        form.addRow("Full Name*:", self.txt_name)
        form.addRow("Age*:", self.spn_age)
        form.addRow("Gender*:", self.cmb_gender)
        form.addRow("Date of Birth (YYYY-MM-DD)*:", self.txt_dob)
        self.stack.addWidget(w)

    def _build_step_2_contact(self):
        w = QWidget()
        form = QFormLayout(w)
        self.txt_email = QLineEdit()
        self.txt_phone = QLineEdit("+91")
        self.txt_address = QLineEdit("Campus Housing")

        form.addRow("Email Address*:", self.txt_email)
        form.addRow("Phone Number*:", self.txt_phone)
        form.addRow("Residential Address:", self.txt_address)
        self.stack.addWidget(w)

    def _build_step_3_academic(self):
        w = QWidget()
        form = QFormLayout(w)
        self.txt_class = QLineEdit("Year-1")
        self.txt_course = QLineEdit("Computer Science")
        self.txt_adm_date = QLineEdit("2026-08-01")
        self.spn_attended = QSpinBox()
        self.spn_attended.setRange(0, 500)
        self.spn_total_classes = QSpinBox()
        self.spn_total_classes.setRange(0, 500)
        self.spn_total_classes.setValue(90)
        self.spn_attended.setValue(80)

        form.addRow("Class / Year*:", self.txt_class)
        form.addRow("Course Title*:", self.txt_course)
        form.addRow("Admission Date (YYYY-MM-DD)*:", self.txt_adm_date)
        form.addRow("Classes Attended*:", self.spn_attended)
        form.addRow("Total Classes Held*:", self.spn_total_classes)
        self.stack.addWidget(w)

    def _build_step_4_marks(self):
        w = QWidget()
        self.marks_form = QFormLayout(w)
        self.subject_inputs = {}
        for sub in self.marks_mgr.get_configured_subjects():
            inp = QLineEdit("85.0")
            self.subject_inputs[sub] = inp
            self.marks_form.addRow(f"{sub} (0-100):", inp)
        self.stack.addWidget(w)

    def _build_step_5_review(self):
        w = QWidget()
        layout = QVBoxLayout(w)
        self.txt_review = QTextEdit()
        self.txt_review.setReadOnly(True)
        layout.addWidget(QLabel("Please confirm the student profile details:"))
        layout.addWidget(self.txt_review)
        self.stack.addWidget(w)

    def next_step(self):
        idx = self.stack.currentIndex()
        try:
            if idx == 0:
                validate_student_id(self.txt_id.text())
                validate_name(self.txt_name.text())
                validate_age(self.spn_age.value())
                validate_date(self.txt_dob.text(), "Date of Birth")
            elif idx == 1:
                validate_email(self.txt_email.text())
                validate_phone(self.txt_phone.text())
            elif idx == 2:
                validate_date(self.txt_adm_date.text(), "Admission Date")
                validate_attendance(self.spn_attended.value(), self.spn_total_classes.value())
            elif idx == 3:
                for sub, inp in self.subject_inputs.items():
                    validate_marks(inp.text())
                self._populate_review()

            if idx < 4:
                self.stack.setCurrentIndex(idx + 1)
                self.btn_prev.setEnabled(True)
                if idx + 1 == 4:
                    self.btn_next.setText("Finish & Save")
            else:
                self._save_student()
        except ValidationError as err:
            QMessageBox.warning(self, "Validation Notice", str(err))

        self._update_step_title()

    def prev_step(self):
        idx = self.stack.currentIndex()
        if idx > 0:
            self.stack.setCurrentIndex(idx - 1)
            self.btn_next.setText("Next")
            if idx - 1 == 0:
                self.btn_prev.setEnabled(False)
        self._update_step_title()

    def _update_step_title(self):
        titles = [
            "Step 1 of 5: Personal Profile",
            "Step 2 of 5: Contact Details",
            "Step 3 of 5: Academic & Attendance",
            "Step 4 of 5: Initial Subject Marks",
            "Step 5 of 5: Review & Save"
        ]
        self.step_label.setText(titles[self.stack.currentIndex()])

    def _populate_review(self):
        lines = [
            f"Student ID : {self.txt_id.text()}",
            f"Name       : {self.txt_name.text()}",
            f"Course     : {self.txt_course.text()} ({self.txt_class.text()})",
            f"Email      : {self.txt_email.text()}",
            f"Attendance : {self.spn_attended.value()} / {self.spn_total_classes.value()}",
            "Marks:"
        ]
        for sub, inp in self.subject_inputs.items():
            lines.append(f"  * {sub}: {inp.text()}")
        self.txt_review.setText("\n".join(lines))

    def _save_student(self):
        marks_dict = {sub: float(inp.text()) for sub, inp in self.subject_inputs.items()}
        payload = {
            "student_id": self.txt_id.text(),
            "name": self.txt_name.text(),
            "age": self.spn_age.value(),
            "gender": self.cmb_gender.currentText(),
            "class_year": self.txt_class.text(),
            "course": self.txt_course.text(),
            "email": self.txt_email.text(),
            "phone": self.txt_phone.text(),
            "dob": self.txt_dob.text(),
            "address": self.txt_address.text(),
            "admission_date": self.txt_adm_date.text(),
            "classes_attended": self.spn_attended.value(),
            "total_classes": self.spn_total_classes.value(),
            "marks": marks_dict
        }
        try:
            self.student_mgr.add_student(payload)
            self.accept()
        except DuplicateStudentError as e:
            QMessageBox.critical(self, "Conflict", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to persist student: {e}")