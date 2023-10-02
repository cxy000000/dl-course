import requests
from utils import WalkingRoute
    
if __name__ == "__main__":
    api_key = '1c5a6f863e2b10154c7ec8357f11f740' 
    
    ori_city = input('请输入出发点城市: ')
    ori_address = input('请输入出发点地址: ')
    des_city = input('请输入目的地城市: ')
    des_address = input('请输入目的地地址: ')

    route = WalkingRoute(api_key)
    ori_geocode = route.get_geocode(ori_address, ori_city)
    des_geocode = route.get_geocode(des_address, des_city)
    route.get_route(ori_geocode, des_geocode)