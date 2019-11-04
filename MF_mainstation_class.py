from MF_substation_class import *
import random
import numpy as np
import matplotlib.pyplot as plt


# 载频个数为1000 ， 载频宽度为2Mhz， 帧长为25.6ms 时隙个数为64 个 ，
# 时隙中前三个时隙为信令时隙，分别为csc acq sync，不传输子站数据
# 主站分配1000 * 61 向量填空问题，每个子站需连续分配不少于4个时隙
class Mainstation(object):
    # 传入一个子站个数ss_num，载频个数frq_num，时隙个数slot_num，根据生成子站计划，依次传入各个子站当中
    # 计算每个载频上时域的信号
    # 总的频域信息
    # 主站主要完成用户资源的计算TBTP，先满足子站申请，分配，同步，回复的过程
    def __init__(self, frq_num, slot_num):
        self.frq_num = frq_num
        self.slot_num = slot_num
        self.substations = []
        # self.ss_num = len(self.substations)
        self.fs_infos = np.zeros((self.frq_num, self.slot_num), dtype=int)  # 格式为{频率：时隙} 键值对
        # 调用分配函数
        # self.allocate_fs()
        # for i in range(self.ss_num):
        #     layer_frame = {"speed": 128, "time": 1}
        #     substation = Substation(self.fs_infos[i], layer_frame)
        #     self.substations.append(substation)

    # # 定义一个分配子站函数，给定为1000 * 61 矩阵，值为子站id
    # def allocate_fs2(self):
    #     # 当前子站个数
    #     ss_num = len(self.substations)
    #     # 已分配资源的子站个数
    #     ss_has_source = 0
    #     for i in range(ss_num):
    #         # 对于子站已经申请 ，并且已经粗同步的子站不进行分配
    #         if self.substations[i].is_acq and self.substations[i].is_csc:
    #             ss_has_source += 1
    #             continue
    #         else:
    #         # 对于创建了子站，还未申请资源，则对子站进行资源分配
    #             self.allocate_fs_new(self.substations[i])
    #
    # # 为新的子站进行资源分配
    # def allocate_fs_new(self, substation):
    #     id = substation.id
    #     # 对fs_info进行赋值操作，值为id，同时对该子站的频率和时隙信息进行赋值。 4 * 14 + 5 来进行二维装箱
    #     rows, cols = self.fs_infos.shape
    #     i = 0
    #     while i < rows:
    #         for j in range(64):
    #             if self.fs_infos[i][j] == 0 and j % 4 == 0:
    #                 self.fs_infos[i][j:j+3] = [id] * 4
    #             else:
    #                 i = i + 1

    # 定义一个分配子站和载频函数，一般情况下，子站的个数 比 跳频 的个数要多
    # 每个子站定义一个唯一标识id，用于更新箱中的数据，采用first fit 方法，从左上角进行装箱

    # 定义一个tbtp生成函数，遍历子站中的所有信息，重新更新fs_infos变量
    def tbtp_generate(self):
        self.fs_infos = np.zeros((self.frq_num, self.slot_num), dtype=int)
        for i in range(len(self.substations)):
            self.allocate_fs_new(self.substations[i])

    # 连续四个时隙分配给一个子站,传递一个substation变量，去子站的id和频率使用数，同时将对应的载频和时隙数纪录在子站信息中
    def allocate_fs_new(self, substation):
        row = 0
        col = 0
        for k in range(substation.frq_num):
            while row < self.frq_num:
                while col < self.slot_num:
                    if col + 1 == self.slot_num or col + 2 == self.slot_num or col + 3 == self.slot_num:
                        col = 0
                        if self.fs_infos[row][col] == 0 and self.fs_infos[row][col + 1] == 0:
                            self.fs_infos[row][col] = substation.id
                            substation.frequency.append(row)
                            substation.slot.append(col)
                            self.fs_infos[row][col + 1] = substation.id
                            substation.frequency.append(row)
                            substation.slot.append(col+1)
                            self.fs_infos[row][col + 2] = substation.id
                            substation.frequency.append(row)
                            substation.slot.append(col+2)
                            self.fs_infos[row][col + 3] = substation.id
                            substation.frequency.append(row)
                            substation.slot.append(col+3)
                            col += 4
                            break
                    elif self.fs_infos[row][col] == 0 and self.fs_infos[row][col + 1] == 0 and self.fs_infos[row][col + 2] == 0 and self.fs_infos[row][col + 3] == 0:
                        self.fs_infos[row][col] = substation.id
                        substation.frequency.append(row)
                        substation.slot.append(col)
                        self.fs_infos[row][col + 1] = substation.id
                        substation.frequency.append(row)
                        substation.slot.append(col+1)
                        self.fs_infos[row][col + 2] = substation.id
                        substation.frequency.append(row)
                        substation.slot.append(col+2)
                        self.fs_infos[row][col + 3] = substation.id
                        substation.frequency.append(row)
                        substation.slot.append(col+3)
                        col += 4
                        break
                    else:
                        col += 1
                row += 1
                break

    def allocate_fs(self):
        if self.ss_num <= self.frq_num:
            # 每一个载频，每一个时隙都可分配一个子站，每一个时隙上，一个子站只能占用一个载频资源
            frequency_range = self.get_list(self.slot_num, self.frq_num)
            for i in range(self.ss_num):
                fs_info = {}
                for j in range(self.slot_num):
                    # 从跳频点中随机找一个频点
                    index = random.randint(0, len(frequency_range[j]) - 1)
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
                    index = random.randint(0, len(frequency_range[j]) - 1)
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
    def reply_burst(self, burst):
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
            for a, b in zip(x, y):
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

    # 定义一个初始化TBTP的函数，TBTP函数为一个1000 * 64 的矩阵，初始矩阵值为0 ，当有子站申请时，矩阵值为子站的id

# 定义一个fft变换，展示信号总的时域和频域的信息（这个函数规程成一个，为不同的类进行调用）

# substaton = Substation()
# mainstation = Mainstation(1000, 61)
# print(mainstation.fs_infos)
#
# substation1 = Substation(1)
# mainstation.substations.append(substation1)
# mainstation.tbtp_generate()
# print(mainstation.fs_infos)
# print(substation1.frequency)
# print(substation1.slot)
# mainstation.allocate_fs_new()
# mainstation.draw_allocate()
