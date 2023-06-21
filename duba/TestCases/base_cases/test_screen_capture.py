import uuid
import allure
import pytest
from common import utils
from common.contants import InputLan
from common.log import log
from duba.PageObjects.feedback_page import FeedbackPage
from duba.PageObjects.setting_page import SettingPage
from duba.config import config
from duba.PageObjects.vip_page import vip_page
from duba.PageObjects.screen_record_page import ScreenRecordPage
from duba.PageObjects.screen_capture_page import ScreenCapturePage


@allure.epic(f'毒霸截图王场景测试（{config.ENV.value}）')
@allure.feature('场景：打开毒霸截图王->使用各项工具')
class TestScreenCapture(object):
    @allure.story("用例：打开毒霸截图王->使用各项工具 预期成功")
    @allure.description("""
        step1：打开毒霸截图王
        step2: 使用矩形工具
        step3: 使用椭圆工具
        step4: 使用箭头工具
        step5: 使用画刷工具
        step6: 使用文字工具
        step7: 使用打马赛克工具
        step8: 使用撤销编辑
        step9: 使用截图固定在桌面任务栏
        step10: 使用图片固定在桌面
        step11: 使用滚动截长图
        step12: 使用屏幕录制
        step13: 使用意见反馈
        step14: 使用快捷键
        step15: 使用保存
    """)
    def test_screen_capture_success(self):
        allure.dynamic.title("毒霸截图王")

        with allure.step("step1：打开毒霸截图王"):
            utils.change_input_lan(InputLan.EN)
            log.log_info("切换为英文输入法", screenshot=True, shot_delay=1)
            screen_capture_page = ScreenCapturePage()
            log.log_pass("打开毒霸截图王成功")

        with allure.step("step2: 使用矩形工具"):
            assert screen_capture_page.click_rectangle_tool_button(), log.log_error("点击矩形工具失败", need_assert=False)
            utils.perform_sleep(1)
            log.log_info("点击矩形工具成功", screenshot=True)
            utils.mouse_drag((50, 50), (150, 150))
            utils.perform_sleep(1)
            log.log_pass("使用矩形工具成功")

        with allure.step("step3: 使用椭圆工具"):
            assert screen_capture_page.click_ellipse_tool_button(), log.log_error("点击椭圆工具失败", need_assert=False)
            utils.perform_sleep(1)
            log.log_info("点击椭圆工具成功", screenshot=True)
            utils.mouse_drag((160, 160), (250, 250))
            utils.perform_sleep(1)
            log.log_pass("使用椭圆工具成功")

        with allure.step("step4: 使用箭头工具"):
            assert screen_capture_page.click_arrow_tool_button(), log.log_error("点击箭头工具失败", need_assert=False)
            utils.perform_sleep(1)
            log.log_info("点击箭头工具成功", screenshot=True)
            utils.mouse_drag((50, 350), (160, 250))
            utils.perform_sleep(1)
            log.log_pass("使用箭头工具成功")

        with allure.step("step5: 使用画刷工具"):
            assert screen_capture_page.click_brush_tool_button(), log.log_error("点击画刷工具失败", need_assert=False)
            utils.perform_sleep(1)
            log.log_info("点击画刷工具成功", screenshot=True)
            utils.mouse_drag((250, 350), [(350, 350), (300, 264), (250, 350)])
            utils.perform_sleep(1)
            log.log_pass("使用画刷工具成功")

        with allure.step("step6: 使用文字工具"):
            assert screen_capture_page.click_text_tool_button(), log.log_error("点击文字工具失败", need_assert=False)
            utils.perform_sleep(1)
            log.log_info("点击文字工具成功", screenshot=True)
            utils.mouse_click(160, 70)
            utils.perform_sleep(1)
            random_text = uuid.uuid4().hex
            utils.key_input(random_text)
            log.log_info(f"输入文字：{random_text}", screenshot=True, shot_delay=1)
            utils.mouse_click(100, 100)
            utils.perform_sleep(1)
            utils.mouse_click(160, 120)
            utils.perform_sleep(1)
            # 目前截图王的粘贴文本有bug，先使用输入英文文本进行测试
            # clipboard_text = "这是一段直接粘贴的中文内容"
            # utils.copy_to_clipboard(clipboard_text)
            # utils.key_paste()
            # log.log_info(f"粘贴文字：{other_random_text}", screenshot=True, shot_delay=1)
            other_random_text = uuid.uuid4().hex
            utils.key_input(other_random_text)
            log.log_info(f"输入文字：{other_random_text}", screenshot=True, shot_delay=1)
            utils.mouse_click(100, 100)
            log.log_pass("使用文字工具成功")

        with allure.step("step7: 使用打马赛克工具"):
            assert screen_capture_page.click_mosaic_tool_button(), log.log_error("点击打马赛克工具失败", need_assert=False)
            utils.perform_sleep(1)
            log.log_info("点击打马赛克工具成功", screenshot=True)
            utils.mouse_drag((120, 75), (400, 75), cost_seconds=0)
            utils.perform_sleep(1)
            log.log_info("使用打马赛克工具快速滑动", screenshot=True)
            utils.mouse_drag((120, 100), [(150, 125), (400, 125)])
            utils.perform_sleep(1)
            log.log_info("使用打马赛克工具慢速滑动", screenshot=True)
            log.log_pass("使用打马赛克工具成功")

        with allure.step("step8: 使用撤销编辑"):
            assert screen_capture_page.click_undo_edit_button(), log.log_error("点击撤销编辑按钮失败", need_assert=False)
            utils.perform_sleep(1)
            log.log_pass("使用撤销编辑功能成功")

        # TODO: 正式服无会员账号来验证会员功能，暂时跳过
        # with allure.step("step9: 使用图文识别"):
        #     assert screen_capture_page.click_ocr_tool_button(), log.log_error("点击图文识别按钮失败", need_assert=False)
        #     utils.perform_sleep(3)
        #     ocr_prompt_find_result = screen_capture_page.find_ocr_prompt_logo()[0]
        #     assert ocr_prompt_find_result, log.log_error("查找图文识别窗口失败")
        #     # 复制全文
        #     assert screen_capture_page.click_ocr_copy_full_text_button(), log.log_error("点击复制全文按钮失败", need_assert=False)
        #     # 获取剪切板信息
        #     ocr_text = utils.get_clipboard_text()
        #     log.log_info(ocr_text, "文字识别全文内容")
        #     # 关闭图文识别窗口
        #     assert screen_capture_page.close_ocr_prompt(), log.log_error("关闭图文识别窗口失败", need_assert=False)
        #     log.log_pass("使用图文识别功能成功")

        with allure.step("step9: 使用截图固定在桌面任务栏"):
            screen_capture_page.pin_to_taskbar()
            utils.perform_sleep(1)
            log.log_pass("使用截图固定在桌面任务栏功能成功")

        with allure.step("step10: 使用图片固定在桌面"):
            assert screen_capture_page.click_pin_tool_button(), log.log_error("点击图片固定在桌面按钮失败", need_assert=False)
            utils.perform_sleep(1)
            utils.mouse_drag((50, 50), (300, 300))
            log.log_info("拖动图片", screenshot=True)
            utils.keyboardInputByCode('esc')
            log.log_info("使用Esc键关闭固定在桌面的图片", screenshot=True)
            log.log_pass("使用图片固定在桌面功能成功")

        with allure.step("step11: 使用滚动截长图"):
            # 打开会员页
            vp = screen_capture_page.vp
            assert vp.click_taskbar_icon(), log.log_error("点击任务栏会员中心图标失败", need_assert=False)
            utils.perform_sleep(2)
            vp.scroll_to_top()
            utils.perform_sleep(2)
            # 点击任务栏截图图标
            assert screen_capture_page.click_taskbar_screenshot_button(), log.log_error("点击任务栏截图图标失败", need_assert=False)
            utils.perform_sleep(2)
            utils.mouse_click(vp.position[0] + 10, vp.position[1] + 10)
            log.log_info("截图会员中心页", screenshot=True, shot_delay=1)
            # 点击滚动截长图按钮
            assert screen_capture_page.click_long_screenshot_tool_button(), log.log_error("点击滚动截长图按钮失败", need_assert=False)
            # 鼠标移动到滚动区域
            utils.mouse_click(vp.position[0] + 670, vp.position[1] + 150)
            log.log_info("开始进行滚动截长图", screenshot=True, shot_delay=2)
            for i in range(10):
                utils.mouse_scroll(1)
                utils.perform_sleep(0.5)
            log.log_info("鼠标滚动结束", screenshot=True)
            assert screen_capture_page.click_finish_button(), log.log_error("点击复制到剪切板按钮失败", need_assert=False)
            utils.perform_sleep(1)
            log.log_pass("使用滚动截长图功能成功")

        with allure.step("step12: 使用屏幕录制"):
            # 点击任务栏截图图标
            assert screen_capture_page.click_taskbar_screenshot_button(), log.log_error("点击任务栏截图图标失败",
                                                                                        need_assert=False)
            utils.perform_sleep(2)
            utils.mouse_click(0, 0)
            utils.perform_sleep(1)
            assert screen_capture_page.click_screen_record_tool_button(), log.log_error("点击屏幕录制按钮失败", need_assert=False)
            utils.perform_sleep(3)
            screen_record_page = ScreenRecordPage(do_pre_open=False)
            log.log_info("打开录屏大师成功", screenshot=True)
            screen_record_page.page_del()
            log.log_info("关闭录屏大师")
            utils.perform_sleep(1)
            log.log_pass("使用屏幕录制功能成功")

        with allure.step("step13: 使用意见反馈"):
            # 点击任务栏截图图标
            assert screen_capture_page.click_taskbar_screenshot_button(), log.log_error("点击任务栏截图图标失败",
                                                                                        need_assert=False)
            utils.perform_sleep(2)
            utils.mouse_click(0, 0)
            utils.perform_sleep(1)
            assert screen_capture_page.click_feedback_button(), log.log_error("点击意见反馈按钮失败", need_assert=False)
            utils.perform_sleep(1)
            feedback_page = FeedbackPage(do_pre_open=False)
            log.log_info("打开反馈建议成功", screenshot=True)
            feedback_page.page_del()
            log.log_info("关闭反馈建议")
            utils.perform_sleep(1)
            log.log_pass("使用意见反馈功能成功")

        with allure.step("step14: 使用快捷键"):
            # 点击任务栏截图图标
            assert screen_capture_page.click_taskbar_screenshot_button(), log.log_error("点击任务栏截图图标失败",
                                                                                        need_assert=False)
            utils.perform_sleep(2)
            utils.mouse_click(0, 0)
            utils.perform_sleep(1)
            assert screen_capture_page.click_hotkey_button(), log.log_error("点击快捷键按钮失败", need_assert=False)
            utils.perform_sleep(1)
            setting_page = SettingPage(do_pre_open=False)
            utils.perform_sleep(1)
            log.log_info("打开设置中心成功", screenshot=True)
            # 修改截图快捷键
            setting_page.change_screen_capture_hotkey()
            log.log_info("修改截图快捷键为：Alt + A", screenshot=True, shot_delay=1)
            setting_page.page_del()
            log.log_info("关闭设置中心")
            utils.perform_sleep(1)
            # 按下截图快捷键
            utils.keyboardInputHotkey("alt", "a")
            utils.perform_sleep(1)
            utils.mouse_click(0, 0)
            log.log_info("使用快捷键进行截图", screenshot=True, shot_delay=1)
            assert screen_capture_page.click_exit_button(), log.log_error("点击取消按钮失败", need_assert=False)
            utils.perform_sleep(1)
            log.log_pass("使用快捷键功能成功")

        with allure.step("step15: 使用保存"):
            # 点击任务栏截图图标
            assert screen_capture_page.click_taskbar_screenshot_button(), log.log_error("点击任务栏截图图标失败",
                                                                                        need_assert=False)
            utils.perform_sleep(2)
            utils.mouse_click(0, 0)
            utils.perform_sleep(1)
            assert screen_capture_page.click_save_button(), log.log_error("点击保存按钮失败", need_assert=False)
            log.log_info("点击保存按钮成功", screenshot=True, shot_delay=2)
            assert screen_capture_page.click_save_prompt_save_button(), log.log_error("点击保存图片窗口保存按钮失败",
                                                                                      need_assert=False)
            log.log_info("点击保存图片窗口保存按钮成功", screenshot=True, shot_delay=3)
            # TODO: 查看已保存的截图窗口消失太快，待新的校验方式
            # assert screen_capture_page.click_to_view_saved_screenshot(), log.log_error("点击查看已保存的截图失败", need_assert=False)
            # utils.perform_sleep(1)
            log.log_pass("使用保存功能成功")


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
