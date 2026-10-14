"""
Unified System Entry Point: Student Management System.
Supports both Professional Desktop GUI and Interactive CLI Terminal Mode.
"""
import sys
import argparse

def launch_cli_mode():
    from cli_app import StudentManagementCLI
    cli = StudentManagementCLI()
    cli.run()

def launch_gui_mode():
    try:
        from gui.app import launch_gui
        sys.exit(launch_gui())
    except ImportError as e:
        print(f"\n[Notice] GUI dependencies not found or terminal is headless ({e}).")
        print("[Notice] Falling back to Interactive Terminal CLI mode.\n")
        launch_cli_mode()

def main():
    parser = argparse.ArgumentParser(description="Student Management System — Professional Edition")
    parser.add_argument("--cli", action="store_true", help="Launch in interactive terminal CLI mode")
    parser.add_argument("--gui", action="store_true", help="Force launch in PySide6 GUI mode (default)")
    parser.add_argument("--health", action="store_true", help="Execute diagnostic health check and exit")
    args = parser.parse_args()

    if args.health:
        from config import DATA_STORAGE_FORMAT, STUDENTS_CSV_FILE, STUDENTS_JSON_FILE
        from storage.csv_storage import CSVStorage
        from storage.json_storage import JSONStorage
        from services.integrity_service import IntegrityService
        storage = CSVStorage(STUDENTS_CSV_FILE) if DATA_STORAGE_FORMAT.upper() == "CSV" else JSONStorage(STUDENTS_JSON_FILE)
        svc = IntegrityService(storage)
        report = svc.perform_system_health_check()
        print("System Health Report:", report)
        sys.exit(0)

    if args.cli:
        launch_cli_mode()
    else:
        launch_gui_mode()

if __name__ == "__main__":
    main()