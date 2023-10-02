import requests
import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import Style


class WalkingRoute:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_route(self, origin, destination):
        url = f'https://restapi.amap.com/v3/direction/walking?origin={origin}&destination={destination}&key={self.api_key}'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == '1':
                    routes = list(route for route in data['route']['paths'])
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
                        # print(f'坐标点: {location}')
                        return location
                    else:
                        print('未找到匹配的地址')
                else:
                    print('请求失败')
            else:
                print('请求失败')
        except Exception as e:
            print(f'发生异常: {str(e)}')


class WalkingRouteGUI(WalkingRoute):
    def __init__(self, root, api_key):
        super().__init__(api_key)
        style = Style()
        style = Style(theme='sandstone')
        #主题可替换为：['vista', 'classic', 'cyborg', 'journal', 'darkly', 'flatly', 'clam', 'alt', 'solar', 'minty', 'litera', 'united', 'xpnative', 'pulse', 'cosmo', 'lumen', 'yeti', 'superhero', 'winnative', 'sandstone', 'default']
        TOP6 = style.master
        self.root = root
        self.root.title("Walking Route")

        # 出发点城市和地址输入框
        self.ori_city_label = tk.Label(root, text="出发点城市:")
        self.ori_city_label.pack()
        self.ori_city_entry = tk.Entry(root)
        self.ori_city_entry.pack()
        self.ori_address_label = tk.Label(root, text="出发点地址:")
        self.ori_address_label.pack()
        self.ori_address_entry = tk.Entry(root)
        self.ori_address_entry.pack()

        # 目的地城市和地址输入框
        self.des_city_label = tk.Label(root, text="目的地城市:")
        self.des_city_label.pack()
        self.des_city_entry = tk.Entry(root)
        self.des_city_entry.pack()
        self.des_address_label = tk.Label(root, text="目的地地址:")
        self.des_address_label.pack()
        self.des_address_entry = tk.Entry(root)
        self.des_address_entry.pack()

        # 步行路径规划按钮
        self.route_button = tk.Button(root, text="步行路径规划", command=self.get_walking_route)
        self.route_button.pack()
        
        # 结果显示文本框
        self.result_text = tk.Text(root, state=tk.DISABLED, height=30, width=40)
        self.result_text.pack()
        
    def display_message(self, message):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, message + '\n')
        self.result_text.config(state=tk.DISABLED)

    def get_walking_route(self):
        ori_city = self.ori_city_entry.get()
        ori_address = self.ori_address_entry.get()
        des_city = self.des_city_entry.get()
        des_address = self.des_address_entry.get()

        ori_geocode = self.get_geocode(ori_address, ori_city)
        self.display_message(f'出发点坐标: {ori_geocode}')
        des_geocode = self.get_geocode(des_address, des_city)
        self.display_message(f'目的地坐标: {des_geocode}')

        if ori_geocode and des_geocode:
            routes = self.get_route(ori_geocode, des_geocode)
            for route in routes:
                distance = route['distance']  # 步行距离（米）
                duration = route['duration']  # 步行时间（秒）
                self.display_message(f'步行距离: {distance}米')
                self.display_message(f'步行时间: {duration}秒')
                self.display_message('步行路线:')
                for step in route['steps']:
                    instruction = step['instruction']
                    self.display_message(f'- {instruction}')

