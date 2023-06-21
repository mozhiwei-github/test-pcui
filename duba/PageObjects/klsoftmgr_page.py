import atexit
import importlib
import os
from enum import Enum
from duba import utils
from common import utils, log
from common.contants import RogueSoftWareInformation
from common.file_process import FileOperation
from common.log import log
from common.basepage import BasePage, page_method_record
from common.samba import Samba
from common.tools import duba_tools
from common.tools.duba_tools import DubaFiles, \
    rename_and_recover_kpopcenter, restart_kxetray, find_dubapath_by_reg
from common.tools.magiccube_tools import get_magiccube_tools, decode_magiccube, \
    get_magicABT_value_by_section, get_magicRaw_value_by_section
from common.utils import perform_sleep, Location

"""软件卸载王页"""


# 共享目录相对地址
from duba.utils import add_test_mode, add_log_reg, check_vip_block, DubaFilePath

rogue_software_share_path = os.path.join("autotest", "清除王黑名单第一批软件")

# 下拉流氓软件安装包的目标路径
rogue_software_local_path = os.path.join("c:", "清除王黑名单第一批软件")

# 本地安装包路径
local_on_cloud_pdf_share_path = os.path.join("c:", "清除王黑名单第一批软件", "PDFOnCloud_setup.exe")
local_hei_note_share_path = os.path.join("c:", "清除王黑名单第一批软件", "heinote_v3.2.1.0_gw_001.exe")
local_elephant_note_share_path = os.path.join("c:", "清除王黑名单第一批软件", "ElephantNoteSetup.exe")
local_qq_music_share_path = os.path.join("c:", "清除王黑名单第一批软件", "QQMusicSetup.exe")


# kvipapp_setting.ini 相关section的列表
kvipapp_setting_section_list = [DubaFiles.SOFT_UNINS_MGR_NORMAL_POP.value, DubaFiles.SOFT_UNINS_MGR_WIN10_TOAST.value]

# kvipapp_setting.ini 右下角泡泡弹出模拟的option值
opt_value_list = [["tool_use_interval_days", "0"], ["diff_pop_same_product_avoid_days", '0'],
                  ["loop_minutes", "10"], ["start_minutes", "0"], ["min_size", "1"],
                  ["switch_on", "1"]]


class RogueSoftWareMsg(Enum):
    ONCLOUDPDF = "云上PDF"  # 云上pdf名称
    HEINOTE = "小黑笔记本"  # 小黑笔记本名称
    NENIUKANTU = "可牛看图"  # 可牛看图名称
    XIAOXIAN = "小象笔记本"  # 小象笔记本名称
    QQMUSCI = "QQ音乐"  # QQ音乐名称

    # 注意一下tab截图需要截取到卸载王界面的最右侧 （需要这个来定位点击防重装）
    # 并且tab图片的高度大概为 70个像素点（需要这个来定位自己的卸载为哪种卸载，参考函数：check_strong_uninstall_btn()）
    ONCLOUDPDFTABPNG = "on_cloud_pdf_tab.png"  # 云上pdf tab图片
    HEINOTETABPNG = "hei_note_tab.png"  # 小黑笔记本 tab图片
    KENIUKANTUPNG = "keniu_pic_tab.png"  # 可牛看图 tab图片
    XIAOXIANPNG = "elephant_note_tab.png"  # 小象笔记本 tab图片
    QQMUSCIPNG = "qq_music_tab.png"  # QQ音乐 tab图片


def pull_package():
    cr = Samba("10.12.36.203", "duba", "duba123")

    # 下拉流氓软件安装包
    cr.download_dir("TcSpace", rogue_software_share_path,
                    rogue_software_local_path)

    while True:
        ret1 = os.path.exists(local_on_cloud_pdf_share_path)  # 判断是否下拉云上pdf安装包成功
        ret2 = os.path.exists(local_hei_note_share_path)  # 判断是否下拉小黑笔记本安装包成功
        if ret1 and ret2:
            log.log_info("下拉文件成功，文件存在")
            break
    return ret1 and ret2


class OnCloudPdf(BasePage):
    # 云上PDF
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

    def install(self):
        if not os.path.exists(local_on_cloud_pdf_share_path):
            log.log_info("目录不存在:  c:\清除王黑名单第一批软件\PDFOnCloud_setup.exe ")
            return False
        utils.process_start(local_on_cloud_pdf_share_path, async_start=True)
        utils.click_element_by_pic(self.get_page_shot("on_cloud_pdf_install.png"))
        utils.perform_sleep(15)
        ret = utils.find_element_by_pic(self.get_page_shot("on_cloud_pdf_install_sucessful.png"))[0]
        if ret:
            utils.kill_process_by_name("PDFOnCloud_setup.exe")

    def check_strong_uninstall(self):
        # 目前lua脚本配置没更新云上pdf相关注册表，故无法删除，等待后续更新lua脚本后，再做删除注册表校验
        result1 = os.path.exists(RogueSoftWareInformation.IPDF_INSTALL_PATH.value)
        if result1:
            log.log_info("云上PDF执行卸载后，没有删除本地文件夹:" + RogueSoftWareInformation.IPDF_INSTALL_PATH.value)
            return False
        log.log_info("云上PDF执行卸载后，已删除本地文件夹:" + RogueSoftWareInformation.IPDF_INSTALL_PATH.value)
        return True


class HeiNote(BasePage):
    # 小黑笔记本
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

    def install(self):
        if not os.path.exists(local_hei_note_share_path):
            log.log_info("目录不存在:" + local_hei_note_share_path)
            return False
        utils.process_start(local_hei_note_share_path, async_start=True)
        utils.click_element_by_pic(self.get_page_shot("hei_note_install.png"))
        utils.perform_sleep(8)
        ret = utils.find_element_by_pic(self.get_page_shot("hei_note_install_sucessful.png"))[0]
        if ret:
            utils.kill_process_by_name("heinote_v3.2.1.0_gw_001.exe")


class ElephantNote(BasePage):
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

    def install(self):
        if not os.path.exists(local_elephant_note_share_path):
            log.log_info("目录不存在:" + local_elephant_note_share_path)
            return False
        utils.process_start(local_elephant_note_share_path, async_start=True)
        utils.perform_sleep(1)
        utils.click_element_by_pic(self.get_page_shot("defense_block_pop_allow.png"), retry=5)
        utils.perform_sleep(1)
        utils.click_element_by_pic(self.get_page_shot("elephant_note_install_confirm.png"), retry=5)
        utils.perform_sleep(1)
        utils.click_element_by_pic(self.get_page_shot("elephant_note_install_accept.png"))
        utils.perform_sleep(1)
        utils.click_element_by_pic(self.get_page_shot("elephant_note_install_next_step.png"))
        utils.perform_sleep(1)
        utils.click_element_by_pic(self.get_page_shot("elephant_note_install.png"))
        utils.perform_sleep(8)
        utils.click_element_by_pic(self.get_page_shot("elephant_note_install_finish.png"))


class QQMusic(BasePage):
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

    def install(self):
        if not os.path.exists(local_qq_music_share_path):
            log.log_info("目录不存在:" + local_qq_music_share_path)
            return False
        utils.process_start(local_qq_music_share_path, async_start=True)
        utils.click_element_by_pic(self.get_page_shot("qq_music_install_btn.png"))
        utils.perform_sleep(8)
        ret = utils.find_element_by_pic(self.get_page_shot("qq_music_install_successful.png"))[0]
        if ret:
            utils.kill_process_by_name("QQMusicSetup.exe")

    def uninstall(self):
        """"使用前需要调用SofewareUninstallPage的 click_normal_uninstall()"""
        perform_sleep(3)
        res = utils.is_process_exists("QQMusicUninst.exe")
        if not res:
            log.log_error("无调起qq音乐卸载程序")
            return False
        utils.click_element_by_pic(self.get_page_shot("qq_music_uninstall.png"))
        utils.click_element_by_pic(self.get_page_shot("qq_music_uninstall_btn.png"))
        for i in range(20):
            utils.perform_sleep(1)
            if not utils.is_process_exists("QQMusicUninst.exe"):
                log.log_info("qq音乐卸载进程已退出")
                return True
        log.log_info("qq音乐卸载进程超时退出，请检查进程情况：QQMusicUninst.exe")
        return True


class SofewareUninstallPage(BasePage):
    """
    1、界面校验
    2、弹泡校验
        1）推广泡
        2）回扫泡
        3）拦截安装泡泡
    3、基本的卸载检查，检查是否真的卸载了
    4、前置条件：安装软件       done
    5、本地引擎校验
    """

    def pre_open(self):
        add_test_mode()  # 注册表加了这个项，毒霸就不会清host.
        add_log_reg()  # 添加毒霸日志注册表，以便后续需要日志时能有详细输出
        # 卸载王暂无会员中心卡牌，故用进程启动方式打开卸载王exe，注意用例结束后要关闭进程
        dubapa = duba_tools.get_duba_file_path(DubaFiles.KL_SOFT_MGR_EXE)
        utils.process_start(dubapa, async_start=True)  # async_start = FALSE 则无法启动，为何？？

    @page_method_record("点击会员中心")
    def vip_center_click(self):
        """软件卸载王点击会员中心"""
        return utils.click_element_by_pics([self.get_page_shot("nor_center.png"), self.get_page_shot("vip_center.png"),
                                            self.get_page_shot("button_login.png")], retry=3,
                                           sim_no_reduce=True)

    def click_lately_install(self):
        """点击最近安装tab"""
        utils.click_element_by_pic(self.get_page_shot("lately_install.png"))

    def check_normal_uninstall_btn(self, soft_tab_png, soft_name):
        """
          检查指定软件是否为一键卸载
          @param soft_tab_png: 为指定软件的tab图片
          @param soft_name: 为指定软件的名称
        """
        nol_un_pos = \
            utils.find_elements_by_pic(self.get_page_shot("normal_uninstall_btn.png"), location=Location.LEFT_UP.value)[
                1]
        hei_note_pos = utils.find_element_by_pic(self.get_page_shot(soft_tab_png), location=Location.LEFT_UP.value)[1]
        ran_1 = hei_note_pos[1] + 4
        ran_2 = hei_note_pos[1] - 4
        for i in nol_un_pos:
            if ran_2 <= i[1] <= ran_1:
                log.log_info(soft_name + "的卸载为：一键卸载", screenshot=True)
                return True
            print(i)
        log.log_info(soft_name + "的卸载不为一键卸载，注意检查ksd.nlb（lua脚本）")
        return False

    def check_strong_uninstall_btn(self, soft_tab_png, soft_name):
        """
          检查指定软件是否为强力卸载
          @param soft_tab_png: 为指定软件的tab图片
          @param soft_name: 为指定软件的名称
        """
        st_un_pos = \
            utils.find_elements_by_pic(self.get_page_shot("strong_uninstall_btn.png"), location=Location.LEFT_UP.value)[
                1]
        soft_pos = utils.find_element_by_pic(self.get_page_shot(soft_tab_png), location=Location.LEFT_UP.value)[1]
        ran_1 = soft_pos[1] + 4
        ran_2 = soft_pos[1] - 4
        print(len(st_un_pos))
        for i in st_un_pos:
            if ran_2 <= i[1] <= ran_1:
                log.log_info(soft_name + "的卸载为：强力卸载", screenshot=True)
                return True
            print(i)
        log.log_info(soft_name + "的卸载不为强力卸载，注意检查ksd.nlb（lua脚本）")
        return False

    def select_reuninstall_btn(self, soft_tab_png):
        """
          勾选指定软件的防重装按钮
          @param soft_tab_png: 为指定软件的tab图片
        """
        log.log_info("勾选防重装按钮")
        soft_pos = utils.find_element_by_pic(self.get_page_shot(soft_tab_png), location=Location.LEFT_UP.value)[1]
        utils.mouse_click_int(soft_pos[0] + 708, soft_pos[1] + 35)
        self.check_antireinstall_tip()
        res = utils.find_element_by_pic(self.get_page_shot("selected_anti_reuninstall_btn.png"))[0]
        if not res:
            return False
        print(res)
        return True

    def click_strong_uninstall(self, soft_tab_png):
        """
          点击指定的软件的强力卸载（有动画）
          @param soft_tab_png: 为指定软件的tab图片
        """
        pos = utils.find_element_by_pic(self.get_page_shot(soft_tab_png), location=Location.LEFT_UP.value)[1]
        utils.mouse_click_int(pos[0] + 880, pos[1] + 35)
        utils.click_element_by_pic(self.get_page_shot("strong_uninstall_confirm_btn.png"))
        res = utils.find_element_by_pic(self.get_page_shot("strong_uninstall_tab.png"))

    def click_normal_uninstall(self, soft_tab_png):
        """
         点击指定的软件的一键卸载
          @param soft_tab_png: 为指定软件的tab图片
       """
        pos = utils.find_element_by_pic(self.get_page_shot(soft_tab_png), location=Location.LEFT_UP.value)[1]
        utils.mouse_click_int(pos[0] + 880, pos[1] + 35)

    def click_anti_reunnistall_list(self):
        """点击防重装列表"""
        # 以前出现过打开防重装列表后崩溃，原因：本地数据库读取错误
        utils.click_element_by_pic(self.get_page_shot("anti_reuninstall_list_btn.png"))
        res = utils.find_element_by_pic(self.get_page_shot("anti_reuninstall_list_tab.png"))
        if not res:
            log.log_info("找不到防重装列表的tab标识，请检查是否已经打开了防重装列表")
            return False
        log.log_info("防重装列表已打开", screenshot=True)
        return True

    def close_anti_reunnistall_list(self):
        """点击防重装列表关闭按钮"""
        utils.click_element_by_pic(self.get_page_shot("anti_reuninstall_list_close_btn.png"))

    def cancel_all_reunistall(self):
        """点击防重装列表全部取消按钮"""
        utils.click_element_by_pic(self.get_page_shot("cancel_all_reuninstall_btn.png"))

    def check_antireinstall_tip(self):
        """检查反重装提示窗口是否弹出"""
        res = utils.find_element_by_pic(self.get_page_shot("reinstall_tips_pop.png"))
        if not res:
            log.log_info("无找到反重装提示窗口")
            return False
        log.log_info("反重装提示窗口已展示", screenshot=True)
        utils.click_element_by_pic(self.get_page_shot("reinstall_tips_pop_confirm_btn.png"))
        return True

    def check_intercept_pop(self):
        """检查拦截安装泡泡是否弹出"""
        utils.perform_sleep(2)
        res = utils.find_element_by_pic(self.get_page_shot("intercept_pop.png"))
        if not res:
            log.log_info("拦截泡泡无弹出，或者超时弹出")
            return False
        res = utils.find_element_by_pic(self.get_page_shot("pop_duba_icon.png"))
        if not res:
            log.log_info("拦截泡泡icon不为毒霸的icon")
            return False
        log.log_info("拦截泡泡已经弹出", screenshot=True)
        perform_sleep(3)
        # 泡泡关闭按钮图片，和防重装列表关闭按钮同款：
        utils.click_element_by_pic(self.get_page_shot("anti_reuninstall_list_close_btn.png"))
        return True

    def check_retrace_pop(self):
        """检查回扫（笑脸）泡泡是否弹出"""
        utils.perform_sleep(2)
        res = utils.find_element_by_pic(self.get_page_shot("retrace_pop_tab.png"), sim_no_reduce=True)
        if not res:
            log.log_info("回扫泡泡无弹出，或者超时弹出")
            return False
        res = utils.find_element_by_pic(self.get_page_shot("pop_duba_icon.png"))
        if not res:
            log.log_info("回扫泡泡icon不为毒霸的icon")
            return False
        log.log_info("回扫泡泡已经弹出", screenshot=True)
        # 泡泡关闭按钮图片，和防重装列表关闭按钮同款：
        perform_sleep(3)
        res = utils.click_element_by_pic(self.get_page_shot("anti_reuninstall_list_close_btn.png"))
        if not res:
            log.log_error("回扫泡关闭失败")
            return False
        log.log_info("回扫泡已点击关闭，关闭成功")
        return True

    def check_local_engine(self, time, obj):
        """
        检查本地引擎是否生效（软件卸载王第三期功能）
        @param time: 魔方：KLOSTMGR_INSTALL_MONITOT_SCAN_MIN_LOOP_MINUTES  配置的等待时间：scan_min_loop_minute  默认：5min
        @param obj: 流氓软件类对象
        前置条件：
        1、安装软件（qq音乐为例）
        2、添加qq音乐到防重装列表、并卸载
        （3、魔方开关开启：KLSOFTMGR_SWITCH_ANTIREINSTALLSOFT_INSTALL_MONITOR）
        4、再次执行qq音乐安装
        """
        # 注意：使用前，需要将软件勾选防重装按钮，并且卸载
        utils.kill_process_by_id("klsoftmgr.exe")
        restart_kxetray()
        utils.perform_sleep(10)
        obj.install()
        utils.perform_sleep(time)
        re = utils.is_process_exists("klsoftmgr.exe")
        # 由于预扫进程启动后可能会迅速关闭，可能导致无法判断进程是否存在，故预扫进程是否启动不做为本地引擎生效的一个判断，故不return
        if re:
            re = utils.compare_cmdline("klsoftmgr.exe", target_pname="autoclean")
            if re:
                log.log_info("预扫进程已启动")
                # 无return
        res = self.check_retrace_pop()
        if not res:
            return False
        return True

    @rename_and_recover_kpopcenter
    def check_lower_right_corner_pop(self):
        """检查推广泡泡（右下角泡泡）是否弹出
        前置条件：
        1、可能被精灵环境规避，故需要屏蔽精灵注册表：HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\MyDrivers\DriverGenius ---AppPath
        2。屏蔽kpopcenter.dll 调用
        """
        utils.kill_process_by_name("klsoftmgr.exe")
        kvipapp_obj = FileOperation(DubaFilePath.kvipapp_setting_path)
        kvipapp_obj.del_section_by_list(kvipapp_setting_section_list)
        kvipapp_obj.add_section_by_list(kvipapp_setting_section_list)
        kvipapp_obj.set_options(DubaFiles.SOFT_UNINS_MGR_NORMAL_POP.value, opt_value_list)
        kvipapp_obj.set_option(DubaFiles.SOFT_UNINS_MGR_WIN10_TOAST.value, DubaFiles.SWITCH_ON.value, "0")
        pop_obj = FileOperation(DubaFilePath.popdata_file_path)
        pop_obj.del_section_by_list(["DefragPop", "last_show_time"])
        duba_tools.restart_kxetray()
        utils.perform_sleep(1)
        res = utils.is_process_exists("klsoftmgr.exe")
        # 由于预扫进程启动后可能会迅速关闭，可能导致无法判断进程是否存在，故预扫进程是否启动不做为本地引擎生效的一个判断，故不return
        if res:
            res = utils.compare_cmdline("klsoftmgr.exe", target_pname="silent")
            if res:
                log.log_info("预扫进程已启动")
                # 无return
        utils.perform_sleep(2)
        res = utils.find_element_by_pic(self.get_page_shot("lower_right_pop_tab.png"), sim_no_reduce=True)[0]
        if not res:
            log.log_info(
                "推广右下角泡泡无弹出, 请检查kxetray.ktrashmon.dll.log---SoftUninstallMgr_NormalPop，若无日志则查看kpopcenter.dll有无屏蔽")
            return False
        res = utils.find_element_by_pic(self.get_page_shot("lower_right_pop_icon.png"))[0]
        if not res:
            log.log_error("右下角推广泡泡不是毒霸icon")
            return False
        log.log_info("推广右下角泡泡已经弹出", screenshot=True)
        # 点击立即卸载
        utils.click_element_by_pic(self.get_page_shot("lower_right_pop_install_btn.png"))
        res = utils.find_element_by_pic(self.get_page_shot("tab_logo.png"))[0]
        if not res:
            log.log_error("点击立即卸载，无调起软件卸载王界面")
            return False
        log.log_info("点击立即卸载，已调起软件卸载王界面")
        return True

    def check_need_vip(self, normal_soft_tab_png, strong_soft_tab_png):
        """检查一键卸载和强力卸载的卡点"""
        get_magiccube_tools("duba")
        path = find_dubapath_by_reg()
        decode_magiccube(path, "duba")
        ret = get_magicABT_value_by_section("duba", "KLSOFTMGR_ABTEST_COMMON_UNINSTALL")  # 获取一键卸载和强力卸载的会员卡点开关魔方配置
        target = ret["custom"]
        if target == "需要Vip":
            self.click_normal_uninstall(normal_soft_tab_png)
            if check_vip_block():
                self.click_strong_uninstall(strong_soft_tab_png)
            # if check_vip_block():

    def test(self):
        ...


if __name__ == "__main__":
    time = get_magicRaw_value_by_section("duba", "KLOSTMGR_INSTALL_MONITOT_SCAN_MIN_LOOP_MINUTES",
                                         key_value_target_key="scan_min_loop_minute")
    print(time)
