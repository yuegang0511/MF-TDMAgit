import os
import random
import time
from matplotlib import pyplot as plt
from scipy.fftpack import fft, ifft
import numpy as np


x = 2 * np.random.randint(0, 2, (64, 64)) - 1
y = 2 * np.random.randint(0, 2, (64, 64)) - 1
s = x + 1j * y
t = np.fft.ifftn(s)

t, w = (np.empty((64, 64), dtype=complex) for i in range(2))

error_sum = 0.0
SNR = 10
Eb_No_lin = 10 ** (SNR/10)
No = 1/Eb_No_lin
scale = np.sqrt(No/2)

for i in range(64):
    n = np.fft.ifftn(np.random.normal(scale=scale, size=64)+1j*np.random.normal(scale=scale, size=64))
    t[i] = np.fft.ifftn(s[i])
    w[i] = np.fft.fftn(t[i] + n)
    z = np.sign(np.real(w[i])) + 1j * np.sign(np.imag(w[i]))
    err = np.where(z != s[i]) # 输出的是两个列表当中不一致的下标
    #print(z)
    #print(s[i])
    #print(err)
    error_sum += float(len(err[0]))

# print(error_sum)
BER = error_sum / (64*64)
print(BER)

# pt3 = plt.subplot(212)
plt.scatter(np.real(w), np.imag(w))

# pt1 = plt.subplot(211)
# pt1.bar(np.real(w).flatten(), np.abs(w).flatten())
plt.show()