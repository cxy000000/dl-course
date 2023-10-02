import requests

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
                    for route in data['route']['paths']:
                        distance = route['distance']  # 步行距离（米）
                        duration = route['duration']  # 步行时间（秒）
                        print(f'步行距离: {distance}米')
                        print(f'步行时间: {duration}秒')
                        print('步行路线:')
                        for step in route['steps']:
                            instruction = step['instruction']
                            print(f'- {instruction}')
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
                        print(f'坐标点: {location}')
                        return location
                    else:
                        print('未找到匹配的地址')
                else:
                    print('请求失败')
            else:
                print('请求失败')
        except Exception as e:
            print(f'发生异常: {str(e)}')


