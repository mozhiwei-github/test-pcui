from enum import Enum, unique

"""导航项目常量"""

class NavigationEnv(Enum):
    """导航测试环境"""
    ONLINE = "https://www.duba.com"
    ONLINEN = "https://www.newduba.cn"
    TEST = "http://cm.duba.com"
    TESTN = "http://cm.newduba.cn"


class NavigationChannel(Enum):
    """导航测试渠道"""
    MAIN = "/index.html"
    TIYAN3 = "/tiyan3.html"
    TIYAN4 = "/tiyan4.html"
    TIYAN4B = "/tiyan4b.html"
    TIYAN21 = "/tiyan21.html"
    SS = "/ss.html"
    SV = "/sv.html"
    YQ = "/yq.html"

@unique
class TaskRunMode(Enum):
    LOCAL = "本机"
    REMOTE = "远程"

class tp_info(Enum):
    """
    tp值对应关系枚举
    """
    index = 'index'
    tiyan21 = 'tiyan21'
    tiyan3 = 'tiyan3'
    tiyan4 = 'tiyan4'
    tiyan4b = 'tiyan5'

class w_info(Enum):
    """
    word值对应关系枚举
    """
    null_value = ''
    num_1 = '1'
    searchbox = 'searchbox'
    searchword = 'searchword'
    rc = 'rc'
    rctpfg = 'rctpfg'
    ksrk = 'ksrk'
    mz = 'mz'
    kz = 'kz'
    sright = 'sright'
    zhongjianlan = 'zhongjianlan'
    cnxh = 'cnxh'
    xwdt = 'xwdt'
    ftab = 'ftab'
    feedlist = 'feedlist'
    ksrk_2020 = '2020ksrk'
    ksrkyx = 'ksrkyx'
    zjltj = 'zjltj'
    ssrc = 'ssrc'
    leftnav = 'leftnav'
    leftnavset = 'leftnavset'
    kztab = 'kztab'
    svmz = 'svmz'
    allskin = 'allskin'

class snode_info(Enum):
    """
    snode值对应关系枚举
    """
    page_show = 100
    search_click = 1264
    close = 10147
    page_click = 1163
    element_show = 1365
    ad_info_upload = 11161

class scene_info(Enum):
    """
    scene值对应关系枚举
    """
    step1 = '导航页面展示上报'
    step2 = '搜索框联想词点击上报'
    step3 = '搜索框输入内容点击搜索上报'
    step4_1 = '搜索框选择下拉框内容点击上报'
    step4_2 = '搜索框选择下拉框内容点击上报-AD'
    step4_3 = '搜索框选择下拉框内容点击上报-OTHERS'
    step5 = '中间栏点击上报'
    step6_1 = '搜索框点击搜索框下方内容上报-client'
    step6_2 = '搜索框点击搜索框下方内容上报-ad'
    step6_3 = '搜索框点击搜索框下方内容上报-accurate'
    step6_4 = '搜索框点击搜索框下方内容上报-back'
    step6_5 = '搜索框点击搜索框下方内容上报'
    step7 = '通栏快速入口点击上报'
    step8 = '名站点击上报'
    step9 = '酷站点击上报'
    step10 = '搜索框右侧轮播点击上报'
    step11 = '猜你喜欢点击上报'
    step12 = '信息流顶部新闻轮播点击上报'
    step13 = '信息流tab点击上报'
    step14 = '信息流列表点击上报'
    step15 = '左侧精选点击上报'
    step16 = '右侧游戏板块点击上报'
    step17 = '右侧热门板块点击上报'

class ss_scene_info(Enum):
    step1 = '办公导航页面展示上报'
    step2 = '办公搜索框联想词点击上报'
    step3 = '办公搜索框选择下拉框内容点击搜索button上报'
    step4 = '办公搜索框输入内容点击搜索button上报'
    step5 = '办公名站点击上报'
    step6 = '办公最近使用模块tab点击上报'
    step7 = '办公酷站点击上报'
    step8 = '办公今日热搜点击上报'
    step9 = '办公今日热搜卡片点击上报'
    step10 = '办公电梯栏点击上报'
    step11 = '办公电梯栏点击设置按钮上报'
    step12 = '办公视频音乐点击左侧大图卡片上报'
    step13 = '办公视频音乐点击右侧卡片上报'
    step14 = '购物出行点击左侧大图卡片上报'
    step15 = '购物出行点击右侧卡片上报'
    step16 = '办公搜索框点击搜索框下方内容上报'

class sv_scene_info(Enum):
    step1 = '简版导航页面展示上报'
    step2 = '简版搜索框选择下拉框内容上报'
    step3 = '简版搜索框输入内容点击搜索button上报'
    step4 = '简版搜索框点击搜索框下方内容上报'
    step5 = '简版点击名站上报'

class yq_scene_info(Enum):
    step1 = '元气导航页面展示上报'
    step2 = '元气搜索框选择下拉框内容上报'
    step3 = '元气搜索框输入内容点击搜索button上报'
    step4 = '元气点击切换皮肤上报'
    step5 = '元气皮肤库切换皮肤点击上报'