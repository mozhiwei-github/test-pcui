import os
import allure
import pytest
from common.samba import Samba
from office.contants import MainUrl, keniuofficeclassname
from common.log import log
from office.PageObjects.keniuoffice_seo import KeniuOfficeSeo, get_config_result,compare_current_expect,deal_word_by_id
from common import utils



@allure.epic('可牛办公web站SEO检测')
@allure.feature('可牛办公web站SEO检测')
class TestKeniuofficeSeo(object):
    @allure.story('可牛办公web站SEO检测')
    @allure.description("""
        step1: 从远端拉取预期结果json文件
        step2: 解析json文件获取内容  
        step3: 验证首页tdk
        step4: 验证分类页tdk
        step5: 验证详情页tdk  
        step6: 验证seo配置文件
    """)
    def test_keniu_seo(self, get_environment):
        env = get_environment
        base_url = MainUrl[env].value

        with allure.step("step1: 从远端拉取预期结果json文件"):
            # 从远端拉取预期配置结果文件
            config_path = os.path.join(os.getcwd(), "KeniuOffice")
            if os.path.exists(config_path):
                utils.remove_path(config_path)
            sambo_o = Samba("10.12.36.203", "duba", "duba123")
            sambo_o.download_dir("TcSpace", os.path.join('autotest', "KeniuOfficeSeo"), config_path)
            config_file_path = os.path.join(config_path, "seotest.json")
            if not os.path.exists(config_file_path):
                log.log_error("从远端拉取json文件失败")
            log.log_pass("从远端获取json文件成功")

        with allure.step("step2: 解析json文件获取内容"):
            # test_path = r"C:\project\dubatestpro\office\seotest.json"
            # result = get_config_result(test_path)
            result = get_config_result(config_file_path)
            if result:
                log.log_pass("json解析获取result成功")
            else:
                log.log_error("json解析获取result失败")

        with allure.step("step3: 验证首页tdk"):
            page_object = KeniuOfficeSeo(base_url)
            if not page_object.check_h_tag():
                log.log_error("首页存在h标签内嵌---不合规")
            log.log_pass("首页不存在h标签内嵌---合规")
            page_title = page_object.get_page_title()
            expect_title = result["mainpage"]["title"]
            if not compare_current_expect(page_title, expect_title):
                log.log_info(f"预期: {expect_title}")
                log.log_info(f"实际: {page_title}")
                log.log_error("首页title与预期不符")
            log.log_pass("首页title与预期一致")
            page_keywords = page_object.get_page_keywords()
            expect_keywords = result["mainpage"]["keywords"]
            if not compare_current_expect(page_keywords, expect_keywords):
                log.log_info(f"预期: {expect_keywords}")
                log.log_info(f"实际: {page_keywords}")
                log.log_error("首页keywords与预期不符")
            log.log_pass("首页keywords与预期一致")
            page_description = page_object.get_page_description()
            expect_description = result["mainpage"]["description"]
            if not compare_current_expect(page_description, expect_description):
                log.log_info(f"预期: {expect_description}")
                log.log_info(f"实际: {page_description}")
                log.log_error("首页description与预期不符")
            log.log_pass("首页description与预期一致")

        with allure.step("step4: 验证分类页tdk"):
            for classname in keniuofficeclassname.CLASSNAME.value:
                test_url = base_url + classname + '/'
                page_object = KeniuOfficeSeo(test_url)
                if not page_object.check_h_tag():
                    log.log_error("分类页存在h标签内嵌---不合规")
                log.log_pass("分类页不存在h标签内嵌---合规")
                current_title = page_object.get_page_title()
                expect_title = result["classpage"]["title"][classname]
                if not compare_current_expect(current_title, expect_title):
                    log.log_info(f"预期: {expect_title}")
                    log.log_info(f"实际: {current_title}")
                    log.log_error(f"{classname}分类页title与预期不符")
                log.log_pass(f"{classname}分类页title与预期一致")
                current_keywords = page_object.get_page_keywords()
                expect_keywords = result["classpage"]["keywords"][classname]
                if not compare_current_expect(current_keywords, expect_keywords):
                    log.log_info(f"预期: {expect_keywords}")
                    log.log_info(f"实际: {current_keywords}")
                    log.log_error(f"{classname}分类页keywords与预期不符")
                log.log_pass(f"{classname}分类页keywords与预期一致")
                current_description = page_object.get_page_description()
                expect_description = result["classpage"]["description"][classname]
                if not compare_current_expect(current_description, expect_description):
                    log.log_info(f"预期: {expect_description}")
                    log.log_info(f"实际: {current_description}")
                    log.log_error(f"{classname}分类页description与预期不符")
                log.log_pass(f"{classname}分类页description与预期一致")

        with allure.step("step5: 验证详情页tdk"):
            for classname in keniuofficeclassname.CLASSNAME.value:
                module_id = result[classname + "_detail_id"]
                test_url = base_url + "t/" + module_id + ".html"
                page_object = KeniuOfficeSeo(test_url)
                if not page_object.check_h_tag():
                    log.log_error("详情页存在h标签内嵌---不合规")
                log.log_pass("详情页不存在h标签内嵌---合规")
                expect_tdk = deal_word_by_id(module_id=module_id, env=env, result=result)
                current_title = page_object.get_page_title()
                expect_title = expect_tdk["title"]
                if not compare_current_expect(current_title, expect_title):
                    log.log_info(f"预期: {expect_title}")
                    log.log_info(f"实际: {current_title}")
                    log.log_error(f"模板{module_id}的title与预期不符")
                log.log_pass(f"模板{module_id}的title与预期一致")
                current_keywords = page_object.get_page_keywords()
                expect_keywords = expect_tdk["keywords"]
                if not compare_current_expect(current_keywords, expect_keywords):
                    log.log_info(f"预期: {expect_keywords}")
                    log.log_info(f"实际: {current_keywords}")
                    log.log_error(f"模板{module_id}的keywords与预期不符")
                log.log_pass(f"模板{module_id}的keywords与预期一致")
                current_description = page_object.get_page_description()
                expect_description = expect_tdk["description"]
                if not compare_current_expect(current_description, expect_description):
                    log.log_info(f"预期: {expect_description}")
                    log.log_info(f"实际: {current_description}")
                    log.log_error(f"模板{module_id}的description与预期不符")
                log.log_pass(f"模板{module_id}的description与预期一致")

        with allure.step("step6: 验证seo配置文件"):
            # 验证robots.txt文件及其配置
            test_url = base_url + "robots.txt"
            page_object = KeniuOfficeSeo(test_url, html_format=False)
            page_object.check_robots_file()
            # 验证sitemap-cate.xml文件及其配置
            test_url = base_url + "sitemap-cate.xml"
            page_object = KeniuOfficeSeo(test_url, html_format=False)
            page_object.check_sitemap_cate_xml()
            # 验证sitemap-topic.xml文件及其配置
            test_url = base_url + "sitemap-topic.xml"
            page_object = KeniuOfficeSeo(test_url, html_format=False)
            page_object.check_sitemap_topic_xml()
            # 验证sitemap-detail.xml文件及其配置
            test_url = base_url + "sitemap-detail.xml"
            page_object = KeniuOfficeSeo(test_url, html_format=False)
            page_object.check_sitemap_detail_xml()
            # # 验证sitemap-keyword.xml文件及其配置
            # test_url = base_url + "sitemap-keyword.xml"
            # page_object = KeniuOfficeSeo(test_url, html_format=False)
            # page_object.check_sitemap_keyword_xml()
            # 验证sitemap-detail.xml文件及其配置
            test_url = base_url + "deadlink.txt"
            page_object = KeniuOfficeSeo(test_url, html_format=False)
            page_object.check_deadlink_file()

if __name__ == "__main__":
    # pytest.main(["-v", "-s", __file__])
    allure_attach_path = os.path.join("Outputs", "allure")
    pytest.main(["-v", "-s", __file__, '--alluredir=%s' % allure_attach_path])
    os.system("allure serve %s" % allure_attach_path)
