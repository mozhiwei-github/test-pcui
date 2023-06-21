from common.tools.magiccube_tools import *
import allure
import pytest
from common import utils
from common.contants import Host
from common.log import log
from common.tools.duba_tools import get_dg_install_reg, set_reg, find_dg_reg, dg_install_reg_remove
from duba.PageObjects.klsoftmgr_page import pull_package, OnCloudPdf, QQMusic, ElephantNote, SofewareUninstallPage, \
    RogueSoftWareMsg
from duba.config import config
from duba.utils import login_normal_user, login_super_vip, close_dg_protect_after_checkreg, \
    close_duba_protect_after_checkreg


# @pytest.fixture()
# def before():
#     utils.modify_host(Host.DUBA_SERVER_TEST.value)
#     print("------->before!!!!!!!!!!!!!!!!!!!!!!!!!!")

@pytest.fixture()
def error_kill_exe():
    dg_reg_value = get_dg_install_reg()
    yield 1
    close_duba_protect_after_checkreg()
    close_dg_protect_after_checkreg()
    utils.kill_process_by_name("kxetray.exe")
    utils.kill_process_by_name("klsoftmgr.exe")
    utils.kill_process_by_name("QQMusicUninst.exe")
    utils.kill_process_by_name("QQMusicSetup.exe")
    utils.kill_process_by_name("Heinote_uninst.exe")
    utils.kill_process_by_name("heinote_v3.2.1.0_gw_001.exe")
    utils.kill_process_by_name("PDFOnCloud_setup.exe")
    utils.kill_process_by_name("ElephantNoteSetup.exe")
    print(dg_reg_value)
    set_reg(repa=find_dg_reg(), kname="AppPath", val=dg_reg_value)



@allure.epic(f'毒霸卸载王基础场景测试（{config.ENV.value}）')
@allure.feature('场景：打开毒霸卸载王界面')
# @pytest.mark.usefixtures("before")
class TestKlsoftmgrBase(object):

    # def setup_class(self):
    #     utils.modify_host(Host.DUBA_SERVER_TEST.value)
    #     print("------->setup_class")

    @allure.story('1.毒霸卸载王基础场景')
    def test_klsoftmgr_base(self, error_kill_exe):
        allure.dynamic.description(
            '\t1.安装流氓软件\n'
            '\t2.检查一键卸载\n'
            '\t3.检查强力卸载\n'
            '\t4.弹泡校验\n'
        )
        allure.dynamic.title('毒霸卸载王基础功能')

        with allure.step("step0：切换到毒霸服务端测试服"):
            utils.modify_host(Host.DUBA_SERVER_TEST.value)
            log.log_info("切换到毒霸服务端测试服")

        with allure.step("step1：拉下流氓软件安装包，并安装"):
            res = pull_package()
            assert res, log.log_error("下拉流氓软件安装包失败！！", need_assert=False)

            onclpdf = OnCloudPdf()
            onclpdf.install()

            qqmu = QQMusic()
            qqmu.install()

            eleno = ElephantNote()
            eleno.install()

            log.log_pass("相关流氓软件已安装")

        with allure.step("step1：检查右下角推广泡泡"):
            close_duba_protect_after_checkreg()
            close_dg_protect_after_checkreg()
            dg_reg_value = get_dg_install_reg()
            dg_install_reg_remove()
            softmgr = SofewareUninstallPage()
            login_normal_user(softmgr)  # 右下角泡需要非会员，故登录普通用户
            res = softmgr.check_lower_right_corner_pop()
            assert res, log.log_error("右下角推广泡泡功能异常", need_assert=False)
            log.log_pass("右下角推广泡泡功能正常")

        with allure.step("step2：检查一键卸载（样本：qq音乐）"):
            # login_super_vip(softmgr, "button_login.png")  # 以下功能需要会员
            login_super_vip(softmgr, username="golanger030", password="kingsoft")  # 以下功能需要会员
            softmgr.click_lately_install()
            res = softmgr.check_normal_uninstall_btn(RogueSoftWareMsg.QQMUSCIPNG.value, RogueSoftWareMsg.QQMUSCI.value)
            softmgr.select_reuninstall_btn(RogueSoftWareMsg.QQMUSCIPNG.value)
            softmgr.click_normal_uninstall(RogueSoftWareMsg.QQMUSCIPNG.value)
            assert res, log.log_error("一键卸载识别异常，请咨询运营规则", need_assert=False)
            res = qqmu.uninstall()
            assert res, log.log_error("一点击一键卸载无调起卸载程序", need_assert=False)
            log.log_pass("一键卸载功能正常")

        with allure.step("step3：检查本地引擎（检查回扫泡）"):
            get_magiccube_tools("duba")
            path = find_dubapath_by_reg()
            decode_magiccube(path, "duba")
            time = get_magicRaw_value_by_section("duba", "KLOSTMGR_INSTALL_MONITOT_SCAN_MIN_LOOP_MINUTES", key_value_target_key="scan_min_loop_minute")[0]
            res = softmgr.check_local_engine(time=(time*60+10), obj=qqmu)
            assert res, log.log_error("本地引擎功能异常", need_assert=False)
            log.log_pass("本地引擎功能正常")

        with allure.step("step4：检查强力卸载（样本：小象笔记本）"):
            softmgr.pre_open()
            softmgr.click_lately_install()
            res = softmgr.check_strong_uninstall_btn(RogueSoftWareMsg.XIAOXIANPNG.value,
                                                     RogueSoftWareMsg.XIAOXIAN.value)
            assert res, log.log_error("强力卸载识别异常，请咨询运营规则", need_assert=False)
            softmgr.select_reuninstall_btn(RogueSoftWareMsg.XIAOXIANPNG.value)
            softmgr.click_strong_uninstall(RogueSoftWareMsg.XIAOXIANPNG.value)

        with allure.step("step5：检查拦截安装泡泡"):
            softmgr.pre_open()
            eleno.install()
            res = softmgr.check_intercept_pop()
            assert res, log.log_error("拦截安装泡泡功能异常", need_assert=False)
            log.log_pass("拦截安装泡泡功能正常")

        with allure.step("step6：检查防重装列表"):
            softmgr.pre_open()
            res = softmgr.click_anti_reunnistall_list()
            assert res, log.log_error("无法打开防重装列表", need_assert=False)
            softmgr.cancel_all_reunistall()
            softmgr.close_anti_reunnistall_list()
            log.log_pass("检查防重装列功能正常")


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
