# 定义载频的带宽，单位是hz
BAND_WIDTH = 2 * 1000 * 1000 * 1000

# 定义载频个数
FREQUENCY_NUM = 8

# 计算每个载频的带宽，单位是hz
FREQUENCY_WIDTH = BAND_WIDTH / FREQUENCY_NUM

# 定义帧时长，时间为s
FLAME_TIME = 0.128

# 定义帧中包含的时隙个数
SLOT_NUM = 128

# 计算每个时隙的时长，以及时隙每秒包含的数据量
SLOT_TIME = FLAME_TIME / SLOT_NUM
SLOT_COUNT = 1 / SLOT_TIME

# 计算时隙中包含的数据量 ,单位是bit
SLOT_DATA = BAND_WIDTH / SLOT_COUNT

# 在时隙之间进行跳频
# 因为 载频带宽 远大于 符号的传输速率，则认为载频之间近似正交

# 定义链路层原始数据传输速率，单位为bit
DATA_SPEED = 128

# 一般情况下，子站数量比跳频个数要多
