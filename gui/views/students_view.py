from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLineEdit, QComboBox,
    QLabel, QHeaderView
)
from managers.student_manager import StudentManager
from managers.search_sort_manager import SearchSortManager
from gui.dialogs.student_wizard import StudentWizardDialog
from managers.marks_manager import MarksManager

class StudentsView(QWidget):
    def __init__(self, student_mgr: StudentManager, marks_mgr: MarksManager, on_view_profile, parent=None):
        super().__init__(parent)
        self.student_mgr = student_mgr
        self.marks_mgr = marks_mgr
        self.on_view_profile = on_view_profile
        self.current_page = 1
        self.page_size = 12

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        top_bar = QHBoxLayout()
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Search by Name, ID, Course, Email... (Ctrl+F)")
        self.txt_search.textChanged.connect(self.apply_filter)

        self.cmb_grade = QComboBox()
        self.cmb_grade.addItems(["All Grades", "A+", "A", "B+", "B", "C", "D", "F"])
        self.cmb_grade.currentIndexChanged.connect(self.apply_filter)

        self.btn_add = QPushButton("+ Add Student")
        self.btn_add.clicked.connect(self.open_add_wizard)

        top_bar.addWidget(self.txt_search, 3)
        top_bar.addWidget(self.cmb_grade, 1)
        top_bar.addWidget(self.btn_add, 1)
        layout.addLayout(top_bar)

        self.table = QTableWidget()
        self.headers = ["ID", "Name", "Course", "Class", "Attendance", "Total", "%", "Grade", "Status", "Actions"]
        self.table.setColumnCount(len(self.headers))
        self.table.setHorizontalHeaderLabels(self.headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.cellDoubleClicked.connect(self.row_double_clicked)
        layout.addWidget(self.table)

        bot_bar = QHBoxLayout()
        self.lbl_stats = QLabel("Showing 0 students")
        self.btn_prev = QPushButton("◀ Previous")
        self.btn_prev.setObjectName("SecondaryButton")
        self.btn_prev.clicked.connect(self.prev_page)
        self.btn_next = QPushButton("Next ▶")
        self.btn_next.setObjectName("SecondaryButton")
        self.btn_next.clicked.connect(self.next_page)

        bot_bar.addWidget(self.lbl_stats)
        bot_bar.addStretch()
        bot_bar.addWidget(self.btn_prev)
        bot_bar.addWidget(self.btn_next)
        layout.addLayout(bot_bar)

        self.filtered_cache = []
        self.reload_data()

    def reload_data(self):
        self.apply_filter()

    def apply_filter(self):
        query = self.txt_search.text().strip()
        selected_grade = self.cmb_grade.currentText()
        grade_filter = None if selected_grade == "All Grades" else selected_grade

        students = self.student_mgr.get_all_students()
        results = SearchSortManager.search(students, query, "all")
        if grade_filter:
            results = SearchSortManager.filter_students(results, grade=grade_filter)

        self.filtered_cache = results
        self.current_page = 1
        self.render_page()

    def render_page(self):
        total_items = len(self.filtered_cache)
        total_pages = max(1, (total_items + self.page_size - 1) // self.page_size)
        start = (self.current_page - 1) * self.page_size
        page_items = self.filtered_cache[start:start + self.page_size]

        self.table.setRowCount(len(page_items))
        for r_idx, s in enumerate(page_items):
            self.table.setItem(r_idx, 0, QTableWidgetItem(s.student_id))
            self.table.setItem(r_idx, 1, QTableWidgetItem(s.name))
            self.table.setItem(r_idx, 2, QTableWidgetItem(s.course))
            self.table.setItem(r_idx, 3, QTableWidgetItem(s.class_year))
            self.table.setItem(r_idx, 4, QTableWidgetItem(f"{s.attendance_percentage}%"))
            self.table.setItem(r_idx, 5, QTableWidgetItem(f"{s.total_marks}"))
            self.table.setItem(r_idx, 6, QTableWidgetItem(f"{s.percentage}%"))
            self.table.setItem(r_idx, 7, QTableWidgetItem(s.grade))
            self.table.setItem(r_idx, 8, QTableWidgetItem(s.pass_status))

            btn_view = QPushButton("View")
            btn_view.setObjectName("SecondaryButton")
            btn_view.clicked.connect(lambda _, sid=s.student_id: self.on_view_profile(sid))
            self.table.setCellWidget(r_idx, 9, btn_view)

        self.lbl_stats.setText(f"Showing {len(page_items)} of {total_items} students (Page {self.current_page}/{total_pages})")
        self.btn_prev.setEnabled(self.current_page > 1)
        self.btn_next.setEnabled(self.current_page < total_pages)

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.render_page()

    def next_page(self):
        total_pages = (len(self.filtered_cache) + self.page_size - 1) // self.page_size
        if self.current_page < total_pages:
            self.current_page += 1
            self.render_page()

    def row_double_clicked(self, row, col):
        item = self.table.item(row, 0)
        if item:
            self.on_view_profile(item.text())

    def open_add_wizard(self):
        wiz = StudentWizardDialog(self.student_mgr, self.marks_mgr, self)
        if wiz.exec() == StudentWizardDialog.Accepted:
            self.reload_data()