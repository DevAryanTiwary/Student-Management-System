"""
Professional QSS Design System supporting Dark and Light palettes.
Ensures high contrast and fixes table item & combobox dropdown visibility.
"""

DARK_THEME_QSS = """
QMainWindow, QDialog {
    background-color: #0F172A;
    color: #F8FAFC;
}
QWidget {
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    font-size: 13px;
    color: #F8FAFC;
}

/* Sidebar Navigation */
#SidebarFrame {
    background-color: #1E293B;
    border-right: 1px solid #334155;
}
#SidebarButton {
    background-color: transparent;
    color: #94A3B8;
    text-align: left;
    padding: 10px 18px;
    border-radius: 6px;
    font-weight: 500;
    border: none;
}
#SidebarButton:hover {
    background-color: #334155;
    color: #FFFFFF;
}
#SidebarButton:checked {
    background-color: #2563EB;
    color: #FFFFFF;
    font-weight: 600;
}

/* Header & Top Bar */
#HeaderFrame {
    background-color: #1E293B;
    border-bottom: 1px solid #334155;
    padding: 6px 16px;
}

/* Card Panels */
#CardWidget {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 16px;
}

/* Standard Inputs & Comboboxes */
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit, QTextEdit {
    background-color: #1E293B;
    border: 1px solid #475569;
    border-radius: 6px;
    padding: 7px 10px;
    color: #F8FAFC;
}
QLineEdit:focus, QComboBox:focus {
    border: 1px solid #38BDF8;
}

/* ComboBox Dropdown Fix */
QComboBox QAbstractItemView {
    background-color: #1E293B;
    color: #F8FAFC;
    selection-background-color: #2563EB;
    selection-color: #FFFFFF;
    border: 1px solid #475569;
    padding: 4px;
}

/* Buttons */
QPushButton {
    background-color: #2563EB;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 600;
}
QPushButton:hover {
    background-color: #1D4ED8;
}
QPushButton:pressed {
    background-color: #1E40AF;
}
QPushButton#SecondaryButton {
    background-color: #334155;
    color: #F8FAFC;
}
QPushButton#SecondaryButton:hover {
    background-color: #475569;
}
QPushButton#DangerButton {
    background-color: #DC2626;
    color: #FFFFFF;
}
QPushButton#DangerButton:hover {
    background-color: #B91C1C;
}

/* Tables & Lists - Explicit Text and Row Contrast */
QTableWidget, QListWidget {
    background-color: #0F172A;
    alternate-background-color: #1E293B;
    color: #F8FAFC;
    gridline-color: #334155;
    border: 1px solid #334155;
    border-radius: 6px;
    selection-background-color: #2563EB;
    selection-color: #FFFFFF;
}
QTableWidget::item {
    color: #F8FAFC;
    padding: 6px;
    background-color: transparent;
}
QTableWidget::item:selected {
    background-color: #2563EB;
    color: #FFFFFF;
}
QHeaderView::section {
    background-color: #1E293B;
    color: #CBD5E1;
    font-weight: 600;
    padding: 8px;
    border: none;
    border-bottom: 1px solid #334155;
}
QTableCornerButton::section {
    background-color: #1E293B;
    border: none;
}

/* Scrollbars */
QScrollBar:vertical {
    background: #0F172A;
    width: 8px;
}
QScrollBar::handle:vertical {
    background: #475569;
    border-radius: 4px;
}
QStatusBar {
    background-color: #1E293B;
    border-top: 1px solid #334155;
    color: #94A3B8;
}
"""

LIGHT_THEME_QSS = """
QMainWindow, QDialog {
    background-color: #F8FAFC;
    color: #0F172A;
}
QWidget {
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    font-size: 13px;
    color: #0F172A;
}
#SidebarFrame {
    background-color: #FFFFFF;
    border-right: 1px solid #E2E8F0;
}
#SidebarButton {
    background-color: transparent;
    color: #475569;
    text-align: left;
    padding: 10px 18px;
    border-radius: 6px;
    font-weight: 500;
    border: none;
}
#SidebarButton:hover {
    background-color: #F1F5F9;
    color: #0F172A;
}
#SidebarButton:checked {
    background-color: #2563EB;
    color: #FFFFFF;
    font-weight: 600;
}
#HeaderFrame {
    background-color: #FFFFFF;
    border-bottom: 1px solid #E2E8F0;
    padding: 6px 16px;
}
#CardWidget {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 16px;
}
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit, QTextEdit {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 7px 10px;
    color: #0F172A;
}
QLineEdit:focus, QComboBox:focus {
    border: 1px solid #2563EB;
}
QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    color: #0F172A;
    selection-background-color: #2563EB;
    selection-color: #FFFFFF;
    border: 1px solid #CBD5E1;
}
QPushButton {
    background-color: #2563EB;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 600;
}
QPushButton:hover {
    background-color: #1D4ED8;
}
QPushButton#SecondaryButton {
    background-color: #F1F5F9;
    color: #334155;
    border: 1px solid #CBD5E1;
}
QPushButton#SecondaryButton:hover {
    background-color: #E2E8F0;
}
QPushButton#DangerButton {
    background-color: #DC2626;
    color: #FFFFFF;
}
QPushButton#DangerButton:hover {
    background-color: #B91C1C;
}
QTableWidget, QListWidget {
    background-color: #FFFFFF;
    alternate-background-color: #F8FAFC;
    color: #0F172A;
    gridline-color: #E2E8F0;
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    selection-background-color: #DBEAFE;
    selection-color: #1E40AF;
}
QTableWidget::item {
    color: #0F172A;
    padding: 6px;
}
QHeaderView::section {
    background-color: #F1F5F9;
    color: #334155;
    font-weight: 600;
    padding: 8px;
    border: none;
    border-bottom: 1px solid #E2E8F0;
}
QScrollBar:vertical {
    background: #F8FAFC;
    width: 8px;
}
QScrollBar::handle:vertical {
    background: #CBD5E1;
    border-radius: 4px;
}
QStatusBar {
    background-color: #FFFFFF;
    border-top: 1px solid #E2E8F0;
    color: #64748B;
}
"""

def get_theme_qss(theme_name: str = "dark") -> str:
    return DARK_THEME_QSS if theme_name.lower() == "dark" else LIGHT_THEME_QSS