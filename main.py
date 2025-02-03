import sys
import json
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QLabel, QFrame, QComboBox

class TimeTracker(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.hours_input = QLineEdit(self)
        self.hours_input.setPlaceholderText("Enter hours spent")
        self.hours_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                border-radius: 10px;
                border: 1px solid #ccc;
                background-color: #f5f5f5;
            }
        """)
        layout.addWidget(self.hours_input)

        self.project_combobox = QComboBox(self)
        self.project_combobox.addItems(["Project A", "Project B", "Project C"])
        self.project_combobox.setStyleSheet("""
            QComboBox {
                padding: 10px;
                font-size: 14px;
                border-radius: 10px;
                border: 1px solid #ccc;
                background-color: #f5f5f5;
            }
        """)
        layout.addWidget(self.project_combobox)

        self.submit_button = QPushButton("Save Hours", self)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.submit_button.clicked.connect(self.save_hours)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def save_hours(self):
        hours = self.hours_input.text()
        project = self.project_combobox.currentText()

        try:
            with open("Float/data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        if project not in data:
            data[project] = []
        data[project].append(hours)

        with open("Float/data.json", "w") as file:
            json.dump(data, file, indent=4)

        self.hours_input.clear()


class TodoList(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.todo_list_widget = QListWidget(self)
        self.todo_list_widget.setStyleSheet("""
            QListWidget {
                padding: 10px;
                border-radius: 10px;
                background-color: #f5f5f5;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 5px;
                background-color: #fff;
            }
            QListWidget::item:hover {
                background-color: #eee;
            }
        """)
        layout.addWidget(self.todo_list_widget)

        self.todo_input = QLineEdit(self)
        self.todo_input.setPlaceholderText("Enter new task")
        self.todo_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                border-radius: 10px;
                border: 1px solid #ccc;
                background-color: #f5f5f5;
            }
        """)
        layout.addWidget(self.todo_input)

        self.add_button = QPushButton("Add Task", self)
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.add_button.clicked.connect(self.add_task)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_task(self):
        task = self.todo_input.text()
        if task:
            self.todo_list_widget.addItem(task)
            self.todo_input.clear()


class Projects(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.project_list = QListWidget(self)
        self.project_list.setStyleSheet("""
            QListWidget {
                padding: 10px;
                border-radius: 10px;
                background-color: #f5f5f5;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 5px;
                background-color: #fff;
            }
            QListWidget::item:hover {
                background-color: #eee;
            }
        """)
        layout.addWidget(self.project_list)

        self.load_projects_button = QPushButton("Load Projects", self)
        self.load_projects_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.load_projects_button.clicked.connect(self.load_projects)
        layout.addWidget(self.load_projects_button)

        self.setLayout(layout)

    def load_projects(self):
        try:
            with open("Float/data.json", "r") as file:
                data = json.load(file)
            self.project_list.clear()
            for project, hours in data.items():
                self.project_list.addItem(f"{project}: {sum(map(int, hours))} hours")
        except FileNotFoundError:
            self.project_list.clear()
            self.project_list.addItem("No data available.")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Project Time Tracker")
        self.setStyleSheet("background-color: #f0f0f0;")  # Set background color for the main window

        self.main_widget = QStackedWidget(self)

        self.sidebar = QFrame(self)
        self.sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        sidebar_layout = QVBoxLayout()
        self.sidebar.setLayout(sidebar_layout)

        self.time_tracker_button = QPushButton("Time Tracker", self)
        self.time_tracker_button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                padding: 12px;
                font-size: 18px;
                border: none;
                border-radius: 10px;
                color: #333;
            }
            QPushButton:hover {
                background-color: #f2f2f2;
            }
        """)
        self.time_tracker_button.clicked.connect(self.show_time_tracker)
        sidebar_layout.addWidget(self.time_tracker_button)

        self.todo_button = QPushButton("To-Do List", self)
        self.todo_button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                padding: 12px;
                font-size: 18px;
                border: none;
                border-radius: 10px;
                color: #333;
            }
            QPushButton:hover {
                background-color: #f2f2f2;
            }
        """)
        self.todo_button.clicked.connect(self.show_todo_list)
        sidebar_layout.addWidget(self.todo_button)

        self.projects_button = QPushButton("Projects", self)
        self.projects_button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                padding: 12px;
                font-size: 18px;
                border: none;
                border-radius: 10px;
                color: #333;
            }
            QPushButton:hover {
                background-color: #f2f2f2;
            }
        """)
        self.projects_button.clicked.connect(self.show_projects)
        sidebar_layout.addWidget(self.projects_button)

        self.time_tracker = TimeTracker()
        self.todo_list = TodoList()
        self.projects = Projects()

        self.main_widget.addWidget(self.time_tracker)
        self.main_widget.addWidget(self.todo_list)
        self.main_widget.addWidget(self.projects)

        self.setCentralWidget(self.main_widget)

        layout = QHBoxLayout()
        layout.addWidget(self.sidebar)
        layout.addWidget(self.main_widget)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def show_time_tracker(self):
        self.main_widget.setCurrentWidget(self.time_tracker)

    def show_todo_list(self):
        self.main_widget.setCurrentWidget(self.todo_list)

    def show_projects(self):
        self.main_widget.setCurrentWidget(self.projects)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(900, 600)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
