import enum

class tp_info(enum.Enum):
    """
    tp值对应关系枚举
    """
    index = 'index'
    tiyan21 = 'tiyan21'
    tiyan3 = 'tiyan3'
    tiyan4 = 'tiyan4'
    tiyan4b = 'tiyan5'

class w_info(enum.Enum):
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

class snode_info(enum.Enum):
    """
    snode值对应关系枚举
    """
    page_show = 100
    search_click = 1264
    close = 10147
    page_click = 1163
    element_show = 1365
    ad_info_upload = 11161

class scene_info(enum.Enum):
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




