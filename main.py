import sys
import json
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QLabel, QFrame, QComboBox, QInputDialog


class TimeTracker(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Start time input
        self.start_time_input = QLineEdit(self)
        self.start_time_input.setPlaceholderText("Enter start time (HH:MM)")
        self.start_time_input.setStyleSheet("""QLineEdit {
            padding: 10px;
            font-size: 14px;
            border-radius: 10px;
            border: 1px solid #ccc;
            background-color: #f5f5f5;
        }""")
        layout.addWidget(self.start_time_input)

        # End time input
        self.end_time_input = QLineEdit(self)
        self.end_time_input.setPlaceholderText("Enter end time (HH:MM)")
        self.end_time_input.setStyleSheet("""QLineEdit {
            padding: 10px;
            font-size: 14px;
            border-radius: 10px;
            border: 1px solid #ccc;
            background-color: #f5f5f5;
        }""")
        layout.addWidget(self.end_time_input)

        # Project combobox
        self.project_combobox = QComboBox(self)
        self.load_projects_into_combobox()  # Load projects into the combobox
        self.project_combobox.setStyleSheet("""QComboBox {
            padding: 10px;
            font-size: 14px;
            border-radius: 10px;
            border: 1px solid #ccc;
            background-color: #f5f5f5;
        }""")
        layout.addWidget(self.project_combobox)

        # Submit button
        self.submit_button = QPushButton("Save Time", self)
        self.submit_button.setStyleSheet("""QPushButton {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 16px;
            border: none;
        }
        QPushButton:hover {
            background-color: #45a049;
        }""")
        self.submit_button.clicked.connect(self.save_time)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def load_projects_into_combobox(self):
        """Load all available projects into the combobox."""
        try:
            with open("Float/data.json", "r") as file:
                data = json.load(file)
            self.project_combobox.clear()
            self.project_combobox.addItems(data.keys())  # Add project names dynamically
        except (FileNotFoundError, json.JSONDecodeError):
            pass  # If no data is available, the combobox will stay empty

    def save_time(self):
        start_time = self.start_time_input.text()
        end_time = self.end_time_input.text()
        project = self.project_combobox.currentText()

        # Simple time difference calculation (assuming valid time input format)
        try:
            start_hour, start_minute = map(int, start_time.split(":"))
            end_hour, end_minute = map(int, end_time.split(":"))
            start_in_minutes = start_hour * 60 + start_minute
            end_in_minutes = end_hour * 60 + end_minute
            time_spent = end_in_minutes - start_in_minutes

            if time_spent < 0:
                raise ValueError("End time must be later than start time.")

            with open("Float/data.json", "r") as file:
                data = json.load(file)
        except (ValueError, FileNotFoundError, json.JSONDecodeError):
            data = {}

        if project not in data:
            data[project] = []
        data[project].append(time_spent)

        with open("Float/data.json", "w") as file:
            json.dump(data, file, indent=4)

        self.start_time_input.clear()
        self.end_time_input.clear()


class TodoList(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.todo_list_widget = QListWidget(self)
        self.todo_list_widget.setStyleSheet("""QListWidget {
            padding: 10px;
            border-radius: 10px;
            background-color: #f5f5f5;
            font-size: 14px;
        }""")
        layout.addWidget(self.todo_list_widget)

        self.todo_input = QLineEdit(self)
        self.todo_input.setPlaceholderText("Enter new task")
        self.todo_input.setStyleSheet("""QLineEdit {
            padding: 10px;
            font-size: 14px;
            border-radius: 10px;
            border: 1px solid #ccc;
            background-color: #f5f5f5;
        }""")
        layout.addWidget(self.todo_input)

        self.add_button = QPushButton("Add Task", self)
        self.add_button.setStyleSheet("""QPushButton {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 16px;
            border: none;
        }""")
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
        self.project_list.setStyleSheet("""QListWidget {
            padding: 10px;
            border-radius: 10px;
            background-color: #f5f5f5;
            font-size: 14px;
        }""")
        layout.addWidget(self.project_list)

        self.load_projects_button = QPushButton("Load Projects", self)
        self.load_projects_button.setStyleSheet("""QPushButton {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 16px;
            border: none;
        }""")
        self.load_projects_button.clicked.connect(self.load_projects)
        layout.addWidget(self.load_projects_button)

        self.add_project_button = QPushButton("Add Project", self)
        self.add_project_button.setStyleSheet("""QPushButton {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 16px;
            border: none;
        }""")
        self.add_project_button.clicked.connect(self.add_project)
        layout.addWidget(self.add_project_button)

        self.setLayout(layout)

    def load_projects(self):
        """Load and display projects with time in hours:minutes format."""
        try:
            with open("Float/data.json", "r") as file:
                data = json.load(file)
            self.project_list.clear()

            for project, hours in data.items():
                total_minutes = sum(map(int, hours))  # Calculate total minutes

                # Convert total minutes into hours and minutes
                hours_part = total_minutes // 60
                minutes_part = total_minutes % 60
                
                # Format the time as hours:minutes
                time_formatted = f"{hours_part}h {minutes_part:02d}m"

                # Add project to the list in hours:minutes format
                self.project_list.addItem(f"{project}: {time_formatted}")

        except FileNotFoundError:
            self.project_list.clear()
            self.project_list.addItem("No data available.")
        except json.JSONDecodeError:
            self.project_list.clear()
            self.project_list.addItem("Invalid data file.")


    def add_project(self):
        """Add a new project."""
        project_name, ok = QInputDialog.getText(self, "Add Project", "Enter project name:")
        if ok and project_name:
            try:
                # Read the existing data from the JSON file
                with open("Float/data.json", "r") as file:
                    # If the file is empty, this will raise an exception
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = {}  # If the file is empty or invalid, initialize as an empty dictionary

                # Add the new project if it doesn't already exist
                if project_name not in data:
                    data[project_name] = []

                # Save the updated data back to the file
                with open("Float/data.json", "w") as file:
                    json.dump(data, file, indent=4)

                # After adding a project, reload the projects into the TimeTracker combobox
                main_window = self.window()
                if isinstance(main_window, MainWindow):
                    main_window.time_tracker.load_projects_into_combobox()  # Update the combobox with the new project

                self.load_projects()

            except Exception as e:
                print(f"An error occurred while adding the project: {e}")


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
        self.time_tracker_button.setStyleSheet("""QPushButton {
            background-color: #ffffff;
            padding: 12px;
            font-size: 18px;
            border: none;
            border-radius: 10px;
            color: #333;
        }""")
        self.time_tracker_button.clicked.connect(self.show_time_tracker)
        sidebar_layout.addWidget(self.time_tracker_button)

        self.todo_button = QPushButton("To-Do List", self)
        self.todo_button.setStyleSheet("""QPushButton {
            background-color: #ffffff;
            padding: 12px;
            font-size: 18px;
            border: none;
            border-radius: 10px;
            color: #333;
        }""")
        self.todo_button.clicked.connect(self.show_todo_list)
        sidebar_layout.addWidget(self.todo_button)

        self.projects_button = QPushButton("Projects", self)
        self.projects_button.setStyleSheet("""QPushButton {
            background-color: #ffffff;
            padding: 12px;
            font-size: 18px;
            border: none;
            border-radius: 10px;
            color: #333;
        }""")
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
