import requests
import json
from common import utils
from common.log import log
from common.contants import ServerHost


class UnExpectWin_System(object):
    def __init__(self):
        utils.screenshot(utils.screen_temp_pic_name)
        self.img_screen = utils.screen_temp_pic_name

    def find_closepos_by_screen(self):
        file = open(self.img_screen, "rb")
        files = {"file_name": file}
        response = requests.request("post", f"{ServerHost.AUTO_TEST_CF.value}/interface/findunexpectwin", files=files)
        r = json.loads(response.content, encoding="utf-8")
        if r["ret"] == "success" and r["result"]["sid"] != 0:
            log.log_info("成功查找弹窗信息返回 " + str(r["result"]))
            return int(r["result"]["closepos_by_screen"][0]), int(r["result"]["closepos_by_screen"][1])
        elif r["ret"] == "success" and r["result"]["sid"] == 0:
            log.log_info("没有查到弹窗信息返回 " + str(r["result"]))
            return int(r["result"]["closepos_by_screen"][0]), int(r["result"]["closepos_by_screen"][1])
        elif r["ret"] == "failed":
            log.log_info("查找弹窗信息出错" + str(r))
            return None
        else:
            return None

    # 规避弹窗系统检测
    def unexpectwin_detect(self):
        unwinclosepos = None
        try:
            unwinclosepos = self.find_closepos_by_screen()
        except Exception as e:
            log.log_error(str(e), need_assert=False)

        if unwinclosepos and unwinclosepos != (0, 0):
            log.log_info("点击关闭弹窗关闭按钮坐标 " + str(unwinclosepos))
            utils.mouse_click(unwinclosepos)
            return True
        return False

    def find_closepos_by_screen_beta(self):
        file = open(self.img_screen, "rb")
        files = {"file_name": file}
        response = requests.request("post", f"{ServerHost.AUTO_TEST_CF.value}/interface/findunexpectwinbeta",
                                    files=files)
        r = json.loads(response.content, encoding="utf-8")
        if r["ret"] == "success" and r["result"]:
            log.log_info("成功查找弹窗信息返回 " + str(r["result"]))
            return int(r["result"][0]), int(r["result"][1])
        elif r["ret"] == "success" and not r["result"]:
            log.log_info("没有查到弹窗信息返回")
            return None
        elif r["ret"] == "failed":
            log.log_info("查找弹窗信息出错" + str(r))
            return None
        else:
            return None

    # 规避弹窗系统检测_beta,强制查找关闭位置。以靠最下方位置弹窗为最佳选择点。
    def unexpectwin_detect_beta(self):
        unwinclosepos = None
        try:
            unwinclosepos = self.find_closepos_by_screen_beta()
        except Exception as e:
            log.log_error(str(e), need_assert=False)

        if unwinclosepos and unwinclosepos != (0, 0):
            log.log_info("点击关闭弹窗关闭按钮坐标 " + str(unwinclosepos))
            utils.mouse_click(unwinclosepos)
            return True
        return False


if __name__ == '__main__':
    print(UnExpectWin_System().unexpectwin_detect())
