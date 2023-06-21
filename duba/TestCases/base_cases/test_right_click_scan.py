#!/usr/bin/evn python
# --coding = 'utf-8' --
import os.path

import allure
import pytest

from common import utils
from common.log import log
from duba.PageObjects.main_page import main_page


@allure.epic(f"毒霸右键扫描测试案例")
@allure.feature("场景：打开资源管理器->桌面图标右键->点击毒霸扫描")
class TestRightClickScan(object):
    @allure.story('右键毒霸快捷图标扫描')
    def test_desktop_right_click_scan(self):
        allure.dynamic.description(
            '\t1.打开资源管理器,桌面图标右键\n'
            '\t2.点击毒霸扫描\n'
            '\t3.检查kscan进行运行\n'
            '\t4.检查毒霸扫描界面运行\n'
            '\t5.正常关闭毒霸界面\n'
        )
        ican_path = os.path.join(os.getcwd(), "duba", "PageShot", "duba_scan")
        desktop_pic = os.path.join(ican_path, "icon_desktop.png")
        tab_duba_scan = os.path.join(ican_path, "tab_duba_scan.png")
        right_click_icon = os.path.join(ican_path, "icon_right_click_scan.png")
        button_cancel_scan = os.path.join(ican_path, "button_cancel_scan.png")
        tab_duba_scan_finish = os.path.join(ican_path, "tab_duba_scan_finish.png")
        tab_duba_scan_finish_bug = os.path.join(ican_path, "tab_duba_scan_finish_bug.png")
        button_back = os.path.join(ican_path, "button_back.png")
        button_give_up_handle = os.path.join(ican_path, "button_give_up_handle.png")

        with allure.step("step1：打开资源管理器,桌面图标右键"):
            log.log_info("打开资源管理器")
            utils.keyboardInput2Key(utils.VK_CODE.get("left_win"), utils.VK_CODE.get("e"))
            find_res, find_pos = utils.find_element_by_pic(desktop_pic)
            if find_res:
                log.log_info("右键点击桌面图标")
                utils.mouse_right_click(find_pos[0], find_pos[1])

        with allure.step("step2：点击毒霸扫描校验正确性"):
            find_res, find_pos = utils.find_element_by_pic(right_click_icon)
            if find_res:
                log.log_info("点击毒霸扫描")
                utils.mouse_click(find_pos)
                utils.perform_sleep(2)
            else:
                log.log_error("没有右键扫描选项")
            # 检查kscan.exe进程是否存在
            if not utils.is_process_exists("kscan.exe"):
                log.log_error("kscan.exe启动失败")
            else:
                log.log_info("检查kscan.exe进程存在")

            if not utils.find_element_by_pic(tab_duba_scan, sim_no_reduce=True)[0]:
                log.log_error("扫描界面启动失败")
            else:
                log.log_info("检查扫描界面启动正常")

            for i in range(50):
                find_res_cancel_scan, find_pos_cancel_scan = utils.find_element_by_pic(button_cancel_scan, retry=2,
                                                                                       sim_no_reduce=True)
                if find_res_cancel_scan:
                    log.log_info("正在扫描中")
                else:
                    break
            if utils.find_element_by_pics([tab_duba_scan_finish, tab_duba_scan_finish_bug], sim_no_reduce=True)[0]:
                log.log_info("扫描结束")
                utils.click_element_by_pic(button_back)
                utils.click_element_by_pic(button_give_up_handle, retry=2)

            main_page_o = main_page(do_pre_open=False)
            main_page_o.page_del()
            # 关闭资源管理器
            log.log_info("关闭资源管理器")
            utils.keyboardInput2Key(utils.VK_CODE.get("alt"), utils.VK_CODE.get("F4"))


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
