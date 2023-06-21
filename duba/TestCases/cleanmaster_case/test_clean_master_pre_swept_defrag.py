import allure
import pytest

from common.log import log
from duba.PageObjects.clean_master_pre_swept_page import CleanMasterPreSweptBubble, set_duba_reg, set_dg_reg
from duba.config import config


@allure.epic(f'清理大师, 碎片清理-预扫泡测试（{config.ENV.value}）')
class TestduliKsysslimInterfacePackage(object):
    @allure.story('1.清理大师, 碎片清理-预扫泡测试')
    def test_ksysslim_base(self):
        allure.dynamic.description(
            '\t1.碎片清理-预扫泡检查\n'
        )
        allure.dynamic.title('碎片清理-预扫泡测试')
        with allure.step("step0：初始化预扫泡类和清除精灵和毒霸注册表"):
            pre_swept = CleanMasterPreSweptBubble()
            # 关闭精灵自保护
            pre_swept.close_dg_protect()

            # 关闭毒霸自保护
            pre_swept.close_duba_protect()

            duba_reg_value = pre_swept.get_duba_install_reg()
            dg_reg_value = pre_swept.get_dg_install_reg()

            pre_swept.install_reg_remove()

        with allure.step("step1：碎片清理预扫泡检查"):
            pre_swept.install_reg_remove()
            pre_swept.popdata_pop_config(defrag_switch="1")
            pre_swept.kvipapp_setting_pop_cconfig(this_pop_name="DefragPop")
            pre_swept.restart_cmcore()
            retpa = pre_swept.close_preswept_kfixstar_pop(name="碎片清理")
            assert retpa, log.log_error("碎片清理预扫泡弹出失败", need_assert=False)
            log.log_pass("碎片清理预扫泡，弹出功能正常")

        if duba_reg_value is not None:
            set_duba_reg(value=duba_reg_value)
        if dg_reg_value is not None:
            set_dg_reg(value=dg_reg_value)


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
