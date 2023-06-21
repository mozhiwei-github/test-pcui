import os
import shutil
from common.log import log
from common.utils import try_import

SMBConnection = try_import('smb.SMBConnection', 'SMBConnection')

"""smb操作"""


class Samba(object):
    def __init__(self, server_ip, username, password, port=445):
        self.conn = SMBConnection(username, password, "", server_ip, is_direct_tcp=True)
        assert self.conn.connect(server_ip, port)

    def download_dir(self, service_name, dir_path, target_path, norm = True):
        """
        递归下载目录下所有文件
        @param service_name: 路径的共享文件夹的名称
        @param dir_path: 相对于service_name的路径
        @param target_path: 下载目标路径
        @param norm: 是否需要判断目标路径是否存在（是否需要重新创建目录）--由于有些工具需要直接下拉到本地的一些现存目录下
                     True 则重新创建target_path目录，若已存在target_path，则会覆盖（即原有文件都删除）
        @return:
        """
        file_info_list = []
        full_dir_name = os.path.join(service_name, dir_path)

        if os.path.exists(target_path) and norm:
            shutil.rmtree(target_path)
        # 创建目标下载目录
        if norm:
            os.makedirs(target_path)

        try:
            for f in self.conn.listPath(service_name, dir_path):
                if f.filename in ['.', '..']:
                    continue

                filepath = os.path.join(dir_path, f.filename)
                target_filepath = os.path.join(target_path, f.filename)
                # 如果为文件夹则再进入该文件夹递归下载
                if f.isDirectory:
                    sub_download_result, sub_file_info_list = self.download_dir(service_name, filepath, target_filepath)
                    file_info_list.extend(sub_file_info_list)
                    if not sub_download_result:
                        return sub_download_result, file_info_list
                else:
                    try:
                        with open(target_filepath, "wb") as t:
                            self.conn.retrieveFile(service_name, filepath, t)

                        file_info_list.append({
                            "filepath": target_filepath,
                            "filename": f.filename,
                        })
                    except Exception as e:
                        log.log_error(f"smb download failed, file: {full_dir_name}, err: {e}", attach=False, need_assert=False)
                        return False, file_info_list

        except Exception as e:
            log.log_error(f"smb download failed, dir: {full_dir_name}, err: {e}", attach=False, need_assert=False)
            return False, file_info_list

        return True, file_info_list

    def download_file(self, service_name, dir_path, target_path, f_name, norm=True):
        """
               下载目录中指定单个文件
               @param service_name: 路径的共享文件夹的名称
               @param dir_path: 相对于service_name的路径
               @param target_path: 下载目标路径
               @param f_name: 指定文件名
               @param norm: 是否需要判断目标路径是否存在
               @return:
        """
        full_dir_name = os.path.join(service_name, dir_path)
        # 创建目标下载目录
        if os.path.exists(target_path) and norm:
            shutil.rmtree(target_path)
        if norm:
            os.makedirs(target_path)
        filepath = os.path.join(dir_path, f_name)
        target_filepath = os.path.join(target_path, f_name)
        try:
            with open(target_filepath, "wb") as t:
                self.conn.retrieveFile(service_name, filepath, t)
        except Exception as e:
            log.log_error(f"smb download failed, file: {full_dir_name}, err: {e}", attach=False, need_assert=False)
            return False
        return True, f_name