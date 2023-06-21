# _*_ coding:UTF-8 _*_
import json
import os
import sys
import subprocess
import run_ui_test
from common.contants import EnvVar, PROCESS_MONITOR_CACHE
from common.log import log
from common.performance.catcher import MachineInfoCatcher
from common.performance.monitor import Monitor
from common.utils import get_host_ip, task_statistic_upload, zip_dir_compress
from common.api.cds import kvm_image_sync_api
from common.yaml_reader import YamlReader

sys.path.append(os.path.join(os.getcwd(), "common"))

"""由tcservice.exe启动的测试脚本"""


def upload_monitor_info(case_id, statistic_path=None, process_path=None):
    """
    上传性能监控数据
    @param case_id: 用例ID
    @param statistic_path: 机器性能数据路径
    @param process_path: 进程性能数据目录路径
    @return:
    """
    # 上传机器性能数据
    if statistic_path and os.path.exists(statistic_file_path):
        upload_result = task_statistic_upload(case_id, statistic_file_path)
        if upload_result:
            print("upload statistic info success")
        else:
            print(f"[Error]upload statistic info failed")

    # 压缩并上传进程性能数据
    if process_path and os.path.exists(process_path):
        output_path = f"{process_path}.zip"
        if os.path.exists(output_path):
            os.remove(output_path)

        process_zip_path = zip_dir_compress(process_path, output_path)
        if not process_zip_path:
            print("[Error]compress process info failed")
            return

        upload_result = task_statistic_upload(case_id, process_zip_path)
        if upload_result:
            print("upload process info success")
        else:
            print(f"[Error]upload process info failed")


if __name__ == "__main__":
    cmd = ""
    case_param = ""
    case_startup_path = ""

    # 从配置文件中获取需要执行虚拟机镜像同步的用例列表
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "common", "config", "config.yml")
    reader = YamlReader()
    config_data = reader.read_yaml(config_path)
    kvm_sync_cases = []
    for config in config_data.values():
        for case in config.get("cases", []):
            do_kvm_sync = bool(case.get("kvm_sync", False))
            case_path = case.get("param")
            if do_kvm_sync and case_path:
                kvm_sync_cases.append(case_path)

    try:
        case_id = os.environ.get(EnvVar.CASE_ID.value, None)
        autotestenv = json.loads(os.environ.get(EnvVar.AUTO_TEST_ENV.value))
        case_param = autotestenv["param"]
        case_startup_path = autotestenv["tcpath"]
        pypath = os.path.join(os.getcwd(), case_startup_path)
        cmd = f"python {pypath} {case_param}"
    except:
        params_list = sys.argv
        params_list.remove(sys.argv[0])
        params = ""
        for p in params_list:
            params = f"{params} {p}"
        cmd = f"python {params}"

    assert case_id, "读取案例ID环境变量失败"

    # 获取机器信息
    print("start machine info catcher...")
    catcher = MachineInfoCatcher()
    catcher.get_all()
    save_result = catcher.save_machine_info(case_id)
    if not save_result:
        print(f"[Error]upload machine info failed")
    print("upload machine info success")

    # 开始收集性能数据
    print("start statistic info monitor...")

    print(PROCESS_MONITOR_CACHE)
    if os.path.exists(PROCESS_MONITOR_CACHE):
        print(f"del PROCESS_MONITOR_CACHE")
        os.remove(PROCESS_MONITOR_CACHE)

    statistic_file_path = os.path.join(os.getcwd(), "statistic_info.csv")
    monitor = Monitor(statistic_file_path, interval=1)
    monitor.start()

    print("start running " + cmd)
    p = subprocess.Popen(cmd)
    p.wait()

    # 停止性能数据收集
    monitor.stop()

    # 上传性能数据
    upload_monitor_info(case_id, statistic_file_path, monitor.process_path)

    # KVM环境运行用例结束后，判断是否需要执行虚拟机镜像同步
    if os.environ.get(EnvVar.KVM_ENV.value, None) == "1" and case_param:
        case_name = os.environ.get(EnvVar.CASE_NAME.value, None)
        case_username = os.environ.get(EnvVar.USERNAME.value, None)
        _, ui_test_filename = os.path.split(run_ui_test.__file__)
        case_list = case_param.split(" ")[0].split(",")
        # 触发用户为robot、启动文件为UI测试，且用例只有毒霸/壁纸升级用例时，运行结束调用虚拟机镜像同步接口
        if case_username == "robot" and case_startup_path == ui_test_filename and len(case_list) == 1:
            running_case = case_list[0]
            for sync_case_name in kvm_sync_cases:
                if sync_case_name.endswith(running_case):
                    ip = get_host_ip()
                    kvm_image_sync_api(ip, case_id, case_name, case_username)

    log.log_finish()
