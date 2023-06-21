from common import utils
from common.basepage import BasePage, page_method_record
from common.log import log
from common.utils import win32gui, win32con
import os
from office.utils import while_operation
from office.contants import QQAccount, keniuofficePath
import random

def is_keniuOfficePage_exist():
    keniuoffice_page_logo_path = os.path.join(os.getcwd(), 'office', 'PageShot', 'keniuoffice_client_page', 'keniuoffice_page_logo.png')
    try_num = 1
    while try_num < 30:
        if utils.find_element_by_pic(
                keniuoffice_page_logo_path, sim=0.8, retry=1)[0]:
            break
        try_num += 1
        utils.perform_sleep(1)
    if try_num >= 30:
        return False
    return True

def close_keniuOfficePage():
    keniuoffice_page_logo_path = os.path.join(os.getcwd(), 'office', 'PageShot', 'keniuoffice_client_page', 'keniuoffice_page_logo.png')
    class_name = "KWebxMainWindow-{FD4C5916-356D-42D1-A0C5-EEC12ABF817A}"
    file_hwnd = utils.get_hwnd_by_class(class_name, title=None)
    win32gui.SetForegroundWindow(file_hwnd)
    win32gui.PostMessage(file_hwnd, win32con.WM_CLOSE, 0, 0)
    utils.perform_sleep(3)
    if utils.find_element_by_pic(
                keniuoffice_page_logo_path, sim=0.8, retry=1)[0]:
        return False
    return True

def judge_local_inputtype():
    # 判断本地当前输入法
    chinese_path = os.path.join(os.getcwd(), 'office', 'PageShot', 'input_type', 'input_Chinese.png')
    english_path = os.path.join(os.getcwd(), 'office', 'PageShot', 'input_type', 'input_English.png')
    if utils.find_element_by_pic(chinese_path, sim=0.8, retry=5)[0]:
        return "Chinese"
    elif utils.find_element_by_pic(english_path, sim=0.8, retry=5)[0]:
        return "English"
    else:
        return None

class KeniuOfficeClientPage(BasePage):

    def pre_open(self):
        keniuoffice_path = os.path.join(keniuofficePath.DEFAULTINSTALLPATH.value, 'ktemplate.exe')
        utils.process_start(keniuoffice_path, async_start=True)

    @page_method_record("关闭可牛办公界面")
    def close_keniuoffice_page(self):
        try_num = 1
        while try_num < 30:
            if utils.find_element_by_pic(
                    self.get_page_shot("keniuoffice_page_logo.png"), sim=0.8, retry=1)[0]:
                class_name = "KWebxMainWindow-{FD4C5916-356D-42D1-A0C5-EEC12ABF817A}"
                file_hwnd = utils.get_hwnd_by_class(class_name, title=None)
                win32gui.SetForegroundWindow(file_hwnd)
                win32gui.PostMessage(file_hwnd, win32con.WM_CLOSE, 0, 0)
                break
            try_num += 1
            utils.perform_sleep(1)
        if try_num >= 30:
            log.log_error("未匹配到可牛办公应用界面")
            return False
        utils.perform_sleep(2)
        if not utils.find_element_by_pic(self.get_page_shot("keniuoffice_page_logo.png"), sim=0.8, retry=2)[0]:
            log.log_info("可牛办公界面关闭成功")
            return True
        log.log_info("可牛办公界面未正常关闭")
        return False

    @page_method_record("验证页面是否展示异常")
    def is_page_show_normal(self, need_wait=True):
        if need_wait:
            return while_operation(self, photo_name="keniuoffice_page_error.png")
        else:
            return utils.find_element_by_pic(
                self.get_page_shot("keniuoffice_page_error.png"), sim=0.8, retry=5)[0]

    @page_method_record("点击登录头像")
    def click_login_tab(self):
        return utils.click_element_by_pic(
            self.get_page_shot("login_tab.png"), sim=0.8, retry=5)

    @page_method_record("判断登录窗是否存在")
    def is_loginPage_exist(self):
        return while_operation(self, photo_name="login_page_logo.png")

    @page_method_record("判断QQ登录窗是否存在")
    def is_qqLoginPage_exist(self):
        if not while_operation(self, photo_name="qq_login_page_logo.png"):
            if not while_operation(self, photo_name="qq_loginpage_logo_2.png"):
                return False
        return True

    @page_method_record("点击登录窗口的QQ登录按钮")
    def click_qq_login(self):
        utils.click_element_by_pic(
            self.get_page_shot("qq_login_logo.png"), sim=0.8, retry=5)

    @page_method_record("点击主页logo")
    def click_keniuoffice_page_logo(self):
        utils.click_element_by_pic(
            self.get_page_shot("keniuoffice_page_logo.png"), sim=0.8, retry=5)

    @page_method_record("点击选择qq登录窗口的账号密码登录")
    def click_login_by_account_button(self):
        utils.click_element_by_pic(
            self.get_page_shot("login_by_account.png"), sim=0.8, retry=5)

    @page_method_record("点击个人中心tab")
    def click_user_center(self):
        utils.click_element_by_pic(
            self.get_page_shot("tab_user_center.png"), sim=0.8, retry=5)

    @page_method_record("点击QQ登录窗口的登录按钮")
    def click_qqlogin_button(self):
        utils.click_element_by_pic(
            self.get_page_shot("qq_login_button.png"), sim=0.8, retry=5)

    @page_method_record("点击qq登录号码密码输入框并输入内容")
    def enter_account(self):
        if judge_local_inputtype() == "Chinese":
            utils.keyboardInputByCode('left_shift')
        if not utils.find_element_by_pic(
                self.get_page_shot("qq_login_with_num.png"), sim=0.8, retry=5)[0]:
            utils.click_element_by_pic(
                self.get_page_shot("qq_login_num.png"), sim=0.8, retry=5)
            for i in QQAccount.QQNUM.value:
                utils.keyboardInputByCode(i)
                utils.perform_sleep(0.5)
        utils.click_element_by_pic(
            self.get_page_shot("qq_login_password.png"), sim=0.8, retry=5)
        for i in QQAccount.QQPASSWORD.value:
            utils.keyboardInputByCode(i)
            utils.perform_sleep(0.5)

    @page_method_record("QQ登录")
    def login_by_qq(self):
        self.click_login_tab()
        if not self.is_loginPage_exist():
            log.log_error("登录页面不存在")
        utils.perform_sleep(2)
        self.click_qq_login()
        if not self.is_qqLoginPage_exist():
            log.log_error("QQ登录窗不存在")
        utils.perform_sleep(1)
        self.click_login_by_account_button()
        if not utils.find_element_by_pic(
            self.get_page_shot("qq_login_button.png"), sim=0.8, retry=3)[0]:
            log.log_error("qq使用账号登录界面展示异常")
        utils.perform_sleep(1)
        self.enter_account()
        utils.perform_sleep(1)
        self.click_qqlogin_button()

    @page_method_record("判断当前是否已登录且位于首页")
    def is_main_page_with_login(self):
        return utils.find_element_by_pic(
            self.get_page_shot("vip_logo.png"), sim=0.95, retry=1)[0]

    @page_method_record("随机点击页面中的立即下载按钮")
    def click_download_button(self):
        result, pos_list = utils.find_elements_by_pic(
            self.get_page_shot("download_button.png"), sim=0.8, retry=3)
        num = random.randint(1, len(pos_list))
        utils.mouse_click(pos_list[num][0], pos_list[num][1])

    @page_method_record("随机点击页面中的收藏按钮")
    def click_collection_button(self):
        result, pos_list = utils.find_elements_by_pic(
            self.get_page_shot("collection_button.png"), sim=0.8, retry=3)
        num = random.randint(1, len(pos_list)-1)
        utils.mouse_click(pos_list[num][0], pos_list[num][1])

    @page_method_record("点击左侧word模板tab")
    def click_leftnav_word(self):
        utils.click_element_by_pic(
            self.get_page_shot("leftnav_word.png"), sim=0.8, retry=5)

    @page_method_record("点击左侧ppt模板tab")
    def click_leftnav_ppt(self):
        utils.click_element_by_pic(
            self.get_page_shot("leftnav_ppt.png"), sim=0.8, retry=5)

    @page_method_record("点击左侧excel模板tab")
    def click_leftnav_excel(self):
        utils.click_element_by_pic(
            self.get_page_shot("leftnav_excel.png"), sim=0.8, retry=5)

    @page_method_record("点击左侧design模板tab")
    def click_leftnav_design(self):
        utils.click_element_by_pic(
            self.get_page_shot("leftnav_design.png"), sim=0.8, retry=5)

    @page_method_record("点击左侧sucai模板tab")
    def click_leftnav_sucai(self):
        utils.click_element_by_pic(
            self.get_page_shot("leftnav_sucai.png"), sim=0.8, retry=5)

    @page_method_record("点击左侧我的下载tab")
    def click_leftnav_mydownload(self):
        utils.click_element_by_pic(
            self.get_page_shot("leftnav_mydownload.png"), sim=0.8, retry=5)

    @page_method_record("点击左侧我的收藏tab")
    def click_leftnav_mycollection(self):
        utils.click_element_by_pic(
            self.get_page_shot("leftnav_mycollection.png"), sim=0.8, retry=5)

    @page_method_record("判断分类tab页面是否展示正常")
    def is_tab_page_normal(self):
        if self.is_page_show_normal(need_wait=False):
            log.log_info("页面展示error")
            return False
        self.scroll_list()
        return utils.find_element_by_pic(
            self.get_page_shot("first_page.png"), sim=0.95, retry=5)[0]

    @page_method_record("判断MY页面是否展示正常")
    def is_my_page_normal(self):
        return utils.find_element_by_pic(
            self.get_page_shot("my_tab.png"), sim=0.8, retry=5)[0]

    @page_method_record("判断我的下载中是否存在新增记录标记")
    def is_more_download(self):
        return utils.find_element_by_pic(
            self.get_page_shot("leftnav_mydownload_with_tag.png"), sim=0.8, retry=5)[0]

    @page_method_record("判断当前页面是否存在已收藏按钮")
    def is_collected_button_exist(self):
        return utils.find_elements_by_pic(
            self.get_page_shot("collection_button_with.png"), sim=0.8, retry=5)

    @page_method_record("点击搜索框搜索按钮")
    def click_search_button(self):
        utils.click_element_by_pic(
            self.get_page_shot("search_button.png"), sim=0.8, retry=5)

    @page_method_record("点击顶部主页tab")
    def click_mainpage_tab(self):
        utils.click_element_by_pic(
            self.get_page_shot("main_page_tab.png"), sim=0.8, retry=5)

    @page_method_record("滚动tab列表")
    def scroll_list(self):
        utils.mouse_move(self.position[0]+500, self.position[1]+400)
        while True:
            if utils.find_element_by_pic(self.get_page_shot("first_page.png"), sim=0.95, retry=1)[0]:
                log.log_info("已到达页面底部")
                break
            else:
                utils.mouse_scroll(250)















