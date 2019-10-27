import os
import random
import time


class Layer2(object):
    # 数据链路层的原始数据函数，定义传输速率speed 默认128 传输时间 time 默认1s
    # 定义生成数据函数，输出为二进制比特流
    # 补充协议相关数据，突发类型，6种
    # 返回一个数据列表
    def __init__(self,speed = 128, time = 1):
        self.speed = speed
        self.time = time
        self.data = []
        self.source_data()

    def source_data(self):
        # 计算需要产生多少个原始二进制数据
        size = self.speed * self.time
        # 计算每个二进制数据时间间隔
        betimes = 1 / self.speed
        i = 0
        while i < size :
            bit_data = random.randint(0, 100) % 2
            self.data.append(bit_data)
            i += 1
            # time.sleep(betimes)


# layer2 = Layer2()
# print(layer2.data)
