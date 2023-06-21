import allure
import pytest

from common import utils
from common.contants import Host
from common.log import log
from duba.PageObjects.privacy_cleaner_page import PrivacyCleanerPage
from duba.config import config
from duba.utils import login_super_vip


@pytest.fixture(scope="class", autouse=True)
def switch_host():
    """
    切换到毒霸服务端测试服
    """
    utils.modify_host(Host.DUBA_SERVER_TEST.value)
    log.log_info("切换到毒霸服务端测试服")
    utils.copy_to_clipboard("utils function")  # 剪切板模拟添加内容


@allure.epic(f'毒霸隐私清理基础场景测试（{config.ENV.value}）')
@allure.feature('场景：打开毒霸界面->打开会员中心->打开隐私清理界面')
class TestKsysslimBase(object):
    @allure.story('1.会员场景测试')
    def test_privacy_cleaner_vip_base(self):
        allure.dynamic.description(
            '\t1.扫描结果检查\n'
            '\t2.清理检查\n'
        )
        allure.dynamic.title('隐私清理会员场景测试')

        with allure.step("step1：登录超级会员"):
            privacy = PrivacyCleanerPage()
            login_super_vip(privacy, username="golanger030", password="kingsoft")
            pass

        with allure.step("step2：检查清理功能"):
            privacy.click_start_scanning_button()        # 点击开始扫描
            privacy.close_password_tips()     # 关闭蒙层
            privacy.check_scaning()           # 检查是否还在扫描
            privacy.close_high_rish_remind_tab()     # 关闭高风险提示
            privacy.click_sensitive_privacy_item()   # 勾选清理项
            privacy.click_clean()             # 点击清理
            privacy.click_close_occupy()      # 关闭垃圾清理占用窗口  如浏览器被占用
            ret1 = privacy.check_cleaning()   # 检查清理
            ret2 = privacy.check_clipboard()  # 检查剪切板
            assert ret1, log.log_error("清理时间过长", need_assert=False)
            log.log_pass("清理结束，界面显示正常")
            assert ret2, log.log_error("清理剪切板失败，功能异常", need_assert=False)
            log.log_pass("清理功能正常，剪切板已被清空")


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])



