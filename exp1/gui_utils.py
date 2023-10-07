from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtCore import Qt
from uiwindow import Ui_MainWindow  # 导入生成的UI类

class RouteGUI(QMainWindow):
    def __init__(self, api_key):
        super().__init__()
        self.route = Route(api_key)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.get_walking_route)
        self.ui.pushButton_2.clicked.connect(self.get_riding_route)
        self.ui.pushButton_3.clicked.connect(self.get_driving_route)

        # GUI的其余代码...

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = RouteGUI("YOUR_API_KEY_HERE")
    window.show()
    sys.exit(app.exec_())
