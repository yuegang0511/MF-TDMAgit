from MF_layer2_class import *
from MF_module_class import *
import numpy as np
import random
from matplotlib import pyplot as plt
from scipy.fftpack import fft, ifft


def random_generate(num):
    random_data = ""
    for i in range(num):
        random_data = random_data + str(random.randint(0, 100) % 2)
    return random_data


class Substation(object):
    # 需要一个链路层数据源 layer_frame 字典形式（speed=128，time=1） 传递两个参数，一个为速率，一个为时长（时长的一个帧的时长）生成了一个帧长的数据
    # 子站有一个唯一id，由mainstation分配
    # 需要一个调制方式
    # 需要频分复用过程中的载频和时隙信息，数据格式为字典格式，键为时隙信息，值为频率信息，以一个帧为例
    # 输出时域和频域的结果
    def __init__(self, id="aaaaaaaa"):
        self.frequency = []
        self.slot = []
        self.id = id
        self.mac = random_generate(32)
        # self.mac_generate()
        # 定义csc信息变量，固定格式，长度欸112bit，包含子站的mac地址,定义前序为16bit，mac地址为32bit
        self.csc_info = ""
        self.pre_csc = random_generate(16)
        # 定义acq信息变量,包长较短，载频的数据为16bit
        self.acq = ""
        self.pre_acp = random_generate(16)
        # 定义sync信息变量，由前导和业务信令业务心灵为128bit
        self.sync = ""
        self.pre_sync = random_generate(16)
        # 生成都对应id的数据文件
        # self.source_data = MF_layer2_class.Layer2(layer_frame["speed"], layer_frame["time"], self.id)
        self.pre_data = random_generate(16)
        # 定义一个函数，对类中的变量进行赋值
        # for key, value in fsinfo.items():
        #     self.frequency.append(value)
        #     self.slot.append(key)
        # 初始化三类突发数据
        self.acq_generate(500)
        self.csc_generate()
        self.sync_generate()
        self.is_acq = False
        self.is_sync = False
        self.is_csc = False
        self.frq_num = 4 * random.randint(1, 15)

    def csc_generate(self):
        plugin_data = random_generate(64)
        self.csc_info = self.pre_csc + self.mac + plugin_data

    def acq_generate(self, frequency_num):
        frequency = "%016d" % int(bin(frequency_num)[2:])
        self.acq = self.pre_acp + frequency

    def sync_generate(self):
        plugin_data = random_generate(128)
        self.sync = self.pre_sync + plugin_data

    def module_data(self):
        # 计算时隙数
        slot_num = len(self.slot)
        # 计算每个时隙的符号数
        slot_data_num = len(self.source_data.data) // slot_num
        # 取出每个时隙的数据
        slot_datas = [self.source_data.data[i: i + slot_data_num] for i in
                      range(0, len(self.source_data.data), slot_data_num)]
        # 对时隙中的数据按照调制方式以及频点进行跳频调制
        # 每个时隙传输的比特数是一样的
        for i in range(slot_num):
            slot_data = slot_data[i]
            slot_info = self.slot[i]
            frequency_info = self.frequency[i]
            # 进行数据调制

        # print(slot_datas)

    # 定义子站的发送模块
    def send_info(self, type):
        if type == "CSC":
            print(self.csc_info)
        elif type == "ACQ":
            print(self.acq)
        elif type == "SYNC":
            print(self.sync)
        else:
            print("error type")


# dict1 = {"12": "1", "22": "3"}
# layer_frame = {"speed": 128, "time": 1}
# substation = Substation(dict1, layer_frame)
#
# print(substation.mac)
# print(substation.csc_info)
# print(substation.sync)
# print(substation.acq)
# substation.module_data()
# print(substation.source_data.data)
# print(substation.frequency)
# print(substation.slot)
