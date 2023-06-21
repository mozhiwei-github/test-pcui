# --coding = 'utf-8' --
import time
from common import utils
from common.log import log
from common.utils import perform_sleep
from common.basepage import BasePage, page_method_record
from duba.PageObjects.baibaoxiang_page import baibaoxiang_page
from duba.PageObjects.unexpected_popup import UnexpectedPopup, UnexpectedPopupInfo
from duba.contants import Keniu_Office_QQAccount
import random

"""可牛办公页面"""


class perfect_office_page(BasePage):
    def __init__(self, do_pre_open=True, page_desc=None, delay_sec=5):
        """
        会员页构造函数
        @param do_pre_open: 执行打开界面操作
        @param page_desc: 页面描述名称
        @param init_user_type: 是否需要检测当前用户类型（检测用户类型函数耗时较长）
        """
        super().__init__(do_pre_open=do_pre_open, page_desc=page_desc, delay_sec=delay_sec)

        # 检查限时福利的弹窗，如果有就直接关闭
        if UnexpectedPopup.popup_process(UnexpectedPopupInfo.PERFECT_OFFICE_RED_PACKET_618, hwnd=self.hwnd):
            perform_sleep(1)

        # 检查会员界面是否自动弹出，支持A/B test（坐标位置不一样）
        if utils.find_element_by_pic(self.get_page_shot("tab_weixin_pay.png"), retry=3, sim_no_reduce=True)[0]:
            utils.mouse_click(self.position[0] + 1017, self.position[1] + 218)
            log.log_info("检查会员界面是否自动弹出并关闭")
            utils.perform_sleep(2)
        if utils.find_element_by_pic(self.get_page_shot("tab_weixin_pay.png"), retry=3, sim_no_reduce=True)[0]:
            utils.mouse_click(self.position[0] + 1017, self.position[1] + 203)
            log.log_info("检查会员界面是否自动弹出并关闭")
            utils.perform_sleep(2)

    def pre_open(self):
        baibaoxiang_page_o = baibaoxiang_page()
        perform_sleep(1)
        baibaoxiang_page_o.otherproduct_click()
        perform_sleep(1)
        baibaoxiang_page_o.tools_button_click(baibaoxiang_page_o.get_page_shot("button_perfect_office.png"))

    def page_confirm_close(self):
        # 查找并关闭创建快捷方式提示窗
        if UnexpectedPopup.popup_process(UnexpectedPopupInfo.PERFECT_OFFICE_QUICK_LINK, hwnd=self.hwnd):
            perform_sleep(1)

        log.log_info("查找二次确认关闭弹窗")
        if utils.find_element_by_pic(self.get_page_shot("confirm_close_prompt_tab_logo.png"), retry=3,
                                     sim_no_reduce=True)[0]:
            log.log_info("点击关闭全部按钮，关闭二次确认弹窗")
            utils.click_element_by_pic(self.get_page_shot("confirm_close_prompt_close_button.png"), retry=3,
                                       sim_no_reduce=True)

    def get_input_language(self):
        if utils.find_element_by_pic(
                self.get_page_shot("English_input.png"), sim=0.85, retry=3)[0]:
            return "English"
        elif utils.find_element_by_pic(
                self.get_page_shot("chinese_input.png"), sim=0.85, retry=3)[0]:
            return "Chinese"

    @page_method_record("点击tab")
    def tab_click(self, tab_button=None, tab_name=None):
        if tab_button is None:
            tab_button = self.get_page_shot("tab_wenzi.png")

        if not utils.click_element_by_pic(tab_button, sim_no_reduce=True):
            log.log_error(f"点击功能页 {tab_name} tab展示异常")
            return

        download_res, download_pos = utils.find_element_by_pic(self.get_page_shot("expect_download_pic.png"), sim=0.7,
                                                               sim_no_reduce=True, retry=3)
        if not download_res:
            mouse_pos_x, mouse_pos_y = utils.get_mouse_point()
            utils.mouse_move(mouse_pos_x + 200, mouse_pos_y)
            download_res, download_pos = utils.find_element_by_pic(self.get_page_shot("expect_download_pic.png"),
                                                                   sim=0.7, sim_no_reduce=True, retry=3)
            if not download_res:
                log.log_error(f"查找功能页 {tab_name} tab下载按钮失败")
                return

        utils.mouse_move(*download_pos)
        for i in range(10):
            utils.mouse_scroll(500)
            time.sleep(0.5)

        if not utils.find_element_by_pic(self.get_page_shot("expect_page_size.png"), sim_no_reduce=True)[0]:
            log.log_error(f"查找功能页 {tab_name} tab分页栏失败")
            return

        utils.attach_screenshot(f"点击功能页 {tab_name} tab成功")

    @page_method_record("点击办公模板tab")
    def tab_office_template_click(self):
        if utils.click_element_by_pic(self.get_page_shot("tab_office_templete.png"), retry=3, sim_no_reduce=True):
            return True
        log.log_error("点击办公模板tab异常")

    @page_method_record("统计我的收藏中收藏模板数量")
    def statistics_collected_num(self):
        collected_num = 0
        # 确保页面位于我的收藏tab中
        utils.click_element_by_pic(
            self.get_page_shot("tab_logo.png"), sim=0.8, retry=3)
        utils.perform_sleep(1)
        utils.click_element_by_pic(self.get_page_shot("tab_user_center.png"), sim_no_reduce=True)
        utils.perform_sleep(2)
        utils.click_element_by_pic(
            self.get_page_shot("tab_mycollection.png"), sim=0.8, retry=3)
        # self.tab_click(tab_button=self.get_page_shot("button_collect.png"), tab_name="我的收藏")
        utils.perform_sleep(1)
        result, pos_list = utils.find_elements_by_pic(
            self.get_page_shot("mypage_collected.png"), sim=0.8, retry=3)
        if result:
            collected_num = len(pos_list)
        return collected_num

    @page_method_record("随机点击页面中的收藏按钮")
    def click_collect_button(self):
        result, pos_list = utils.find_elements_by_pic(
            self.get_page_shot("button_collect.png"), sim=0.8, retry=3)
        click_pos = pos_list[random.randint(0,len(pos_list)-1)]
        utils.mouse_click(click_pos)

    @page_method_record("随机点击页面中的立即下载按钮")
    def click_download_button(self):
        result, pos_list = utils.find_elements_by_pic(
            self.get_page_shot("button_download.png"), sim=0.8, retry=3)
        click_pos = pos_list[random.randint(0,len(pos_list)-1)]
        utils.mouse_click(click_pos)

    @page_method_record("判断我的下载中是否有新增tips")
    def is_downloading(self):
        return utils.find_element_by_pic(
            self.get_page_shot("mydownloading.png"), sim=0.8, retry=3)[0]

    @page_method_record("点击搜索功能")
    def search_click(self):
        if utils.click_element_by_pic(self.get_page_shot("button_search.png"), sim_no_reduce=True):
            return True
        log.log_error("点击搜索功能异常")

    @page_method_record("判断页面是否为异常页面")
    def is_page_error(self):
        return utils.find_element_by_pic(
            self.get_page_shot("error_page.png"), sim=0.8, retry=3)[0]

    @page_method_record("检查会员扫码")
    def check_vip_price(self):
        if utils.click_element_by_pic(self.get_page_shot("button_vip.png"), sim_no_reduce=True):
            if utils.find_element_by_pic(self.get_page_shot("tab_weixin_pay.png"), sim_no_reduce=True)[0]:
                perform_sleep(2)
                utils.attach_screenshot("会员扫码界面")
                # wx_url = None
                # find_weixin_pay, pos_weixin_pay = utils.find_element_by_pic(self.get_page_shot("tab_weixin_pay.png"),
                #                                                             retry=3, location=Location.LEFT_UP.value)
                #
                # if find_weixin_pay:
                #     wx_url = utils.decode_qrcode_by_img(utils.cutscreen_img(pos_weixin_pay[0] - 20,
                #                                                             pos_weixin_pay[1] - 120,
                #                                                             pos_weixin_pay[0] + 100,
                #                                                             pos_weixin_pay[1]
                #                                                             ))
                wx_url = utils.decode_qrcode()
                if wx_url and wx_url.find("weixin://wxpay/bizpayurl?") >= 0:
                    log.log_pass("检查会员扫码正常")
                else:
                    log.log_error("会员支付页扫码异常")
        else:
            log.log_error("点击进入VIP界面异常")
            return False

        # 关闭VIP界面
        return self.close_vip_page()

    @page_method_record("关闭VIP界面")
    def close_vip_page(self):
        # 关闭VIP界面
        log.log_info("查找VIP界面关闭按钮")
        if utils.click_element_by_pic(self.get_page_shot("vip_close.png"), sim=0.85, sim_no_reduce=True):
            log.log_info("点击VIP界面关闭按钮")
            utils.perform_sleep(3)

        # 由于支付关闭按钮太小同时样式有变动。使用相对坐标处理。
        # 点击完关闭的坐标后，检查微信支付标记是否存在判断关闭成功与否
        # utils.mouse_click(self.position[0] + 1017, self.position[1] + 218)

        # 检查优惠券是否弹出，若有则点击我不需要，则会关闭窗口
        if utils.click_element_by_pic(self.get_page_shot("button_youhuiquan_do_not_need.png"), retry=3,
                                      sim_no_reduce=True):
            log.log_info("点击我不需要按钮，关闭优惠券弹窗")
            utils.perform_sleep(2)

        if utils.find_element_by_pic(self.get_page_shot("tab_weixin_pay.png"), retry=3, sim_no_reduce=True)[0]:
            utils.click_element_by_pic(self.get_page_shot("vip_close.png"), sim=0.85, sim_no_reduce=True)
            log.log_info("检查会员界面是否自动弹出并关闭")
            utils.perform_sleep(2)

        return not utils.find_element_by_pic(self.get_page_shot("tab_weixin_pay.png"), retry=1, sim_no_reduce=True)[0]

    @page_method_record("判断当前登录状态")
    def is_login(self):
        button_result, button_pos = utils.find_element_by_pic(self.get_page_shot("need_login_button.png"), retry=3,
                                                              sim_no_reduce=True)
        if not button_result:
            log.log_info("用户已登录")
            return True
        log.log_info("用户未登录")
        return False

    @page_method_record("点击顶部登录入口")
    def click_login_tab(self):
        utils.click_element_by_pic(
            self.get_page_shot("need_login_button.png"), sim=0.8, retry=3)

    @page_method_record("在登录窗中选择qq登录")
    def click_qq_login_button(self):
        utils.click_element_by_pic(
            self.get_page_shot("qq_login_button.png"), sim=0.8, retry=3)

    @page_method_record("判断登录窗口是否存在")
    def is_loginpage_exist(self):
        if not utils.find_element_by_pic(
            self.get_page_shot("loginpage_tab.png"), sim=0.8, retry=3)[0]:
            return False
        return True

    @page_method_record("判断QQ登录窗口是否存在")
    def is_qqloginpage_exist(self):
        if utils.find_element_by_pic(
                self.get_page_shot("qq_loginpage_logo.png"), sim=0.8, retry=3)[0] or \
                utils.find_element_by_pic(
                self.get_page_shot("qq_loginpage_logo_2.png"), sim=0.8, retry=3)[0]:
            return True
        return False

    @page_method_record("选择QQ账号密码登录方式")
    def qq_login_by_account(self):
        utils.click_element_by_pic(
            self.get_page_shot("qq_login_by_account.png"), sim=0.85, retry=3)

    @page_method_record("点击确认授权QQ登录")
    def click_qq_login_button_sure(self):
        utils.click_element_by_pic(
            self.get_page_shot("qq_login_button_sure.png"), sim=0.85, retry=3)

    @page_method_record("QQ登录窗中输入账号密码")
    def input_qqnum_and_qqpwd(self):
        num_result, num_pos = utils.find_element_by_pic(
            self.get_page_shot("qq_login_num.png"), sim=0.8, retry=3)
        if num_result:
            utils.mouse_click(num_pos)
            utils.perform_sleep(1)
            for i in Keniu_Office_QQAccount.QQNUM.value:
                utils.keyboardInputByCode(i)
                utils.perform_sleep(0.5)
        utils.perform_sleep(1)
        pwd_result, pwd_pos = utils.find_element_by_pic(
            self.get_page_shot("qq_login_pwd.png"), sim=0.8, retry=3)
        if pwd_result:
            utils.mouse_click(pwd_pos)
            utils.perform_sleep(1)
            if self.get_input_language() == "Chinese":
                utils.keyboardInputByCode('left_shift')
            for i in Keniu_Office_QQAccount.QQPWD.value:
                utils.keyboardInputByCode(i)
                utils.perform_sleep(0.5)

    @page_method_record("QQ登录")
    def qq_login(self):
        if self.is_login():
            return True
        utils.click_element_by_pic(
            self.get_page_shot("need_login_button.png"), sim=0.8, retry=3)
        utils.perform_sleep(1)
        if not self.is_loginpage_exist():
            log.log_error("登录窗口不存在")
        self.click_qq_login_button()
        utils.perform_sleep(1)
        if not self.is_qqloginpage_exist():
            log.log_error("QQ登录窗口不存在")
        self.qq_login_by_account()
        utils.perform_sleep(1)
        self.input_qqnum_and_qqpwd()
        utils.perform_sleep(1)
        self.click_qq_login_button_sure()
        utils.perform_sleep(5)
        if self.is_qqloginpage_exist() or self.is_loginpage_exist():
            log.log_error("登录后登录窗口仍存在")
            return False
        if not self.is_login():
            log.log_info("当前为未登录状态")
            return False
        log.log_info("当前为已登录状态")
        return True

    @page_method_record("关闭登录后的vip客服tips弹窗")
    def close_vip_tips(self):
        if utils.find_element_by_pic(
                self.get_page_shot("vip_tips_logo.png"), sim=0.9, retry=3)[0]:
            utils.click_element_by_pic(
                self.get_page_shot("vip_tips_sure_button.png"), sim=0.85, retry=2)
            utils.perform_sleep(1)
            if not utils.find_element_by_pic(
                    self.get_page_shot("vip_tips_logo.png"), sim=0.9, retry=3)[0]:
                log.log_info("vip_tips关闭成功")
            else:
                log.log_error("vip_tips未正常关闭")
        else:
            log.log_info("vip_tips弹窗不存在")
            return


if __name__ == '__main__':
    perfect_office_page_o = perfect_office_page()
    if perfect_office_page_o.check_vip_price():
        utils.attach_screenshot("VIP扫码功能测试成功")
    else:
        log.log_error("VIP扫码功能测试失败")
