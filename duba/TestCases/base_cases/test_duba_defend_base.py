import os

import allure
import pytest
from common import utils
from common.log import log
from common.samba import Samba
from common.utils import perform_sleep
from common.tools.pop_tools import BasePop, get_pop_shot
from duba.PageObjects.setting_page import SettingPage


@allure.epic(f'毒霸防御基础功能测试')
@allure.feature('场景：打开毒霸自保护->下拉防御基础功能测试工具->依次执行测试工具->操作弹出泡泡')
class TestSelfProtect(object):
    @allure.story('1.毒霸防御基础功能测试')
    def test_self_protect(self):
        allure.dynamic.description(
            '\t1.打开毒霸自保护\n'
            '\t2.下拉防御基础功能测试工具\n'
            '\t3.依次执行测试工具\n'
            '\t4.双后缀名拦截样本测试\n'
            '\t5.捆绑软件安装拦截样本测试\n'
            '\t6.服务与驱动注册运行拦截样本测试\n'
            '\t7.修改密码拦截样本测试\n'
            '\t8.注册表写入拦截样本测试\n'
            '\t10.创建用户拦截样本测试\n'
            '\t11.创建注册表拦截样本测试\n'
            '\t12.防黑墙恶意网址拦截测试\n'
            '\t13.防黑墙挖矿程序访问拦截测试\n'
            # '\t14.防黑墙后台程序下载文件(wscript)拦截测试\n'
            # '\t15.防黑墙后台程序下载文件(cscript)拦截测试\n'
        )
        allure.dynamic.title('毒霸防御基础功能测试')

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
            demo_path = os.path.join("autotest", "dubadefend")
            samba_o.download_dir("TcSpace", demo_path, defend_tool_path)
            # 双后缀名拦截样本
            tool_path_1 = os.path.join(defend_tool_path, "1.jpg.exe")
            # 捆绑软件安装拦截样本
            tool_path_2 = os.path.join(defend_tool_path, "2.exe")
            # 水银黑拦截样本
            tool_path_3 = os.path.join(defend_tool_path, "3.exe")
            # 服务与驱动注册运行拦截样本
            tool_path_4 = os.path.join(defend_tool_path, "4.exe")
            tool_path_4_2 = os.path.join(defend_tool_path, "4.sys")
            # 修改密码拦截样本
            tool_path_5 = os.path.join(defend_tool_path, "5.bat")
            # 注册表写入拦截样本
            tool_path_6 = os.path.join(defend_tool_path, "6.exe")
            # 放黑墙拦截样本
            # tool_path_7 = os.path.join(defend_tool_path, "7.bat")
            # 创建用户拦截样本
            tool_path_8 = os.path.join(defend_tool_path, "8.bat")
            # 创建注册表拦截样本
            tool_path_9 = os.path.join(defend_tool_path, "writerunreg.exe")
            # # 防黑墙恶意网址拦截测试
            # tool_path_10 = os.path.join(defend_tool_path, "http1.lnk")
            # # 防黑墙挖矿程序访问拦截测试
            # tool_path_11 = os.path.join(defend_tool_path, "http2.lnk")
            # 防黑墙后台程序下载文件拦截测试
            tool_path_12 = os.path.join(defend_tool_path, "8000.vbs")
            # 防黑墙后台程序下载文件(cscript)拦截测试
            tool_path_13 = os.path.join(defend_tool_path, "anti_cscript.bat")
            # 防黑墙恶意网址和挖矿程序访问拦截工具
            tool_path_14 = os.path.join(defend_tool_path, "http.exe")

            if os.path.exists(tool_path_1) and os.path.exists(tool_path_2) and os.path.exists(tool_path_3) \
                    and os.path.exists(tool_path_4) and os.path.exists(tool_path_4_2) and os.path.exists(tool_path_5) \
                    and os.path.exists(tool_path_6) and os.path.exists(tool_path_8) and os.path.exists(tool_path_9) \
                    and os.path.exists(tool_path_14) and os.path.exists(tool_path_12) \
                    and os.path.exists(tool_path_13):
                log.log_pass("下拉所有毒霸防御测试工具成功", attach=False)
                utils.perform_sleep(5)
            else:
                log.log_error("下拉毒霸防御测试工具失败", attach=False)

        with allure.step("step3：双后缀名拦截样本测试"):
            utils.process_start(tool_path_1, async_start=True)
            utils.perform_sleep(5)
            defendpop = BasePop()
            if defendpop.pop_init:
                log.log_pass("双后缀名拦截泡泡正常")
                defendpop.click_defend_stop()

        with allure.step("step4：捆绑软件安装拦截样本测试"):
            utils.process_start(tool_path_2, async_start=True)
            utils.perform_sleep(5)
            defendpop = BasePop()
            if defendpop.pop_init:
                log.log_pass("捆绑软件安装拦截泡泡正常")
                defendpop.click_defend_stop()

        with allure.step("step5：水银黑拦截样本测试"):
            utils.process_start(tool_path_3, async_start=True)
            utils.perform_sleep(5)
            defendpop = BasePop()
            if defendpop.pop_init:
                log.log_pass("水银黑拦截泡泡正常")
                defendpop.click_defend_stop()

        with allure.step("step6：服务与驱动注册运行拦截样本测试"):
            utils.process_start(tool_path_4, param=tool_path_4_2 + " test", async_start=True)
            utils.perform_sleep(5)
            defendpop = BasePop()
            if defendpop.pop_init:
                log.log_pass("服务与驱动注册运行拦截泡泡正常")
                defendpop.click_defend_stop()

        with allure.step("step7：修改密码拦截样本测试"):
            utils.process_start(tool_path_5, async_start=True)
            utils.perform_sleep(5)
            defendpop = BasePop()
            if defendpop.pop_init:
                log.log_pass("修改密码拦截泡泡正常")
                defendpop.click_defend_stop()

        with allure.step("step8：注册表写入拦截样本测试"):
            utils.process_start(tool_path_6, async_start=True)
            utils.perform_sleep(5)
            defendpop = BasePop()
            if defendpop.pop_init:
                log.log_pass("注册表写入拦截泡泡正常")
                defendpop.click_defend_stop()

        # with allure.step("step9：防黑墙拦截样本测试"):
        #     utils.process_start(tool_path_7, async_start=True)
        #     utils.perform_sleep(5)
        #     defendpop = BasePop()
        #     if defendpop.pop_init:
        #         log.log_pass("防黑墙拦截泡泡正常")
        #         defendpop.click_defend_anti_stop()
        #     # 结束掉脚本调起的ftp进程
        #     utils.kill_process_by_name("ftp.exe")

        with allure.step("step10：创建用户拦截样本测试"):
            utils.process_start(tool_path_8, async_start=True)
            utils.perform_sleep(5)
            defendpop = BasePop()
            if defendpop.pop_init:
                log.log_pass("创建用户拦截泡泡正常")
                defendpop.click_defend_stop()
        with allure.step("step11：创建注册表拦截样本测试"):
            utils.process_start(tool_path_9, async_start=True)
            utils.perform_sleep(5)
            defendpop = BasePop()
            if defendpop.pop_init:
                log.log_pass("创建注册表拦截泡泡正常")
                b_antireg_pop, b_antireg_position = utils.find_element_by_pic(get_pop_shot("antihack_setuser.png"))
                utils.perform_sleep(10)
                if b_antireg_pop:
                    log.log_pass("注册表拦截泡泡策略----正常")
                else:
                    log.log_error("注册表拦截泡泡未找到！！！！")
                defendpop.click_defend_stop()
        with allure.step("step12：防黑墙恶意网址拦截测试"):
            utils.process_start(tool_path_14, param=r'http://iiaonline.in/111.jpg', async_start=True)
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
        with allure.step("step13：防黑墙挖矿程序访问拦截测试"):
            utils.process_start(tool_path_14, param=r'http://cs.strongapt.ml/powershell.jpg', async_start=True)
            utils.perform_sleep(5)
            defendpop = BasePop()
            if defendpop.pop_init:
                log.log_pass("创建防黑墙挖矿程序访问拦截泡泡正常")
                b_antireg_pop, b_antireg_position = utils.find_element_by_pic(get_pop_shot("antihack_mining.png"))
                utils.perform_sleep(10)
                if b_antireg_pop:
                    log.log_pass("防黑墙挖矿程序访问拦截泡泡策略----正常")
                else:
                    log.log_error("防黑墙挖矿程序访问拦截泡泡未找到！！！！")
                defendpop.click_defend_stop()
        # with allure.step("step14：防黑墙后台程序下载文件(wscript)测试"):
        #     utils.process_start(tool_path_12, async_start=True)
        #     utils.perform_sleep(5)
        #     defendpop = BasePop()
        #     if defendpop.pop_init:
        #         log.log_pass("创建防黑墙后台程序下载文件(wscript)拦截泡泡正常")
        #         b_antireg_pop, b_antireg_position = utils.find_element_by_pic(get_pop_shot("antihack_wscript_intercept.png"))
        #         utils.perform_sleep(10)
        #         if b_antireg_pop:
        #             log.log_pass("防黑墙后台程序下载文件(wscript)拦截泡泡策略----正常")
        #         else:
        #             log.log_error("防黑墙后台程序下载文件(wscript)拦截泡泡未找到！！！！")
        #         defendpop.click_defend_stop()
        #     utils.kill_process_by_name("wscript.exe")
        # with allure.step("step15：防黑墙后台程序下载文件(cscript)测试"):
        #     utils.process_start(tool_path_13, async_start=True)
        #     utils.perform_sleep(5)
        #     defendpop = BasePop()
        #     if defendpop.pop_init:
        #         log.log_pass("创建防黑墙后台程序下载文件(cscript)拦截泡泡正常")
        #         b_antireg_pop, b_antireg_position = utils.find_element_by_pic(get_pop_shot("antihack_cscript_intercept.png"))
        #         utils.perform_sleep(10)
        #         if b_antireg_pop:
        #             log.log_pass("防黑墙后台程序下载文件(cscript)拦截泡泡策略----正常")
        #         else:
        #             log.log_error("防黑墙后台程序下载文件(cscript)拦截泡泡未找到！！！！")
        #         defendpop.click_defend_stop()
        #     utils.kill_process_by_name("cscript.exe")
if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
