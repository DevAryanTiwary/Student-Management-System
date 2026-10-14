from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class StatCard(QWidget):
    def __init__(self, title: str, value: str, subtext: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("CardWidget")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(4)

        self.lbl_title = QLabel(title.upper())
        self.lbl_title.setStyleSheet("color: #A0AEC0; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;")

        self.lbl_val = QLabel(value)
        self.lbl_val.setStyleSheet("font-size: 24px; font-weight: 700; color: #63B3ED;")

        self.lbl_sub = QLabel(subtext)
        self.lbl_sub.setStyleSheet("font-size: 11px; color: #718096;")

        layout.addWidget(self.lbl_title)
        layout.addWidget(self.lbl_val)
        if subtext:
            layout.addWidget(self.lbl_sub)

    def update_value(self, value: str, subtext: str = ""):
        self.lbl_val.setText(value)
        if subtext:
            self.lbl_sub.setText(subtext)