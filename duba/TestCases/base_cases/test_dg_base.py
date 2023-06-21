import allure
import pytest
from common.log import log
from common.utils import perform_sleep
from duba.PageObjects.dg_page import DgPage
from duba.config import config



@allure.epic(f'驱动精灵基础场景测试（{config.ENV.value}）')
@allure.feature('场景：打开驱动精灵->点击立即检测')
class TestDgBase(object):
    @allure.story('1.驱动精灵全面体检')
    def test_dg_base(self):
        allure.dynamic.description(
            '\t1.-------\n'
            '\t2.-------\n'
        )
        allure.dynamic.title('电脑体检基本功能')

        with allure.step("step1：执行电脑体检功能"):
            dg = DgPage()
            dg.click_to_examination()
            dg.check_examing()
            dg.click_back_button()

        with allure.step("step2：执行垃圾清理功能"):
            dg = DgPage()
            dg.click_to_clean()
            dg.check_clean_scanning()
            dg.click_start_clean_button()
            dg.check_warning()
            dg.check_cleaning()
            dg.click_close_button()

if __name__ == '__main__':
    # pytest.main(["-v", "-s", __file__])
    test = TestDgBase()
    test.test_dg_base()
