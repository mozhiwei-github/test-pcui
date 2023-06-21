# _*_ coding:UTF-8 _*_
import os
import sys
import time
import shutil
import psutil
import win32api
import win32gui
import win32con
import win32print
from win32com.client import Dispatch
from common import utils
from common.log import log
from common.samba import Samba
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import *
from pdfminer.pdfinterp import resolve1
import requests
from enum import unique, Enum
# import PyPDF2 as p
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed


# 获取毒霸注册表路径
def find_db_by_reg():
    """
    获取中注册表毒霸的ProgramPath值
    @return: 未找到时会返回 None
    """
    if os.path.exists(r"C:\Program Files (x86)"):
        regpath = r"SOFTWARE\WOW6432Node\kingsoft\antivirus"
        regvalue = utils.query_reg_value(win32con.HKEY_LOCAL_MACHINE, regpath, "ProgramPath")
    else:
        regpath = r"SOFTWARE\kingsoft\antivirus"
        regvalue = utils.query_reg_value(win32con.HKEY_LOCAL_MACHINE, regpath, "ProgramPath")
    return regvalue


def get_duba_tryno():
    """获取毒霸版本号"""
    duba_path = find_db_by_reg()
    if duba_path:
        with open(os.path.join(duba_path, "ressrc", "chs", "uplive.svr"), "r") as fr:
            while True:
                row_data = fr.readline()
                if row_data.find("TryNo") >= 0:
                    return row_data.replace("TryNo=", "").replace("\n", "")
                if not row_data:
                    return ""


# 获取极光注册表路径
def find_jg_by_reg():
    reg_path = r"SOFTWARE\fastpdf"
    reg_value = utils.query_reg_value(win32con.HKEY_CURRENT_USER, reg_path, "installpath")
    return reg_value


# 获取可牛注册表路径
def find_kn_by_reg():
    reg_path = r"SOFTWARE\keniupdf"
    reg_value = utils.query_reg_value(win32con.HKEY_CURRENT_USER, reg_path, "installpath")
    return reg_value


# 获取可牛转换器独立版注册表路径
def find_kncvt_by_reg():
    reg_path = r"SOFTWARE\keniupdfcvt"
    reg_value = utils.query_reg_value(win32con.HKEY_CURRENT_USER, reg_path, "installpath")
    return reg_value


# 获取精灵注册表路径
def find_dg_by_reg():
    if os.path.exists(r"C:\Program Files (x86)"):
        regpath = r"SOFTWARE\WOW6432Node\MyDrivers\DriverGenius"
        regvalue = utils.query_reg_value(win32con.HKEY_LOCAL_MACHINE, regpath, "AppPath")
    else:
        regpath = r"SOFTWARE\MyDrivers\DriverGenius"
        regvalue = utils.query_reg_value(win32con.HKEY_LOCAL_MACHINE, regpath, "AppPath")
    return regvalue


# 获取毒霸阅读器路径
def find_db_reader_path():
    if find_db_by_reg():
        return os.path.join(find_db_by_reg(), "app", "pdfreader", "dbpdf.exe")
    else:
        return None


# 获取精灵阅读器路径
def find_dg_reader_path():
    if find_dg_by_reg():
        return os.path.join(find_dg_by_reg(), "app", "pdfreader", "dgpdf.exe")
    else:
        return None


# 极光阅读器路径获取
def find_jg_reader_path():
    if find_jg_by_reg():
        return os.path.join(find_jg_by_reg(), 'fastpdf.exe')
    else:
        return None


# 获取coolnewpdf注册表路径
def find_cn_by_reg():
    reg_path = r"SOFTWARE\coolnewpdf"
    reg_value = utils.query_reg_value(win32con.HKEY_CURRENT_USER, reg_path, "installpath")
    return reg_value


# 获取pdfagile注册表路径
def find_agile_by_reg():
    reg_path = r"SOFTWARE\pdfagile"
    reg_value = utils.query_reg_value(win32con.HKEY_CURRENT_USER, reg_path, "installpath")
    return reg_value


# 获取52好压pdf注册表路径
def find_52zippdf_by_reg():
    reg_path = r"SOFTWARE\k52zippdf\pdfcvt"
    reg_value = utils.query_reg_value(win32con.HKEY_CURRENT_USER, reg_path, "install_dir")
    return reg_value


# 可牛pdf路径
def find_kn_reader_path():
    if find_kn_by_reg():
        return os.path.join(find_kn_by_reg(), 'fastpdf.exe')
    else:
        return None


# 可牛pdf转换器路径
def find_kncvt_reader_path():
    if find_kncvt_by_reg():
        return os.path.join(find_kncvt_by_reg(), 'pdfconverter.exe')
    else:
        return None


# 海外版路径
def find_cn_reader_path():
    if find_cn_by_reg():
        return os.path.join(find_cn_by_reg(), "coolnewpdf.exe")
    else:
        return None


# 海外版pdfagile路径
def find_agile_reader_path():
    if find_agile_by_reg():
        return os.path.join(find_agile_by_reg(), "pdfagile.exe")
    else:
        return None


# 获取图片编辑路径
def find_picture_edit_path():
    local_path = os.getenv('LOCALAPPDATA')
    if find_jg_by_reg():
        return os.path.join(find_jg_by_reg(), 'fastimageg.exe')
    elif find_db_by_reg():
        return os.path.join(find_db_by_reg(), "app", "pdfreader", "fastimageg.exe")
    elif find_dg_by_reg():
        return os.path.join(find_dg_by_reg(), "app", "pdfreader", "fastimageg.exe")
    elif os.path.exists(os.path.join(local_path, 'k52zippdf', 'pdf', 'fastpdf.exe')):
        return os.path.join(local_path, 'k52zippdf', 'pdf', 'fastimageg.exe')
    elif find_kn_by_reg():
        return os.path.join(find_kn_by_reg(), 'fastimageg.exe')
    elif os.path.exists(os.path.join(local_path, 'kfastpicpdf', 'pdf', 'fastpdf.exe')):
        return os.path.join(local_path, 'kfastpicpdf', 'pdf', 'fastimageg.exe')
    elif os.path.exists(os.path.join(local_path, 'kyqwppdf', 'pdf', 'fastpdf.exe')):
        return os.path.join(local_path, 'kyqwppdf', 'pdf', 'fastimageg.exe')
    else:
        # log.log_info("----当前环境未找到fastimageg.exe---")
        return None


# 获取全文翻译路径
def find_translation_path():
    if find_jg_by_reg():
        return os.path.join(find_jg_by_reg(), 'translation.exe')
    elif find_db_by_reg():
        return os.path.join(find_db_by_reg(), "app", "pdfreader", "translation.exe")
    else:
        return None


# 查询系统PDF默认打开方式
def find_pdf_open_by_default():
    reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.pdf\UserChoice"
    reg_value = utils.query_reg_value(win32con.HKEY_CURRENT_USER, reg_path, "ProgId")
    return reg_value


# 查询毒霸锁默认标记值
def find_db_lock_default():
    if os.path.exists(r"C:\Program Files (x86)"):
        reg_path = r"SOFTWARE\WOW6432Node\kingsoft\antivirus"
        reg_value = utils.query_reg_value(win32con.HKEY_LOCAL_MACHINE, reg_path, "is_authorization_pdf")
    else:
        reg_path = r"SOFTWARE\kingsoft\antivirus"
        reg_value = utils.query_reg_value(win32con.HKEY_LOCAL_MACHINE, reg_path, "is_authorization_pdf")
    return reg_value


# 查询精灵锁默认标记值
def find_dg_lock_default():
    if os.path.exists(r"C:\Program Files (x86)"):
        reg_path = r"SOFTWARE\WOW6432Node\MyDrivers\DriverGenius"
        reg_value = utils.query_reg_value(win32con.HKEY_LOCAL_MACHINE, reg_path, "is_authorization_pdf")
    else:
        reg_path = r"SOFTWARE\MyDrivers\DriverGenius"
        reg_value = utils.query_reg_value(win32con.HKEY_LOCAL_MACHINE, reg_path, "is_authorization_pdf")
    return reg_value


# 查询极光锁默认值
def find_jg_lock_default():
    reg_path = r"SOFTWARE\fastpdf"
    reg_value = utils.query_reg_value(win32con.HKEY_CURRENT_USER, reg_path, "default")
    return reg_value


# 查询可牛锁默认值
def find_kn_lock_default():
    reg_path = r"SOFTWARE\keniupdf"
    reg_value = utils.query_reg_value(win32con.HKEY_CURRENT_USER, reg_path, "default")
    return reg_value


# 查询海外版锁默认值
def find_hw_lock_default():
    reg_path = r"SOFTWARE\coolnewpdf"
    reg_value = utils.query_reg_value(win32con.HKEY_CURRENT_USER, reg_path, "default")
    return reg_value


# 查询海外版pdfagile锁默认值
def find_agile_lock_default():
    reg_path = r"SOFTWARE\pdfagile"
    reg_value = utils.query_reg_value(win32con.HKEY_CURRENT_USER, reg_path, "default")
    return reg_value


# 检查文件是否加密
def jm(f):
    pdf = open(f, 'rb')
    rd = p.PdfFileReader(pdf)
    print(rd)
    if rd.isEncrypted:
        print('%s文件有加密' % f)
    else:
        print('%s文件没有加密' % f)
    pdf.close()


# 判断工作电脑是否为win11
def IsWin11():
    if sys.getwindowsversion().build > 20000:
        return True
    else:
        return False


# 解析PDF获取文件内容
class ParsePDF(object):
    def __init__(self, file_path):
        # 文件路径
        self.file_path = file_path
        # 创建PDF资源管理器
        self.resource = PDFResourceManager()
        # 创建一个PDF参数分析器
        self.laparam = LAParams()
        # 创建聚合器
        self.device = PDFPageAggregator(self.resource, laparams=self.laparam)
        # 创建PDF页面解析器
        self.interpreter = PDFPageInterpreter(self.resource, self.device)

        # 初始化文档

    def init_file(self):
        fp = open(self.file_path, 'rb')  # 以二进制读模式打开
        # 用文件对象来创建一个pdf文档分析器
        praser = PDFParser(fp)
        # 创建一个PDF文档
        doc = PDFDocument()
        # 连接分析器 与文档对象
        praser.set_document(doc)
        doc.set_parser(praser)
        fp.close()
        return doc

    # 是否加密
    def is_encrypt(self):
        doc = self.init_file()
        return doc.encryption

    # 判断加密状态
    def is_encrypting(self):
        try:
            self.init_file()
            log.log_info("当前文档为非加密状态")
            return True
        except:
            log.log_info("当前文档为加密状态")
            return False

    # 获取文档页数
    def get_page_num(self):
        doc = self.init_file()
        return resolve1(doc.catalog['Pages'])['Count']

    # 获取所有页面内容
    def get_content(self):
        doc = self.init_file()
        all_page_text = []
        for page in doc.get_pages():
            self.interpreter.process_page(page)
            layout = self.device.get_result()
            text = ""
            for out in layout:
                if isinstance(out, LTTextBoxHorizontal):
                    text += str(out.get_text())
            all_page_text.append(text)
        return all_page_text

    # 获取所有页面旋转角度
    def get_rotate(self):
        doc = self.init_file()
        all_page_text = []
        for page in doc.get_pages():
            all_page_text.append(page.rotate)
        return all_page_text

    # 获取所有页面尺寸
    def get_page_size(self):
        doc = self.init_file()
        size_list = []
        for page in doc.get_pages():
            size = page.cropbox
            size_list.append((int(size[2] * 0.3528), int(size[3] * 0.3528)))
        return size_list


class Custom(object):
    OPEN_FILE = 0
    Save = 1
    PRINT_OUT = 2
    REVOKE = 3
    RESTORE = 4
    START_LOGO = 5
    Minimize = 6
    Windowing = 7
    Close = 8
    Converter_suspension = 9
    Collapse_Toolbar = 10
    Show_head_page = 11
    Previous_page = 12
    Next_page = 13
    Show_last_page = 14
    Reduce_Size = 15
    Add_Size = 16


class CommonCasePdf:
    local_path = os.getenv('LOCALAPPDATA')
    k52zip_pdf = os.path.join(local_path, 'k52zippdf', 'pdf', 'fastpdf.exe')
    kfastpic_pdf = os.path.join(local_path, 'kfastpicpdf', 'pdf', 'fastpdf.exe')
    kyqwp_pdf = os.path.join(local_path, 'kyqwppdf', 'pdf', 'fastpdf.exe')
    lbpdf = os.path.join(local_path, 'liebao', '8.0.0.21121', 'Module', 'liebaofastpdf', 'lbpdf.exe')
    jg_pdf = find_jg_reader_path()
    duba_pdf = find_db_reader_path()
    dg_pdf = find_dg_reader_path()
    hw_pdf = find_cn_reader_path()
    agile_pdf = find_agile_reader_path()
    kn_pdf = find_kn_reader_path()
    # 全文翻译路径
    translation = find_translation_path()
    # 阅读器子窗口名称
    process_name = ['dbpdf', 'dgpdf', 'fastpdf']
    # 阅读器exe名称
    all_reader_name = ['dbpdf.exe', 'dgpdf.exe', 'fastpdf.exe', 'coolnewpdf.exe', 'pdfagile.exe']
    # 所有阅读器路径(*注意：需要将毒霸阅读器放在最后)
    # cooperative_version_path = [jg_pdf]
    cooperative_version_path = [jg_pdf, dg_pdf, duba_pdf, kn_pdf, k52zip_pdf, kfastpic_pdf, kyqwp_pdf, lbpdf, hw_pdf,
                                agile_pdf]
    # 海外推广版本
    overseas_promotion_version = [agile_pdf, hw_pdf]
    # 无全文翻译的版本
    no_full_text_translation = [agile_pdf, hw_pdf, dg_pdf, k52zip_pdf, kfastpic_pdf, kyqwp_pdf, lbpdf, kn_pdf]
    # 全文翻译版本路径
    translation_version_path = [translation]
    # 会员中心，合作版与独立版均为同一个exe名称
    member_exe = {'fastpdf.exe': 'kvipgui.exe', 'dbpdf.exe': 'knewvip.exe', 'dgpdf.exe': 'kvipgui.exe',
                  'coolnewpdf.exe': 'vipgui.exe', 'pdfagile.exe': 'vipgui.exe'}
    # duba小渠道（存在可牛模板，页面元素索引发生变化故特殊处理）
    duba_small_channel = ["1509"]
    # 新建TAB支持渠道
    independent_edition = [jg_pdf, kn_pdf]
    # 开启右侧小极智能助手入口
    pdf_ai = [jg_pdf]
    # 图片编辑路径
    picture_edit = find_picture_edit_path()

    # 判断默认阅读器
    @staticmethod
    def judge_default_reader():
        reader_name = CommonCasePdf.get_reader_path()
        reg_value = find_pdf_open_by_default()
        if reader_name == CommonCasePdf.duba_pdf:
            return "dbpdf.exe.pdf" == reg_value
        elif reader_name == CommonCasePdf.dg_pdf:
            return "dgpdf.exe.pdf" == reg_value
        elif reader_name == CommonCasePdf.kn_pdf:
            return "keniupdf.exe.pdf" == reg_value
        elif reader_name == CommonCasePdf.hw_pdf:
            return "coolnewpdf.exe.pdf" == reg_value
        elif reader_name == CommonCasePdf.agile_pdf:
            return "pdfagile.exe.pdf" == reg_value
        else:
            return "fastpdf.exe.pdf" == reg_value

    # 判断更改篡改后，篡改标志是否一起更新
    @staticmethod
    def judge_snatch_mark(mark):
        reader_name = CommonCasePdf.get_reader_path()
        # 查询毒霸集成版篡改标记
        if reader_name == CommonCasePdf.duba_pdf:
            return find_db_lock_default() == mark
        # 查询精灵集成版篡改标记
        elif reader_name == CommonCasePdf.dg_pdf:
            return find_dg_lock_default() == mark
        # 查询极光独立版版篡改标记
        elif reader_name == CommonCasePdf.jg_pdf:
            return find_jg_lock_default() == mark
        # 查询可牛独立版篡改标记
        elif reader_name == CommonCasePdf.kn_pdf:
            return find_kn_lock_default() == mark
        # 查询海外版独立版篡改标记
        elif reader_name == CommonCasePdf.hw_pdf:
            return find_hw_lock_default() == mark
        # 海外版pdfagile篡改标记
        elif reader_name == CommonCasePdf.agile_pdf:
            return find_agile_lock_default() == mark
        # 其他合作版本暂不校验
        else:
            log.log_info("合作版阅读器不校验")
            return True

    # 模式键盘输入ctrl+w
    @staticmethod
    def keyboardInputCtrlW():
        log.log_info("键盘输入 ctrl + W")
        win32api.keybd_event(0x11, 0, 0, 0)
        win32api.keybd_event(0x57, 0, 0, 0)
        win32api.keybd_event(0x57, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(0x11, 0, win32con.KEYEVENTF_KEYUP, 0)
        utils.perform_sleep(1)

    # 模式键盘输入ctrl+s
    @staticmethod
    def keyboardInputCtrlS():
        log.log_info("键盘输入 ctrl + s,进行保存")
        win32api.keybd_event(0x11, 0, 0, 0)
        win32api.keybd_event(0x53, 0, 0, 0)
        win32api.keybd_event(0x53, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(0x11, 0, win32con.KEYEVENTF_KEYUP, 0)
        utils.perform_sleep(1)

    # 模式键盘输入ctrl+z
    @staticmethod
    def keyboardInputCtrlZ():
        log.log_info("键盘输入 ctrl + Z")
        win32api.keybd_event(0x11, 0, 0, 0)
        win32api.keybd_event(0x5A, 0, 0, 0)
        win32api.keybd_event(0x5A, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(0x11, 0, win32con.KEYEVENTF_KEYUP, 0)
        utils.perform_sleep(1)

    # 模拟键盘按delete
    @staticmethod
    def keyboard_delete():
        win32api.keybd_event(0x2E, 0, 0, 0)
        win32api.keybd_event(0x2E, 0, win32con.KEYEVENTF_KEYUP, 0)
        utils.perform_sleep(0.5)
        log.log_info("键盘按下delete键")

    # 获取阅读器路径
    @staticmethod
    def get_reader_path():
        for path in CommonCasePdf.cooperative_version_path:
            if path is None:
                continue
            if os.path.exists(path):
                return path
            if path == CommonCasePdf.duba_pdf:
                return path

    # 获取全文翻译路径
    @staticmethod
    def get_translation_path():
        for path in CommonCasePdf.translation_version_path:
            if path is None:
                continue
            if os.path.exists(path):
                return path
            if path == CommonCasePdf.duba_pdf:
                return path

    # 获取海外版本阅读器路径
    @staticmethod
    def get_reader_overseas():
        for path in CommonCasePdf.overseas_promotion_version:
            if path is None:
                continue
            if os.path.exists(path):
                return path

    # 获取图片编辑路径
    @staticmethod
    def get_picture_edit():
        for path in CommonCasePdf.overseas_promotion_version:
            if path is None:
                continue
            if os.path.exists(path):
                return path

    # 获取子窗口进程名
    @staticmethod
    def get_son_window_name():
        path = commoncasepdf.get_reader_path()
        for name in CommonCasePdf.process_name:
            if name in path:
                return name

    # 获取会员进程名
    @staticmethod
    def get_member_name():
        pdf_path = CommonCasePdf.get_reader_path()
        for exe_name in CommonCasePdf.all_reader_name:
            if exe_name in pdf_path:
                return CommonCasePdf.member_exe.get(exe_name)

    # 从共享网盘内拷贝文件夹到本地目录下
    @staticmethod
    def copy_file(root_path, folder_name, f_name="", judge_size=True):
        local_path = os.path.join(CommonCasePdf.find_desktop_by_reg(), folder_name)
        if os.path.exists(local_path):
            try:
                shutil.rmtree(local_path)
            except PermissionError:
                log.log_info("文件被程序占用中，无法删除")
                return True
        samba = Samba('10.12.36.203', 'duba', 'duba123')
        if f_name:
            samba.download_file('TcSpace', root_path, local_path, f_name)
        else:
            samba.download_dir('TcSpace', root_path, local_path)
        folder_path = os.path.join(CommonCasePdf.find_desktop_by_reg(), folder_name, f_name)
        file_size = (round(os.path.getsize(folder_path) / 1024))  # 获取文件大小，单位kb（download方法下载文件不存在会自动创建，故判断下载文件大小）
        if os.path.exists(folder_path):
            if judge_size and file_size > 0:
                log.log_info("拷贝文件成功！")
                return True
            else:
                log.log_info("拷贝文件成功！")
                return True
        else:
            log.log_error("拷贝文件失败，缺少目标文件无法执行功能检查！")
            return False

    # 从共享网盘内拷贝文件到本地目录下
    @staticmethod
    def copy_updatefile(root_path, folder_name, f_name):
        local_path = os.path.join(CommonCasePdf.find_desktop_by_reg(), folder_name)
        if os.path.exists(local_path):
            try:
                shutil.rmtree(local_path)
            except PermissionError:
                log.log_info("文件被程序占用中，无法删除")
                return True
        upfile = Samba('10.12.32.222', 'duba', '7w4P&4#i')
        upfile.download_file('dubarelease', root_path, local_path, f_name)
        folder_path = os.path.join(CommonCasePdf.find_desktop_by_reg(), folder_name, f_name)
        file_size = (round(os.path.getsize(folder_path) / 1024))  # 获取文件大小，单位kb（download方法下载文件不存在会自动创建，故判断下载文件大小）
        if os.path.exists(folder_path) and file_size > 0:
            log.log_info("拷贝文件成功！")
            return True
        else:
            log.log_error("拷贝文件失败，缺少目标文件无法执行功能检查！")
            return False

    # 获取桌面路径
    @staticmethod
    def find_desktop_by_reg():
        reg_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        reg_value = utils.query_reg_value(win32con.HKEY_CURRENT_USER, reg_path, "Desktop")
        return reg_value

    # 获取系统TEMP路径
    @staticmethod
    def find_temp_by_reg():
        return os.getenv('TEMP')

    # 获取当前文件路径
    @staticmethod
    def find_update_by_reg(filename, exename):
        reg_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        reg_value = utils.query_reg_value(win32con.HKEY_CURRENT_USER, reg_path, "Desktop")
        reg_updatepdf = os.path.join(reg_value, filename, exename)
        # reg_updatepdf =os.path.join(reg_value,"updatepdf","fastpdf.exe")
        return reg_updatepdf

    # 根据句柄获取窗口中心坐标
    @staticmethod
    def get_center_position(window_name):
        hld = win32gui.FindWindow(None, window_name)
        if hld != 0:
            left, top, right, bottom = win32gui.GetWindowRect(hld)
            x = int((left + right) / 2)
            y = int((top + bottom) / 2)
            return x, y
        return False

    # 右键点击方法
    @staticmethod
    def mouse_right_click(x=None, y=None):
        if not x is None and not y is None:
            utils.mouse_move(x, y)
            time.sleep(0.05)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
        utils.perform_sleep(1)

    # 鼠标绘制图形框
    @staticmethod
    def mouse_draw_graphics(x=None, y=None, ene_x=150, end_y=120):
        if not x is None and not y is None:
            x, y = int(x), int(y)
            utils.mouse_move(x, y)
            time.sleep(0.05)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            utils.perform_sleep(0.05)
            utils.mouse_move(x + ene_x, y + end_y)
            utils.perform_sleep(0.05)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            utils.perform_sleep(1)
            log.log_info("从(%s，%s)到(%s，%s)绘制图形框" % (x, y, x + ene_x, y + end_y))

    # 创建文件夹
    @staticmethod
    def create_folder(folder_name):
        folder_path = os.path.join(CommonCasePdf.find_desktop_by_reg(), folder_name)
        if os.path.exists(folder_path):
            CommonCasePdf.delete_folder(folder_path)
        os.mkdir(folder_path)
        return folder_path

    # 删除文件夹
    @staticmethod
    def delete_folder(folder_path):
        if os.path.exists(folder_path):
            utils.perform_sleep(1)
            try:
                shutil.rmtree(folder_path)
                log.log_info("删除文件夹: %s" % folder_path)
                return True
            except PermissionError:
                log.log_info("文件被程序占用中，无法删除")
                return
        log.log_info("文件路径不存在")
        return

    # 杀掉会员中心进程
    @staticmethod
    def kill_knewvip(member_name):
        if not utils.is_process_exists(member_name):
            log.log_error("未调起会员中心")
            return False
        os.system('taskkill /f /im %s' % member_name)
        utils.perform_sleep(1)
        if utils.is_process_exists(member_name):
            log.log_error("杀掉会员中心进程失败！")
            return False
        log.log_info("杀掉会员中心进程")
        return True

    # 获取文件版本号
    @staticmethod
    def get_version_via_com(file_path):
        parser = Dispatch("Scripting.FileSystemObject")
        version = parser.GetFileVersion(file_path)
        return version

    @staticmethod
    def is_version_greater(version1, version2):
        """判断版本号 version1 是否大于 version2,仅适用于版本号均为四段式的情况"""
        v1_list = [int(i) for i in version1.split('.')]
        v2_list = [int(i) for i in version2.split('.')]
        for i in range(len(v2_list)):
            if v1_list[i] > v2_list[i]:
                return True
            elif v1_list[i] < v2_list[i]:
                return False
        # 如果版本号相等，则返回True
        return True

    @staticmethod
    # 获取转换器版本号
    def get_convert_version():
        convert_path = CommonConvert.get_convert_path()
        process_path = os.path.join(convert_path, "pdfconverter.exe")
        ver = CommonCasePdf.get_version_via_com(process_path)
        return ver

    @staticmethod
    # 获取阅读器版本号
    def get_pdf_version():
        pdf_path = CommonCasePdf.get_reader_path()
        return CommonCasePdf.get_version_via_com(pdf_path)

    # 获取屏幕分辨率
    @staticmethod
    def get_screen_resolution():
        hDC = win32gui.GetDC(0)
        w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
        h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
        return h, w

    # 获取阅读器进程数
    @staticmethod
    def get_reader_process_num():
        path, process_name = os.path.split(CommonCasePdf.get_reader_path())
        process_num = 0
        for process in psutil.process_iter():
            process_info = process.as_dict(attrs=['pid', 'name'])
            if process_info['name'] == process_name:
                if "-worker=1" in psutil.Process(process.pid).cmdline():
                    continue
                process_num += 1
        return process_num

    # 等待进程自然结束
    @staticmethod
    def wait_process_quit(process_name, wait_time=300):
        while True:
            if not utils.is_process_exists(process_name):
                break
            time.sleep(1)
            wait_time -= 1
            if wait_time <= 0:
                os.system('taskkill /f /im %s' % process_name)
                log.log_info("%s进程退出超时，杀掉进程！")
                break

    @staticmethod
    # 读取海外版本
    def overseas_version_field():
        pdf_overseas = find_agile_by_reg()
        if pdf_overseas:
            with open(os.path.join(pdf_overseas, "data", "language.dat"), "r") as fr:
                while True:
                    row_data = fr.readline()
                    if row_data.find("language") >= 0:
                        row = int(row_data.replace("language=", "").replace("\n", ""))
                        return row
                    if not row_data:
                        return ""

    @staticmethod
    # 判断海外版language，若存在删除
    def delete_language_dat():
        dat_name = os.path.join(find_agile_by_reg(), "data", "language.dat")
        if os.path.exists(dat_name):
            try:
                os.remove(dat_name)
            except PermissionError:
                log.log_info("文件被程序占用中，无法删除")

    @staticmethod
    # 获取海外版按钮列表
    def get_button_list(dit: dict):
        ls = []
        value = dit
        for i in value.values():
            ls.append(i)
        return ls


# 比较str_a，str_b两个字符串是否相同
def comparison(str_a, str_b):
    """
    @param str_a:字符串a
    @param str_b:字符串b
    """
    ib = 0
    for ia in range(len(str_a)):
        if ord(str_a[ia:ia + 1]) - ord(str_b[ib:ib + 1]) == 0:
            ib = ib + 1
            if ib == len(str_b):
                log.log_info('两段字符串内容一致')
                return True
        else:
            log.log_error('{},\n {} 两段字符串内容不一致'.format(str_a, str_b))
            return False


# 将字符串转换为unicode
def string_to_unicode(str_o):
    """
    @param str_o:被转换字符串
    """
    str_unicode = ""
    for ia in range(len(str_o)):
        o = str(ord(str_o[ia:ia + 1]))
        str_unicode += o
    return str_unicode


# 根据进程命令行是否包含某个字段返回进程对应的pid
def get_pid_by_cmdline(process_name, line_value):
    """
    @param process_name: 进程名
    @param line_value: 命令行
    """
    for process in psutil.process_iter():
        process_info = process.as_dict(attrs=['pid', 'name'])
        if process_info['name'] == process_name:
            for line in psutil.Process(process.pid).cmdline():
                if line_value in line:
                    return process.pid
    return None


# 毒霸转换器
def find_db_convert_path():
    if find_db_by_reg():
        return os.path.join(find_db_by_reg(), "vipapp", "pdfconverter")
    else:
        return None


# 精灵转换器
def find_dg_convert_path():
    if find_dg_by_reg():
        return os.path.join(find_dg_by_reg(), "pdfconverter")
    else:
        return None


# 极光转换器
def find_jg_convert_path():
    if find_jg_by_reg():
        return find_jg_by_reg()
    else:
        return None


# 可牛转换器
def find_kn_convert_path():
    if find_kn_by_reg():
        return find_kn_by_reg()
    else:
        return None


# 可牛转换器独立版
def find_kncvt_convert_path():
    if find_kncvt_by_reg():
        return find_kncvt_by_reg()
    else:
        return None


# 海外转换器
def find_hw_convert_path():
    if find_cn_by_reg():
        return find_cn_by_reg()
    else:
        return None


# aglie转换器
def find_aglie_convert_path():
    if find_agile_by_reg():
        return find_agile_by_reg()
    else:
        return None


# 调用Tesseract-OCR接口，进行ocr识别
def ocr(image_path):
    """
    调用Tesseract-OCR接口，进行ocr识别
    @param image_path: 文件绝对路径
    @return:
    """
    ocr_url = 'http://10.12.168.233:5000/ocr'
    try:
        with open(image_path, 'rb') as image_file:
            files = {'image': image_file}
            response = requests.post(ocr_url, files=files, timeout=10)

            if response.status_code == 200:
                result = response.json()
                text = result.get('text', '')
                log.log_info('OCR Result:', text)
                return text
            else:
                log.log_info('OCR Request Failed，请求失败！')
    except requests.exceptions.Timeout:
        log.log_info('OCR Request Timed Out,请求超时！')
    except requests.exceptions.RequestException as e:
        log.log_info('OCR Request Error:', e)




class CommonConvert:
    local_path = os.getenv('LOCALAPPDATA')
    k52zip_pdf = os.path.join(local_path, 'k52zippdf', 'pdf')
    kfastpic_pdf = os.path.join(local_path, 'kfastpicpdf', 'pdf')
    kyqwp_pdf = os.path.join(local_path, 'kyqwppdf', 'pdf')
    db_convert = find_db_convert_path()
    dg_convert = find_dg_convert_path()
    jg_convert = find_jg_convert_path()
    hw_convert = find_hw_convert_path()
    agile_convert = find_aglie_convert_path()
    kn_convert = find_kn_convert_path()
    # 可牛PDF转换器独立版
    kncvt_convert = find_kncvt_convert_path()

    all_convert_path = [jg_convert, dg_convert,
                        db_convert, kn_convert, kncvt_convert, agile_convert, hw_convert, k52zip_pdf, kfastpic_pdf,
                        kyqwp_pdf]

    # 获取转换器路径
    @staticmethod
    def get_convert_path():
        convert_path = ""
        for path in CommonConvert.all_convert_path:
            if path is None:
                continue
            if os.path.exists(path):
                convert_path = path
                break
            if path == CommonConvert.db_convert:
                convert_path = path
        return convert_path


@unique
class overseas_version_language(Enum):
    overseas_de_field = 3


@unique
class SpecialVersionNumber(Enum):
    # 图转pdf2期弹窗版本
    Picture_to_PDF_2_pop_up_window = "2023.4.11.703"


commoncasepdf = CommonCasePdf()
convert = CommonConvert()
