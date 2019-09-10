import sys
from startup_logic import StartupDialog

from PyQt5.QtWidgets import QApplication

__app_name__: str = "BBCheck"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    startup_window = StartupDialog()

    startup_window.show()
    sys.exit(app.exec_())
