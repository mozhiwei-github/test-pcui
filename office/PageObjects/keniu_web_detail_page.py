from common.log import log
from common.webpage import WebPage
from selenium.webdriver.common.by import By

class KeniuWebDetailPage(WebPage):

    def __init__(self,driver,do_pre_open=False):
        self.driver = driver
        log.log_info("driver tab 切换至详情页")

    def click_download(self):
        """在详情页中点击下载按钮"""
        # TODO：如何判断文件是否下载完成？
        self.click((By.XPATH,'//div[@class="right_down"]/button[@class="down_btn cf-btn"]'))
