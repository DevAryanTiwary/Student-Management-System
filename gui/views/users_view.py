from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLineEdit, QComboBox,
    QHeaderView, QMessageBox, QLabel
)
from managers.auth_manager import AuthManager
from config import ALL_ROLES

class UsersView(QWidget):
    def __init__(self, auth_mgr: AuthManager, parent=None):
        super().__init__(parent)
        self.auth_mgr = auth_mgr

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        lbl_head = QLabel("User Management & Authentication Permissions")
        lbl_head.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(lbl_head)

        create_bar = QHBoxLayout()
        self.txt_new_user = QLineEdit()
        self.txt_new_user.setPlaceholderText("New Username")
        self.txt_new_pass = QLineEdit()
        self.txt_new_pass.setPlaceholderText("Password (min 8 chars)")
        self.cmb_role = QComboBox()
        self.cmb_role.addItems(ALL_ROLES)
        self.btn_create = QPushButton("+ Create User")
        self.btn_create.clicked.connect(self.create_user)

        create_bar.addWidget(self.txt_new_user)
        create_bar.addWidget(self.txt_new_pass)
        create_bar.addWidget(self.cmb_role)
        create_bar.addWidget(self.btn_create)
        layout.addLayout(create_bar)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Username", "Role", "Locked?", "Enabled?", "Actions", ""])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.reload_users()

    def reload_users(self):
        users = self.auth_mgr.list_users()
        self.table.setRowCount(len(users))
        for r, u in enumerate(users):
            self.table.setItem(r, 0, QTableWidgetItem(u["username"]))
            self.table.setItem(r, 1, QTableWidgetItem(u["role"]))
            self.table.setItem(r, 2, QTableWidgetItem("YES (Locked)" if u["is_locked"] else "No"))
            self.table.setItem(r, 3, QTableWidgetItem("Active" if u["is_enabled"] else "Disabled"))

            btn_unlock = QPushButton("Unlock")
            btn_unlock.setObjectName("SecondaryButton")
            btn_unlock.setEnabled(u["is_locked"])
            btn_unlock.clicked.connect(lambda _, uname=u["username"]: self.unlock(uname))
            self.table.setCellWidget(r, 4, btn_unlock)

            btn_toggle = QPushButton("Disable" if u["is_enabled"] else "Enable")
            btn_toggle.setObjectName("DangerButton" if u["is_enabled"] else "SecondaryButton")
            btn_toggle.clicked.connect(lambda _, uname=u["username"], status=u["is_enabled"]: self.toggle_user(uname, not status))
            self.table.setCellWidget(r, 5, btn_toggle)

    def create_user(self):
        uname = self.txt_new_user.text().strip()
        pwd = self.txt_new_pass.text()
        role = self.cmb_role.currentText()
        try:
            self.auth_mgr.create_user(uname, pwd, role)
            QMessageBox.information(self, "Success", f"User '{uname}' provisioned successfully.")
            self.txt_new_user.clear()
            self.txt_new_pass.clear()
            self.reload_users()
        except Exception as e:
            QMessageBox.critical(self, "Failed", str(e))

    def unlock(self, username: str):
        self.auth_mgr.unlock_account(username)
        QMessageBox.information(self, "Unlocked", f"Account '{username}' unlocked.")
        self.reload_users()

    def toggle_user(self, username: str, new_status: bool):
        try:
            self.auth_mgr.toggle_user_enabled(username, new_status)
            self.reload_users()
        except Exception as e:
            QMessageBox.warning(self, "Action Denied", str(e))