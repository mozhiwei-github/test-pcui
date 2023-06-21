import allure
import pytest

from common.contants import Host
from common.log import log
from common import utils
from duba.PageObjects.file_shredding_page import FileShreddingPage, pull_file
from duba.config import config
from duba.utils import login_super_vip


@pytest.fixture(scope="class", autouse=True)
def test_before():
    utils.modify_host(Host.DUBA_SERVER_TEST.value)
    pull_file()


@allure.epic(f'毒霸文件粉碎会员场景测试（{config.ENV.value}）')
@allure.feature('场景：打开毒霸界面->打开会员中心->打开碎片清理理界面')
class TestFileShreddingVip(object):
    @allure.story('1.会员场景测试')
    def test_file_shredding_vip(self):
        allure.dynamic.description(
            '\t1.添加文件'
            '\t2.执行粉碎'
        )
        allure.dynamic.title('隐私清理会员场景测试')

        with allure.step("step1: 登录超级会员"):
            filesherdding = FileShreddingPage()
            login_super_vip(filesherdding, username="golanger030", password="kingsoft")
            pass

        with allure.step("step2：检查粉碎功能"):
            filesherdding.click_add_file_button()
            res, pos = utils.find_element_by_pic(filesherdding.get_page_shot("add_file_open_button.png"))
            utils.perform_sleep(2)
            utils.mouse_click_int(pos[0] - 180, pos[1])
            utils.copy_to_clipboard("\"c:\\FileShredding\\11.exe\" \"c:\\FileShredding\\22.exe\" "
                                    "\"c:\\FileShredding\\33.exe\"")
            utils.key_paste()
            filesherdding.click_add_file_open_button()
            filesherdding.click_start_shredding_button()
            filesherdding.click_confirm_btn()
            res = filesherdding.check_clean_finished()
            assert res, log.log_error("文件粉碎功能异常", need_assert=False)
            log.log_pass("文件粉碎功能正常")


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
