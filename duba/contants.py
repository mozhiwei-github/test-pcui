from enum import unique, Enum, IntEnum


@unique
class Env(Enum):
    """测试环境"""
    TEST = "测试服"
    PRODUCTION = "正式服"


@unique
class UserType(Enum):
    """用户类型"""
    GUEST = "游客"  # 游客
    NON_VIP = "普通用户"  # 非会员（普通用户）
    COMMON_VIP = "普通会员"  # 普通会员
    DIAMOND_VIP = "钻石会员"  # 钻石会员
    SUPER_VIP = "超级会员"  # 超级会员
    HONOR_VIP = "荣耀会员"  # 荣誉会员（体验会员）
    QQ = "QQ用户会员" # QQ登录的会员

@unique
class PaySettingShow(IntEnum):
    VIP_CENTER = 1  # 会员中心套餐
    ONE_FOR_ONE_INSPECTION_SINGLE = 3  # 一对一体检按次套餐
    PHONE_DATA_RECOVERY = 4  # 数据恢复、照片恢复、手机恢复的兼容老会员的落地页
    VIP_CONTRACT = 5  # 纯签约套餐
    AD_BLOCKING = 7  # 广告净化套餐
    PRIVACY_CLEANUP = 30  # 隐私清理套餐
    ONE_FOR_ONE_INSPECTION_UNLIMITED = 31  # 1对1服务钻石会员套餐（电脑医生）
    DATA_RECOVERY = 34  # 数据恢复、照片恢复、手机恢复的兼容老会员的落地页
    FILE_SHREDDING = 35  # 文件粉碎
    PDF_CONVERSION = 36  # PDF转WORD/PDF转换（毒霸）
    C_DRIVE_CLEANUP = 37  # C盘瘦身
    DUBA_PICTURE = 42  # 金山看图
    SCREEN_RECORDING_MASTER = 43  # 录屏大师
    TEXT_TO_SPEECH = 49  # 文字转语音
    DOCUMENT_REPAIR = 53  # 文档修复独立支付页
    YOUHUI = 119  # 使用优惠券
    HOME1 = 285  # 家庭版1台非使用优惠券
    SYSTEM_DEBRIS_CLEANER = 73  # 系统碎片清理王独立支付页
    PAYMENT_PAGE_UNPAID_COUPON_UNUSED = 74  # 多次调起支付页未付费优惠券[未使用]
    PAYMENT_PAGE_UNPAID_COUPON_USED = 75  # 多次调起支付页未付费优惠券[使用]


# 会员支付pay_settings各个展示场景的对应值
PaySettingsInfo = {
    "会员中心": {  # 会员中心套餐
        "show": [PaySettingShow.VIP_CENTER.value]
    },
    "垃圾清理": {  # 会员中心套餐
        "show": [PaySettingShow.VIP_CENTER.value]
    },
    "C盘瘦身专家": {  # C盘瘦身
        "show": [PaySettingShow.C_DRIVE_CLEANUP.value]
    },
    "超级隐私清理": {  # 隐私清理套餐
        "show": [PaySettingShow.PRIVACY_CLEANUP.value]
    },
    "右键菜单管理": {  # 会员中心套餐
        "show": [PaySettingShow.VIP_CENTER.value]
    },
    "数据恢复": {  # 数据恢复、照片恢复、手机恢复的新落地页
        "show": [PaySettingShow.DATA_RECOVERY.value]
    },
    "弹窗拦截": {  # 广告净化套餐
        "show": [PaySettingShow.AD_BLOCKING.value]
    },
    "毒霸PDF转换": {  # PDF转WORD/PDF转换（毒霸）
        "show": [PaySettingShow.PDF_CONVERSION.value]
    },
    "文件粉碎": {  # 文件粉碎
        "show": [PaySettingShow.FILE_SHREDDING.value]
    },
    "纯净无广告": {  # 会员中心套餐
        "show": [PaySettingShow.VIP_CENTER.value]
    },
    "浏览器主页修复": {  # 会员中心套餐
        "show": [PaySettingShow.VIP_CENTER.value]
    },
    "文档修复": {  # 文档修复独立支付页
        "show": [PaySettingShow.DOCUMENT_REPAIR.value]
    },
    "文档卫士": {  # 会员中心套餐
        "show": [PaySettingShow.VIP_CENTER.value]
    },
    "隐私无痕模式": {  # 会员中心套餐
        "show": [PaySettingShow.VIP_CENTER.value]
    },
    "隐私护盾": {  # 会员中心套餐
        "show": [PaySettingShow.VIP_CENTER.value]
    },
    "人工服务": {  # 一对一体检按次套餐、1对1服务钻石会员套餐（电脑医生）
        "show": [
            PaySettingShow.ONE_FOR_ONE_INSPECTION_SINGLE.value,
            PaySettingShow.ONE_FOR_ONE_INSPECTION_UNLIMITED.value
        ]
    },
    "VIP客服答疑": {  # 会员中心套餐
        "show": [PaySettingShow.VIP_CENTER.value]
    },
    "专属主题皮肤": {  # 会员中心套餐
        "show": [PaySettingShow.VIP_CENTER.value]
    },
    "文件夹加密": {  # 会员中心套餐
        "show": [PaySettingShow.VIP_CENTER.value]
    },
    "手机数据恢复": {  # 数据恢复、照片恢复、手机恢复的兼容老会员的落地页
        "show": [PaySettingShow.PHONE_DATA_RECOVERY.value]
    },
    "录屏大师": {  # 录屏大师
        "show": [PaySettingShow.SCREEN_RECORDING_MASTER.value]
    },
    "网络测速": {  # 会员中心套餐
        "show": [PaySettingShow.VIP_CENTER.value]
    },
    "文字转语音": {  # 文字转语音
        "show": [PaySettingShow.TEXT_TO_SPEECH.value]
    },
    "自动清理加速": {  # 会员中心套餐
        "show": [PaySettingShow.VIP_CENTER.value]
    },
    "系统碎片清理王": {  # 系统碎片清理王独立支付页
        "show": [PaySettingShow.SYSTEM_DEBRIS_CLEANER.value]
    },
    "电脑加速": {  # 会员中心套餐
        "show": [PaySettingShow.VIP_CENTER.value]
    },
    "开机加速": {  # 会员中心套餐
        "show": [PaySettingShow.VIP_CENTER.value]
    },
    "加速球": {  # 会员中心套餐
        "show": [PaySettingShow.VIP_CENTER.value]
    },
    "毒霸PDF阅读器": {  # PDF转WORD/PDF转换（毒霸）
        "show": [PaySettingShow.PDF_CONVERSION.value]
    },
    "毒霸看图": {  # 金山看图
        "show": [PaySettingShow.DUBA_PICTURE.value]
    },
    "毒霸流程图": {  # PDF转WORD/PDF转换（毒霸）
        "show": [PaySettingShow.PDF_CONVERSION.value]
    },
    "优惠券": {
        "show": [PaySettingShow.YOUHUI.value]
    },
    "家庭版1台": {
        "show": [PaySettingShow.HOME1.value]
    }
}


@unique
class DubaApiHeaders(Enum):
    """毒霸api请求头"""
    NEWVIP_HEADERS = {
        "Content-Type": "application/json",
        "Host": "newvip.duba.net",
        "X-Cf-Debug-Key": "6323b064bf"
    }
    FAKE_PAY_SERVER_HEADERS = {
        "Content-Type": "application/json",
        "Host": "fakepayserver.aix-test-k8s.iweikan.cn"
    }
    NEWVIP_DEV2_HEADERS = {
        "Content-Type": "application/json",
        "X-Cm-Admin-Auth": "ff657a9f4f80ffaa"
    }
    WXPAY_DEDUCTION_TRIGGER_HEADERS = {
        "Content-Type": "application/json",
        "X-Cm-Admin-Auth": "98ae341851b6e4fa"
    }

@unique
class Accelerate_module(Enum):
    """电脑加速列表各项名称与脚本logo名称匹配"""
    module_dict = [
    # 开机加速
        ("KJJS","start_accelerate_logo.png"),
    # 运行加速
        ("YXJS","run_accelerate_logo.png"),
    # 系统加速
        ("XTJS","system_accelerate_logo.png"),
    # Win10提速
        ("WINTS","win_accelerate_logo.png")

    ]

@unique
class Software_manage_operation(Enum):
    """软件管家不同操作按钮图片匹配"""
    operation_dict = [
        ("SEMINSTALL", "seminstall_button.png"),
        ("INSTALL", "install_button.png"),
        ("UNINSTALL", "uninstall_button.png"),
        ("UPDATE", "update_button.png")
    ]

@unique
class Keniu_Office_QQAccount(Enum):
    """可牛办公QQ登录账号密码"""
    QQNUM = "2327753400"
    QQPWD = "mozhiweidemima55"

@unique
class TaskRunMode(Enum):
    """任务运行方式"""
    LOCAL = "本机"
    REMOTE = "远程"

@unique
class ChromeCachePath(Enum):
    CHROMECACHEPATH = r"C:\Users\admin\AppData\Local\Google\Chrome\User Data\GrShaderCache"

@unique
class DubaVersion(Enum):
    EXCEPTVERSION = "2023"





