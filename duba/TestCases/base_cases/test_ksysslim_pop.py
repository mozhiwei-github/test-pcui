import allure
import pytest
from common import utils
from common.file_process import FileOperation
from common.log import log
from common.tools.duba_tools import DubaFiles
from duba.config import config
from common.tools import duba_tools
from duba.PageObjects.c_slimming_pre_swept_page import CSlimmingPreSweptPage
from duba.utils import close_duba_self_protecting, DubaFilePath


@pytest.fixture()
def error_kill_exe():
    yield 1
    utils.kill_process_by_name("ksysslim.exe")
    utils.kill_process_by_name("kfixstar.exe")
    utils.kill_process_by_name("kxetray.exe")


@allure.epic(f'毒霸C盘瘦身右下角推广泡泡基础场景测试（{config.ENV.value}）')
@allure.feature('场景：调起c盘瘦身右下角推广泡泡')
class TestKsysslimPop(object):
    @allure.story('1.C盘瘦身预扫泡基础场景')
    def test_ksysslim_base(self, error_kill_exe):
        allure.dynamic.description(
            '\t1.c盘瘦身白色泡泡检查\n'
            '\t2.c盘瘦身红色泡泡检查\n'
        )
        allure.dynamic.title('c盘瘦身推广泡基本功能')
        popdata_removelist = [DubaFiles.LAST_SHOW_TIME.value, DubaFiles.NO_SHOW_ANYMORE.value]  # 删除
        kplanetcache_removelist = [DubaFiles.PURE_VIP_NOAD_POP.value]
        ksyscfg_removelist = [DubaFiles.SCAN.value]

        with allure.step("step1：检查c盘瘦身白色泡泡基础功能"):
            close_duba_self_protecting()
            ksyspop = CSlimmingPreSweptPage()
            # 弹泡前准备操作
            duba_tools.rename_kpopcenter()

            # ksyscfg.ini 调整
            ks_fo = FileOperation(DubaFilePath.ksyscfg_file_path)
            ks_fo.del_section_by_list(ksyscfg_removelist)

            # popdata.ini 调整
            po_fo = FileOperation(DubaFilePath.popdata_file_path)
            po_fo.del_section_by_list(popdata_removelist)

            # kplanetcache.ini 调整
            kp_fo = FileOperation(DubaFilePath.kplanetcache_file_path)
            kp_fo.del_section_by_list(kplanetcache_removelist)
            kp_fo.add_section_by_list(kplanetcache_removelist)
            kp_fo.set_option(DubaFiles.PURE_VIP_NOAD_POP.value, DubaFiles.PARAM.value,
                             DubaFiles.WHITE_PARAM_VALUE.value)

            # 重启kxetray.exe,注意：用例结束后需要关闭kxetray进程，否则阻塞无法上传自动化报告
            duba_tools.restart_kxetray()

            # 白色泡泡检查
            ksyspop.pop_by_commandline()
            ret = ksyspop.check_white_bubble_style()
            assert ret, log.log_error("白泡泡组件样式异常", need_assert=False)
            log.log_pass("白泡泡组件样式正确")

            ret = ksyspop.check_white_bubble_release()
            assert ret, log.log_error("白泡泡释放按钮异常", need_assert=False)
            log.log_pass("白泡泡释放按钮正常")

            ksyspop.pop_by_commandline()
            ret = ksyspop.check_white_bubble_close()
            assert ret, log.log_error("白泡泡关闭按钮异常", need_assert=False)
            log.log_pass("白泡泡关闭按钮正常")

            ksyspop.pop_by_commandline()
            ret = ksyspop.check_white_bubble_never_notify()
            assert ret, log.log_error("白泡泡不再提醒功能异常", need_assert=False)
            log.log_pass("白泡泡不再提醒功能正常")

            # ksyspop.pop_by_commandline()
            # assert ksyspop.check_bubble_auto_close(), "白泡泡自动关闭异常"
            # log.log_pass("白泡泡自动关闭功能正常")

        with allure.step("step2：检查c盘瘦身红色泡泡基础功能"):
            # 弹泡前准备操作
            ks_fo = FileOperation(DubaFilePath.ksyscfg_file_path)
            ks_fo.del_section_by_list(ksyscfg_removelist)

            po_fo = FileOperation(DubaFilePath.popdata_file_path)
            po_fo.del_section_by_list(popdata_removelist)

            kp_fo = FileOperation(DubaFilePath.kplanetcache_file_path)
            kp_fo.del_section_by_list(kplanetcache_removelist)
            kp_fo.add_section_by_list(kplanetcache_removelist)
            sf = FileOperation(DubaFilePath.kplanetcache_file_path)
            sf.set_option(DubaFiles.PURE_VIP_NOAD_POP.value, DubaFiles.PARAM.value, DubaFiles.RED_PARAM_VALUE.value)

            # 红色泡泡检查
            ksyspop.pop_by_commandline()
            ret = ksyspop.check_red_bubble_style()
            assert ret, log.log_error("红泡泡组件样式异常", need_assert=False)
            log.log_pass("红泡泡组件样式正确")

            ret = ksyspop.check_red_bubble_release()
            assert ret, log.log_error("红泡泡释放按钮异常", need_assert=False)
            log.log_pass("红泡泡释放按钮正常")

            ksyspop.pop_by_commandline()
            ret = ksyspop.check_red_bubble_abandon_release()
            assert ret, log.log_error("红泡泡放弃释放按钮异常", need_assert=False)
            log.log_pass("红泡泡放弃释放按钮正常")

            ksyspop.pop_by_commandline()
            ret = ksyspop.check_red_bubble_close()
            assert ret, log.log_error("红泡泡关闭按钮异常", need_assert=False)
            log.log_pass("红泡泡关闭按钮正常")

            ksyspop.pop_by_commandline()
            ret = ksyspop.check_red_bubble_never_notify()
            assert ret, log.log_error("红泡泡不再提醒功能异常", need_assert=False)
            log.log_pass("红泡泡不再提醒功能正常")

            # ksyspop.pop_by_commandline()
            # assert ksyspop.check_bubble_auto_close(), "红泡泡自动关闭异常"
            # log.log_pass("红泡泡自动关闭功能正常")

            # 还原kpopcenter.dll
            duba_tools.recover_kpopcenter()


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
