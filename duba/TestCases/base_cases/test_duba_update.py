import allure
import pytest
from common.log import log
from duba.config import config
from duba.PageObjects.update_page import update_page


@allure.epic(f'毒霸升级场景测试（{config.ENV.value}）')
@allure.feature('场景：打开毒霸界面->打开升级界面->升级完成')
class TestDubaUpdate(object):
    @allure.story('1.毒霸升级')
    def test_duba_update(self):
        allure.dynamic.description(
            '\t1.打开主界面\n'
            '\t2.点击菜单-检查更新\n'
            '\t3.打开升级程序点击升级\n'
        )
        allure.dynamic.title('正常毒霸升级')

        with allure.step("step1：打开主界面的菜单调起升级程序"):
            up = update_page()
            ret = up.update_click()
            assert ret, log.log_error("毒霸升级失败", need_assert=False)
            log.log_pass("毒霸升级成功")


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
