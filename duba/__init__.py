from duba.config import config
from common.log import log

log.log_info(f"当前配置类型为：{config.ENV.value}", attach=False)
