import os
from common import utils
import requests
from lxml import etree
from common.log import log
import json
import time
from office.utils import send_request


def get_resource(url):
    response = requests.get(url)
    if response.status_code == 200:
        log.log_info("页面请求状态码为200")
        return response.content.decode('utf-8')
    log.log_info(f"请求链接{url}")
    log.log_error("页面请求状态码不为200")
    return None

def get_config_result(file_path):
    f = open(file_path, encoding='utf-8')
    file = json.load(f) # file;file["mainpage"];file["detailpage"]["title"];
    return file

def compare_current_expect(current, expect):
    if not current:
        log.log_error("实际值异常")
    if not expect:
        log.log_error("期望值异常")
    if not current == expect:
        return False
    return True

def get_module_detail(envir, data=None):
    url = r"/api/mat/detail/v2"
    resp = send_request(envir, url, "POST", json=data)
    return resp["info"] # dict

def get_module_name(detail):
    """
    @param detail: 模板详情 dict
    @return:
    """
    return detail["name"]


def get_module_classifyname(detail,envir):
    """
    @param detail: 模板的详情信息，dict
    @return: module 一二三级分类名称 dict
    """
    # 获取模板的各classid
    category1_id = detail['class1_id']
    category2_id = detail['class2_id']
    category3_id = detail['class_id']
    categoryid_list = [category1_id, category2_id, category3_id]
    categoryname_dict = {
        "category1":"",
        "category2":"",
        "category3":""
    }
    data = {
        "common":{
            "uid":"",
            "token":""
        }
    }
    url = r"/api/category/list"
    resp = send_request(envir, url, "POST", json=data)
    category_list = resp['list'] # list
    # # 方法一：整合所有分类至一个列表中
    # search_category_list = []
    # for i in category_list:
    #     new_dict = {"id":i["id"],"name":i["name"]}
    #     search_category_list.append(new_dict)
    #     new_dict = {}
    #     if not len(i['list']) == 0:
    #         for j in i['list']:
    #             new_dict_2 = {"id":j["id"],"name":j["name"]}
    #             search_category_list.append(new_dict_2)
    #             new_dict_2 = {}
    #             if not len(j['list']) == 0:
    #                 for k in j['list']:
    #                     new_dict_3 = {"id": k["id"], "name": k["name"]}
    #                     search_category_list.append(new_dict_3)
    #                     new_dict_3 = {}
    # for module in search_category_list:
    #     if module["id"] == category1_id:
    #         categoryname_dict['category1'] = module["name"]
    #     if module["id"] == category2_id:
    #         categoryname_dict['category2'] = module["name"]
    #     if module["id"] == category3_id:
    #         categoryname_dict['category3'] = module["name"]

    # 方法2：根据id遍历查找
    for i in category_list:
        if category1_id != 0 and i["id"] == category1_id:
            categoryname_dict['category1'] = i["name"]
            if category2_id == 0 or len(i['list']) == 0:
                break
            for j in i['list']:
                if j["id"] == category2_id:
                    categoryname_dict['category2'] = j["name"]
                    if category3_id == 0 or len(j['list']) == 0:
                        break
                    for k in j['list']:
                        if k["id"] == category3_id:
                            categoryname_dict['category3'] = k["name"]
    return categoryname_dict, categoryid_list

def deal_word_by_id(module_id, env, result):
    """

    @param module_id:
    @param env: ONLINEURL、TESTURL
    @param result: json文件解析结果
    @return:
    """

    data = {
        "common":{
            "uid" : "",
            "token" : ""
        },
        "mat_id": int(module_id)
    }
    envir = ""
    if env == "ONLINEURL":
        envir = "MASTER"
    elif env == "TESTURL":
        envir = "TEST"
    resp_info_json = get_module_detail(envir, data=data)
    category_result = get_module_classifyname(resp_info_json, envir)
    module_name = get_module_name(resp_info_json)
    # 获取对应模板详情页的tdk
    if category_result[1][0] == 1:
        category = "ppt"
    elif category_result[1][0] == 16:
        category = "word"
    elif category_result[1][0] == 31:
        category = "excel"
    elif category_result[1][0] == 210:
        category = "design"
    elif category_result[1][0] == 207:
        category = "sucai"
    else:
        category = ""
    detailpage_tdk = result['detailpage'][category]
    # 替换规则中的指定规则项
    detailpage_tdk["title"] = detailpage_tdk["title"].replace("[模板名称]", module_name)
    detailpage_tdk["title"] = detailpage_tdk["title"].replace("[一级分类]", category_result[0]["category1"])
    detailpage_tdk["title"] = detailpage_tdk["title"].replace("[二级分类]", category_result[0]["category2"])
    detailpage_tdk["title"] = detailpage_tdk["title"].replace("[三级分类]", category_result[0]["category3"])
    detailpage_tdk["keywords"] = detailpage_tdk["keywords"].replace("[模板名称]", module_name)
    detailpage_tdk["keywords"] = detailpage_tdk["keywords"].replace("[一级分类]", category_result[0]["category1"])
    detailpage_tdk["keywords"] = detailpage_tdk["keywords"].replace("[二级分类]", category_result[0]["category2"])
    detailpage_tdk["keywords"] = detailpage_tdk["keywords"].replace("[三级分类]", category_result[0]["category3"])
    detailpage_tdk["description"] = detailpage_tdk["description"].replace("[模板名称]", module_name)
    detailpage_tdk["description"] = detailpage_tdk["description"].replace("[一级分类]", category_result[0]["category1"])
    detailpage_tdk["description"] = detailpage_tdk["description"].replace("[二级分类]", category_result[0]["category2"])
    detailpage_tdk["description"] = detailpage_tdk["description"].replace("[三级分类]", category_result[0]["category3"])

    return detailpage_tdk

class KeniuOfficeSeo():
    def __init__(self, url, html_format=True):
        self.url = url
        self.resource = get_resource(self.url)
        if html_format:
            self.html_resource = etree.HTML(self.resource)

    def get_page_title(self):
        return self.html_resource.xpath('//head/title')[0].text

    def get_page_keywords(self):
        return self.html_resource.xpath('//head/meta[@name="keywords"]//@content')[0]

    def get_page_description(self):
        return self.html_resource.xpath('//head/meta[@name="description"]//@content')[0]

    def check_h_tag(self):
        # 检查源码中不出现h标签内嵌h标签
        result = self.html_resource.xpath('//h//h')
        if not len(result) == 0:
            return False
        return True

    def check_robots_file(self):

        sitemap_cate_xml = r"sitemap:https://o.keniu.com/sitemap-cate.xml"
        sitemap_topic_xml = r"sitemap:https://o.keniu.com/sitemap-topic.xml"
        sitemap_detail_xml = r"sitemap:https://o.keniu.com/sitemap-detail.xml"
        sitemap_keyword_xml = r"sitemap:https://o.keniu.com/sitemap-keyword.xml"

        robot_detail = self.resource

        if not sitemap_cate_xml in robot_detail:
            log.log_error("sitemap_cate_xml 配置缺失")
        if not sitemap_topic_xml in robot_detail:
            log.log_error("sitemap_topic_xml 配置缺失")
        if not sitemap_detail_xml in robot_detail:
            log.log_error("sitemap_detail_xml 配置缺失")
        # if not sitemap_keyword_xml in robot_detail:
        #     log.log_error("sitemap_keyword_xml 配置缺失")
        log.log_pass("robots.txt 配置符合预期")

    def check_sitemap_cate_xml(self):
        sitemap_cate_xml = self.resource
        if not sitemap_cate_xml:
            log.log_error("sitemap-cate.xml 中无配置")
        log.log_pass("sitemap-cate.xml 中存在配置")

    def check_sitemap_topic_xml(self):
        sitemap_topic_xml = self.resource
        if not sitemap_topic_xml:
            log.log_error("sitemap-topic.xml 中无配置")
        log.log_pass("sitemap-topic.xml 中存在配置")

    def check_sitemap_detail_xml(self):
        sitemap_detail_xml = self.resource
        if not sitemap_detail_xml:
            log.log_error("sitemap-detail.xml 中无配置")
        log.log_pass("sitemap-detail.xml 中存在配置")

    def check_sitemap_keyword_xml(self):
        sitemap_keyword_xml = self.resource
        if not sitemap_keyword_xml:
            log.log_error("sitemap-keyword.xml 中无配置")
        log.log_pass("sitemap-keyword.xml 中存在配置")

    def check_deadlink_file(self):
        deadlink_file = self.resource
        if not deadlink_file:
            log.log_error("deadlink.txt 中无配置")
        log.log_pass("deadlink.txt 中存在配置")



