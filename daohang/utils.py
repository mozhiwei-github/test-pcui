import time
import allure
import pytest
from common.log import log
from contextlib import contextmanager
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException,NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait

"""导航项目功能函数"""


def switch_to_new_window(driver, original_window):
    """
    切换到新标签页窗口
    @param driver: selenium浏览器driver
    @param original_window: 原始窗口的ID
    @return:
    """
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break


def back_to_original_window(driver, original_window, assert_handles=True, window_count=1, scroll_top=True):
    """
    关闭新标签页，切换回原始标签页
    @param driver: selenium浏览器driver
    @param original_window: 原始窗口的ID
    @param assert_handles: 进行窗口数量断言检查
    @param window_count: 窗口数量
    @param scroll_top: 是否滚动到页面顶部
    @return:
    """
    if len(driver.window_handles) > 1:
        # 当前窗口句柄为原始窗口时，需要先切换到新标签页窗口
        if driver.current_window_handle == original_window:
            switch_to_new_window(driver, original_window)
        # 关闭新标签页
        driver.close()

    # 切换回原始标签页
    driver.switch_to.window(original_window)

    # 是否进行窗口数量断言检查
    if assert_handles:
        assert len(driver.window_handles) == window_count, "窗口数量检查失败"

    # 是否滚动到页面顶部
    if scroll_top:
        driver.execute_script("window.scrollTo(0, 0)")

    time.sleep(1)


@contextmanager
def driver_step(step_name, driver, original_window=None, assume=True, clear_cookies=True, back_to_original=True):
    """
    自定义selenium step
    @param step_name: 步骤名
    @param driver: selenium浏览器driver
    @param original_window: 原始窗口句柄ID
    @param assume: 断言错误后是否继续执行其他用例
    @param clear_cookies: 执行用例前是否清除cookies
    @param back_to_original: 测试结束后是否切换回原始窗口
    @return:
    """
    try:
        def main():
            if clear_cookies:
                driver.delete_all_cookies()

        with allure.step(step_name):
            # 即使上报断言失败也继续执行后续测试流程
            if assume:
                with pytest.assume:
                    yield main()
            else:
                yield main()
    finally:
        if back_to_original and original_window:
            # 切换为原始窗口
            back_to_original_window(driver, original_window)


# 存储全局 driver WebDriverWait 实例
driver_wait_dict = {}


def driver_wait_until(driver, method, message='', wait_seconds=10, retries=1):
    """
    自定义 driver wait.util 函数
    @param driver: selenium浏览器driver
    @param method: wait.utils method
    @param message: wait.utils message
    @param wait_seconds: 等待超时时间，默认等待10秒
    @param retries: 重试次数，默认重试1次
    @return:
    """
    # 获取 WebDriverWait 实例
    global driver_wait_dict
    wait = driver_wait_dict.get(wait_seconds, None)
    if not wait:  # 没有相应 WebDriverWait 实例时创建
        wait = WebDriverWait(driver, wait_seconds)
        driver_wait_dict[wait_seconds] = wait

    # 执行 retries + 1 次等待
    for i in range(retries+1):
        try:
            wait.until(method, message)
            break
        except TimeoutException as e:
            if i >= retries:
                assert not e, log.log_error(f"等待超时且超过最大重试次数，{e}", need_assert=False, driver=driver)
            else:
                log.log_info(f"{message}等待超时，进行第{i+1}次重试")
                continue

def driver_get_reload(driver, base_url, retries=1):
    """
    自定义driver_get_reload 函数
    """
    for i in range(retries+1):
        try:
            driver.get(base_url)
        except TimeoutException as e:
            if i >= retries:
                assert not e, log.log_error(f"等待超时且超过最大重试次数，{e}", need_assert=False, driver=driver)
            else:
                log.log_info(f"加载页面等待超时，进行第{i + 1}次重试")
                continue

def driver_click(driver, element=None, idxpath="", xpath="", classxpath="",namexpath=""):
    """
    自定义driver_click 函数
    """
    try:
        if idxpath != "":
            driver.find_element_by_id(idxpath).click()
        elif xpath != "":
            driver.find_element_by_xpath(xpath).click()
        elif namexpath != "":
            driver.find_element_by_name(namexpath).click()
        elif element != None:
            element.click()
        else:
            driver.find_element_by_class_name(classxpath).click()

    except ElementClickInterceptedException as e:
        assert not e, log.log_error(f"点击{xpath}元素失败", need_assert=False, driver=driver)
    except NoSuchElementException as e:
        assert not e, log.log_error(f"找不到该点击元素", need_assert=False, driver=driver)
    except ElementClickInterceptedException as e:
        assert not e, log.log_error(f"点击失败，元素未能正常展示/被遮挡", need_assert=False, driver=driver)
    except Exception as e:
        assert not e, log.log_error(f"点击{xpath}元素失败,失败原因{e}", need_assert=False, driver=driver)




