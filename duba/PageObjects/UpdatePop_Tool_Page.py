from common import utils
from common.basepage import BasePage, page_method_record


class UpdatePopToolPage(BasePage):

    @page_method_record("点击升级泡弹出按钮")
    def click_show_updatepop_button(self):
        if not utils.click_element_by_pic(self.get_page_shot("show_updatepop_button.png")):
            return False
        return True

