import os
from selenium.webdriver.common.by import By
from common import utils
from common.log import log
from common.wadlib import wadlib
from common.tools.pdf_tools import CommonCasePdf
from common.tools.video_tools import CommonCaseVideo


class VideoWaterMarkFunc(object):

    def __init__(self, path):
        self.con = wadlib(app_path=path)
        self.process_path = CommonCaseVideo.get_conversion_process_path()
        self.file_path = os.path.join(CommonCasePdf.find_desktop_by_reg(), 'videofile', 'demo.mp4')
        self.output_path = CommonCasePdf.create_folder('watermark_result')

    # 视频去水印
    def video_clear_watermark(self):
        CommonCaseVideo.window_top(self.con.driver.title)
        self.con.click_find_by_name("视频水印")
        self.con.click_find_by_name("添加文件")
        self.con.input_find_by_classname("Edit", self.file_path)
        self.con.click_find_by_name("打开(O)")
        CommonCaseVideo.click_by_pic(CommonCaseVideo.video_clear_watermark)
        assert self.con.isElementPresent(By.NAME, "添加去水印区域")
        self.con.click_find_by_name("添加去水印区域")
        self.con.click_find_by_name("确定")
        file_name = CommonCaseVideo.update_name()
        self.con.click_find_by_name("自定义路径")
        self.con.click_find_by_name("浏览")
        self.con.input_find_by_classname('Edit', self.output_path)
        self.con.click_find_elements_by_property(By.NAME, '选择文件夹', 1)
        self.con.click_find_by_name("全部开始")
        CommonCaseVideo.conversion_spend_time()
        con_file = CommonCaseVideo.get_file_name(self.output_path)
        assert file_name == con_file[-1].split(".")[0], "视频去水印失败！"
        log.log_pass("视频去水印成功！")
        self.con.click_find_by_name("清空列表")
        self.con.click_find_by_name("确定")

    # 设置开始时间段
    def set_watermark_period(self):
        self.con.click_find_by_name("添加文件")
        self.con.input_find_by_classname("Edit", self.file_path)
        self.con.click_find_by_name("打开(O)")
        CommonCaseVideo.click_by_pic(CommonCaseVideo.video_clear_watermark)
        assert self.con.isElementPresent(By.NAME, "添加去水印区域")
        self.con.click_find_by_name("添加去水印区域")
        self.con.click_find_elements_by_property(By.CLASS_NAME, "QLineEdit", 0, "开始时间")
        # 输入水印开始时间
        for i in range(0, 3, 1):
            utils.keyboardInputByCode('right_arrow')
        utils.perform_sleep(0.5)
        utils.keyboardInputByCode('backspace')
        utils.key_input('3')
        utils.perform_sleep(1)
        # 输入水印结束时间
        self.con.click_find_elements_by_property(By.CLASS_NAME, "QLineEdit", 1, "结束时间")
        for i in range(0, 3, 1):
            utils.keyboardInputByCode('right_arrow')
        utils.perform_sleep(0.5)
        utils.keyboardInputByCode('backspace')
        utils.key_input('10')
        utils.perform_sleep(1)
        self.con.click_find_by_name("确定")
        file_name = CommonCaseVideo.update_name()
        self.con.click_find_by_name("全部开始")
        CommonCaseVideo.conversion_spend_time()
        con_file = CommonCaseVideo.get_file_name(self.output_path)
        con_file_path = os.path.join(self.output_path, con_file[-1])
        assert file_name == con_file[-1].split(".")[0], "视频转换失败！"
        img_1 = CommonCaseVideo.get_frame_of_video(self.file_path, self.output_path)
        img_2 = CommonCaseVideo.get_frame_of_video(con_file_path, self.output_path)
        assert utils.compare_picture_similarity(img_1, img_2, sim=0.99), "(未带水印片段)设置开始时间段失败！"
        img_3 = CommonCaseVideo.get_frame_of_video(self.file_path, self.output_path, frame_time=4000)
        img_4 = CommonCaseVideo.get_frame_of_video(con_file_path, self.output_path, frame_time=4000)
        assert (not utils.compare_picture_similarity(img_3, img_4, sim=0.99)),  "设置开始时间段失败！"
        log.log_pass("设置开始时间段成功！")
        img_5 = CommonCaseVideo.get_frame_of_video(self.file_path, self.output_path, frame_time=12000)
        img_6 = CommonCaseVideo.get_frame_of_video(con_file_path, self.output_path, frame_time=12000)
        assert utils.compare_picture_similarity(img_5, img_6, sim=0.99), "设置结束时间段失败！"
        log.log_pass("设置结束时间段成功！", attach=False)
        self.con.click_find_by_name("清空列表")
        self.con.click_find_by_name("确定")

    # 视频加图片水印
    def video_add_watermark(self):
        pic_path = os.path.join(CommonCasePdf.find_desktop_by_reg(), 'videofile', 'pic.jpg')
        self.con.click_find_by_name("添加文件")
        self.con.input_find_by_classname("Edit", self.file_path)
        self.con.click_find_by_name("打开(O)")
        CommonCaseVideo.click_by_pic(CommonCaseVideo.video_add_watermark)
        assert self.con.isElementPresent(By.NAME, "添加图片水印")
        self.con.click_find_by_name("添加图片水印")
        self.con.input_find_by_classname("Edit", pic_path)
        self.con.click_find_by_name("打开(O)")
        self.con.click_find_by_name("确定")
        file_name = CommonCaseVideo.update_name()
        self.con.click_find_by_name("全部开始")
        CommonCaseVideo.conversion_spend_time()
        con_file = CommonCaseVideo.get_file_name(self.output_path)
        assert file_name == con_file[-1].split(".")[0], "视频加图片水印失败！"
        log.log_pass("视频加图片水印成功！")
        self.con.click_find_by_name("清空列表")
        self.con.click_find_by_name("确定")

    # 退出转换器
    def quit_process(self):
        self.con.click_find_elements_by_property(By.CLASS_NAME, 'CustomButton', 4, "关闭")
        utils.perform_sleep(2)
        log.log_info("关闭视频转换器成功！")


if __name__ == '__main__':
    exe_path = CommonCaseVideo.get_conversion_process_path()
    video_con = VideoWaterMarkFunc(exe_path)
    video_con.video_clear_watermark()
    video_con.set_watermark_period()
    video_con.video_add_watermark()
