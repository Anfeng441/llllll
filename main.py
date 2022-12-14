import random
from time import localtime
from requests import get, post
from datetime import datetime, date
from zhdate import ZhDate
import sys
import os
import requests
 
 
def get_color():
    # 获取随机颜色
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)
 
 
def get_access_token():
    # appId
    app_id = config["app_id"]
    # appSecret
    app_secret = config["app_secret"]
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    try:
        access_token = get(post_url).json()['access_token']
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
        os.system("pause")
        sys.exit(1)
    # print(access_token)
    return access_token
 
 
def get_weather(region):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.113 Safari/537.36'
    }
    key = config["weather_key"]
    region_url = "https://free-api.heweather.com/s6/weather/forecast?location={}&key={}".format(region, key)
    response = get(region_url, headers=headers).json()
    print(response)

    # 获取地区的location--id
    location_id = response['HeWeather6'][0]["basic"]["cid"]
    weather_url = "https://free-api.heweather.com/s6/weather/forecast?location={}&key={}".format(location_id, key)
    response = get(weather_url, headers=headers).json()
    # 天气帅达版
    weather = '白天'+response['HeWeather6'][0]["daily_forecast"][0]["cond_txt_d"]+'，'+'傍晚'+response['HeWeather6'][0]["daily_forecast"][0]["cond_txt_n"]
    # 当前温度
    temp = response['HeWeather6'][0]["daily_forecast"][0]["tmp_min"]+ u"\N{DEGREE SIGN}" + "C"+'—'+response['HeWeather6'][0]["daily_forecast"][0]["tmp_max"]+ u"\N{DEGREE SIGN}" + "C"
def get_ciba():
    url = "http://open.iciba.com/dsapi/"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    r = get(url, headers=headers)
    note_en = r.json()["content"]
    note_ch = r.json()["note"]
    return note_ch, note_en
 
 
def send_message(to_user, access_token, region_name, weather, temp, xigua, wind_dir, note_ch, note_en):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]

