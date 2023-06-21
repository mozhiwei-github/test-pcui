

# from common.utils import set_reg_value, is_reg_exist, query_reg_value
import os
from common.utils import get_hwnd_by_class
import win32gui
import time
from common import utils
from common.utils import find_element_by_pic,mouse_move,click_element_by_pic,mouse_click
# import time
# from duba.contants import Accelerate_module
# from common.tools.duba_tools import find_dubapath_by_reg
from common.utils import unicode
from common.file_process import FileOperation
from common.tools.duba_tools import find_dubapath_by_reg, deal_mainpage_close_pop
from duba.utils import close_duba_self_protecting
import configparser
from duba.contants import DubaVersion

if __name__ == '__main__':
    select_path = r"C:\project\dubatestpro\duba\PageShot\rubbish_clean_page\select_checkbox.png"
    result = utils.find_elements_by_pic(select_path)
    if result[0]:
        print("111111")
        for i in result[1]:
            utils.mouse_move(i[0], i[1])
            utils.perform_sleep(2)


            """
            is_deep_clean_button_exist()   True
            select_checkbox_operation()   True
            is_selected_window_exist()  True
            select_checkbox_operation()   True
            sure_button_click()    True
            deep_clean_button_click()   True
            is_return_button_exist()  True
            
            """










