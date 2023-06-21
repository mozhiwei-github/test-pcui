#!/usr/bin/evn python
# --coding = 'utf-8' --
# Python Version 3.8
import os

page_shot_path = os.path.join(os.getcwd(), "office", "PageShot")

# 标签key必须与页面类名一致
page_resource = {
    "KeniuOfficeClientPage":{
        "page_class": "KWebxMainWindow-{FD4C5916-356D-42D1-A0C5-EEC12ABF817A}",
        "page_title": "可牛办公",
        "page_desc": "可牛办公独立版",
        "process_path": None,
        "process_name": "ktemplate.exe",
        "entry_pic": None,
        "tab_pic": os.path.join(page_shot_path, "keniuoffice_client_page", "keniuoffice_page_logo.png"),
        "exit_pic": os.path.join(page_shot_path, "keniuoffice_client_page", "keniuoffice_page_close_button.png")
    },
    "KeniuOfficeInstallPage":{
        "page_class": "ATL:004CC428",
        "page_title": "可牛办公",
        "page_desc": "可牛办公独立版安装界面",
        "process_path": None,
        "process_name": "debug_package.exe",
        "entry_pic": None,
        "tab_pic": os.path.join(page_shot_path, "keniuoffice_install_page", "keniuoffice_install_logo.png"),
        "exit_pic": os.path.join(page_shot_path, "keniuoffice_install_page", "keniuoffice_install_close_button.png")
    },
    "KeniuOfficeUninstallPage":{
        "page_class": "ATL:00493CB0",
        "page_title": "可牛办公",
        "page_desc": "可牛办公独立版卸载界面",
        "process_path": None,
        "process_name": "uninstall.exe",
        "entry_pic": None,
        "tab_pic": os.path.join(page_shot_path, "keniuoffice_uninstall_page", "uninstallpage_logo.png"),
        "exit_pic": os.path.join(page_shot_path, "keniuoffice_uninstall_page", "uninstallpage_close_button.png")
    },
    "KnstorePage":{
        "page_class": "store dialog class",
        "page_title": "可牛应用市场",
        "page_desc": "可牛应用市场主界面",
        "process_path": None,
        "process_name": "knstore.exe",
        "entry_pic": None,
        "tab_pic": os.path.join(page_shot_path, "knstore_page", "knstore_logo.png"),
        "exit_pic": os.path.join(page_shot_path, "knstore_page", "knstore_close_button.png")
    },
    "KnstoreInstallPage":{
        "page_class": "ATL:004D55C8",
        "page_title": "可牛应用市场",
        "page_desc": "可牛应用市场安装界面",
        "process_path": None,
        "process_name": "knstore_debug_package.exe",
        "entry_pic": None,
        "tab_pic": os.path.join(page_shot_path, "knstore_install_page", "install_page_logo.png"),
        "exit_pic": os.path.join(page_shot_path, "knstore_install_page", "install_page_close_button.png")
    },
    "KnstoreUninstallPage":{
        "page_class": "ATL:00493CE0",
        "page_title": "可牛应用市场",
        "page_desc": "可牛应用市场卸载界面",
        "process_path": None,
        "process_name": "uninstall.exe",
        "entry_pic": None,
        "tab_pic": os.path.join(page_shot_path, "knstore_uninstall_page", "uninstall_page_logo.png"),
        "exit_pic": os.path.join(page_shot_path, "knstore_uninstall_page", "uninstall_page_close_button.png")
    }
}