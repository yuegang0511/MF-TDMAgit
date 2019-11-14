# -*- coding:utf-8 -*-
import numpy as np
from math import pi
import matplotlib.pyplot as plt
import matplotlib
import scipy.signal as signal
import math
from scipy.fftpack import fft, ifft

# 码元数,横坐标为1000个点
size = 24
sampling_t = 0.01
t = np.arange(0, size, sampling_t)

# 随机生成信号序列
# 随机生成二进制数，一共10个bit，由size决定
a = 2 * np.random.randint(0, 2, (2, 24)) - 1
b = 2 * np.random.randint(0, 2, (2, 24)) - 1
# a[0]对应I路信号，a[1]对应Q路信号
# m为定义的长度为1000个0列表，类型为float
I = np.zeros(len(t), dtype=np.float32)
Q = np.zeros(len(t), dtype=np.float32)
# 循环给m赋值
for i in range(len(t)):
    I[i] = a[0][math.floor(t[i])]
    Q[i] = a[1][math.floor(t[i])]
fig = plt.figure()
ax1 = fig.add_subplot(4, 3, 1)
# 画出I路信号
zhfont1 = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')
ax1.set_title('I路信号', fontproperties=zhfont1, fontsize=15)
# 定义图的横纵坐标范围
plt.axis([0, size, -2, 2])
plt.plot(t, I, 'b')
# 画出Q路信号
ax2 = fig.add_subplot(4, 3, 4)
# 解决set_title中文乱码
zhfont1 = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')
ax2.set_title('Q路信号', fontproperties=zhfont1, fontsize=15)
# 定义图的横纵坐标范围
plt.axis([0, size, -2, 2])
plt.plot(t, Q, 'b')

# # 定义两个载频
# 定义载波频率为1024hz
fc1 = 2048
# fc2 = 10000
# # 定义采样频率，采样频率要大于信号带宽的两倍
fs = 50000
# # 100 为0.01相当于1个符号采样100个点
ts = np.arange(0, (100 * size) / fs, 1 / fs)
# # np.dot返回两个数组的点积，ts为一个数组，返回前一个数与后一个数组的积，为一个数组
coherent_carrier = np.cos(np.dot(2 * pi * fc1, ts))
coherent_carrier1 = np.sin(np.dot(2 * pi * fc1, ts))
# # 两个数组相乘，得到的也是一个数组，两个数组对应下标的乘积，同时两个数组的长度要一致
qpsk = I * coherent_carrier + Q * coherent_carrier1
#
# # BPSK调制信号波形
ax3 = fig.add_subplot(4, 3, 7)
ax3.set_title('QPSK调制信号', fontproperties=zhfont1, fontsize=15)
plt.axis([0, size, -2, 2])
plt.plot(t, qpsk, 'r')


#
#
# 定义加性高斯白噪声 y为原始信号，snr为信噪比
def awgn(y, snr):
    # 根据db信噪比计算信号与造成的功率比
    snr = 10 ** (snr / 10.0)
    # 原始信号的的归一化功率 值的平方除以抽样点的数量
    xpower = np.sum(y ** 2) / len(y)
    # 噪声的平均功率
    npower = xpower / snr
    # randn为标准正态分布 ，在与原始噪声相加，加性噪声
    return np.random.randn(len(y)) * np.sqrt(npower) + y


#
#
# # 加AWGN噪声
noise_qpsk = awgn(qpsk, 50)
#
# BPSK调制信号叠加噪声波形
ax3 = fig.add_subplot(4, 3, 10)
ax3.set_title('调制信号叠加噪声波形', fontproperties=zhfont1, fontsize=15)
plt.axis([0, size, -2, 2])
plt.plot(t, noise_qpsk, 'r')
#
# 带通buffer滤波器设计，通带为[1500，2500]
b, a = signal.butter(4, [1500 * 2 / fs, 2500 * 2 / fs], 'bandpass')
# # 低通滤波器设计，通带截止频率为2000Hz，截至频率计算方法，截止数值 * 2 / 抽样点数
bl, al = signal.butter(4, 1500 * 2 / fs, 'lowpass')
#
# # 通过带通滤波器滤除带外噪声
bandpass_out1 = signal.filtfilt(b, a, noise_qpsk)
#
# # 相干解调,乘以同频同相的相干载波
coherent_demodI = bandpass_out1 * coherent_carrier
coherent_demodQ = bandpass_out1 * coherent_carrier1

# 通过低通滤波器
lowpass_outI = signal.filtfilt(bl, al, coherent_demodI)
lowpass_outQ = signal.filtfilt(bl, al, coherent_demodQ)

bx1 = fig.add_subplot(4, 3, 8)
bx1.set_title('I路信号相干解调后的信号', fontproperties=zhfont1, fontsize=15)
plt.axis([0, size, -2, 2])
plt.plot(t, lowpass_outI, 'r')

bx2 = fig.add_subplot(4, 3, 11)
bx2.set_title('Q路信号相干解调后的信号', fontproperties=zhfont1, fontsize=15)
plt.axis([0, size, -2, 2])
plt.plot(t, lowpass_outQ, 'r')

# 抽样判决
# 抽样的数据为1000个，类型为float
detection_I = np.zeros(len(t), dtype=np.float32)
detection_Q = np.zeros(len(t), dtype=np.float32)
# 译码的数据为10个，类型为float
flagI = np.zeros(size, dtype=np.float32)
flagQ = np.zeros(size, dtype=np.float32)

# 循环从1000个数据中取值，如果100此求和，如果最终的结果大于50，则为1
for i in range(size):
    tempI = 0
    tempQ = 0
    for j in range(100):
        tempI = tempI + lowpass_outI[i * 100 + j]
        tempQ = tempQ + lowpass_outQ[i * 100 + j]

    flagI[i] = np.sign(tempI)
    flagQ[i] = np.sign(tempQ)
#
# 将抽样数据规整，100个值要求一致
for i in range(size):
    if flagI[i] == 1:
        for j in range(100):
            detection_I[i * 100 + j] = 1
    else:
        for j in range(100):
            detection_I[i * 100 + j] = -1
    if flagQ[i] == 1:
        for j in range(100):
            detection_Q[i * 100 + j] = 1
    else:
        for j in range(100):
            detection_Q[i * 100 + j] = -1


# 定义一个fft函数
def signal_fft(signal):
    fy = fft(signal)
    fy_real = fy.real
    fy_imag = fy.imag
    fy_abs = abs(fy)
    fy1 = fy_abs / len(signal)
    fy2 = fy1[range(int(len(signal) / 2))]
    xf = np.arange(len(signal))
    xf1 = xf
    xf2 = xf[range(int(len(signal) / 2))]
    return fy_abs
    # plt.subplot(311)
    # plt.plot(xf, fy_abs, 'r')
    # plt.title("FFT of Mixed wave(two sides)")
    # plt.subplot(312)
    # plt.plot(xf1, fy1, 'g')
    # plt.title("FFT of Mixed wave(normalization)")
    # plt.subplot(313)
    # plt.plot(xf2, fy2, 'b')
    # plt.title("FFT of Mixed wave")
    # plt.show()


originalI_fft = signal_fft(I)
originalQ_fft = signal_fft(Q)
module_fft = signal_fft(qpsk)
noise_fft = signal_fft(noise_qpsk)
x = np.arange(len(I))
fp1 = fig.add_subplot(4, 3, 3)
fp1.set_title('I路频谱', fontproperties=zhfont1, fontsize=15)
# plt.axis([0, len(I), 0, 2])
plt.plot(x[0:500], originalI_fft[0:500], 'r')
fp1 = fig.add_subplot(4, 3, 6)
fp1.set_title('Q路频谱', fontproperties=zhfont1, fontsize=15)
# plt.axis([0, len(I), 0, 2])
plt.plot(x[0:500], originalQ_fft[0:500], 'r')
fp1 = fig.add_subplot(4, 3, 9)
fp1.set_title('QPSK频谱', fontproperties=zhfont1, fontsize=15)
# plt.axis([0, len(I), 0, 2])
plt.plot(x[0:500], module_fft[0:500], 'r')
fp1 = fig.add_subplot(4, 3, 12)
fp1.set_title('加噪频谱', fontproperties=zhfont1, fontsize=15)
# plt.axis([0, len(I), 0, 2])
plt.plot(x[0:500], noise_fft[0:500], 'r')

bx2 = fig.add_subplot(4, 3, 2)
bx2.set_title('I路抽样判决后的信号', fontproperties=zhfont1, fontsize=15)
plt.axis([0, size, -2, 2])
plt.plot(t, detection_I, 'r')
bx2 = fig.add_subplot(4, 3, 5)
bx2.set_title('Q路抽样判决后的信号', fontproperties=zhfont1, fontsize=15)
plt.axis([0, size, -2, 2])
plt.plot(t, detection_Q, 'r')
plt.show()
