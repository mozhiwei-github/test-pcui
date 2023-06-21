import allure
import pytest

from common import utils
from common.log import log
from common.utils import perform_sleep
from duba.PageObjects.clean_master_page import CleanMasterPage
from duba.PageObjects.clean_master_pre_swept_page import CleanMasterPreSweptBubble
from duba.config import config


@allure.epic(f'独立版C盘瘦身场景测试（{config.ENV.value}）')
@allure.feature('场景：打开C盘瘦身独立版->点击各tab场景测试')
class TestDuliCslimming(object):
    @allure.story('独立版C盘瘦身测试')
    def test_duli_cslimming(self):
        allure.dynamic.description(
            '\t1.打开主界面\n'
            '\t2.C盘瘦身tab检查\n'
            '\t3.垃圾清理tab检查\n'
            '\t4.电脑加速tab检查\n'
            '\t5.隐私清理tab检查\n'
            '\t6.碎片清理tab检查\n'
            '\t7.弹窗拦截tab检查\n'
            '\t8.文件粉碎tab检查\n'
        )
        allure.dynamic.title('独立版C盘瘦身场景测试')

        with allure.step("step1：打开主界面"):
            duli_c_slimming_page_o = CleanMasterPage()
            perform_sleep(3)

        with allure.step("step2：C盘瘦身tab检查"):
            if duli_c_slimming_page_o.tab_click_c_slimming():
                log.log_pass("C盘瘦身tab检查成功")
            perform_sleep(3)

        with allure.step("step3：垃圾清理tab检查"):
            duli_c_slimming_page_o.check_clean_trash_tab()
            log.log_pass("垃圾清理tab检查成功")
            perform_sleep(3)

        with allure.step("step4：电脑加速tab检查"):
            duli_c_slimming_page_o.check_accelerate_tab()
            log.log_pass("电脑加速tab检查成功")
            perform_sleep(3)

        with allure.step("step5：隐私清理tab检查"):
            duli_c_slimming_page_o.check_privacy_clean_tab()
            log.log_pass("隐私清理tab检查成功")
            perform_sleep(3)

        with allure.step("step6：碎片清理tab检查"):
            if duli_c_slimming_page_o.tab_click_defrag():
                log.log_pass("碎片清理王tab检查成功")
            else:
                log.log_error("碎片清理王tab检查失败")
            perform_sleep(3)

        with allure.step("step7：弹窗拦截tab检查"):
            if duli_c_slimming_page_o.tab_click_pop_intercept():
                log.log_pass("弹窗拦截tab检查成功")
            else:
                log.log_error("弹窗拦截tab检查失败")
            perform_sleep(3)

        with allure.step("step8：文件粉碎tab检查"):
            if duli_c_slimming_page_o.tab_click_file_destroy():
                log.log_pass("文件粉碎tab检查成功")
            else:
                log.log_error("文件粉碎tab检查失败")
            perform_sleep(3)

        with allure.step("step9：碎片清理预扫泡检查"):
            preswept = CleanMasterPreSweptBubble()
            param = "{\"popname\":\"defrag_pop\",\"size\":\"1000\"}"
            preswept.modify_kplanetcache(param=param)
            cmdline = " -app:pop -task:\"pure_vip_noad_pop\" -wait:0 -mask:0"
            duli_c_slimming_page_o.scan_pop("kfixstar.exe", cmdline)
            if duli_c_slimming_page_o.check_defage_scan_pop():
                log.log_pass("碎片清理预扫泡检查成功")
            else:
                log.log_error("碎片清理预扫泡功能异常")
            perform_sleep(3)

if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
