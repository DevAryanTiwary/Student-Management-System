# Student Management System (SMS) — Professional Edition

A production-grade, modular desktop and CLI application for academic record administration, grading analytics, and cohort tracking. Built with Python 3, PySide6, Matplotlib, and ReportLab.

---

## Key Features

1. **Dual Interface**:
   - **Modern Desktop GUI**: PySide6 dark/light interface with stat cards, Matplotlib charts, global search (`Ctrl+K`), and a 5-step student enrollment wizard.
   - **Terminal CLI Mode**: Full-featured terminal interface running via `python main.py --cli`.
2. **Security & RBAC**:
   - PBKDF2-HMAC-SHA256 password hashing with 16-byte random salts.
   - Brute-force account lockout after 3 failed attempts.
   - Roles: `Super Admin`, `Administrator`, `Teacher`, and `Viewer`.
3. **Student Lifecycle Management (CRUD)**:
   - Formatted auto-generated IDs (`STU001`, `STU002`, ...).
   - Validation for names, dates, phone numbers, emails, and ages.
   - Soft-delete mechanism preserving audit history.
4. **Academic & Attendance Engines**:
   - Configurable subjects stored in `data/subjects.json`.
   - Automated computation of Total, Percentage, GPA, Rank, and Letter Grades.
   - Strict pass/fail logic across all subjects.
   - Attendance tracking with shortage warnings below 75%.
5. **Storage & Data Integrity**:
   - Abstract persistence layer supporting interchangeable **JSON** and **CSV** files.
   - Atomic file writes using temporary files and `os.replace` to prevent data corruption.
   - Timestamped point-in-time backup and restore engine.
   - Audit trail in `logs/activity.log`.

---

## Installation & Setup

### 1. Prerequisites
- Python 3.10+ installed.

### 2. Virtual Environment Setup

**Windows PowerShell:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1