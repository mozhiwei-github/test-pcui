import os
import shutil

import allure
import pytest
from common import utils
from common.log import log
from common.samba import Samba
from common.utils import perform_sleep
from common.tools.pop_tools import BasePop, get_pop_shot
from duba.PageObjects.setting_page import SettingPage


@allure.epic(f'毒霸防御网络驱动功能测试')
@allure.feature('场景：打开毒霸自保护->下拉网络驱动功能测试工具->依次执行测试工具->操作弹出泡泡')
class TestSelfProtect(object):
    @allure.story('1.毒霸网络驱动功能测试')
    def test_self_protect(self):
        allure.dynamic.description(
            '\t1.打开毒霸自保护\n'
            '\t2.下拉网络驱动功能测试工具\n'
            '\t3.依次执行测试工具\n'
            '\t4.防黑墙恶意网址拦截测试\n'
            '\t5.防黑墙后台程序下载文件(wscript)拦截测试\n'
            '\t6.防黑墙后台程序下载文件(cscript)拦截测试\n'
        )
        allure.dynamic.title('毒霸网络驱动功能测试')

        with allure.step("step1：打开毒霸自保护"):
            setting_page_o = SettingPage()
            # 先关闭毒霸自保护，删除自动拦截不弹泡泡的键值
            if setting_page_o.self_protecting_close():
                if utils.query_reg_value(None, r"SOFTWARE\WOW6432Node\kingsoft\antivirus", "DenyAuto"):
                    if utils.remove_reg_value(None, r"SOFTWARE\WOW6432Node\kingsoft\antivirus", "DenyAuto"):
                        log.log_pass("删除自动拦截不弹泡泡的键值", attach=False)
            perform_sleep(1)
            if setting_page_o.self_protecting_open():
                log.log_pass("打开毒霸自保护成功", attach=False)
            perform_sleep(1)

        with allure.step("step2：下拉防御基础功能测试工具/样本"):
            defend_tool_path = os.path.join(os.getcwd(), "defendtool")
            samba_o = Samba("10.12.36.203", "duba", "duba123")
            demo_path = os.path.join("autotest", "defendnet")
            samba_o.download_dir("TcSpace", demo_path, defend_tool_path)
            # 防黑墙恶意网址拦截测试
            tool_path_1 = os.path.join(defend_tool_path, "http.exe")
            # 防黑墙URL过滤拦截测试
            tool_path_2 = os.path.join(defend_tool_path, "http_360.exe")
            # 防黑墙后台程序下载文件拦截测试
            tool_path_3 = os.path.join(defend_tool_path, "8000.vbs")
            # 防黑墙后台程序下载文件(cscript)拦截测试
            tool_path_4 = os.path.join(defend_tool_path, "anti_cscript.bat")

            if os.path.exists(tool_path_1) and os.path.exists(tool_path_2) and os.path.exists(tool_path_3) \
                    and os.path.exists(tool_path_4):
                log.log_pass("下拉所有毒霸防御测试工具成功", attach=False)
                utils.perform_sleep(5)
            else:
                log.log_error("下拉毒霸防御测试工具失败", attach=False)

        with allure.step("step3：防黑墙恶意网址拦截测试"):
            utils.process_start(tool_path_1, param=r'http://iiaonline.in/111.jpg', async_start=True)
            utils.perform_sleep(5)
            defendpop = BasePop()
            if defendpop.pop_init:
                log.log_pass("创建防黑墙恶意网址拦截泡泡正常")
                b_antireg_pop, b_antireg_position = utils.find_element_by_pic(get_pop_shot("antihack_dangerurl.png"))
                utils.perform_sleep(10)
                if b_antireg_pop:
                    log.log_pass("恶意网址拦截泡泡策略----正常")
                else:
                    log.log_error("恶意网址拦截泡泡未找到！！！！")
                defendpop.click_defend_stop()
        with allure.step("step4：防黑墙URL过滤拦截测试"):
            setting_page_o = SettingPage()
            # 先关闭毒霸自保护，删除自动拦截不弹泡泡的键值
            if setting_page_o.self_protecting_close():
                if utils.query_reg_value(None, r"SOFTWARE\WOW6432Node\kingsoft\antivirus", "DenyAuto"):
                    if utils.remove_reg_value(None, r"SOFTWARE\WOW6432Node\kingsoft\antivirus", "DenyAuto"):
                        log.log_pass("删除自动拦截不弹泡泡的键值", attach=False)
                # 结束毒霸服务和托盘，替换测试文件fnsign.dat到data目录
                if utils.is_process_exists("kxetray.exe"):
                    utils.kill_process_by_name("kxetray.exe")
                    perform_sleep(2)
                if utils.is_process_exists("kxescore.exe"):
                    utils.kill_process_by_name("kxescore.exe")
                    perform_sleep(2)
                Dubainstallpath = utils.query_reg_value(None, r"SOFTWARE\WOW6432Node\kingsoft\antivirus", "ProgramPath")
                Dubadata = os.path.join(Dubainstallpath,'data')
                tool_path_fnsign = os.path.join(defend_tool_path, "fnsign.dat")
                try:
                    shutil.copyfile(tool_path_fnsign,Dubadata)
                except IOError as e:
                    exit(1)
                Desktoppath = os.path.join(os.path.expanduser('~'),'Desktop')
                shutil.copyfile(tool_path_3, Desktoppath)
                shutil.copyfile(tool_path_4, Desktoppath)
                utils.process_start(os.path.join(Dubainstallpath,'kxetray.exe'))
                perform_sleep(30)
            if setting_page_o.self_protecting_open():
                log.log_pass("打开毒霸自保护成功", attach=False)
            perform_sleep(1)
            utils.process_start(tool_path_2, param=r'http://news.china.com.cn/2021-10/25/content_77829524.htm', async_start=True)
            utils.perform_sleep(5)
            defendpop = BasePop()
            if defendpop.pop_init:
                log.log_pass("创建防黑墙URL过滤拦截泡泡正常")
                b_antireg_pop, b_antireg_position = utils.find_element_by_pic(get_pop_shot("antihackuploadurl.png"))
                utils.perform_sleep(10)
                if b_antireg_pop:
                    log.log_pass("URL过滤拦截泡泡策略----正常")
                else:
                    log.log_error("URL过滤拦截泡泡未找到！！！！")
                defendpop.click_defend_stop()
        with allure.step("step5：防黑墙后台程序下载文件(wscript)测试"):
            utils.process_start(tool_path_3, async_start=True)
            utils.perform_sleep(5)
            defendpop = BasePop()
            if defendpop.pop_init:
                log.log_pass("创建防黑墙后台程序下载文件(wscript)拦截泡泡正常")
                b_antireg_pop, b_antireg_position = utils.find_element_by_pic(get_pop_shot("antihack_wscript_intercept.png"))
                utils.perform_sleep(10)
                if b_antireg_pop:
                    log.log_pass("防黑墙后台程序下载文件(wscript)拦截泡泡策略----正常")
                else:
                    log.log_error("防黑墙后台程序下载文件(wscript)拦截泡泡未找到！！！！")
                defendpop.click_defend_stop()
            utils.kill_process_by_name("wscript.exe")
        with allure.step("step6：防黑墙后台程序下载文件(cscript)测试"):
            utils.process_start(os.path.join(Desktoppath,'anti_cscript.bat'), async_start=True)
            utils.perform_sleep(5)
            defendpop = BasePop()
            if defendpop.pop_init:
                log.log_pass("创建防黑墙后台程序下载文件(cscript)拦截泡泡正常")
                b_antireg_pop, b_antireg_position = utils.find_element_by_pic(get_pop_shot("antihack_cscript_intercept.png"))
                utils.perform_sleep(10)
                if b_antireg_pop:
                    log.log_pass("防黑墙后台程序下载文件(cscript)拦截泡泡策略----正常")
                else:
                    log.log_error("防黑墙后台程序下载文件(cscript)拦截泡泡未找到！！！！")
                defendpop.click_defend_stop()
            utils.kill_process_by_name("cscript.exe")
if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
