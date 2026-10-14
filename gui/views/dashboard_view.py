from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from gui.widgets.stat_card import StatCard
from gui.widgets.chart_view import ChartView
from managers.student_manager import StudentManager
from managers.report_manager import ReportManager
from config import MIN_ATTENDANCE_PERCENT

class DashboardView(QWidget):
    def __init__(self, student_mgr: StudentManager, dark_mode: bool = True, parent=None):
        super().__init__(parent)
        self.student_mgr = student_mgr
        self.dark_mode = dark_mode

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        lbl_head = QLabel("System Dashboard & Cohort Analytics")
        lbl_head.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(lbl_head)

        kpi_layout = QHBoxLayout()
        self.card_total = StatCard("Total Students", "0", "Enrolled Cohort")
        self.card_avg = StatCard("Class Average", "0.0%", "Across All Subjects")
        self.card_att = StatCard("Average Attendance", "0.0%", f"Requirement: {MIN_ATTENDANCE_PERCENT}%")
        self.card_topper = StatCard("Cohort Topper", "N/A", "Top Academic Performer")

        kpi_layout.addWidget(self.card_total)
        kpi_layout.addWidget(self.card_avg)
        kpi_layout.addWidget(self.card_att)
        kpi_layout.addWidget(self.card_topper)
        layout.addLayout(kpi_layout)

        chart_layout = QHBoxLayout()
        self.chart_grades = ChartView(dark_mode=self.dark_mode)
        self.chart_subjects = ChartView(dark_mode=self.dark_mode)
        chart_layout.addWidget(self.chart_grades)
        chart_layout.addWidget(self.chart_subjects)
        layout.addLayout(chart_layout)

        self.refresh_metrics()

    def refresh_metrics(self):
        students = self.student_mgr.get_all_students()
        rm = ReportManager(students)
        summary = rm.get_class_performance_summary()

        total = len(students)
        avg_pct = summary.get("average_percentage", 0.0)
        topper = summary.get("topper", "N/A")
        att_avg = summary.get("attendance", {}).get("avg_att", 0.0)

        self.card_total.update_value(str(total), f"{total} Active Records")
        self.card_avg.update_value(f"{avg_pct}%", "Cohort Overall")
        self.card_att.update_value(f"{att_avg}%", f"Min Target: {MIN_ATTENDANCE_PERCENT}%")
        self.card_topper.update_value(topper.split()[0] if topper != "N/A" else "N/A", topper)

        dist = rm.generate_grade_distribution()
        labels = [g for g, cnt in dist.items() if cnt > 0]
        vals = [cnt for cnt in dist.values() if cnt > 0]
        self.chart_grades.render_pie(labels, vals, "Grade Scale Distribution")

        sub_analysis = rm.generate_subject_wise_analysis()
        s_labels = list(sub_analysis.keys())
        s_vals = [v["avg"] for v in sub_analysis.values()]
        self.chart_subjects.render_bar(s_labels, s_vals, "Average Score per Subject", ylabel="Marks (out of 100)")