"""性能数据统计信息"""


class StatisticInfo(object):
    def __init__(self, cpu_percent=None, memory_percent=None, disk_read_bytes=None, disk_write_bytes=None,
                 net_bytes_sent=None, net_bytes_recv=None):
        self.cpu_percent = cpu_percent
        self.memory_percent = memory_percent
        self.disk_read_bytes = disk_read_bytes
        self.disk_write_bytes = disk_write_bytes
        self.net_bytes_sent = net_bytes_sent
        self.net_bytes_recv = net_bytes_recv

    @property
    def data(self):
        return self.__dict__


class MachineInfo(object):
    def __init__(self):
        # 操作系统
        self.sys_info = {}
        # 主板
        self.motherboard_info = {}
        # CPU
        self.cpu_info = {}
        # GPU
        self.gpu_info = []
        # 内存
        self.ram_info = []

    def update_sys_info(self, caption, version, os_architecture):
        """
        更新系统信息
        @param caption: 系统说明
        @param version: 版本号
        @param os_architecture: 操作系统架构
        @return:
        """
        self.sys_info = {
            "caption": caption,
            "version": version,
            "os_architecture": os_architecture,
        }

    def update_motherboard_info(self, model, manufacturer):
        """
        更新主板信息
        @param model: 型号
        @param manufacturer: 制造商
        @return:
        """
        self.motherboard_info = {
            "model": model,
            "manufacturer": manufacturer,
        }

    def update_cpu_info(self, model, core_count, logical_core_count):
        """
        更新CPU信息
        @param model: 型号
        @param core_count: 核心数
        @param logical_core_count: 逻辑核心数
        @return:
        """
        self.cpu_info = {
            "model": model,
            "core_count": core_count,
            "logical_core_count": logical_core_count,
        }

    def update_gpu_info(self, caption, adapter_ram):
        """
        更新显卡信息
        @param caption: 显卡说明
        @param adapter_ram: 显存大小（单位：GB）
        @return:
        """
        self.gpu_info.append({
            "caption": caption,
            "adapter_ram": adapter_ram,
        })

    def update_ram_info(self, caption, manufacturer, capacity, memory_type, speed):
        """
        更新内存信息
        @param caption: 内存说明
        @param manufacturer: 制造商
        @param capacity: 容量（单位：GB）
        @param memory_type: 内存类型（20：DDR 21: DDR2 22: DDR2 FB-DIMM 24: DDR3 26: DDR4）
        @param speed: 速度（单位：MHz）
        @return:
        """
        self.ram_info.append({
            "capacity": capacity,
            "caption": caption,
            "manufacturer": manufacturer,
            "memory_type": memory_type,
            "speed": speed,
        })

    @property
    def data(self):
        return self.__dict__


if __name__ == '__main__':
    info = StatisticInfo()
    print(info.data)
    # machine_info = MachineInfo()
    # print(machine_info.data)
