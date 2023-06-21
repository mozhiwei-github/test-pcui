import os
from ftplib import FTP
import traceback
import sys
from common.log import log


# 如需要支持中文名文件传输，需要将ftplib.py文件中的  encoding = "latin-1"  改为   encoding = "utf-8"
class FTP1(FTP):  # 继承FTP类，修改解码参数，解决不识别文件名中文的问题
    encoding = "utf-8"

upload_file_count = 0  # 计算有多少文件上传到了FTP
def is_same_size(ftp, local_file, remote_file):
    """
        比对本地文件和上传文件的大小
        @param ftp: ftp
        @param local_file: 配置本地文件夹的路径
        @param remote_file: 配置远端FTP的文件夹路径
        @return:
        """
    try:
        remote_file_size = ftp.size(remote_file)  # 获取远端文件大小
        log.log_info("获取远程文件大小为：%s" % remote_file_size)
    except Exception as err:
        log.log_info("获取远程文件大小失败, 原因为:%s" % err)
        remote_file_size = -1  # 如果获取FTP文件失败，则返回-1
    try:
        local_file_size = os.path.getsize(local_file)  # 获取本地文件大小
    except Exception as err:
        log.log_info("获取本地文件大小失败, 原因为:%s" % err)
        local_file_size = -1  # 如果获取本地文件失败，则返回-1
        # 三目运算符
    result = True if (remote_file_size == local_file_size) else False  # 文件大小对比
    return result, remote_file_size, local_file_size  # 返回对比结果，FTP文件和本地文件的大小


def upload_file(ftp, local_file, remote_file):
    """
        上传单个文件的函数,里面调用了比对本地文件和上传文件的大小的函数
        @param ftp: ftp
        @param local_file: 配置本地文件夹的路径
        @param remote_file: 配置远端FTP的文件夹路径
        @return:
        """
    global upload_file_count
    fail_count=0
    # 检查本地是否有此文件
    if not os.path.exists(local_file):  # 如果不存在本地文件，记录日志并返回False
        log.log_info(f'上传文件：本地待上传的文件:{local_file}不存在。')
    result, remote_file_size, local_file_size = is_same_size(ftp, local_file, remote_file)  # FTP如果文件已存在，则对比大小
    if True != result:  # 如果对比大小不一致，则上传文件
        log.log_info(f'上传文件：远程文件 {remote_file} 不存在，现在开始上传...')
        global FTP_PERFECT_BUFF_SIZE  # 把全局变量传进来
        try:  # 上传文件到FTP
            with open(local_file, 'rb') as f:  # 打开本地文件
                # ftp.retrbinary('RETR %s' % remote_file, f.write, buffsize)    #下载FTP文件
                if ftp.storbinary('STOR ' + remote_file, f):  # 上传本地文件到FTP
                    result, remote_file_size, local_file_size = is_same_size(ftp, local_file, remote_file)
                # 打印上传失败或成功的日志
                log.log_info(
                    f'{remote_file}文件上传成功, 远程文件大小 = {remote_file_size}, 本地文件大小 = {local_file_size}')
                upload_file_count += 1
        except Exception as err:
            log.log_info(f'上传文件有错误发生:{local_file}, 错误:{err}')
            fail_count += 1
            result = False
    else:
        log.log_info(f'{local_file}文件已存在，无需上传!')

def upload_file_tree(local_path, remote_path, ftp, IsRecursively=True):
    """
            上传目录的函数，里面有调用上传单个文件的函数
            @param local_path: 配置本地文件夹的路径
            @param remote_path: 配置远端FTP的文件夹路径
            @param ftp: ftp
            @param IsRecursively: 是否复制子目录下文件的开关，不需要可配置为False,默认为True
            @return:
            """
    fail_count=0
    # 有远端目录的话进入目录，没有目录的话创建目录
    log.log_info('================开始上传本地文件到ftp！========================')
    log.log_info(f'upload_file_tree函数开始运行！FTP远程目录为:{remote_path}')
    # 切换到FTP的目标目录，如果没有的话则创建
    try:
        ftp.cwd(remote_path)  # 进入FTP工作目录
    except Exception as e:
        log.log_info(f'FTP目录：{remote_path}文件夹不存在，错误信息:{e}')
        base_dir, part_path = ftp.pwd(), remote_path.split('/')
        for subpath in part_path:
            # 针对类似  '//wangshaobo/dump/' 格式的目录
            if '' == subpath:  # 如果是空字符，跳出此循环，执行下一个。
                continue
            base_dir = (os.path.join(base_dir, subpath)).replace("\\", "/")  # base_dir + subpath  # 拼接子目录,去除\为/
            try:
                ftp.cwd(base_dir)  # 进入目录
            except Exception as e:
                log.log_info(f'创建FTP目录:{base_dir}')
                ftp.mkd(base_dir)  # 不存在创建当前子目录 直到创建所有
                continue
        ftp.cwd(remote_path)  # 进入FTP工作目录
    # 本地目录切换
    try:
        # 远端目录通过ftp对象已经切换到指定目录或创建的指定目录
        file_list = os.listdir(local_path)  # 列出本地文件夹第一层目录的所有文件和目录
        for file_name in file_list:
            if os.path.isdir(os.path.join(local_path, file_name)):  # 判断是文件还是目录，是目录为真
                if IsRecursively:  # 递归变量，默认为Ture
                    # 使用FTP进入远程目录，如果没有远程目录则创建它
                    try:  # 如果是目录，则尝试进入到这个目录，再退出来。
                        cwd = ftp.pwd()  # 获取FTP当前路径
                        ftp.cwd(file_name)  # 如果cwd成功 则表示该目录存在 退出到上一级
                        ftp.cwd(cwd)  # 再返回FTP之前的目录
                    except Exception as e:
                        ftp.mkd(file_name)  # 建立目录
                        log.log_info(f'在{remote_path}目录中新建子目录 {file_name} ...')
                    p_local_path = os.path.join(local_path, file_name)  # 拼接本地第一层子目录，递归时进入下一层
                    p_remote_path = os.path.join(ftp.pwd(), file_name)  # 拼接FTP第一层子目录，递归时进入下一层
                    upload_file_tree(p_local_path, p_remote_path, ftp, IsRecursively)  # 递归
                    ftp.cwd("..")  # 对于递归 ftp 每次传输完成后需要切换目录到上一级
                else:
                    log.log_info('传输模式是非递归模式,不会创建多级目录!')
                    continue
            else:
                # 是文件 直接上传
                local_file = os.path.join(local_path, file_name)
                remote_file = os.path.join(remote_path, file_name).replace("\\", "/")
                upload_file(ftp, local_file, remote_file)

    except:
        log.log_info(f'上传文件时有一些错误发生 :{file_name},错误:{traceback.format_exc()}')
        fail_count += 1
    type_dict = dict()
    for each_type in type_dict:
        if each_type == '文件夹':
            continue
        log.log_info(f"目录[{local_path}]中文件类型为[{each_type}]的数量有：{type_dict[each_type]} 个")
    log.log_info(f"目录[{local_path}]本地文件数量为:{file_count(local_path)}，本次FTP文件累计上传数量为:{upload_file_count}")
    if not fail_count:
        log.log_info("本地文件上传FTP全部成功！")
    else:
        log.log_info("本地文件上传FTP有失败记录，请检查日志！")
    log.log_info('===================上传本地文件到ftp结束！======================')
    return


# 计算本地文件夹中文件个数
def file_count(local_path, type_dict=dict()):
    """
            计算本地文件夹中文件个数
            @param local_path: 配置本地文件夹的路径
            @param type_dict: 定义一个保存文件类型及数量的空字典
            @return:
            """
    local_file_count=0  # 声明全局变量
    file_list = os.listdir(local_path)  # 列出本地文件夹第一层目录的所有文件和目录
    for file_name in file_list:
        if os.path.isdir(os.path.join(local_path, file_name)):  # 判断是文件还是目录，是目录为真
            type_dict.setdefault("文件夹", 0)  # 如果字典key不存在，则添加并设置为初始值
            type_dict["文件夹"] += 1
            p_local_path = os.path.join(local_path, file_name)  # 拼接本地第一层子目录，递归时进入下一层
            file_count(p_local_path, type_dict)
        else:
            ext = os.path.splitext(file_name)[1]  # 获取到文件的后缀
            type_dict.setdefault(ext, 0)  # 如果字典key不存在，则添加并设置为初始值
            type_dict[ext] += 1
            local_file_count += 1  # 计算总文件数量
    return local_file_count


if __name__ == '__main__':

    # 配置连接FTP的参数
    host = '10.12.36.203'  # $$$ 配置FTP服务器IP
    port = 21
    username = 'duba'  # $$$ 配置FTP帐号
    password = 'duba123'  # $$$ 配置FTP密码
    ftp = FTP1()
    ftp.connect(host, port)
    ftp.login(username, password)
    # 定义变量
    local_path = ''  # $$$ 配置本地文件夹的路径
    remote_path = ''  # $$$ 配置远端FTP的文件夹路径

    # 本地文件计数和上传文件
    file_count(local_path)  # 运行计算本地文件夹文件数量








