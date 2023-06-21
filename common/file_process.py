#!/usr/bin/evn python
# --coding = 'utf-8' --
# Author An hongyun
# Python Version 3.8
import os
import sys
import platform
import configparser

if platform.system() == "Windows":
    import winreg


# print(os.name)
# print(sys.getdefaultencoding())
# print(sys.version)
# print(sys.version_info)

class FileOperation:
    def __init__(self, file, encoding=None):
        self.file = file
        self.conf = configparser.ConfigParser()
        self.conf.read(file, encoding)

    def get_appdata(self):
        return os.getenv('APPDATA')

    def get_desktop(self):
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        return winreg.QueryValueEx(key, "Desktop")[0]

    # 获取ini配置文件中section名称
    def get_sessions(self):
        return self.conf.sections()

    # 获取ini配置文件中section下所有字段内容
    def get_items(self, sec):
        return self.conf.items(section=sec)

    # 获取某一个section下所有option字段
    def get_options(self, sec):
        return self.conf.options(section=sec)

    # 获取某一个section下，某一个option下的值
    def get_option(self, sec, opt):
        result = None
        if self.conf.has_option(sec, opt):
            result = self.conf.get(sec, opt)
        return result

    # 添加section
    def add_section(self, section):
        self.conf.add_section(section)

    # 删除section
    def del_section(self, section):
        self.conf.remove_section(section)

    # 修改某一个section下，某一option下的值
    # 若sec, opt为空，则会自动创建
    def set_option(self, sec, opt, new_value):
        if not (sec in self.get_sessions()):
            self.add_section(sec)
        self.conf.set(sec, opt, new_value)
        f = open(self.file, 'w')
        self.conf.write(f)
        f.close()

    def set_options(self, sec, opt_value):
        """
        批量修改某一个section下，某一option下的值
        :param sec: 目标section
        :param opt_value: opt_value键值对，组成的列表或元祖
        :return:
        """
        for i in range(len(opt_value)):
            self.set_option(sec, opt_value[i][0], opt_value[i][1])

    def del_option(self, sec, opt):
        """
        删除某一个section下，某一个option
        :param sec: 目标section
        :param opt: 目标option
        :return:
        """
        if self.conf.has_option(sec, opt):
            self.conf.remove_option(sec, opt)
            f = open(self.file, 'w')
            self.conf.write(f)
            f.close()

    def del_option_by_list(self, sec, removeOption: list = None):
        """
        某一个section下，批量删除指定option
        :param sec: 目标section
        :param removeOption: 要删除的option的列表
        :return:
        """
        if removeOption is not None:
            for b in range(len(removeOption)):
                self.del_option(sec, removeOption[b - 1])
        with open(self.file, "w") as file:
            self.conf.write(file)

    def del_section_by_list(self, removeSection: list = None):
        """
        批量刪除section
        :param removeSection: 要删除的删除section列表
        :return:
        """
        if removeSection is not None:
            for b in range(len(removeSection)):
                self.conf.remove_section(removeSection[b - 1])
        with open(self.file, "w") as file:
            self.conf.write(file)

    # 批量添加section
    def add_section_by_list(self, addSection: list = None):
        if addSection is not None:
            for a in range(len(addSection)):
                self.conf.add_section(addSection[a - 1])
        with open(self.file, "w") as file:
            self.conf.write(file)


class DirOperation():
    # 判断目录是否存在，若不存在，则创建
    def makedir(self, filepath):
        if not os.path.exists(path=filepath):
            os.makedirs(filepath)
