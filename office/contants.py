from enum import unique, Enum

"""办公模板用例常量"""

@unique
class TaskRunMode(Enum):
    """任务运行方式"""
    LOCAL = "本机"
    REMOTE = "远程"

@unique
class Env(Enum):
    """环境配置"""
    TEST = "测试服"
    PRODUCTION = "正式服"

@unique
class MainUrl(Enum):
    """办公web站相关域名常量"""
    ONLINEURL = "https://o.keniu.com/"
    TESTURL = "http://ppt-material-web-keniu-test-fe.aix-test-k8s.iweikan.cn/"
    SEMONLINEURL = "https://ppt3.ycywx.com/"
    SEMTESTURL = "http://ppt-material-web-keniu-semtest-fe.aix-test-k8s.iweikan.cn/"

@unique
class QQAccount(Enum):
    """测试专用登录账号"""
    # QQNUM= "2139016269"
    # QQPASSWORD = "KeniuOfficeTest666"
    QQNUM = "2327753400"
    QQPASSWORD = "mozhiweidemima55"


@unique
class ChromeDownloadPath(Enum):
    """chrome浏览器下载路径配置"""
    DOWNLOADPATH = r"C:\Users\admin\Downloads"

@unique
class SearchWord(Enum):
    """搜索验证用关键词配置"""
    ZONGJIE = "总结"

@unique
class keniuofficePath(Enum):
    DEFAULTINSTALLPATH = r"C:\Program Files (x86)\keniu\kntemplate"


@unique
class knstorePath(Enum):
    DEFAULTINSTALLPATH = r"C:\Program Files (x86)\keniu\knstore"

@unique
class keniuofficeclassname(Enum):
    CLASSNAME = ['ppt','word','excel','design','sucai']

@unique
class keniuofficeenvironment(Enum):
    MASTER = "https://api.777ppt.com"
    TEST = "https://test-loveoffice.zhhainiao.com"
    CMSMASTER = "http://loveofficecms.aix-test-k8s.iweikan.cn"
    CMSTEST = "https://loveofficecms.zhhainiao.com"





