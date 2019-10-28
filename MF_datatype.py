class DataType(object):
    def __init__(self,datatype):
        self.data_type = datatype
        self.data = []
        self.generate_data(self.data_type)

    # 定义各突发的数据格式，同时返回二进制比特流
    def generate_data(self,data_type):
        data = []
        if data_type == "0":
            # TODO 定义类型为0的数据格式
            data = []
        elif data_type == "1":
            # TODO 定义类型为0的数据格式
            data = []
        elif data_type == "2":
            # TODO 定义类型为0的数据格式
            data = []
        elif data_type == "3":
            # TODO 定义类型为0的数据格式
            data = []
        elif data_type == "4":
            # TODO 定义类型为0的数据格式
            data = []
        elif data_type == "5":
            # TODO 定义类型为0的数据格式
            data = []
        self.data = data
