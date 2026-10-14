from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QPushButton, QLabel, QMessageBox
)
from managers.backup_manager import BackupManager

class BackupView(QWidget):
    def __init__(self, backup_mgr: BackupManager, on_backup_restored, parent=None):
        super().__init__(parent)
        self.backup_mgr = backup_mgr
        self.on_backup_restored = on_backup_restored

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        lbl_head = QLabel("Backup Snapshots & Data Recovery Center")
        lbl_head.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(lbl_head)

        lbl_sub = QLabel("Create isolated point-in-time snapshots of the database or restore from prior archives.")
        lbl_sub.setStyleSheet("color: #A0AEC0;")
        layout.addWidget(lbl_sub)

        btn_bar = QHBoxLayout()
        self.btn_create = QPushButton("+ Create New Backup Snapshot")
        self.btn_create.clicked.connect(self.create_snapshot)

        self.btn_restore = QPushButton("Restore Selected Backup")
        self.btn_restore.setObjectName("DangerButton")
        self.btn_restore.clicked.connect(self.restore_snapshot)

        self.btn_refresh = QPushButton("Refresh List")
        self.btn_refresh.setObjectName("SecondaryButton")
        self.btn_refresh.clicked.connect(self.load_backups)

        btn_bar.addWidget(self.btn_create)
        btn_bar.addWidget(self.btn_restore)
        btn_bar.addWidget(self.btn_refresh)
        btn_bar.addStretch()
        layout.addLayout(btn_bar)

        self.backup_list = QListWidget()
        layout.addWidget(self.backup_list)

        self.load_backups()

    def load_backups(self):
        self.backup_list.clear()
        backups = self.backup_mgr.list_backups()
        for b in backups:
            self.backup_list.addItem(b)

    def create_snapshot(self):
        try:
            b_name = self.backup_mgr.create_backup()
            QMessageBox.information(self, "Backup Successful", f"Created snapshot archive:\n{b_name}")
            self.load_backups()
        except Exception as e:
            QMessageBox.critical(self, "Backup Failed", str(e))

    def restore_snapshot(self):
        curr = self.backup_list.currentItem()
        if not curr:
            QMessageBox.warning(self, "Notice", "Please select a backup from the list to restore.")
            return

        b_name = curr.text()
        conf = QMessageBox.warning(
            self,
            "Confirm Overwrite",
            f"Are you sure you want to rollback the database to snapshot:\n{b_name}?\n\nCurrent unsaved data will be replaced.",
            QMessageBox.Yes | QMessageBox.No
        )
        if conf == QMessageBox.Yes:
            try:
                self.backup_mgr.restore_backup(b_name)
                QMessageBox.information(self, "Restored", "Data state restored successfully.")
                self.on_backup_restored()
            except Exception as e:
                QMessageBox.critical(self, "Restore Failed", str(e))