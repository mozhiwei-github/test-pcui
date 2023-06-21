import os
from common import utils
from common.log import log


def get_pop_shot(pic_name):
    return os.path.join(os.getcwd(), "duba", "PopShot", pic_name)


def pop_method_record(info):
    def wrapper(func):
        def dec(self, *args, **kwargs):
            if self.tab_position:
                log.log_info(str(info))
                result = func(self, *args, **kwargs)
                return result

            log.log_error("failed " + str(info), need_assert=False)

        return dec

    return wrapper


class BasePop(object):
    def __init__(self):
        bk_hwnd = utils.get_hwnd_by_class("BkShadowWndClass", None)
        self.hwnd = utils.get_parent_hwnd(bk_hwnd)
        self.tab_position = None
        if self.hwnd and utils.get_pos_by_hwnd(bk_hwnd) != (0, 0, 0, 0):
            self.tab_position = utils.get_pos_by_hwnd(self.hwnd)

        self.pop_init = True
        if not self.tab_position:
            log.log_error("初始化泡泡失败，无法获取泡泡位置", need_assert=False)
            self.pop_init = False

    @pop_method_record("点击pop相对于左上角的某个位置")
    def click_func(self, dx, dy):
        utils.mouse_click(self.tab_position[0] + dx, self.tab_position[1] + dy)

    @pop_method_record("点击pop关闭按钮")
    def click_close(self):
        utils.mouse_click(self.tab_position[2] - 5, self.tab_position[1] + 5)

    @pop_method_record("点击防御pop中间阻止按钮")
    def click_defend_stop(self):
        self.click_func(425, 233)

    @pop_method_record("点击防黑墙pop中间阻止按钮")
    def click_defend_anti_stop(self):
        self.click_func(556, 363)


if __name__ == '__main__':
    defendpop = BasePop()
    print(defendpop.tab_position)
    defendpop.click_defend_stop()
