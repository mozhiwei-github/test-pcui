# --coding = 'utf-8' --
from common.basepage import BasePage, page_method_record
from common import utils
from common.log import log
from common.unexpectwin_system import UnExpectWin_System
from common.utils import perform_sleep, win32gui, win32con
from duba.PageObjects.main_page import main_page
from duba.PageObjects.c_slimming_page import CreateGarbage
from duba.contants import Software_manage_operation
from duba.utils import while_operation
import os
"""软件管家页"""

product_path = os.path.join(os.getcwd(), "duba", "PageShot", "software_manage_page")

class SoftWareManagePage(BasePage):
    def pre_open(self):
        # TODO：执行打开动作
        self.mp = main_page()
        self.mp.software_manager_click()

    @page_method_record("点击卸载页tab")
    def click_uninstall_tab(self):
        utils.click_element_by_pic(self.get_page_shot("uninstall_tab.png"), sim=0.8, retry=3)
        utils.perform_sleep(2)
        while not utils.find_element_by_pic(
                self.get_page_shot("uninstall_page_uninstall_button.png"), sim=0.8, retry=2)[0] \
                and utils.find_element_by_pic(
                    self.get_page_shot("uninstall_page_logo.png"), sim=0.8, retry=2)[0]:
            utils.click_element_by_pic(self.get_page_shot("uninstall_tab.png"), sim=0.9, retry=3)

    @page_method_record("点击升级页tab")
    def click_update_tab(self):
        utils.click_element_by_pic(self.get_page_shot("update_tab.png"), sim=0.9, retry=3)

    @page_method_record("点击全部页tab")
    def click_all_tab(self):
        utils.click_element_by_pic(self.get_page_shot("all_tab.png"), sim=0.9, retry=3)

    @page_method_record("点击主页logo")
    def click_logo(self):
        utils.click_element_by_pic(self.get_page_shot("software_manage_logo.png"), sim=0.9, retry=3)

    @page_method_record("点击游戏页tab")
    def click_game_tab(self):
        utils.click_element_by_pic(self.get_page_shot("game_tab.png"), sim=0.9, retry=3)

    @page_method_record("点击首页tab")
    def click_mainpage_tab(self):
        utils.click_element_by_pic(self.get_page_shot("main_page_tab.png"), sim=0.9, retry=3)

    @page_method_record("点击权限管理tab")
    def click_permission_tab(self):
        utils.click_element_by_pic(self.get_page_shot("permission_manage_tab.png"), sim=0.9, retry=3)

    @page_method_record("准备前置软件")
    def create_software(self):
        winRAR = CreateGarbage()
        winRAR.create_garbage()

    @page_method_record("检查卸载功能")
    def check_uninstall(self):
        ...

    @page_method_record("检查轮播位置是否正常轮播")
    # 仅能确定轮播是否正常，未判断轮播内容是否正常
    def is_shlidshow_normal(self):
        result, logo_pos = utils.find_element_by_pic(self.get_page_shot("software_manage_logo.png"))
        if not result:
            return False
        color_list = []
        same_num, sum_num, diff_num = 0, 0, 0
        for i in range(1,30):
            sum_num += 1
            point_left = utils.get_pic_coordinates_color(logo_pos[0]+250, logo_pos[1]+125)
            point_center = utils.get_pic_coordinates_color(logo_pos[0]+400, logo_pos[1]+130)
            color_point = (point_left, point_center)
            if color_point in color_list:
                same_num += 1
            else:
                color_list.append(color_point)
                diff_num += 1
            # 轮播时间间隔为3s
            utils.perform_sleep(2.7)
        specific_value = diff_num/sum_num
        if specific_value < 0.5 and len(color_list) >= 6:
            return True
        return False

    @page_method_record("判断界面展示是否为异常页面")
    def is_page_show_normal(self):
        if utils.find_element_by_pic(self.get_page_shot("software_manage_logo.png"))[0]:
            utils.perform_sleep(1)
            if not (utils.find_element_by_pic(
                    self.get_page_shot("page_show_error.png"), sim=0.8, retry=2)[0] or
                utils.find_element_by_pic(
                    self.get_page_shot("page_show_internet_error.png"), sim=0.8, retry=2)[0]):
                return True
        return False

    @page_method_record("点击首页的刷新按钮")
    def click_reload_button(self):
        utils.click_element_by_pic(self.get_page_shot("reload_button.png"), sim=0.8, retry=2)

    @page_method_record("在首页查找可牛办公tab并点击进行安装")
    def install_keniuoffice_from_mainpage(self):
        # 点击首页logo返回主页确保页面位于首页
        utils.click_element_by_pic(
            self.get_page_shot("software_manage_logo.png"), sim=0.8, retry=3)
        utils.perform_sleep(1)
        # 切换分类至办公必备
        utils.click_element_by_pic(self.get_page_shot("office_category_tab.png"), sim=0.85, retry=3)
        utils.perform_sleep(1)
        result, pos_list = utils.find_elements_by_pic(
            self.get_page_shot("keniuoffice_logo.png"), sim=0.8, retry=2)
        if result:
            utils.mouse_click(pos_list[0][0]+60, pos_list[0][1]+15)
            utils.perform_sleep(3)
            if while_operation(
                product_path=product_path, photo_name="keniuoffice_install_page.png", sim=0.8, retry=3):
                if self.keniuoffice_install():
                    return True
        return False

    @page_method_record("可牛办公软件安装")
    def keniuoffice_install(self):
        utils.perform_sleep(2)
        if not while_operation(
            product_path=product_path, photo_name="keniuoffice_install_page.png", sim=0.7, retry=1):
            log.log_error("未匹配到可牛办公安装界面")
            return False
        utils.click_element_by_pic(
            self.get_page_shot("keniuoffice_install_button.png"), sim=0.8, retry=5)
        log.log_info("点击可牛办公安装界面的安装按钮")
        if not while_operation(
            product_path=product_path, photo_name="keniuoffice_install_finished.png", sim=0.8, retry=1):
            log.log_error("未匹配到可牛办公安装完成按钮")
            return False
        log.log_info("可牛办公软件安装完成")
        utils.click_element_by_pic(
            self.get_page_shot("keniuoffice_install_finished.png"), sim=0.8, retry=2)
        utils.perform_sleep(3)

        if not while_operation(
            product_path=product_path, photo_name="keniuoffice_page_logo.png", sim=0.8, retry=1):
            log.log_error("未匹配到可牛办公应用界面")
            return False
        class_name = "KWebxMainWindow-{FD4C5916-356D-42D1-A0C5-EEC12ABF817A}"
        file_hwnd = utils.get_hwnd_by_class(class_name, title=None)
        win32gui.SetForegroundWindow(file_hwnd)
        win32gui.PostMessage(file_hwnd, win32con.WM_CLOSE, 0, 0)

        utils.perform_sleep(2)
        if not utils.find_element_by_pic(self.get_page_shot("keniuoffice_page_logo.png"), sim=0.8, retry=2)[0]:
            log.log_info("可牛办公界面关闭成功")
            return True
        log.log_info("可牛办公界面未正常关闭")
        return False

    @page_method_record("在首页查找腾讯视频tab并点击进行安装")
    def install_tencent_video_from_mainpage(self):
        # 切换至看视频分类tab以查找腾讯视频
        utils.click_element_by_pic(self.get_page_shot("video_category_tab.png"), sim=0.8, retry=1)
        utils.perform_sleep(1)
        result, pos_list = utils.find_elements_by_pic(self.get_page_shot("tencentvideo_logo.png"), sim=0.8, retry=2)
        if result:
            utils.mouse_click(pos_list[0][0] + 60, pos_list[0][1] + 15)
            self.judge_pop_detect()
            if self.tencentvideo_install():
                return True
        return False

    @page_method_record("腾讯视频软件安装")
    def tencentvideo_install(self):
        used_time = 0
        install_status = False
        # 暂定腾讯视频能在60s内安装完成
        while used_time < 90:
            UnExpectWin_System().unexpectwin_detect()
            if utils.is_reg_exist(regpath=r'SOFTWARE\WOW6432Node\Tencent\qqlive'):
                install_status = True
                break
            used_time += 1
            utils.perform_sleep(1)
        if used_time >= 60:
            log.log_error("腾讯视频安装1min30s内未安装完成")
            return False
        if install_status:
            return True
        return False

    @page_method_record("在卸载页面卸载可牛办公软件")
    def uninstall_keniuoffice(self):
        keniuoffice_photo = "keniuoffice_logo2.png"
        operation_name = "UNINSTALL"
        result = self.scroll_pagelist(keniuoffice_photo, operation_name)
        utils.perform_sleep(1)
        if result:
            utils.mouse_click(result[0], result[1])
            utils.perform_sleep(2)
        if not self.keniuoffice_uninstall():
            return False
        return True

    @page_method_record("可牛办公软件卸载")
    def keniuoffice_uninstall(self):
        utils.perform_sleep(3)
        if utils.find_element_by_pic(
                self.get_page_shot("keniuoffice_uninstall_page.png"), sim=0.8, retry=5)[0]:
            utils.click_element_by_pic(
                self.get_page_shot("keniuoffice_uninstall_button.png"), sim=0.8, retry=1)
        else:
            log.log_error("未匹配到可牛办公卸载界面")
            return False

        if not while_operation(
                product_path=product_path, photo_name="keniuoffice_uninstall_finished.png", sim=0.8, retry=1):
            log.log_error("未匹配到可牛办公卸载完成按钮")
            return False
        utils.click_element_by_pic(
            self.get_page_shot("keniuoffice_uninstall_finished.png"), sim=0.8, retry=3)

        if not utils.find_element_by_pic(
                self.get_page_shot("keniuoffice_uninstall_page_logo.png"), sim=0.8, retry=2)[0]:
            return True
        return False

    @page_method_record("卸载腾讯视频软件")
    def uninstall_tencentvideo(self):
        tencentvideo_photo = "tencentvideo_logo2.png"
        operation_name = "UNINSTALL"
        result = self.scroll_pagelist(tencentvideo_photo, operation_name)
        if result:
            utils.mouse_click(result[0], result[1])
        if not self.tencentvideo_uninstall():
            return False
        return True

    @page_method_record("腾讯视频软件卸载")
    def tencentvideo_uninstall(self):
        if not while_operation(
            product_path=product_path, photo_name="tencentvideo_uninstall_page_logo.png", sim=0.8, retry=1):
            log.log_error("未匹配到腾讯视频卸载界面")
            return False

        utils.click_element_by_pic(
            self.get_page_shot("tencentvideo_uninstall_page_uninstall_button.png"), sim=0.8, retry=2)
        utils.perform_sleep(1)
        utils.click_element_by_pic(
            self.get_page_shot("tencentvideo_uninstall_page_uninstall_button2.png"), sim=0.8, retry=2)

        if not while_operation(
                product_path=product_path, photo_name="tencentvideo_uninstall_page_sure_button.png", sim=0.8, retry=1):
            log.log_error("未匹配到腾讯视频卸载过程按钮")
            return False
        utils.perform_sleep(1)
        utils.click_element_by_pic(
            self.get_page_shot("tencentvideo_uninstall_page_uninstall_button3.png"), sim=0.8, retry=5)

        self.judge_pop_detect()
        while True:
            result1, pos1 = utils.find_element_by_pic(self.get_page_shot("tencentvideo_uninstall_page_close_button.png"), sim=0.9, retry=1)
            result2, pos2 = utils.find_element_by_pic(self.get_page_shot("tencentvideo_uninstall_page_close_button2.png"), sim=0.9, retry=1)
            if result1 or result2:
                break
            utils.perform_sleep(1)
            # UnExpectWin_System().unexpectwin_detect()
        if result1:
            utils.mouse_click(pos1[0],pos1[1])
        elif result2:
            utils.mouse_click(pos2[0],pos2[1])
        utils.perform_sleep(2)
        if utils.is_reg_exist(regpath=r'SOFTWARE\WOW6432Node\Tencent\qqlive'):
           return False
        return True

    @page_method_record("滚动页面列表至指定软件处")
    def scroll_pagelist(self, software_path, operation):
        """
        @param software_path: 要滚动列表至该软件处的软件图标截图
        @param operation: 找到软件后要差进行的操作---用于区分卸载uninstall/安装install/升级update
        @return:返回指定按钮的坐标
        """
        page_result, page_pos = utils.find_element_by_pic(
            self.get_page_shot("software_manage_logo.png"), sim=0.8,retry=1)
        assert page_result,log.log_error("软件管家界面展示异常")
        utils.mouse_move(page_pos[0]+450, page_pos[1]+350)
        while True:
            software_result, software_pos = utils.find_element_by_pic(
                self.get_page_shot(software_path), sim=0.9, retry=1)
            if not software_result:
                utils.mouse_scroll(150)
                continue
            button_result, button_pos = utils.find_elements_by_pic(
                self.get_page_shot(self.get_operation_name(operation)), sim=0.8, retry=2)
            assert button_result, log.log_error("未匹配到对应按钮")
            for real_pos in button_pos:
                gap = real_pos[1] - software_pos[1]
                if gap <= 3 and gap >= -3:
                    return real_pos

    @page_method_record("匹配operation对应键值")
    def get_operation_name(self, operation):
        operation_name = ""
        operation_name_list = Software_manage_operation.operation_dict.value
        for i in operation_name_list:
            if i[0] == operation:
                operation_name = i[1]
        return operation_name

    @page_method_record("卸载可牛办公和腾讯视频软件")
    # 由于多个场景涉及她两的卸载作为前置条件，故将二者绑定卸载作为调用
    def uninstall_keniuoffice_and_tencentvideo(self):
        # 切换至卸载tab
        self.click_all_tab()
        utils.perform_sleep(1)
        self.click_uninstall_tab()
        if not utils.find_element_by_pic(
                self.get_page_shot("uninstall_page_logo.png"), sim=0.8, retry=2)[0]:
            log.log_error("未匹配到卸载界面logo")
            return False
        utils.perform_sleep(1)
        if not self.is_page_show_normal():
            log.log_error("卸载tab界面未正常展示")
        log.log_pass("卸载tab界面展示正常")
        utils.click_element_by_pic(
            self.get_page_shot("uninstall_page_setting_menu.png"), sim=0.8, retry=3)
        utils.perform_sleep(1)
        utils.click_element_by_pic(
            self.get_page_shot("uninstall_page_sort_by_name.png"), sim=0.8, retry=3)
        if not self.uninstall_keniuoffice():
            log.log_error("可牛办公软件卸载异常")
        log.log_pass("可牛办公软件卸载完成")
        utils.perform_sleep(3)
        self.click_logo()
        utils.perform_sleep(1)
        self.click_reload_button()
        utils.perform_sleep(1)
        self.click_uninstall_tab()
        if not self.uninstall_tencentvideo():
            log.log_error("腾讯视频软件卸载异常")
        log.log_pass("腾讯视频软件卸载完成")

    @page_method_record("在搜索框中输入指定内容并回车搜索")
    def search_input(self, input_word):
        result, pos = utils.find_element_by_pic(
            self.get_page_shot("search.png"), sim=0.8, retry=1)
        result2, pos2 = utils.find_element_by_pic(
            self.get_page_shot("search_button.png"), sim=0.8, retry=1)
        if result:
            utils.mouse_click(pos[0],pos[1])
        elif result2:
            utils.mouse_click(pos2[0] - 40, pos2[1])
            utils.keyboardInputDel()
            utils.mouse_click(pos2[0] - 40, pos2[1])
        for i in input_word:
            utils.keyboardInputByCode(i)
        # 点击两次是为了避免处理系统中英文及输入法
        utils.keyboardInputEnter()
        utils.keyboardInputEnter()

    @page_method_record("在全部tab安装可牛办公")
    def install_keniuoffice_from_alltab(self):
        keniuoffice_name = "keniubangong"
        self.click_all_tab()
        utils.perform_sleep(2)
        self.search_input(keniuoffice_name)
        if utils.find_element_by_pic(
                self.get_page_shot("keniuoffice_logo.png"), sim=0.8, retry=3)[0]:
            utils.click_element_by_pic(
                self.get_page_shot("install_button.png"), sim=0.8, retry=5)
        if self.keniuoffice_install():
            return True
        return False

    @page_method_record("在全部tab安装腾讯视频")
    def install_tencentvideo_from_alltab(self):
        tencentvideo_name = "tengxunshipin"
        self.click_all_tab()
        utils.perform_sleep(2)
        self.search_input(tencentvideo_name)
        utils.perform_sleep(3)
        result, pos_list = utils.find_elements_by_pic(
            self.get_page_shot("tencentvideo_logo.png"), sim=0.8, retry=3)
        if not result:
            return False
        button_result, button_pos_list = utils.find_elements_by_pic(
            self.get_page_shot("seminstall_button.png"), sim=0.8, retry=2)
        utils.mouse_click(button_pos_list[0][0],button_pos_list[0][1])
        if not self.tencentvideo_install():
            return False
        return True

    @page_method_record("在详情页安装可牛办公")
    def install_keniuoffice_from_detail(self):
        keniuoffice_name = "keniubangong"
        self.click_all_tab()
        self.search_input(keniuoffice_name)
        utils.click_element_by_pic(
            self.get_page_shot("keniuoffice_logo.png"), sim=0.8, retry=5)
        utils.perform_sleep(2)
        if not self.is_page_show_normal():
            log.log_error("详情页展示异常")
        log.log_pass("详情页面展示正常")
        utils.click_element_by_pic(
            self.get_page_shot("detail_install_button.png"), sim=0.8, retry=5)
        if not self.keniuoffice_install():
            return False
        return True

    @page_method_record("在详情页里安装腾讯视频")
    def install_tencentvideo_from_detail(self):
        tencentvideo_name = "tengxunshipin"
        self.click_all_tab()
        self.search_input(tencentvideo_name)
        utils.perform_sleep(3)
        result, pos_list = utils.find_elements_by_pic(
            self.get_page_shot("tencentvideo_logo.png"), sim=0.8, retry=2)
        if not result:
            return False
        utils.mouse_click(pos_list[0][0], pos_list[0][1])
        utils.perform_sleep(2)
        if not self.is_page_show_normal():
            log.log_error("详情页展示异常")
        log.log_pass("详情页面展示正常")
        button_result, button_pos_list = utils.find_elements_by_pic(
            self.get_page_shot("detail_seminstall_button.png"), sim=0.8, retry=2)
        utils.mouse_click(button_pos_list[0][0], button_pos_list[0][1])
        if not self.tencentvideo_install():
            return False
        return True

    @page_method_record("安装低版本winrar")
    def install_old_winrar(self, package_path):
        utils.process_start(process_path=package_path, async_start=True)
        utils.perform_sleep(5)
        # self.judge_pop_detect()
        if utils.click_element_by_pic(self.get_page_shot("winrar_pop_sure_button.png"), sim=0.75, retry=10):
            log.log_info("关闭软管拦截弹窗")

        if not while_operation(product_path=product_path, photo_name="winrar_install_logo.png", sim=0.75):
            log.log_error("未匹配到winrar安装窗口")
            return False
        winrar_class_name = "#32770"
        winrar_file_hwnd = utils.get_hwnd_by_class(winrar_class_name, title=None)
        if winrar_file_hwnd:
            win32gui.SetForegroundWindow(winrar_file_hwnd)

        utils.click_element_by_pic(
            self.get_page_shot("winrar_install_button.png"), sim=0.75, retry=5)

        if not while_operation(product_path=product_path, photo_name="winrar_install_sure_button.png", sim=0.75, retry=1):
            log.log_error("未匹配到winrar安装确认按钮")
            return False
        utils.click_element_by_pic(
            self.get_page_shot("winrar_install_sure_button.png"), sim=0.75, retry=1)

        if not while_operation(
                product_path=product_path, photo_name="winrar_install_thanksword.png", sim=0.75, retry=1):
            log.log_error("未匹配到winrar安装完成文案")
            return False

        if not utils.click_element_by_pic(
                self.get_page_shot("winrar_install_finish_button2.png"), sim=0.75, retry=1):
            utils.click_element_by_pic(
                self.get_page_shot("winrar_install_finish_button.png"), sim=0.75, retry=1)
        utils.perform_sleep(2)
        if utils.find_element_by_pic(
                self.get_page_shot("winrar_install_pop_logo.png"), sim=0.75, retry=10)[0]:
            utils.click_element_by_pic(
                self.get_page_shot("winrar_install_pop_sure_button.png"), sim=0.75, retry=5)
        mainpage_class_name = "kismain{1ACD30B1-18F3-4f4d-B52D-4709D099998C}"
        mainpage_file_hwnd = utils.get_hwnd_by_class(mainpage_class_name, title=None)
        win32gui.SetForegroundWindow(mainpage_file_hwnd)
        sp_class_name = "soft uninst class"
        sp_file_hwnd = utils.get_hwnd_by_class(sp_class_name, title=None)
        win32gui.SetForegroundWindow(sp_file_hwnd)
        #win32gui.PostMessage(file_hwnd, win32con.WM_CLOSE, 0, 0)
        utils.perform_sleep(2)
        if not utils.is_reg_exist(regpath=r'SOFTWARE\WOW6432Node\WinRAR'):
            return False
        return True

    @page_method_record("在升级tab升级winrar软件")
    def update_winrar_from_update(self):
        software_photo = "winrar_logo.png"
        operation_name = "UPDATE"
        button_pos = self.scroll_pagelist(software_photo, operation_name)
        utils.mouse_click(button_pos[0],button_pos[1])

        if not while_operation(product_path=product_path, photo_name="winrar_logo.png", sim=0.8, retry=1):
            log.log_info("匹配到winrar升级完成")

        if not utils.is_reg_exist(regpath=r'SOFTWARE\WOW6432Node\WinRAR'):
            return False
        return True

    @page_method_record("点击分发弹窗暂不需要按钮")
    def recommend_pop_refuse_button_click(self):
        return utils.click_element_by_pic(
            self.get_page_shot("recommend_pop_refuse_button.png"), sim=0.8, retry=2)

    @page_method_record("关闭软管推荐泡泡")
    def close_recommend_pop(self):
        if utils.find_element_by_pic(
                self.get_page_shot("recommend_pop_logo.png"), sim=0.85, retry=3)[0]:
            result, pos = utils.find_element_by_pic(
                self.get_page_shot("recommend_pop_menu.png"), sim=0.8, retry=3)
            if result:
                self.recommend_pop_refuse_button_click()
        elif utils.find_element_by_pic(
                self.get_page_shot("recommend_pop_logo_old.png"), sim=0.85, retry=3)[0]:
            result, pos = utils.find_element_by_pic(
                self.get_page_shot("recommend_pop_menu.png"), sim=0.8, retry=3)
            if result:
                self.recommend_pop_refuse_button_click()
            return True
        else:
            return True
        utils.perform_sleep(2)
        if utils.find_element_by_pic(
                self.get_page_shot("recommend_pop_logo.png"), sim=0.8, retry=3)[0] or \
                utils.find_element_by_pic(
                self.get_page_shot("recommend_pop_logo_old.png"), sim=0.8, retry=3)[0]:
            return False
        return True

    @page_method_record("轮询判断弹窗规避")
    def judge_pop_detect(self):
        try_num = 1
        while try_num<10:
            if UnExpectWin_System().unexpectwin_detect():
                break
            utils.perform_sleep(1)
            try_num += 1




