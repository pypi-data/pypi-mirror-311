## 无耦合的阈值功率为0.03796W ，若泵浦从0开始增加，每轮增加0.05mW，需要760轮到达阈值，
## 一般分叉发生在760轮之前，因为有耦合之后，阈值功率会降低。
## 参考《Traveling-wave model of coherent Ising machine based on fiber loop with
## pulse-pumped phase-sensitive amplifier》

import numpy as np
from .. import device
from .. import setup
from .. import solver
from ...utils import const
from ...utils.file_J import read_J
from ...utils.getIsingEnergy import Ising

def RK45Discrete(device , setup):
    
    # 物理层输入
    L = device.L_ppln
    eta = device.loss
    kappa = device.kappa
    tao = device.tao
    t_end = 1 * tao # 在PSA中的行进时间

    # 应用层输入
    J = setup.couple_matrix
    N = J.shape[0]
    lunshu = setup.round_number
    intensity = setup.intensity
    init_Ep = setup.pump_schedule
    
    # 返回参数
    # gain = np.zeros((N,lunshu)) # 用来表示一轮的整个过程中获得的增益（算上损耗、耦合、噪声的影响）
    c = np.zeros((N,lunshu)) # 同相分量  ,Es 就是 c

    # 临时参数
    sign_value = np.zeros((N,lunshu-1)) # 同相分量的符号值
    sqrt_G_I = np.zeros((N,lunshu)) # 同相分量的增益
    N_I = np.zeros((N,lunshu)) # 同相分量的噪声
    noise_size = 2e-6  # 噪声大小的量级

    # 这里默认信号光相位为0/π
    N_I[:N,0] = noise_size * np.random.normal(0, 0.5, N) # 初始值来源于真空波动
    u = np.zeros(2*N,) # 0 ~ N-1 是 Es,后 N 个是 Ep
    c[0:N,0] = N_I[0:N,0]

    
    for k in range(0,lunshu-1): 
        u[0:N] = c[0:N,k] # Es 就是 c
        u[N:2*N] = init_Ep[k]
        sol_info = solver.RK45(u,t_end,kappa)
        if(sol_info.success == False):
            print("False!")
        Es = sol_info.y[0:N]
        
        ################## discrete模型中出现增益为0的情况后的debug处理####################
        for i in range(len(Es[:N,-1])):
            if(Es[i,-1] == 0):
                tmp_sign = np.sign(Es[i,0])
                Es[i,-1] = tmp_sign * noise_size * abs( np.random.normal(0, 0.5, 1) )
        ##################                                          ####################        
        
        sqrt_G_I[:N,k] = Es[:N,-1] / Es[:N,0]  # 这一轮同相分量经PSA获得的增益
        
        ################## discrete模型中出现增益为0的情况后的debug处理####################
        for i in range(len(sqrt_G_I[:N,k])):
            if(sqrt_G_I[i,k] == 0):
                sqrt_G_I[i,k] = sqrt_G_I[i,k-1]
        ##################                                          ####################        
        
        N_I[:N,k] = noise_size * np.random.normal(0, 1, N) * np.sqrt(0.25*(2-eta)*(sqrt_G_I[:N,k]**2))
        c[:N,k+1] = sqrt_G_I[:N,k] * np.sqrt(eta) * c[:N,k] \
            + sqrt_G_I[:N,k] * intensity[k] * np.dot(c[:,k],J) + N_I[0:N,k]
        # gain[:N,k] = c[:N,k+1] / c[:N,k]
    return c,sqrt_G_I

def RK4Discrete(device , setup):

    return 

def eulerDiscrete(device , setup):
    
    return 