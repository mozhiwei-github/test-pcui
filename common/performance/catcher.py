import wmi
from common.performance.statistic_info import MachineInfo
from common.utils import info_up

"""机器信息获取"""


class MachineInfoCatcher(object):
    def __init__(self):
        self.wmi_obj = wmi.WMI()
        self.machine_info = MachineInfo()

    def get_system_info(self):
        """
        获取系统信息
        @return:
        """
        system_info = self.wmi_obj.Win32_OperatingSystem()[0]
        data = {
            'caption': system_info.Caption,
            'version': system_info.Version,
            'os_architecture': system_info.OSArchitecture,
        }

        return data

    def get_motherboard_info(self):
        """
        获取主板信息
        :return:
        """
        computer_info = self.wmi_obj.Win32_ComputerSystem()[0]
        data = {
            'manufacturer': computer_info.Manufacturer,
            'model': computer_info.Model,
        }

        return data

    def get_cpu_info(self):
        """
        获取CPU信息
        @return:
        """
        cpu_lists = self.wmi_obj.Win32_Processor()
        cpu_core_count = 0
        logical_cpu_core_count = 0
        for cpu in cpu_lists:
            cpu_core_count += cpu.NumberOfCores
            logical_cpu_core_count += cpu.NumberOfLogicalProcessors

        cpu_model = cpu_lists[0].Name  # CPU型号（所有的CPU型号都是一样的）
        data = {
            "model": cpu_model,
            "core_count": cpu_core_count,
            "logical_core_count": logical_cpu_core_count
        }

        return data

    def get_gpu_info(self):
        """
        获取显卡信息
        @return:
        """
        info = []
        for gpu in self.wmi_obj.Win32_videocontroller():
            if not gpu:
                continue

            try:
                gpu_adapterRAM = gpu.AdapterRAM or 0
                ram_size = int(int(gpu_adapterRAM) / (1024 ** 3))  # 转换内存单位为GB
                info.append({
                    'caption': gpu.Caption,  # 显卡名称
                    'adapter_ram': ram_size,  # 显存（单位：GB）
                })
            except Exception as e:
                print(f"[Error]get_gpu_info failed: {e}")
                continue

        return info

    def get_ram_info(self):
        """
        获取内存信息
        :return:
        """
        info = []
        for ram in self.wmi_obj.Win32_PhysicalMemory():
            if not ram:
                continue

            try:
                ram_capacity = ram.Capacity or 0
                ram_size = int(int(ram_capacity) / (1024 ** 3))  # 转换内存单位为GB
                info.append({
                    "caption": ram.Caption,
                    "manufacturer": ram.Manufacturer,
                    "capacity": ram_size,
                    "memory_type": ram.SMBIOSMemoryType,  # 内存类型 20：DDR 21: DDR2 22: DDR2 FB-DIMM 24: DDR3 26: DDR4
                    "speed": ram.Speed,
                })
            except Exception as e:
                print(f"[Error]get_ram_info failed: {e}")
                continue

        return info

    def get_all(self):
        system_info = self.get_system_info()
        self.machine_info.update_sys_info(**system_info)

        cpu_info = self.get_cpu_info()
        self.machine_info.update_cpu_info(**cpu_info)

        motherboard_info = self.get_motherboard_info()
        self.machine_info.update_motherboard_info(**motherboard_info)

        gpu_info_list = self.get_gpu_info()
        for gpu_info in gpu_info_list:
            self.machine_info.update_gpu_info(**gpu_info)

        ram_info_list = self.get_ram_info()
        for ram_info in ram_info_list:
            self.machine_info.update_ram_info(**ram_info)

    def save_machine_info(self, case_id):
        """存储机器信息到测试平台"""
        info_data = self.machine_info.data
        info_data["caseid"] = case_id
        return info_up(info_data)


if __name__ == '__main__':
    catcher = MachineInfoCatcher()
    catcher.get_all()
    print(catcher.machine_info.data)
    # save_result = catcher.save_machine_info("1")
    # print(save_result)
