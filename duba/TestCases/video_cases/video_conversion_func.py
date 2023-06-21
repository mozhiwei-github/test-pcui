import os
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from common import utils
from common.log import log
from common.wadlib import wadlib
from common.tools.pdf_tools import CommonCasePdf
from common.tools.video_tools import CommonCaseVideo


class VideoConversionFunc(object):

    def __init__(self, path):
        self.con = wadlib(app_path=path)
        self.file_path = os.path.join(CommonCasePdf.find_desktop_by_reg(), 'videofile', 'demo.mp4')
        self.output_path = CommonCasePdf.create_folder('video_com')

    # 对比普通转换和极速转换
    def con_mode_conversion(self):
        # 普通模式
        CommonCaseVideo.window_top(self.con.driver.title)
        self.con.click_find_by_name("视频转换")
        self.con.click_find_by_name("添加文件")
        self.con.input_find_by_classname("Edit", self.file_path)
        self.con.click_find_by_name("打开(O)")
        con_list = self.con.find_elements_by_property(By.CLASS_NAME, 'CustomListWidget', By.TAG_NAME, 'ListItem')
        assert len(con_list) == 1
        file_name = CommonCaseVideo.update_name()
        self.con.click_find_by_name("全部转换")
        normal_con_time = CommonCaseVideo.conversion_spend_time()
        con_file_num = CommonCaseVideo.get_file_name(os.path.join(CommonCasePdf.find_desktop_by_reg(), 'videofile'))
        assert file_name == con_file_num[-1].split(".")[0], "转换失败！"
        log.log_pass("%s转换成功，花费时间：%.4f秒" % (con_file_num[-1], normal_con_time))
        self.con.click_find_by_name("清空列表")
        self.con.click_find_by_name("确定")
        # 极速模式
        self.con.click_find_by_name("极速模式")
        self.con.click_find_by_name("添加文件")
        self.con.input_find_by_classname("Edit", self.file_path)
        self.con.click_find_by_name("打开(O)")
        assert len(con_list) == 1
        file_name = CommonCaseVideo.update_name()
        self.con.click_find_by_name("自定义路径")
        self.con.click_find_by_name("浏览")
        self.con.input_find_by_classname('Edit', self.output_path)
        self.con.click_find_elements_by_property(By.NAME, '选择文件夹', 1)
        self.con.click_find_by_name("全部转换")
        speed_con_time = CommonCaseVideo.conversion_spend_time()
        con_file_num = CommonCaseVideo.get_file_name(self.output_path)
        assert (speed_con_time < normal_con_time and file_name == con_file_num[-1].split(".")[0]), "进入极速模式失败！"
        log.log_pass("进入极速模式成功，花费时间：%.4f秒" % speed_con_time)
        self.con.click_find_by_name("清空列表")
        self.con.click_find_by_name("确定")

    # 顺时针旋转90°
    def clockwise_rotate_90(self):
        self.con.click_find_by_name("添加文件")
        self.con.input_find_by_classname("Edit", self.file_path)
        self.con.click_find_by_name("打开(O)")
        file_name = CommonCaseVideo.update_name()
        CommonCaseVideo.click_by_pic(CommonCaseVideo.video_crop)
        assert self.con.isElementPresent(By.NAME, "视频裁剪")
        self.con.click_element_by_list(By.CLASS_NAME, "VideoCatDialog", By.CLASS_NAME, "CustomButton", 1, "顺时针旋转90°")
        self.con.click_find_by_name("确定")
        self.con.click_find_by_name("全部转换")
        CommonCaseVideo.conversion_spend_time()
        con_file_num = CommonCaseVideo.get_file_name(self.output_path)
        assert file_name == con_file_num[-1].split(".")[0], "转换文件失败！"
        img_1 = CommonCaseVideo.get_frame_of_video(self.file_path, self.output_path)
        img_2 = CommonCaseVideo.get_frame_of_video(os.path.join(self.output_path, con_file_num[-1]), self.output_path)
        img_3 = CommonCaseVideo.rotate_pic_by_value(90, img_2, self.output_path)
        assert utils.compare_picture_similarity(img_1, img_3, sim=0.98), "顺时针旋转90°失败！"
        log.log_pass("顺时针旋转90°成功！")
        self.con.click_find_by_name("清空列表")
        self.con.click_find_by_name("确定")

    # 逆时针旋转90°
    def counterclockwise_rotate_90(self):
        self.con.click_find_by_name("添加文件")
        self.con.input_find_by_classname("Edit", self.file_path)
        self.con.click_find_by_name("打开(O)")
        file_name = CommonCaseVideo.update_name()
        CommonCaseVideo.click_by_pic(CommonCaseVideo.video_crop)
        assert self.con.isElementPresent(By.NAME, "视频裁剪")
        self.con.click_element_by_list(By.CLASS_NAME, "VideoCatDialog", By.CLASS_NAME, "CustomButton", 2, "逆时针旋转90°")
        self.con.click_find_by_name("确定")
        self.con.click_find_by_name("全部转换")
        CommonCaseVideo.conversion_spend_time()
        con_file_num = CommonCaseVideo.get_file_name(self.output_path)
        assert file_name == con_file_num[-1].split(".")[0], "转换文件失败！"
        img_1 = CommonCaseVideo.get_frame_of_video(self.file_path, self.output_path)
        img_2 = CommonCaseVideo.get_frame_of_video(os.path.join(self.output_path, con_file_num[-1]), self.output_path)
        img_3 = CommonCaseVideo.rotate_pic_by_value(90, img_1, self.output_path)
        assert utils.compare_picture_similarity(img_2, img_3, sim=0.98), "逆时针旋转90°失败！"
        log.log_pass("逆时针旋转90°成功！")
        self.con.click_find_by_name("清空列表")
        self.con.click_find_by_name("确定")

    # 水平翻转
    def horizontal_flip(self):
        self.con.click_find_by_name("添加文件")
        self.con.input_find_by_classname("Edit", self.file_path)
        self.con.click_find_by_name("打开(O)")
        file_name = CommonCaseVideo.update_name()
        CommonCaseVideo.click_by_pic(CommonCaseVideo.video_crop)
        assert self.con.isElementPresent(By.NAME, "视频裁剪")
        self.con.click_element_by_list(By.CLASS_NAME, "VideoCatDialog", By.CLASS_NAME, "CustomButton", 3, "水平翻转")
        self.con.click_find_by_name("确定")
        self.con.click_find_by_name("全部转换")
        CommonCaseVideo.conversion_spend_time()
        con_file_num = CommonCaseVideo.get_file_name(self.output_path)
        assert file_name == con_file_num[-1].split(".")[0], "转换文件失败！"
        img_1 = CommonCaseVideo.get_frame_of_video(self.file_path, self.output_path)
        img_2 = CommonCaseVideo.get_frame_of_video(os.path.join(self.output_path, con_file_num[-1]), self.output_path)
        img_3 = CommonCaseVideo.flip_pic_level(img_2, self.output_path)
        assert utils.compare_picture_similarity(img_1, img_3, sim=0.98), "水平翻转失败！"
        log.log_pass("水平翻转成功！")
        self.con.click_find_by_name("清空列表")
        self.con.click_find_by_name("确定")

    # 垂直翻转
    def vertically_flip(self):
        self.con.click_find_by_name("添加文件")
        self.con.input_find_by_classname("Edit", self.file_path)
        self.con.click_find_by_name("打开(O)")
        file_name = CommonCaseVideo.update_name()
        CommonCaseVideo.click_by_pic(CommonCaseVideo.video_crop)
        assert self.con.isElementPresent(By.NAME, "视频裁剪")
        self.con.click_element_by_list(By.CLASS_NAME, "VideoCatDialog", By.CLASS_NAME, "CustomButton", 4, "垂直翻转")
        self.con.click_find_by_name("确定")
        self.con.click_find_by_name("全部转换")
        CommonCaseVideo.conversion_spend_time()
        con_file_num = CommonCaseVideo.get_file_name(self.output_path)
        assert file_name == con_file_num[-1].split(".")[0], "转换文件失败！"
        img_1 = CommonCaseVideo.get_frame_of_video(self.file_path, self.output_path)
        img_2 = CommonCaseVideo.get_frame_of_video(os.path.join(self.output_path, con_file_num[-1]), self.output_path)
        img_3 = CommonCaseVideo.flip_pic_vertical(img_2, self.output_path)
        assert utils.compare_picture_similarity(img_1, img_3, sim=0.98), "垂直翻转失败！"
        log.log_pass("垂直翻转成功！")
        self.con.click_find_by_name("清空列表")
        self.con.click_find_by_name("确定")

    # 播放速度
    def video_play_speed(self):
        self.con.click_find_by_name("添加文件")
        self.con.input_find_by_classname("Edit", self.file_path)
        self.con.click_find_by_name("打开(O)")
        file_name = CommonCaseVideo.update_name()
        CommonCaseVideo.click_by_pic(CommonCaseVideo.video_crop)
        assert self.con.isElementPresent(By.NAME, "视频裁剪")
        self.con.click_find_elements_by_property(By.CLASS_NAME, "QDoubleSpinBox", 0, "播放速度")
        for i in range(0, 3, 1):
            utils.keyboardInputByCode('backspace')
            utils.perform_sleep(0.1)
        utils.key_input('3')
        utils.perform_sleep(1)
        self.con.click_find_by_name("确定")
        self.con.click_find_by_name("全部转换")
        CommonCaseVideo.conversion_spend_time()
        con_file_num = CommonCaseVideo.get_file_name(self.output_path)
        assert file_name == con_file_num[-1].split(".")[0], "转换文件失败！"
        origin_seconds = CommonCaseVideo.get_video_duration(self.file_path)
        target_seconds = CommonCaseVideo.get_video_duration(os.path.join(self.output_path, con_file_num[-1]))
        assert target_seconds <= origin_seconds / 3, "设置播放速度失败！"
        log.log_pass("设置播放速度成功！")
        self.con.click_find_by_name("清空列表")
        self.con.click_find_by_name("确定")

    # MP4转换为所有格式
    def conversion_all_format(self):
        all_format_file = CommonCasePdf.create_folder('all_format')
        main_title = self.con.driver.title
        self.con.click_find_by_name("自定义路径")
        self.con.click_find_by_name("浏览")
        self.con.input_find_by_classname('Edit', all_format_file)
        self.con.click_find_elements_by_property(By.NAME, '选择文件夹', 1)
        """
        fail_num：统计失败次数
        con_num_sigh：统计转换总次数
        end_sign：滚轮滚动参数。当输入格式重复时，则不再需要增加滚轮滚动参数
        con_num：每滚动一次滚轮时，转换格式次数
        cycle_num：滚轮滚动参数
        """
        fail_num = []
        con_num_sigh, end_sign, con_num, cycle_num = 0, 0, 0, 0
        while True:
            self.con.click_find_elements_by_property(By.CLASS_NAME, 'QToolButton', 0, "选择格式")
            self.con.switch_windows("VideoFormatDialog")
            format_list = self.con.driver.find_elements_by_class_name("QListWidget")[0]. find_elements_by_tag_name('ListItem')
            if cycle_num >= 1:
                ActionChains(self.con.driver).move_to_element(format_list[0]).perform()
                utils.perform_sleep(1)
                utils.mouse_scroll(int(125 * CommonCaseVideo.get_scaling_ratio()) * cycle_num)
                utils.perform_sleep(1)
                format_list = self.con.driver.find_elements_by_class_name("QListWidget")[0].find_elements_by_tag_name('ListItem')
            if cycle_num >= 3:
                ActionChains(self.con.driver).move_to_element(format_list[2]).perform()
                utils.perform_sleep(1)
                utils.mouse_scroll(150 * cycle_num)
                utils.perform_sleep(1)
                format_list = self.con.driver.find_elements_by_class_name("QListWidget")[0].find_elements_by_tag_name('ListItem')
            format_list[con_num].click()
            con_num += 1
            utils.perform_sleep(1)
            resolution_list = self.con.driver.find_elements_by_class_name("QListWidget")[1].find_elements_by_tag_name('ListItem')
            resolution_list[0].click()
            utils.perform_sleep(1)
            self.con.switch_windows(main_title)
            # 判断该格式是否已经转换过
            current_format = self.con.driver.find_element_by_class_name("QToolButton").get_attribute('Name')
            if not CommonCaseVideo.all_format[con_num_sigh] == str(current_format).split(' ')[0]:
                end_sign = 1
                continue
            # 添加文件
            self.con.click_find_by_name("添加文件")
            self.con.input_find_by_classname("Edit", self.file_path)
            self.con.click_find_by_name("打开(O)")
            # 修改输出文件名字
            file_name = CommonCaseVideo.update_name()
            file_list = self.con.find_elements_by_property(By.CLASS_NAME, 'CustomListWidget', By.TAG_NAME, 'ListItem')
            assert len(file_list) == 1
            self.con.click_find_by_name("全部转换")
            spend_time = CommonCaseVideo.conversion_spend_time()
            result_file_name = CommonCaseVideo.get_file_name(all_format_file)[-1].split(".")[0]
            if file_name == result_file_name:
                log.log_pass("[%s]格式转换成功，花费时间：%.4f秒！" % (CommonCaseVideo.all_format[con_num_sigh], spend_time))
            else:
                fail_num.append(CommonCaseVideo.all_format[con_num_sigh])
            if end_sign == 0:
                if con_num == 3:
                    cycle_num += 1
                    con_num = 0
            self.con.click_find_by_name("清空列表")
            self.con.click_find_by_name("确定")
            con_num_sigh += 1
            if con_num_sigh == 14:
                break
        log.log_pass("所有格式转换完成。失败次数：%s次，失败格式：[%s]" % (len(fail_num), fail_num))

    def quit_process(self):
        self.con.click_find_elements_by_property(By.CLASS_NAME, 'CustomButton', 4, "关闭")
        utils.perform_sleep(2)
        if self.con.isElementPresent(By.NAME, "立即添加"):
            self.con.click_find_by_name("立即添加")
            utils.perform_sleep(2)
        assert self.con.driver_exist(), "关闭视频转换器失败！"
        log.log_info("关闭视频转换器成功！")


if __name__ == '__main__':
    exe_path = CommonCaseVideo.get_conversion_process_path()
    video_con = VideoConversionFunc(exe_path)
