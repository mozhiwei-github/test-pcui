# _*_ coding:UTF-8 _*_
import os
import time
import win32api
import win32gui
import win32con
import win32print
from PIL import Image
from common import utils
from common.log import log
from common.tools.duba_tools import find_dubapath_by_reg
from common.tools.pdf_tools import find_jg_by_reg
from cv2 import cv2


# 获取极光视频转换器路径
def find_jg_vc_path():
    if find_jg_by_reg():
        return os.path.join(find_jg_by_reg(), 'fastvc.exe')
    else:
        return None


# 获取毒霸视频转换器路径
def find_db_vc_path():
    if find_dubapath_by_reg():
        return os.path.join(find_dubapath_by_reg(), "app", "fastvc", "fastvc.exe")
    else:
        return None


# 获取可牛视频转换器路径
def find_kn_vc_path():
    if find_kn_by_reg():
        return os.path.join(find_kn_by_reg(), 'fastvc.exe')
    else:
        return None


# 获取可牛视频转换器注册表路径
def find_kn_by_reg():
    reg_path = r"SOFTWARE\fastvc"
    reg_value = utils.query_reg_value(win32con.HKEY_CURRENT_USER, reg_path, "installpath")
    return reg_value


class CommonCaseVideo:
    db_video_path = find_db_vc_path()
    jg_video_path = find_jg_vc_path()
    kn_video_path = find_kn_vc_path()
    program_video_path = [kn_video_path, jg_video_path, db_video_path]
    type_name = {jg_video_path: '极光视频格式专家', db_video_path: '毒霸视频格式专家', kn_video_path: '可牛视频转换器'}
    all_format = ['MP4', 'MOV', 'MKV', 'AVI', 'WMV', 'M4V', 'MPG', 'VOB', 'WEBM', 'OGV', '3GP', 'FLV', 'F4V', 'SWF']

    # 图片资源
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    back_dir, base_dir_name = os.path.split(base_path)
    update_name_logo = os.path.join(back_dir, "convert", "PageShot", 'video_page', 'update_name_logo.png')
    video_seg = os.path.join(back_dir, "convert", "PageShot", 'video_page', 'video_seg.png')
    video_add_watermark = os.path.join(back_dir, "convert", "PageShot", 'video_page', 'video_add_watermark.png')
    video_clear_watermark = os.path.join(back_dir, "convert", "PageShot", 'video_page', 'video_clear_watermark.png')
    video_optimize_settings = os.path.join(back_dir, "convert", "PageShot", 'video_page', 'video_optimize_settings.png')
    video_crop = os.path.join(back_dir, "convert", "PageShot", 'video_page', 'video_crop.png')

    # 获取文件路径
    @staticmethod
    def get_conversion_process_path():
        program_path = ""
        for path in CommonCaseVideo.program_video_path:
            if path is None:
                continue
            if os.path.exists(path):
                program_path = path
                break
        return program_path

    # 根据文件夹路径，返回文件夹下所有文件后缀名
    @staticmethod
    def get_file_suffix(file_path):
        lists = []
        for root, dirs, files in os.walk(file_path):
            for file in files:
                lists.append(os.path.splitext(file)[1])
        return lists

    # 获取视频长度
    @staticmethod
    def get_video_duration(filename):
        cap = cv2.VideoCapture(filename)
        if cap.isOpened():
            rate = cap.get(5)
            frame_num = cap.get(7)
            duration = frame_num / rate
            return int(duration)
        return False

    # 获取文件夹下文件名，根据生成时间排序
    @staticmethod
    def get_file_name(filepath):
        if os.path.exists(filepath):
            lists = os.listdir(filepath)
            lists.sort(key=lambda x: os.path.getctime((filepath + "\\" + x)))
            return lists
        else:
            log.log_info("路径不存在")
            return False

    # 获取文件夹下文件数量
    @staticmethod
    def get_file_num_to_folder(folder_path):
        if os.path.exists(folder_path):
            file_name = os.listdir(folder_path)
            return len(file_name)

    # 获取屏幕缩放比例
    @staticmethod
    def get_scaling_ratio():
        hDC = win32gui.GetDC(0)
        # 获取屏幕原本真实的分辨率(横)
        w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
        # 获取缩放后的分辨率
        s_w = win32api.GetSystemMetrics(0)
        x = w / s_w
        if x == 1:
            return 1
        elif 1.25 >= x > 1:
            return 1.25
        elif 1.50 >= x > 1.25:
            return 1.5
        elif 1.75 >= x > 1.50:
            return 1.75
        elif 2 >= x > 1.75:
            return 2
        elif 2.25 >= x > 2:
            return 2.25
        else:
            return 1

    # 根据屏幕缩放比例，鼠标移动增大相对应的倍率
    @staticmethod
    def mouse_click(x=None, y=None):
        scaling_ratio = CommonCaseVideo.get_scaling_ratio()
        if not x is None and not y is None:
            utils.mouse_move(int(x / scaling_ratio), int(y / scaling_ratio))
            time.sleep(0.5)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    # 输入文件路径获取文件体积倍数
    @staticmethod
    def get_file_size_multiple(one_file_path, two_file_path):
        if os.path.exists(one_file_path) and os.path.exists(two_file_path):
            one_file_size = os.stat(one_file_path).st_size
            two_file_size = os.stat(two_file_path).st_size
            com_effect = float(int(two_file_size / 1024) / int(one_file_size / 1024))
            return round(com_effect, 2)
        return False

    # 让窗口跑到最前面
    @staticmethod
    def window_top(hwnd_title):
        hwnd_win = win32gui.FindWindow(None, hwnd_title)
        win32gui.SetWindowPos(hwnd_win, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
        utils.perform_sleep(1)

    # 转换成功判断方法
    @staticmethod
    def conversion_spend_time():
        wait_time = 0
        new_time = time.perf_counter()
        while True:
            utils.perform_sleep(1)
            if not utils.is_process_exists("ffmpeg.exe"):
                con_spend_time = time.perf_counter() - new_time
                return con_spend_time
            if wait_time == 600:
                log.log_error("视频转换失败！")
                return False
            wait_time += 1

    # 适配高缩放比例点击图片方法
    @staticmethod
    def click_by_pic(pic):
        find_result, pic_position = utils.find_element_by_pic(pic, sim=0.7)
        if find_result:
            CommonCaseVideo.mouse_click(pic_position[0], pic_position[1])
            log.log_info("鼠标点击:(%s,%s)" % (pic_position[0], pic_position[1]))
            utils.perform_sleep(1)
            return True
        return False

    # 修改名称
    @staticmethod
    def update_name():
        file_name = str(int(time.time()))
        CommonCaseVideo.click_by_pic(CommonCaseVideo.update_name_logo)
        for i in range(0, 20, 1):
            utils.keyboardInputByCode('backspace')
            time.sleep(0.01)
        utils.perform_sleep(0.5)
        utils.key_input(file_name)
        log.log_info("键盘输入：%s" % file_name)
        utils.keyboardInputEnter()
        utils.perform_sleep(1)
        return file_name

    # 获取视频文件第一帧
    @staticmethod
    def get_frame_of_video(video_path, img, frame_time=1000):
        utils.perform_sleep(1)
        path = os.path.join(img, str(int(time.time())))
        img_path = path + ".png"
        cap = cv2.VideoCapture(video_path)
        cap.set(cv2.CAP_PROP_POS_MSEC, frame_time - 1)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(img_path, frame)
        cap.release()
        return img_path

    # 水平翻转
    @staticmethod
    def flip_pic_level(origin_path, target_path):
        img_path = os.path.join(target_path, str(int(time.time()))) + ".png"
        utils.perform_sleep(1)
        origin_img = Image.open(origin_path)
        origin_img.transpose(Image.FLIP_LEFT_RIGHT).save(img_path)
        return img_path

    # 垂直翻转
    @staticmethod
    def flip_pic_vertical(origin_path, target_path):
        img_path = os.path.join(target_path, str(int(time.time()))) + ".png"
        utils.perform_sleep(1)
        origin_img = Image.open(origin_path)
        origin_img.transpose(Image.FLIP_TOP_BOTTOM).save(img_path)
        return img_path

    # 根据输入数值旋转图片
    @staticmethod
    def rotate_pic_by_value(sim, origin_path, target_path):
        par_list = {90: Image.ROTATE_90, 180: Image.ROTATE_180, 270: Image.ROTATE_270}
        utils.perform_sleep(1)
        img_path = os.path.join(target_path, str(int(time.time()))) + ".png"
        origin_img = Image.open(origin_path)
        origin_img.transpose(par_list.get(int(sim))).save(img_path)
        return img_path
