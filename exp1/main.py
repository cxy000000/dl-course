from utils import RouteGUI, MenuGUI, SMapGUI
import sys
from PyQt5.QtWidgets import QApplication

def closeAndShowRouteWindow(w_1, w_2):
    w_1.close()
    w_2.show()

if __name__ == "__main__":
    api_key = '1c5a6f863e2b10154c7ec8357f11f740'
    app = QApplication(sys.argv)
    w_menu = MenuGUI()
    w_route = RouteGUI(api_key)
    w_map = SMapGUI(api_key)
    w_menu.show()
    
    # 跳联关系
    w_menu.ui.pushButton_r.clicked.connect(lambda: closeAndShowRouteWindow(w_menu, w_route))
    w_menu.ui.pushButton_m.clicked.connect(lambda: closeAndShowRouteWindow(w_menu, w_map))
    w_route.ui.pushButton_back.clicked.connect(lambda: closeAndShowRouteWindow(w_route, w_menu))
    w_map.ui.pushButton_back.clicked.connect(lambda: closeAndShowRouteWindow(w_map, w_menu))

    w_menu.ui.pushButton_quit.clicked.connect(app.quit)
    app.exec_()
    
    

