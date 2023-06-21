#!/usr/bin/evn python
# --coding = 'utf-8' --
import allure
import pytest
from common import utils
from common.log import log
from common.utils import perform_sleep
from duba.config import config
from common.tools.duba_tools import clean_vipinfo
from duba.PageObjects.setting_page import SettingPage
from duba.PageObjects.vip_page import vip_page


@allure.epic(f"毒霸VIP会员页，游客账号价格检查（{config.ENV.value}）")
@allure.feature("场景：设置游客账号->点击各套餐读取二维码价格->读取各套餐价格->校验价格正确性")
class TestYoukePrice(object):
    @allure.story('校验非会员套餐价格')
    def test_no_vip_price_check(self):
        allure.dynamic.description(
            '\t1.设置游客账号\n'
            '\t2.打开会员中心\n'
            '\t3.逐个点击套餐并读取二维码中返回的价格\n'
            '\t4.屏幕识别各套餐中的价格数量\n'
            '\t5.校验二维码获取的价格与套餐中显示的是否一致\n'
        )
        allure.dynamic.title('校验游客套餐价格')

        with allure.step("step1：设置游客账号"):
            SettingPage_ = SettingPage()
            SettingPage_.self_protecting_close()
            assert SettingPage_.page_close(), log.log_error("关闭设置页失败", need_assert=False)
            res = clean_vipinfo()
            assert res, log.log_error("清除会员账号，恢复游客模式", need_assert=False)

        with allure.step("step2：打开会员中心"):
            vp = vip_page()
            assert vp.position is not None, log.log_error("打开会员页失败", need_assert=False)

        with allure.step("step3：点击各套餐读取二维码价格"):
            # 判断是否使用优惠券
            is_use_youhui = False
            if utils.find_element_by_pic(vp.get_page_shot("button_youhuiquan_use.png"), retry=2)[0]:
                is_use_youhui = True
            paycodes_price_list, under_price_list = vp.get_each_paycodes_price_youke()

            log.log_info(paycodes_price_list, "paycodes_price_list")
            assert paycodes_price_list is not None, log.log_error("套餐二维码价格获取失败", need_assert=False)

        with allure.step("step4：读取屏幕各套餐显示价格"):
            if is_use_youhui:
                screen_price_list = under_price_list
            else:
                screen_price_list = vp.get_price_on_screen()

            log.log_info(screen_price_list, "paycodes_price_list")
            utils.attach_screenshot("屏幕各套餐显示")
            assert screen_price_list is not None, log.log_error("屏幕各套餐显示价格获取失败", need_assert=False)

        with allure.step("step5：读取屏幕各套餐显示价格"):
            assert paycodes_price_list == screen_price_list, log.log_error("对比价格不一致", need_assert=False)
            log.log_pass("对比价格一致")
            perform_sleep(10)


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
