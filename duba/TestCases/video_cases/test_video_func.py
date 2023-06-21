import os
import allure
import pytest
from selenium.webdriver.common.by import By
from common import utils
from common.contants import InputLan
from common.log import log
from common.wadlib import wadlib
from common.tools.pdf_tools import CommonCasePdf
from common.tools.video_tools import CommonCaseVideo
from duba.PageObjects.setting_page import SettingPage
from duba.TestCases.video_cases.video_conversion_func import VideoConversionFunc
from duba.TestCases.video_cases.video_segmentation_func import VideoSegmentationFunc
from duba.TestCases.video_cases.video_watermark_func import VideoWaterMarkFunc
from duba.TestCases.video_cases.video_compression_func import VideoCompressionFunc
from duba.TestCases.video_cases.video_merge_func import VideoMergeFunc


@allure.epic(f'极光视频转换器场景测试')
@allure.feature('极光视频转换器功能测试')
class TestVideoConversion(object):

    def setup_class(self):
        allure.dynamic.description(
            '\t初始化环境\n'
        )
        allure.dynamic.title("初始化电脑环境")

        with allure.step("初始化环境"):
            # 毒霸集成版关闭自保护
            if CommonCaseVideo.get_conversion_process_path() == CommonCaseVideo.db_video_path:
                SettingPage_ = SettingPage()
                SettingPage_.self_protecting_close()
                assert SettingPage_.page_close(), "关闭设置页失败"
            CommonCasePdf.copy_file(r'\liangzhibo\视频格式\videofile', 'videofile')
            utils.change_input_lan(InputLan.EN)

    def teardown_class(self):
        allure.dynamic.description(
            '\t执行结束后\n'
        )
        allure.dynamic.title("执行结束")
        with allure.step("执行结束"):
            utils.change_input_lan(InputLan.ZH)

    @pytest.fixture(scope='function', autouse=True)
    def kill_process(self):
        if utils.is_process_exists('fastvc.exe'):
            os.system('taskkill /f /im fastvc.exe')
            log.log_info("杀掉fastvc.exe进程")

    @allure.story('视频转换')
    @pytest.mark.flaky(reruns=1)
    def test_video_conversion(self):
        allure.dynamic.description(
            '\t1.打开视频转换器\n'
            '\t2.添加视频文件\n'
            '\t3.点击全部转换\n'
        )
        allure.dynamic.title('视频转换页签功能测试')

        with allure.step("极速模式"):
            many_format_con = VideoConversionFunc(CommonCaseVideo.get_conversion_process_path())
            many_format_con.con_mode_conversion()

        with allure.step("翻转/旋转"):
            many_format_con.clockwise_rotate_90()
            many_format_con.counterclockwise_rotate_90()
            many_format_con.horizontal_flip()
            many_format_con.vertically_flip()

        with allure.step("播放速度"):
            many_format_con.video_play_speed()

        with allure.step("转换所有格式文件"):
            many_format_con.conversion_all_format()

        with allure.step("退出转换器"):
            many_format_con.quit_process()

    @allure.story('视频分割')
    @pytest.mark.flaky(reruns=1)
    def test_video_segmentation(self):
        allure.dynamic.description(
            '\t1.打开视频转换器\n'
            '\t2.添加视频文件\n'
            '\t2.点击全部分割\n'
        )
        allure.dynamic.title('视频分割页签功能测试')

        with allure.step("视频分割—对半"):
            video_seg = VideoSegmentationFunc(CommonCaseVideo.get_conversion_process_path())
            video_seg.split_in_half()

        with allure.step("多格式转换为MP4"):
            video_seg.many_format_con_mp4()

        with allure.step("MP4转换为多格式"):
            video_seg.mp4_con_all_format()
            video_seg.quit_process()

    @allure.story('视频水印')
    @pytest.mark.flaky(reruns=1)
    def test_video_watermark(self):
        allure.dynamic.description(
            '\t1.打开视频转换器\n'
            '\t2.添加视频文件\n'
            '\t2.添加去水印、加水印，点击全部开始\n'
        )
        allure.dynamic.title('视频水印页签功能测试')

        with allure.step("视频去水印"):
            water_func = VideoWaterMarkFunc(CommonCaseVideo.get_conversion_process_path())
            water_func.video_clear_watermark()

        with allure.step("设置水印开始结束时间"):
            water_func.set_watermark_period()

        with allure.step("视频加水印"):
            water_func.video_add_watermark()
            water_func.quit_process()

    @allure.story('视频压缩')
    @pytest.mark.flaky(reruns=1)
    def test_video_compression(self):
        allure.dynamic.description(
            '\t1.打开视频转换器\n'
            '\t2.添加视频文件\n'
            '\t2.点击全部压缩\n'
        )
        allure.dynamic.title('视频压缩页签功能测试')

        with allure.step("step4-1:视频压缩"):
            com_func = VideoCompressionFunc(CommonCaseVideo.get_conversion_process_path())
            com_func.compression_video()

        with allure.step("step4-2:多格式文件压缩"):
            com_func.many_format_compression()
            com_func.quit_process()

    @allure.story('视频合并')
    @pytest.mark.flaky(reruns=1)
    def test_video_merge(self):
        allure.dynamic.description(
            '\t1.打开视频转换器\n'
            '\t2.添加视频文件\n'
            '\t2.点击全部合并\n'
        )
        allure.dynamic.title('视频合并页签功能测试')

        with allure.step("同视频合并"):
            merge_func = VideoMergeFunc(CommonCaseVideo.get_conversion_process_path())
            merge_func.same_file_merge()

        with allure.step("不同分辨率视频合并"):
            merge_func.different_resolution_merge()

        with allure.step("不同格式视频合并"):
            merge_func.different_format_merge()

        with allure.step("合并后输出为不同格式"):
            merge_func.output_many_format_merge()
            merge_func.quit_process()

    @allure.story('视频转GIF')
    @pytest.mark.flaky(reruns=1)
    def test_video_con_gif(self):
        allure.dynamic.description(
            '\t1.打开视频转换器\n'
            '\t2.添加视频文件\n'
            '\t2.点击全部合并\n'
        )
        allure.dynamic.title('视频转GIF页签功能测试')

        with allure.step("视频转GIF"):
            folder_path = os.path.join(CommonCasePdf.find_desktop_by_reg(), 'videofile')
            video_con_gif = wadlib(CommonCaseVideo.get_conversion_process_path())
            CommonCaseVideo.window_top(video_con_gif.driver.title)
            utils.perform_sleep(1)
            video_con_gif.click_find_by_name("视频转GIF")
            video_con_gif.click_find_by_name("添加文件")
            video_con_gif.input_find_by_classname("Edit", os.path.join(folder_path, "demo.mp4"))
            video_con_gif.click_find_by_name("打开(O)")
            file_name = CommonCaseVideo.update_name()
            video_con_gif.click_find_by_name("全部转换")
            CommonCaseVideo.conversion_spend_time()
            con_file = CommonCaseVideo.get_file_name(folder_path)
            assert file_name == con_file[-1].split(".")[0] and os.stat(os.path.join(folder_path, con_file[-1])), "转换失败！"
            log.log_pass("视频转换GIF成功！")
            video_con_gif.click_find_elements_by_property(By.CLASS_NAME, 'CustomButton', 4, "关闭")
            utils.perform_sleep(2)
            assert video_con_gif.driver_exist(), "关闭视频转换器失败！"
            log.log_info("关闭视频转换器成功！")

    @allure.story('视频美化')
    @pytest.mark.flaky(reruns=1)
    def test_video_beautify(self):
        allure.dynamic.description(
            '\t1.打开视频转换器\n'
            '\t2.添加视频文件\n'
            '\t2.点击全部美化\n'
        )
        allure.dynamic.title('视频美化页签功能测试')

        with allure.step("视频美化"):
            folder_path = os.path.join(CommonCasePdf.find_desktop_by_reg(), 'videofile')
            video_bea = wadlib(CommonCaseVideo.get_conversion_process_path())
            CommonCaseVideo.window_top(video_bea.driver.title)
            utils.perform_sleep(1)
            video_bea.click_find_by_name('视频美化')
            video_bea.click_find_by_name("添加文件")
            video_bea.input_find_by_classname("Edit", os.path.join(folder_path, "demo.mp4"))
            video_bea.click_find_by_name("打开(O)")
            CommonCaseVideo.click_by_pic(CommonCaseVideo.video_optimize_settings)
            assert video_bea.isElementPresent(By.NAME, "美化设置"), "进入美化设置界面失败！"
            video_bea.click_find_by_name("老旧")
            video_bea.click_find_by_name("确定")
            file_name = CommonCaseVideo.update_name()
            video_bea.click_find_by_name("全部优化")
            CommonCaseVideo.conversion_spend_time()
            con_file = CommonCaseVideo.get_file_name(folder_path)
            assert file_name == con_file[-1].split(".")[0], "视频美化失败！"
            log.log_pass("视频美化成功！")
            video_bea.click_find_elements_by_property(By.CLASS_NAME, 'CustomButton', 4, "关闭")
            utils.perform_sleep(2)
            assert video_bea.driver_exist(), "关闭视频转换器失败！"
            log.log_info("关闭视频转换器成功！")

    @allure.story('音频转换')
    @pytest.mark.flaky(reruns=1)
    def test_music_con(self):
        allure.dynamic.description(
            '\t1.打开视频转换器\n'
            '\t2.添加视频文件\n'
            '\t2.点击全部美化\n'
        )
        allure.dynamic.title('音频转换页签功能测试')

        with allure.step("音频转换"):
            folder_path = os.path.join(CommonCasePdf.find_desktop_by_reg(), 'videofile')
            if os.path.exists(os.path.join(folder_path, "demo_转换.mp3")):
                os.remove(os.path.join(folder_path, "demo_转换.mp3"))
            music_con = wadlib(CommonCaseVideo.get_conversion_process_path())
            CommonCaseVideo.window_top(music_con.driver.title)
            utils.perform_sleep(1)
            music_con.click_find_by_name("视频转换")
            music_con.click_find_by_name("音频转换")
            music_con.click_find_by_name("添加文件")
            music_con.input_find_by_classname("Edit", os.path.join(folder_path, "demo.mp4"))
            music_con.click_find_by_name("打开(O)")
            music_con.click_find_by_name("全部转换")
            CommonCaseVideo.conversion_spend_time()
            con_file = CommonCaseVideo.get_file_name(folder_path)
            assert con_file[-1] == "demo_转换.mp3", "转换失败！"
            log.log_pass("mp4转换成mp3成功！")
            music_con.click_find_elements_by_property(By.CLASS_NAME, 'CustomButton', 4, "关闭")
            utils.perform_sleep(2)
            assert music_con.driver_exist(), "关闭视频转换器失败！"
            log.log_info("关闭视频转换器成功！")


if __name__ == '__main__':
    pytest.main("-v -s")
