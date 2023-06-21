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
    if (len(url_list) == 1):
        if status_list[0] ==200:
            f = furl(url_list[0])
            log.log_info(f"{word}{snode_str}---存在该埋点上报且只上报一次")
            if tpstr == f.args['tp']:
                if w == f.args['w']:
                    if (text.replace(" ", "") == f.args['md5'].replace(" ", "")) or (
                            "statTime" in f.args['md5'].replace(" ", "")):
                        log.log_info(f"{word}{snode_str}---该埋点参数校验通过")
                        return True
                    else:
                        log.log_info(f"{word}{snode_str}---md5上报检验错误")
                        log.log_info(f"期望值为{text},实际值为{f.args['md5']}")
                        return False
                else:
                    log.log_info(f"{word}{snode_str}---w上报检验错误")
                    log.log_info(f"期望值为{w},实际值为{f.args['w']}")
                    return False
            else:
                log.log_info(f"{word}{snode_str}---tp上报检验错误")
                log.log_info(f"期望值为{tpstr},实际值为{f.args['tp']}")
                return False
        else:
            log.log_info(f"{word}{snode_str}---该埋点上报状态异常,状态为{status_list[0]}")
    elif len(url_list)==0:
        log.log_info(f"{word}{snode_str}---该埋点未上报")
        return False
    else:
        log.log_info(f"{word}{snode_str}---该埋点上报多次")
        return False

def handle(word, channel):
    tpdict = {
        '/index.html': 'index',
        '/tiyan21.html': 'tiyan21',
        '/tiyan4.html': 'tiyan4',
        '/tiyan4b.html': 'tiyan4b',
        '/tiyan3.html': 'tiyan3'
    }
    tp = tpdict[channel]
    word_snode_dict = {
        '导航页面展示上报': ['', 100],
        '搜索框输入内容点击搜索button上报': ['1', 1264],
        '搜索框选择下拉框内容点击上报': ['searchbox', 1264],
        '搜索框选择下拉框内容点击上报-AD': ['searchword', 1163],
        '搜索框选择下拉框内容点击上报-OTHERS': ['searchbox', 1264],
        '搜索框点击搜索框下方内容上报': ['rc', 1264],
        '搜索框点击搜索框下方内容上报-client': ['rc', 1163],
        '搜索框点击搜索框下方内容上报-ad': ['rctpfg', 1163],
        '搜索框点击搜索框下方内容上报-accurate': ['rc', 1264],
        '通栏快速入口点击上报': ['ksrk', 1163],
        '名站点击上报': ['mz', 1163],
        '酷站点击上报': ['kz', 1163],
        '搜索框右侧轮播点击上报': ['sright', 1163],
        '中间栏点击上报': ['zhongjianlan', 1163],
        '猜你喜欢点击上报': ['cnxh', 1163],
        '信息流顶部新闻轮播点击上报': ['xwdt', 1163],
        '信息流tab点击上报': ['ftab', 1163],
        '信息流列表点击上报': ['feedlist', 1163],
        '左侧精选点击上报': ['2020ksrk', 1163],
        '右侧游戏板块点击上报': ['ksrkyx', 1163],
        '右侧热门板块点击上报': ['zjltj', 1163],
        '搜索框联想词点击上报': ['1',1264]
    }
    w = word_snode_dict.get(word, None)[0]
    snode = word_snode_dict.get(word, None)[1]
    return tp, w, snode


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

        # 场景一：导航页面展示上报snode=100上报
        with driver_step("step1: 导航页面展示上报", driver):
            # proxy.new_har(proxy_trace_url)
            driver_get_reload(driver,base_url)
            #driver.get(base_url)
            proxy.new_har(proxy_trace_url)
            # 采用增加全局广告开关cookie的形式规避开屏广告
            if get_ad_sort(env,channel):
                set_cookie_value(driver,"global_ad_close", "close")
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
            word = '导航页面展示上报'
            message = handle(word, channel)
            judge_result = judge(message[2], message[0], message[1], text, result, word)
            if judge_result:
                log.log_pass("导航页面展示上报成功", driver=driver)
            else:
                log.log_error("导航页面展示上报失败", driver=driver)

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
                xpath = '//*[@id="mainSearchTip"]/div/table/tbody/tr'
            else:
                xpath = '//*[@id="mainSearchTip"]/div/div[2]/table/tbody/tr/td'
            item_list = driver.find_elements_by_xpath(xpath)
            assert item_list, "获取搜索框下拉列表数据失败"
            item = random.choice(item_list)
            # 搜索下拉框列表存在广告文字链
            if item.get_attribute("sctype") == 'accurate_baidu':
                word = '搜索框选择下拉框内容点击上报'
            elif item.get_attribute("sctype") == 'AD':
                word = '搜索框选择下拉框内容点击上报-AD'
            else:
                word = '搜索框选择下拉框内容点击上报-OTHERS'
            text = item.find_element_by_xpath('./td').get_attribute("word")
            # 点击搜索下拉框内容
            driver_click(driver, element=item)
            log.log_info(f"点击搜索框下拉列表关键词：{text}")
            # 等待搜索结果标签页打开
            driver_wait_until(driver, EC.number_of_windows_to_be(2))
            switch_to_new_window(driver, original_window)
            log.log_info(f"打开 {text} 搜索结果标签页成功", driver=driver)
            result = proxy.har
            message = handle(word, channel)
            judge_result = judge(message[2], message[0], message[1], text, result, word)
            if judge_result:
                log.log_pass("搜索框选择下拉框内容点击搜索上报成功", driver=driver)
            else:
                log.log_error("搜索框选择下拉框内容点击搜索上报失败", driver=driver)

if __name__ == "__main__":
    # pytest.main(["-v", "-s", __file__])
    allure_attach_path = os.path.join("Outputs", "allure")
    pytest.main(["-v", "-s", __file__, '--alluredir=%s' % allure_attach_path])
    os.system("allure serve %s" % allure_attach_path)
