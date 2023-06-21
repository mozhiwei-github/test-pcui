import allure
import pytest
from common.log import log
from common.utils import perform_sleep
from duba.config import config
from duba.PageObjects.c_slimming_page import CreateGarbage, dgCSlimmingPage


@allure.epic(f'精灵C盘瘦身基础场景测试（{config.ENV.value}）')
@allure.feature('场景：打开精灵微信专清')
class TestKsysslimBase(object):
    @allure.story('1.C盘瘦身基础场景')
    def test_ksysslim_base(self):
        allure.dynamic.description(
            '\t1.执行C盘瘦身垃圾清理功能\n'
            '\t2.执行大文件搬家功能\n'
            '\t2.执行软件搬家功能\n'
        )
        allure.dynamic.title('C盘瘦身基本功能')

        with allure.step("step1：执行C盘瘦身垃圾清理功能"):
            grab = CreateGarbage()
            retgb = grab.create_garbage()
            assert retgb, "下拉文件失败！！"
            log.log_pass("下拉文件成功")
            dgksysslim = dgCSlimmingPage()
            dgksysslim.click_scan_button()
            dgksysslim.click_to_slimming()
            ret = dgksysslim.ksysslim_check_clean()
            assert ret, "C盘瘦身基本功能异常！！"
            log.log_pass("C盘瘦身基本功能正常")
            perform_sleep(1)

        with allure.step("step2：执行大文件搬家功能"):
            dgksysslim.click_continue_button()
            dgksysslim.click_to_slimming_bigfilemoving()
            ret2 = dgksysslim.big_file_moving_check_clean()
            assert ret2, "大文件搬家功能异常"
            log.log_pass("大文件搬家功能正常")

        with allure.step("step3：执行软件搬家功能"):
            dgksysslim.click_to_software_moving()
            ret3 = dgksysslim.software_moving_check_clean()
            assert ret3, "软件搬家功能异常"
            log.log_pass("软件搬家功能正常")


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
