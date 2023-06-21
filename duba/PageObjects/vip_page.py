#!/usr/bin/evn python
# --coding = 'utf-8' --
import json
import urllib
import requests
from enum import Enum, unique
from common import utils
from common.log import log
from common.basepage import BasePage, page_method_record
from common.tools.base_tools import get_page_shot
from common.tools.duba_tools import get_duba_tryno
from common.unexpectwin_system import UnExpectWin_System
from duba.contants import UserType
from duba.utils import get_tool_pay_settings
from common.utils import perform_sleep, Location
from duba.PageObjects.main_page import main_page
from duba.PageObjects.unexpected_popup import UnexpectedPopup, UnexpectedPopupInfo

"""会员页"""


def get_shot_path(name):
    return get_page_shot("vip_page", name)


@unique
class VipKaitongPageShot(Enum):
    DEFRAG = get_shot_path("tag_defrag.png")  # 系统碎片清理王
    DOCUMENT_REPAIR = get_shot_path("tag_document_repair.png")  # 文档修复
    FILE_SHREDDING = get_shot_path("tag_file_shredding.png")  # 文件粉碎
    PDF_CONVERT = get_shot_path("tag_pdf_convert.png")  # PDF转换
    POPUP_INTERCEPT = get_shot_path("tag_popup_intercept.png")  # 弹窗拦截
    SCREEN_RECORD = get_shot_path("tag_screen_record.png")  # 毒霸录屏大师
    TEXT_TO_VOICE = get_shot_path("tag_text_to_voice.png")  # 毒霸文字转语音
    C_SLIMMING = get_shot_path("tag_c_slimming.png")  # C盘瘦身
    PRIVACY_CLEANUP = get_shot_path("tag_privacy_cleanup.png")  # 超级隐私清理
    DATA_RECOVERY = get_shot_path("tag_data_recovery.png")  # 数据恢复
    FAST_PICTURE = get_shot_path("tag_fast_picture.png")  # 毒霸看图
    DRIVER_MANAGER = get_shot_path("tag_driver_manager.png")  # 驱动管理王


@unique
class UserTypeShot(Enum):
    GUEST = get_shot_path("user_type_guest.png")  # 游客
    NON_VIP = get_shot_path("user_type_non_vip.png")  # 非会员（普通用户）
    COMMON_VIP = get_shot_path("user_type_common_vip.png")  # 普通会员
    DIAMOND_VIP = get_shot_path("user_type_diamond_vip.png")  # 钻石会员
    SUPER_VIP = get_shot_path("user_type_super_vip.png")  # 超级会员
    HONOR_VIP = get_shot_path("user_type_honor_vip.png")  # 荣誉会员


@unique
class VipPageShot(Enum):
    LOGIN_NOW = get_shot_path("button_lijidenglu.png")  # 立即登录按钮
    LOGOUT = get_shot_path("button_logout.png")  # 退出登录按钮
    LOGOUT_II = get_shot_path("button_logout_ii.png")  # 退出登录按钮2
    LOGOUT_III = get_shot_path("button_logout_update.png")  # 退出登录按钮3
    SWITCH_ACCOUNT = get_shot_path("button_switch_account.png")  # 切换账号按钮
    SWITCH_WX_PAY_BUTTON = get_shot_path("button_switch_wx_pay.png")  # 切换微信支付按钮
    SWITCH_ALI_PAY_BUTTON = get_shot_path("button_switch_ali_pay.png")  # 切换支付宝支付按钮
    BROWSER_PROTECT_BTN = get_shot_path("tools_browser_protect_button.png")  # 浏览器主页修复按钮
    C_SLIMMING_BTN = get_shot_path("tools_c_slimming_button.png")  # C盘瘦身按钮
    DATA_RECOVERY_BTN = get_shot_path("tools_data_recovery_button.png")  # 数据恢复按钮
    DOCUMENT_PROTECT_BTN = get_shot_path("tools_document_protect_button.png")  # 文档卫士按钮
    DOCUMENT_REPAIR_BTN = get_shot_path("tools_document_repair_button.png")  # 文档修复按钮
    FAST_PICTURE_BTN = get_shot_path("tools_fast_picture_button.png")  # 毒霸看图按钮
    FILE_SHREDDING_BTN = get_shot_path("tools_file_shredding_button.png")  # 文件粉碎按钮
    FOLDER_ENCRYPT_BTN = get_shot_path("tools_folder_encrypt_button.png")  # 文件夹加密按钮
    NETWORK_SPEED_BTN = get_shot_path("tools_network_speed.png")  # 网络优化按钮
    PDF_CONVERT_BTN = get_shot_path("tools_pdf_convert_button.png")  # PDF转换按钮
    POPUP_INTERCEPT_BTN = get_shot_path("tools_popup_intercept_button.png")  # 恶意弹窗拦截按钮
    PRIVACY_CLEANER_BTN = get_shot_path("tools_privacy_cleaner_button.png")  # 超级隐私清理按钮
    PRIVACY_NO_TRACE_BTN = get_shot_path("tools_privacy_no_trace.png")  # 隐私无痕模式按钮
    PRIVACY_SHIELD_BTN = get_shot_path("tools_privacy_shield_button.png")  # 隐私护盾按钮
    PURE_NO_AD_BTN = get_shot_path("tools_pure_no_ad_button.png")  # 纯净无广告按钮
    RIGHT_MENU_MGR_BTN = get_shot_path("tools_right_menu_mgr_button.png")  # 右键菜单管理按钮
    SCREEN_RECORD_BTN = get_shot_path("tools_screen_record_button.png")  # 录屏大师按钮
    TEXT_TO_VOICE_BTN = get_shot_path("tools_text_to_voice_button.png")  # 文字转语音按钮
    TRASH_AUTO_CLEAN_BTN = get_shot_path("tools_trash_auto_clean_button.png")  # 自动清理垃圾按钮
    DEFRAG_BTN = get_shot_path("tools_defrag_button.png")  # 系统碎片清理王按钮
    TEEN_MODE_BTN = get_shot_path("tools_teen_mode_button.png")  # 孩子守护王按钮
    TECHNICAL_EXPERT_SERVICE_BTN = get_shot_path("tools_technical_expert_service_button.png")  # 技术专家服务按钮
    VIP_SERVICE_BTN = get_shot_path("tools_vip_service_button.png")  # VIP客服按钮
    FIVE_X_SPEED_BTN = get_shot_path("tools_5x_speed_button.png")  # 5倍积分按钮
    VIP_CRASH_BTN = get_shot_path("tools_vip_crash_button.png")  # 会员返现按钮
    VIP_SKIN_BTN = get_shot_path("tools_vip_skin_button.png")  # 专属主题皮肤按钮
    DRIVE_DOWNLOAD_BTN = get_shot_path("tools_drive_download_button.png")  # 驱动高速下载按钮
    FAST_VC_BTN = get_shot_path("tools_fast_vc_button.png")  # 视频转换按钮
    SCREEN_CAPTURE_BTN = get_shot_path("tools_screen_capture_button.png")  # 截图王按钮
    EXPERIENCE_NOW = get_shot_path("button_lijitiyan.png")  # 立即体验按钮
    GET_IT_NOW = get_shot_path("button_lijilingqu.png")  # 立即领取按钮
    BOOK_NOW = get_shot_path("button_lijiyuyue.png")  # 立即预约按钮
    YUAN_MARK = get_shot_path("mark_yuan.png")  # 人民币标志图


# 用户类型对应的标识截图
UserTypeToShot = {
    UserType.GUEST: UserTypeShot.GUEST.value,
    UserType.NON_VIP: UserTypeShot.NON_VIP.value,
    UserType.COMMON_VIP: UserTypeShot.COMMON_VIP.value,
    UserType.SUPER_VIP: UserTypeShot.SUPER_VIP.value,
    UserType.DIAMOND_VIP: UserTypeShot.DIAMOND_VIP.value,
    UserType.HONOR_VIP: UserTypeShot.HONOR_VIP.value,
}


class vip_page(BasePage):
    def __init__(self, do_pre_open=True, page_desc=None, delay_sec=0, init_user_type=False):
        """
        会员页构造函数
        @param do_pre_open: 执行打开界面操作
        @param page_desc: 页面描述名称
        @param init_user_type: 是否需要检测当前用户类型（检测用户类型函数耗时较长）
        """
        super().__init__(do_pre_open=do_pre_open, page_desc=page_desc, delay_sec=delay_sec)

        # 用户类型
        self.user_type = None
        if init_user_type:
            self.user_type = self.check_user_type()
            log.log_info(f"检测到当前用户类型为：{self.user_type.value}")

        # 检查限时福利的弹窗，如果有就直接关闭
        if UnexpectedPopup.popup_process(UnexpectedPopupInfo.TIME_LIMITED_BENEFITS, hwnd=self.hwnd):
            perform_sleep(1)

        # 初始化最左边套餐的元图标位置
        self.left_yuan_position = ()

    def pre_open(self):
        self.mp = main_page()
        self.mp.vip_click()

    def page_confirm_close(self):
        # 查找并关闭服务评分弹窗
        if UnexpectedPopup.popup_process(UnexpectedPopupInfo.SERVICE_SCORE, hwnd=self.hwnd):
            perform_sleep(1)

        # 检测并关闭会员惊喜砸蛋弹窗
        if UnexpectedPopup.popup_process(UnexpectedPopupInfo.VIP_SURPRISE_SMASH_EGG, hwnd=self.hwnd):
            perform_sleep(1)

    @page_method_record("检测当前用户类型")
    def check_user_type(self):
        user_type_result = None
        # 依次查找用户类型标识
        for user_type in UserTypeToShot.keys():
            shot = UserTypeToShot[user_type]
            if utils.find_element_by_pic(shot, retry=2, sim=0.9, sim_no_reduce=True, hwnd=self.hwnd)[0]:
                user_type_result = user_type
                break

        if user_type_result is None:
            log.log_error("当前用户类型检测失败")

        return user_type_result

    # 点击用户登录中心
    @page_method_record("点击登录")
    def user_login_click(self):
        # 检查用户是否已经登录，登录则点击退出
        self.logout()
        perform_sleep(2)
        if not utils.click_element_by_pics(
                [self.get_page_shot("button_liji_login.png"), self.get_page_shot("button_switch_account_link.png")],
                retry=2):
            utils.mouse_click(self.position[0] + 41, self.position[1] + 48)

    # 点击积分商城
    @page_method_record("点击积分商城")
    def jifen_shop_click(self):
        utils.mouse_click(self.position[0] + 453, self.position[1] + 15)

    # 点击兑换码
    @page_method_record("点击兑换码")
    def change_code_click(self):
        utils.mouse_click(self.position[0] + 513, self.position[1] + 15)

    # 点击专属会员福利
    @page_method_record("点击专属会员福利")
    def vip_single_benefits_click(self):
        utils.mouse_click(self.position[0] + 555, self.position[1] + 16)

    # 点击反馈建议
    @page_method_record("点击反馈建议")
    def suggestion_click(self):
        utils.mouse_click(self.position[0] + 604, self.position[1] + 15)

    # 点击毒霸服务播报
    @page_method_record("点击毒霸服务播报")
    def service_report_click(self):
        utils.mouse_click(self.position[0] + 655, self.position[1] + 15)

    def check_payurl(self, payurl=""):
        if payurl.find("duba.net/api/v2/url/jump?c=") < 0:
            return None

        response = utils.send_request(payurl, method='get', verify=False)
        parseresult = requests.utils.urlparse(urllib.parse.unquote(response.url))
        query = str(parseresult[4])
        param_dict = {}
        for d in query.split("&"):
            param_dict.update({d.split("=")[0]: d.split("=")[1]})
        return param_dict

    # 逐个点击游客账号套餐按钮并检查二维码
    @page_method_record("逐个点击游客账号套餐按钮并检查二维码")
    def get_each_paycodes_price_youke(self):
        paycodes_point = []
        paymoney_list = []
        u_x, u_y, u_x1, u_y1 = 0, 0, 0, 0
        under_price_list = []

        find_r, elements_pos_list = utils.find_elements_by_pic(self.get_page_shot("tip_yuan.png"))
        if find_r:
            first_line_y = elements_pos_list[0][1]
            temp_x = 0
            for el_pos in elements_pos_list:
                # 判断同一行的价格，并且筛选掉匹配上的重叠价格
                if abs(el_pos[1] - first_line_y) < 4 and abs(el_pos[0] - temp_x) > 15:
                    x = el_pos[0] + 10
                    y = el_pos[1] - 15
                    temp_x = el_pos[0]
                    paycodes_point.append((x, y))
                # 获取下方二维码旁边价格的坐标
                elif el_pos[1] > first_line_y:
                    u_x = el_pos[0] + 13
                    u_y = el_pos[1] - 23
                    u_x1 = u_x + 70
                    u_y1 = u_y + 35

        # 开始逐个点击套餐按钮并检查二维码
        for paycode_point in paycodes_point:
            utils.mouse_click(paycode_point[0], paycode_point[1])

            perform_sleep(1)
            utils.mouse_move(1, 1)  # 移开鼠标防止tips覆盖到价格

            # 获取下方二维码旁边价格
            pic = utils.cutscreen_img(u_x, u_y, u_x1, u_y1)
            price = utils.renum(utils.tcreadimgnum(pic))
            utils.attach_screenshot("获取下方二维码旁边价格为" + str(price), image_path=pic)
            under_price_list.append(price)

            perform_sleep(3)
            try:
                payurl = utils.decode_qrcode()
                paydata = self.check_payurl(payurl)
                if paydata:
                    log.log_info(paydata)
                    paymoney_list.append(int(paydata["pay_money"]))
            except:
                log.log_error("获取二维码价格失败")
            perform_sleep(3)
        return paymoney_list, under_price_list

    # 逐个点击套餐按钮并检查二维码
    @page_method_record("逐个点击套餐按钮并检查二维码")
    def get_each_paycodes_price(self, tool="会员中心"):
        paycodes_point = []  # 界面上的价格坐标
        paymoney_list = []  # 二维码请求的价格
        # price_list = []  # 界面上的价格
        u_x, u_y, u_x1, u_y1 = 0, 0, 0, 0
        under_price_list = []

        find_r, elements_pos_list = utils.find_elements_by_pic(self.get_page_shot("tip_yuan.png"))

        # 排序elements_pos_list，发现有的识别顺序不是从左到右识别
        def takeone(e):
            return e[0]

        elements_pos_list.sort(key=takeone)
        if find_r:
            first_line_y = elements_pos_list[0][1]
            temp_x = 0
            for el_pos in elements_pos_list:
                # 判断同一行的价格，并且筛选掉匹配上的重叠价格
                if abs(el_pos[1] - first_line_y) < 4 and abs(el_pos[0] - temp_x) > 15:
                    # 获取价格坐标
                    x = el_pos[0] + 10
                    y = el_pos[1] - 15
                    temp_x = el_pos[0]
                    paycodes_point.append((x, y))

                # 获取下方二维码旁边价格的坐标
                elif el_pos[1] > first_line_y:
                    u_x = el_pos[0] + 13
                    u_y = el_pos[1] - 23
                    u_x1 = u_x + 70
                    u_y1 = u_y + 35

        pay_setting_result = []
        for paycode_point in paycodes_point:
            utils.mouse_click(paycode_point[0], paycode_point[1])
            perform_sleep(1)
            utils.mouse_move(1, 1)  # 移开鼠标防止tips覆盖到价格

            # 获取下方二维码旁边价格
            pic = utils.cutscreen_img(u_x, u_y, u_x1, u_y1)
            price = utils.renum(utils.tcreadimgnum(pic))
            utils.attach_screenshot("获取下方二维码旁边价格为" + str(price), image_path=pic)
            under_price_list.append(price)

            perform_sleep(3)
            try:
                payurl = utils.decode_qrcode()
                pay_result_dict = self.check_payurl(payurl)
                payParams = json.loads(pay_result_dict["payParams"])
                log.log_info("payParams")
                log.log_info(payParams)
                if not pay_setting_result:
                    pay_setting_result = get_tool_pay_settings(tool, payParams["open_id"], payParams["token"],
                                                               get_duba_tryno(), payParams["server_id"])
                    log.log_info("pay_setting_result")
                    log.log_info(pay_setting_result)
            except Exception as e:
                log.log_error("获取二维码价格失败")
            if pay_setting_result:
                for pay_info in pay_setting_result:
                    if pay_info["id"] == payParams["pay_setting_id"]:
                        paymoney_list.append(int(pay_info["current_price"]))
            perform_sleep(3)
        return paymoney_list, under_price_list

    # 逐个点击套餐按钮并检查二维码
    @page_method_record("获取界面上的价格")
    def get_price_on_screen(self):
        price_list = []
        find_r, elements_pos_list = utils.find_elements_by_pic(self.get_page_shot("tip_yuan.png"))
        if find_r:
            first_line_y = elements_pos_list[0][1]
            temp_x = 0
            i = 0
            for el_pos in elements_pos_list:
                # 判断同一行的价格，并且筛选掉匹配上的重叠价格
                if abs(el_pos[1] - first_line_y) < 4 and abs(el_pos[0] - temp_x) > 15:
                    x = el_pos[0] + 10
                    y = el_pos[1] - 15
                    x1 = x + 60
                    y1 = y + 30
                    pic = utils.cutscreen_img(x, y, x1, y1)
                    price = utils.renum(utils.tcreadimgnum(pic))
                    utils.attach_screenshot("读取第" + str(i + 1) + "个价格为" + str(price), image_path=pic)
                    price_list.append(price)  # 取返回的数组里的第二个值，第一个值识别为元符号
                    i += 1
                    temp_x = el_pos[0]
        return price_list

    def get_left_yuan_position(self):
        if self.left_yuan_position:
            return self.left_yuan_position

        yuan_find_result, yuan_positions = utils.find_elements_by_pic(VipPageShot.YUAN_MARK.value, sim=0.8,
                                                                      location=Location.LEFT_UP.value, retry=3,
                                                                      sim_no_reduce=False)

        def find_left_position(elem):
            return elem[0]

        if yuan_find_result:
            yuan_positions.sort(key=find_left_position)
            self.left_yuan_position = yuan_positions[0]
        return self.left_yuan_position

    # 滚动鼠标到展示会员特权
    @staticmethod
    def go_operation(self, scroll=500):
        utils.mouse_click(self.position[0], self.position[1])
        utils.mouse_move(self.position[0] + 20, self.position[1] + 300)
        utils.mouse_scroll(scroll)
        perform_sleep(0.5)

    # 鼠标滚动至页面顶部
    def scroll_to_top(self):
        index = 1
        while True:
            # 根据滚动条顶部坐标点颜色判断滚动条是否滚动到顶部
            # if utils.get_dominant_color(
            #         utils.cutscreen_img(self.position[0] + 680, self.position[1] + 100, self.position[0] + 700,
            #                             self.position[1] + 112)) == (255, 255, 255):
            color_hex = utils.get_pic_coordinates_color(self.position[0] + 683, self.position[1] + 140)
            color_hex2 = utils.get_pic_coordinates_color(self.position[0] + 690, self.position[1] + 140)
            if color_hex == "#ffffff" and color_hex2 == "#ffffff":
                self.go_operation(self, -3000)
                perform_sleep(0.5)
            else:
                break
            if index > 10:
                log.log_error("scroll_to_top error")
                return

            index += 1

    # 点击切换支付方式，switch_type:1为微信 2为支付宝
    @page_method_record("点击切换支付方式")
    def switch_pay_type(self, switch_type=1):
        if switch_type == 2:
            utils.click_element_by_pic(VipPageShot.SWITCH_ALI_PAY_BUTTON.value, 0.8)
        else:
            utils.click_element_by_pic(VipPageShot.SWITCH_WX_PAY_BUTTON.value, 0.8)

    def do_open_tools(self, tool_pic, open_btn_pic, pos_index=0):
        """
        打开工具
        @param tool_pic: 工具图片
        @param open_btn_pic: 工具打开按钮图片
        @param pos_index: 待点击打开按钮图片索引，默认为0，即点击第一个
        @return:
        """
        self.scroll_to_top()  # 先确保滚动到页面最顶
        perform_sleep(0.5)
        utils.mouse_move(self.position[0] + 20, self.position[1] + 300)
        scroll_sum = 0
        scroll = 300
        click_tools_btn_result = False
        while scroll_sum <= 2100:
            click_result = utils.click_element_by_pic(tool_pic.value, retry=2, hwnd=self.hwnd, sim=0.7)
            if click_result:
                click_tools_btn_result = True
                break
            utils.mouse_move(self.position[0] + 20, self.position[1] + 300)
            utils.mouse_scroll(scroll)
            scroll_sum += scroll
            perform_sleep(0.5)

        if not click_tools_btn_result:
            log.log_error(f"会员页找不到该工具图标：{tool_pic}")
            return False

        perform_sleep(1)

        # 普通会员、钻石会员、超级会员用户点击工具图标会直接打开该工具
        if self.user_type and self.user_type not in [UserType.GUEST, UserType.NON_VIP, UserType.HONOR_VIP]:
            return True

        # 查找打开工具的按钮，如：立即体验、立即预约...
        find_result, pos_list = utils.find_elements_by_pic(open_btn_pic.value, 0.8, retry=2)
        if not find_result:
            # 部分功能点击工具图标会直接打开该工具
            return True

        # 过滤掉y坐标相同的坐标
        def repeat_filter(pos_list):
            result = []
            for index, pos in enumerate(pos_list):
                if index == 0 or pos[1] != pos_list[index - 1][1]:
                    result.append(pos)
            return result

        pos_list.sort(key=lambda x: x[1])
        pos_list = repeat_filter(pos_list)
        position = pos_list[pos_index] if pos_index < len(pos_list) else pos_list[0]
        utils.mouse_click(position)
        perform_sleep(1)

    # 点击数据恢复
    @page_method_record("点击数据恢复")
    def data_recovery_click(self):
        self.do_open_tools(VipPageShot.DATA_RECOVERY_BTN, VipPageShot.EXPERIENCE_NOW)

    # 点击纯净无广告
    @page_method_record("点击纯净无广告")
    def pure_no_ad_click(self):
        self.do_open_tools(VipPageShot.PURE_NO_AD_BTN, VipPageShot.EXPERIENCE_NOW)

    # 点击pdf转换
    @page_method_record("点击PDF转换")
    def pdfconvert_click(self):
        self.do_open_tools(VipPageShot.PDF_CONVERT_BTN, VipPageShot.EXPERIENCE_NOW)

    # 点击弹窗拦截
    @page_method_record("点击弹窗拦截")
    def tanchuang_lanjie_click(self):
        self.do_open_tools(VipPageShot.POPUP_INTERCEPT_BTN, VipPageShot.EXPERIENCE_NOW)

    # 点击会员返现
    @page_method_record("点击会员返现")
    def vip_cash_click(self):
        self.do_open_tools(VipPageShot.VIP_CRASH_BTN, VipPageShot.GET_IT_NOW)

    # 点击超级隐私清理
    @page_method_record("点击超级隐私清理")
    def privacy_clean_click(self):
        self.do_open_tools(VipPageShot.PRIVACY_CLEANER_BTN, VipPageShot.EXPERIENCE_NOW)

    # 点击文件夹加密
    @page_method_record("点击文件夹加密")
    def file_encode_click(self):
        self.do_open_tools(VipPageShot.FOLDER_ENCRYPT_BTN, VipPageShot.EXPERIENCE_NOW)

    # 点击技术专家服务
    @page_method_record("点击技术专家服务")
    def skill_master_service_click(self):
        self.do_open_tools(VipPageShot.TECHNICAL_EXPERT_SERVICE_BTN, VipPageShot.BOOK_NOW)

    # 点击文件粉碎
    @page_method_record("点击文件粉碎")
    def file_shredding_click(self):
        self.do_open_tools(VipPageShot.FILE_SHREDDING_BTN, VipPageShot.EXPERIENCE_NOW)

    # 点击c盘瘦身专家
    @page_method_record("点击c盘瘦身专家")
    def c_slimming_click(self):
        self.do_open_tools(VipPageShot.C_SLIMMING_BTN, VipPageShot.EXPERIENCE_NOW)

    # 点击浏览器主页修复
    @page_method_record("点击浏览器主页修复")
    def browser_mainpage_fix_click(self):
        self.do_open_tools(VipPageShot.BROWSER_PROTECT_BTN, VipPageShot.EXPERIENCE_NOW)

    # 点击vip客服
    @page_method_record("点击vip客服")
    def vip_service_click(self):
        self.do_open_tools(VipPageShot.VIP_SERVICE_BTN, VipPageShot.EXPERIENCE_NOW)

    # 点击专属皮肤
    @page_method_record("点击专属皮肤")
    def single_vipskin_click(self):
        self.do_open_tools(VipPageShot.VIP_SKIN_BTN, VipPageShot.EXPERIENCE_NOW)

    # 点击5倍积分加速
    @page_method_record("点击5倍积分加速")
    def jifen_5x_speed_click(self):
        self.do_open_tools(VipPageShot.FIVE_X_SPEED_BTN, VipPageShot.EXPERIENCE_NOW)

    # 点击文档修复
    @page_method_record("点击文档修复")
    def file_fix_click(self):
        self.do_open_tools(VipPageShot.DOCUMENT_REPAIR_BTN, VipPageShot.EXPERIENCE_NOW)

    # 点击文档卫士
    @page_method_record("点击文档卫士")
    def file_guard_click(self):
        self.do_open_tools(VipPageShot.DOCUMENT_PROTECT_BTN, VipPageShot.EXPERIENCE_NOW)

    # 点击隐私护盾
    @page_method_record("点击隐私护盾")
    def privacy_shield_click(self):
        self.do_open_tools(VipPageShot.PRIVACY_SHIELD_BTN, VipPageShot.EXPERIENCE_NOW)

    # 点击隐私无痕模式
    @page_method_record("点击隐私无痕模式")
    def privacy_notrace_click(self):
        self.do_open_tools(VipPageShot.PRIVACY_NO_TRACE_BTN, VipPageShot.EXPERIENCE_NOW)

    # 点击右键菜单管理
    @page_method_record("点击右键菜单管理")
    def right_mouse_menu_click(self):
        self.do_open_tools(VipPageShot.RIGHT_MENU_MGR_BTN, VipPageShot.EXPERIENCE_NOW)

    # 点击毒霸看图
    @page_method_record("点击毒霸看图")
    def duba_see_pic_click(self):
        self.do_open_tools(VipPageShot.FAST_PICTURE_BTN, VipPageShot.EXPERIENCE_NOW)

    # 点击录屏大师
    @page_method_record("点击录屏大师")
    def screen_record_click(self):
        self.do_open_tools(VipPageShot.SCREEN_RECORD_BTN, VipPageShot.EXPERIENCE_NOW)

    # 点击网络优化
    @page_method_record("点击网络优化")
    def network_speed_click(self):
        self.do_open_tools(VipPageShot.NETWORK_SPEED_BTN, VipPageShot.EXPERIENCE_NOW)

    # 点击文字转语音
    @page_method_record("点击文字转语音")
    def font_to_voice_click(self):
        self.do_open_tools(VipPageShot.TEXT_TO_VOICE_BTN, VipPageShot.EXPERIENCE_NOW)

    # 点击自动清理垃圾
    @page_method_record("点击自动清理垃圾")
    def auto_clean_crash_click(self):
        self.do_open_tools(VipPageShot.TRASH_AUTO_CLEAN_BTN, VipPageShot.EXPERIENCE_NOW)

    # 点击系统碎片清理王
    @page_method_record("点击系统碎片清理王")
    def system_defrag_click(self):
        self.do_open_tools(VipPageShot.DEFRAG_BTN, VipPageShot.EXPERIENCE_NOW)

    # 点击孩子守护王
    @page_method_record("点击孩子守护王")
    def teen_mode_click(self):
        self.do_open_tools(VipPageShot.TEEN_MODE_BTN, VipPageShot.EXPERIENCE_NOW)

    # 点击驱动高速下载
    @page_method_record("点击驱动高速下载")
    def drive_download_click(self):
        self.do_open_tools(VipPageShot.DRIVE_DOWNLOAD_BTN, VipPageShot.EXPERIENCE_NOW)

    # 点击视频转换
    @page_method_record("点击视频转换")
    def fast_vc_click(self):
        self.do_open_tools(VipPageShot.FAST_VC_BTN, VipPageShot.EXPERIENCE_NOW)

    # 点击截图王
    @page_method_record("点击截图王")
    def screen_capture_click(self):
        self.do_open_tools(VipPageShot.SCREEN_CAPTURE_BTN, VipPageShot.EXPERIENCE_NOW, pos_index=1)

    @page_method_record("退出账号")
    def logout(self):
        result = utils.click_element_by_pics([self.get_page_shot("button_logout.png"),
                                              self.get_page_shot("button_logout_ii.png"),
                                              self.get_page_shot("button_switch_account.png"),
                                              self.get_page_shot("button_logout_update.png")], retry=2, sim=0.8,
                                             sim_no_reduce=True)
        if self.user_type is not None:
            if result:
                self.user_type = UserType.GUEST
            log.log_info(f"当前用户类型为：{self.user_type.value}")

        return result

    @page_method_record("判断是否登录成功")
    def is_logined(self):
        # 由于登录等待时间比较长，故先设置等待40秒同时抛出登录时长异常
        result = True
        i = 0
        while result:
            utils.perform_sleep(5)
            result = utils.find_element_by_pic(VipPageShot.LOGIN_NOW.value, retry=3)[0]
            i += 1
            if i > 5:
                log.log_error("登录接口返回时间过长，抛出等待异常", need_assert=False)
                break
            log.log_error("登录接口返回时间超过5秒，等待5秒重试", need_assert=False)
        return not result

    @page_method_record("判断是否为游客")
    def is_guest_user(self):
        return utils.find_element_by_pic(VipPageShot.LOGIN_NOW.value, retry=3)[0]

    # 点击任务栏会员中心图标
    @page_method_record("点击任务栏会员中心图标")
    def click_taskbar_icon(self):
        return utils.click_element_by_pic(self.get_page_shot("taskbar_icon.png"), retry=3, sim_no_reduce=True)


# 用于开通毒霸会员的会员中心类
class vip_kaitong_page(vip_page):
    # 开通毒霸的会员中心坐标跟原会员中心的不一致
    def __init__(self, page_desc=None, delay_sec=1):
        super().__init__(do_pre_open=False, page_desc=page_desc, delay_sec=delay_sec, init_user_type=False)
        self.position = (self.position[0], self.position[1] + 28)

    def pre_open(self):
        """此类的页面需要在testcase自己打开，没有默认的打开方法"""
        pass

    def page_confirm_close(self):
        # 处理非预期弹窗（PDF转换、C盘瘦身、弹窗拦截、隐私清理、毒霸看图）
        if UnexpectedPopup.popup_process(UnexpectedPopupInfo.COUPON, hwnd=self.hwnd):
            perform_sleep(1)

        # 检测并关闭会员惊喜砸蛋弹窗
        if UnexpectedPopup.popup_process(UnexpectedPopupInfo.VIP_SURPRISE_SMASH_EGG, hwnd=self.hwnd):
            perform_sleep(1)

    @page_method_record("退出账号")
    def logout(self):
        return utils.click_element_by_pic(VipPageShot.LOGOUT_III.value, retry=3)

    @page_method_record("检查会员中心的标记")
    def check_page_tag(self, source):
        """source请使用VipKaitongPageShot对应的value"""
        if not utils.find_element_by_pic(source, sim_no_reduce=True, retry=3)[0]:
            if UnExpectWin_System().unexpectwin_detect():
                return utils.find_element_by_pic(source, sim_no_reduce=True, retry=3)[0]
        return utils.find_element_by_pic(source, sim_no_reduce=True, retry=3)[0]


if __name__ == '__main__':
    vip_page_o = vip_page(init_user_type=False)
    r = vip_page_o.get_each_paycodes_price(tool="家庭版1台")
    print(r)
