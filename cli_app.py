"""
Command Line Interface Engine for the Student Management System.
Preserves 100% of CLI capabilities with zero regressions.
"""
import sys
import getpass
from config import (
    DATA_STORAGE_FORMAT,
    STUDENTS_CSV_FILE,
    STUDENTS_JSON_FILE,
    MIN_ATTENDANCE_PERCENT
)
from storage.csv_storage import CSVStorage
from storage.json_storage import JSONStorage
from managers.auth_manager import AuthManager
from managers.student_manager import StudentManager
from managers.marks_manager import MarksManager
from managers.attendance_manager import AttendanceManager
from managers.search_sort_manager import SearchSortManager
from managers.report_manager import ReportManager
from managers.backup_manager import BackupManager
from managers.export_manager import ExportManager
from utils.exceptions import SMSException
from utils.helpers import (
    clear_screen,
    print_header,
    print_separator,
    print_success,
    print_error,
    print_table
)
from utils.logger import read_recent_logs

class StudentManagementCLI:
    def __init__(self):
        if DATA_STORAGE_FORMAT.upper() == "CSV":
            self.storage = CSVStorage(STUDENTS_CSV_FILE)
        else:
            self.storage = JSONStorage(STUDENTS_JSON_FILE)

        self.auth_mgr = AuthManager()
        self.backup_mgr = BackupManager()
        self.export_mgr = ExportManager()

    @property
    def student_mgr(self) -> StudentManager:
        return StudentManager(self.storage, self.auth_mgr.current_user or "Admin")

    @property
    def marks_mgr(self) -> MarksManager:
        return MarksManager(self.storage, self.auth_mgr.current_user or "Admin")

    @property
    def att_mgr(self) -> AttendanceManager:
        return AttendanceManager(self.storage, self.auth_mgr.current_user or "Admin")

    def run(self):
        clear_screen()
        print_header("STUDENT MANAGEMENT SYSTEM - AUTHENTICATION")
        print("Default Initial Admin: admin  |  Password: AdminPassword@123\n")

        while not self.auth_mgr.is_authenticated():
            username = input("Username: ").strip()
            password = getpass.getpass("Password: ")

            try:
                self.auth_mgr.login(username, password)
                print_success(f"Welcome, {username}!")
                input("Press Enter to continue to Main Menu...")
                break
            except SMSException as e:
                print_error(str(e))
                choice = input("\nTry again? (y/n): ").strip().lower()
                if choice != 'y':
                    print("Exiting application.")
                    sys.exit(0)

        self.main_menu()

    def main_menu(self):
        while True:
            clear_screen()
            print_header(f"STUDENT MANAGEMENT SYSTEM (User: {self.auth_mgr.current_user})")
            print("1.  Add Student")
            print("2.  View All Students (Paginated)")
            print("3.  Search Student")
            print("4.  Update Student")
            print("5.  Delete Student")
            print("6.  Manage Marks")
            print("7.  Manage Attendance")
            print("8.  Sort Students")
            print("9.  Filter Students")
            print("10. Performance & Analytics Reports")
            print("11. Backup & Restore Data")
            print("12. Export Reports & Tables")
            print("13. Change Password")
            print("14. View Activity / Audit Logs")
            print("15. Logout")
            print("0.  Exit")
            print_separator()

            choice = input("Enter your choice (0-15): ").strip()
            try:
                if choice == "1":
                    self.add_student_flow()
                elif choice == "2":
                    self.view_students_flow()
                elif choice == "3":
                    self.search_students_flow()
                elif choice == "4":
                    self.update_student_flow()
                elif choice == "5":
                    self.delete_student_flow()
                elif choice == "6":
                    self.manage_marks_flow()
                elif choice == "7":
                    self.manage_attendance_flow()
                elif choice == "8":
                    self.sort_students_flow()
                elif choice == "9":
                    self.filter_students_flow()
                elif choice == "10":
                    self.reports_menu()
                elif choice == "11":
                    self.backup_restore_flow()
                elif choice == "12":
                    self.export_flow()
                elif choice == "13":
                    self.change_password_flow()
                elif choice == "14":
                    self.view_logs_flow()
                elif choice == "15":
                    self.auth_mgr.logout()
                    print_success("Logged out successfully.")
                    input("Press Enter to return to login...")
                    self.run()
                    return
                elif choice == "0":
                    print("\nThank you for using Student Management System. Goodbye!")
                    sys.exit(0)
                else:
                    print_error("Invalid selection. Please choose a valid menu item.")
            except SMSException as e:
                print_error(str(e))
            except Exception as e:
                print_error(f"An unexpected error occurred: {e}")

            input("\nPress Enter to return to menu...")

    def add_student_flow(self):
        clear_screen()
        print_header("ADD NEW STUDENT")
        auto_id = input("Auto-generate Student ID? (y/n, default y): ").strip().lower()
        if auto_id != 'n':
            student_id = self.student_mgr.generate_next_student_id()
            print(f"Generated Student ID: {student_id}")
        else:
            student_id = input("Enter Student ID (e.g., STU001): ").strip()

        name = input("Full Name: ")
        age = input("Age: ")
        gender = input("Gender (Male/Female/Other): ")
        class_year = input("Class/Year (e.g. CS-Year2): ")
        course = input("Course (e.g. Computer Science): ")
        email = input("Email: ")
        phone = input("Phone Number: ")
        dob = input("Date of Birth (YYYY-MM-DD): ")
        address = input("Address: ")
        admission_date = input("Admission Date (YYYY-MM-DD): ")

        data = {
            "student_id": student_id,
            "name": name,
            "age": age,
            "gender": gender,
            "class_year": class_year,
            "course": course,
            "email": email,
            "phone": phone,
            "dob": dob,
            "address": address,
            "admission_date": admission_date,
            "classes_attended": 0,
            "total_classes": 0,
            "marks": {}
        }
        student = self.student_mgr.add_student(data)
        print_success(f"Student {student.name} ({student.student_id}) enrolled successfully!")

    def view_students_flow(self, student_list=None):
        clear_screen()
        print_header("STUDENT DIRECTORY")
        students = student_list if student_list is not None else self.student_mgr.get_all_students()

        if not students:
            print("No student records available.")
            return

        page_size = 5
        total_pages = (len(students) + page_size - 1) // page_size
        current_page = 1

        while True:
            clear_screen()
            print_header(f"STUDENT DIRECTORY (Page {current_page} of {total_pages})")
            start = (current_page - 1) * page_size
            page_items = students[start:start + page_size]

            headers = ["ID", "Name", "Class", "Course", "Attendance", "Total", "%", "Grade", "Status"]
            rows = []
            for s in page_items:
                rows.append([
                    s.student_id,
                    s.name,
                    s.class_year,
                    s.course,
                    f"{s.attendance_percentage}%",
                    f"{s.total_marks}/{s.max_possible_marks}",
                    f"{s.percentage}%",
                    s.grade,
                    s.pass_status
                ])
            print_table(headers, rows)

            if total_pages == 1:
                break

            nav = input("\n[N]ext Page | [P]revious Page | [Q]uit View: ").strip().lower()
            if nav == 'n' and current_page < total_pages:
                current_page += 1
            elif nav == 'p' and current_page > 1:
                current_page -= 1
            elif nav == 'q':
                break

    def search_students_flow(self):
        clear_screen()
        print_header("SEARCH STUDENTS")
        print("Search Options: 1. ID | 2. Name | 3. Class | 4. Course | 5. Grade | 6. All Fields")
        sc = input("Select field (1-6): ").strip()
        mapping = {"1": "id", "2": "name", "3": "class", "4": "course", "5": "grade", "6": "all"}
        field = mapping.get(sc, "all")
        query = input("Enter search query: ").strip()

        all_students = self.student_mgr.get_all_students()
        results = SearchSortManager.search(all_students, query, field)
        print_success(f"Found {len(results)} matching records.")
        self.view_students_flow(results)

    def update_student_flow(self):
        clear_screen()
        print_header("UPDATE STUDENT RECORD")
        sid = input("Enter Student ID to update: ").strip()
        student = self.student_mgr.get_student(sid)

        print(f"\nEditing Student: {student.name} ({student.student_id})")
        print("Leave blank to keep existing value.\n")

        new_name = input(f"Name [{student.name}]: ").strip()
        new_age = input(f"Age [{student.age}]: ").strip()
        new_gender = input(f"Gender [{student.gender}]: ").strip()
        new_class = input(f"Class/Year [{student.class_year}]: ").strip()
        new_course = input(f"Course [{student.course}]: ").strip()
        new_email = input(f"Email [{student.email}]: ").strip()
        new_phone = input(f"Phone [{student.phone}]: ").strip()
        new_dob = input(f"DOB [{student.dob}]: ").strip()
        new_address = input(f"Address [{student.address}]: ").strip()

        updates = {}
        if new_name: updates["name"] = new_name
        if new_age: updates["age"] = new_age
        if new_gender: updates["gender"] = new_gender
        if new_class: updates["class_year"] = new_class
        if new_course: updates["course"] = new_course
        if new_email: updates["email"] = new_email
        if new_phone: updates["phone"] = new_phone
        if new_dob: updates["dob"] = new_dob
        if new_address: updates["address"] = new_address

        if updates:
            self.student_mgr.update_student(sid, updates)
            print_success("Student profile updated successfully.")
        else:
            print("No modifications entered.")

    def delete_student_flow(self):
        clear_screen()
        print_header("DELETE STUDENT RECORD")
        sid = input("Enter Student ID to delete: ").strip()
        student = self.student_mgr.get_student(sid)

        confirm = input(f"Are you sure you want to delete {student.name} ({student.student_id})? (y/n): ").strip().lower()
        if confirm == 'y':
            self.student_mgr.delete_student(sid, soft_delete=True)
            print_success(f"Student {sid} has been archived/deleted.")
        else:
            print("Deletion canceled.")

    def manage_marks_flow(self):
        clear_screen()
        print_header("ACADEMIC MARKS MANAGEMENT")
        print("1. Enter / Update Student Marks")
        print("2. Add New Subject to System")
        print("3. View Configured Subjects")
        choice = input("Choice (1-3): ").strip()

        if choice == "1":
            sid = input("Enter Student ID: ").strip()
            student = self.student_mgr.get_student(sid)
            subjects = self.marks_mgr.get_configured_subjects()

            print(f"\nEntering marks for {student.name} (0 - 100):")
            marks_payload = {}
            for subj in subjects:
                current_score = student.marks.get(subj, "Not assigned")
                val = input(f"{subj} [Current: {current_score}] (Enter new score or skip): ").strip()
                if val:
                    marks_payload[subj] = float(val)

            if marks_payload:
                self.marks_mgr.update_student_marks(sid, marks_payload)
                print_success("Student marks recorded successfully.")
        elif choice == "2":
            new_sub = input("Enter new subject title: ").strip()
            self.marks_mgr.add_configured_subject(new_sub)
            print_success(f"Subject '{new_sub}' added.")
        elif choice == "3":
            print("\nConfigured Subjects:")
            for s in self.marks_mgr.get_configured_subjects():
                print(f" - {s}")

    def manage_attendance_flow(self):
        clear_screen()
        print_header("ATTENDANCE MANAGEMENT")
        sid = input("Enter Student ID: ").strip()
        student = self.student_mgr.get_student(sid)
        print(f"Student: {student.name} | Current Attendance: {student.classes_attended}/{student.total_classes} ({student.attendance_percentage}%)")

        att = input("Enter total classes attended: ").strip()
        tot = input("Enter total classes held: ").strip()
        self.att_mgr.record_attendance(sid, int(att), int(tot))
        print_success("Attendance updated successfully.")

    def sort_students_flow(self):
        clear_screen()
        print_header("SORT STUDENTS")
        print("Sort by: 1. ID | 2. Name | 3. Age | 4. Marks | 5. Percentage | 6. Attendance | 7. Admission Date")
        opt = input("Select sort key (1-7): ").strip()
        crit_map = {
            "1": "id", "2": "name", "3": "age", "4": "marks",
            "5": "percentage", "6": "attendance", "7": "admission_date"
        }
        crit = crit_map.get(opt, "id")
        order = input("Order: [A]scending or [D]escending (default D): ").strip().lower()
        reverse = False if order == 'a' else True

        students = self.student_mgr.get_all_students()
        sorted_list = SearchSortManager.sort_students(students, crit, reverse)
        self.view_students_flow(sorted_list)

    def filter_students_flow(self):
        clear_screen()
        print_header("FILTER STUDENTS")
        grade = input("Filter by Grade (A+, A, B+, B, C, D, F) or press Enter: ").strip()
        status = input("Filter by Status (Pass / Fail) or press Enter: ").strip()
        course = input("Filter by Course or press Enter: ").strip()
        att_shortage = input("Show only attendance shortage (<75%)? (y/n): ").strip().lower()

        max_att = MIN_ATTENDANCE_PERCENT - 0.01 if att_shortage == 'y' else None

        students = self.student_mgr.get_all_students()
        filtered = SearchSortManager.filter_students(
            students,
            grade=grade if grade else None,
            pass_status=status if status else None,
            course=course if course else None,
            max_attendance=max_att
        )
        print_success(f"Filtered down to {len(filtered)} records.")
        self.view_students_flow(filtered)

    def reports_menu(self):
        clear_screen()
        print_header("ACADEMIC PERFORMANCE & ANALYTICS REPORTS")
        print("1. Topper Report (Top N Students)")
        print("2. Class Performance Summary")
        print("3. Pass / Fail Analysis")
        print("4. Grade Distribution Breakdown")
        print("5. Subject-wise Marks Analysis")
        print("6. Attendance Risk Report (<75%)")
        print("7. Individual Student Transcript / Performance Card")
        print_separator()
        choice = input("Select report (1-7): ").strip()

        students = self.student_mgr.get_all_students()
        rm = ReportManager(students)

        if choice == "1":
            n = input("How many top students to display? (e.g. 3, 5, 10): ").strip()
            count = int(n) if n.isdigit() else 3
            toppers = rm.get_toppers(count)
            print_header(f"TOP {count} STUDENTS")
            headers = ["Rank", "ID", "Name", "Course", "Percentage", "Grade"]
            rows = [[idx + 1, t.student_id, t.name, t.course, f"{t.percentage}%", t.grade] for idx, t in enumerate(toppers)]
            print_table(headers, rows)

        elif choice == "2":
            summary = rm.get_class_performance_summary()
            print_header("CLASS PERFORMANCE SUMMARY")
            print(f"Total Enrolled Students : {summary.get('total_students', 0)}")
            print(f"Overall Class Average   : {summary.get('average_percentage', 0.0)}%")
            print(f"Highest Percentage      : {summary.get('highest_percentage', 0.0)}%")
            print(f"Lowest Percentage       : {summary.get('lowest_percentage', 0.0)}%")
            print(f"Batch Topper            : {summary.get('topper', 'N/A')}")
            print(f"Pass Rate               : {summary.get('pass_fail', {}).get('pass_pct', 0.0)}%")
            print(f"Average Attendance      : {summary.get('attendance', {}).get('avg_att', 0.0)}%")

        elif choice == "3":
            pf = rm.generate_pass_fail_summary()
            print_header("PASS / FAIL SUMMARY")
            print(f"Total Assessed Students : {pf['total']}")
            print(f"Students Passed         : {pf['passed']} ({pf['pass_pct']}%)")
            print(f"Students Failed         : {pf['failed']} ({pf['fail_pct']}%)")

        elif choice == "4":
            dist = rm.generate_grade_distribution()
            print_header("GRADE DISTRIBUTION")
            headers = ["Grade", "Student Count"]
            rows = [[k, str(v)] for k, v in dist.items()]
            print_table(headers, rows)

        elif choice == "5":
            sub_analysis = rm.generate_subject_wise_analysis()
            print_header("SUBJECT-WISE PERFORMANCE")
            headers = ["Subject", "Average", "Highest", "Lowest"]
            rows = [[s, f"{v['avg']}", f"{v['highest']}", f"{v['lowest']}"] for s, v in sub_analysis.items()]
            print_table(headers, rows)

        elif choice == "6":
            shortage = [s for s in students if s.attendance_percentage < MIN_ATTENDANCE_PERCENT]
            print_header(f"STUDENTS WITH ATTENDANCE SHORTAGE (<{MIN_ATTENDANCE_PERCENT}%)")
            headers = ["ID", "Name", "Classes Attended", "Total Classes", "Attendance %"]
            rows = [[s.student_id, s.name, s.classes_attended, s.total_classes, f"{s.attendance_percentage}%"] for s in shortage]
            print_table(headers, rows)

        elif choice == "7":
            sid = input("Enter Student ID: ").strip()
            s = self.student_mgr.get_student(sid)
            rank = rm.get_student_rank(sid)
            self._render_student_transcript(s, rank)

    def _render_student_transcript(self, s, rank: int):
        clear_screen()
        print("=" * 60)
        print("STUDENT PERFORMANCE CARD".center(60))
        print("=" * 60)
        print(f"Student ID     : {s.student_id}")
        print(f"Name           : {s.name}")
        print(f"Course & Class : {s.course} | {s.class_year}")
        print(f"Email & Phone  : {s.email} | {s.phone}")
        print("-" * 60)
        print("ACADEMIC RESULTS:")
        for subj, score in s.marks.items():
            print(f"  {subj:<25} : {score:>6.2f} / 100")
        print("-" * 60)
        print(f"Total Marks    : {s.total_marks} / {s.max_possible_marks}")
        print(f"Percentage     : {s.percentage}%")
        print(f"Grade          : {s.grade}")
        print(f"Result Status  : {s.pass_status}")
        print(f"Batch Rank     : #{rank if rank > 0 else 'N/A'}")
        print(f"Attendance     : {s.classes_attended}/{s.total_classes} ({s.attendance_percentage}%) - {s.attendance_status}")
        print("=" * 60)

    def backup_restore_flow(self):
        clear_screen()
        print_header("BACKUP & RESTORATION ENGINE")
        print("1. Create New Timestamped Backup")
        print("2. List Existing Backups")
        print("3. Restore Data from Backup")
        choice = input("Choice (1-3): ").strip()

        if choice == "1":
            backup_name = self.backup_mgr.create_backup()
            print_success(f"Snapshot created successfully: {backup_name}")
        elif choice == "2":
            backups = self.backup_mgr.list_backups()
            print("\nAvailable Backups:")
            for b in backups:
                print(f" - {b}")
        elif choice == "3":
            backups = self.backup_mgr.list_backups()
            if not backups:
                print("No backups available.")
                return
            for idx, b in enumerate(backups):
                print(f"{idx + 1}. {b}")
            sel = input("Select backup number to restore: ").strip()
            if sel.isdigit() and 1 <= int(sel) <= len(backups):
                b_name = backups[int(sel) - 1]
                confirm = input(f"Warning: Overwrites current data with {b_name}. Proceed? (y/n): ").strip().lower()
                if confirm == 'y':
                    self.backup_mgr.restore_backup(b_name)
                    print_success(f"Data restored from {b_name} successfully.")
            else:
                print_error("Invalid selection.")

    def export_flow(self):
        clear_screen()
        print_header("DATA & REPORT EXPORT ENGINE")
        print("1. Export All Student Data (CSV)")
        print("2. Export Class Summary (TXT)")
        print("3. Export Full Dataset (JSON)")
        print("4. Export Class Summary (PDF - Optional)")
        choice = input("Select export option (1-4): ").strip()

        students = self.student_mgr.get_all_students()
        rm = ReportManager(students)

        if choice == "1":
            p = self.export_mgr.export_students_to_csv("students_export", students)
            print_success(f"File exported to: {p.resolve()}")
        elif choice == "2":
            summary = rm.get_class_performance_summary()
            lines = [
                "CLASS PERFORMANCE SUMMARY REPORT\n",
                f"Total Students: {summary.get('total_students', 0)}",
                f"Average Percentage: {summary.get('average_percentage', 0.0)}%",
                f"Batch Topper: {summary.get('topper', 'N/A')}",
                f"Pass Percentage: {summary.get('pass_fail', {}).get('pass_pct', 0.0)}%\n"
            ]
            p = self.export_mgr.export_to_txt("class_summary", "\n".join(lines))
            print_success(f"Text report saved: {p.resolve()}")
        elif choice == "3":
            raw_data = [s.to_dict() for s in students]
            p = self.export_mgr.export_to_json("students_dump", raw_data)
            print_success(f"JSON dump saved: {p.resolve()}")
        elif choice == "4":
            summary = rm.get_class_performance_summary()
            text_lines = [
                "Academic Year Report Summary",
                f"Generated for: {len(students)} Students",
                f"Class Average: {summary.get('average_percentage', 0.0)}%",
                f"Highest Percentage: {summary.get('highest_percentage', 0.0)}%",
                f"Pass Rate: {summary.get('pass_fail', {}).get('pass_pct', 0.0)}%",
                f"Average Attendance: {summary.get('attendance', {}).get('avg_att', 0.0)}%"
            ]
            pdf_path = self.export_mgr.export_to_pdf("class_report", "Class Performance Summary", text_lines)
            if pdf_path:
                print_success(f"PDF Report generated: {pdf_path.resolve()}")
            else:
                print_error("ReportLab library not installed. Install with 'pip install reportlab' to enable PDF export.")

    def change_password_flow(self):
        clear_screen()
        print_header("CHANGE ADMIN PASSWORD")
        old_p = getpass.getpass("Current Password: ")
        new_p = getpass.getpass("New Password (min 8 characters): ")
        confirm_p = getpass.getpass("Confirm New Password: ")

        if new_p != confirm_p:
            print_error("New passwords do not match.")
            return

        self.auth_mgr.change_password(old_p, new_p)
        print_success("Admin password changed successfully.")

    def view_logs_flow(self):
        clear_screen()
        print_header("SYSTEM ACTIVITY & AUDIT LOGS")
        logs = read_recent_logs(25)
        if not logs:
            print("No activity logs recorded yet.")
        else:
            for line in logs:
                print(line.strip())