import os
import random
import time
from matplotlib import pyplot as plt
from scipy.fftpack import fft, ifft
import numpy as np

# 定义CSC比特流，在一个调度会话中，子站的前导序一致，对于恶意子站来说，
# 发送多个接入干扰信号，所有时隙发送或选择发送，接入突发序列一致或不一
# 致，共四种情况。

# 一个crc接入请求共16bytes ，128bit数据其中，从4~9byte为mac地址
# 定义恶意子站的mac地址，对应I和Q路的比特信息
m_mac = 2 * np.random.randint(0, 2, (2, 24)) - 1
print(m_mac)

# 设载频为128hz 采样频率1024hz FFT变换区间N值为2048 取0~3s之间的数据 共3072个采样点
f = 128
N = 256
# 调制过程
x = np.linspace(0, 3, N)
for i in range(N):
    index = i // ((N // 24)+1)
    y = m_mac[0][index] * np.cos(2*np.pi*f*x) + m_mac[1][index] * np.sin(2*np.pi*f*x)
plt.subplot(421)
x_signal = np.arange(24)
plt.plot(x_signal, m_mac[0], drawstyle='steps-post')
plt.subplot(423)
plt.plot(x_signal, m_mac[1], drawstyle='steps-post')
fy = fft(y)
fy_abs = abs(fy)
fy1 = fy_abs / len(x)
xf = np.arange(len(y))
plt.subplot(425)
plt.plot(x, y)
plt.subplot(427)
plt.plot(xf, fy1)
# s_mac = 2 * np.random.randint(0, 2, (2, 24)) - 1
# print(s_mac)
# for i in range(N):
#     index = i // ((N // 24)+1)
#     y1 = s_mac[0][index] * np.cos(2*np.pi*f*x) + s_mac[1][index] * np.sin(2*np.pi*f*x)


# 解调过程(相干解调)
for i in range(N):
    i_demodule = y * np.cos(2*np.pi*f*x)
    q_demodule = y * np.sin(2*np.pi*f*x)
plt.subplot(422)
plt.plot(x, i_demodule)
plt.subplot(424)
plt.plot(x, q_demodule)

plt.show()
