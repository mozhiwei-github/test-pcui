#!/usr/bin/evn python
# --coding = 'utf-8' --
# Python Version 3.8
import os

page_shot_path = os.path.join(os.getcwd(), "duba", "PageShot")

# 标签key必须与页面类名一致
page_resource = {
    "main_page": {
        "page_class": "kismain{1ACD30B1-18F3-4f4d-B52D-4709D099998C}",
        "page_title": "金山毒霸",
        "page_desc": "毒霸主界面",
        "process_path": None,
        "process_name": "kxetray.exe",
        "entry_pic": None,
        "tab_pic": os.path.join(page_shot_path, "main_page", "tab_duba_logo.png"),
        "exit_pic": os.path.join(page_shot_path, "main_page", "exit_duba.png")
    },
    "PopupInterceptPage": {
        "page_class": "KDubaSoftPurifierWClass2",
        "page_title": "金山毒霸弹窗拦截",
        "page_desc": "弹窗拦截",
        "process_path": None,
        "process_name": "ksoftpurifier.exe",
        "entry_pic": None,
        "tab_pic": [os.path.join(page_shot_path, "popup_intercept_page", "tab.png"),
                    os.path.join(page_shot_path, "popup_intercept_page", "tab_2.png"),
                    os.path.join(page_shot_path, "popup_intercept_page", "tab_3.png")],
        "exit_pic": os.path.join(page_shot_path, "popup_intercept_page", "exit.png")
    },
    "vip_page": {
        "page_class": "UserProfile",
        "page_title": "毒霸会员中心",
        "page_desc": "毒霸会员中心",
        "process_path": None,
        "process_name": "knewvip.exe",
        "entry_pic": None,
        "tab_pic": [os.path.join(page_shot_path, "vip_page", "tab_vip_logo.png"),
                    os.path.join(page_shot_path, "vip_page", "tab_vip_logo_2.png")],
        "exit_pic": [os.path.join(page_shot_path, "vip_page", "exit_vip.png"),
                     os.path.join(page_shot_path, "vip_page", "exit_vip_2.png")]
    },
    "vip_kaitong_page": {
        "page_class": "UserProfile",
        "page_title": "毒霸会员中心",
        "page_desc": "开通毒霸会员中心",
        "process_path": None,
        "process_name": "knewvip.exe",
        "entry_pic": None,
        "tab_pic": os.path.join(page_shot_path, "vip_page", "tab_vip_update_logo.png"),
        "exit_pic": os.path.join(page_shot_path, "vip_page", "exit_vip.png")
    },
    "LoginPage": {
        "page_desc": "登录",
        "process_path": None,
        "process_name": None,
        "entry_pic": None,
        "tab_pic": [os.path.join(page_shot_path, "login_page", "tab_login_logo.png"),
                    os.path.join(page_shot_path, "login_page", "tab_login_logo_2.png")],
        "exit_pic": os.path.join(page_shot_path, "login_page", "exit_login.png")
    },
    "DataRecoveryPage": {
        "page_class": "ATL:004A4E40",
        "page_title": "金山数据恢复",
        "page_desc": "数据恢复",
        "process_path": None,  # 进程地址
        "process_name": "kavdr.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "data_recovery_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "data_recovery_page", "exit_button.png")  # 页面关闭按钮图
    },
    "CSlimmingPage": {
        "page_class": "system slim class",
        "page_title": "C盘瘦身专家",
        "page_desc": "C盘瘦身专家",
        "process_path": None,  # 进程地址
        "process_name": "ksysslim.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": [os.path.join(page_shot_path, "c_slimming_page", "tab_logo_2.png"),
                    os.path.join(page_shot_path, "c_slimming_page", "tab_logo.png")],  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "c_slimming_page", "exit.png")  # 页面关闭按钮图
    },
    "DgPage": {
        "page_class": "CMainFrm",
        "page_title": "驱动精灵",
        "page_desc": "驱动精灵",
        "process_path": None,  # 进程地址
        "process_name": "drivergenius.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "dg_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "dg_page", "exit.png")  # 页面关闭按钮图
    },
    "dgCSlimmingPage": {
        "page_class": "SysSlim_{76FD9E1D-79BB-49b6-9B11-1CEC4ABB2C51}",
        "page_title": "C盘瘦身专家",
        "page_desc": "C盘瘦身专家",
        "process_path": None,  # 进程地址
        "process_name": "ksysslim.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": [os.path.join(page_shot_path, "c_slimming_page", "tab_logo_2.png"),
                    os.path.join(page_shot_path, "c_slimming_page", "tab_logo.png")],  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "c_slimming_page", "exit.png")  # 页面关闭按钮图
    },
    "baibaoxiang_page": {
        "page_desc": "百宝箱",
        "process_path": None,  # 进程地址
        "process_name": "kxetray.exe",  # 进程名
        "entry_pic": [os.path.join(page_shot_path, "baibaoxiang_page", "entry_baibaoxiang.png"),
                      os.path.join(page_shot_path, "baibaoxiang_page", "entry_baibaoxiang_new.png")],  # 功能入口图片
        "tab_pic": [os.path.join(page_shot_path, "baibaoxiang_page", "tab_baibaoxiang.png"),
                    os.path.join(page_shot_path, "baibaoxiang_page", "tab_baibaoxiang_new.png")],  # 页面tab图
        "exit_pic": [os.path.join(page_shot_path, "baibaoxiang_page", "exit_baibaoxiang.png"),
                     os.path.join(page_shot_path, "baibaoxiang_page", "exit_baibaoxiang_new.png")]  # 页面关闭按钮图
    },
    "FileShreddingPage": {
        "page_class": "{1F68723B-A074-4539-A7CA-C9583C025F31}",
        "page_title": "金山文件粉碎器",
        "page_desc": "文件粉碎",
        "process_path": None,  # 进程地址
        "process_name": "kfiledestroy64.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "file_shredding_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "file_shredding_page", "exit_button.png")  # 页面关闭按钮图
    },
    "PDFConvertPage": {
        "page_class": "pdfconvert_{4C8FDCC8-3B12-4617-B081-CC950F8389EC}_1",
        "page_title": "PDF转换器",
        "page_desc": "PDF转换",
        "process_path": None,  # 进程地址
        "process_name": "pdfconverter.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "pdf_convert_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "pdf_convert_page", "exit_button.png")  # 页面关闭按钮图
    },
    "pure_office_page": {
        "page_desc": "纯净办公",
        "process_path": None,  # 进程地址
        "process_name": None,  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "pure_office_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": None  # 页面关闭按钮图
    },
    "document_weishi_page": {
        "page_desc": "文档卫士",
        "process_path": None,  # 进程地址
        "process_name": None,  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "pure_office_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": None  # 页面关闭按钮图
    },
    "private_weishi_page": {
        "page_desc": "隐私卫士",
        "process_path": None,  # 进程地址
        "process_name": None,  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "pure_office_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": None  # 页面关闭按钮图
    },
    "PrivacyCleanerPage": {
        "page_class": "kprivacy__{F4EF0303-450D-4e49-8B9F-9B13E4145719}",
        "page_title": "金山毒霸-超级隐私清理",
        "page_desc": "超级隐私清理",
        "process_path": None,  # 进程地址
        "process_name": "kprcycleaner.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": [os.path.join(page_shot_path, "privacy_cleaner_page", "tab_logo.png"),
                    os.path.join(page_shot_path, "privacy_cleaner_page", "tab_logo1.png"),
                    os.path.join(page_shot_path, "privacy_cleaner_page", "tab_logo2.png")],  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "privacy_cleaner_page", "exit_button.png")  # 页面关闭按钮图
    },
    "FileProtectPage": {
        "page_class": "kui_{091E5C47-A818-430A-B5BA-690AF3779960}",
        "page_title": "文件保护",
        "page_desc": "文件夹加密",
        "process_path": None,  # 进程地址
        "process_name": "kfp.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "file_protect_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "file_protect_page", "exit_button.png")  # 页面关闭按钮图
    },
    "RightMenuMgrPage": {
        "page_class": "rightmenudlg__{98443C33-8349-4c6a-869F-0313DCF628F4}",
        "page_title": "右键菜单管理",
        "page_desc": "右键菜单管理",
        "process_path": None,  # 进程地址
        "process_name": "krightmenumgr.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "right_menu_mgr_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "right_menu_mgr_page", "exit_button.png")  # 页面关闭按钮图
    },
    "BrowserHomeProtectPage": {
        "page_class": "khomefix__{BFFCFBF4-D000-4c5c-9D56-76A51E900FF8}",
        "page_title": "浏览器主页修复",
        "page_desc": "浏览器修复",
        "process_path": None,  # 进程地址
        "process_name": "khomeprotectvip.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "browser_home_protect_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "browser_home_protect_page", "exit_button.png")  # 页面关闭按钮图
    },
    "DocumentRepairPage": {
        "page_class": "ATL:004A31B8",
        "page_title": "金山文档修复大师",
        "page_desc": "文档修复",
        "process_path": None,  # 进程地址
        "process_name": "documentrepair.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "document_repair_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "document_repair_page", "exit_button.png")  # 页面关闭按钮图
    },
    "DocumentProtectPage": {
        "page_class": "kdocprotect__{34ABC924-87BF-41b7-9C65-ECA46E9544D9}",
        "page_title": "文档卫士",
        "page_desc": "文档保护",
        "process_path": None,  # 进程地址
        "process_name": "kdocprotect.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "document_protect_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "document_protect_page", "exit_button.png")  # 页面关闭按钮图
    },
    "PrivacyShieldPage": {
        "page_class": "kprivacyshield__{1CAD7361-F4E0-4ffe-ACDC-B3BE820B270B}",
        "page_title": "隐私护盾",
        "page_desc": "隐私护盾",
        "process_path": None,  # 进程地址
        "process_name": "kprivacyshield.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "privacy_shield_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "privacy_shield_page", "exit_button.png")  # 页面关闭按钮图
    },
    "PrivacyNoTracePage": {
        "page_class": "kprivacynotrace__{AEF8260E-946B-4f47-9882-9786602206EE}",
        "page_title": "隐私无痕模式",
        "page_desc": "隐私无痕模式",
        "process_path": None,  # 进程地址
        "process_name": "kprcynotrace.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "privacy_no_trace_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "privacy_no_trace_page", "exit_button.png")  # 页面关闭按钮图
    },
    "FastPicturePage": {
        "page_class": "db_Fastpic_{CAC78C77-BC1C-456d-A26A-57E1B59B18CC}",
        "page_title": "毒霸看图",
        "page_desc": "毒霸看图",
        "process_path": None,  # 进程地址
        "process_name": "fastpic.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "fast_picture_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "fast_picture_page", "exit_button.png")  # 页面关闭按钮图
    },
    "PictureBeautificationPage": {
        "page_class": "ATL:006FE7A0",
        "page_title": None,
        "page_desc": "图片美化（毒霸看图）",
        "process_path": None,  # 进程地址
        "process_name": "fastpic.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "fast_picture_page", "picture_beautification_tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "fast_picture_page", "picture_beautification_exit_button.png")
        # 页面关闭按钮图
    },
    "ScreenRecordPage": {
        "page_class": "SOUIHOST",
        "page_title": "毒霸录屏大师",
        "page_desc": "录屏大师",
        "process_path": None,  # 进程地址
        "process_name": "jsrecord.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "screen_record_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "screen_record_page", "exit_button.png")  # 页面关闭按钮图
    },
    "NetworkSpeedPage": {
        "page_class": "KDubaNetWorkSpeedWClass",
        "page_title": "网络测速",
        "page_desc": "网络测速",
        "process_path": None,  # 进程地址
        "process_name": "knetworkspeed.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "network_speed_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "network_speed_page", "exit_button.png")  # 页面关闭按钮图
    },
    "TextToVoicePage": {
        "page_class": "SOUIHOST",
        "page_title": "毒霸文字转语音",
        "page_desc": "文字转语音",
        "process_path": None,  # 进程地址
        "process_name": "jstexttovoice.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "text_to_voice_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "text_to_voice_page", "exit_button.png")  # 页面关闭按钮图
    },
    "TrashAutoCleanPage": {
        "page_class": "ktrashautoclean__{86C7EC62-DBD0-4de4-9109-F7D5E92C6E45}",
        "page_title": "自动清理加速",
        "page_desc": "自动清理垃圾",
        "process_path": None,  # 进程地址
        "process_name": "ktrashautoclean.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "trash_auto_clean_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "trash_auto_clean_page", "exit_button.png")  # 页面关闭按钮图
    },
    "overall_scan_page": {
        "page_desc": "全面扫描",
        "process_path": None,  # 进程地址
        "process_name": "kxetray.exe",  # 进程名
        "entry_pic": os.path.join(page_shot_path, "overall_scan_page", "entry_overall_scan.png"),  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "overall_scan_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "overall_scan_page", "exit_button.png")  # 页面关闭按钮图
    },
    "DefragPage": {
        "page_class": "KWebxMainWindow-{FD4C5916-356D-42D1-A0C5-EEC12ABF817A}",
        "page_title": "系统碎片清理王",
        "page_desc": "系统碎片清理王",
        "process_path": None,  # 进程地址
        "process_name": "kdefrag.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "defrag_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "defrag_page", "exit_button.png")  # 页面关闭按钮图
    },
    "SofewareUninstallPage": {
        "page_class": "{DC92FB0C-5BC3-4F20-AE6B-7364D265BA54}",
        "page_title": "软件卸载王",
        "page_desc": "软件卸载王",
        "process_path": None,  # 进程地址
        "process_name": "klsoftmgr.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "klsoftmgr_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "klsoftmgr_page", "exit_button.png")  # 页面关闭按钮图
    },
    "TeenModePage": {
        "page_class": "kteenmode__{878D0782-F2E3-4c5c-AB8A-0DD2CEF43DE9}",
        "page_title": "孩子守护王",
        "page_desc": "孩子守护王",
        "process_path": None,  # 进程地址
        "process_name": "kteenmode.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "teen_mode_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "teen_mode_page", "exit_button.png")  # 页面关闭按钮图
    },
    "PureNoADPage": {
        "page_class": "kpuernoad__{878D0782-F2E3-4c5c-AB8A-0DD2CEF43DE9}",
        "page_title": "纯净无广告",
        "page_desc": "纯净无广告",
        "process_path": None,  # 进程地址
        "process_name": "kpurenoad.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "pure_no_ad_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "pure_no_ad_page", "exit_button.png")  # 页面关闭按钮图
    },
    "PhoneRecoveryPage": {
        "page_class": "ATL:004A0510",
        "page_title": "金山手机数据恢复",
        "page_desc": "手机数据恢复",
        "process_path": None,  # 进程地址
        "process_name": "phonerecovery.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "phone_recovery_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "phone_recovery_page", "exit_button.png")  # 页面关闭按钮图
    },
    "SettingPage": {
        "page_desc": "主界面设置",
        "process_path": None,  # 进程地址
        "process_name": "kxetray.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "setting_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "setting_page", "exit_button.png")  # 页面关闭按钮图
    },
    "update_page": {
        "page_class": "ATL:004B9B40",
        "page_title": None,
        "page_desc": "升级程序",
        "process_path": None,  # 进程地址
        "process_name": "kislive.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "update_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "update_page", "exit_button.png")  # 页面关闭按钮图
    },
    "DriverManagerPage": {
        "page_class": "CMainFrm",
        "page_title": "驱动管理王",
        "page_desc": "驱动管理王",
        "process_path": None,  # 进程地址
        "process_name": "kdriver_manager.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "driver_manager_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "driver_manager_page", "exit_button.png")  # 页面关闭按钮图
    },
    "perfect_office_page": {
        "page_class": "KWebxMainWindow-{FD4C5916-356D-42D1-A0C5-EEC12ABF817A}",
        "page_title": "完美办公",
        "page_desc": "完美办公",
        "process_path": None,  # 进程地址
        "process_name": "ktemplate.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "perfect_office_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "perfect_office_page", "exit_button.png")  # 页面关闭按钮图
    },
    "CleanMasterPage": {
        "page_class": "SysSlim_{44FC9300-F03E-46d0-A143-2BF8F9362C46}",
        "page_title": "C盘瘦身",
        "page_desc": "清理大师",
        "process_path": None,  # 进程地址
        "process_name": "cmtray.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "clean_master_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "clean_master_page", "exit_button.png")  # 页面关闭按钮图
    },
    "CleanMasterPreSweptBubble": {
        "page_class": "SysSlim_{44FC9300-F03E-46d0-A143-2BF8F9362C46}",
        "page_title": "C盘瘦身",
        "page_desc": "清理大师预扫泡",
        "process_path": None,  # 进程地址
        "process_name": "cmtray.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "clean_master_pre_swept_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "clean_master_pre_swept_page", "exit_button.png")  # 页面关闭按钮图
    },
    "FastVcPage": {
        "page_class": "Qt5150QWindowIcon",
        "page_title": "毒霸视频转换器",
        "page_desc": "毒霸视频格式专家",
        "process_path": None,  # 进程地址
        "process_name": "fastvc.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "fast_vc_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "fast_vc_page", "exit_button.png")  # 页面关闭按钮图
    },
    "SoftWareManagePage": {
        "page_class": "soft uninst class",
        "page_title": "软件管家",
        "page_desc": "软件管家",
        "process_path": None,  # 进程地址
        "process_name": "ksoftmgr.exe",  # 进程名
        "entry_pic": os.path.join(page_shot_path, "software_manage_page", "software_manage_entry_button.png"),  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "software_manage_page", "software_manage_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "software_manage_page", "software_manage_close_button.png")  # 页面关闭按钮图
    },
    "KcleanMasterInstall": {
        "page_title": "清理大师安装",
        "page_desc": "清理大师安装",
        "process_path": None,  # 进程地址
        "process_name": None,  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": [os.path.join(page_shot_path, "clean_master_install_page", "tab_logo.png"),
                    os.path.join(page_shot_path, "clean_master_install_page", "re_install.png")],  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "clean_master_install_page", "exit_button.png")  # 页面关闭按钮图
    },
    "KcleanMasterUnInstall": {
        "page_title": "清理大师卸载",
        "page_desc": "清理大师卸载",
        "process_path": None,  # 进程地址
        "process_name": "uni0nst.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "clean_master_uninstall_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "clean_master_uninstall_page", "exit_button.png")  # 页面关闭按钮图
    },
    "mycomputerpro_page": {
        "page_class": "Qt5150QWindowToolSaveBits",
        "page_title": "kexplorermain",
        "page_desc": "我的电脑pro",
        "process_path": None,  # 进程地址
        "process_name": "kexplorermain.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "mycomputerpro_page", "tab_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "mycomputerpro_page", "exit_button.png")  # 页面关闭按钮图
    },
    "ScreenCapturePage": {
        "page_class": "#32770",
        "page_title": "桌面截图工具栏",
        "page_desc": "毒霸截图王",
        "process_path": None,  # 进程地址
        "process_name": "kscrcap.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": "tab_logo.png",  # 页面tab图
        "exit_pic": "exit_button.png"  # 页面关闭按钮图
    },
    "FeedbackPage": {
        "page_class": "ATL:0048E4E8",
        "page_title": "金山毒霸-反馈建议",
        "page_desc": "反馈建议",
        "process_path": None,  # 进程地址
        "process_name": "feedbackwin.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": "tab_logo.png",  # 页面tab图
        "exit_pic": "exit_button.png"  # 页面关闭按钮图
    },
    "StartMenuProPage": {
        "page_class": "Qt5150QWindowIcon",
        "page_title": "ksoftlaunchpad",
        "page_desc": "开始菜单Pro",
        "process_path": None,  # 进程地址
        "process_name": "ksoftlaunchpad.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": "tab_logo.png",  # 页面tab图
        "exit_pic": "exit_button.png"  # 页面关闭按钮图
    },
    "KsapiToolPage": {
        "page_title": "fantasy_ksapi",
        "page_desc": "ksapi测试工具",
        "process_path": None,  # 进程地址
        "process_name": "fantasy_ksapi.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": [os.path.join(page_shot_path, "ksapi_tool_page", "tab_logo.png"),
                    os.path.join(page_shot_path, "ksapi_tool_page", "tab_logo1.png"),
                    os.path.join(page_shot_path, "ksapi_tool_page", "tab_logo_win7.png"),
                    os.path.join(page_shot_path, "ksapi_tool_page", "tab_logo_win7_2.png")],  # 页面tab图
        "exit_pic": [os.path.join(page_shot_path, "ksapi_tool_page", "close_tool_button.png"),
                     os.path.join(page_shot_path, "ksapi_tool_page", "close_tool_button_win7.png"),
                     os.path.join(page_shot_path, "ksapi_tool_page", "close_tool_button_win11_22h2.png")]  # 页面关闭按钮图
    },
    "UpdatePopToolPage": {
        "page_title": "tttttttttttttttttttttttttttttt",
        "page_desc": "升级完成泡弹泡工具",
        "process_path": None,  # 进程地址
        "process_name": "tttttttttttttttttttttttttttttt.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "UpdatePop_Tool_Page", "updatePopToolTab.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "UpdatePop_Tool_Page", "updatePopToolExitButton.png")  # 页面关闭按钮图
    },
    "UpdatePopPage": {
        "page_desc": "升级完成泡",
        "process_path": None,  # 进程地址
        "process_name": "kxetray.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": [os.path.join(page_shot_path, "UpdatePop_Page", "updatepop_tab_1.png"),
                    os.path.join(page_shot_path, "UpdatePop_Page", "updatepop_tab_2.png")], # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "UpdatePop_Page", "updatepop_exit_button.png")  # 页面关闭按钮图
    },
    "ComputerAcceleratePage": {
        "page_desc": "电脑加速",
        "process_path": None,  # 进程地址
        "process_name": "kismain.exe",  # 进程名
        "entry_pic": os.path.join(page_shot_path, "computer_accelerate_page", "entry_computer_accelerate.png"),  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "computer_accelerate_page", "tab_logo_new.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "computer_accelerate_page", "return_button_new.png")  # 页面关闭按钮图
    },
    "RubbishCleanPage": {
        "page_desc": "垃圾清理",
        "process_path": None,  # 进程地址
        "process_name": "kismain.exe",  # 进程名
        "entry_pic": os.path.join(page_shot_path, "rubbish_clean_page", "entry_rubbish_clean.png"),  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "rubbish_clean_page", "page_logo.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "rubbish_clean_page", "page_return_button.png")  # 页面关闭按钮图
    },
    "KsthlpToolPage": {
        "page_title": "TestDlg",
        "page_desc": "ksthlp测试工具",
        "process_path": None,  # 进程地址
        "process_name": "TestDlg_self_sign.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": [os.path.join(page_shot_path, "ksthlp_tool_page", "ksapitool_tab_logo_win10.png"),
                    os.path.join(page_shot_path, "ksthlp_tool_page", "ksapitool_tab_logo_win7.png")],  # 页面tab图
        "exit_pic": [os.path.join(page_shot_path, "ksthlp_tool_page", "close_ksthlptool_button_win10.png"),
                     os.path.join(page_shot_path, "ksthlp_tool_page", "close_ksthlptool_button_win7.png")]  # 页面关闭按钮图
    },
    "DeviceInfoPage": {
        "page_title": "金山毒霸-电脑状态",
        "page_desc": "金山毒霸-电脑状态",
        "process_path": None,  # 进程地址
        "process_name": "kdinfomgr.exe",  # 进程名
        "entry_pic": None,  # 功能入口图片
        "tab_pic": os.path.join(page_shot_path, "device_info_page", "device_info_tab.png"),  # 页面tab图
        "exit_pic": os.path.join(page_shot_path, "device_info_page", "device_info_close_button.png")  # 页面关闭按钮图
    }
}
