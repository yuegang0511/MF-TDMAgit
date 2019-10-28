# 定义载波频段
BAND_TYPE = "C"

# 定义载频的带宽，单位是hz
BAND_WIDTH = 0 # 设置初始带宽，默认为0
if BAND_TYPE == "C":
    BAND_WIDTH = 2 * 1000 * 1000 * 1000
else:
    BAND_WIDTH = 3 * 1000 * 1000 * 1000

# 定义载频个数
FREQUENCY_NUM = 8

# 定义帧时长，时间为s
FLAME_TIME = 0.128

# 定义帧中包含的时隙个数
SLOT_NUM = 128

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

# 定义每个时隙内原始数据量
Data_source = SLOT_TIME * DATA_SPEED

# 计算每个原始数据最大采样数
Sample_number = Data_frequency / Data_source
