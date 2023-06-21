import os
from selenium.webdriver.common.by import By
from common import utils
from common.log import log
from common.wadlib import wadlib
from common.tools.pdf_tools import CommonCasePdf
from common.tools.video_tools import CommonCaseVideo


class VideoMergeFunc(object):

    def __init__(self, path):
        self.con = wadlib(app_path=path)
        self.file_path = os.path.join(CommonCasePdf.find_desktop_by_reg(), 'videofile', 'demo.mp4')
        self.output_path = CommonCasePdf.create_folder('video_merge')
        self.process_path = CommonCaseVideo.get_conversion_process_path()

    # 合并相同文件
    def same_file_merge(self):
        CommonCaseVideo.window_top(self.con.driver.title)
        utils.perform_sleep(1)
        self.con.click_find_by_name("视频合并")
        self.con.click_find_by_name("自定义路径")
        self.con.click_find_by_name("浏览")
        self.con.input_find_by_classname('Edit', self.output_path)
        self.con.click_find_elements_by_property(By.NAME, '选择文件夹', 1)
        self.con.click_find_by_name("添加文件")
        self.con.input_find_by_classname("Edit", self.file_path)
        self.con.click_find_by_name("打开(O)")
        self.con.click_find_by_name("全部合并")
        assert self.con.isElementPresent(By.NAME, '请至少添加两个待合并文件！')
        self.con.click_find_by_name("确定")
        self.con.click_find_by_name("添加文件")
        self.con.input_find_by_classname("Edit", self.file_path)
        self.con.click_find_by_name("打开(O)")
        self.con.click_find_by_name("全部合并")
        CommonCaseVideo.conversion_spend_time()
        result_text = self.con.driver.find_element_by_class_name('ElidedLabel').get_attribute('Name')
        con_file = os.path.join(self.output_path, result_text.strip("您的视频文件“”已合并完成"))
        assert os.path.exists(con_file), "文件合并成功！"
        self.con.click_element_by_list(By.CLASS_NAME, "MergeProgressDialog", By.CLASS_NAME, "CustomButton", 0)
        origin_video_length = CommonCaseVideo.get_video_duration(self.file_path)
        target_video_length = CommonCaseVideo.get_video_duration(con_file)
        assert (origin_video_length * 2) <= target_video_length <= (origin_video_length * 2) + 3, "合并视频长度有误"
        log.log_pass("原视频长度%s秒,合并后视频长度%s秒" % (origin_video_length, target_video_length))
        self.con.click_find_by_name("清空列表")
        self.con.click_find_by_name("确定")

    # 合并分辨率不同文件
    def different_resolution_merge(self):
        portrait_file = os.path.join(CommonCasePdf.find_desktop_by_reg(), "videofile", "portrait_demo.mp4")
        self.con.click_find_by_name("添加文件")
        self.con.input_find_by_classname("Edit", portrait_file)
        self.con.click_find_by_name("打开(O)")
        self.con.click_find_by_name("添加文件")
        self.con.input_find_by_classname("Edit", self.file_path)
        self.con.click_find_by_name("打开(O)")
        self.con.click_find_by_name("全部合并")
        CommonCaseVideo.conversion_spend_time()
        result_text = self.con.driver.find_element_by_class_name('ElidedLabel').get_attribute('Name')
        con_file = os.path.join(self.output_path, result_text.strip("您的视频文件“”已合并完成"))
        assert os.path.exists(con_file), "文件合并成功！"
        self.con.click_element_by_list(By.CLASS_NAME, "MergeProgressDialog", By.CLASS_NAME, "CustomButton", 0, "关闭")
        origin_length_1 = CommonCaseVideo.get_video_duration(self.file_path)
        origin_length_2 = CommonCaseVideo.get_video_duration(portrait_file)
        target_video_length = CommonCaseVideo.get_video_duration(con_file)
        assert (origin_length_1 + origin_length_2) <= target_video_length <= (origin_length_1 + origin_length_2) + 3, "合并视频长度有误"
        log.log_pass("原视频长度%s秒,合并后视频长度%s秒" % ((origin_length_1 + origin_length_2), target_video_length))
        self.con.click_find_by_name("清空列表")
        self.con.click_find_by_name("确定")

    # 不同格式文件合并
    def different_format_merge(self):
        for file_name in ["com_demo_mo.mov", "com_demo_mk.mkv", "com_demo_f.flv"]:
            file_path = os.path.join(CommonCasePdf.find_desktop_by_reg(), "videofile", file_name)
            self.con.click_find_by_name("添加文件")
            self.con.input_find_by_classname("Edit", '"{}" "{}"'.format(self.file_path, file_path))
            self.con.click_find_by_name("打开(O)")
            self.con.click_find_by_name("全部合并")
            CommonCaseVideo.conversion_spend_time()
            result_text = self.con.driver.find_element_by_class_name('ElidedLabel').get_attribute('Name')
            con_file = os.path.join(self.output_path, result_text.strip("您的视频文件“”已合并完成"))
            assert os.path.exists(con_file), "文件合并成功！"
            log.log_pass("{0}与mp4格式文件合并成功！".format(file_name.split(".")[-1]))
            self.con.click_element_by_list(By.CLASS_NAME, "MergeProgressDialog", By.CLASS_NAME, "CustomButton", 0, object_name="关闭")
            self.con.click_find_by_name("清空列表")
            self.con.click_find_by_name("确定")

    # 输出为其他格式文件
    def output_many_format_merge(self):
        other_file_path = os.path.join(CommonCasePdf.find_desktop_by_reg(), "videofile", "demo_merge.mp4")
        main_title = self.con.driver.title
        for i in range(1, 5, 1):
            self.con.click_find_by_name("添加文件")
            self.con.input_find_by_classname("Edit", '"{}" "{}"'.format(self.file_path, other_file_path))
            self.con.click_find_by_name("打开(O)")
            self.con.click_find_elements_by_property(By.CLASS_NAME, 'QToolButton', 0, "选择格式")
            self.con.switch_windows("VideoFormatDialog")
            format_list = self.con.driver.find_elements_by_class_name("QListWidget")[0].find_elements_by_tag_name('ListItem')
            format_list[i].click()
            utils.perform_sleep(1)
            resolution_list = self.con.driver.find_elements_by_class_name("QListWidget")[1].find_elements_by_tag_name('ListItem')
            resolution_list[0].click()
            utils.perform_sleep(1)
            self.con.switch_windows(main_title)
            self.con.click_find_by_name("全部合并")
            CommonCaseVideo.conversion_spend_time()
            result_text = self.con.driver.find_element_by_class_name('ElidedLabel').get_attribute('Name')
            con_file = os.path.join(self.output_path, result_text.strip("您的视频文件“”已合并完成"))
            assert os.path.exists(con_file), "文件合并成功！"
            log.log_pass("{}文件合并成功！".format(result_text.strip("您的视频文件“”已合并完成")))
            self.con.click_element_by_list(By.CLASS_NAME, "MergeProgressDialog", By.CLASS_NAME, "CustomButton", 0,
                                           object_name="关闭")
            self.con.click_find_by_name("清空列表")
            self.con.click_find_by_name("确定")

    # 关闭阅读器
    def quit_process(self):
        self.con.click_find_elements_by_property(By.CLASS_NAME, 'CustomButton', 4, "关闭")
        utils.perform_sleep(2)
        assert self.con.driver_exist(), "关闭视频转换器失败！"
        log.log_info("关闭视频转换器成功！")


if __name__ == '__main__':
    exe_path = CommonCaseVideo.get_conversion_process_path()
    video_con = VideoMergeFunc(exe_path)

