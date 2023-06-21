import allure
import pytest

from common import utils
from common.log import log
from common.tools.duba_tools import rename_and_recover_kpopcenter, rename_kpopcenter, recover_kpopcenter
from duba.PageObjects.disk_manage_pre_swept_page import DiskManagePreSweptPage, set_kvipapp_setting, del_popdata, \
    del_runtime_info_cache, check_pre_scan_process_up, check_pre_scan_result, set_pop_time_to_yesterday
from duba.PageObjects.setting_page import SettingPage
from duba.config import config
from duba.utils import DubaFilePath


def restart_kxetray():
    """ 重启托盘 """
    utils.kill_process_by_name("kxetray.exe")
    utils.process_start(DubaFilePath.kxetray_file_path, async_start=True)


def check_sacn_process(obj, process, section):
    """
    校验预扫进程用例
    :param obj: 对象，传磁盘管理实例对象
    :param process: 所检查的预扫进程
    :param section: 所检查的预扫结果的section
    :return:
    """
    utils.perform_sleep(60)
    res = check_pre_scan_process_up(process, section)
    assert res, log.log_error("没有调起预扫进程，也没有预扫结果，检查日志: kxetray.ktrashmon.dll.log", need_assert=False)
    if res:
        res1 = obj.check_pre_sacn_exit(process)
        assert res1, log.log_error("5分钟内，预扫进程仍未退出", need_assert=False)
        log.log_pass("预扫进程已退出")


def check_sacn_result(section):
    """
    检查是否有预扫结果
    :param section: 所检查的预扫结果的section
    :return:
    """
    res2 = check_pre_scan_result(section)
    assert res2, log.log_error("无预扫结果", need_assert=False)
    log.log_pass("已生成预扫记录")


def check_pop(obj):
    """ 检查是否弹泡，并关闭 """
    res3 = obj.click_pop_close_btn()
    assert res3, log.log_error("无检测到泡泡关闭按钮", need_assert=False)
    log.log_pass("已弹泡，并关闭")


@pytest.fixture(scope="class", autouse=True)
def preconditions():
    """
    前置条件
    :return:
    """
    close = SettingPage()
    close.self_protecting_close()
    rename_kpopcenter()


@pytest.fixture(scope="class", autouse=True)
def post_operation():
    """
    后置操作
    :return:
    """
    yield 1
    recover_kpopcenter()
    utils.kill_process_by_name("kxetray.exe")


@allure.epic(f'磁盘管理预扫弹泡测试（{config.ENV.value}）')
@allure.feature('场景：启动kxetray.exe，进入预扫流程')
class TestDiskMangePreSwept(object):

    @allure.story('大文件专清')
    def test_klargecleanup_pre_swept(self):
        allure.dynamic.description(
            '\t1.大文件专清，预扫检查\n'
            '\t2.大文件专清，推广泡检查\n'
        )
        allure.dynamic.title('大文件专清预扫和弹泡功能')

        with allure.step("step1：大文件专清预扫--右下角弹泡流程测试"):
            test = DiskManagePreSweptPage()
            set_kvipapp_setting()
            del_popdata()
            del_runtime_info_cache()

            restart_kxetray()
            check_sacn_process(test, "klargecleanup.exe", "largeclean")
            check_sacn_result("largeclean")
            check_pop(test)

        with allure.step("step2：大文件专清预扫--win10弹泡流程测试"):
            set_pop_time_to_yesterday("kdisk_mgr_pop")

            restart_kxetray()
            utils.perform_sleep(62)  # 重启托盘，需要等待一分钟才弹泡
            check_pop(test)

    @allure.story('重复文件专清')
    def test_kdupcleanup_pre_swept(self):
        allure.dynamic.description(
            '\t1.重复文件专清，预扫检查\n'
            '\t2.重复文件专清，推广泡检查\n'
        )
        allure.dynamic.title('重复文件预扫和弹泡功能')

        with allure.step("step1：重复文件专清预扫--右下角弹泡流程测试"):
            test = DiskManagePreSweptPage()
            set_kvipapp_setting()
            del_popdata()
            set_pop_time_to_yesterday("kdisk_mgr_pop")
            set_pop_time_to_yesterday("kdisk_mgr_pop_win_toast")
            del_runtime_info_cache()

            restart_kxetray()
            check_sacn_process(test, "kdupcleanup.exe", "repeatclean")
            check_sacn_result("repeatclean")
            check_pop(test)

        with allure.step("step2：重复专清预扫--win10弹泡流程测试"):
            set_pop_time_to_yesterday("kdiskopt_dupclean")

            restart_kxetray()
            utils.perform_sleep(62)  # 重启托盘，需要等待一分钟才弹泡
            check_pop(test)

    @allure.story('微信专清')
    def test_kwechatcleanup_pre_swept(self):
        allure.dynamic.description(
            '\t1.微信专清，预扫检查\n'
            '\t2.微信专清，推广泡检查\n'
        )
        allure.dynamic.title('微信专清预扫和弹泡功能')

        with allure.step("step1：微信专清预扫--右下角弹泡流程测试"):
            test = DiskManagePreSweptPage()
            set_kvipapp_setting()
            del_popdata()
            set_pop_time_to_yesterday("kdisk_mgr_pop")
            set_pop_time_to_yesterday("kdisk_mgr_pop_win_toast")
            set_pop_time_to_yesterday("kdiskopt_dupclean")
            set_pop_time_to_yesterday("kdiskopt_dupclean_win_toast")
            del_runtime_info_cache()

            restart_kxetray()
            check_sacn_process(test, "kwechatcleanup.exe", "wechatclean")
            check_sacn_result("wechatclean")
            check_pop(test)

        with allure.step("step2：微信专清预扫--win10弹泡流程测试"):
            set_pop_time_to_yesterday("kdiskopt_wechatclean")

            restart_kxetray()
            utils.perform_sleep(62)  # 重启托盘，需要等待一分钟才弹泡
            check_pop(test)

    @allure.story('qq专清')
    def test_kqqcleanup_pre_swept(self):
        allure.dynamic.description(
            '\t1.qq专清专清，预扫检查\n'
            '\t2.qq专清专清，推广泡检查\n'
        )
        allure.dynamic.title('qq专清预扫和弹泡功能')

        with allure.step("step1：qq专清预扫--右下角弹泡流程测试"):
            test = DiskManagePreSweptPage()
            set_kvipapp_setting()
            del_popdata()
            set_pop_time_to_yesterday("kdisk_mgr_pop")
            set_pop_time_to_yesterday("kdisk_mgr_pop_win_toast")
            set_pop_time_to_yesterday("kdiskopt_dupclean")
            set_pop_time_to_yesterday("kdiskopt_dupclean_win_toast")
            set_pop_time_to_yesterday("kdiskopt_wechatclean")
            set_pop_time_to_yesterday("kdiskopt_wechatclean_win_toast")
            del_runtime_info_cache()

            restart_kxetray()
            check_sacn_process(test, "kqqcleanup.exe", "QQclean")
            check_sacn_result("QQclean")
            check_pop(test)

        # 目前qq专清win10泡是关闭的，故暂不检查
        # with allure.step("step2：qq专清预扫--win10弹泡流程测试"):
        #     set_pop_time_to_yesterday("kdiskopt_qqclean")
        #
        #     restart_kxetray()
        #     utils.perform_sleep(62)  # 重启托盘，需要等待一分钟才弹泡
        #     check_pop(test)


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
