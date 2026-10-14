from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QListWidget,
    QListWidgetItem, QLabel
)
from PySide6.QtCore import Qt
from managers.student_manager import StudentManager
from managers.search_sort_manager import SearchSortManager

class GlobalSearchDialog(QDialog):
    def __init__(self, student_mgr: StudentManager, on_select_callback, parent=None):
        super().__init__(parent)
        self.student_mgr = student_mgr
        self.on_select_callback = on_select_callback
        self.setWindowTitle("Spotlight Search — Students")
        self.setFixedSize(540, 400)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search students by ID, Name, Course, Class... (Esc to close)")
        self.search_input.setStyleSheet("font-size: 15px; padding: 10px;")
        self.search_input.textChanged.connect(self.do_search)

        self.results_list = QListWidget()
        self.results_list.itemDoubleClicked.connect(self.item_selected)

        self.lbl_status = QLabel("Type to begin search...")
        self.lbl_status.setStyleSheet("color: #718096; font-size: 11px;")

        layout.addWidget(self.search_input)
        layout.addWidget(self.results_list)
        layout.addWidget(self.lbl_status)

        self.all_students = self.student_mgr.get_all_students()

    def do_search(self, query: str):
        self.results_list.clear()
        q = query.strip()
        if not q:
            self.lbl_status.setText("Type to begin search...")
            return

        matches = SearchSortManager.search(self.all_students, q, "all")
        self.lbl_status.setText(f"Found {len(matches)} matching students.")

        for s in matches[:30]:
            item = QListWidgetItem(f"[{s.student_id}] {s.name}  —  {s.course} ({s.class_year})  |  Grade: {s.grade}")
            item.setData(Qt.UserRole, s.student_id)
            self.results_list.addItem(item)

    def item_selected(self, item: QListWidgetItem):
        sid = item.data(Qt.UserRole)
        if sid and self.on_select_callback:
            self.on_select_callback(sid)
            self.accept()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.reject()
        elif event.key() == Qt.Key_Return and self.results_list.currentItem():
            self.item_selected(self.results_list.currentItem())
        else:
            super().keyPressEvent(event)