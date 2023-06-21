import os
import re
import traceback
from pathlib import Path

base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_project_path(call_filepath):
    """
    获取项目路径
    @param call_filepath:
    @return:
    """
    rel_call_filepath = Path(call_filepath).relative_to(Path(base_path)).as_posix()
    matched = re.match(r'^(\w+)/.*$', rel_call_filepath)
    assert matched, f"项目路径解析失败：{call_filepath}"
    return matched.group(1)


def get_page_shot(page_filename, shot_name):
    """
    获取指定页面截图文件路径
    @param page_filename: 页面名称
    @param shot_name: 截图文件名
    @return:
    """
    call_filepath = traceback.extract_stack()[-2].filename
    project_path = get_project_path(call_filepath)

    shot_path = os.path.join(base_path, project_path, "PageShot", page_filename, shot_name)
    assert os.path.exists(shot_path), f"获取指定页面截图文件路径失败: {shot_path}"

    return shot_path
