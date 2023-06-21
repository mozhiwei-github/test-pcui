import time
import requests
from selenium.common.exceptions import TimeoutException, NoSuchWindowException
from selenium.webdriver.support.wait import WebDriverWait
from office.contants import keniuofficeenvironment
from common import utils
from common.log import log
from office.contants import QQAccount



# 存储全局 driver WebDriverWait 实例
driver_wait_dict = {}

def driver_wait_until(driver, method, message='', wait_seconds=10, retries=1):
    """
    自定义 driver wait.util 函数
    @param driver: selenium浏览器driver
    @param method: wait.utils method
    @param message: wait.utils message
    @param wait_seconds: 等待超时时间，默认等待10秒
    @param retries: 重试次数，默认重试1次
    @return:
    """
    # 获取 WebDriverWait 实例
    global driver_wait_dict
    wait = driver_wait_dict.get(wait_seconds, None)
    if not wait:  # 没有相应 WebDriverWait 实例时创建
        wait = WebDriverWait(driver, wait_seconds)
        driver_wait_dict[wait_seconds] = wait

    # 执行 retries + 1 次等待
    for i in range(retries+1):
        try:
            wait.until(method, message)
            break
        except TimeoutException as e:
            if i >= retries:
                assert not e, log.log_error(f"等待超时且超过最大重试次数，{e}", need_assert=False, driver=driver)
            else:
                log.log_info(f"{message}等待超时，进行第{i+1}次重试")
                continue

def back_to_original_window(driver, original_window, assert_handles=True, window_count=1, scroll_top=True):
    """
    关闭新标签页，切换回原始标签页
    @param driver: selenium浏览器driver
    @param original_window: 原始窗口的ID
    @param assert_handles: 进行窗口数量断言检查
    @param window_count: 窗口数量
    @param scroll_top: 是否滚动到页面顶部
    @return:
    """
    if len(driver.window_handles) > 1:
        # 当前窗口句柄为原始窗口时，需要先切换到新标签页窗口
        if driver.current_window_handle == original_window:
            switch_to_new_window(driver, original_window)
        # 关闭新标签页
        driver.close()

    # 切换回原始标签页
    driver.switch_to.window(original_window)

    # 是否进行窗口数量断言检查
    if assert_handles:
        assert len(driver.window_handles) == window_count, "窗口数量检查失败"

    # 是否滚动到页面顶部
    if scroll_top:
        driver.execute_script("window.scrollTo(0, 0)")

    time.sleep(1)



def switch_to_new_window(driver, original_window):
    """
    切换到新标签页窗口
    @param driver: selenium浏览器driver
    @param original_window: 原始窗口的ID
    @return:
    """
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to_window(window_handle)
            break

def qq_login_operation(driver,original_window):
    """
    QQ登录界面操作
    @param driver: selenium浏览器driver
    @param original_window: 原始主页页面handle
    @return: QQ登录结果
    """
    # 采用账号密码形式登录

    driver.switch_to_frame('ptlogin_iframe')
    driver.find_element_by_xpath('//div[@id="bottom_qlogin"]/a[@id="switcher_plogin"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//input[@id="u"]').send_keys(QQAccount.QQNUM.value)
    time.sleep(1)
    driver.find_element_by_xpath('//input[@id="p"]').send_keys(QQAccount.QQPASSWORD.value)
    time.sleep(1)
    driver.find_element_by_xpath('//input[@id="login_button"]').click()
    time.sleep(2)
    try:
        driver.switch_to.default_content()
    except NoSuchWindowException as e:
        back_to_original_window(driver,original_window)
        if driver.current_window_handle == original_window:
            return True
    return False

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

def while_operation(self, try_max=30, photo_name=None, sim=0.8, retry=1):
    try_num = 1
    result = False
    while try_num < try_max:
        if utils.find_element_by_pic(
                self.get_page_shot(photo_name), sim=sim, retry=retry):
            result = True
            break
        try_num += 1
        utils.perform_sleep(1)
    return result

def send_request(envir, url, method, data=None, json=None, params=None):
    """
    @param env: 请求环境，正式服/测试服
    @param url: 请求url
    @return: response
    """
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
        "Content-Type": "application/json"
    }
    resp = None
    base_url = keniuofficeenvironment[envir].value + url
    if method == "POST":
        resp = requests.post(url=base_url, data=data, json=json, headers=headers)
    elif method == "GET":
        resp = requests.get(url=base_url, params=params, headers=headers)
    if resp.status_code == 200:
        return resp.json()


