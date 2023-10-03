from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtCore import Qt
import requests
from uiwindow import Ui_MainWindow 

class Route:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_walkingroute(self, origin, destination):
        url = f'https://restapi.amap.com/v3/direction/walking?origin={origin}&destination={destination}&key={self.api_key}'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == '1':
                    routes = data['route']['paths']
                    return routes
                else:
                    print('未找到路径')
            else:
                print('请求失败')
        except Exception as e:
            print(f'发生异常: {str(e)}')
        
    def get_geocode(self, address, city=None):
        url = f'https://restapi.amap.com/v3/geocode/geo?key={self.api_key}&address={address}&output=JSON'
        if city:
            url += f'&city={city}'
            
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == '1':
                    geocodes = data['geocodes']
                    if geocodes:
                        location = geocodes[0]['location']  # 坐标点（经度，纬度）
                        return location
                    else:
                        print('未找到匹配的地址')
                else:
                    print('请求失败')
            else:
                print('请求失败')
        except Exception as e:
            print(f'发生异常: {str(e)}')

class RouteGUI(QMainWindow):
    def __init__(self, api_key):
        super().__init__()
        self.route = Route(api_key)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.get_walking_route)

    def display_message(self, message):
        self.ui.textEdit.setPlainText(self.ui.textEdit.toPlainText() + message + '\n')

    def get_walking_route(self):
        ori_city = self.ui.lineEdit.text()
        ori_address = self.ui.lineEdit_2.text()
        des_city = self.ui.lineEdit_3.text()
        des_address = self.ui.lineEdit_4.text()

        ori_geocode = self.route.get_geocode(ori_address, ori_city)
        self.display_message(f'出发点坐标: {ori_geocode}')
        des_geocode = self.route.get_geocode(des_address, des_city)
        self.display_message(f'目的地坐标: {des_geocode}')

        if ori_geocode and des_geocode:
            routes = self.route.get_walkingroute(ori_geocode, des_geocode)
            self.ui.textEdit.clear()
            for route in routes:
                distance = route['distance']  # 步行距离（米）
                duration = route['duration']  # 步行时间（秒）
                self.display_message(f'步行距离: {distance}米')
                self.display_message(f'步行时间: {duration}秒')
                self.display_message('步行路线:')
                for step in route['steps']:
                    instruction = step['instruction']
                    self.display_message(f'- {instruction}')