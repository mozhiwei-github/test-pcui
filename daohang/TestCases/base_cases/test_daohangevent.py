import os
import time
import random
import allure
import pytest
from furl import furl
from common.log import log
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from daohang.utils import switch_to_new_window, driver_step, driver_get_reload, driver_wait_until, driver_click, \
    back_to_original_window
from daohang.web_message import *

from daohang.contants import *

# from common.utils import keyboardInputByCode,keyboardInputByCode_alt_tab

def analysis(result, snode):
    url_list = []
    response_list = []
    status_list = []
    snode_param = 'snode=' + str(snode)
    for entry in result['log']['entries']:
        url = entry['request']['url']  # str
        if snode_param in url:
            url_list.append(url)
            response = entry['response']
            response_list.append(response)
            status = response.get('status')
            status_list.append(status)
    return url_list, response_list, status_list


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

@allure.epic('导航基础埋点案例测试')
@allure.feature('场景：导航基础埋点上报')
class TestDaoHangEvent(object):
    @allure.story('用例：导航基础埋点上报 预期成功')
    @allure.description("""
        step1: 导航页面展示上报
        step2: 搜索框联想词点击上报
        step3: 搜索框输入内容点击搜索上报
        step4: 搜索框选择下拉框内容点击搜索上报
        step5: 中间栏点击上报
        step6: 搜索框点击搜索框下方内容上报
        step7: 通栏快速入口点击上报
        step8: 名站点击上报
        step9: 酷站点击上报
        step10: 搜索框右侧轮播点击上报
        step11: 猜你喜欢点击上报
        step12: 信息流顶部新闻轮播点击上报
        step13: 信息流tab点击上报
        step14: 信息流列表点击上报
        step15: 左侧精选点击上报
        step16: 右侧游戏板块点击上报
        step17: 右侧热门板块点击上报
    """)
    def test_eventtest(self, chrome_driver_init, get_env_and_channel):
        proxy, driver = chrome_driver_init
        # 浏览器窗口最大化
        driver.maximize_window()
        # 导航首页
        env, channel = get_env_and_channel
        base_url = env + channel
        if env in ["https://www.duba.com", "https://www.newduba.cn"]:
            proxy_trace_url = f"{env}/proxy/trace"
        else:
            proxy_trace_url = "http://dh2.tj.ijinshan.com/__dh.gif"
        allure.dynamic.title(f"导航基础埋点上报 渠道: {base_url}")

        # 上报的渠道号 tp
        tp = channel.split('.html')[0][1:]

        # 场景一：导航页面展示上报snode=100上报
        with driver_step("step1: 导航页面展示上报", driver):
            # proxy.new_har(proxy_trace_url)
            driver_get_reload(driver,base_url)
            #driver.get(base_url)
            proxy.new_har(proxy_trace_url)
            # 采用增加全局广告开关cookie的形式规避开屏广告---临时方案
            if get_ad_sort(env, channel):
                set_cookie_value(driver, "global_ad_close", "close")
                driver.refresh()
                log.log_info("页面刷新成功")
            else:
                log.log_info("未配置开屏广告")
                driver.refresh()
                log.log_info("页面刷新成功")
            # 存储原始窗口的 ID
            original_window = driver.current_window_handle
            assert len(driver.window_handles) == 1, "窗口个数检查失败"
            # 等待页面加载完毕
            if env in ["https://www.duba.com", "http://cm.duba.com"]:
                driver_wait_until(driver, EC.title_is("毒霸网址大全 - 安全实用的网址导航"))
            elif env in ["https://www.newduba.cn", "http://cm.newduba.cn"]:
                driver_wait_until(driver, EC.title_is("上网导航—安全快捷的网址大全"))
                log.log_info("导航页面打开成功", driver=driver)
            # 查找上报请求
            result = proxy.har
            text = ''
            judge_result = judge(snode_info.page_show.value, tp, w_info.null_value.value, text, result, scene_info.step1.value)
            if judge_result:
                log.log_pass("导航页面展示上报成功", driver=driver)
            else:
                log.log_error("导航页面展示上报失败", driver=driver)

        # 场景二：搜索框联想词点击上报
        with driver_step("step2: 搜索框联想词点击上报", driver, original_window):
            entertext = "test"
            proxy.new_har(proxy_trace_url)
            # 将页面滚动至顶部，使得搜索框正常展示
            # js_top = 'document.documentElement.scrollTop=0'
            # driver.execute_script(js_top)
            # log.log_info(f"将页面返回至顶部")
            # 点击输入框，清空其内容
            driver_click(driver,idxpath="search_keyword")
            log.log_info(f"清空搜索输入框内容", driver=driver)
            driver.find_element_by_id("search_keyword").send_keys(entertext)
            log.log_info(f"输入搜索词 test", driver=driver)
            # 获取联想词内容list
            time.sleep(1)
            xpath = '//div[@class="search_suggest_panel"]/a[@class="sug_item g_oh"]'
            item_list = driver.find_elements_by_xpath(xpath)
            assert item_list, "获取搜索框联想词数据失败"
            item = random.choice(item_list)
            text = item.text
            # 点击联想词
            driver_click(driver,element=item)
            log.log_info(f"点击联想词:{text}")
            # 等待搜索联想词结果标签页打开
            driver_wait_until(driver, EC.number_of_windows_to_be(2))
            switch_to_new_window(driver, original_window)
            log.log_info(f"点击打开联想词{text} 结果标签页成功", driver=driver)
            result = proxy.har
            judge_result = judge(snode_info.search_click.value, tp, w_info.num_1.value, text, result, scene_info.step2.value)
            if judge_result:
                log.log_pass("搜索框联想词点击上报成功", driver=driver)
            else:
                log.log_error("搜索框联想词点击上报失败", driver=driver)

        # 场景三：搜索框输入内容点击搜索button上报snode=1264
        with driver_step("step3: 搜索框输入内容点击搜索上报", driver, original_window):
            proxy.new_har(proxy_trace_url)
            # 输入搜索内容
            text = "EventTest"
            # 点击输入框，清空其内容
            driver.find_element_by_id("search_keyword").clear()
            log.log_info(f"清空搜索输入框内容", driver=driver)
            driver.find_element_by_id("search_keyword").send_keys(text)
            log.log_info(f"输入搜索内容：{text}", driver=driver)
            driver_click(driver,classxpath="btn_search")
            log.log_info("点击搜索按钮")
            # 等待搜索结果标签页打开
            driver_wait_until(driver, EC.number_of_windows_to_be(2))
            # 将窗口句柄切换到新标签页
            switch_to_new_window(driver, original_window)
            log.log_info(f"打开 {text} 搜索结果标签页成功", driver=driver)
            result = proxy.har
            judge_result = judge(snode_info.search_click.value, tp, w_info.num_1.value, text, result, scene_info.step3.value)
            if judge_result:
                log.log_pass("搜索框输入内容点击搜索上报成功", driver=driver)
            else:
                log.log_error("搜索框输入内容点击搜索上报失败", driver=driver)

        # 场景四：搜索框选择下拉框内容点击搜索button上报snode=1264---pass
        with driver_step("step4: 搜索框选择下拉框内容点击搜索上报", driver, original_window):
            proxy.new_har(proxy_trace_url)
            # 点击输入框，清空其内容
            driver_click(driver, idxpath="search_keyword")
            driver.find_element_by_id("search_keyword").clear()
            log.log_info(f"清空搜索输入框内容", driver=driver)
            # 判断是否存在历史搜索模块
            history_search_xpath = '//*[@id="mainSearchTip"]/div/div[@class="m_search_history"]'
            try:
                driver.find_element_by_xpath(history_search_xpath)
            except:
                xpath = '//*[@id="mainSearchTip"]//div[@class="panel_wrap g_clr"]//a[@class="shc_link g_oh"]/span[@class="text"]'
            else:
                xpath = '//*[@id="mainSearchTip"]//div[@class="panel_wrap g_clr"]//a[@class="shc_link g_oh"]/span[@class="text"]'
            item_list = driver.find_elements_by_xpath(xpath)
            assert item_list, "获取搜索框下拉列表数据失败"
            item = random.choice(item_list)
            text = item.text
            # 搜索下拉框列表存在广告文字链、百度推荐下发、精准推荐、后台配置--做标记
            if item.get_attribute("sctype") == 'accurate_baidu':
                type = 'accurate_baidu'
            elif item.get_attribute("sctype") == 'AD':
                type = 'ad'
            else:
                type = 'others'
            # 点击搜索下拉框内容
            driver_click(driver, element=item)
            log.log_info(f"点击搜索框下拉列表关键词：{text}")
            # 等待搜索结果标签页打开
            driver_wait_until(driver, EC.number_of_windows_to_be(2))
            switch_to_new_window(driver, original_window)
            log.log_info(f"打开 {text} 搜索结果标签页成功", driver=driver)
            result = proxy.har
            # 搜索下拉框列表存在广告文字链、百度推荐下发、精准推荐、后台配置
            if type == 'accurate_baidu':
                judge_result = judge(snode_info.search_click.value,tp, w_info.searchbox.value, text, result,
                                     scene_info.step4_1.value)
            elif type == 'ad':
                judge_result = judge(snode_info.page_click.value, tp, w_info.searchword.value, text, result,
                                     scene_info.step4_2.value)
            else:
                judge_result = judge(snode_info.search_click.value, tp, w_info.searchbox.value, text, result,
                                     scene_info.step4_3.value)
            if judge_result:
                log.log_pass("搜索框选择下拉框内容点击搜索上报成功", driver=driver)
            else:
                log.log_error("搜索框选择下拉框内容点击搜索上报失败", driver=driver)

        # 场景五：中间栏点击上报snode=1163---pass
        with driver_step("step5: 中间栏点击上报", driver, original_window):
            proxy.new_har(proxy_trace_url)
            # 点击中间栏
            xpath = '//*[@id="wrapper"]//div[contains(@class, "rtcenter_game")]/table/tbody/tr/td[2]/div/ul/li/a'
            item_list = driver.find_elements_by_xpath(xpath)
            assert item_list, "获取中间栏数据失败"
            # TODO: 目前直接去除了最后一个点击不到的京东按钮
            item = random.choice(item_list[:-1])
            text = item.text
            driver_click(driver, element=item)
            log.log_info(f"点击中间栏：{text}", driver=driver)
            driver_wait_until(driver, EC.number_of_windows_to_be(2))
            switch_to_new_window(driver, original_window)
            log.log_info(f"打开中间栏 {text} 成功", driver=driver, shot_delay=2)
            result = proxy.har
            judge_result = judge(snode_info.page_click.value, tp, w_info.zhongjianlan.value, text, result, scene_info.step5.value)
            if judge_result:
                log.log_pass(f"{scene_info.step5.value}成功", driver=driver)
            else:
                log.log_error(f"{scene_info.step5.value}失败", driver=driver)

        # 场景六：搜索框点击搜索框下方内容上报snode=1264---pass
        with driver_step("step6: 搜索框点击搜索框下方内容上报", driver, original_window, clear_cookies=False):
            # 执行场景用例前先关闭页面所有广告
            ad_switch_xpath = '//*[@class="header_close_ads_btn btn"]/a'
            driver_click(driver,xpath=ad_switch_xpath)
            log.log_info(f"页面所有广告关闭成功", driver=driver)
            # 点击一下body，关闭广告关闭提示，否则会遮挡输入框下方内容
            driver.execute_script("document.body.click()")
            log.log_info("关闭广告关闭提示", driver=driver)
            proxy.new_har(proxy_trace_url)
            # 点击一下body，确保焦点不在输入框上，否则会遮挡输入框下方内容
            driver.execute_script("document.body.click()")
            log.log_info("取消输入框上的焦点", driver=driver)

            # 获取搜索框下方内容
            xpath = '//*[@id="search_form"]//ul[contains(@class, "hot_link")]/li/a'
            item_list = driver.find_elements_by_xpath(xpath)
            assert item_list, "获取搜索框下方内容失败"

            # TODO: 由于有部分搜索框下方关键词被遮挡，需要循环获取没被遮挡的
            while True:
                item = random.choice(item_list)
                if item.is_displayed() and item.is_enabled():
                    break
            text = item.text
            url_args = furl(item.get_attribute("href")).args
            keyword = url_args.get('word', None) or url_args.get('wd', None)
            # 后台配置的部分特殊热词herf中无wd or word
            if not keyword:
                keyword = text
            #assert keyword, "获取搜索关键词失败"
            # TODO: 由于有部分搜索框下方关键词有些是调起客户端搜索词--兜底数据上报1163，需要区分判断
            sctype_type = item.get_attribute("sctype")
            class_type = item.get_attribute("class")
            driver_click(driver, element=item)
            log.log_info(f"点击搜索框下方关键词：{text}，实际搜索关键词为：{keyword}", driver=driver)
            # 区分默认搜索词和接口下发热词、特殊热词、图片广告
            if sctype_type == "normal":
                if "jq_open_client" in class_type:
                    # 后台配置调起客户端热词
                    keyword = text
                    # 切换系统焦点从打开的client程序至导航页面--暂时不做关闭该客户端页面处理
                    # keyboardInputByCode_alt_tab('tab')
                    log.log_info("切换焦点至导航页面完成")
                    switch_to_new_window(driver, original_window)
                    log.log_info(f"打开 {keyword} 搜索结果标签页成功", driver=driver)
                    result = proxy.har
                    judge_result = judge(snode_info.page_click.value, tp, w_info.rc.value, keyword, result, scene_info.step6_1.value)
                elif "jq_fixed" in class_type:
                    # 后台配置固定位置热词
                    keyword = text
                    # 等待搜索结果标签页打开
                    driver_wait_until(driver, EC.number_of_windows_to_be(2))
                    switch_to_new_window(driver, original_window)
                    log.log_info(f"打开 {keyword} 搜索结果标签页成功", driver=driver)
                    result = proxy.har
                    judge_result = judge(snode_info.search_click.value, tp, w_info.rc.value, keyword, result,
                                         scene_info.step6_4.value)
                else:
                    # 预留新增类型
                    keyword = text
                    # 等待搜索结果标签页打开
                    driver_wait_until(driver, EC.number_of_windows_to_be(2))
                    switch_to_new_window(driver, original_window)
                    log.log_info(f"打开 {keyword} 搜索结果标签页成功", driver=driver)
                    result = proxy.har
                    judge_result = judge(snode_info.search_click.value, tp, w_info.rc.value, keyword, result,
                                         scene_info.step6_5.value)
            elif sctype_type == 'accurate_baidu' or 'accurate_recommend':
                # 百度搜索热词accurate_baidu  or  精准推荐热词 accurate_recommend
                keyword = text
                # 等待搜索结果标签页打开
                driver_wait_until(driver, EC.number_of_windows_to_be(2))
                switch_to_new_window(driver, original_window)
                log.log_info(f"打开 {keyword} 搜索结果标签页成功", driver=driver)
                result = proxy.har
                judge_result = judge(snode_info.search_click.value, tp, w_info.rc.value, keyword, result,
                                     scene_info.step6_3.value)
            elif class_type == "fixed_img g_fimg":
                # 图片广告
                keyword = ''
                driver_wait_until(driver, EC.number_of_windows_to_be(2))
                switch_to_new_window(driver, original_window)
                log.log_info(f"打开图片广告结果标签页成功", driver=driver)
                result = proxy.har
                judge_result = judge(snode_info.page_click.value, tp, w_info.rctpfg.value, keyword, result,
                                     scene_info.step6_2.value)
            else:
                result = proxy.har
                judge_result = judge(snode_info.search_click.value, tp, w_info.rc.value, keyword, result,
                                     scene_info.step6_5.value)
            if judge_result:
                log.log_pass("搜索框点击搜索框下方内容上报成功", driver=driver)
            else:
                log.log_error("搜索框点击搜索框下方内容上报失败", driver=driver)

        # 场景七：通栏快速入口点击上报snode=1163--pass
        with driver_step("step7: 通栏快速入口点击上报", driver, original_window):
            proxy.new_har(proxy_trace_url)
            xpath = '//div[@class="m_second_nav"]//div[@class="second_nav_tabs"]/ul/li/a'
            shouye_xpath = '//div[@class="m_second_nav"]//div[@class="second_nav_tabs"]/ul/li/a[@ttab="首页"]'
            item_list = driver.find_elements_by_xpath(xpath)
            assert item_list, "获取通栏快速入口数据失败"
            item = random.choice(item_list)
            # iframe_get用于判断获取到的快速入口打开新标签页与否
            iframe_get = str(item.get_attribute("iframeheight"))
            text = item.find_element_by_xpath('./span').text
            driver_click(driver,element=item)
            log.log_info(f"点击通栏快速入口：{text}", driver=driver)
            # 点击个别标签不会打开新标签页
            if iframe_get is None:
                # 等待通栏入口新标签页打开
                driver_wait_until(driver, EC.number_of_windows_to_be(2))
                switch_to_new_window(driver, original_window)
                log.log_info(f"打开通栏 {text} 快速入口成功", driver=driver)
            result = proxy.har
            judge_result = judge(snode_info.page_click.value, tp, w_info.ksrk.value, text, result, scene_info.step7.value)
            if judge_result:
                log.log_pass("通栏快速入口点击上报成功", driver=driver)
            else:
                log.log_error("通栏快速入口点击上报失败", driver=driver)
            # 执行完该用例后，页面布局可能会改变（original_window采用的是窗口句柄id判断）
            # 所以需要点击一次首页确保还原成最初的样子
            shouye_item = driver.find_element_by_xpath(shouye_xpath)
            driver_click(driver,element=shouye_item)
            log.log_info("点击快速入口首页恢复页面完成")

        # 场景八：名站点击上报snode=1163---pass
        with driver_step("step8: 名站点击上报", driver, original_window):
            proxy.new_har(proxy_trace_url)
            # 名站点击上报
            xpath = '//*[@id="wrapper"]//div[@class="m_hotsite"]//ul[contains(@class, "hot_top")]/li/div/a'
            item_list = driver.find_elements_by_xpath(xpath)
            assert item_list, "获取名站数据失败"
            item = random.choice(item_list)
            text = item.text
            # 含有md5属性的a标签，text为md5值（如：游戏精选）
            item_md5_attr = item.get_attribute("md5")
            if item_md5_attr:
                try:
                    item = item.find_element_by_xpath('./img')
                except:
                    item = item.find_element_by_xpath('./span')
                text = item_md5_attr
            driver_click(driver, element=item)
            log.log_info(f"点击名站：{text}", driver=driver)
            driver_wait_until(driver, EC.number_of_windows_to_be(2))
            switch_to_new_window(driver, original_window)
            log.log_info(f"打开名站 {text} 成功", driver=driver)

            result = proxy.har
            judge_result = judge(snode_info.page_click.value, tp, w_info.mz.value, text, result, scene_info.step8.value)
            if judge_result:
                log.log_pass("名站点击上报成功", driver=driver)
            else:
                log.log_error("名站点击上报失败", driver=driver)

        # 场景九：酷站点击上报snode=1163---pass
        with driver_step("step9: 酷站点击上报", driver, original_window):
            proxy.new_har(proxy_trace_url)
            # 酷站点击上报
            xpath = '//*[@id="wrapper"]//div[@class="m_site_cool_wrap"]//ul[@class="site_cool_list"]/li/a[@cid]'
            item_list = driver.find_elements_by_xpath(xpath)
            assert item_list, "获取酷站数据失败"
            item = random.choice(item_list)
            text = item.text
            if item.get_attribute("class") == 'sc_item':
                item = item.find_element_by_xpath('./span[2]')
                text = item.text
            driver_click(driver, element=item)
            log.log_info(f"点击酷站：{text}", driver=driver)
            driver_wait_until(driver, EC.number_of_windows_to_be(2))
            switch_to_new_window(driver, original_window)
            log.log_info(f"打开酷站 {text} 成功", driver=driver)
            result = proxy.har
            judge_result = judge(snode_info.page_click.value, tp, w_info.kz.value, text, result, scene_info.step9.value)
            if judge_result:
                log.log_pass("酷站点击上报成功", driver=driver)
            else:
                log.log_error("酷站点击上报失败")

        # 场景十：搜索框右侧轮播点击上报snode=1163---pass
        with driver_step("step10: 搜索框右侧轮播点击上报", driver, original_window):
            proxy.new_har(proxy_trace_url)
            # 点击搜索框右侧轮播
            xpath = '//*[@id="wrapper"]//ul[@class="hotwords"]/li/a'
            item_list = driver.find_elements_by_xpath(xpath)
            assert item_list, "获取搜索框右侧轮播数据失败"
            item = random.choice(item_list)
            cid = item.get_attribute("cid")
            # 等待轮播元素可点击时再进行点击
            driver_wait_until(driver, EC.element_to_be_clickable((By.XPATH, f'{xpath}[@cid="{cid}"]')))
            text = item.text
            driver_click(driver, element=item)
            log.log_info(f"点击搜索框右侧轮播：{text}", driver=driver)
            driver_wait_until(driver, EC.number_of_windows_to_be(2))
            switch_to_new_window(driver, original_window)
            log.log_info(f"打开搜索框右侧轮播 {text} 成功", driver=driver)
            result = proxy.har
            judge_result = judge(snode_info.page_click.value, tp, w_info.sright.value, text, result, scene_info.step10.value)
            if judge_result:
                log.log_pass("搜索框右侧轮播点击上报成功", driver=driver)
            else:
                log.log_error("搜索框右侧轮播点击上报失败", driver=driver)

        # 场景十一：猜你喜欢点击上报snode=1163---pass
        with driver_step("step11: 猜你喜欢点击上报", driver, original_window):
            # 获取猜你喜欢数据
            xpath = '//*[@id="wrapper"]//div[@class="fav_box_content"]//div[@class="J_w_stats"]'
            wrapper_list = driver.find_elements_by_xpath(xpath)
            assert wrapper_list, "获取猜你喜欢数据失败"
            wrapper = random.choice(wrapper_list)
            wrapper_name = None
            item_list = []
            item = None
            while True:
                # 分栏元素不可见时点击最右侧下一页按钮
                if wrapper.get_attribute("style") == 'display: none;':
                    log.log_info("点击猜你喜欢下一页按钮")
                    driver_click(driver, xpath='//div[@class="fav_box_wrap"]//a[contains(@class, "page_change_next")]')
                    continue

                # 获取分栏名称
                if not wrapper_name:
                    wrapper_name = wrapper.find_element_by_class_name("title").text

                # 获取分栏元素
                if not item_list:
                    item_list = wrapper.find_elements_by_xpath(".//ul/li/a")
                    assert item_list, f"获取猜你喜欢 {wrapper_name} 分栏数据失败"
                    item = random.choice(item_list)

                # 分栏元素不可见时，点击换一换按钮
                if not item.is_displayed() or not item.is_enabled():
                    change_btn = wrapper.find_element_by_class_name("jq_cnxh_change")
                    if not change_btn.is_displayed() or not change_btn.is_enabled():
                        continue

                    driver_click(driver, element=change_btn)
                    log.log_info(f"点击猜你喜欢 {wrapper_name} 分栏中的换一换按钮")
                    time.sleep(0.5)
                    continue

                # 在最后一次点击操作之前重新拦截请求，避免判断出多次上报的问题
                proxy.new_har(proxy_trace_url)
                # 点击猜你喜欢分栏中的元素
                text = item.text
                driver_click(driver, element=item)
                log.log_info(f"点击猜你喜欢 {wrapper_name} 分栏中的：{text}", driver=driver)
                driver_wait_until(driver, EC.number_of_windows_to_be(2))
                switch_to_new_window(driver, original_window)
                log.log_info(f"打开猜你喜欢 {wrapper_name} 分栏中的：{text} 成功", driver=driver)
                break

            result = proxy.har
            judge_result = judge(snode_info.page_click.value, tp, w_info.cnxh.value, text, result, scene_info.step11.value)
            if judge_result:
                log.log_pass(f"{scene_info.step11.value}成功", driver=driver)
            else:
                log.log_error(f"{scene_info.step11.value}F失败")

        # 场景十二：信息流顶部新闻轮播点击上报snode=1163
        with driver_step("step12: 信息流顶部新闻轮播点击上报", driver, original_window):
            judge_info_element_exist_xpath = '//div[@class="m_infoflow_main"]/div[@w="xwdt"]//div[@class="swiper-slide-template on"]/ul/li'
            info_item_list = driver.find_elements_by_xpath(judge_info_element_exist_xpath)
            judge_picture_element_exist_xpath = '//div[@class="m_infoflow_banner"]//div[@class="swiper-slide on"]/a'
            picture_item_list = driver.find_elements_by_xpath(judge_picture_element_exist_xpath)
            judge_status = False
            if len(info_item_list) == 0:
                if len(picture_item_list) == 0:
                    log.log_pass("信息流顶部新闻轮播模块未正常展示，请检查后台配置或接口请求数据", driver=driver)
                else:
                    judge_status = True
            else:
                judge_status = True

            if judge_status:
                proxy.new_har(proxy_trace_url)
                # 获取信息流顶部新闻轮播数据
                xpath = '//div[contains(@class,"swiper-slide-template")]/ul[@class="right-content"]/li/a'
                item_list = driver.find_elements_by_xpath(xpath)
                # 信息流顶部新闻存在非轮播样式，多图构成
                if len(item_list) == 0:
                    xpath = '//div[@class="m_infoflow_banner"]//div[@class="swiper-slide on"]/a'
                    item_list = driver.find_elements_by_xpath(xpath)
                    assert item_list, "获取信息流顶部大图新闻信息数据失败"
                else:
                    assert item_list, "获取信息流顶部新闻轮播数据失败"
                    # TODO：避免获取的元素为新闻中台覆盖的新闻
                while True:
                    item = random.choice(item_list)
                    if item.get_attribute("cid") != None:
                        cid = item.get_attribute("cid")
                        break
                # 等待至元素可点击
                xpath_new = xpath + "[@cid=\"" + cid + "\"]"
                driver_wait_until(driver, EC.element_to_be_clickable((By.XPATH, xpath_new)), wait_seconds=20)
                text = item.find_element_by_xpath(f'./span[contains(@class,"swiper-slide-title")]').text
                driver_click(driver, element=item)
                log.log_info(f"点击信息流顶部新闻：{text}", driver=driver)
                driver_wait_until(driver, EC.number_of_windows_to_be(2))
                switch_to_new_window(driver, original_window)
                log.log_info(f"打开信息流顶部新闻：{text} 成功", driver=driver)
                result = proxy.har
                judge_result = judge(snode_info.page_click.value, tp, w_info.xwdt.value, text, result, scene_info.step12.value)
                if judge_result:
                    log.log_pass(f"{scene_info.step12.value}成功", driver=driver)
                else:
                    log.log_error(f"{scene_info.step12.value}失败")

        # 场景十三：信息流tab点击上报snode=1163---pass
        with driver_step("step13: 信息流tab点击上报", driver, original_window):
            proxy.new_har(proxy_trace_url)
            # 信息流tab点击上报
            xpath = '//*[@id="jq_tabs_outside"]//div[contains(@class, "ss_tabs")]/a'
            item_list = driver.find_elements_by_xpath(xpath)
            assert item_list, "获取信息流tab数据失败"
            item = random.choice(item_list)
            text = item.text
            driver_click(driver, element=item)
            log.log_info(f"点击信息流tab：{text}", driver=driver)
            result = proxy.har
            judge_result = judge(snode_info.page_click.value, tp, w_info.ftab.value, text, result, scene_info.step13.value)
            if judge_result:
                log.log_pass(f"{scene_info.step13.value}成功", driver=driver)
            else:
                log.log_error(f"{scene_info.step13.value}失败")

        # 场景十四：信息流列表点击上报snode=1163---pass
        with driver_step("step14: 信息流列表点击上报", driver, original_window):
            proxy.new_har(proxy_trace_url)
            # 信息流列表点击上报
            base_xpath = '//*[@id="wrapper"]//div[contains(@class, "info_flow")]//div[contains(@class, "newslist")]'
            log.log_info("等待信息流列表加载完成")
            driver_wait_until(driver, EC.presence_of_element_located((By.XPATH, f'{base_xpath}/*')))
            log.log_info("信息流列表加载完成")
            xpath = '//*[@class="newslist jq_newslist"]/a/dl/dd/h2'
            item_list = driver.find_elements_by_xpath(xpath)
            assert item_list, "获取信息流列表数据失败"
            item = random.choice(item_list)
            # 滚动到目标位置后点击
            ActionChains(driver).move_to_element(item).perform()
            time.sleep(0.5)
            text = item.text
            driver_click(driver, element=item)
            log.log_info(f"点击信息流列表：{text}", driver=driver)
            driver_wait_until(driver, EC.number_of_windows_to_be(2))
            switch_to_new_window(driver, original_window)
            log.log_info(f"打开信息流列表：{text} 成功", driver=driver)

            result = proxy.har
            judge_result = judge(snode_info.page_click.value, tp, w_info.feedlist.value, text, result, scene_info.step14.value)
            if judge_result:
                log.log_pass(f"{scene_info.step14.value}成功", driver=driver)
            else:
                log.log_error(f"{scene_info.step14.value}失败")

        # 场景十五：左侧精选点击上报snode=1163---pass
        with driver_step("step15: 左侧精选点击上报", driver, original_window):
            proxy.new_har(proxy_trace_url)

            xpath = '//*[@id="wrapper"]//div[@class="m_site_tool_wrap"]//ul[@class="site_list"]/li/div[@class="site_item"]/a[@cid]'
            item_list = driver.find_elements_by_xpath(xpath)
            assert item_list, "获取左侧精选数据失败"
            item = random.choice(item_list)
            # 滚动到目标位置后点击
            ActionChains(driver).move_to_element(item).perform()
            time.sleep(0.5)
            text = item.text
            driver_click(driver, element=item)
            log.log_info(f"点击左侧精选：{text}", driver=driver)
            driver_wait_until(driver, EC.number_of_windows_to_be(2))
            switch_to_new_window(driver, original_window)
            log.log_info(f"打开左侧精选：{text} 成功", driver=driver)

            result = proxy.har
            judge_result = judge(snode_info.page_click.value, tp, w_info.ksrk_2020.value, text, result, scene_info.step15.value)
            if judge_result:
                log.log_pass(f"{scene_info.step15.value}成功", driver=driver)
            else:
                log.log_error(f"{scene_info.step15.value}失败")

        # 场景十六：右侧游戏板块点击上报snode=1163---pass
        with driver_step("step16: 右侧游戏板块点击上报", driver, original_window):
            proxy.new_har(proxy_trace_url)
            base_xpath = '//*[@class="m_hot_rec_box_base m_rec_game no_bottom_border"]'
            tab_list = driver.find_elements_by_xpath(f'{base_xpath}//div[@class="rec_tabs-bar"]/a')
            assert tab_list, "获取右侧游戏板块tab数据失败"
            log.log_info("获取右侧游戏板块tab数据成功", driver=driver)
            # 随机选择一个tab，然后鼠标移动到该tab
            tab = random.choice(tab_list)
            # 滚动到右侧游戏板块tab，因为搜索栏会悬浮所以需要减去个偏移量
            driver.execute_script(f"window.scrollTo(0, {tab.location['y'] - 210});", tab)
            log.log_info(f"滚动到右侧游戏板块tab: {tab.text}")
            ActionChains(driver).move_to_element(tab).perform()
            log.log_info(f"鼠标移动到右侧游戏板块tab: {tab.text}")
            # 查找该tab下的游戏信息
            xpath = f'{base_xpath}//div[@class="rec_tabs_content"]/div[@class="tab_panel" and not(@style="display: none;")]//div[@class="game_sm_bl_pn"]/a'
            item_list = driver.find_elements_by_xpath(xpath)
            assert item_list, "获取右侧游戏板块数据失败"
            item = random.choice(item_list)
            # 滚动到目标位置后点击
            ActionChains(driver).move_to_element(item).perform()
            text = item.find_element_by_xpath("./div[2]/h2").text
            driver_click(driver, element=item)
            log.log_info(f"点击右侧游戏板块：{text}", driver=driver, shot_delay=2)
            driver_wait_until(driver, EC.number_of_windows_to_be(2))
            switch_to_new_window(driver, original_window)
            log.log_info(f"打开右侧游戏板块：{text} 成功", driver=driver)

            result = proxy.har
            judge_result = judge(snode_info.page_click.value, tp, w_info.ksrkyx.value, text, result, scene_info.step16.value)
            if judge_result:
                log.log_pass(f"{scene_info.step16.value}成功", driver=driver)
            else:
                log.log_error(f"{scene_info.step16.value}失败")

        # 场景十七：右侧热门板块点击上报snode=1163---pass
        with driver_step("step17: 右侧热门板块点击上报", driver, original_window):
            judge_element_exist_xpath = '//*[@id="m_hot_rec_main"]/div[contains(@class, "m_hot_rec_box_base m_rec_hot")]/div[3]/a'
            hot_item_list = driver.find_elements_by_xpath(judge_element_exist_xpath)
            if len(hot_item_list) == 0:
                log.log_pass("右侧热门板块未正常展示，请检查后台配置或接口请求数据", driver=driver)
            else:
                proxy.new_har(proxy_trace_url)
                # 获取右侧热门板块tab数据
                xpath = '//*[@id="m_hot_rec_main"]/div[contains(@class, "m_rec_hot")]/div[3]/a'
                item_list = driver.find_elements_by_xpath(xpath)
                assert item_list, "获取右侧热门板块数据失败"
                item = random.choice(item_list)
                text = item.find_element_by_xpath('./span[2]').text
                driver_click(driver, element=item)
                log.log_info(f"点击右侧热门板块：{text}", driver=driver, shot_delay=2)
                driver_wait_until(driver, EC.number_of_windows_to_be(2))
                switch_to_new_window(driver, original_window)
                log.log_info(f"打开右侧热门板块：{text} 成功", driver=driver)
                result = proxy.har
                judge_result = judge(snode_info.page_click.value, tp, w_info.zjltj.value, text, result, scene_info.step17.value)
                if judge_result:
                    log.log_pass(f"{scene_info.step17.value}成功", driver=driver)
                else:
                    log.log_error(f"{scene_info.step17.value}失败")


if __name__ == "__main__":
    # pytest.main(["-v", "-s", __file__])
    allure_attach_path = os.path.join("Outputs", "allure")
    pytest.main(["-v", "-s", __file__, '--alluredir=%s' % allure_attach_path])
    os.system("allure serve %s" % allure_attach_path)
