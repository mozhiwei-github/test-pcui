from common import utils
from common.basepage import BasePage, page_method_record
from common.log import log
from common.utils import Location
from duba.PageObjects.vip_page import vip_page

"""文档修复"""


class DocumentRepairPage(BasePage):
    def __init__(self, do_pre_open=True, page_desc=None, delay_sec=5):
        super().__init__(do_pre_open=do_pre_open, page_desc=page_desc, delay_sec=delay_sec)

        # 查找并关闭文档修复大师须知弹窗
        self.close_notice()

    def pre_open(self):
        # 从会员页进入文档修复页
        self.vp = vip_page()
        self.vp.file_fix_click()

    def page_confirm_close(self):
        # 关闭退出确认弹窗
        log.log_info("查找退出确认弹窗")
        if utils.find_element_by_pic(self.get_page_shot("prompt_tab_logo.png"), sim=0.9, retry=2, hwnd=self.hwnd)[0]:
            assert self.click_prompt_confirm_button(), "点击确定按钮（退出弹窗）失败"

    @page_method_record("点击确定按钮（退出弹窗）")
    def click_prompt_confirm_button(self):
        return utils.click_element_by_pic(self.get_page_shot("prompt_confirm_button.png"), hwnd=self.hwnd)

    @page_method_record("点击取消按钮（退出弹窗）")
    def click_prompt_cancel_button(self):
        return utils.click_element_by_pic(self.get_page_shot("prompt_cancel_button.png"), hwnd=self.hwnd)

    @page_method_record("点击用户头像")  # 未登录时会弹出快速登录弹窗
    def click_user_avatar_button(self):
        utils.mouse_click(self.position[0] + 592, self.position[1] + 26)
        utils.mouse_move(self.position[0] + 592, self.position[1] + 62)

    @page_method_record("点击立刻充值/查看更多权益按钮")
    def click_recharge_now_button(self):
        return utils.click_element_by_pics(
            [self.get_page_shot("recharge_now_button.png"), self.get_page_shot("show_more_rights_button.png")],
            sim=0.9, retry=2)

    @page_method_record("打开文档修复支付页")
    def open_recharge_page(self):
        # 点击用户头像
        self.click_user_avatar_button()
        # 点击立刻充值按钮
        assert self.click_recharge_now_button(), "点击立刻充值按钮失败"

    @page_method_record("查找并关闭文档修复大师须知")
    def close_notice(self):
        find_result, pos = utils.find_element_by_pic(self.get_page_shot("notice_tab_logo.png"), sim=0.8, hwnd=self.hwnd,
                                                     sim_no_reduce=True, location=Location.LEFT_UP.value)
        if find_result:
            utils.mouse_click(pos[0] + 398, pos[1] + 20)
            return True
        else:
            log.log_info("未找到文档修复大师须知弹窗")
        return False


if __name__ == '__main__':
    page = DocumentRepairPage()
    # page.open_recharge_page()
    # document_repair_vip_page = vip_kaitong_page(page_desc="文档修复支付", delay_sec=3)
