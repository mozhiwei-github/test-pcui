import ctypes
import os
import sys
import json
import random
from common.tools.duba_tools import find_dubapath_by_reg, find_dgpath_by_reg
from common.log import log
from common.utils import is_admin, remove_path
from common.samba import Samba

"""
        ----------目录------------
 
目前对于魔方操作已有的方法  (直接搜下列中文即可搜到函数)：
    1、下拉魔方工具（精灵、毒霸）
    2、更新魔方数据（精灵、毒霸）
    3、删除魔方数据
    4、判断魔方加密/解密文件是否存在
    5、解密本地魔方数据
    6、加密本地魔方数据
    7、获取本地魔方Abtest数据
    8、获取本地魔方Switch数据
    9、获取本地魔方Raw数据
    10、通过section更新ab测数据
    11、通过section更新switch数据
    12、通过section更新raw数据
    13、获取Abtest中key_value中指定key的value
    14、获取Switch中key_value中指定key的value
    15、获取Raw中key_value中指定key的value

"""


# 该方法调用前需要先将自保护关闭
def get_magiccube_tools(product_name):
    """
    下拉魔方工具（精灵、毒霸）
    @param product_name: 需要验证产品名称 dg duba
    """
    magiccube_tool_path = get_product_path_by_productname(product_name)
    sambo_o = Samba("10.12.36.203", "duba", "duba123")
    sambo_o.download_dir("TcSpace", os.path.join('autotest', 'magiccube'), magiccube_tool_path, norm=False)
    # tool_path = os.path.join(magiccube_tool_path,'KDubaAnalyzeTool.exe')
    if not os.path.exists(magiccube_tool_path):
        log.log_info("下拉魔方工具失败")
        return False, magiccube_tool_path
    log.log_info("下拉魔方工具成功")
    return True, magiccube_tool_path


def update_magiccube_data(product_name):
    """
    更新魔方数据（精灵、毒霸）
    @param product_name: 需要验证产品名称 dg duba
    """
    product_path = get_product_path_by_productname(product_name)
    # 判断是否具有管理员权限
    if is_admin():
        os.chdir(product_path)
        os.system("kupdata.exe -magiccube_update")
    else:
        if sys.version_info[0] == 3:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    if not is_file_exists("dat", product_name):
        return False
    return True


def delete_magiccube_file(product_name):
    """
    删除魔方数据
    @param product_name: 需要验证产品名称 dg duba
    """
    basic_path = os.path.join(get_product_path_by_productname(product_name), "data")
    remove_path(os.path.join(basic_path, 'abtest_record.dat'))
    remove_path(os.path.join(basic_path, 'raw_record.dat'))
    remove_path(os.path.join(basic_path, 'switch_record.dat'))
    remove_path(os.path.join(basic_path, 'abtest_record.json'))
    remove_path(os.path.join(basic_path, 'raw_record.json'))
    remove_path(os.path.join(basic_path, 'switch_record.json'))


def get_product_path_by_productname(product_name):
    """
    通过产品名称获取产品安装路径
    @param product_name: 需要验证产品名称 dg duba
    """
    if product_name == 'dg':
        product_path = find_dgpath_by_reg()
    if product_name == 'duba':
        product_path = find_dubapath_by_reg()
    return product_path


def is_file_exists(file_type, product_name):
    """
    判断魔方加密/解密文件是否存在
    @param file_type: 判断类型：json为解密文件，dat为加密文件
    @param product_name: 需要验证产品名称 dg duba
    """
    magic_file_basic_path = os.path.join(get_product_path_by_productname(product_name), 'data')

    if file_type == 'json':
        abtest_record_json_path = os.path.join(magic_file_basic_path, 'abtest_record.json')
        raw_record_json_path = os.path.join(magic_file_basic_path, 'raw_record.json')
        switch_record_json_path = os.path.join(magic_file_basic_path, 'switch_record.json')
        # 判断是否存在加密文件
        if (os.path.exists(abtest_record_json_path)
                and os.path.exists(raw_record_json_path)
                and os.path.exists(switch_record_json_path)):
            log.log_info("解密文件存在")
        else:
            log.log_info("解密文件不存在")
            return False
    if file_type == 'dat':
        abtest_record_dat_path = os.path.join(magic_file_basic_path, 'abtest_record.dat')
        raw_record_dat_path = os.path.join(magic_file_basic_path, 'raw_record.dat')
        switch_record_dat_path = os.path.join(magic_file_basic_path, 'switch_record.dat')
        # 判断是否存在加密文件
        if (os.path.exists(abtest_record_dat_path)
                and os.path.exists(raw_record_dat_path)
                and os.path.exists(switch_record_dat_path)):
            log.log_info("加密文件存在")
        else:
            log.log_info("加密文件不存在")
            return False
    return True


def decode_magiccube(magiccube_path, product_name):
    """
    解密本地魔方数据
    @param product_path: 产品所处路径
    @param magiccube_path: 魔方工具所在路径
    @param product_name: 需要验证产品名称 dg duba
    """
    # 判断是否存在加密文件
    if not is_file_exists('dat', product_name):
        return
    # 判断是否具有管理员权限
    if is_admin():
        os.chdir(magiccube_path)
        os.system("KDubaAnalyzeTool.exe -action:magiccube_decrypt")
    else:
        if sys.version_info[0] == 3:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    # 执行完解密后判断解密文件是否存在
    if not is_file_exists('json', product_name):
        log.log_error("解密文件失败---解密后文件不存在")
    log.log_pass("解密文件成功")


def encode_magiccube(magiccube_path, product_name):
    """
    加密本地魔方数据
    @param product_path: 产品所处路径
    @param magiccube_path: 魔方工具所在路径
    @param product_name: 需要验证产品名称 dg duba
    """
    # 判断是否存在加密文件
    if not is_file_exists('json', product_name):
        return
    # 判断是否具有管理员权限
    if is_admin():
        os.chdir(magiccube_path)
        os.system("KDubaAnalyzeTool.exe -action:magiccube_encrypt")
    else:
        if sys.version_info[0] == 3:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    # 执行完解密后判断解密文件是否存在
    if not is_file_exists('dat', product_name):
        log.log_error("加密文件失败---加密后文件不存在")
    log.log_pass("加密文件成功")


def get_magicABT_data(product_name):
    """
    获取本地魔方Abtest数据
    @param product_name: 需要验证产品名称 dg duba
    """
    product_path = get_product_path_by_productname(product_name)
    magic_abrecord_path = os.path.join(product_path, 'data', 'abtest_record.json')
    with open(magic_abrecord_path, 'r') as f:
        data = json.load(f)  # dict
    return data


def get_magicABT_value_by_section(product_name, section_name, nesting_key="key_value", key_value_target_key="switch"):
    """
    获取Abtest中字典的value值
    :param nesting_key: 该key的value，嵌套了一个字典
    :param product_name: 产品名字（duba，dg）
    :param section_name: 魔方某个字典中，section_name的value值
    :param key_value_target_key: 魔方的某个key（nesting_key参数）嵌套字典中的key
    :return: 返回：key_value_target_key的value值, 参数section所处的整个字典
    """
    code = get_magicABT_data(product_name)
    is_section_exists = False
    for i in code["data"]:
        if i["section"] == section_name:
            key_value = eval(i[nesting_key])
            return key_value[key_value_target_key], i
    if not is_section_exists:
        log.log_info("解密魔方文件无找到指定section")
        return False


def get_magicSwitch_data(product_name):
    """
    获取本地魔方Switch数据
    @param product_name: 需要验证产品名称 dg duba
    """
    product_path = get_product_path_by_productname(product_name)
    magic_switchrecord_path = os.path.join(product_path, 'data', 'switch_record.json')
    with open(magic_switchrecord_path, 'r') as f:
        data = json.load(f)  # dict
    return data


def get_magicSwitch_value_by_section(product_name, section_name, nesting_key="key_value", key_value_target_key="switch"):
    """
    获取Switch中字典的value值
    :param nesting_key: 该key的value，嵌套了一个字典
    :param product_name: 产品名字（duba，dg）
    :param section_name: 魔方某个字典中，section_name的value值
    :param key_value_target_key: 魔方的某个key（nesting_key参数）嵌套字典中的key
    :return: 返回：key_value_target_key的value值, 参数section所处的整个字典
    """
    code = get_magicSwitch_data(product_name)
    is_section_exists = False
    for i in code["data"]:
        if i["section"] == section_name:
            key_value = eval(i[nesting_key])
            return key_value[key_value_target_key], i
    if not is_section_exists:
        log.log_info("解密魔方文件无找到指定section")
        return False


def get_magicRaw_data(product_name):
    """
    获取本地魔方Raw数据
    @param product_name: 需要验证产品名称 dg duba
    """
    product_path = get_product_path_by_productname(product_name)
    magic_rawrecord_path = os.path.join(product_path, 'data', 'raw_record.json')
    with open(magic_rawrecord_path, 'r') as f:
        data = json.load(f)  # dict
    return data


def get_magicRaw_value_by_section(product_name, section_name, nesting_key="key_value", key_value_target_key="switch"):
    """
    获取Raw中字典的value值
    :param nesting_key: 该key的value，嵌套了一个字典
    :param product_name: 产品名字（duba，dg）
    :param section_name: 魔方某个字典中，section_name的value值
    :param key_value_target_key: 魔方的某个key（nesting_key参数）嵌套字典中的key值
    :return: 返回：key_value_target_key的value值, 参数section所处的整个字典
    """
    code = get_magicRaw_data(product_name)
    is_section_exists = False
    for i in code["data"]:
        if i["section"] == section_name:
            key_value = eval(i[nesting_key])
            return key_value[key_value_target_key], i
    if not is_section_exists:
        log.log_info("解密魔方文件无找到指定section")
        return False


def update_magic_abdata_by_section(product_name, section_name, update_percent, aorb=None):
    """
    通过section更新ab测数据
    @param product_name: 验证产品名称
    @param section_name: 魔方配置的section_name
    @param update_percent: 更新后的abt比例 '30:70'
    @param aorb: 更新后需要命中a/b 'a'、'b'
    """
    abrecode = get_magicABT_data(product_name)  # dict
    atest_percent = int(update_percent.split(':')[0])
    btest_percent = int(update_percent.split(':')[1])
    percent = random.randint(1, 100)
    is_section_exists = False
    for i in abrecode['data']:  # abrecode['data'] is list
        if i["section"] == section_name:
            is_section_exists = True
            key_value = eval(i["key_value"])  # key_value is str
            key_value["switch"] = update_percent
            i["key_value"] = (str(key_value)).replace("'", "\"")  # i["key_value"] is dict
            if aorb == "a":
                i["percent"] = random.randint(1, atest_percent)
                i["strategyid"] = 1
            elif aorb == "b":
                i["percent"] = random.randint(atest_percent + 1, 100)
                i["strategyid"] = 2
            elif percent <= atest_percent:
                i["percent"] = percent
                i["strategyid"] = 1
            else:
                i["percent"] = percent
                i["strategyid"] = 2
            log.log_info("魔方数据已更新-json")
            break
    if is_section_exists:
        # 将新数据写入文件中
        product_path = get_product_path_by_productname(product_name)
        magic_abrecord_path = os.path.join(product_path, 'data', 'abtest_record.json')
        with open(magic_abrecord_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(abrecode, indent=4, ensure_ascii=False))
        log.log_info("魔方数据已更新至文件中---后续使用需要先加密为dat文件")
    else:
        log.log_info("未找到指定的section--请检查魔方平台配置")


def update_magic_switchdata_by_section(product_name, section_name, switch, status=None):
    """
    通过section更新switch数据
    @param product_name: 验证产品名称
    @param section_name: 魔方配置的section_name
    @param switch: 更新后的switch  '0','100'
    @param status: 更新后需要命中on、off
    """
    switchrecode = get_magicSwitch_data(product_name)  # dict
    is_section_exists = False
    for i in switchrecode['data']:
        if i['section'] == section_name:
            is_section_exists = True
            key_value = eval(i["key_value"])  # key_value is str  to  dict
            key_value["switch"] = switch
            i["key_value"] = (str(key_value)).replace("'", "\"")  # i["key_value"] is dict
            if status == 'on':
                i['on'] = 1
            elif status == 'off':
                i['on'] = 0
            log.log_info("魔方数据已更新-json")
            break
    if is_section_exists:
        # 将新数据写入文件中
        product_path = get_product_path_by_productname(product_name)
        magic_switchrecord_path = os.path.join(product_path, 'data', 'switch_record.json')
        with open(magic_switchrecord_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(switchrecode, indent=4, ensure_ascii=False))
        log.log_info("魔方数据已更新至文件中---后续使用需要先加密为dat文件")
    else:
        log.log_info("未找到指定的section--请检查魔方平台配置")


def update_magic_rawdata_by_section(product_name, section_name, update_dict):
    """
    通过section更新raw数据
    @param product_name: 验证产品名称
    @param section_name: 魔方配置的section_name
    @param update_dict: 需要更新的key_value中的key-value对
    """
    key_list = []
    for key in update_dict:
        key_list.append(key)
    rawrecode = get_magicRaw_data(product_name)  # dict
    is_section_exists = False
    for i in rawrecode['data']:
        if i['section'] == section_name:
            is_section_exists = True
            key_value = i['key_value']  # str
            key_value_new = eval(key_value)
            for key_update in update_dict:
                if key_update in key_list:
                    key_value_new[key_update] = update_dict[key_update]
            i["key_value"] = str(key_value_new).replace("'", "\"")
    if not is_section_exists:
        log.log_info("未找到指定的section--请检查魔方平台配置")
        return
    product_path = get_product_path_by_productname(product_name)
    magic_rawrecord_path = os.path.join(product_path, 'data', 'raw_record.json')
    with open(magic_rawrecord_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(rawrecode, indent=4, ensure_ascii=False))
    log.log_info("魔方数据已更新至文件中---后续使用需要先加密为dat文件")


if __name__ == "__main__":
    # get_magiccube_tools("duba")
    path = find_dubapath_by_reg()
    decode_magiccube(path, "duba")
    a = get_magicABT_value_by_section("duba", "KLSOFTMGR_ABTEST_COMMON_UNINSTALL", key_value_target_key="switch")[0]
    b = get_magicABT_value_by_section("duba", "KLSOFTMGR_ABTEST_COMMON_UNINSTALL")[1]
    print(b["id"])

#     update_magic_switchdata_by_section("duba","uplive_pop_show","100","on")
#     update_magic_abdata_by_section("duba", "defrag_pop_style_abtest", "50:50", "a")
#     update_magic_rawdata_by_section("duba", "KLSOFTMGR_SWITCH_ANTIREINSTALL_DEFENDPOP",update_dict)
