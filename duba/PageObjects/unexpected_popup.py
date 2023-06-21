# --coding = 'utf-8' --
from enum import Enum, unique
from common import utils
from common.log import log

from common.tools.base_tools import get_page_shot

"""非预期弹窗处理"""


def get_shot_path(shot_name):
    return get_page_shot("unexpected_popup", shot_name)


@unique
class UnexpectedPopupInfo(Enum):
    TIME_LIMITED_BENEFITS = {  # 限时福利 https://twiki.cmcm.com/pages/viewpage.action?pageId=128713098
        "info": "限时福利",
        "logo_shot": get_shot_path("time_limited_benefits.png"),
        "exit_shot": get_shot_path("time_limited_benefits_exit.png"),
        "find_sim": 0.9,
        "find_retry": 3,
        "click_sim": 0.8,
        "click_retry": 2,
    }
    PDF_RED_PACKET = {  # 毒霸PDF红包
        "info": "毒霸PDF红包",
        "logo_shot": get_shot_path("pdf_red_packet_logo.png"),
        "exit_shot": get_shot_path("pdf_red_packet_exit.png"),
        "find_sim": 0.9,
        "find_retry": 2,
        "click_sim": 0.8,
        "click_retry": 2,
    }
    EXIT_VIP_UPDATE = {  # 升级会员弹窗
        "info": "金山毒霸会员升级",
        "logo_shot": [get_shot_path("vip_update_tab_logo_1.png"), get_shot_path("vip_update_tab_logo_2.png"),
                      get_shot_path("vip_update_tab_logo_3.png"), get_shot_path("vip_update_tab_logo_4.png"),
                      get_shot_path("vip_update_tab_logo_5.png")],
        "exit_shot": get_shot_path("exit_vip_update.png"),
        "find_sim": 0.8,
        "find_retry": 2,
        "click_sim": 0.8,
        "click_retry": 2,
    }
    COUPON = {  # 优惠券弹窗 https://twiki.cmcm.com/pages/viewpage.action?pageId=128713098
        "info": "恭喜您获得优惠券",
        "logo_shot": get_shot_path("coupon.png"),
        "exit_shot": get_shot_path("exit_coupon.png"),
        "find_sim": 0.8,
        "find_retry": 2,
        "click_sim": 0.8,
        "click_retry": 2,
    }
    QUICK_LOGIN = {  # 快速登录
        "info": "快速登录",
        "logo_shot": get_shot_path("quick_login_tab_logo.png"),
        "exit_shot": get_shot_path("quick_login_exit_button.png"),
        "find_sim": 0.9,
        "find_retry": 2,
        "click_sim": 0.9,
        "click_retry": 2,
    }
    VIP_EXCLUSIVE_RIGHTS = {  # 毒霸会员专属权益
        "info": "毒霸会员专属权益",
        "logo_shot": get_shot_path("vip_exclusive_rights_tab_logo.png"),
        "exit_shot": get_shot_path("vip_exclusive_rights_exit_button.png"),
        "find_sim": 0.9,
        "find_retry": 2,
        "click_sim": 0.9,
        "click_retry": 2,
    }
    VIP_SURPRISE_SMASH_EGG = {  # 会员惊喜砸蛋 https://twiki.cmcm.com/pages/viewpage.action?pageId=160858123
        "info": "会员惊喜砸蛋",
        "logo_shot": get_shot_path("vip_surprise_smash_egg_tab_logo.png"),
        "exit_shot": get_shot_path("vip_surprise_smash_egg_exit_button.png"),
        "find_sim": 0.9,
        "find_retry": 2,
        "click_sim": 0.9,
        "click_retry": 2,
    }
    SERVICE_SCORE = {  # 服务评分 https://twiki.cmcm.com/pages/viewpage.action?pageId=158302249
        "info": "服务评分",
        "logo_shot": get_shot_path("service_score_tab_logo.png"),
        "exit_shot": get_shot_path("service_score_exit_button.png"),
        "find_sim": 0.9,
        "find_retry": 2,
        "click_sim": 0.9,
        "click_retry": 2,
    }
    QUICK_LINK = {  # 创建桌面快捷方式
        "info": "快捷方式",
        "logo_shot": get_shot_path("create_quick_link_tab.png"),
        "exit_shot": get_shot_path("close_quick_link.png"),
        "find_sim": 0.9,
        "find_retry": 2,
        "click_sim": 0.9,
        "click_retry": 2,
    }
    PERFECT_OFFICE_RED_PACKET_618 = {  # 可牛办公618红包
        "info": "可牛办公618红包",
        "logo_shot": get_shot_path("perfect_office_red_packet_618.png"),
        "exit_shot": get_shot_path("exit_perfect_office_red_packet_618.png"),
        "find_sim": 0.9,
        "find_retry": 2,
        "click_sim": 0.9,
        "click_retry": 2,
    }
    PERFECT_OFFICE_QUICK_LINK = {  # 可牛办公退出创建快捷方式提示
        "info": "可牛办公退出创建快捷方式提示",
        "logo_shot": get_shot_path("perfect_office_quicklink.png"),
        "exit_shot": get_shot_path("cancel_perfect_office_quicklink.png"),
        "find_sim": 0.9,
        "find_retry": 2,
        "click_sim": 0.9,
        "click_retry": 2,
    }


def unexpected_popup_record(func):
    def dec(*args, **kwargs):
        popup_type = args[0]
        assert popup_type in UnexpectedPopupInfo, f"找不到该弹窗类型：{popup_type}"
        info = popup_type.value["info"]

        if info:
            log.log_info(f"正在处理{info}弹窗")
            result = func(*args, **kwargs)
            if result:
                log.log_info(f"已执行点击退出{info}弹窗")
            else:
                log.log_info(f"未检测到{info}弹窗")
        else:
            result = func(*args, **kwargs)
        return result

    return dec


# 用于处理非预期弹出窗口的关闭
class UnexpectedPopup:
    @staticmethod
    @unexpected_popup_record
    def popup_process(popup_type: UnexpectedPopupInfo, find_retry=None, sim_no_reduce=True, hwnd=None):
        """
        :param popup_type 弹窗类型枚举
        :param find_retry 查找弹窗标识的重试次数
        :param sim_no_reduce 是否找到相似度查找
        :param hwnd 指定窗口内寻图的窗口句柄
        """
        shot_info = popup_type.value

        if not find_retry:
            find_retry = shot_info["find_retry"]

        logo_shot = shot_info["logo_shot"]
        logo_shot_list = []
        if type(logo_shot) == str:
            logo_shot_list.append(logo_shot)
        elif type(logo_shot) == list:
            logo_shot_list = logo_shot

        for shot in logo_shot_list:
            # 查找弹窗
            if utils.find_element_by_pic(
                    shot,
                    sim=shot_info["find_sim"],
                    retry=find_retry,
                    sim_no_reduce=sim_no_reduce,
                    hwnd=hwnd
            )[0]:
                # 关闭弹窗
                utils.click_element_by_pic(
                    shot_info["exit_shot"],
                    sim=shot_info["click_sim"],
                    retry=shot_info["click_retry"],
                    hwnd=hwnd
                )
                return True
        return False


if __name__ == '__main__':
    UnexpectedPopup.popup_process(UnexpectedPopupInfo.TIME_LIMITED_BENEFITS)
