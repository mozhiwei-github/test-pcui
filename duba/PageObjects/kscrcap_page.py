# --coding = 'utf-8' --
import os

from common import utils
from common.utils import perform_sleep
from duba.conftest import find_dubapath_by_reg

"""毒霸截图王"""


class Kscrap:
    def pre_open(self):
        # TODO：执行打开动作
        dubapath = find_dubapath_by_reg()
        scriptpath = os.getcwd()
        for i in range(1, 3, 1):
            os.chdir(dubapath)
            utils.process_start("kscrcap.exe", True)
            os.chdir(scriptpath)
            perform_sleep(2)
        os.chdir(scriptpath)


if __name__ == '__main__':
    for i in range(1, 200, 1):
        test = Kscrap()
        test.pre_open()
        utils.mouse_dclick(100, 100)
        perform_sleep(4)
        result = utils.is_process_exists("kscrcap.exe")
        print(i)
        if result:
            print("请检查进程是否卡死！！！！")
            break






