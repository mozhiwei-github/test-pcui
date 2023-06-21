import os
import time
import allure
import pytest
import random
from furl import furl
from selenium.webdriver.common.keys import Keys
from common.log import log
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from daohang.utils import switch_to_new_window, driver_get_reload, driver_step, driver_wait_until, driver_click
from daohang.conftest import get_env_and_channel
# from selenium import webdriver
# from browsermobproxy import Server
# from selenium.webdriver.chrome.options import Options

from daohang.contants import *


def analysis(result, snode):
    urllist = []
    responselist = []
    statuslist = []
    snodenum = 'snode=' + str(snode)
    for entry in result['log']['entries']:
        url = entry['request']['url']  # str
        if snodenum in url:
            urllist.append(url)
            response = entry['response']
            responselist.append(response)
            status = response.get('status')
            statuslist.append(status)
    return urllist, responselist, statuslist

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


@allure.epic(f'办公导航基础埋点案例测试')
@allure.feature('测试场景：办公导航基础埋点上报')
class TestBanGongDaoHangEvent(object):
    @allure.story('用例：办公导航基础埋点上报 预期成功')
    @allure.description("""
        step1: 办公导航页面展示上报
        step2: 办公搜索框联想词点击上报
        step3:办公搜索框选择下拉框内容点击搜索上报
        step4:办公搜索框输入内容点击搜索上报
        step5:办公名站点击上报
        step6:办公最近使用模块tab点击上报
        step7:办公酷站点击上报
        step8:办公今日热搜点击上报
        step9:办公今日热搜卡片点击上报
        step10:办公电梯栏点击上报
        step11:办公电梯栏点击设置按钮上报
        step12:视频音乐点击左侧大图卡片上报
        step13:视频音乐点击右侧卡片上报
        step14:购物出行点击左侧大图卡片上报
        step15:视频音乐点击右侧卡片上报
        step16:办公搜索框点击搜索框下方内容上报
    """)

    def test_eventtest(self,chrome_driver_init,get_env_and_channel):
        proxy, driver = chrome_driver_init
        #浏览器窗口最大化
        driver.maximize_window()
        #设置等待函数等待时间
        wait = WebDriverWait(driver, 10)
        #办公导航首页
        env,channel = get_env_and_channel
        base_url = env + channel
        if env in["https://www.duba.com","https://www.newduba.cn"]:
            proxy_trace_url = f"{env}/proxy/trace"
        else:
            proxy_trace_url = "http://dh2.tj.ijinshan.com/__dh.gif"
        allure.dynamic.title(f"办公导航基础埋点上报 渠道：{base_url}")

        tp = channel[1:].split('.')[0]

        # 场景一：办公导航页面展示上报snode=100上报---pass
        with driver_step("step1: 办公导航页面展示上报",driver):
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
            driver_wait_until(driver, EC.title_is("办公导航 - 纯净的办公导航，为价值和高效而生"))
            log.log_info("导航页面打开成功", driver=driver)
            # 查找上报请求
            result = proxy.har
            text = ''
            judge_result = judge(snode_info.page_show.value, tp, w_info.null_value.value, text, result, ss_scene_info.step1.value)
            if judge_result:
                log.log_pass("办公导航页面展示上报成功", driver=driver)
            else:
                log.log_error("办公导航页面展示上报失败", driver=driver)

        # 场景二：办公搜索框联想词点击上报
        with driver_step("step2: 办公搜索框联想词点击上报",driver,original_window):
            entertext = "test"
            proxy.new_har(proxy_trace_url)
            log.log_info(f"清空搜索输入框内容",driver=driver)
            # # 将页面滚动至顶部，使得搜索框正常展示
            # js_top = 'document.documentElement.scrollTop=0'
            # driver.execute_script(js_top)
            # log.log_info(f"将页面返回至顶部")
            # 点击输入框，清空其内容
            driver.find_element_by_name("word").clear()
            driver_click(driver, namexpath="word")
            driver.find_element_by_name("word").send_keys(entertext)
            log.log_info(f"输入搜索词 test",driver=driver)
            # 获取联想词内容list
            time.sleep(1)
            xpath  = '//div[@class="search_suggest_wrap"]/div/a'
            item_list = driver.find_elements_by_xpath(xpath)
            assert item_list,"获取搜索框联想词数据失败"
            item = random.choice(item_list)
            text = item.text
            # 点击联想词
            driver_click(driver, element=item)
            log.log_info(f"点击联想词:{text}")
            # 等待搜索联想词结果标签页打开
            driver_wait_until(driver,EC.number_of_windows_to_be(2))
            switch_to_new_window(driver, original_window)
            log.log_info(f"点击打开联想词{text} 结果标签页成功",driver=driver)
            result = proxy.har
            judge_result = judge(snode_info.search_click.value, tp, w_info.num_1.value, text, result, ss_scene_info.step2.value)
            if judge_result:
                log.log_pass("办公搜索框联想词点击上报成功", driver=driver)
            else:
                log.log_error("办公搜索框联想词点击上报失败", driver=driver)


        # 场景三：搜索框选择下拉框内容点击搜索button上报snode=1264---pass
        with driver_step('step3:办公搜索框选择下拉框内容点击搜索上报', driver, original_window):
            proxy.new_har(proxy_trace_url)
            # 点击输入框，清空其内容
            driver_click(driver, namexpath="word")
            driver.find_element_by_name("word").clear()
            log.log_info(f"清空搜索输入框内容", driver=driver)
            # 点击搜索下拉框内容
            xpath = '//*[@class="m_search_dropdown_word"]/a/span/span[2]'
            item_list = driver.find_elements_by_xpath(xpath)
            assert item_list, "获取办公导航搜索下拉框列表数据失败"
            item = random.choice(item_list)
            text = item.text
            driver_click(driver, element=item)
            log.log_info(f"点击搜索框下拉列表关键词：{text}")
            # 等待搜索结果标签页打开
            driver_wait_until(driver, EC.number_of_windows_to_be(2))
            switch_to_new_window(driver, original_window)
            log.log_info(f"打开{text}搜索结果标签页成功", driver=driver)
            result = proxy.har
            judge_result = judge(snode_info.search_click.value, tp, w_info.searchbox.value, text, result, ss_scene_info.step3.value)
            if judge_result:
                log.log_pass("办公搜索框选择下拉框内容点击搜索button上报成功", driver=driver)
            else:
                log.log_error("办公搜索框选择下拉框内容点击搜索button上报失败", need_assert=False, driver=driver)

        # 场景四：办公搜索框输入内容点击搜索button上报snode=1264
        with driver_step("step4:办公搜索框输入内容点击搜索上报", driver, original_window):
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
            judge_result = judge(snode_info.search_click.value, tp, w_info.num_1.value, text, result, ss_scene_info.step4.value)
            time.sleep(2)
            if judge_result:
                log.log_pass("办公搜索框输入内容点击搜索上报成功", driver=driver)
            else:
                log.log_error("办公搜索框输入内容点击搜索上报失败", driver=driver)

        # 场景五：办公名站点击上报snode=1163---pass
        with driver_step('step5:办公名站点击上报', driver, original_window):
            proxy.new_har(proxy_trace_url)
            # 办公导航名站点击上报
            xpath = '//*[@class="m_hot_site"]/div[@class="hot_site"]/div/div/a'
            item_list = driver.find_elements_by_xpath(xpath)
            assert item_list, "获取办公名站数据失败"
            item = random.choice(item_list)
            text = item.text
            driver_click(driver, element=item)
            log.log_info(f"点击名站{text}", driver=driver)
            driver_wait_until(driver, EC.number_of_windows_to_be(2))
            switch_to_new_window(driver, original_window)
            log.log_info(f"打开办公名站{text}成功", driver=driver)
            result = proxy.har
            judge_result = judge(snode_info.page_click.value, tp, w_info.mz.value, text, result, ss_scene_info.step5.value)
            time.sleep(2)
            if judge_result:
                log.log_pass("办公名站点击上报成功", driver=driver)
            else:
                log.log_error("办公名站点击上报失败", driver=driver, need_assert=False)

        # 场景六：办公最近使用模块tab点击上报snode=1163---pass
        with driver_step('step6:办公最近使用模块tab点击上报', driver, original_window):
            # 办公导航最近使用模块tab点击上报
            proxy.new_har(proxy_trace_url)
            xpath = '//*[@class="m_site_tab_card"]/ul/li[@ttab="常用网址"]'
            item_list = driver.find_elements_by_xpath(xpath)
            assert item_list, "获取办公最近使用模块tab数据失败"
            item = random.choice(item_list)
            text = item.text
            driver_click(driver, element=item)
            log.log_info(f"点击最近使用模块tab {text}", driver=driver)
            log.log_info(f"点击最近使用模块tab{text}成功", driver=driver)
            result = proxy.har
            judge_result = judge(snode_info.page_click.value, tp, w_info.kztab.value, text, result, ss_scene_info.step6.value)
            time.sleep(2)
            if judge_result:
                log.log_pass("办公最近使用模块tab点击上报成功", driver=driver)
            else:
                log.log_error("办公最近使用模块tab点击上报失败", driver=driver, need_assert=False)

        # 场景七：酷站点击上报snode=1163---pass
        with driver_step("step7:办公酷站点击上报", driver, original_window):
            proxy.new_har(proxy_trace_url)
            # 办公导航酷站点击上报
            xpath = '//*[@class="card_body"]/ul/li/a/span[@class="site_name"]'
            item_list = driver.find_elements_by_xpath(xpath)
            assert item_list, "获取网页酷站数据失败"
            item = random.choice(item_list)
            text = item.text
            driver_click(driver, element=item)
            log.log_info(f"点击酷站 {text}", driver=driver)
            driver_wait_until(driver, EC.number_of_windows_to_be(2))
            switch_to_new_window(driver, original_window)
            log.log_info(f"办公酷站 {text}点击成功", driver=driver)
            result = proxy.har
            judge_result = judge(snode_info.page_click.value, tp, w_info.kz.value, text, result, ss_scene_info.step7.value)
            time.sleep(2)
            if judge_result:
                log.log_pass("办公酷站点击上报成功", driver=driver)
            else:
                log.log_error("办公酷站点击上报失败", need_assert=False)

        # 场景八：今日热搜点击上报snode=1163---pass
        with driver_step('step8:办公今日热搜点击上报', driver, original_window):
            try_xpath = '//*[@class="news_list_wrapper"]/div[@class="m_site_text_news_item news_card"]'
            try:
                driver.find_element_by_xpath(try_xpath)
            except:
                log.log_pass("未查到下拉列表及卡片，请检查开关配置是否打开", driver=driver)
            else:
                proxy.new_har(proxy_trace_url)
                # 办公导航今日热搜点击上报
                xpath = '//*[@class="m_site_text_news_item news_card"]/a[@arp_tg="新闻热榜"]'
                item_list = driver.find_elements_by_xpath(xpath)
                assert item_list, "获取新闻热榜数据失败"
                item = random.choice(item_list)
                text = item.get_attribute("title")
                driver_click(driver, element=item)
                log.log_info(f"新闻热榜点击 {text}", driver=driver)
                driver_wait_until(driver, EC.number_of_windows_to_be(2))
                switch_to_new_window(driver, original_window)
                log.log_info(f"新闻热榜点击 {text} 成功", driver=driver)
                result = proxy.har
                judge_result = judge(snode_info.page_click.value, tp, w_info.kz.value, text, result, ss_scene_info.step8.value)
                if judge_result:
                    log.log_pass("办公今日热搜点击上报上报成功", driver=driver)
                else:
                    log.log_error("办公今日热搜点击上报上报失败", driver=driver)

        # 场景jiu：今日热搜卡片点击上报snode=1163---pass
        with driver_step('step9:办公今日热搜卡片点击上报', driver, original_window):
            try_xpath = '//*[@class="news_list_wrapper"]/div[@class="m_site_pic_and_text_items_card news_card"]/a[@ttab="新闻资讯"]'
            try:
                try_list = driver.find_elements_by_xpath(try_xpath)
            except:
                log.log_pass("未查到下拉列表及卡片，请检查开关配置是否打开", driver=driver)
            else:
                if (len(try_list) != 0):
                    proxy.new_har(proxy_trace_url)
                    # 办公导航今日热搜卡片点击上报
                    xpath = '//*[@class="m_site_pic_and_text_items_card news_card"]/a[@arp_tg="内容"]'
                    item_list = driver.find_elements_by_xpath(xpath)
                    assert item_list, "获取今日热搜卡片数据失败"
                    item = random.choice(item_list)
                    text = item.get_attribute("md5")
                    driver_click(driver, element=item)
                    log.log_info(f"今日热搜卡片点击 {text}", driver=driver)
                    driver_wait_until(driver, EC.number_of_windows_to_be(2))
                    switch_to_new_window(driver, original_window)
                    log.log_info(f"今日热搜卡片点击 {text} 成功", driver=driver)
                    result = proxy.har
                    judge_result = judge(snode_info.page_click.value, tp, w_info.kz.value, text, result, ss_scene_info.step9.value)
                    time.sleep(2)
                    if judge_result:
                        log.log_pass("办公今日热搜卡片点击上报成功", driver=driver)
                    else:
                        log.log_error("办公今日热搜卡片点击上报失败", need_assert=False, driver=driver)
                else:
                    log.log_pass("未查到下拉列表及卡片，请检查开关配置是否打开", driver=driver)

        # 场景十：电梯栏点击上报snode=1163---pass
        with driver_step('step10:办公电梯栏点击上报', driver, original_window):
            proxy.new_har(proxy_trace_url)
            # 办公导航电梯栏点击上报
            # 当前焦点所在频道 class="m_nav_item g_clr current"
            # 其他频道 class="m_nav_item g_clr"
            current_xpath = '//*[@class="m_nav_item g_clr current"]/div[@class="nav_item_wrap"]/span'
            xpath = '//*[@class="m_nav_item g_clr"]/div[@class="nav_item_wrap"]/span'
            item_list = driver.find_elements_by_xpath(xpath)
            item_list.append(driver.find_element_by_xpath(current_xpath))
            assert item_list, "获取电梯栏数据失败"
            item = random.choice(item_list)
            text = item.text
            driver_click(driver, element=item)
            log.log_info(f"电梯栏点击 {text} 成功", driver=driver)
            result = proxy.har
            judge_result = judge(snode_info.page_click.value, tp, w_info.leftnav.value, text, result, ss_scene_info.step10.value)
            time.sleep(2)
            if judge_result:
                log.log_pass("办公电梯栏点击上报成功", driver=driver)
            else:
                log.log_error("办公电梯栏点击上报失败", need_assert=False)

        # 场景十一：办公电梯栏点击设置按钮上报snode=1163---pass
        with driver_step('step11:办公电梯栏点击设置按钮上报', driver, original_window):
            proxy.new_har(proxy_trace_url)
            # 办公电梯栏点击设置按钮上报
            # 当前焦点所在频道 class="m_nav_item g_clr current"
            # 其他频道 class="m_nav_item g_clr"
            current_xpath = '//*[@class="m_nav_item g_clr current"]/button'
            xpath = '//*[@class="m_nav_item g_clr"]/button'
            item_list = driver.find_elements_by_xpath(xpath)
            item_list.append(driver.find_element_by_xpath(current_xpath))
            assert item_list, "获取电梯栏数据失败"
            item = random.choice(item_list)
            text = item.get_attribute("md5")
            driver_click(driver, element=item)
            log.log_info(f"办公电梯栏点击设置按钮 {text} 成功", driver=driver)
            result = proxy.har
            judge_result = judge(snode_info.page_click.value, tp, w_info.leftnavset.value, text, result, ss_scene_info.step11.value)
            time.sleep(2)
            if judge_result:
                log.log_pass("办公电梯栏点击设置按钮上报成功", driver=driver)
            else:
                log.log_error("办公电梯栏点击设置按钮上报失败", need_assert=False)

        # 场景十二：视频音乐点击左侧大图卡片上报snode=1163---pass
        with driver_step('step12:视频音乐点击左侧大图卡片上报', driver, original_window):
            # 视频音乐点击上报--左侧大图卡片
            # 该频道模块列表数据需要页面滑动至此处才会发起加载请求，故需要先行定位至该频道使其加载
            requests_xpath = '//*[@class="m_nav_item g_clr"]/div[@class="nav_item_wrap"]/span'
            span_list = driver.find_elements_by_xpath(requests_xpath)
            for i in span_list:
                if i.text == '视频音乐':
                    driver_click(driver, element=i)
                    time.sleep(1.5)
            try_xpath = '//*[@class="news_list_wrapper"]/a[@ttab="视频音乐"]'
            try:
                driver.find_element_by_xpath
            except:
                log.log_pass("未查到该模块元素，请检查开关配置是否打开")
            else:
                proxy.new_har(proxy_trace_url)
                xpath = '//*[@class="news_list_wrapper"]/a[@arp_index="1"]/div[@class="news_info"]/div'
                item = driver.find_element_by_xpath(xpath)
                text = item.text
                driver_click(driver, element=item)
                log.log_info(f"视频音乐点击上报--左侧大图卡片标题 {text}", driver=driver)
                driver_wait_until(driver, EC.number_of_windows_to_be(2))
                switch_to_new_window(driver, original_window)
                log.log_info(f"视频音乐点击上报--左侧大图卡片标题 {text} 成功", driver=driver)
                result = proxy.har
                judge_result = judge(snode_info.page_click.value, tp, w_info.kz.value, text, result, ss_scene_info.step12.value)
                time.sleep(2)
                if judge_result:
                    log.log_pass("办公视频音乐点击左侧大图卡片上报成功", driver=driver)
                else:
                    log.log_error("办公视频音乐点击左侧大图卡片上报失败", need_assert=False)

        # 场景十三：视频音乐点击右侧卡片上报snode=1163---pass
        with driver_step('step13:视频音乐点击右侧卡片上报', driver, original_window):
            # 视频音乐点击上报--右侧卡片
            # 该频道模块列表数据需要页面滑动至此处才会发起加载请求，故需要先行定位至该频道使其加载
            requests_xpath = '//*[@class="m_nav_item g_clr"]/div[@class="nav_item_wrap"]/span'
            span_list = driver.find_elements_by_xpath(requests_xpath)
            for i in span_list:
                if i.text == '视频音乐':
                    driver_click(driver, element=i)
                    time.sleep(3)
            try_xpath = '//*[@class="news_list_wrapper"]/div[@class="m_site_video_items_card news_card"]/div/a[@ttab="视频音乐"]'
            try:
                try_list = driver.find_elements_by_xpath(try_xpath)
            except:
                log.log_pass("未查到该模块元素，请检查开关配置是否打开")
            else:
                if len(try_list) != 0:
                    proxy.new_har(proxy_trace_url)
                    xpath = '//*[@class="m_site_video_items_card news_card"]/div/a/div/div[@class="news_info"]/div[@class="title dobule_text_overflow"]'
                    item_list = driver.find_elements_by_xpath(xpath)
                    assert item_list, "办公视频音乐右侧卡片数据获取失败"
                    item = random.choice(item_list)
                    text = item.text
                    driver_click(driver, element=item)
                    log.log_info(f"视频音乐点击上报--右侧卡片卡片标题 {text}", driver=driver)
                    driver_wait_until(driver, EC.number_of_windows_to_be(2))
                    switch_to_new_window(driver, original_window)
                    log.log_info(f"视频音乐点击上报--右侧卡片卡片标题 {text} 成功", driver=driver)
                    result = proxy.har
                    judge_result = judge(snode_info.page_click.value, tp, w_info.kz.value, text, result, ss_scene_info.step13.value)
                    time.sleep(2)
                    if judge_result:
                        log.log_pass("办公视频音乐点击右侧卡片上报成功", driver=driver)
                    else:
                        log.log_error("办公视频音乐点击右侧卡片上报失败", need_assert=False)
                else:
                    log.log_pass("未查到该模块元素，请检查开关配置是否打开")
        # 场景十四：购物出行点击左侧大图卡片上报snode=1163---pass
        with driver_step('step14:购物出行点击左侧大图卡片上报', driver, original_window):
            # 购物出行点击上报--左侧大图卡片
            # 该频道模块列表数据需要页面滑动至此处才会发起加载请求，故需要先行定位至该频道使其加载
            requests_xpath = '//*[@class="m_nav_item g_clr"]/div[@class="nav_item_wrap"]/span'
            span_list = driver.find_elements_by_xpath(requests_xpath)
            for i in span_list:
                if i.text == '购物出行':
                    driver_click(driver, element=i)
                    time.sleep(1.5)
            try_xpath = '//*[@class="news_list_wrapper"]/a[@ttab="购物出行"]'
            try:
                driver.find_element_by_xpath
            except:
                log.log_pass("未查到该模块元素，请检查开关配置是否打开")
            else:
                proxy.new_har(proxy_trace_url)
                xpath = '//*[@class="news_list_wrapper"]/a[@exp="购物出行"]/div[@class="news_info"]/div'
                item = driver.find_element_by_xpath(xpath)
                text = item.text
                driver_click(driver, element=item)
                log.log_info(f"购物出行点击左侧大图卡片上报标题 {text}", driver=driver)
                driver_wait_until(driver, EC.number_of_windows_to_be(2))
                switch_to_new_window(driver, original_window)
                log.log_info(f"购物出行点击左侧大图卡片上报标题 {text} 成功", driver=driver)
                result = proxy.har
                judge_result = judge(snode_info.page_click.value, tp, w_info.kz.value, text, result, ss_scene_info.step14.value)
                time.sleep(2)
                if judge_result:
                    log.log_pass("购物出行点击左侧大图卡片上报成功", driver=driver)
                else:
                    log.log_error("购物出行点击左侧大图卡片上报失败", need_assert=False)

        # 场景十五：购物出行点击右侧卡片上报snode=1163---pass
        with driver_step('step15:视频音乐点击右侧卡片上报', driver, original_window):
            # 购物出行点击右侧卡片上报
            # 该频道模块列表数据需要页面滑动至此处才会发起加载请求，故需要先行定位至该频道使其加载
            requests_xpath = '//*[@class="m_nav_item g_clr"]/div[@class="nav_item_wrap"]/span'
            span_list = driver.find_elements_by_xpath(requests_xpath)
            for i in span_list:
                if i.text == '购物出行':
                    driver_click(driver, element=i)
                    time.sleep(3)
            try_xpath = '//*[@class="news_list_wrapper"]/div[@class="m_site_pic_and_text_items_card news_card""]/a[@ttab="购物出行"]'
            try:
                try_list = driver.find_elements_by_xpath(try_xpath)
            except:
                log.log_pass("未查到该模块元素，请检查开关配置是否打开")
            else:
                if len(try_list) != 0:
                    proxy.new_har(proxy_trace_url)
                    xpath = '//*[@class="m_site_pic_and_text_items_card news_card"]/a[@ttab="购物出行"]/div[@class="news_info"]/div[@class="title dobule_text_overflow"]'
                    item_list = driver.find_elements_by_xpath(xpath)
                    assert item_list, "购物出行右侧卡片数据获取失败"
                    item = random.choice(item_list)
                    text = item.text
                    driver_click(driver, element=item)
                    log.log_info(f"购物出行点击右侧卡片上报--右侧卡片卡片标题 {text}", driver=driver)
                    driver_wait_until(driver, EC.number_of_windows_to_be(2))
                    switch_to_new_window(driver, original_window)
                    log.log_info(f"购物出行点击右侧卡片上报--右侧卡片卡片标题 {text} 成功", driver=driver)
                    result = proxy.har
                    judge_result = judge(snode_info.page_click.value, tp, w_info.kz.value, text, result, ss_scene_info.step15.value)
                    time.sleep(2)
                    if judge_result:
                        log.log_pass("购物出行点击右侧卡片上报成功", driver=driver)
                    else:
                        log.log_error("购物出行点击右侧卡片上报失败", need_assert=False)
                else:
                    log.log_pass("未查到该模块元素，请检查开关配置是否打开")

        # 场景十六：办公搜索框点击搜索框下方内容上报snode=1264---pass
        with driver_step('step16:办公搜索框点击搜索框下方内容上报', driver, original_window):
            proxy.new_har(proxy_trace_url)
            # 点击一下body，确保焦点不在输入框上，否则会遮挡输入框下方内容
            driver.execute_script("document.body.click()")
            log.log_info("取消输入框上的焦点", driver=driver)

            xpath = '//*[@class="m_hot_word g_clr"]/a/span'
            item_list = driver.find_elements_by_xpath(xpath)
            assert item_list, "搜索框下方热词数据获取失败"
            # TODO: 由于有部分搜索框下方关键词被遮挡，需要循环获取没被遮挡的
            while True:
                item = random.choice(item_list)
                if item.is_displayed() and item.is_enabled():
                    break
            # item = random.choice(item_list)
            text = item.text
            log.log_info(f"办公搜索框点击搜索框下方内容 {text}", driver=driver)
            driver_click(driver, element=item)
            driver_wait_until(driver, EC.number_of_windows_to_be(2))
            switch_to_new_window(driver, original_window)
            log.log_info(f"办公搜索框点击搜索框下方内容 {text} 成功", driver=driver)
            result = proxy.har
            judge_result = judge(snode_info.search_click.value, tp, w_info.ssrc.value, text, result, ss_scene_info.step16.value)
            time.sleep(2)
            if judge_result:
                log.log_pass("办公搜索框点击搜索框下方内容上报成功", driver=driver)
            else:
                log.log_error("办公搜索框点击搜索框下方内容上报失败", need_assert=False)


if __name__ == '__main__':
    # pytest.main(["-v", "-s", __file__])
    allure_attach_path = os.path.join("Outputs", "allure")
    pytest.main(["-v", "-s", __file__, '--alluredir=%s' % allure_attach_path])
    os.system("allure serve %s" % allure_attach_path)
