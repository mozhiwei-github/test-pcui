import allure
import pytest

from common import utils
from common.log import log
from common.utils import perform_sleep, find_element_by_pic
from duba.PageObjects.mycomputerpro_page import mycomputerpro_page
from duba.config import config
from duba.PageObjects.c_slimming_page import CSlimmingPage, CreateGarbage


@allure.epic(f'毒霸我的电脑pro基础场景测试（{config.ENV.value}）')
@allure.feature('场景：打开毒霸界面->打开会员中心->打开我的电脑pro界面')
class TestKsysslimBase(object):
    @allure.story('1.我的电脑pro基础场景')
    def test_ksysslim_base(self):
        allure.dynamic.description(
            '\t1.打开百宝箱启动我的电脑pro\n'
            '\t2.执行常规测试操作\n'
        )
        allure.dynamic.title('我的电脑pro基本功能')
        mycomputerpro_page_o = mycomputerpro_page()
        with allure.step("执行常规测试操作"):
            if mycomputerpro_page_o.open_patten_c():
                log.log_pass("打开本地磁盘C成功")
            else:
                log.log_error("打开本地磁盘C失败")
            perform_sleep(3)

            if mycomputerpro_page_o.back_upper_folder():
                log.log_pass("返回上一级目录成功")
            else:
                log.log_pass("返回上一级目录失败")
            perform_sleep(3)

            if mycomputerpro_page_o.add_tab_page():
                log.log_pass("新增tab页成功")
            else:
                log.log_error("新增tab页失败")
            perform_sleep(3)

        with allure.step("执行书签测试操作"):
            find_icon_favious, pos_icon_faious = find_element_by_pic(
                mycomputerpro_page_o.get_page_shot("icon_favious.png"), retry=2, sim_no_reduce=True)

            for i in range(1, 5, 1):  # 重复5遍判断添加书签提示是否存在
                find_tip_add_favious, pos_tip_add_favious = find_element_by_pic(
                    mycomputerpro_page_o.get_page_shot("tip_add_favious.png"), retry=2, sim_no_reduce=True)
                if not find_tip_add_favious:
                    utils.mouse_right_click(pos_icon_faious[0] + 20, pos_icon_faious[1])
                    utils.click_element_by_pic(mycomputerpro_page_o.get_page_shot("button_del_favious.png"), retry=2,
                                               sim_no_reduce=True)
                else:
                    break
                perform_sleep(2)

            if find_icon_favious:
                find_button_bendicipanC, pos_button_bendicipanC = find_element_by_pic(
                    mycomputerpro_page_o.get_page_shot("button_bendicipanC.png"), retry=2, sim_no_reduce=True)
                if find_button_bendicipanC:
                    utils.mouse_drag(pos_button_bendicipanC, (pos_icon_faious[0] + 20, pos_icon_faious[1]))

                find_button_favious_bendicipanC, pos_button_favious_bendicipanC = find_element_by_pic(
                    mycomputerpro_page_o.get_page_shot("button_favious_bendicipanC.png"), retry=2, sim_no_reduce=True)
                if find_button_favious_bendicipanC:
                    log.log_pass("添加书签成功")
            else:
                log.log_error("添加书签失败")
            perform_sleep(3)

        with allure.step("执行工具栏测试操作"):
            if mycomputerpro_page_o.open_patten_c():
                log.log_info("打开本地磁盘C成功")
            else:
                log.log_error("打开本地磁盘C失败")
            perform_sleep(3)

            if utils.click_element_by_pic(mycomputerpro_page_o.get_page_shot("button_newfolder.png"), retry=2,
                                          sim_no_reduce=True):
                utils.mouse_click(mycomputerpro_page_o.position)
                find_icon_newfolder, pos_icon_newfolder = find_element_by_pic(
                    mycomputerpro_page_o.get_page_shot("icon_newfolder.png"), retry=2, sim_no_reduce=True)
                perform_sleep(2)
                if find_icon_newfolder:
                    utils.mouse_click(pos_icon_newfolder)
                    log.log_pass("新建文件夹成功")
                    perform_sleep(2)
                    utils.click_element_by_pic(mycomputerpro_page_o.get_page_shot("button_copy.png"), retry=2,
                                               sim_no_reduce=True)
                    perform_sleep(2)
                    utils.click_element_by_pic(mycomputerpro_page_o.get_page_shot("button_paste.png"), retry=2,
                                               sim_no_reduce=True)
                    perform_sleep(2)
                    utils.mouse_click(mycomputerpro_page_o.position)
                    perform_sleep(2)
                    log.log_pass("复制粘贴文件夹成功")
                    for i in range(1, 3, 1):
                        find_icon_newfolder, pos_icon_newfolder = find_element_by_pic(
                            mycomputerpro_page_o.get_page_shot("icon_newfolder.png"), retry=2, sim_no_reduce=True)
                        perform_sleep(2)
                        if find_icon_newfolder:
                            utils.mouse_click(pos_icon_newfolder)
                            perform_sleep(2)
                            if utils.click_element_by_pic(mycomputerpro_page_o.get_page_shot("button_delete.png"),
                                                          retry=2,
                                                          sim_no_reduce=True):
                                log.log_pass("删除文件夹成功")


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
