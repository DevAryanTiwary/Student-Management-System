from PySide6.QtWidgets import QLabel, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation

class ToastNotification(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.SubWindow | Qt.FramelessWindowHint)
        self.setStyleSheet("""
            background-color: #2B6CB0;
            color: #FFFFFF;
            font-weight: 600;
            padding: 10px 20px;
            border-radius: 6px;
        """)
        self.setAlignment(Qt.AlignCenter)
        self.opacity = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity)
        self.hide()

    def show_message(self, text: str, is_error: bool = False, duration_ms: int = 3000):
        color = "#C53030" if is_error else "#2B6CB0"
        self.setStyleSheet(f"""
            background-color: {color};
            color: #FFFFFF;
            font-weight: 600;
            padding: 10px 20px;
            border-radius: 6px;
        """)
        self.setText(text)
        self.adjustSize()
        if self.parent():
            p_width = self.parent().width()
            self.move((p_width - self.width()) // 2, 60)
        self.show()
        QTimer.singleShot(duration_ms, self._fade_out)

    def _fade_out(self):
        anim = QPropertyAnimation(self.opacity, b"opacity")
        anim.setDuration(400)
        anim.setStartValue(1.0)
        anim.setEndValue(0.0)
        anim.finished.connect(self.hide)
        anim.start()