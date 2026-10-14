"""
GUI Application Bootstrapper.
Applies the global design system stylesheet at the QApplication level so all
dialogs (including LoginDialog) inherit correct background and text colors.
"""
import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from config import DATA_STORAGE_FORMAT, STUDENTS_CSV_FILE, STUDENTS_JSON_FILE, DEFAULT_THEME
from storage.csv_storage import CSVStorage
from storage.json_storage import JSONStorage
from managers.auth_manager import AuthManager
from managers.student_manager import StudentManager
from managers.marks_manager import MarksManager
from managers.attendance_manager import AttendanceManager
from managers.backup_manager import BackupManager
from managers.export_manager import ExportManager
from services.integrity_service import IntegrityService
from gui.themes import get_theme_qss
from gui.dialogs.login_dialog import LoginDialog
from gui.main_window import MainWindow

def launch_gui() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Student Management System Pro")

    # Apply global stylesheet to the whole application
    app.setStyleSheet(get_theme_qss(DEFAULT_THEME))

    storage = CSVStorage(STUDENTS_CSV_FILE) if DATA_STORAGE_FORMAT.upper() == "CSV" else JSONStorage(STUDENTS_JSON_FILE)

    auth_mgr = AuthManager()
    student_mgr = StudentManager(storage, "System")
    marks_mgr = MarksManager(storage, "System")
    att_mgr = AttendanceManager(storage, "System")
    backup_mgr = BackupManager("System")
    export_mgr = ExportManager("System")
    integrity_svc = IntegrityService(storage)

    # Diagnostic health check
    health = integrity_svc.perform_system_health_check()
    if health["status"] == "CRITICAL":
        QMessageBox.critical(None, "Startup Failure", f"Critical errors encountered during startup:\n{', '.join(health['issues'])}")
        return 1

    # Authentication Gateway Dialog
    login_dlg = LoginDialog(auth_mgr)
    if login_dlg.exec() != LoginDialog.Accepted:
        return 0

    # Launch Primary Window
    window = MainWindow(
        auth_mgr, student_mgr, marks_mgr, att_mgr,
        backup_mgr, export_mgr, integrity_svc,
        theme=DEFAULT_THEME
    )
    window.show()
    return app.exec()