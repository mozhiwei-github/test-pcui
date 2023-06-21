import os
import shutil
import time
import psutil
import threading
from enum import unique, Enum
from psutil import NoSuchProcess, AccessDenied
from common.contants import PROCESS_MONITOR_CACHE
from common.csv_lib import CsvLib
from common.utils import get_pid, add_process_monitor

"""性能监控"""


@unique
class StatisticField(Enum):
    TIMESTAMP = "timestamp"
    CPU_PERCENT = "cpu_percent"
    MEM_USED = "memory_used"
    DISK_READ = "disk_read"
    DISK_WRITE = "disk_write"
    NET_SEND = "network_send"
    NET_RECV = "network_recv"


@unique
class ProcessField(Enum):
    TIMESTAMP = "timestamp"
    CPU_PERCENT = "cpu_percent"
    MEM_RSS = "memory_rss"
    DISK_READ = "disk_read"
    DISK_WRITE = "disk_write"
    NUM_HANDLES = "num_handles"  # 此进程当前使用的句柄数


class Monitor(object):
    def __init__(self, csv_path, interval=1, show_log=False, process_monitor=True, statistic_monitor=True,
                 process_folder=".proc_data"):
        """
        构造函数
        @param csv_path: csv文件路径
        @param interval: 采集间隔（秒）
        @param show_log: 显示日志信息
        @param process_monitor: 开启进程监控
        @param statistic_monitor: 开启系统性能监控
        @param process_folder: 进程监控数据存放文件夹名称
        """
        self.csv_path = csv_path
        if os.path.isabs(self.csv_path):
            self.dir_path = os.path.dirname(self.csv_path)
        else:
            self.dir_path = os.getcwd()
        self.interval = interval
        self.show_log = show_log
        self.process_monitor = process_monitor
        self.statistic_monitor = statistic_monitor
        self.process_folder = process_folder
        self.process_path = os.path.join(self.dir_path, process_folder)
        self.statistic_thread = None
        self.process_thread = None
        self.running = False
        self.last_disk_read_bytes = None
        self.last_disk_write_bytes = None
        self.last_network_bytes_sent = None
        self.last_network_bytes_recv = None
        # 进程监控相关
        self.proc_monitor_cache_size = 0
        self.monitored_process_info = {}
        # 获取初始信息
        self.get_disk_io_bytes()
        self.get_network_io_bytes()

    def start(self):
        self.running = True

        if self.statistic_monitor:
            self.statistic_thread = threading.Thread(target=self.get_statistic_info, name='StatisticThread')
            self.statistic_thread.start()

        if self.process_monitor:
            # 创建进程数据存储目录，已存在时清空重新创建
            if os.path.exists(self.process_path):
                shutil.rmtree(self.process_path)

            os.makedirs(self.process_path)

            self.process_thread = threading.Thread(target=self.get_process_info, name='ProcessThread')
            self.process_thread.start()

    def stop(self):
        self.running = False

        if self.statistic_thread:
            self.statistic_thread = None

        if self.process_monitor:
            self.process_monitor = None

    @staticmethod
    def get_cpu_percent():
        return psutil.cpu_percent()

    @staticmethod
    def get_memory_info(virtual=True):
        if virtual:
            return psutil.virtual_memory()

        return psutil.swap_memory()

    def get_disk_io_bytes(self):
        """获取硬盘读写速度"""
        io_counters = psutil.disk_io_counters()
        counter_read_bytes = io_counters.read_bytes
        counter_write_bytes = io_counters.write_bytes

        read_bytes = None
        write_bytes = None

        if self.last_disk_read_bytes:
            read_bytes = counter_read_bytes - self.last_disk_read_bytes

        if self.last_disk_write_bytes:
            write_bytes = counter_write_bytes - self.last_disk_write_bytes

        self.last_disk_read_bytes = counter_read_bytes
        self.last_disk_write_bytes = counter_write_bytes

        return read_bytes, write_bytes

    def get_network_io_bytes(self):
        """获取网络收发速度"""
        io_counters = psutil.net_io_counters()
        counter_bytes_sent = io_counters.bytes_sent
        counter_bytes_recv = io_counters.bytes_recv

        bytes_sent = None
        bytes_recv = None
        if self.last_network_bytes_sent:
            bytes_sent = counter_bytes_sent - self.last_network_bytes_sent

        if self.last_network_bytes_recv:
            bytes_recv = counter_bytes_recv - self.last_network_bytes_recv

        self.last_network_bytes_sent = counter_bytes_sent
        self.last_network_bytes_recv = counter_bytes_recv

        return bytes_sent, bytes_recv

    def bytes2kb(self, data, digits=1, interval=1):
        """
        bytes转KB
        @param data: 字节数
        @param digits: 保留小数点位数
        @param interval: 采集间隔（用于计算每秒速度）
        @return:
        """
        if data is None:
            return data

        return round((data / interval) / 1024, digits)

    def bytes2kbps(self, data, digits=1, interval=1):
        """
        bytes转kbps
        @param data: 字节数
        @param digits: 保留小数点位数
        @param interval: 采集间隔（用于计算每秒速度）
        @return:
        """
        if data is None:
            return data

        return round(self.bytes2kb(data, interval=interval) * 8, digits)

    def auto_sleep(self, start_time):
        interval = self.interval - (time.time() - start_time)
        if interval > 0:
            time.sleep(interval)

    def get_statistic_info(self):
        with CsvLib(self.csv_path, StatisticField._value2member_map_) as csv_lib:
            while self.running:
                start_time = time.time()

                cpu_percent = self.get_cpu_percent()
                memory_used = self.bytes2kb(self.get_memory_info().used)
                read_bytes, write_bytes = self.get_disk_io_bytes()
                bytes_sent, bytes_recv = self.get_network_io_bytes()

                disk_read = self.bytes2kb(read_bytes, interval=self.interval)
                disk_write = self.bytes2kb(write_bytes, interval=self.interval)

                network_send = self.bytes2kbps(bytes_sent, interval=self.interval)
                network_recv = self.bytes2kbps(bytes_recv, interval=self.interval)

                if self.show_log:
                    print(f"cpu_percent: {cpu_percent}%")
                    print(f"memory_used: {memory_used} KB")
                    print(f"disk_io read: {disk_read} KB/s, write: {disk_write} KB/s")
                    print(f"network_io send: {network_send} Kbps, recv: {network_recv} Kbps")
                    print("-" * 50)

                csv_lib.write_row({
                    StatisticField.TIMESTAMP.value: int(round(time.time() * 1000)),
                    StatisticField.CPU_PERCENT.value: cpu_percent,
                    StatisticField.MEM_USED.value: memory_used,
                    StatisticField.DISK_READ.value: disk_read,
                    StatisticField.DISK_WRITE.value: disk_write,
                    StatisticField.NET_SEND.value: network_send,
                    StatisticField.NET_RECV.value: network_recv,
                })

                self.auto_sleep(start_time)

    def get_process_info(self):
        cpu_count = psutil.cpu_count()
        while self.running:
            start_time = time.time()
            # 更新监控进程信息
            self.update_process_monitor()

            # 获取监控进程性能数据
            for proc_name in self.monitored_process_info:
                process_info = self.monitored_process_info[proc_name]

                if not process_info["csv_file"]:
                    csv_path = os.path.join(self.process_path, f"{proc_name}.csv")
                    process_info["csv_file"] = CsvLib(csv_path, ProcessField._value2member_map_)

                proc_cpu_percent = 0
                proc_memory_rss = 0
                proc_disk_read = 0
                proc_disk_write = 0
                proc_num_handles = 0

                for pid in list(process_info["pid_info"].keys()):
                    pid_info = process_info["pid_info"][pid]

                    try:
                        if not pid_info["process"]:
                            pid_info["process"] = psutil.Process(pid)

                        p = pid_info["process"]

                        if pid_info["last_disk_read_bytes"] is None or pid_info["last_disk_write_bytes"] is None:
                            with p.oneshot():
                                pid_info["last_disk_read_bytes"] = p.io_counters().read_bytes
                                pid_info["last_disk_write_bytes"] = p.io_counters().write_bytes

                        with p.oneshot():
                            # 将进程CPU利用率除以CPU个数，使其与Windows任务管理器显示一致
                            cpu_percent = p.cpu_percent() / cpu_count
                            memory_rss = self.bytes2kb(p.memory_info().rss)

                            p_read_bytes = p.io_counters().read_bytes - pid_info["last_disk_read_bytes"]
                            p_write_bytes = p.io_counters().write_bytes - pid_info["last_disk_write_bytes"]

                            pid_info["last_disk_read_bytes"] = p.io_counters().read_bytes
                            pid_info["last_disk_write_bytes"] = p.io_counters().write_bytes

                            disk_read = self.bytes2kb(p_read_bytes, interval=self.interval)
                            disk_write = self.bytes2kb(p_write_bytes, interval=self.interval)

                            num_handles = p.num_handles()

                            proc_cpu_percent += cpu_percent
                            proc_memory_rss += memory_rss
                            proc_disk_read += disk_read
                            proc_disk_write += disk_write
                            proc_num_handles += num_handles

                    except (NoSuchProcess, AccessDenied):
                        del process_info["pid_info"][pid]
                    except Exception as e:
                        print(e)

                proc_cpu_percent = round(proc_cpu_percent, 2)
                proc_memory_rss = round(proc_memory_rss, 2)
                proc_disk_read = round(proc_disk_read, 2)
                proc_disk_write = round(proc_disk_write, 2)

                if self.show_log:
                    print(f"{proc_name} cpu: {proc_cpu_percent} %")
                    print(f"{proc_name} memory: {proc_memory_rss} KB")
                    print(f"{proc_name} disk read: {proc_disk_read} KB/s, write: {proc_disk_write} KB/s")
                    print(f"{proc_name} used handles: {proc_num_handles}")
                    print("*" * 50)

                process_info["csv_file"].write_row({
                    ProcessField.TIMESTAMP.value: int(round(time.time() * 1000)),
                    ProcessField.CPU_PERCENT.value: proc_cpu_percent,
                    ProcessField.MEM_RSS.value: proc_memory_rss,
                    ProcessField.DISK_READ.value: proc_disk_read,
                    ProcessField.DISK_WRITE.value: proc_disk_write,
                    ProcessField.NUM_HANDLES.value: proc_num_handles,
                })

            self.auto_sleep(start_time)

        # 关闭进程监控的csv文件
        for proc_name in self.monitored_process_info:
            process_info = self.monitored_process_info[proc_name]
            if process_info["csv_file"]:
                process_info["csv_file"].close()

    def update_process_monitor(self):
        if not os.path.exists(PROCESS_MONITOR_CACHE):
            return

        # 缓存文件大小未改变时，不更新监控进程
        cache_size = os.path.getsize(PROCESS_MONITOR_CACHE)
        if cache_size == self.proc_monitor_cache_size:
            return

        self.proc_monitor_cache_size = cache_size

        # 读取监控进程名
        with open(PROCESS_MONITOR_CACHE, "r") as pmc:
            proc_name_list = pmc.read().splitlines()

        proc_name_list = list(set(proc_name_list))

        for proc_name in proc_name_list:
            proc_pid_list = get_pid(proc_name, first=False)
            if not proc_pid_list:
                continue

            if proc_name not in self.monitored_process_info:
                self.monitored_process_info[proc_name] = {
                    "proc_name": proc_name,
                    "csv_file": None,
                    "pid_info": {},
                }

            proc_pid_info = self.monitored_process_info[proc_name]["pid_info"]
            for proc_pid in proc_pid_list:
                if proc_pid not in proc_pid_info:
                    proc_pid_info[proc_pid] = {
                        "process": None,
                        "last_disk_read_bytes": None,
                        "last_disk_write_bytes": None
                    }


if __name__ == '__main__':
    # monitor = Monitor("statistic_info.csv", interval=1, show_log=True)
    # monitor.start()
    # time.sleep(60*35)
    # monitor.stop()
    # print(monitor.get_pid_by_process_name("kxetray.exe"))
    # print(monitor.get_pid_by_process_name("chrome.exe"))

    # monitor = Monitor("statistic_info.csv", interval=1, show_log=True, statistic_monitor=False)
    # add_process_monitor("chrome.exe")
    try:
        monitor = Monitor("statistic_info.csv", interval=1, show_log=True)
        monitor.start()
        time.sleep(60 * 0.5)
    except KeyboardInterrupt:
        print('close monitor')
    finally:
        monitor.stop()
