import MF_substation_class
import random
import numpy as np
import matplotlib.pyplot as plt


class Mainstation(object):
    # 传入一个子站个数ss_num，载频个数frq_num，时隙个数slot_num，根据生成子站计划，依次传入各个子站当中
    # 计算每个载频上时域的信号
    # 总的频域信息
    def __init__(self, ss_num, frq_num, slot_num):
        self.ss_num = ss_num
        self.frq_num = frq_num
        self.slot_num = slot_num
        self.substations = []
        self.fs_infos = []  # 格式为{频率：时隙} 键值对
        # 调用分配函数
        self.allocate_fs()
        for i in range(self.ss_num):
            layer_frame = {"speed": 128, "time": 1}
            substation = MF_substation_class.Substation(self.fs_infos[i],layer_frame)
            self.substations.append(substation)

    # 定义一个分配子站和载频函数，一般情况下，子站的个数 比 跳频 的个数要多
    def allocate_fs(self):
        if self.ss_num <= self.frq_num:
            # 每一个载频，每一个时隙都可分配一个子站，每一个时隙上，一个子站只能占用一个载频资源
            frequency_range = self.get_list(self.slot_num, self.frq_num)
            for i in range(self.ss_num):
                fs_info = {}
                for j in range(self.slot_num):
                    # 从跳频点中随机找一个频点
                    index = random.randint(0, len(frequency_range[j])-1)
                    frq_info = frequency_range[j][index]
                    frequency_range[j].pop(index)
                    fs_info.update({j: frq_info})
                self.fs_infos.append(fs_info)
        else:
            # 从子站中随机找到 frq_num 个，在每一个时隙当中分配一个载频
            frequency_range = self.get_list(self.slot_num, self.ss_num)
            for i in range(self.ss_num):
                fs_info = {}
                for j in range(self.slot_num):
                    index = random.randint(0, len(frequency_range[j])-1)
                    frq_info = frequency_range[j][index]
                    frequency_range[j].pop(index)
                    if frq_info >= self.frq_num:
                        # -1表示该时隙下，第i个子站没有分配对应的频点信息
                        frq_info = -1
                    fs_info.update({j: frq_info})
                self.fs_infos.append(fs_info)
        # print(self.fs_infos)

    def get_list(self, slot, frequency):
        n = []
        for i in range(slot):
            fre = []
            for j in range(frequency):
                fre.append(j)
            n.append(fre)
        return n

    # 定义一个各子站在一帧内的时域函数，则为MF-TDMA时域帧信号
    def add_signal(self):
        for i in range(len(self.substations)):
            return

    # 定时生成一个广播信号数据根据数据类型
    def broadcast(self):
        # 周期性获取子站的申请信息
        print("get substation csc burst")
        # 生成广播数据，分配子站的载频和时隙
        print("get broadcast info")

    # 定义前向链路的回执
    def reply_burst(self,burst):
        # burst的类型，对应返回的数据
        print("burst type and reply")

    # 定义一个画图函数，能够图示化每个用户的分配信息
    def draw_allocate(self):
        # 图中线的数量为用户个数，横坐标为时隙，纵坐标为频率
        # plt.figure(figsize=(self.slot_num, self.frq_num))
        plt.figure()
        # fig, ax = plt.subplots(self.ss_num, 1)
        for i in range(self.ss_num):
            # ax[i].set_title("substation%d f-s allocation" % i)
            # ax[i].set_xlabel("slot")
            # ax[i].set_ylabel("frequency")
            x = self.substations[i].slot
            y = self.substations[i].frequency
            plt.scatter(x, y, s=[2000] * len(x), marker="s", label="ss %d" % i)
            for a, b in zip(x,y):
                plt.text(a, b, "UE%d" % i, ha='center', va='bottom', fontsize=10)
            # plt.plot(x, y)
            # plt.subplot(self.ss_num, 1, i)
            # ax[i].scatter(x, y, s=[50] * len(x), marker="o")
            # ax[i].plot(x, y, label="ss %d" % i)
            # ax[i].legend(loc="best")
        # plt.legend(loc="best")
        plt.xlabel("slot")
        plt.ylabel("frequency")
        plt.title("substation f-s allocation")
        plt.show()


# 定义一个fft变换，展示信号总的时域和频域的信息（这个函数规程成一个，为不同的类进行调用）

mainstation = Mainstation(5, 5, 10)
mainstation.draw_allocate()
