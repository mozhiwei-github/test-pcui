# !/usr/bin/evn python
# --coding = 'utf-8' --
import atexit
import configparser
import importlib
import os

import duba.utils
from common import utils
from common.log import log
from common.utils import perform_sleep
from common.basepage import BasePage
from common.tools import duba_tools
from common.tools.duli_tools import find_duli_c_slimming_by_reg
from duba.PageObjects.dg_page import DgPage

duba_reg = r"SOFTWARE\WOW6432Node\kingsoft\Antivirus"
dg_reg = r"SOFTWARE\WOW6432Node\MyDrivers\DriverGenius"


def set_duba_reg(value):
    utils.set_reg_value(regpath=duba_reg, keyname="ProgramPath", value=value)


def set_dg_reg(value):
    utils.set_reg_value(regpath=dg_reg, keyname="AppPath", value=value)


def get_path():
    product_path = find_duli_c_slimming_by_reg()
    return product_path


popdata_file_path = os.path.join(get_path(), "data", "popdata.ini")
kvipapp_setting_file_path = os.path.join(get_path(), "data", "kvipapp_setting.ini")
vippopcfg_file_path = os.path.join(get_path(), "data", "vippopcfg.ini")
ksyscfg_file_path = os.path.join(get_path(), "data", "ksyscfg.ini")

# 预扫泡kvipapp_setting.ini 中节点名字
pop_name = ["SoftUninstallMgr_NormalPop",
            "privacy",
            "DefragPop",
            "trashclean_prescan_pop",
            "sysslim_pop"
            ]

pop_pic_name = {"碎片清理": "defrag_pre_swept_pop.png",
                "垃圾清理": "ktrash_pre_swept_pop.png",
                "隐私清理": "privacy_pre_swept_pop.png",
                "软件卸载": "software_pre_swept_pop.png",
                "c盘瘦身白泡": "sysslim_pre_swept_pop.png",
                "c盘瘦身红泡": "sysslim_pre_swept_pop2.png"
                }


class CleanMasterPreSweptBubble(BasePage):

    # 去除页面初始化校验的初始化函数
    def __init__(self, do_pre_open=True, page_desc=None, delay_sec=0):
        perform_sleep(delay_sec)
        # 子类类名
        self.page_name = self.__class__.__name__
        # 子类文件路径
        self.filepath = importlib.import_module(self.__module__).__file__
        self.file_dir, self.filename_with_ext = os.path.split(self.filepath)
        # 子类文件名与扩展名
        self.filename, self.file_ext = os.path.splitext(self.filename_with_ext)
        # 关闭窗口允许执行变量，True为可执行，False为不可执行
        self.is_allow_close = True
        # 返回窗口允许执行变量，True为可执行，False为不可执行
        self.is_allow_back = True
        # 计算page_close的操作次数
        self.count_page_close = 0
        # 计算page_back的操作次数
        self.count_page_back = 0
        # 窗口句柄
        self.hwnd = None
        # 窗口对角坐标
        self.rect_pos = None
        # 启用尝试点击句柄窗口右上角坐标关闭
        self.enable_rect_pos_close = True

        class_resource_dict = self.get_init_by_name(self.file_dir, self.page_name)
        if class_resource_dict:
            self.page_desc = page_desc or class_resource_dict.get("page_desc", None)
            self.process_name = class_resource_dict.get("process_name", None)
            self.process_path = class_resource_dict.get("process_path", None)
            self.entry_pic = class_resource_dict.get("entry_pic", None)
            self.tab_pic = self.get_page_resource_pic(class_resource_dict.get("tab_pic", None))
            self.exit_pic = self.get_page_resource_pic(class_resource_dict.get("exit_pic", None))
            self.back_pic = self.get_page_resource_pic(class_resource_dict.get("back_pic", None))
            self.page_class = class_resource_dict.get("page_class", None)
            self.page_title = class_resource_dict.get("page_title", None)
        else:
            self.page_desc = page_desc
            self.process_name = None
            self.process_path = None
            self.entry_pic = None
            self.tab_pic = None
            self.exit_pic = None
            self.back_pic = None
            self.page_class = None
            self.page_title = None

        # 是否执行预打开操作
        self.do_pre_open = do_pre_open
        if self.do_pre_open:
            self.pre_open()

        log.log_debug(f"{self.page_desc} hwnd = {self.hwnd}")

        # 注册析构函数
        atexit.register(self.page_del)

    # 刷新kvipapp_popdata.ini的预扫泡节点,为修改做准备
    def refash_popdata(self, conf_obj):
        conf_obj.read(popdata_file_path, encoding='utf-8')
        conf_obj.remove_section("trashclean_prescan_pop")
        conf_obj.remove_section("SoftUninstallMgr_NormalPop")
        conf_obj.remove_section("privacy")
        conf_obj.remove_section("no_show_anymore")
        conf_obj.remove_section("DefragPop")
        conf_obj.remove_section("last_show_time")  # 去除 c盘瘦身弹出记录（c盘瘦身的kvipapp_setting的interval_days好像不起作用）
        """-------------------------------------"""
        conf_obj.add_section("no_show_anymore")
        conf_obj.add_section("DefragPop")

    # 刷新kvipapp_setting.ini的预扫泡节点,为修改做准备
    def refash_kvipapp_setting(self, conf_obj):
        conf_obj.read(kvipapp_setting_file_path, encoding='utf-8')
        conf_obj.remove_section("trashclean_prescan_pop")
        conf_obj.remove_section("privacy")
        conf_obj.remove_section("SoftUninstallMgr_NormalPop")
        conf_obj.remove_section("DefragPop")
        conf_obj.remove_section("sysslim_pop")
        """-------------------------------------"""
        conf_obj.add_section("trashclean_prescan_pop")
        conf_obj.add_section("privacy")
        conf_obj.add_section("SoftUninstallMgr_NormalPop")
        conf_obj.add_section("DefragPop")
        conf_obj.add_section("sysslim_pop")

    # 刷新vippopcfg.ini的预扫泡节点,为修改做准备
    def refash_vippopcfg(self, conf_obj):
        conf_obj.write(open(vippopcfg_file_path, "w", encoding='utf-8'))  # 修改文件的编码为 utf-8
        conf_obj.read(vippopcfg_file_path, encoding='utf-8')
        conf_obj.remove_section("sysslim_pop")
        """-------------------------------------"""
        conf_obj.add_section("sysslim_pop")

    def set_kvipapp_setting(self, conf_obj, pop_name):
        conf_obj.set(pop_name, "switch_on", "1")
        conf_obj.set(pop_name, "start_minutes", "0")
        conf_obj.set(pop_name, "loop_minutes", "100")
        conf_obj.set(pop_name, "scan_interval_days", "0")
        conf_obj.set(pop_name, "tool_use_interval_days", "0")
        conf_obj.set(pop_name, "interval_days", "0")
        conf_obj.set(pop_name, "diff_pop_same_product_avoid_days", "0")
        conf_obj.set(pop_name, "min_size ", "0")

    def set_vippopcfg(self, conf_obj, pop_name):
        conf_obj.set(pop_name, "debug", "0")
        conf_obj.set(pop_name, "pop_check_first_delaytime_minisecond", "0")
        conf_obj.set(pop_name, "pop_check_first_delaytime_minisecond_debug", "180000")
        conf_obj.set(pop_name, "pop_check_interval_minisecond", "180000")
        conf_obj.set(pop_name, "pop_check_interval_minisecond_debug", "180000")
        conf_obj.set(pop_name, "pop_check_interval_show_fail_minisecond", "180000")
        conf_obj.set(pop_name, "pop_check_interval_show_fail_minisecond_debug", "180000")

    # popdata.ini 调整
    def popdata_pop_config(self, defrag_switch, no_show_sys="1"):
        conf = configparser.ConfigParser()
        self.refash_popdata(conf_obj=conf)
        conf.set("no_show_anymore", "sys_slim_pop_2", no_show_sys)  # 关闭c盘瘦身2预扫泡
        conf.set("no_show_anymore", "sys_slim_pop", no_show_sys)  # 关闭c盘瘦身1预扫泡
        conf.set("DefragPop", "switch", defrag_switch)  # 此处逻辑是bug，应该改为,读kvipapp_setting.ini 的switch_on 。后续等待客户端改动

        with open(popdata_file_path, "w") as file:
            conf.write(file)

    # kvipapp_setting.ini 调整
    def kvipapp_setting_pop_cconfig(self, this_pop_name):
        conf = configparser.ConfigParser()
        self.refash_kvipapp_setting(conf_obj=conf)
        self.set_kvipapp_setting(conf_obj=conf, pop_name=this_pop_name)

        for popname in pop_name:
            if popname == this_pop_name:
                continue
            conf.set(popname, "switch_on", "0")  # 关闭其余预扫泡

        with open(kvipapp_setting_file_path, "w") as file:
            conf.write(file)

    # c盘瘦身预扫泡规避条件配置
    def vippopcfg_pop_config(self, this_pop_name):
        # vippopcfg.ini 调整  c盘瘦身用
        conf = configparser.ConfigParser()
        self.refash_vippopcfg(conf_obj=conf)
        self.set_vippopcfg(conf_obj=conf, pop_name=this_pop_name)

        with open(vippopcfg_file_path, "w") as file:
            conf.write(file)

    def ksyscfg_pop_config(self):
        # ksyscfg.ini 调整   c盘瘦身用
        conf = configparser.ConfigParser()
        conf.read(ksyscfg_file_path, encoding='utf-8')
        conf.remove_section("scan")  # 去除扫描系统盘时间规避    当天已经使用过C盘瘦身扫描，（写死在代码，1天间隔）

        with open(ksyscfg_file_path, "w") as file:
            conf.write(file)

    # 配置文件之外的限制条件：规避毒霸、精灵安装（修改注册表），规避会员（退出登录）
    def duba_install_reg_remove(self):
        # 屏蔽毒霸的文件目录，模拟毒霸未安装
        duba_reg = r"SOFTWARE\WOW6432Node\kingsoft\Antivirus"
        utils.remove_reg_value(regpath=duba_reg, value="ProgramPath")

    def dg_install_reg_remove(self):
        # 屏蔽精灵的文件目录，模拟精灵未安装
        dg_reg = r"SOFTWARE\WOW6432Node\MyDrivers\DriverGenius"
        utils.remove_reg_value(regpath=dg_reg, value="AppPath")

    # 删除毒霸和精灵的注册表安装标识
    def install_reg_remove(self):
        log.log_info("弹泡前检查精灵和毒霸的安装注册表是否被重写，有则删除")
        duba_reg_value = self.get_duba_install_reg()
        dg_reg_value = self.get_dg_install_reg()
        if duba_reg_value:
            self.duba_install_reg_remove()
        if dg_reg_value:
            self.dg_install_reg_remove()

    # 获取毒霸的文件目录，便于删除后恢复
    def get_duba_install_reg(self):
        ProgramPath_value = utils.query_reg_value(regpath=duba_reg, keyname="ProgramPath")
        return ProgramPath_value

    # 获取精灵的文件目录，便于删除后恢复
    def get_dg_install_reg(self):
        ProgramPath_value = utils.query_reg_value(regpath=dg_reg, keyname="AppPath")
        return ProgramPath_value

    def close_duba_protect(self):
        res = utils.query_reg_value(regpath=duba_reg, keyname="ProgramPath")
        if res is not None:
            duba.utils.close_duba_self_protecting()
        else:
            log.log_info("此环境没有毒霸安装目录注册表项")
            return

    def close_dg_protect(self):
        res = utils.query_reg_value(regpath=dg_reg, keyname="AppPath")
        if res is not None:
            dg = DgPage()
            dg.self_protecting_close()
        else:
            log.log_info("此环境没有精灵安装目录注册表项")
            return

            # 重启cmcore进行预扫逻辑

    def restart_cmcore(self):
        utils.kill_process_by_name("cmcore.exe")
        utils.process_start(process_path="net start cmcore", async_start=True)

    # 此处默认成功预扫，按照目前的配置调整，应该是会执行cmtray.exe的write cache预扫的
    # kfixstar弹泡专用
    def close_preswept_kfixstar_pop(self, name):
        for i in range(1, 300):
            utils.perform_sleep(1)
            print(i)
            result = utils.find_element_by_pic(self.get_page_shot(pop_pic_name[name]), retry=1,
                                               sim_no_reduce=True)[0]

            if result:
                log.log_pass(name + "预扫泡已弹出")
                perform_sleep(2)
                utils.keyboardInputAltF4()
                result = utils.find_element_by_pic(self.get_page_shot(pop_pic_name[name]), retry=1,
                                                   sim_no_reduce=True)[0]
                if not result:
                    log.log_info(name + "预扫泡已关闭", screenshot=True)
                return True
            if i == 120:
                self.install_reg_remove()
            if i == 299:
                result = utils.is_process_exists("cmtray.exe")
                if not result:
                    return False

                log.log_info("cmcore进程启动了10分钟左右，预扫进程依旧没退出，仍在预扫")
                log.log_info("准备手动删除预扫进程，模拟弹泡")
                utils.kill_process_by_id("cmtray.exe")
                result = utils.find_element_by_pic(self.get_page_shot(pop_pic_name[name]), retry=1,
                                                   sim_no_reduce=True)[0]
                if not result:
                    return False

                log.log_pass(name + "预扫泡已弹出")

                # result = utils.click_element_by_pics([self.get_page_shot("pre_swept_pop_close.png"),
                #                                       self.get_page_shot("pre_swept_pop_close2.png")],
                #                                      retry=5, sim_no_reduce=True)
                perform_sleep(2)
                utils.keyboardInputAltF4()
                result = utils.find_element_by_pic(self.get_page_shot(pop_pic_name[name]), retry=1,
                                                   sim_no_reduce=True)[0]

                if not result:
                    log.log_pass(name + "预扫泡已关闭")
                return True

            if i == 300:
                log.log_error(name + "预扫泡没弹出（请查看cmcore.dll.log）")
                return False

    # 此处默认成功预扫，按照目前的配置调整，应该是会执行cmtray.exe的write cache预扫的
    # kfixstar弹泡专用
    def close_preswept_sysslim_pop(self, name="c盘瘦身白泡", name2="c盘瘦身红泡"):
        for i in range(1, 300):
            utils.perform_sleep(1)
            print(i)
            result = utils.find_element_by_pics([self.get_page_shot(pop_pic_name[name]),
                                                 self.get_page_shot(pop_pic_name[name2])], retry=1,
                                                sim_no_reduce=True)[0]

            if result:
                log.log_pass("c盘瘦身预扫泡已弹出")
                perform_sleep(2)
                utils.keyboardInputAltF4()
                result = utils.find_element_by_pics([self.get_page_shot(pop_pic_name[name]),
                                                     self.get_page_shot(pop_pic_name[name2])], retry=1,
                                                    sim_no_reduce=True)[0]
                if not result:
                    log.log_info("c盘瘦身预扫泡已关闭", screenshot=True)
                return True
            if i == 120:
                self.install_reg_remove()
            if i == 299:
                result = utils.is_process_exists("cmtray.exe")
                if not result:
                    return False

                log.log_info("cmcore进程启动了10分钟左右，预扫进程依旧没退出，仍在预扫")
                log.log_info("准备手动删除预扫进程，模拟弹泡")
                utils.kill_process_by_id("cmtray.exe")
                utils.perform_sleep(3)
                result = utils.find_element_by_pics([self.get_page_shot(pop_pic_name[name]),
                                                     self.get_page_shot(pop_pic_name[name2])], retry=1,
                                                    sim_no_reduce=True)[0]

                if not result:
                    return False

                log.log_pass("c盘瘦身预扫泡已弹出")
                perform_sleep(2)
                utils.keyboardInputAltF4()
                result = utils.find_element_by_pics([self.get_page_shot(pop_pic_name[name]),
                                                     self.get_page_shot(pop_pic_name[name2])], retry=1,
                                                    sim_no_reduce=True)[0]
                if not result:
                    log.log_pass("c盘瘦身预扫泡已关闭")
                    return True

            if i == 300:
                log.log_error("c盘瘦身预扫泡没弹出（请查看cmcore.dll.log）")
                return False

    # def test(self):

    # 调起预扫命令行(检查不到cmcore是否能自动调起预扫)

    # 或者将文件直接替换(备选方案)

    # c盘瘦身预扫泡模拟（当天）已经弹泡

    # 垃圾清理预扫泡模拟（当天）已经弹泡

    # 碎片清理预扫泡模拟（当天）已经弹泡

    # 隐私清理预扫泡模拟（当天）已经弹泡

    # 打开日志开关

    # 读取日志

    # kplanetcache.ini修改   (预扫命令行记录)
    def modify_kplanetcache(self, param):
        file_name = os.path.join(get_path(), "data", "kplanetcache.ini")
        conf = configparser.ConfigParser()
        conf.read(file_name, encoding='utf-8')
        conf.remove_section("pure_vip_noad_pop")

        conf.add_section("pure_vip_noad_pop")

        conf.set("pure_vip_noad_pop", "param", param)
        with open(file_name, "w") as file:
            conf.write(file)

    # 从弹泡记录文件判断泡泡是否已经弹出
    def judge_popdata_file_path(self, pop_section):
        conf = configparser.ConfigParser()
        conf.read(popdata_file_path, encoding='utf-8')
        res = conf.get(pop_section, "last_show_time", fallback=False)
        if res:
            return True
        else:
            return False

    # def judge_pre_swept(self, process_name="cmtray.exe"):
    # res = utils.get_cmdline(process_name)
    # i=0
    # for i in :
    #     if res[0]==


from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello world!"


if __name__ == '__main__':
    app.run()
    # pre_swept = CleanMasterPreSweptBubble()
    # test.judge_pre_swept(process_name="cmcore.exe")
    # duba_reg_value = test.get_duba_install_reg()
    # dg_reg_value = test.get_dg_install_reg()

    # pre_swept.install_reg_remove()
    # pre_swept.popdata_pop_config(defrag_switch="0", no_show_sys="0")
    # pre_swept.kvipapp_setting_pop_cconfig(this_pop_name="sysslim_pop")
    # pre_swept.vippopcfg_pop_config(this_pop_name="sysslim_pop")
    # pre_swept.ksyscfg_pop_config()
    # pre_swept.restart_cmcore()
    # pre_swept.install_reg_remove()
    # pre_swept.popdata_pop_config(defrag_switch="0", no_show_sys="0")
    # pre_swept.kvipapp_setting_pop_cconfig(this_pop_name="sysslim_pop")
    # pre_swept.vippopcfg_pop_config(this_pop_name="sysslim_pop")
    # pre_swept.ksyscfg_pop_config()
    # pre_swept.restart_cmcore()
    # retpa = pre_swept.close_preswept_sysslim_pop()
    # assert retpa, "c盘瘦身预扫泡无弹出"
    # log.log_pass("c盘瘦身预扫泡弹出成功")
