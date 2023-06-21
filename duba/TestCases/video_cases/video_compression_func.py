import os
from selenium.webdriver.common.by import By
from common import utils
from common.log import log
from common.wadlib import wadlib
from common.tools.pdf_tools import CommonCasePdf
from common.tools.video_tools import CommonCaseVideo


class VideoCompressionFunc(object):

    def __init__(self, path):
        self.con = wadlib(app_path=path)
        self.process_path = CommonCaseVideo.get_conversion_process_path()
        self.file_path = os.path.join(CommonCasePdf.find_desktop_by_reg(), 'videofile', 'demo.mp4')
        self.output_path = CommonCasePdf.create_folder('compression_result')

    # 视频压缩功能校验
    def compression_video(self):
        com_video_file = os.path.join(CommonCasePdf.find_desktop_by_reg(), 'videofile', 'com_demo.mp4')
        main_windows = self.con.driver.title
        CommonCaseVideo.window_top(self.con.driver.title)
        self.con.click_find_by_name("视频压缩")
        self.con.click_find_by_name("极速模式")
        self.con.click_find_by_name("自定义路径")
        self.con.click_find_by_name("浏览")
        self.con.input_find_by_classname('Edit', self.output_path)
        self.con.click_find_elements_by_property(By.NAME, '选择文件夹', 1)
        compression_options = ['体积较小(25%)有损', '推荐压缩(50%)一般', '体积较大(75%)清晰', '输入比例(自定义)']
        for option_name in compression_options:
            self.con.click_find_by_name("添加文件")
            self.con.input_find_by_classname("Edit", com_video_file)
            self.con.click_find_by_name("打开(O)")
            file_name = CommonCaseVideo.update_name()
            self.con.click_find_elements_by_property(By.CLASS_NAME, 'QComboBox', 0, "压缩比例")
            self.con.switch_windows_to_condition(By.NAME, option_name)
            self.con.click_find_by_name(option_name)
            self.con.switch_windows(main_windows)
            if option_name == "输入比例(自定义)":
                self.con.input_find_by_classname('QLineEdit', '35')
            self.con.click_find_by_name("全部压缩")
            CommonCaseVideo.conversion_spend_time()
            con_file = CommonCaseVideo.get_file_name(self.output_path)
            assert file_name == con_file[-1].split(".")[0], "转换文件失败"
            size_mut = CommonCaseVideo.get_file_size_multiple(com_video_file, os.path.join(self.output_path, con_file[-1]))
            if option_name == "体积较小(25%)有损":
                assert size_mut <= 0.30, "视频压缩失败！"
            if option_name == "推荐压缩(50%)一般":
                assert size_mut <= 0.55, "视频压缩失败！"
            if option_name == "体积较大(75%)清晰":
                assert size_mut <= 0.80, "视频压缩失败！"
            if option_name == "输入比例(自定义)":
                assert size_mut <= 0.40, "视频压缩失败！"
            log.log_pass("视频压缩[%s]成功，压缩后大小为原来的%s倍!" % (option_name, size_mut))
            self.con.click_find_by_name("清空列表")
            self.con.click_find_by_name("确定")
        self.con.click_find_elements_by_property(By.CLASS_NAME, 'QComboBox', 0, "压缩比例")
        self.con.switch_windows_to_condition(By.NAME, "推荐压缩(50%)一般")
        self.con.click_find_by_name("推荐压缩(50%)一般")
        self.con.switch_windows(main_windows)

    # 多格式文件压缩
    def many_format_compression(self):
        utils.perform_sleep(1)
        multi_format = ["com_demo_f.flv", "com_demo_mk.mkv", "com_demo_mo.mov"]
        for file_name in multi_format:
            other_com_file_path = os.path.join(CommonCasePdf.find_desktop_by_reg(), 'videofile', file_name)
            self.con.click_find_by_name("添加文件")
            self.con.input_find_by_classname("Edit", other_com_file_path)
            self.con.click_find_by_name("打开(O)")
            file_name = CommonCaseVideo.update_name()
            self.con.click_find_by_name("全部压缩")
            CommonCaseVideo.conversion_spend_time()
            con_file = CommonCaseVideo.get_file_name(self.output_path)
            assert file_name == con_file[-1].split(".")[0], "文件转换失败！"
            size_mut = CommonCaseVideo.get_file_size_multiple(other_com_file_path, os.path.join(self.output_path, con_file[-1]))
            print(size_mut)
            if ".flv" in con_file[-1]:
                assert size_mut <= 1, "视频压缩失败！"
            else:
                assert size_mut <= 0.55, "视频压缩失败！"
            log.log_pass("视频压缩成功，压缩后大小为原来的%s倍!" % size_mut)
            self.con.click_find_by_name("清空列表")
            self.con.click_find_by_name("确定")

    # 退出转换器
    def quit_process(self):
        self.con.click_find_elements_by_property(By.CLASS_NAME, 'CustomButton', 4, "关闭")
        utils.perform_sleep(2)
        log.log_info("关闭视频转换器成功！")


if __name__ == '__main__':
    exe_path = CommonCaseVideo.get_conversion_process_path()
    video_con = VideoCompressionFunc(exe_path)
    video_con.many_format_compression()
