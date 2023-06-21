import os
import time
import allure
import pytest
from common.log import log
from office.PageObjects.keniu_web_main_page import KeniuWebMainPage
from office.PageObjects.keniu_web_detail_page import KeniuWebDetailPage
from selenium.webdriver.support import expected_conditions as EC
from office.utils import driver_wait_until,switch_to_new_window,qq_login_operation,back_to_original_window

@allure.epic('可牛办公web站基础用例测试')
@allure.feature('可牛办公web站基础用例测试')
class TestKeniuWeb(object):
    @allure.story('可牛办公web站基础用例测试 预期成功')
    @allure.description("""
        step1: 打开页面正常并完成加载验证
        step2: 页面登录验证
        step3: 办公web站首页列表展示验证
        step4: 验证首页顶部banner展示及点击
        step5: 办公web站下载功能验证
        step6: 验证搜索功能
    """)
    def test_keniu_web(self, chrome_driver_init, get_environment):
        proxy, driver = chrome_driver_init
        env = get_environment
        if env == 'TESTURL':
            os.environ['URL'] = "http://ppt-material-web-keniu-test-fe.aix-test-k8s.iweikan.cn/"
        elif env == 'ONLINEURL':
            os.environ['URL'] = "https://o.keniu.com/"
        elif env == 'SEMTESTURL':
            os.environ['URL'] = "http://ppt-material-web-keniu-semtest-fe.aix-test-k8s.iweikan.cn/"
        elif env == 'SEMONLINE':
            os.environ['URL'] = "https://ppt3.ycywx.com/"


        with allure.step("step1：打开页面正常并完成加载验证"):
            try:
                MainPage = KeniuWebMainPage(driver)
            except:
                log.log_error("打开页面失败")
            # 存储当前界面窗口句柄
            original_window = driver.current_window_handle
            log.log_pass("打开页面成功")

        with allure.step("step2：页面登录验证"):
            MainPage.close_open_ad()
            time.sleep(1)
            MainPage.click_login()
            if not MainPage.is_login_page_exist():
                log.log_error("登录界面不存在")
            log.log_pass("成功打开登录窗口")
            MainPage.click_qq_login()
            driver_wait_until(driver,EC.number_of_windows_to_be(2))
            time.sleep(1)
            switch_to_new_window(driver,original_window)
            driver.maximize_window()
            log.log_info("成功打开QQ登录页面")
            if not qq_login_operation(driver,original_window):
                log.log_error("使用QQ登录失败")
            log.log_pass("使用QQ登录验证成功")

        with allure.step("step3: 办公web站首页列表展示验证"):
            """主要验证在首页中是否会出现加载失败或者展示空白的情况"""
            back_to_original_window(driver,original_window)
            result = MainPage.is_list_error_exist()
            if not (result[0] == 0):
                log.log_error("存在加载失败模板")
            if not result[1]:
                log.log_error("存在模板加载时长超过30s")
            log.log_pass("首页中没有出现模板加载失败/展示空白情况")

        with allure.step("step4:验证首页顶部banner展示及点击"):
            # 返回至页面顶部banner展示位置
            driver.execute_script("scroll(0, 0);")
            result = MainPage.is_banner_error_exist()
            if not (result[0] == 0):
                log.log_error("存在加载失败banner")
            if not result[1]:
                log.log_error("存在banner加载时长超过30s")
            log.log_pass("首页中banner加载及展示正常")
            log.log_info("选取一张banner验证点击跳转")
            MainPage.click_banner()
            if MainPage.is_buy_windows_exist():
                log.log_pass("首页banner点击跳转成功-成功调起支付窗")
                MainPage.close_buy_window()
            else:
                try:
                    driver_wait_until(driver, EC.number_of_windows_to_be(2))
                except:
                    log.log_error("首页banner点击跳转失败")
                log.log_pass("首页banner点击跳转成功")
            back_to_original_window(driver,original_window)


        with allure.step("step5: 办公web站下载功能验证"):
            href = MainPage.click_list_to_detail()
            driver_wait_until(driver,EC.number_of_windows_to_be(2))
            switch_to_new_window(driver,original_window)
            if driver.current_url == href:
                log.log_info("首页点击切换至详情页成功")
            else:
                log.log_error("首页点击切换至详情页失败")
            detail_page = KeniuWebDetailPage(driver)
            # TODO:判断下载结果
            try:
                detail_page.click_download()
            except:
                log.log_error("在详情页中点击下载失败")
            log.log_pass("在详情页中点击下载成功")

        with allure.step("step6:验证搜索功能"):
            back_to_original_window(driver, original_window)
            MainPage.search_input_click()
            try:
                driver_wait_until(driver, EC.number_of_windows_to_be(2))
                switch_to_new_window(driver,original_window)
            except:
                log.log_error("搜索功能使用失败")
            if "error" in driver.current_url:
                log.log_error("落地页是一个错误页面")
            log.log_pass("搜索功能使用成功")


if __name__ == "__main__":
    # pytest.main(["-v", "-s", __file__])
    allure_attach_path = os.path.join("Outputs", "allure")
    pytest.main(["-v", "-s", __file__, '--alluredir=%s' % allure_attach_path])
    os.system("allure serve %s" % allure_attach_path)