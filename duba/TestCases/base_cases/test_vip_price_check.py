#!/usr/bin/evn python
# --coding = 'utf-8' --
import allure
import pytest
from common import utils
from common.log import log
from common.utils import perform_sleep
from duba.config import config
from duba.PageObjects.login_page import LoginPage
from duba.contants import PaySettingShow


@allure.epic(f"毒霸VIP会员页，非会员账号价格检查（{config.ENV.value}）")
@allure.feature("场景：老金山账号登录->点击各套餐读取二维码价格->读取各套餐价格->校验价格正确性")
class TestVipPrice(object):
    @allure.story('校验非会员套餐价格')
    def test_no_vip_price_check(self):
        allure.dynamic.description(
            '\t1.打开会员中心\n'
            '\t2.使用非会员账号登录\n'
            '\t3.逐个点击套餐并读取二维码中返回的价格\n'
            '\t4.屏幕识别各套餐中的价格数量\n'
            '\t5.校验二维码获取的价格与套餐中显示的是否一致\n'
        )
        allure.dynamic.title('校验非会员套餐价格')

        with allure.step("step1：打开主界面的会员中心"):
            lp = LoginPage()
            assert lp.open_result, log.log_error("点击用户头像失败", need_assert=False)

        with allure.step("step2：使用老金山账号登录"):
            assert lp.normal_user_login(), log.log_error("老金山账号登录失败", need_assert=False)

        with allure.step("step3：点击各套餐读取二维码价格"):
            # 判断是否使用优惠券
            is_use_youhui = False
            if utils.find_element_by_pic(lp.vp.get_page_shot("button_youhuiquan_use.png"), retry=2)[0]:
                is_use_youhui = True
                paycodes_price_list, under_price_list = lp.vp.get_each_paycodes_price(tool="优惠券")
            elif utils.find_element_by_pic(lp.vp.get_page_shot("button_select_computer_1.png"), retry=2)[0]:
                paycodes_price_list, under_price_list = lp.vp.get_each_paycodes_price(tool="家庭版1台")
            else:
                paycodes_price_list, under_price_list = lp.vp.get_each_paycodes_price()
            log.log_info(paycodes_price_list, "paycodes_price_list")
            assert paycodes_price_list is not None, log.log_error("套餐二维码价格获取失败", need_assert=False)

        with allure.step("step4：读取屏幕各套餐显示价格"):
            if is_use_youhui:
                screen_price_list = under_price_list
            else:
                screen_price_list = lp.vp.get_price_on_screen()
            log.log_info(screen_price_list, "screen_price_list")
            utils.attach_screenshot(f"屏幕各套餐显示")
            assert screen_price_list is not None, log.log_error("屏幕各套餐显示价格获取失败", need_assert=False)

        with allure.step("step5：对比获取到的价格"):
            assert paycodes_price_list == screen_price_list, log.log_error("对比价格不一致", need_assert=False)
            log.log_pass("对比价格一致")
            perform_sleep(10)


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
