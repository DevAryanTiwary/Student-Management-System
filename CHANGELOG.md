# Changelog

All notable changes to the Student Management System (SMS) are documented here.

## [2.0.0] - 2026-10-04
### Added
- **PySide6 Modern Desktop GUI**: Integrated dark/light theme support, custom navigation, and modern typography.
- **Role-Based Access Control (RBAC)**: Support for `Super Admin`, `Administrator`, `Teacher`, and `Viewer`.
- **Global Spotlight Search**: Quick search modal accessible via `Ctrl+K`.
- **Enrollment Wizard**: 5-step interactive GUI modal for adding new students.
- **Embedded Analytics**: Dynamic Matplotlib charts for grade distributions and subject averages.
- **Data Integrity & Health Checks**: Startup diagnostic scanner detecting dataset anomalies.
- **Dual-Mode Startup**: Seamless CLI (`--cli`) and GUI execution modes.

### Preserved
- Unchanged CSV/JSON storage formats and atomic write safety (`os.replace`).
- Unchanged PBKDF2 password hashing, salt sizes, and lockout thresholds.
- Unchanged academic calculation formulas (Percentages, Grades, Pass/Fail, Attendance).
- Full compatibility with all pre-existing unit tests.