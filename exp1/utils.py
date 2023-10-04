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
        
    def get_ridingroute(self, origin, destination):
        url = f'https://restapi.amap.com/v4/direction/bicycling?origin={origin}&destination={destination}&key={self.api_key}'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                routes = data['data']['paths']
                return routes
            else:
                print('请求失败')
        except Exception as e:
            print(f'发生异常: {str(e)}')
            
    def get_drivingroute(self, origin, destination):
        url = f'https://restapi.amap.com/v3/direction/driving?origin={origin}&destination={destination}&extensions=all&output=JSON&key={self.api_key}'
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
        self.ui.pushButton_2.clicked.connect(self.get_riding_route)
        self.ui.pushButton_3.clicked.connect(self.get_driving_route)
        
        # 美化界面
        # 设置标签样式
        label_style = "font: 25 11pt '微软雅黑 Light';" \
                    "color: rgb(31,31,31);" \
                    "background-color: rgb(255, 255, 255);" \
                    "border:2px solid rgb(255,255,255);border-radius:15px;"
                    
        self.ui.label.setStyleSheet(label_style)
        self.ui.label_2.setStyleSheet(label_style)
        self.ui.label_3.setStyleSheet(label_style)
        self.ui.label_4.setStyleSheet(label_style)

        # 设置按钮样式
        button_style = "QPushButton{font: 25 13pt '微软雅黑 Light';color: rgb(255,255,255);" \
                    "background-color: rgb(20,196,188);" \
                    "border: none;border-radius:15px;}" \
                    "QPushButton:hover{background-color: rgb(22,218,208);}" \
                    "QPushButton:pressed{background-color: rgb(17,171,164);}"

        self.ui.pushButton.setStyleSheet(button_style)
        self.ui.pushButton_2.setStyleSheet(button_style)
        self.ui.pushButton_3.setStyleSheet(button_style)

        # 设置窗口背景样式
        window_style = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, " \
                    "stop:0 rgba(255,255,255, 200), stop:1 rgba(20,196,188, 210));"
        self.setStyleSheet(window_style)
        
        #设置layout的样式
        frame_style = "background-color: rgb(255, 255, 255);" \
                      "border: 2px solid rgb(20,196,188);border-radius: 15px;"
        self.ui.formLayoutWidget.setStyleSheet(frame_style)

        #设置lineEdit的样式
        line_style = "font: 25 11pt '微软雅黑 Light';" \
                    "color: rgb(31,31,31);" \
                    "background-color: rgb(255, 255, 255);" \
                    "border:2px solid rgb(20,196,188);border-radius:15px;"
        self.ui.lineEdit.setStyleSheet(line_style)
        self.ui.lineEdit_2.setStyleSheet(line_style)
        self.ui.lineEdit_3.setStyleSheet(line_style)
        self.ui.lineEdit_4.setStyleSheet(line_style)


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
                distance = route['distance']  
                duration = route['duration']  
                self.display_message(f'步行距离: {distance}米')
                self.display_message(f'步行时间: {duration}秒')
                self.display_message('步行路线:')
                for step in route['steps']:
                    instruction = step['instruction']
                    self.display_message(f'- {instruction}')
                    
    def get_riding_route(self):
        ori_city = self.ui.lineEdit.text()
        ori_address = self.ui.lineEdit_2.text()
        des_city = self.ui.lineEdit_3.text()
        des_address = self.ui.lineEdit_4.text()

        ori_geocode = self.route.get_geocode(ori_address, ori_city)
        self.display_message(f'出发点坐标: {ori_geocode}')
        des_geocode = self.route.get_geocode(des_address, des_city)
        self.display_message(f'目的地坐标: {des_geocode}')

        if ori_geocode and des_geocode:
            routes = self.route.get_ridingroute(ori_geocode, des_geocode)
            self.ui.textEdit.clear()
            for route in routes:
                distance = route['distance']  
                duration = route['duration']  
                self.display_message(f'骑行距离: {distance}米')
                self.display_message(f'骑行时间: {duration}秒')
                self.display_message('骑行路线:')
                for step in route['steps']:
                    instruction = step['instruction']
                    self.display_message(f'- {instruction}')
                    
    def get_driving_route(self):
        ori_city = self.ui.lineEdit.text()
        ori_address = self.ui.lineEdit_2.text()
        des_city = self.ui.lineEdit_3.text()
        des_address = self.ui.lineEdit_4.text()

        ori_geocode = self.route.get_geocode(ori_address, ori_city)
        self.display_message(f'出发点坐标: {ori_geocode}')
        des_geocode = self.route.get_geocode(des_address, des_city)
        self.display_message(f'目的地坐标: {des_geocode}')

        if ori_geocode and des_geocode:
            routes = self.route.get_drivingroute(ori_geocode, des_geocode)
            self.ui.textEdit.clear()
            for route in routes:
                distance = route['distance']  
                duration = route['duration']  
                self.display_message(f'行驶距离: {distance}米')
                self.display_message(f'行驶时间: {duration}秒')
                self.display_message('行驶路线:')
                for step in route['steps']:
                    instruction = step['instruction']
                    self.display_message(f'- {instruction}')