import MF_layer2_class
import numpy as np
from matplotlib import pyplot as plt
from scipy.fftpack import fft, ifft


# 用2FSK调制NRZ信号，NRZ信号由layer2产生，每个符号的采样点个数
class Module(object):
    def __init__(self, layer2, sample=100):
        self.layer2 = layer2
        self.sample = sample
        self.x_axis = []
        self.y_axis = []
        # self.MFSK()

    def MFSK(self, f0, f1):
        # f0 = 256
        # f1 = 512
        i = 0
        # 求链路层数据总的采样点个数
        samples = len(self.layer2.data) * self.sample

        # 采样的时刻为
        self.x_axis = np.linspace(0, self.layer2.time, samples)  # 注意采样点和时间为对应关系。

        while i < samples:
            re_i = i // self.sample
            if self.layer2.data[re_i] == 1:
                self.y_axis.append(np.cos(2 * f0 * np.pi * self.x_axis[i]))
            else:
                self.y_axis.append(np.cos(2 * f1 * np.pi * self.x_axis[i]))
            i += 1
            # y = np.cos(x)

    def QPSK(self, f):
        # 将输入原始信号进行串并转换得倒I路和Q路的信号
        data_length = len(self.layer2.data)
        I = []
        Q = []
        for i in range(data_length):
            if i % 2 == 0:
                I.append(self.layer2.data[i])
            else:
                Q.append(self.layer2.data[i])
        # print(I)
        # print(Q)
        samples = len(I) * self.sample
        self.x_axis = np.linspace(0, self.layer2.time, samples)  # 注意采样点和时间为对应关系。
        i = 0
        while i < samples:
            index = i // self.sample
            I_a = 0
            Q_a = 0
            if I[index] == 0 and Q[index] == 0:
                I_a = 1
                Q_a = 1
            elif I[index] == 0 and Q[index] == 1:
                I_a = -1
                Q_a = 1
            elif I[index] == 1 and Q[index] == 0:
                I_a = -1
                Q_a = -1
            elif I[index] == 1 and Q[index] == 1:
                I_a = 1
                Q_a = -1
            y_value = I_a * np.cos(2 * np.pi * f * self.x_axis[i]) + Q_a * np.sin(2 * np.pi * f * self.x_axis[i])
            self.y_axis.append(y_value)
            i += 1

    # 定义调制后的信号的快速傅里叶变换
        def fft_function(self, x_data, y_data):
            fy = fft(y_data)
            fy_real = fy.real
            fy_imag = fy.imag
            fy_abs = abs(fy)
            fy1 = fy_abs / len(x_data)
            fy2 = fy1[range(int(len(x_data) / 2))]
            xf = np.arange(len(y_data))
            xf1 = xf
            xf2 = xf[range(int(len(x_data) / 2))]
            plt.subplot(221)
            plt.plot(x_data[0:2000], y_data[0:2000])
            plt.title("original wave")
            plt.subplot(222)
            plt.plot(xf, fy_abs, 'r')
            plt.title("FFT of Mixed wave(two sides)")
            plt.subplot(223)
            plt.plot(xf1, fy1, 'g')
            plt.title("FFT of Mixed wave(normalization)")
            plt.subplot(224)
            plt.plot(xf2, fy2, 'b')
            plt.title("FFT of Mixed wave")
            plt.show()


# layer2 = MF_layer2_class.Layer2(speed=128, time=1)
#
# print(layer2.data)
#
# module = Module(layer2, 256)
# module.MFSK(256, 512)
# module.QPSK(256)
# module.fft_function(module.x_axis, module.y_axis)

# module.MFSK(200, 400)

# plt.plot(module.x_axis, module.y_axis)
# plt.show()
