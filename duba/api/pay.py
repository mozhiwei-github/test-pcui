from common.log import log
from duba.config import config
from common.utils import send_request
from duba.contants import DubaApiHeaders, PaySettingShow

"""支付相关api接口"""


def pay_settings_api(open_id, token, server_id, tryno, is_continuous=1, time_type=0,
                     show=[PaySettingShow.VIP_CENTER.value],
                     is_all=None, is_upgrade=False):
    """
    获取支付套餐
    http://apix.kisops.com/project/484/interface/api/15087
    @param server_host: 服务器地址
    @param product: 接口版本
    @param open_id: 用户open_id
    @param token: 用户token
    @param server_id: 客户端serverId
    @param is_continuous: 1为续费套餐，0为非自动续费套餐
    @param time_type: 按年和月区分套餐，1为年，2为月，3为按次，0则不进行区分
    @param show: 展示套餐类型，1为会员中心套餐 40为超级会员[升级] 其他值见于api文档
    @param is_all: 1为忽略is_continuous值，返回全部套餐
    @param is_upgrade: 是否为升级到目标套餐，此时请求 common 中必须带用户授权信息
    @param  attach_allure True打印请求数据的日志，否则不打印
    @return:
    """
    url = f"{config.GATEWAY_HOST}/api/v3/pay/settings"

    data = {
        "common": {
            "server_id": server_id,
            "token": token,
            "open_id": open_id,
            "tryno": str(tryno)
        },
        "token": token,
        "open_id": open_id,
        "is_continuous": is_continuous,
        "time_type": time_type,
        "is_all": 1,  # 把续费所有价格展示加上的参数
        "show": show
    }

    if is_all is not None:
        data["is_all"] = is_all
    if is_upgrade:
        data["is_upgrade"] = 1

    log.log_info("会员查询pay_setting请求url:%s  post参数%s" % (url, str(data)))  # 方便查询请求的参数排查问题
    res = send_request(url, json=data, headers=DubaApiHeaders.NEWVIP_HEADERS.value)
    return res
