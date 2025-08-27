import sys
from PySide6.QtWidgets import QApplication
from gui import WorkoutTrackerApp


if __name__ == "__main__":
    app = QApplication(sys.argv) 
    window = WorkoutTrackerApp()
    window.show()
    sys.exit(app.exec())