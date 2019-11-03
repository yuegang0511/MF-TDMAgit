from MF_clock import *
from MF_mainstation_class import *
from MF_substation_class import *

# 定义载波频段
BAND_TYPE = "C"

# 定义载频的带宽，单位是hz
BAND_WIDTH = 0 # 设置初始带宽，默认为0
if BAND_TYPE == "C":
    BAND_WIDTH = 2 * 1000 * 1000 * 1000
else:
    BAND_WIDTH = 3 * 1000 * 1000 * 1000

# 定义载频个数
FREQUENCY_NUM = 1000

# 定义每个载频的频带宽度为
FREQUENCY_WIDTH = BAND_WIDTH / FREQUENCY_NUM

# 定义帧时长，时间为s 128ms 27ms
FLAME_TIME = 0.0256

# 定义帧中包含的时隙个数，时隙最大数为256 64个时隙则每个时隙0.4ms 0.0004s
SLOT_NUM = 64

# 定义链路层原始数据传输速率，单位为bit
DATA_SPEED = 128

# 计算每个载频的带宽，单位是hz
FREQUENCY_WIDTH = BAND_WIDTH / FREQUENCY_NUM

# 定义载频频点：
fn = []
for i in range(FREQUENCY_NUM):
    f = BAND_WIDTH * (2 * i + 1) / (2 * FREQUENCY_NUM)
    fn.append(f)
# print(fn)

# 计算每个时隙的时长，以及时隙每秒包含的数据量
SLOT_TIME = FLAME_TIME / SLOT_NUM

# 每个时隙内传输的最大数据量
Data_frequency = SLOT_TIME * FREQUENCY_WIDTH
# print(Data_frequency/8)  一个时隙最大可传输31250bypes字节 当时隙28ms时，6800bytes


# 定义每个时隙内原始数据量
Data_source = SLOT_TIME * DATA_SPEED

# 计算每个原始数据最大采样数
Sample_number = Data_frequency / Data_source


# 开始计算每个时刻主站和子站的功能
# 定义一个时钟实例用于同步
clock = Clock()
# 定义一个主站实例用于计算分配规则
mainstation = Mainstation(5, 5, 10)
mainstation.draw_allocate()
while True:
    # 定义子站变量，子站在对应的时间发送相关数据，子站为动态定义
    # substation = Substation()
    clock_count = clock.slot_count
    clock.set_time()
    if clock_count == clock.slot_count:
        continue
    else:
        print(clock.message)