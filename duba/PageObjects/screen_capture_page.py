# !/usr/bin/evn python
# --coding = 'utf-8' --
from common import utils
from common.log import log
from common.basepage import BasePage, page_method_record
from duba.PageObjects.vip_page import vip_page

"""毒霸截图王"""


class ScreenCapturePage(BasePage):
    def __init__(self, do_pre_open=True, page_desc=None, delay_sec=0):
        super().__init__(do_pre_open=do_pre_open, page_desc=page_desc, delay_sec=delay_sec)

        # 不使用窗口右上角坐标关闭页面
        self.enable_rect_pos_close = False

    def pre_open(self):
        self.vp = vip_page()
        self.vp.screen_capture_click()
        # 在鼠标点击一下，触发显示截图工具栏
        utils.mouse_click(0, 0)

    @page_method_record("点击矩形工具按钮")
    def click_rectangle_tool_button(self):
        return utils.click_element_by_pic(self.get_page_shot("rectangle_tool_button.png"), retry=3, sim_no_reduce=True)

    @page_method_record("点击椭圆工具按钮")
    def click_ellipse_tool_button(self):
        return utils.click_element_by_pic(self.get_page_shot("ellipse_tool_button.png"), retry=3, sim_no_reduce=True)

    @page_method_record("点击箭头工具按钮")
    def click_arrow_tool_button(self):
        return utils.click_element_by_pic(self.get_page_shot("arrow_tool_button.png"), retry=3, sim_no_reduce=True)

    @page_method_record("点击画刷工具按钮")
    def click_brush_tool_button(self):
        return utils.click_element_by_pic(self.get_page_shot("brush_tool_button.png"), retry=3, sim_no_reduce=True)

    @page_method_record("点击文字工具按钮")
    def click_text_tool_button(self):
        return utils.click_element_by_pic(self.get_page_shot("text_tool_button.png"), retry=3, sim_no_reduce=True)

    @page_method_record("点击马赛克工具按钮")
    def click_mosaic_tool_button(self):
        return utils.click_element_by_pic(self.get_page_shot("mosaic_tool_button.png"), retry=3, sim_no_reduce=True)

    @page_method_record("点击撤销编辑按钮")
    def click_undo_edit_button(self):
        return utils.click_element_by_pic(self.get_page_shot("undo_edit_button.png"), retry=3, sim_no_reduce=True)

    @page_method_record("点击滚动截长图按钮")
    def click_long_screenshot_tool_button(self):
        return utils.click_element_by_pics([self.get_page_shot("long_screenshot_tool_button.png"),
                                           self.get_page_shot("new_long_screenshot_tool_button.png")], retry=3,
                                           sim_no_reduce=True)

    @page_method_record("点击提取图片中的文字按钮")
    def click_ocr_tool_button(self):
        return utils.click_element_by_pic(self.get_page_shot("ocr_tool_button.png"), retry=3, sim_no_reduce=True)

    @page_method_record("点击屏幕录制按钮")
    def click_screen_record_tool_button(self):
        return utils.click_element_by_pic(self.get_page_shot("screen_record_tool_button.png"), retry=3,
                                          sim_no_reduce=True)

    @page_method_record("查找图文识别窗口标识")
    def find_ocr_prompt_logo(self):
        return utils.find_element_by_pic(self.get_page_shot("ocr_tab_logo.png"), retry=3, sim_no_reduce=True)

    @page_method_record("关闭图文识别窗口")
    def close_ocr_prompt(self):
        return utils.click_element_by_pic(self.get_page_shot("ocr_exit_button.png"), retry=3, sim_no_reduce=True)

    @page_method_record("点击复制全文按钮")
    def click_ocr_copy_full_text_button(self):
        return utils.click_element_by_pic(self.get_page_shot("ocr_copy_full_text_button.png"), retry=3,
                                          sim_no_reduce=True)

    @page_method_record("点击图片固定在桌面上按钮")
    def click_pin_tool_button(self):
        return utils.click_element_by_pic(self.get_page_shot("pin_tool_button.png"), retry=3, sim_no_reduce=True)

    @page_method_record("截图固定在桌面任务栏")
    def pin_to_taskbar(self):
        click_result = utils.click_element_by_pic(self.get_page_shot("pin_to_taskbar_button.png"), retry=3,
                                                  sim_no_reduce=True)
        assert click_result, log.log_error("点击截图固定在桌面任务栏按钮失败", need_assert=False)
        find_result = utils.find_element_by_pic(self.get_page_shot("pin_to_taskbar_success.png"), sim=0.7,
                                                sim_no_reduce=True)[0]
        assert find_result, log.log_error("截图固定在桌面任务栏提示信息校验失败", need_assert=False)

    @page_method_record("点击任务栏截图图标")
    def click_taskbar_screenshot_button(self):
        return utils.click_element_by_pic(self.get_page_shot("taskbar_screenshot_button.png"), retry=5,
                                          sim_no_reduce=True)

    @page_method_record("点击取消按钮")
    def click_exit_button(self):
        return utils.click_element_by_pic(self.get_page_shot("exit_button.png"), retry=3, sim_no_reduce=True)

    @page_method_record("点击复制到剪切板按钮")
    def click_finish_button(self):
        result, pos = utils.find_element_by_pic(self.get_page_shot("finish_button.png"), retry=3, sim_no_reduce=True)
        if not result:
            return False

        utils.mouse_click(pos)
        utils.perform_sleep(1)
        # 第一次点击完成按钮的时候无效，需要再点击一次
        utils.mouse_click(pos)

        return True

    @page_method_record("点击意见反馈按钮")
    def click_feedback_button(self):
        return utils.click_element_by_pic(self.get_page_shot("feedback_button.png"), retry=3, sim_no_reduce=True)

    @page_method_record("点击快捷键按钮")
    def click_hotkey_button(self):
        return utils.click_element_by_pic(self.get_page_shot("hotkey_button.png"), retry=3, sim_no_reduce=True)

    @page_method_record("点击保存按钮")
    def click_save_button(self):
        return utils.click_element_by_pic(self.get_page_shot("save_button.png"), retry=3, sim_no_reduce=True)

    @page_method_record("点击保存图片窗口保存按钮")
    def click_save_prompt_save_button(self):
        return utils.click_element_by_pic(self.get_page_shot("save_prompt_save_button.png"), retry=3,
                                          sim_no_reduce=True)

    @page_method_record("点击查看已保存的截图")
    def click_to_view_saved_screenshot(self):
        return utils.click_element_by_pic(self.get_page_shot("click_to_view_button.png"), retry=3, sim_no_reduce=True)


if __name__ == '__main__':
    page = ScreenCapturePage()
