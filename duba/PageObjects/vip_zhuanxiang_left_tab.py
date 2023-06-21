#!/usr/bin/evn python
# --coding = 'utf-8' --
# vip专属左侧边栏
from common.basepage import BasePage, page_method_record
from common import utils


class pure_office_page(BasePage):
    @page_method_record("点击弹窗拦截")
    def pop_intercept_click(self):
        utils.mouse_click(self.position[0] + 48, self.position[1] + 75)

    @page_method_record("点击纯净无广告")
    def vip_pure_noad_click(self):
        utils.mouse_click(self.position[0] + 48, self.position[1] + 155)

    @page_method_record("点击浏览器修复")
    def browser_fix_click(self):
        utils.mouse_click(self.position[0] + 48, self.position[1] + 235)

    @page_method_record("点击c盘瘦身")
    def c_slimming_click(self):
        utils.mouse_click(self.position[0] + 48, self.position[1] + 315)

    @page_method_record("点击数据恢复")
    def data_recovery_click(self):
        utils.mouse_click(self.position[0] + 48, self.position[1] + 395)

    @page_method_record("点击自动清理加速")
    def auto_clean_upspeed_click(self):
        utils.mouse_click(self.position[0] + 48, self.position[1] + 475)


class document_weishi_page(BasePage):
    @page_method_record("点击文档保护")
    def document_protect_click(self):
        utils.mouse_click(self.position[0] + 48, self.position[1] + 75)

    @page_method_record("点击文档修复")
    def document_fix_click(self):
        utils.mouse_click(self.position[0] + 48, self.position[1] + 155)

    @page_method_record("点击文档加密")
    def file_encode_click(self):
        utils.mouse_click(self.position[0] + 48, self.position[1] + 235)

    @page_method_record("点击数据恢复")
    def data_recovery_click(self):
        utils.mouse_click(self.position[0] + 48, self.position[1] + 315)

    @page_method_record("点击PDF转WORD")
    def pdf_to_word_click(self):
        utils.mouse_click(self.position[0] + 48, self.position[1] + 395)


class private_weishi_page(BasePage):
    @page_method_record("点击隐私清理")
    def private_clean_click(self):
        utils.mouse_click(self.position[0] + 48, self.position[1] + 75)

    @page_method_record("点击无痕模式")
    def nomark_mode_click(self):
        utils.mouse_click(self.position[0] + 48, self.position[1] + 155)

    @page_method_record("点击隐私护盾")
    def private_hudun_click(self):
        utils.mouse_click(self.position[0] + 48, self.position[1] + 235)

    @page_method_record("点击文件夹加密")
    def dir_encode_click(self):
        utils.mouse_click(self.position[0] + 48, self.position[1] + 315)

    @page_method_record("点击文件粉碎")
    def file_destroy_click(self):
        utils.mouse_click(self.position[0] + 48, self.position[1] + 395)

    @page_method_record("点击右键菜单管理")
    def right_menu_manage_click(self):
        utils.mouse_click(self.position[0] + 48, self.position[1] + 395)
