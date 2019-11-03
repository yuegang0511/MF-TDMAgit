import time


class Clock(object):
    # slot 为时隙时长，单位为ms ，slot_num 为帧中时隙的个数 ，默认为64
    def __init__(self, slot=4, slot_num=64):
        self.slot = slot
        self.slot_num = slot_num
        self.slot_count = 0
        self.message = ""
        # self.set_time()

    def set_time(self):
        ticks = time.time()
        m_sec = int(ticks * 10000)
        if m_sec % self.slot == 0:
            # 当为帧时长的整数倍时，主站下发基站分配信息
            # print("this is mainstation-TBTP time")
            # 当为时隙长时，第一个时隙为子站的申请时隙，第二个时隙为子站的粗同步时隙，第三个时隙为系统不时隙，其余时隙为用户业务时隙
            self.slot_count += 1
            if self.slot_count % self.slot_num == 0:
                # print("1")
                # print("this is mainstation-TBTP time")
                self.message = "INIT"
                return self.message
            elif self.slot_count % self.slot_num == 1:
                # print("2")
                self.message = "ACQ"
                return self.message
            elif self.slot_count % self.slot_num == 2:
                # print("3")
                self.message = "SYNC"
                return self.message
            else:
                self.message = self.slot_count % self.slot_num
                return self.message



