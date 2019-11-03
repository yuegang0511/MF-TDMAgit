import numpy as np
import random

# 先定义一个10 * 9 的0 矩阵，每加入一个子站，进行二维装箱，其中每个子站需要连续分配 两 个时隙，每个子站都有一个总时隙数，范围为1-9之间
fs_info = np.zeros((10, 9), dtype=int)
print(fs_info)
rows, cols = fs_info.shape
# print(rows, cols)

slot_num = random.randint(1, 9)
# print(slot_num)

# 计算需要分配的载频数
frq_num = (slot_num // 2)
print(frq_num)


# 每个子站定义一个唯一标识id，用于更新箱中的数据，采用first fit 方法，从左上角进行装箱
def allcate_fs(id, frq_num):
    row = 0
    col = 0
    for k in range(frq_num):
        while row < rows:
            while col < cols:
                if col + 1 == 9:
                    col = 0
                    if fs_info[row][col] == 0 and fs_info[row][col+1] == 0:
                        fs_info[row][col] = id
                        fs_info[row][col + 1] = id
                        col += 2
                        break
                elif fs_info[row][col] == 0 and fs_info[row][col+1] == 0:
                    fs_info[row][col] = id
                    fs_info[row][col+1] = id
                    col += 2
                    break
                else:
                    col += 1
            row += 1
            break


allcate_fs(1, frq_num)
slot_num = random.randint(1, 9)
frq_num = (slot_num // 2)
allcate_fs(2, frq_num)
slot_num = random.randint(1, 9)
frq_num = (slot_num // 2)
allcate_fs(3, frq_num)
slot_num = random.randint(1, 9)
frq_num = (slot_num // 2)
allcate_fs(4, frq_num)
print(fs_info)