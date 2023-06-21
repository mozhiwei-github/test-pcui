from common.log import log
import allure
from duba.config import config
import pytest
from duba.PageObjects.device_info_page import DeviceInfoPage
from common import utils
import os

@allure.epic(f"设备管理-电脑状态功能用例测试({config.ENV.value})")
@allure.feature("设备管理-电脑状态功能用例测试")
class TestDeviceInfo(object):
    @allure.story("设备管理-电脑状态功能用例测试")
    def test_device_info(self):
        allure.dynamic.description(
            '\tstep1:循环调起电脑状态界面并执行关闭\n'
        )
        allure.dynamic.title('设备管理-电脑状态功能用例测试')

        with allure.step("step1:循环调起电脑状态界面并执行关闭"):
            dump_path = r"C:\Users\admin\AppData\Local\Temp\KingsoftDump"
            try_num_max = 50
            try_no = 0
            while try_no <= try_num_max:
                try_no += 1
                if os.path.exists(dump_path):
                    utils.remove_path(dump_path)
                deviceInfoPage = DeviceInfoPage()
                utils.perform_sleep(10)
                deviceInfoPage.click_close_button()
                utils.perform_sleep(1)
                if deviceInfoPage.is_satisfction_exist():
                    if not deviceInfoPage.close_satisfction_page():
                        log.log_error("满意度调查窗口关闭失败")
                    log.log_pass("满意度调查窗口关闭成功")
                utils.perform_sleep(1)
                if not os.path.exists(dump_path):
                    log.log_info(f"第{try_no}次尝试，未出现dump")
                else:
                    log.log_info(f"第{try_no}次尝试，出现了dump！！！！！！")

if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])