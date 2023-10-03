from utils import RouteGUI
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    api_key = '1c5a6f863e2b10154c7ec8357f11f740'
    app = QApplication(sys.argv)
    window = RouteGUI(api_key)
    window.show()
    sys.exit(app.exec_())
