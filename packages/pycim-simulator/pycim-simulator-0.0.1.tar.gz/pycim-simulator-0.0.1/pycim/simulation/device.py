import numpy as np

from pycim.utils import const

class device:
    def __init__(self):
        ##### discrete(行波)模型中需要的参数
        # 光速 m/s
        self.c  = 2.99792458e8  
        #腔长度 noraml: m
        self.L_cavity = 100 
        # Set the loss of the cavity, normal : dB
        self.loss = 10**(-11/10)
        # Set the gain coefficient of the PPLN crystals, normal: W^(-1/2)
        self.kappa = 130 * self.c 
        # Set the length of PPLN crystals, normal : m
        self.L_ppln = 0.05 
        # 往返时间
        self.T_rt = self.L_cavity / self.c
        # PPLN中行进时间
        self.tao = self.L_ppln / self.c

        ##### c-number模型中需要的参数
        #信号光 光子衰减率
        self.r_s = 1
        #泵浦光 光子衰减率
        self.r_p = 10264
        # PPLN晶体增益系数
        self.k = 130 
        # 阈值泵浦振幅
        self.F_th = (self.r_s*np.sqrt(self.r_p))/(4*self.k)
        self.As = np.sqrt(self.r_s*self.r_p/(2*self.k**2))
        self.g2 = 1/self.As

        ##### meanFiled模型中需要的参数
        # 泵浦光波长 780nm
        self.lambda_in = 780e-9
        # 泵浦光频率
        self.w1 = const.c / self.lambda_in
        # 耦合波方程项的系数
        self.eps = 130  # 等价于κ  
        # 折射率    0.7179
        self.n = self.w1*2*const.deff/(self.eps * const.c)
        # 增益系数
        self.G0 = np.e**(2 * self.eps * self.L_ppln * np.sqrt(0.03796) ) ###自定义的  
        # 无耦合阈值功率
        self.b0 = np.log(self.G0)/(2 * self.eps * self.L_ppln)  
        # 饱和参数
        self.beta = (self.G0-1-np.log(self.G0))/(4*(self.b0**2)*np.log(self.G0)) 
