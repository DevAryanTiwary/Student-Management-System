"""
Main Application Desktop Window.
Integrates responsive sidebar, header indicators, view-routing, and shortcut triggers.
Includes a dedicated '+ Add Student' quick action button in the sidebar.
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QStackedWidget, QPushButton, QLabel, QFrame,
    QStatusBar, QMessageBox
)
from PySide6.QtCore import QTimer
from PySide6.QtGui import QKeySequence, QShortcut

from config import (
    APP_NAME, APP_VERSION, DATA_STORAGE_FORMAT,
    SESSION_TIMEOUT_MINUTES, ROLE_SUPER_ADMIN
)
from managers.auth_manager import AuthManager
from managers.student_manager import StudentManager
from managers.marks_manager import MarksManager
from managers.attendance_manager import AttendanceManager
from managers.backup_manager import BackupManager
from managers.export_manager import ExportManager
from services.integrity_service import IntegrityService

from gui.themes import get_theme_qss
from gui.widgets.toast import ToastNotification
from gui.dialogs.global_search_dialog import GlobalSearchDialog
from gui.dialogs.student_wizard import StudentWizardDialog
from gui.views.dashboard_view import DashboardView
from gui.views.students_view import StudentsView
from gui.views.profile_view import StudentProfileView
from gui.views.academics_view import AcademicsView
from gui.views.attendance_view import AttendanceView
from gui.views.reports_view import ReportsView
from gui.views.backup_view import BackupView
from gui.views.audit_view import AuditView
from gui.views.users_view import UsersView
from gui.views.settings_view import SettingsView


class MainWindow(QMainWindow):
    def __init__(
        self,
        auth_mgr: AuthManager,
        student_mgr: StudentManager,
        marks_mgr: MarksManager,
        att_mgr: AttendanceManager,
        backup_mgr: BackupManager,
        export_mgr: ExportManager,
        integrity_svc: IntegrityService,
        theme: str = "dark"
    ):
        super().__init__()
        self.auth_mgr = auth_mgr
        self.student_mgr = student_mgr
        self.marks_mgr = marks_mgr
        self.att_mgr = att_mgr
        self.backup_mgr = backup_mgr
        self.export_mgr = export_mgr
        self.integrity_svc = integrity_svc
        self.theme_name = theme

        self.setWindowTitle(f"{APP_NAME} (v{APP_VERSION})")
        self.resize(1200, 800)
        self.setStyleSheet(get_theme_qss(self.theme_name))

        # Central Root Container
        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # Build UI Structure
        self._build_sidebar(root_layout)
        self._build_content_area(root_layout)
        self._setup_status_bar()
        self._setup_shortcuts()
        self._setup_inactivity_timer()

        # Floating notification toast layer
        self.toast = ToastNotification(self)

    def _build_sidebar(self, parent_layout):
        sidebar = QFrame()
        sidebar.setObjectName("SidebarFrame")
        sidebar.setFixedWidth(230)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(12, 20, 12, 20)
        layout.setSpacing(6)

        # App Logo / Title
        lbl_brand = QLabel("SMS PRO")
        lbl_brand.setStyleSheet("font-size: 18px; font-weight: 800; color: #38BDF8; padding-left: 10px;")
        layout.addWidget(lbl_brand)
        layout.addSpacing(10)

        # Dedicated Add Student Action Button in Sidebar
        btn_quick_add = QPushButton("+ Add Student")
        btn_quick_add.setStyleSheet("""
            background-color: #059669;
            color: #FFFFFF;
            font-weight: 700;
            padding: 10px 18px;
            border-radius: 6px;
            text-align: center;
        """)
        btn_quick_add.clicked.connect(self.open_new_wizard)
        layout.addWidget(btn_quick_add)
        layout.addSpacing(10)

        self.nav_buttons = {}
        routes = [
            ("Dashboard", self.go_dashboard),
            ("Students Directory", self.go_students),
            ("Academics & Marks", self.go_academics),
            ("Attendance Ledger", self.go_attendance),
            ("Report Center", self.go_reports),
            ("Backup & Recovery", self.go_backup),
            ("Activity / Audit", self.go_audit),
            ("Settings & Subjects", self.go_settings),
        ]
        if self.auth_mgr.current_role == ROLE_SUPER_ADMIN:
            routes.append(("User Administration", self.go_users))

        for name, callback in routes:
            btn = QPushButton(name)
            btn.setObjectName("SidebarButton")
            btn.setCheckable(True)
            btn.clicked.connect(callback)
            layout.addWidget(btn)
            self.nav_buttons[name] = btn

        layout.addStretch()

        # Theme Switcher
        btn_theme = QPushButton("Toggle Dark / Light")
        btn_theme.setObjectName("SidebarButton")
        btn_theme.clicked.connect(self.toggle_theme)
        layout.addWidget(btn_theme)

        # Logout Button
        btn_logout = QPushButton("Sign Out")
        btn_logout.setObjectName("DangerButton")
        btn_logout.clicked.connect(self.close)
        layout.addWidget(btn_logout)

        parent_layout.addWidget(sidebar)

    def _build_content_area(self, parent_layout):
        content_frame = QFrame()
        layout = QVBoxLayout(content_frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header Bar
        header = QFrame()
        header.setObjectName("HeaderFrame")
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(16, 8, 16, 8)

        lbl_user = QLabel(f"Authenticated: {self.auth_mgr.current_user} ({self.auth_mgr.current_role})")
        lbl_user.setStyleSheet("font-weight: 600; color: #A0AEC0;")

        btn_spotlight = QPushButton("Quick Search (Ctrl+K)")
        btn_spotlight.setObjectName("SecondaryButton")
        btn_spotlight.clicked.connect(self.open_spotlight)

        h_layout.addWidget(lbl_user)
        h_layout.addStretch()
        h_layout.addWidget(btn_spotlight)
        layout.addWidget(header)

        # Main Page Stack
        self.stack = QStackedWidget()
        self.view_dashboard = DashboardView(self.student_mgr, dark_mode=(self.theme_name == "dark"))
        self.view_students = StudentsView(self.student_mgr, self.marks_mgr, on_view_profile=self.view_student_profile)
        self.view_profile = StudentProfileView(self.student_mgr, on_back=self.go_students)
        self.view_academics = AcademicsView(self.student_mgr, self.marks_mgr)
        self.view_attendance = AttendanceView(self.student_mgr, self.att_mgr)
        self.view_reports = ReportsView(self.student_mgr, self.export_mgr)
        self.view_backup = BackupView(self.backup_mgr, on_backup_restored=self.refresh_all_views)
        self.view_audit = AuditView()
        self.view_settings = SettingsView(self.marks_mgr)

        self.stack.addWidget(self.view_dashboard)   # 0
        self.stack.addWidget(self.view_students)    # 1
        self.stack.addWidget(self.view_profile)     # 2
        self.stack.addWidget(self.view_academics)   # 3
        self.stack.addWidget(self.view_attendance)  # 4
        self.stack.addWidget(self.view_reports)     # 5
        self.stack.addWidget(self.view_backup)      # 6
        self.stack.addWidget(self.view_audit)       # 7
        self.stack.addWidget(self.view_settings)    # 8

        if self.auth_mgr.current_role == ROLE_SUPER_ADMIN:
            self.view_users = UsersView(self.auth_mgr)
            self.stack.addWidget(self.view_users)   # 9

        layout.addWidget(self.stack)
        parent_layout.addWidget(content_frame)

        self.go_dashboard()

    def _setup_status_bar(self):
        sb = QStatusBar()
        self.setStatusBar(sb)
        total_s = len(self.student_mgr.get_all_students())
        sb.showMessage(f"Ready | Storage: {DATA_STORAGE_FORMAT} | Active Students: {total_s} | System Status: Optimal")

    def _setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+K"), self, self.open_spotlight)
        QShortcut(QKeySequence("Ctrl+N"), self, self.open_new_wizard)
        QShortcut(QKeySequence("Ctrl+R"), self, self.refresh_all_views)

    def _setup_inactivity_timer(self):
        self.inactivity_timer = QTimer(self)
        self.inactivity_timer.setInterval(SESSION_TIMEOUT_MINUTES * 60 * 1000)
        self.inactivity_timer.timeout.connect(self.handle_session_timeout)
        self.inactivity_timer.start()

    def handle_session_timeout(self):
        self.inactivity_timer.stop()
        QMessageBox.warning(self, "Session Expired", "Your session has expired due to inactivity. Please sign in again.")
        self.close()

    def open_spotlight(self):
        dlg = GlobalSearchDialog(self.student_mgr, on_select_callback=self.view_student_profile, parent=self)
        dlg.exec()

    def open_new_wizard(self):
        wiz = StudentWizardDialog(self.student_mgr, self.marks_mgr, parent=self)
        if wiz.exec() == StudentWizardDialog.Accepted:
            self.refresh_all_views()
            self.toast.show_message("Student enrolled successfully.")

    def view_student_profile(self, student_id: str):
        self.view_profile.load_student(student_id)
        self.stack.setCurrentIndex(2)

    def go_dashboard(self):
        self._select_nav("Dashboard")
        self.view_dashboard.refresh_metrics()
        self.stack.setCurrentIndex(0)

    def go_students(self):
        self._select_nav("Students Directory")
        self.view_students.reload_data()
        self.stack.setCurrentIndex(1)

    def go_academics(self):
        self._select_nav("Academics & Marks")
        self.view_academics.load_data()
        self.stack.setCurrentIndex(3)

    def go_attendance(self):
        self._select_nav("Attendance Ledger")
        self.view_attendance.load_data()
        self.stack.setCurrentIndex(4)

    def go_reports(self):
        self._select_nav("Report Center")
        self.view_reports.generate_class_summary()
        self.stack.setCurrentIndex(5)

    def go_backup(self):
        self._select_nav("Backup & Recovery")
        self.view_backup.load_backups()
        self.stack.setCurrentIndex(6)

    def go_audit(self):
        self._select_nav("Activity / Audit")
        self.view_audit.load_logs()
        self.stack.setCurrentIndex(7)

    def go_settings(self):
        self._select_nav("Settings & Subjects")
        self.view_settings.render_subjects()
        self.stack.setCurrentIndex(8)

    def go_users(self):
        if hasattr(self, 'view_users'):
            self._select_nav("User Administration")
            self.view_users.reload_users()
            self.stack.setCurrentIndex(9)

    def _select_nav(self, active_name: str):
        for name, btn in self.nav_buttons.items():
            btn.setChecked(name == active_name)

    def toggle_theme(self):
        self.theme_name = "light" if self.theme_name == "dark" else "dark"
        self.setStyleSheet(get_theme_qss(self.theme_name))
        self.toast.show_message(f"Switched to {self.theme_name.capitalize()} Mode")

    def refresh_all_views(self):
        self.view_dashboard.refresh_metrics()
        self.view_students.reload_data()
        self.view_academics.load_data()
        self.view_attendance.load_data()
        total_s = len(self.student_mgr.get_all_students())
        self.statusBar().showMessage(f"Refreshed | Storage: {DATA_STORAGE_FORMAT} | Active Students: {total_s} | System Status: Optimal")