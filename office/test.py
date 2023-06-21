from common import utils
import json
import requests
from lxml import etree

from office.conftest import chrome_driver_init
from office.utils import send_request
from common.log import log
from office.contants import MainUrl
from office.contants import keniuofficeclassname
from office.PageObjects.keniuoffice_seo import get_module_detail,get_module_classifyname

class testing(chrome_driver_init):
    url = r"https://www.baidu.com"
    proxy, driver = chrome_driver_init()
    driver.get(url)


if __name__ == '__main__':
    test = testing()







