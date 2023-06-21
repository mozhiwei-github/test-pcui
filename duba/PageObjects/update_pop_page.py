import os

from common.samba import Samba
from common.tools import duba_tools
from common.utils import remove_reg_key, remove_reg_value, query_reg_value, get_reg_key, delete_reg_key_with_son, \
    remove_path
from common.log import log
from common.basepage import BasePage, page_method_record

# 引用变量
duba_path = duba_tools.find_dubapath_by_reg()
kpopdata_file_path = os.path.join(duba_path,r"data\kpopdata.dat")
rekpopdata_file_path = os.path.join(duba_path,r"data\kpopdata_1.dat")
user_basic_path = r'C:\Users'

# 获取当前系统%AppData%路径并删除本地pophistory.dat文件
def delete_pophistory():
    username = os.environ['USERNAME']
    pophistory_path = os.path.join(user_basic_path, username, r"AppData\Roaming\kingsoft\duba\pophistory")
    if os.path.exists(pophistory_path):
        remove_path(pophistory_path)
        log.log_pass("本地pophistory已删除")

# 屏蔽泡泡中心：重命名kpopcenter.dll；重命名kpopdata.dat；
def block_popcenter():
    duba_tools.rename_kpopcenter()
    if os.path.exists(rekpopdata_file_path):
        os.remove(rekpopdata_file_path)
    if os.path.exists(kpopdata_file_path):
        os.rename(kpopdata_file_path,rekpopdata_file_path)
        log.log_pass("泡泡中心kpopdata配置文件已删除")

# 配置注册表记录使其满足升级完成泡弹出环境
def update_reg_operation():
    recommend_regpath = r"SOFTWARE\WOW6432Node\kingsoft\Antivirus\recommend"
    newrcmd_regpath = r"SOFTWARE\WOW6432Node\kingsoft\Antivirus\NewRcmd"
    update_regpath = r"SOFTWARE\WOW6432Node\kingsoft\KISCommon\Update"
    delete_reg_key_with_son(regroot=None,regpath=recommend_regpath)
    delete_reg_key_with_son(regroot=None,regpath=newrcmd_regpath)

    reg_key_list = get_reg_key(regroot=None,regpath=update_regpath)
    for key in reg_key_list:
        if not key[0]=='TryNo':
            remove_reg_value(regroot=None,regpath=update_regpath,value=key[0])



class UpdatePopPage(BasePage):
    pass









