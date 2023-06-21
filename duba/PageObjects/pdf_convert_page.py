#!/usr/bin/evn python
# --coding = 'utf-8' --
from common import utils
from common.basepage import BasePage, page_method_record
from common.log import log
from common.utils import Location, perform_sleep
from duba.PageObjects.vip_page import vip_page
from duba.PageObjects.unexpected_popup import UnexpectedPopup, UnexpectedPopupInfo

"""PDF转换页"""


class PDFConvertPage(BasePage):
    def __init__(self, do_pre_open=True, page_desc=None, delay_sec=0):
        super().__init__(do_pre_open=do_pre_open, page_desc=page_desc, delay_sec=delay_sec)

        perform_sleep(3)
        # 检查PDF红包的弹窗，如果有就直接关闭
        if UnexpectedPopup.popup_process(UnexpectedPopupInfo.PDF_RED_PACKET, hwnd=self.hwnd):
            perform_sleep(3)

    def pre_open(self):
        # 从会员页进入PDF转换页
        self.vp = vip_page()
        self.vp.pdfconvert_click()

    def page_confirm_close(self):
        # 首次关闭工具时，查找并关闭服务评分弹窗
        if self.count_page_close < 1 and \
                UnexpectedPopup.popup_process(UnexpectedPopupInfo.SERVICE_SCORE, hwnd=self.hwnd):
            perform_sleep(1)
            return

        log.log_info("检测退出提示弹窗（添加到桌面）")
        prompt_result, prompt_position = utils.find_element_by_pic(self.get_page_shot("prompt_tab_logo.png"), retry=2,
                                                                   sim=0.9, sim_no_reduce=True, hwnd=self.hwnd,
                                                                   location=Location.LEFT_UP.value)
        if prompt_result:
            utils.mouse_click(prompt_position[0] + 386, prompt_position[1] + 20)  # 点击右上角关闭
            log.log_info("关闭退出提示弹窗（添加到桌面）")

        log.log_info("检测退出提示弹窗（默认关联方式）")
        association_prompt_result, association_prompt_position = utils.find_element_by_pic(
            self.get_page_shot("association_prompt_tab_logo.png"), retry=2, sim=0.9, sim_no_reduce=True, hwnd=self.hwnd,
            location=Location.LEFT_UP.value)
        if association_prompt_result:
            utils.mouse_click(association_prompt_position[0] + 386, association_prompt_position[1] + 20)  # 点击右上角关闭
            log.log_info("关闭退出提示弹窗（默认关联方式）")

    @page_method_record("点击确认按钮（提示窗口）")
    def click_prompt_confirm_button(self):
        return utils.click_element_by_pic(self.get_page_shot("prompt_confirm_button.png"))

    @page_method_record("点击取消按钮（提示窗口）")
    def click_prompt_cancel_button(self):
        return utils.click_element_by_pic(self.get_page_shot("prompt_cancel_button.png"))

    @page_method_record("点击清空按钮（提示窗口）")
    def click_prompt_clear_button(self):
        return utils.click_element_by_pic(self.get_page_shot("prompt_clear_button.png"))

    @page_method_record("点击PDF转Word功能")
    def open_pdf_to_word(self):
        utils.mouse_click(self.position[0] + 172, self.position[1] + 24)

    @page_method_record("点击Word转PDF功能")
    def open_word_to_pdf(self):
        utils.mouse_click(self.position[0] + 286, self.position[1] + 24)

    @page_method_record("点击PDF操作功能")
    def open_pdf_operating(self):
        utils.mouse_click(self.position[0] + 398, self.position[1] + 24)

    @page_method_record("点击图片操作功能")
    def open_picture_operating(self):
        utils.mouse_click(self.position[0] + 512, self.position[1] + 24)

    @page_method_record("点击OCR图文识别功能")
    def open_ocr(self):
        utils.mouse_click(self.position[0] + 626, self.position[1] + 24)

    @page_method_record("点击转Word按钮")
    def click_pdf_to_word_button(self):
        utils.mouse_click(self.position[0] + 80, self.position[1] + 94)

    @page_method_record("点击转Excel按钮")
    def click_pdf_to_excel_button(self):
        utils.mouse_click(self.position[0] + 160, self.position[1] + 94)

    @page_method_record("点击转PPT按钮")
    def click_pdf_to_ppt_button(self):
        utils.mouse_click(self.position[0] + 240, self.position[1] + 94)

    @page_method_record("点击转图片按钮")
    def click_pdf_to_image_button(self):
        utils.mouse_click(self.position[0] + 320, self.position[1] + 94)

    @page_method_record("点击转TXT按钮")
    def click_pdf_to_txt_button(self):
        utils.mouse_click(self.position[0] + 400, self.position[1] + 94)

    @page_method_record("点击转CAD按钮")
    def click_pdf_to_cad_button(self):
        utils.mouse_click(self.position[0] + 480, self.position[1] + 94)

    @page_method_record("点击Word转PDF按钮")
    def click_word_to_pdf_button(self):
        utils.mouse_click(self.position[0] + 78, self.position[1] + 94)

    @page_method_record("点击Excel转PDF按钮")
    def click_excel_to_pdf_button(self):
        utils.mouse_click(self.position[0] + 158, self.position[1] + 94)

    @page_method_record("点击PPT转PDF按钮")
    def click_ppt_to_pdf_button(self):
        utils.mouse_click(self.position[0] + 238, self.position[1] + 94)

    @page_method_record("点击图片转PDF按钮")
    def click_image_to_pdf_button(self):
        utils.mouse_click(self.position[0] + 318, self.position[1] + 94)

    @page_method_record("点击CAD转PDF按钮")
    def click_cad_to_pdf_button(self):
        utils.mouse_click(self.position[0] + 398, self.position[1] + 94)

    @page_method_record("点击拆分PDF按钮")
    def click_split_pdf_button(self):
        utils.mouse_click(self.position[0] + 80, self.position[1] + 94)

    @page_method_record("点击合并PDF按钮")
    def click_merge_pdf_button(self):
        utils.mouse_click(self.position[0] + 160, self.position[1] + 94)

    @page_method_record("点击PDF加密按钮")
    def click_pdf_encrypt_button(self):
        utils.mouse_click(self.position[0] + 240, self.position[1] + 94)

    @page_method_record("点击提取页面按钮")
    def click_get_pdf_page_button(self):
        utils.mouse_click(self.position[0] + 320, self.position[1] + 94)

    @page_method_record("点击删除页面按钮")
    def click_remove_pdf_page_button(self):
        utils.mouse_click(self.position[0] + 400, self.position[1] + 94)

    @page_method_record("点击提取图片按钮")
    def click_get_pdf_image_button(self):
        utils.mouse_click(self.position[0] + 480, self.position[1] + 94)

    @page_method_record("点击添加水印按钮")
    def click_pdf_add_watermark_button(self):
        utils.mouse_click(self.position[0] + 560, self.position[1] + 94)

    @page_method_record("点击PDF压缩按钮")
    def click_pdf_compress_button(self):
        utils.mouse_click(self.position[0] + 640, self.position[1] + 94)

    @page_method_record("点击PDF转图片按钮（图片操作）")
    def click_image_operate_to_image_button(self):
        utils.mouse_click(self.position[0] + 80, self.position[1] + 94)

    @page_method_record("点击图片转PDF按钮（图片操作）")
    def click_image_operate_to_pdf_button(self):
        utils.mouse_click(self.position[0] + 160, self.position[1] + 94)

    @page_method_record("点击拖拽区域")
    def click_drag_area(self):
        utils.mouse_click(self.position[0] + 505, self.position[1] + 280)

    @page_method_record("点击开始按钮")  # 开始转换/开始拆分/开始合并...
    def click_start_button(self):
        utils.mouse_click(self.position[0] + 846, self.position[1] + 534)

    @page_method_record("点击添加文件按钮")
    def click_add_file_button(self):
        return utils.click_element_by_pic(self.get_page_shot("add_file_button.png"))

    @page_method_record("点击清空列表按钮")
    def click_clear_file_list_button(self):
        return utils.click_element_by_pic(self.get_page_shot("clear_file_list.png"))

    @page_method_record("点击打开按钮（添加文件窗口）")
    def click_add_file_open_button(self):
        return utils.click_element_by_pic(self.get_page_shot("add_file_open_button.png"))

    @page_method_record("点击取消按钮（添加文件窗口）")
    def click_add_file_cancel_button(self):
        return utils.click_element_by_pic(self.get_page_shot("add_file_cancel_button.png"))

    @page_method_record("点击登录按钮")
    def click_login_button(self):
        return utils.click_element_by_pic(self.get_page_shot("login_button.png"))


if __name__ == '__main__':
    page = PDFConvertPage()
