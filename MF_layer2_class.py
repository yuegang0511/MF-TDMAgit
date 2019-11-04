import os
import random
import time


# 定义的数据以文件格式进行存储，文件名为子站的id，时长为1s，文件格式txt文件，内容为0，1比特，每行根据传输速率定义为一个时隙传输的二进制内容
class Layer2(object):
    # 数据链路层的原始数据函数，定义传输速率speed 单位为k/s，默认128 传输时间 time 默认1s，slot_num为一帧的时隙个数
    # 定义生成数据函数，输出为二进制比特流
    # 补充协议相关数据，突发类型，6种
    # 返回一个数据列表
    def __init__(self, speed=128, time=1, id="test", slot_num=64):
        self.speed = speed
        self.time = time
        self.data = ""
        # self.source_data()
        self.filename = str(id)
        self.slot_num = slot_num
        self.write_source_data()

    def source_data(self):
        # 计算需要产生多少个原始二进制数据
        size = int(self.speed * self.time)
        # 计算每个二进制数据时间间隔
        betimes = 1 / self.speed
        i = 0
        self.data = ""
        while i < size:
            bit_data = random.randint(0, 100) % 2
            self.data = self.data + str(bit_data)
            i += 1
            # time.sleep(betimes)

    def write_source_data(self):
        i = 0
        # if os.path.exists(self.filename):
        file = open(self.filename, "w")
        while i < self.slot_num:
            self.source_data()
            file.write(self.data)
            file.write("\n")
            i += 1
        file.close()


# layer2 = Layer2()
# layer2.write_source_data()
# print(layer2.data)
