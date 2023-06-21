import os
from selenium.webdriver.common.by import By
from common import utils
from common.log import log
from common.wadlib import wadlib
from common.tools.pdf_tools import CommonCasePdf
from common.tools.video_tools import CommonCaseVideo


class VideoSegmentationFunc(object):

    def __init__(self, path):
        self.con = wadlib(app_path=path)
        self.process_path = CommonCaseVideo.get_conversion_process_path()
        self.file_path = os.path.join(CommonCasePdf.find_desktop_by_reg(), 'videofile', 'demo.mp4')
        self.output_path = CommonCasePdf.create_folder('seg_result')

    # 对半分割
    def split_in_half(self):
        CommonCaseVideo.window_top(self.con.driver.title)
        self.con.click_find_by_name("视频分割")
        self.con.click_find_by_name("添加文件")
        self.con.input_find_by_classname("Edit", self.file_path)
        self.con.click_find_by_name("打开(O)")
        self.con.click_find_by_name("自定义路径")
        self.con.click_find_by_name("浏览")
        self.con.input_find_by_classname('Edit', self.output_path)
        self.con.click_find_elements_by_property(By.NAME, '选择文件夹', 1)
        CommonCaseVideo.click_by_pic(CommonCaseVideo.video_seg)
        assert self.con.isElementPresent(By.NAME, "截取当前片段")
        self.con.click_element_by_list(By.CLASS_NAME, 'timeline::Ruler', By.CLASS_NAME, 'QFrame', 0, "进度条")
        end_x, end_y = utils.get_mouse_point()
        self.con.click_find_elements_by_property(By.CLASS_NAME, 'timeline::MyRightLabel', 0, "左拖拽")
        start_x, start_y = utils.get_mouse_point()
        CommonCasePdf.mouse_drag(start_x, start_y, end_x, end_y)
        self.con.click_find_by_name("截取当前片段")
        self.con.click_find_by_name("保存")
        file_name = CommonCaseVideo.update_name()
        self.con.click_find_by_name("全部分割")
        CommonCaseVideo.conversion_spend_time()
        con_file_num = CommonCaseVideo.get_file_name(self.output_path)
        assert file_name == con_file_num[-1].split(".")[0], "转换文件失败！"
        video_duration = CommonCaseVideo.get_video_duration(self.file_path)
        seg_video_duration = CommonCaseVideo.get_video_duration(os.path.join(self.output_path, con_file_num[-1]))
        assert video_duration / 2 == seg_video_duration, "视频对半分割失败！"
        log.log_pass("原视频长度:{}秒，分割后视频长度:{}秒".format(video_duration, seg_video_duration))
        self.con.click_find_by_name("清空列表")
        self.con.click_find_by_name("确定")

    # MP4转换为多格式
    def mp4_con_all_format(self):
        utils.perform_sleep(1)
        for i in range(1, 5, 1):
            self.con.click_find_by_name("添加文件")
            self.con.input_find_by_classname("Edit", self.file_path)
            self.con.click_find_by_name("打开(O)")
            CommonCaseVideo.click_by_pic(CommonCaseVideo.video_seg)
            self.con.click_find_by_name("截取当前片段")
            self.con.click_find_by_name("保存")
            file_name = CommonCaseVideo.update_name()
            self.con.driver.find_element_by_class_name('QToolButton').click()
            utils.perform_sleep(1)
            video_format = wadlib.new_driver(self.process_path)
            format_list = video_format.driver.find_elements_by_class_name("QListWidget")[0].find_elements_by_tag_name('ListItem')
            format_list[i].click()
            utils.perform_sleep(1)
            resolution_list = video_format.driver.find_elements_by_class_name("QListWidget")[1].find_elements_by_tag_name('ListItem')
            resolution_list[0].click()
            utils.perform_sleep(1)
            self.con.click_find_by_name("全部分割")
            CommonCaseVideo.conversion_spend_time()
            con_file_num = CommonCaseVideo.get_file_name(self.output_path)
            assert file_name == con_file_num[-1].split(".")[0], "转换文件失败！"
            log.log_pass("MP4转换为{}成功!".format(con_file_num[-1].split(".")[-1]))
            self.con.click_find_by_name("清空列表")
            self.con.click_find_by_name("确定")

    # 多格式转换为MP4
    def many_format_con_mp4(self):
        utils.perform_sleep(1)
        multi_format = ["com_demo_f.flv", "com_demo_mk.mkv", "com_demo_mo.mov"]
        for format_name in multi_format:
            other_com_file_path = os.path.join(CommonCasePdf.find_desktop_by_reg(), 'videofile', format_name)
            self.con.click_find_by_name("添加文件")
            self.con.input_find_by_classname("Edit", other_com_file_path)
            self.con.click_find_by_name("打开(O)")
            CommonCaseVideo.click_by_pic(CommonCaseVideo.video_seg)
            self.con.click_find_by_name("截取当前片段")
            self.con.click_find_by_name("保存")
            file_name = CommonCaseVideo.update_name()
            self.con.click_find_by_name("全部分割")
            CommonCaseVideo.conversion_spend_time()
            con_file_num = CommonCaseVideo.get_file_name(self.output_path)
            assert file_name == con_file_num[-1].split(".")[0] and con_file_num[-1].split(".")[-1] == "mp4", "转换文件失败！"
            log.log_pass("{}转换为mp4成功!".format(format_name))
            self.con.click_find_by_name("清空列表")
            self.con.click_find_by_name("确定")

    # 退出转换器
    def quit_process(self):
        self.con.click_find_elements_by_property(By.CLASS_NAME, 'CustomButton', 4, "关闭")
        utils.perform_sleep(2)
        log.log_info("关闭视频转换器成功！")


if __name__ == '__main__':
    exe_path = CommonCaseVideo.get_conversion_process_path()
    video_con = VideoSegmentationFunc(exe_path)

