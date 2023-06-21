# --coding = 'utf-8' --
from common import utils
from common.unexpectwin_system import UnExpectWin_System
from common.utils import perform_sleep
from common.log import log
from common.basepage import BasePage, page_method_record
from duba.config import config
from duba.contants import UserType
from duba.PageObjects import vip_page
from duba.PageObjects.unexpected_popup import UnexpectedPopup, UnexpectedPopupInfo

"""登录页"""

# 用户类型对照配置文件账号
UserTypeToAccountConfig = {
    UserType.NON_VIP: config.NON_VIP_ACCOUNT,
    UserType.COMMON_VIP: config.COMMON_VIP_ACCOUNT,
    UserType.DIAMOND_VIP: config.DIAMOND_VIP_ACCOUNT,
    UserType.SUPER_VIP: config.SUPER_VIP_ACCOUNT,
    UserType.HONOR_VIP: config.HONOR_VIP_ACCOUNT,
    UserType.QQ: config.QQ_ACCOUNT,
}


class LoginPage(BasePage):
    def __init__(self, do_pre_open=True, page_desc=None, init_user_type=False):
        """
        登录页构造函数
        @param do_pre_open: 执行打开界面操作
        @param page_desc: 页面描述名称
        @param init_user_type: 是否需要检测当前用户类型（检测用户类型函数耗时较长）
        """
        self.init_user_type = init_user_type

        super().__init__(do_pre_open=do_pre_open, page_desc=page_desc)

    def pre_open(self):
        self.vp = vip_page.vip_page(init_user_type=self.init_user_type)
        self.vp.user_login_click()
        if UnExpectWin_System().unexpectwin_detect():
            self.vp.user_login_click()

    def reset_page_status(self):
        """
        如果账号登录后，登录页自动关闭，则把is_allow_close置为false，在page_close里不执行关闭
        """
        perform_sleep(3)
        if not self.find_login_tab():
            self.is_allow_close = False

    @page_method_record("QQ账号登陆")
    def qq_login(self, username, password):
        log.log_info("查找qq账号登录入口")
        if utils.click_element_by_pic(self.get_page_shot("button_qq_entry.png"), retry=10, sim_no_reduce=True):
            perform_sleep(10)
            if utils.click_element_by_pic(self.get_page_shot("button_account_login.png"), retry=10, sim_no_reduce=True):
                log.log_info("点击使用QQ账号登录")
                utils.mouse_click(utils.get_mouse_point()[0] + 74, utils.get_mouse_point()[1] - 179)
                # 默认坐标定位到账号框，先进行清除操作
                for i in range(20):
                    utils.keyboardInputByCode("backspace")
                    perform_sleep(0.3)
                utils.key_input(username)
                perform_sleep(0.3)
                utils.keyboardInputByCode("tab")
                perform_sleep(0.3)
                utils.key_input(password)
                perform_sleep(0.3)
                utils.keyboardInputEnter()
                perform_sleep(0.3)
                utils.keyboardInputEnter()
                self.reset_page_status()
                # 通过vip会员界面打开的登录窗才执行规避校验操作
                if self.do_pre_open:
                    UnexpectedPopup.popup_process(UnexpectedPopupInfo.TIME_LIMITED_BENEFITS, find_retry=5,
                                                  hwnd=self.vp.hwnd)
                    perform_sleep(1)
                    result = self.vp.is_logined()
                log.log_info(f"QQ账号登录{'成功' if result else '失败'}")
                return result
        return False

    @page_method_record("金山通行证账号登录(老会员)")
    def ijinshan_login(self, username, password):
        log.log_info(f"账号：{username}, 密码：{password}")
        log.log_info("查找金山通行证登录入口")
        utils.click_element_by_pic(self.get_page_shot("other_account.png"), retry=3, sim_no_reduce=True)

        ijinshan_account, ijinshan_account_position = utils.find_element_by_pic(
            self.get_page_shot("ijinshan_account.png"), 0.9, sim_no_reduce=True)
        if ijinshan_account:
            utils.mouse_click(ijinshan_account_position)
        else:
            log.log_error("找不到金山通行证登录入口")

        # 获取账号密码位置，输入账号密码
        utils.click_element_by_pic(self.get_page_shot("user_input_ijinshan.png"), retry=3, sim_no_reduce=True)
        perform_sleep(0.3)
        utils.copy_to_clipboard(username)
        utils.key_paste()

        utils.click_element_by_pic(self.get_page_shot("pwd_input_ijinshan.png"), retry=3, sim_no_reduce=True)
        perform_sleep(0.3)
        utils.copy_to_clipboard(password)
        utils.key_paste()

        # 点击登录
        utils.click_element_by_pic(self.get_page_shot("button_ijinshan_login.png"), retry=3, sim_no_reduce=True)

        self.reset_page_status()

        result = True
        # 通过vip会员界面打开的登录窗才执行规避校验操作
        if self.do_pre_open:
            UnexpectedPopup.popup_process(UnexpectedPopupInfo.TIME_LIMITED_BENEFITS, find_retry=5, hwnd=self.vp.hwnd)
            perform_sleep(1)

            result = self.vp.is_logined()
        log.log_info(f"金山通行证账号登录{'成功' if result else '失败'}")

        return result

    def do_user_login(self, user_type, username=None, password=None):
        """
        用户登录
        @param user_type: 用户类型
        @param username: 用户名
        @param password: 密码
        @return:
        """
        if not username or not password:
            # 未传用户名、密码参数时，从配置文件中获取
            account_config = UserTypeToAccountConfig[user_type]
            if not account_config:
                log.log_error(f"配置文件中未找到 {user_type.value} 账号")
                return False
            username = account_config.username
            password = account_config.password
        # 判断用户类型为是否用QQ登录
        if user_type == UserType.QQ:
            login_result = self.qq_login(username, password)
        else:
            # 使用金山通行证方式登录
            login_result = self.ijinshan_login(username, password)
        if login_result and self.do_pre_open:
            self.vp.user_type = user_type
        log.log_info(f"当前用户类型为：{user_type.value}")
        return login_result

    @page_method_record("设备授权")
    def device_num_remove(self):
        res, pos = utils.find_element_by_pic(self.get_page_shot("reminder_tab.png"))
        if not res:
            return
        log.log_info("弹出设备管理弹窗")
        utils.click_element_by_pic(self.get_page_shot("device_manager_btn.png"))
        utils.click_element_by_pic(self.get_page_shot("remove_btn.png"))
        utils.click_element_by_pic(self.get_page_shot("sure_btn.png"))
        res, pos = utils.find_element_by_pic(self.get_page_shot("device_manager_tab.png"))
        utils.mouse_click_int(pos[0]+506, pos[1])  # 关闭电脑管理页面
        return self.super_vip_user_login()

    @page_method_record("登录普通用户账号")
    def normal_user_login(self, username=None, password=None):
        return self.do_user_login(UserType.NON_VIP, username, password)

    @page_method_record("登录普通会员用户账号")
    def common_vip_user_login(self, username=None, password=None):
        return self.do_user_login(UserType.COMMON_VIP, username, password)

    @page_method_record("登录超级会员用户账号")
    def super_vip_user_login(self, username=None, password=None):
        return self.do_user_login(UserType.SUPER_VIP, username, password)

    @page_method_record("登录钻石会员用户账号")
    def diamond_vip_user_login(self, username=None, password=None):
        return self.do_user_login(UserType.DIAMOND_VIP, username, password)

    @page_method_record("登录荣誉会员用户账号")
    def honor_vip_user_login(self, username=None, password=None):
        return self.do_user_login(UserType.HONOR_VIP, username, password)

    @page_method_record("登录QQ会员用户账号")
    def qq_user_login(self, username=None, password=None):
        return self.do_user_login(UserType.QQ, username, password)

    @page_method_record("点击第一个快速登录的账号")
    def login_default_account(self):
        utils.mouse_click(self.position[0] + 80, self.position[1] + 145)
        self.reset_page_status()
        return not self.find_login_tab()

    @page_method_record("寻找快速登录页的logo")
    def find_login_tab(self):
        return \
            utils.find_element_by_pic(self.get_page_shot("tab_login_logo.png"), retry=3, sim=0.9, sim_no_reduce=True)[0]

    @page_method_record("查找并退出快速登录弹窗")
    def find_and_exit_login_tab(self):
        if self.find_login_tab:
            return utils.click_element_by_pic(self.get_page_shot("exit_login.png"), retry=3, sim_no_reduce=True)
        log.log_info("未找到快速登录弹窗")
        return False


if __name__ == '__main__':
    page = LoginPage()
    # 普通用户登录
    page.qq_user_login()
