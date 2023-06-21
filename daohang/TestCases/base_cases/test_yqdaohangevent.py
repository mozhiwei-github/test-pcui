import os
import time
import allure
import pytest
import random
from furl import furl
from common.log import log
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from daohang.utils import switch_to_new_window,driver_step,driver_wait_until,driver_get_reload, driver_click
from selenium.webdriver import ActionChains
from daohang.contants import *


def analysis(result,snode):
    urllist = []
    responselist = []
    statuslist = []
    snodenum='snode='+str(snode)
    for entry in result['log']['entries']:
        url = entry['request']['url']   #str
        if snodenum in url:
            urllist.append(url)
            response = entry['response']
            responselist.append(response)
            status = response.get('status')
            statuslist.append(status)
    return urllist,responselist,statuslist


def judge(snode, tp, w, text, result, word):
    url_list, response_list, status_list = analysis(result, snode)
    snode_str = 'snode=' + str(snode)
    if tp == 'home':
        tpstr = 'index'
    else:
        tpstr = tp

    if (len(url_list) != 1): # 不只上报一次
        if (len(url_list) != 0):
            log.log_info(f"{word}{snode_str}---该埋点上报多次")
            return False
        # 该埋点未上报
        log.log_info(f"{word}{snode_str}---该埋点未上报")
        return False
    if status_list[0] != 200:
        log.log_info(f"{word}{snode_str}---该埋点上报状态异常,状态为{status_list[0]}")
        return False
    f = furl(url_list[0])
    if tpstr != f.args['tp']:
        log.log_info(f"{word}{snode_str}---tp上报检验错误")
        log.log_info(f"期望值为{tpstr},实际值为{f.args['tp']}")
        return False
    if w != f.args['w']:
        log.log_info(f"{word}{snode_str}---w上报检验错误")
        log.log_info(f"期望值为{w},实际值为{f.args['w']}")
        return False
    if (text.replace(" ", "") != f.args['md5'].replace(" ", "")) and ("statTime" not in f.args['md5'].replace(" ", "")):
        log.log_info(f"{word}{snode_str}---md5上报检验错误")
        log.log_info(f"期望值为{text},实际值为{f.args['md5']}")
        return False
    log.log_info(f"{word}{snode_str}---该埋点参数校验通过")
    return True

@allure.epic(f'元气导航埋点案例测试')
@allure.feature('测试场景：元气导航基础埋点上报')
class TestSVDaoHangEvent(object):
    @allure.story('用例：元气导航基础埋点上报 预期成功')
    @allure.description("""
        step1：元气导航页面展示上报
        step2：元气搜索框选择下拉框内容上报
        step3：元气搜索框输入内容点击搜索button上报
        step4：元气点击切换皮肤上报
        step5：元气皮肤库切换皮肤点击上报
    """)

    def test_eventtest(self,chrome_driver_init,get_env_and_channel):
        proxy,driver = chrome_driver_init
        # 浏览器窗口最大化
        driver.maximize_window()
        # 设置等待函数等待时间
        wait = WebDriverWait(driver,10)
        # 简版导航首页
        env,channel = get_env_and_channel
        base_url = env + channel
        if env in["https://www.duba.com","https://www.newduba.cn"]:
            proxy_trace_url = f"{env}/proxy/trace"
        else:
            proxy_trace_url = "http://dh2.tj.ijinshan.com/__dh.gif"
        allure.dynamic.title(f"元气导航基础埋点上报 渠道：{base_url}")

        tp = channel[1:].split('.')[0]

        # 场景一：简版导航页面展示上报
        with driver_step("step1: 元气导航页面展示上报",driver):
            #driver.get(base_url)
            driver_get_reload(base_url)
            proxy.new_har(proxy_trace_url)
            # 重新刷新一次页面使得页面数据获取完全（部分接口数据首次请求无数据返回）
            # keyboardInputByCode('F5')
            driver.refresh()
            log.log_info("页面刷新成功")
            # 存储原始的窗口ID
            original_window = driver.current_window_handle
            assert len(driver.window_handles) == 1, "窗口个数检查失败"
            # 等待页面加载完毕
            driver_wait_until(driver,EC.title_is("元气主页-极简炫酷的上网主页"))
            log.log_info("导航页面打开成功", driver=driver)
            # 查找上报请求
            result = proxy.har
            text = ''
            judge_result = judge(snode_info.page_show.value, tp, w_info.null_value.value, text, result, yq_scene_info.step1.value)
            if judge_result:
                log.log_pass("元气导航页面展示上报成功", driver=driver)
            else:
                log.log_error("元气导航页面展示上报失败", driver=driver)

        # 场景二：元气搜索框选择下拉框内容上报
        with driver_step('step2:元气搜索框选择下拉框内容上报',driver,original_window):
            proxy.new_har(proxy_trace_url)
            # 点击输入框，清空其内容
            driver_click(driver, namexpath="word")
            driver.find_element_by_name("word").clear()
            log.log_info(f"清空搜索输入框内容", driver=driver)
            # 点击搜索下拉框内容
            xpath = '//*[@class="m_search_drop_down"]/span/span[@class="text g_oh"]'
            item_list = driver.find_elements_by_xpath(xpath)
            assert item_list, "获取元气导航搜索下拉框列表数据失败"
            item = random.choice(item_list)
            text = item.text
            driver_click(driver, element=item)
            log.log_info(f"点击搜索框下拉列表关键词：{text}")
            # 等待搜索结果标签页打开
            driver_wait_until(driver,EC.number_of_windows_to_be(2))
            switch_to_new_window(driver, original_window)
            log.log_info(f"打开{text}搜索结果标签页成功", driver=driver)
            result = proxy.har
            judge_result = judge(snode_info.search_click.value, tp, w_info.searchbox.value, text, result, yq_scene_info.step2.value)
            if judge_result:
                log.log_pass("元气搜索框选择下拉框内容上报成功", driver=driver)
            else:
                log.log_error("元气搜索框选择下拉框内容上报失败", need_assert=False, driver=driver)

        # 场景三：元气搜索框输入内容点击搜索button上报
        with driver_step("step3:元气搜索框输入内容点击搜索button上报", driver, original_window):
            proxy.new_har(proxy_trace_url)
            # 点击输入框，清空其内容
            driver_click(driver, namexpath="word")
            driver.find_element_by_name("word").clear()
            # 输入搜索内容
            text = "EventTest"
            driver.find_element_by_name("word").send_keys(text)
            log.log_info(f"输入搜索内容：{text}", driver=driver)
            driver_click(driver, classxpath="search_btn")
            log.log_info("点击搜索按钮")
            # 等待搜索结果标签页打开
            driver_wait_until(driver, EC.number_of_windows_to_be(2))
            # 将窗口句柄切换到新标签页
            switch_to_new_window(driver, original_window)
            log.log_info(f"打开{text} 搜索结果标签页成功", driver=driver)
            result = proxy.har
            judge_result = judge(snode_info.search_click.value, tp, w_info.num_1.value, text, result, yq_scene_info.step3.value)
            time.sleep(2)
            if judge_result:
                log.log_pass("元气搜索框输入内容点击搜索button上报成功", driver=driver)
            else:
                log.log_error("元气搜索框输入内容点击搜索button上报失败", driver=driver)

        # 场景四：元气点击切换皮肤上报
        with driver_step('step4: 元气点击切换皮肤上报',driver,original_window):
            proxy.new_har(proxy_trace_url)
            xpath = '//*[@w="allskin"]/span'
            text = driver.find_element_by_xpath(xpath).text
            driver_click(driver, xpath=xpath)
            log.log_info(f"元气切换皮肤按钮点击成功")
            skin_window_xpath = '//*[@class="modal_skin"]'
            assert driver.find_element_by_xpath(skin_window_xpath),"元气皮肤库窗口打开失败"
            log.log_info(f'打开皮肤库成功')
            # 需要增加一个等待时间供接口请求上报完成
            time.sleep(1)
            result = proxy.har
            judge_result = judge(snode_info.page_click.value, tp, w_info.allskin.value, text, result, yq_scene_info.step4.value)
            if judge_result:
                log.log_pass("元气点击切换皮肤上报成功",driver=driver)
            else:
                log.log_error("元气点击切换皮肤上报失败",driver=driver)


        # 场景五：元气皮肤库切换皮肤点击上报
        with driver_step('step5: 元气皮肤库切换皮肤点击上报',driver,original_window):
            skin_window_xpath = '//*[@class="modal_skin"]'
            if not driver.find_element_by_xpath(skin_window_xpath):

                button_xpath = '//*[@w="allskin"]/span'
                driver_click(driver, xpath=button_xpath)
                log.log_info(f"元气切换皮肤按钮点击成功")
                assert driver.find_element_by_xpath(skin_window_xpath),"元气皮肤库窗口打开失败"
                log.log_info(f'打开皮肤库成功')
            else:
                log.log_info(f'皮肤库窗口已打开')
            # 选择皮肤
            proxy.new_har(proxy_trace_url)
            xpath = '//*[@class="modal_skin"]/div[@class="skin_list"]//div[@class="skin_item_wrap g_fl"]/div'
            item_list = driver.find_elements_by_xpath(xpath)
            # 由于一个页面只会展示9个皮肤，需要滚动才会展示更多皮肤，故需要滚动至皮肤处点击
            item = random.choice(item_list)
            ActionChains(driver).move_to_element(item).perform()
            time.sleep(1)
            text = item.get_attribute("md5")
            driver_click(driver, element=item)
            log.log_info(f'元气皮肤库切换皮肤点击皮肤: {text}')
            time.sleep(1)
            result = proxy.har
            judge_result = judge(snode_info.page_click.value, tp, w_info.allskin.value, text, result, yq_scene_info.step5.value)
            if judge_result:
                log.log_pass("元气皮肤库切换皮肤点击上报成功",driver=driver)
            else:
                log.log_error("元气皮肤库切换皮肤点击上报失败",driver=driver)

if __name__ == '__main__':
    # pytest.main(["-v", "-s", __file__])
    allure_attach_path = os.path.join("Outputs", "allure")
    pytest.main(["-v", "-s", __file__, '--alluredir=%s' % allure_attach_path])
    os.system("allure serve %s" % allure_attach_path)