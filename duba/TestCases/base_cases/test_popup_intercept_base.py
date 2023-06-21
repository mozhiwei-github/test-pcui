import allure
import pytest
from common import utils
from common.contants import Host
from common.log import log
from common.utils import perform_sleep, find_element_by_pic
from duba.PageObjects.login_page import LoginPage
from duba.PageObjects.popup_intercept_page import PopupInterceptPage
from duba.PageObjects.vip_page import vip_page, VipPageShot
from duba.config import config
from duba.contants import UserType, Env

# 目前正式服只有游客和非会员账号
from duba.utils import login_normal_user, login_super_vip

USER_TYPE_LIST = UserType if config.ENV == Env.TEST else [UserType.GUEST, UserType.NON_VIP]


@allure.epic(f'弹窗拦截场景功能测试（{config.ENV.value}）')
@allure.feature('场景1：普通用户场景；场景2：会员场景')
class TestPopUpintercept(object):
    @allure.story('1.普通用户场景功能测试')
    def test_popup_intercept(self):
        allure.dynamic.description(
            '\t1.打开弹窗拦截界面\n'
            '\t2.登录普通用户\n'
            '\t3.执行模拟弹窗样本，弹窗盖帽测试\n'
            '\t4.检查拦截记录\n'
        )
        allure.dynamic.title('弹窗拦截场景普通用户功能测试')

        with allure.step("step0：切换到毒霸服务端测试服"):
            utils.modify_host(Host.DUBA_SERVER_TEST.value)

        with allure.step("step1：打开弹窗拦截界面"):
            PopupInterceptPage_o = PopupInterceptPage()
            pass

        with allure.step("step2：登录普通用户"):
            login_normal_user(PopupInterceptPage_o)
            pass

        with allure.step("step3：执行模拟弹窗样本，弹窗盖帽测试"):
            assert PopupInterceptPage_o.clear_block_mark(), "清空拦截记录失败"
            assert PopupInterceptPage_o.clear_no_block_mark(), "清空不拦截记录失败"
            assert PopupInterceptPage_o.execute_demo_exe("ucalendar.exe"), "执行样本失败"
            utils.attach_screenshot("执行ucalendar.exe样本")
            assert PopupInterceptPage_o.click_block_hat_pop(), "点击拦截泡泡盖帽失败。若截图无广告窗口，请检查环境是否只有毒霸一款弹窗拦截产品"
            if utils.is_process_exists("ucalendar.exe"):
                utils.kill_process_by_name("ucalendar.exe")

        with allure.step("step4：检查拦截记录"):
            if utils.click_element_by_pic(PopupInterceptPage_o.get_page_shot("button_block_mark.png"), retry=2,
                                          sim_no_reduce=True):
                if utils.find_element_by_pic(PopupInterceptPage_o.get_page_shot("button_all_cancel.png"), retry=2,
                                             sim_no_reduce=True)[0]:
                    log.log_pass("检查有拦截记录成功")
                    utils.click_element_by_pic(PopupInterceptPage_o.get_page_shot("button_all_cancel.png"), retry=2,
                                               sim_no_reduce=True)
            # 关闭拦截了记录
            utils.perform_sleep(1)
            utils.keyboardInputAltF4()

    @allure.story('2.会员场景功能测试')
    def test_popup_vip_intercept(self):
        allure.dynamic.description(
            '\t1.打开弹窗拦截界面\n'
            '\t2.登录会员用户\n'
            '\t3.执行模拟弹窗样本，自动弹窗拦截测试\n'
            '\t4.检查拦截记录\n'
        )
        allure.dynamic.title('弹窗拦截场景会员用户功能测试')

        with allure.step("step1：打开弹窗拦截界面"):
            PopupInterceptPage_o_vip = PopupInterceptPage()
            pass

        with allure.step("step2：登录超级会员"):
            login_super_vip(PopupInterceptPage_o_vip, username="golanger030", password="kingsoft")
            pass

        with allure.step("step3：执行模拟弹窗样本，自动弹窗拦截测试"):
            assert PopupInterceptPage_o_vip.clear_block_mark(), "清空拦截记录失败"
            assert PopupInterceptPage_o_vip.clear_no_block_mark(), "清空不拦截记录失败"
            assert PopupInterceptPage_o_vip.execute_demo_exe("winrar.exe"), "执行样本失败"
            utils.attach_screenshot("执行winrar.exe样本")
            assert PopupInterceptPage_o_vip.click_block_hat_pop(), "点击拦截泡泡盖帽失败。若截图无广告窗口，请检查环境是否只有毒霸一款弹窗拦截产品"
            if utils.is_process_exists("winrar.exe"):
                utils.kill_process_by_name("winrar.exe")
            pass

        with allure.step("step4：检查拦截记录"):
            if utils.click_element_by_pic(PopupInterceptPage_o_vip.get_page_shot("button_no_block_mark.png"), retry=2,
                                          sim_no_reduce=True):
                if utils.find_element_by_pic(PopupInterceptPage_o_vip.get_page_shot("button_all_cancel.png"), retry=2,
                                             sim_no_reduce=True)[0]:
                    log.log_pass("检查有不拦截记录成功")
                    utils.click_element_by_pic(PopupInterceptPage_o_vip.get_page_shot("button_all_cancel.png"), retry=2,
                                               sim_no_reduce=True)
            pass
            # 关闭拦截了记录
            utils.perform_sleep(1)
            utils.keyboardInputAltF4()

if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
