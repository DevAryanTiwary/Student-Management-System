"""
Professional Modal Authentication Dialog.
Configured with explicit contrast styling to remain readable across all platforms.
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from managers.auth_manager import AuthManager
from utils.exceptions import AuthenticationError, AccountLockedError

class LoginDialog(QDialog):
    def __init__(self, auth_mgr: AuthManager, parent=None):
        super().__init__(parent)
        self.auth_mgr = auth_mgr
        self.setWindowTitle("System Authentication — Student Management System")
        self.setFixedSize(420, 360)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        # Explicit dark modal palette
        self.setStyleSheet("""
            QDialog {
                background-color: #0F172A;
            }
            QLabel {
                color: #F8FAFC;
                font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            }
            QLineEdit {
                background-color: #1E293B;
                border: 1px solid #475569;
                border-radius: 6px;
                padding: 9px 12px;
                color: #FFFFFF;
                font-size: 13px;
                selection-background-color: #2563EB;
            }
            QLineEdit:focus {
                border: 1px solid #38BDF8;
                background-color: #0F172A;
            }
            QPushButton {
                background-color: #2563EB;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
            QPushButton:pressed {
                background-color: #1E40AF;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(10)

        lbl_head = QLabel("Welcome Back")
        lbl_head.setStyleSheet("font-size: 22px; font-weight: 700; color: #38BDF8;")
        
        lbl_sub = QLabel("Please authenticate with your administrator credentials.")
        lbl_sub.setStyleSheet("font-size: 12px; color: #94A3B8; margin-bottom: 8px;")
        lbl_sub.setWordWrap(True)

        layout.addWidget(lbl_head)
        layout.addWidget(lbl_sub)

        lbl_user = QLabel("Username")
        lbl_user.setStyleSheet("font-weight: 600; font-size: 12px; color: #E2E8F0;")
        self.txt_user = QLineEdit()
        self.txt_user.setPlaceholderText("Enter username (e.g. admin)")

        lbl_pass = QLabel("Password")
        lbl_pass.setStyleSheet("font-weight: 600; font-size: 12px; color: #E2E8F0;")
        self.txt_pass = QLineEdit()
        self.txt_pass.setPlaceholderText("Enter password")
        self.txt_pass.setEchoMode(QLineEdit.Password)

        layout.addWidget(lbl_user)
        layout.addWidget(self.txt_user)
        layout.addWidget(lbl_pass)
        layout.addWidget(self.txt_pass)
        layout.addSpacing(8)

        self.btn_login = QPushButton("Log In")
        self.btn_login.setDefault(True)
        self.btn_login.clicked.connect(self.handle_login)
        layout.addWidget(self.btn_login)

    def handle_login(self):
        user = self.txt_user.text().strip()
        pwd = self.txt_pass.text()
        if not user or not pwd:
            QMessageBox.warning(self, "Validation Error", "Please provide both username and password.")
            return

        try:
            self.auth_mgr.login(user, pwd)
            self.accept()
        except AccountLockedError as e:
            QMessageBox.critical(self, "Account Locked", str(e))
        except AuthenticationError as e:
            QMessageBox.warning(self, "Authentication Failed", str(e))
            self.txt_pass.clear()
            self.txt_pass.setFocus()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Unexpected error during authentication: {e}")