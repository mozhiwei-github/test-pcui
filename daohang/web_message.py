import json
from common.log import log
import requests


"""
针对浏览器页面的cookies和local storage进行获取和更改
"""

def get_cookies(driver):
    """
    获取当前页面cookies方法
    @param driver: driver对象
    @return cookies_dict
    """
    cookies_dict = {}
    cookies = driver.get_cookies() # list
    for cookie in cookies:
        cookies_dict[cookie['name']] = cookie['value']
    return cookies_dict

def get_localStorage(driver):
    """
    获取当前页面localStorage方法
    @param driver: driver对象
    @return localStorage_dict
    """
    localStorage_dict = driver.execute_script('return window.localStorage') # dict

    return localStorage_dict


def get_cookie_value(driver,key):
    """
    @param driver: driver对象
    @param key: cookie_key
    @return value: cookie_value
    """
    cookies_dict = get_cookies(driver)
    if key in cookies_dict.keys():
        cookie_value = cookies_dict[key]
    else:
        log.log_error(f"该cookie—key{key}不存在")
    return cookie_value

def set_cookie_value(driver,key,value):
    """
    @param driver: driver对象
    @param key: cookie_key
    @param value: cookie_value
    """
    cookies_dict = get_cookies(driver)
    driver.add_cookie({"name":key,"value":value})

def get_localStorage_value(driver,key):
    """
    @param driver: driver对象
    @param key: localStorage_key
    @return localStorage_value
    """
    localStorage_dict = get_localStorage(driver)
    if key in localStorage_dict.keys():
        localStorage_value = localStorage_dict[key]
    else:
        log.log_error(f"该localStorage{key}不存在")
    return localStorage_value

def set_localStorage_value(driver,key,value):
    """
    @param driver: driver对象
    @param key: localStorage_key
    @param value: localStorage_value
    """
    localStorage_dict = get_localStorage(driver)

    driver.execute_script(f'localStorage.setItem("{key}","{value}")')

def get_page_configs(env,channel):
    request_url = f"{env}/api_json.html"
    #ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    # header = {
    #     'User-Agent' : ua
    # }
    if channel[1:].split('.')[0] == 'index':
        channel = "home"
    else:
        channel = channel[1:].split('.')[0]
    data = {
        'pi': 8,
        'channel': channel,
        'pwd': 'E0AC84CD8254ED41187FD517EB57A060'
    }
    # channel[1:].split('.')[0]
    #response = requests.get(url=request_url,headers=header,params=params)
    response = requests.get(url=request_url, params=data)
    response_json = json.loads(response.text)
    return response_json

def get_ad_sort(env,channel):
    online_open_ad_list = ['ad63','ad64','ad58','ad46']
    test_open_ad_list = ['']
    open_ad_status = False
    response_json = get_page_configs(env,channel)
    adrule_key = "jrhd_gg_sort"
    if adrule_key not in response_json.keys() :
        log.log_error(f"未配置广告队列",need_assert=False)
    else:
        ad_sort_rule = response_json[adrule_key]   # str
        ad_sort_len = len(ad_sort_rule)  # 存在的广告加载梯队个数
        if env in ["https://www.duba.com", "https://www.newduba.cn"]:
            open_ad_list = online_open_ad_list
        else:
            open_ad_list = test_open_ad_list
        for ad in open_ad_list:
            if ad in ad_sort_rule: #判断广告是否存在广告队列中
                open_ad_status = True
    return open_ad_status



