from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
import requests
from uiwindow import Ui_MainWindow as Ui_MainWindow_route
from menu import Ui_MainWindow as Ui_MainWindow_menu
from uiwindow2 import Ui_MainWindow as Ui_MainWindow_smap
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QPainter
class Map_API:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_walkingroute(self, origin, destination):
        """
        Get walking route information from the AMap API.

        Parameters:
        - origin (str): The origin location for the walking route.
        - destination (str): The destination location for the walking route.

        Returns:
        - list: A list of route information.
        """
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
        """
        Get riding route information from the AMap API.

        Parameters:
        - origin (str): The origin location for the riding route.
        - destination (str): The destination location for the riding route.

        Returns:
        - list: A list of route information.
        """
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
        """
        Get driving route information from the AMap API.

        Parameters:
        - origin (str): The origin location for the driving route.
        - destination (str): The destination location for the driving route.

        Returns:
        - list: A list of route information.
        """
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
        """
        Get geocode information (latitude and longitude) from the AMap API.

        Parameters:
        - address (str): The address for which to obtain geocode information.
        - city (str, optional): The city to search within (default is None).

        Returns:
        - str: The location (latitude and longitude) in the format "latitude,longitude".
        """
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
                        location = geocodes[0]['location']  
                        return location
                    else:
                        print('未找到匹配的地址')
                else:
                    print('请求失败')
            else:
                print('请求失败')
        except Exception as e:
            print(f'发生异常: {str(e)}')
            
    def get_static_map(self, location, zoom, size):
        """
        Get a static map image from the AMap API.

        Parameters:
        - location (str): The location (latitude and longitude) for the map.
        - zoom (int): The zoom level for the map.
        - size (str): The size of the map image in the format "width*height".

        Returns:
        - bytes: The binary image data of the static map.
        """
        url = f'https://restapi.amap.com/v3/staticmap?&location={location}&zoom={zoom}&size={size}&markers=mid,0x008000,A:{location}&key={self.api_key}&output=JSON'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.content
            else:
                print('请求失败')
        except Exception as e:
            print(f'发生异常: {str(e)}')
            

class RouteGUI(QMainWindow):
    def __init__(self, api_key):
        super().__init__()
        self.route = Map_API(api_key)
        self.ui = Ui_MainWindow_route()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.get_walking_route)
        self.ui.pushButton_2.clicked.connect(self.get_riding_route)
        self.ui.pushButton_3.clicked.connect(self.get_driving_route)
        self.setup_ui_style()

    # beautify GUI
    def setup_ui_style(self):
        # label config
        label_style = "font: 25 11pt '微软雅黑 Light';" \
                      "color: rgb(31,31,31);" \
                      "background-color: rgb(255, 255, 255);" \
                      "border:2px solid rgb(255,255,255);border-radius:15px;"

        self.ui.label.setStyleSheet(label_style)
        self.ui.label_2.setStyleSheet(label_style)
        self.ui.label_3.setStyleSheet(label_style)
        self.ui.label_4.setStyleSheet(label_style)

        # PushButton config
        button_style = "QPushButton{font: 25 13pt '微软雅黑 Light';color: rgb(255,255,255);" \
                       "background-color: rgb(20,196,188);" \
                       "border: none;border-radius:15px;}" \
                       "QPushButton:hover{background-color: rgb(22,218,208);}" \
                       "QPushButton:pressed{background-color: rgb(17,171,164);}"

        self.ui.pushButton.setStyleSheet(button_style)
        self.ui.pushButton_2.setStyleSheet(button_style)
        self.ui.pushButton_3.setStyleSheet(button_style)
        self.ui.pushButton_back.setStyleSheet(button_style)

        # background config
        background_image = QPixmap("background.png")
        background_image = background_image.scaled(850, 850)
        
        # alpha
        background_image2 = QPixmap(background_image.size())
        background_image2.fill(Qt.transparent) 
        painter = QPainter(background_image2)
        painter.setOpacity(0.6) 
        painter.drawPixmap(0, 0, background_image)
        painter.end()

        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(background_image2)) 
        self.setPalette(palette)

        # layout config
        frame_style = "background-color: rgb(255, 255, 255);" \
                      "border: 2px solid rgb(200,200,200);border-radius: 15px;"
        self.ui.formLayoutWidget.setStyleSheet(frame_style)

        # lineEdit config
        line_style = "font: 25 11pt '微软雅黑 Light';" \
                     "color: rgb(31,31,31);" \
                     "background-color: rgb(255, 255, 255);" \
                     "border:2px solid rgb(20,196,188);border-radius:15px;"
        self.ui.lineEdit.setStyleSheet(line_style)
        self.ui.lineEdit_2.setStyleSheet(line_style)
        self.ui.lineEdit_3.setStyleSheet(line_style)
        self.ui.lineEdit_4.setStyleSheet(line_style)
        
        # textEdit config
        textEdit_style = "font: 25 9pt '微软雅黑 Light';" \
                     "border:2px solid rgb(20,196,188);border-radius:15px;"
        self.ui.textEdit.setStyleSheet(textEdit_style)
        
    def display_message(self, message):
        """
        Displays a message in the textEdit widget.

        Parameters:
        - message (str): The message to be displayed.
        """
        self.ui.textEdit.setPlainText(self.ui.textEdit.toPlainText() + message + '\n')

    def get_walking_route(self):
        """
        Retrieves and displays a walking route based on user input.
        """
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
        """
        Retrieves and displays a riding route based on user input.
        """
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
        """
        Retrieves and displays a driving route based on user input.
        """
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
                    
                    
class MenuGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow_menu()
        self.ui.setupUi(self)
        self.setup_ui_style()

    # beautify GUI
    def setup_ui_style(self):
        # label config
        button_style = "QPushButton{font: 25 13pt '微软雅黑 Light';color: rgb(255,255,255);" \
                       "background-color: rgb(20,196,188);" \
                       "border: none;border-radius:15px;}" \
                       "QPushButton:hover{background-color: rgb(22,218,208);}" \
                       "QPushButton:pressed{background-color: rgb(17,171,164);}"

        self.ui.pushButton_r.setStyleSheet(button_style)
        self.ui.pushButton_m.setStyleSheet(button_style)
        self.ui.pushButton_quit.setStyleSheet(button_style)

        # background config
        background_image = QPixmap("background.png")
        background_image = background_image.scaled(850, 850)
        
        # alpha
        background_image2 = QPixmap(background_image.size())
        background_image2.fill(Qt.transparent) 
        painter = QPainter(background_image2)
        painter.setOpacity(0.6) 
        painter.drawPixmap(0, 0, background_image)
        painter.end()

        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(background_image2)) 
        self.setPalette(palette)

        # layout config
        frame_style = "background-color: rgb(255, 255, 255);" \
                      "border: 2px solid rgb(255,255,255);border-radius: 15px;"
        self.ui.verticalLayoutWidget.setStyleSheet(frame_style)

        # lineEdit config
        line_style = "color: rgb(31,31,31);" \
                     "background-color: rgb(255, 255, 255);" \
                    #  "border:2px solid rgb(20,196,188);border-radius:15px;"
        self.ui.lineEdit.setStyleSheet(line_style)

        
class SMapGUI(QMainWindow):
    def __init__(self, api_key):
        super().__init__()
        self.route = Map_API(api_key)
        self.ui = Ui_MainWindow_smap()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.get_image)
        self.setup_ui_style()

    # beautify GUI
    def setup_ui_style(self):
        # label config
        label_style = "font: 25 11pt '微软雅黑 Light';" \
                      "color: rgb(31,31,31);" \
                      "background-color: rgb(255, 255, 255);" \
                      "border:2px solid rgb(255,255,255);border-radius:15px;"

        self.ui.label.setStyleSheet(label_style)
        self.ui.label_2.setStyleSheet(label_style)

        # PushButton config
        button_style = "QPushButton{font: 25 14pt '微软雅黑 Light';color: rgb(255,255,255);" \
                       "background-color: rgb(20,196,188);" \
                       "border: none;border-radius:15px;}" \
                       "QPushButton:hover{background-color: rgb(22,218,208);}" \
                       "QPushButton:pressed{background-color: rgb(17,171,164);}"

        self.ui.pushButton_back.setStyleSheet(button_style)
        self.ui.pushButton.setStyleSheet(button_style)

        # background config
        background_image = QPixmap("background.png")
        background_image = background_image.scaled(850, 850)
        
        # alpha
        background_image2 = QPixmap(background_image.size())
        background_image2.fill(Qt.transparent) 
        painter = QPainter(background_image2)
        painter.setOpacity(0.6) 
        painter.drawPixmap(0, 0, background_image)
        painter.end()

        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(background_image2)) 
        self.setPalette(palette)

        # layout config
        frame_style = "background-color: rgb(255, 255, 255);" \
                      "border: 2px solid rgb(200,200,200);border-radius: 15px;"
        self.ui.gridLayoutWidget.setStyleSheet(frame_style)

        # lineEdit config
        line_style = "font: 25 11pt '微软雅黑 Light';" \
                     "color: rgb(31,31,31);" \
                     "background-color: rgb(255, 255, 255);" \
                     "border:2px solid rgb(20,196,188);border-radius:15px;"
        self.ui.lineEdit.setStyleSheet(line_style)

    def get_image(self):
        """
        Retrieves and displays a static map image based on user input.
        - Fetches the location, zoom level, and geocode.
        - Calls the get_static_map method from the Map_API class to obtain the map image.
        - Sets the map image to be displayed on the GUI.
        """
        location = self.ui.lineEdit.text()
        zoom = self.ui.spinBox.text()
        loc_geocode = self.route.get_geocode(location)
        size = '750*550'

        if loc_geocode:
            map_image = self.route.get_static_map(loc_geocode, zoom, size)
            pixmap = QPixmap()
            pixmap.loadFromData(map_image)
            self.ui.label_3.setPixmap(pixmap)
                    
