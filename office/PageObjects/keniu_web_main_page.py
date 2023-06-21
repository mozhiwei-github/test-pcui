import random
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from common.webpage import page_method_record
from common.utils import find_element_by_pic
from common.webpage import WebPage
from office.contants import MainUrl,SearchWord
from office.conftest import *
import os


class KeniuWebMainPage(WebPage):
    # TODO:在类初始化的时候会给PageUrl和PageName赋值，但是此时为None，故实际打开不使用这个值
    PageUrl = os.getenv('URL')
    PageName = "可牛办公首页"
    def pre_open(self):
        right_url = os.getenv('URL')
        self.open_url(right_url)
        self.open_result = True

    @page_method_record("点击页面登录头像")
    def click_login(self):
        #self.find_element(By.XPATH,'//div[@class="icon_default_user icon"]',multiple=False)
        self.click((By.XPATH,'//div[@class="icon_default_user icon"]'))

    @page_method_record("判断登录窗口是否存在")
    def is_login_page_exist(self):
        return self.find_element((By.XPATH, '//div[@class="dialog_box"]'))

    @page_method_record("点击QQ登录")
    def click_qq_login(self):
        self.click((By.XPATH,'//div[@class="login_item"]'))
        time.sleep(1)

    @page_method_record("关闭界面开屏广告")
    def close_open_ad(self):
        is_ad_exist = self.find_element((By.XPATH,'//div[@class="summer_tips" and not(@style="display:none;"]'),multiple=False)
        if is_ad_exist:
            self.click((By.XPATH,'//div/span[@class="icon_close"]'))
        else:
            log.log_info("不存在开屏广告",screenshot=True)

    @page_method_record("点击首页列表随机一个模板的下载按钮")
    def click_list_to_detail(self):
        mainpage_module_list = self.find_element((By.XPATH,'//a[@class="flex_item model_item"]'),multiple=True)
        item = random.choice(mainpage_module_list)
        href = item.get_attribute("href")
        # default_module_id
        module_id = "default"
        if '=' in href:
            module_id = href.split('=')[1]
        elif '/t' in href:
            module_id = (href.split('/t/')[1]).split(".")[0]
        self.page_scroll_to_view(item)
        # 点击立即下载和点击模板都会跳转至详情页
        self.element_click(item,module_id,move_to_element=True)
        return href

    @page_method_record("判断页面中是否存在模板加载失败情况")
    def is_list_error_exist(self):
        load_status = True
        error_num = 0
        module_loading_list = None
        classify_list = self.find_element((By.XPATH,'//div[@class="home_content_classify"]'),multiple=True)
        for item in classify_list:
            self.page_scroll_to_view(item)
            time.sleep(1)
            current_time = time.time()
            while not module_loading_list:
                try:
                    module_loading_list = item.find_element_by_xpath('//a[@class="flex_item model_item"]//img[@lazy="loading"]')
                except NoSuchElementException as e :
                    break
                if time.time() > (current_time+30):
                    load_status = False
                    break
            try:
                module_error_list = item.find_element_by_xpath('//a[@class="flex_item model_item"]//img[@lazy="error"]')
            except NoSuchElementException as e :
                pass
            else:
                if module_error_list:
                    error_num += 1
        return [error_num,load_status]

    @page_method_record("判断首页顶部banner是否存在加载失败情况")
    def is_banner_error_exist(self):
        load_status = True
        error_num = 0
        banner_loading_list = None
        banner_list = self.find_element((By.XPATH,'//div[@class="swiper_box"]/div[@class="content_box"]/div/div/a'),multiple=True)
        for item in banner_list:
            current_time = time.time()
            while not banner_loading_list:
                try:
                    banner_loading_list = item.find_element_by_xpath('/div[@lazy="loading"]')
                except NoSuchElementException as e:
                    break
                if time.time() > (current_time+30):
                    load_status = False
                    break
            try:
                banner_error_list = item.find_element_by_xpath('/div[@lazy="error"]')
            except NoSuchElementException as e:
                pass
            else:
                if banner_error_list:
                    error_num += 1

        return [error_num, load_status]

    @page_method_record("点击首页banner")
    def click_banner(self):
        banner_list = self.find_element((By.XPATH,'//div[@class="swiper_box"]/div[@class="content_box"]/div/div/a/div[@lazy="loaded"]'),multiple=True)
        #item = random.choice(banner_list)
        item = banner_list[1]
        self.click_element_if_clickable(item,retries=10)

    @page_method_record("判断页面是否存在支付窗")
    def is_buy_windows_exist(self):
        buy_window = self.find_element((By.XPATH,'//div[@class="buy_dialog_box"]'))
        if not buy_window:
            return False
        return True

    @page_method_record("关闭支付窗")
    def close_buy_window(self):
        self.click((By.XPATH,'//div[@class="buy_body"]//span[@class="common_close close_btn"]'))

    @page_method_record("在首页搜索框输入关键词搜索")
    def search_input_click(self):
        self.input_text((By.XPATH,'//div[@class="search_box home_search_box"]/input[@class="input"]'),
                        text="总结")
        self.click((By.XPATH,'//div[@class="search_box home_search_box"]/button[@class="btn reset_btn cf-btn"]'))



















