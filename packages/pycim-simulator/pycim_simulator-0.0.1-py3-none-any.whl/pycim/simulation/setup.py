import numpy as np

# 首先定义一个类，要有__init__
class setup:
    
    def __init__(self):
        
        def pump_schedule(t):
            return np.sqrt( (1/760) * t )
        
        # Set the couple matrix
        # self.couple_matrix = - np.array([
        #         [0, 1, 0, 1, 1, 0, 0, 1, 1, 0],
        #         [1, 0, 1, 0, 0, 1, 1, 1, 0, 0],
        #         [0, 1, 0, 1, 1, 0, 0, 0, 1, 0],
        #         [1, 0, 1, 0, 0, 1, 1, 0 ,1, 0],
        #         [1, 0, 1, 0, 0, 1, 0, 1, 0, 1],
        #         [0, 1, 0, 1, 1, 0, 0, 0, 1, 1],
        #         [0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
        #         [1, 1, 0, 0, 1, 0, 0, 0, 1, 0],
        #         [1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
        #         [0, 0, 0, 0, 1, 1, 1, 0, 1, 0]])
        # 腔中OPO的数目
        self.N = 10
        # # Set the couple matrix
        self.couple_matrix = - np.zeros((self.N,self.N))
        # 往返轮数
        self.round_number = 1500
        # Set the coupling intensity
        self.intensity = 0.03 * np.ones(self.round_number,)
        # Set the pump of the CIM system, normal:W
        self.pump_schedule = np.sqrt( 5e-5 * np.linspace(1,self.round_number,self.round_number) )
        # 归一化的泵浦功率, 用于c-number 和 meanFiled模型中
        self.p = pump_schedule
        