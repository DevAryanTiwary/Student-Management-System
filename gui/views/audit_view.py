from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QPushButton, QLabel, QLineEdit
)
from utils.logger import read_recent_logs

class AuditView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        lbl = QLabel("System Activity & Audit Trail")
        lbl.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(lbl)

        btn_bar = QHBoxLayout()
        self.txt_filter = QLineEdit()
        self.txt_filter.setPlaceholderText("Filter logs by user, action, or date...")
        self.txt_filter.textChanged.connect(self.filter_logs)

        btn_refresh = QPushButton("Refresh Logs")
        btn_refresh.clicked.connect(self.load_logs)

        btn_bar.addWidget(self.txt_filter)
        btn_bar.addWidget(btn_refresh)
        layout.addLayout(btn_bar)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.raw_logs = []
        self.load_logs()

    def load_logs(self):
        self.raw_logs = read_recent_logs(100)
        self.filter_logs()

    def filter_logs(self):
        self.list_widget.clear()
        q = self.txt_filter.text().strip().lower()
        for line in reversed(self.raw_logs):
            if not q or q in line.lower():
                self.list_widget.addItem(line.strip())