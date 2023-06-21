import time
import allure
import pytest
from common import utils
from common.log import log
from common.utils import perform_sleep
from duba.config import config
from duba.PageObjects.perfect_office_page import perfect_office_page
from duba.PageObjects.login_page import LoginPage


@allure.epic(f'可牛办公场景功能测试（{config.ENV.value}）')
@allure.feature('场景：打开可牛办公界面->登录验证->打开校验各tab界面->收藏功能测试->下载功能测试->搜索功能测试')
class TestPerfectOffice(object):
    @allure.story('1.可牛办公功能测试')
    def test_perfect_office(self):
        allure.dynamic.description("""
            1.打开可牛办公界面
            2.验证可牛办公登录
            3.打开校验各tab界面
            4.收藏功能测试
            5.下载功能测试
            6.搜索功能测试
        """)
        allure.dynamic.title('可牛办公功能测试')

        with allure.step("step1：打开可牛办公界面"):
            perfect_office_page_o = perfect_office_page()
            perform_sleep(1)
            log.log_pass("打开可牛办公界面成功")

        with allure.step("step2：验证可牛办公登录"):
            if not perfect_office_page_o.qq_login():
                log.log_error("登录验证失败")
            log.log_pass("登录验证成功")
            perform_sleep(2)
            perfect_office_page_o.close_vip_page()
            perfect_office_page_o.close_vip_tips()
            log.log_pass("登录检查完成")

        with allure.step("step3：打开校验各tab界面"):
            perfect_office_page_o.tab_click(perfect_office_page_o.get_page_shot("tab_wenzi.png"), "Word模板")
            perform_sleep(1)
            perfect_office_page_o.tab_click(perfect_office_page_o.get_page_shot("tab_biaoge.png"), "Excel模板")
            perform_sleep(1)
            perfect_office_page_o.tab_click(perfect_office_page_o.get_page_shot("tab_sheji.png"), "海报插画")
            perform_sleep(1)
            perfect_office_page_o.tab_click(perfect_office_page_o.get_page_shot("tab_yuansu.png"), "素材模板")
            perform_sleep(1)
            perfect_office_page_o.tab_click(perfect_office_page_o.get_page_shot("tab_yanshi.png"), "PPT模板")
            perform_sleep(1)
            utils.click_element_by_pic(perfect_office_page_o.get_page_shot("tab_user_center.png"), sim_no_reduce=True)
            utils.perform_sleep(2)
            utils.click_element_by_pic(perfect_office_page_o.get_page_shot("tab_mycollection.png"), sim_no_reduce=True)
            perform_sleep(1)
            if perfect_office_page_o.is_page_error():
                log.log_error("我的收藏列表页展示异常")
            log.log_info("我的收藏列表页展示正常")
            utils.click_element_by_pic(perfect_office_page_o.get_page_shot("tab_mydownload.png"), sim_no_reduce=True)
            perform_sleep(1)
            if perfect_office_page_o.is_page_error():
                log.log_error("我的下载列表页展示异常")
            log.log_info("我的下载列表页展示正常")
            log.log_pass("打开可牛办公各tab界面成功")

        with allure.step("step4：收藏功能测试"):
            # 以PPT模板作为验证对象
            sum_old = perfect_office_page_o.statistics_collected_num()
            # 切换回PPT模板列表页
            utils.click_element_by_pic(perfect_office_page_o.get_page_shot("tab_yanshi.png"), sim=0.8, retry=3)
            utils.perform_sleep(3)
            perfect_office_page_o.click_collect_button()
            utils.perform_sleep(1)
            sum_new = perfect_office_page_o.statistics_collected_num()
            if not sum_new == sum_old + 1:
                log.log_info(f"原先已收藏模板数量{sum_old}")
                log.log_info(f"现在已收藏模板数量{sum_new}")
                log.log_error("收藏后未新增收藏记录")
            log.log_pass("收藏后新增了收藏记录")

        with allure.step("step5: 下载功能验证"):
            # 以PPT模板作为验证对象
            utils.perform_sleep(2)
            # 切换回PPT模板列表页
            utils.click_element_by_pic(perfect_office_page_o.get_page_shot("tab_yanshi.png"), sim_no_reduce=True)
            utils.perform_sleep(3)
            perfect_office_page_o.click_download_button()
            utils.perform_sleep(1)
            if not perfect_office_page_o.is_downloading():
                log.log_error("不存在新下载记录")
            log.log_pass("存在新下载记录")

        with allure.step("step6：搜索功能测试"):
            perfect_office_page_o.search_click()
            perform_sleep(1)
            mouse_x, mouse_y = utils.get_mouse_point()
            utils.mouse_click(mouse_x - 100, mouse_y + 35)
            perform_sleep(3)

            download_res, download_pos = utils.find_element_by_pic(
                perfect_office_page_o.get_page_shot("expect_download_pic.png"), sim=0.7, sim_no_reduce=True)
            if not download_res:
                log.log_error("查找搜索结果页下载按钮失败")

            utils.mouse_move(*download_pos)
            for i in range(10):
                utils.mouse_scroll(500)
                time.sleep(0.5)

            if not utils.find_element_by_pic(perfect_office_page_o.get_page_shot("expect_page_size.png"),
                                             sim_no_reduce=True)[0]:
                log.log_error("查找搜索结果页分页栏失败")

            utils.mouse_click(perfect_office_page_o.position[0] + 30, perfect_office_page_o.position[1] + 20)
            log.log_info("返回主页")
            utils.attach_screenshot("返回主页")

        # with allure.step("step7：VIP扫码功能测试"):
        #     if perfect_office_page_o.check_vip_price():
        #         utils.attach_screenshot("VIP扫码功能测试成功")
        #     else:
        #         log.log_error("VIP扫码功能测试失败")

if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
