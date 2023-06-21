import os
import sys
import atexit
import pytest
from common.log import log
from common.singleton import Singleton
from common.yaml_reader import YamlReader

"""
pytest共用fixture
"""

SMB_DUBA_FILEPATH = "old"


@Singleton
class Config(object):
    def __init__(self):
        self.context = YamlReader.read_yaml(os.path.join(os.getcwd(), "common", "config", "config.yml"))


def pytest_addoption(parser):
    """pytest自定义命令行参数"""
    parser.addoption("--smb", action="store", type=str, help="smb地址，使用smb中文件替换毒霸相应文件")
    parser.addoption("--channel", action="store", type=str, help="测试渠道")
    parser.addoption("--env", action="store", type=str, help="测试环境")
    parser.addoption("--tod", action="store", type=str, help="安装包tod")


def pytest_generate_tests(metafunc):
    # 测试用例函数地址
    node_id = metafunc.definition.nodeid
    node_path = node_id.split("::")[0]

    # 获取配置
    config = Config()
    config_info = config.context
    match_case_info = {}
    # TODO: 待各项目统一启动函数后，改为获取当前运行项目
    for project in config_info:
        project_info = config_info[project]
        if not project_info:
            continue
        case_list = project_info.get("cases", None)
        if not case_list:
            continue

        for case in case_list:
            case_param = case.get("param", "")
            if case_param and node_path.endswith(case_param):
                match_case_info = case
                break
        if match_case_info:
            break

    fixture_names = metafunc.fixturenames

    for fixture_name in fixture_names:
        # 根据 autosession 参数判断是否执行关闭毒霸自保护等操作，缺省时不执行
        if fixture_name in ["turnoff_duba_self_protecting", "reset_duba_page", "replace_duba_file_with_smb"]:
            try:
                autosession = match_case_info.get("autosession", False)
                metafunc.parametrize(fixture_name, [bool(autosession)], indirect=True)
            except Exception as e:
                log.log_error(f"{fixture_name} parametrize error", log_only=True)
                raise e


@pytest.fixture(autouse=True)
def capture_wrap():
    """
    解决写日志时 ValueError: I/O operation on closed file. 问题
    https://github.com/pytest-dev/pytest/issues/5502#issuecomment-678368525
    """
    sys.stderr.close = lambda *args: None
    sys.stdout.close = lambda *args: None
    yield
    atexit._run_exitfuncs()


@pytest.fixture(scope="function")
def user_type(request):
    """获取用户类型"""
    return request.param
