import allure
import pytest
from common.log import log
from common.utils import find_element_by_pic, perform_sleep
from duba.config import config
from duba.PageObjects.login_page import LoginPage
from duba.PageObjects.vip_page import VipPageShot


@allure.epic(f'毒霸账号登录 业务流程测试（{config.ENV.value}）')
@allure.feature('场景：老金山账号登录->退出登录->快速登录')
class TestLogin(object):
    @allure.story('1.老金山账号登录')
    def test_login_ijinshan_account(self):
        allure.dynamic.description(
            '\t1.打开主界面\n'
            '\t2.点击会员中心\n'
            '\t3.使用老金山账号登录\n'
        )
        allure.dynamic.title('老金山账号登录')

        with allure.step("step1：打开主界面的会员中心，并点击用户头像"):
            lp = LoginPage()
            assert lp.open_result, log.log_error("点击用户头像失败", need_assert=False)

        with allure.step("step2：使用老金山账号登录"):
            assert lp.normal_user_login(), log.log_error("老金山账号登录失败", need_assert=False)

        with allure.step("step3：退出账号"):
            if lp.vp.logout:
                logout_result, _ = find_element_by_pic(VipPageShot.LOGIN_NOW.value)
            assert logout_result, log.log_error("退出账号失败", need_assert=False)

    @allure.story('2.快速登录')
    def test_fast_login(self):
        allure.dynamic.title('快速登录')

        with allure.step("step1：打开主界面的会员中心，并点击用户头像"):
            lp = LoginPage()
            assert lp.open_result, log.log_error("点击用户头像失败", need_assert=False)
            perform_sleep(1)

        with allure.step("step2：使用已有账号登录"):
            assert lp.login_default_account()
            perform_sleep(3)
            assert lp.vp.is_logined(), log.log_error("快速登录失败", need_assert=False)


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
