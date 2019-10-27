from MF_layer2_class import *
from MF_module_class import *
import numpy as np
from matplotlib import pyplot as plt
from scipy.fftpack import fft, ifft


class Substation(object):
    # 需要一个链路层数据源 layer_frame 字典形式（speed=128，time=1） 传递两个参数，一个为速率，一个为时长（时长的一个帧的时长）生成了一个帧长的数据
    # 需要一个调制方式
    # 需要频分复用过程中的载频和时隙信息，数据格式为字典格式，键为时隙信息，值为频率信息，以一个帧为例
    # 输出时域和频域的结果
    def __init__(self, fsinfo, layer_frame):
        self.frequency = []
        self.slot = []
        self.source_data = MF_layer2_class.Layer2(layer_frame["speed"],layer_frame["time"])
        # 定义一个函数，对类中的变量进行赋值
        for key, value in fsinfo.items():
            self.frequency.append(value)
            self.slot.append(key)

    def module_data(self):
        # 计算时隙数
        slot_num = len(self.slot)
        # 计算每个时隙的符号数
        slot_data_num = len(self.source_data.data) // slot_num
        # 取出每个时隙的数据
        slot_datas = [self.source_data.data[i: i+slot_data_num] for i in range(0, len(self.source_data.data), slot_data_num)]
        # 对时隙中的数据按照调制方式以及频点进行跳频调制
        # 每个时隙传输的比特数是一样的
        for i in range(slot_num):
            slot_data = slot_data[i]
            slot_info = self.slot[i]
            frequency_info = self.frequency[i]
            # 进行数据调制
            
        # print(slot_datas)


dict1 = {"12": "1", "22": "3"}
layer_frame = {"speed": 128, "time": 1}
substation = Substation(dict1, layer_frame)
# substation.module_data()
# print(substation.source_data.data)
# print(substation.frequency)
# print(substation.slot)
