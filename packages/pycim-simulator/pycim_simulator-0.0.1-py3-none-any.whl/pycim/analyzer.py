from matplotlib import pyplot as plt
import numpy as np
from pycim.simulation import setup
from functools import singledispatch 
import scipy 
from scipy.integrate import solve_ivp
# 计算 Ising能
def Ising(J, sign_value):
    col,row = J.shape
    e = 0
    for c in range(col):
        for r in range(row):
            e += - 0.5*J[c][r]*sign_value[c]*sign_value[r]
    return e
# 分叉时间点 
# def findfenchatime(sol,x):
#     for ti in range(0,len(x)):
#         if(abs(sol[0][ti]) > abs((0.1*sol[0][-1]))):
#             return x[ti]
  
#倒序搜索，目的是找到稳态时达到Max-cut_value的时间点   (discrete 模型)
def findSteadyTime(c,setup):

    x = np.linspace(0,setup.round_number - 1,setup.round_number)
    sign_value = np.sign(c[:,:setup.round_number - 1])
    cut_value = -0.5 * Ising(setup.couple_matrix, sign_value) - 0.25 * np.sum(setup.couple_matrix)
    for ti in range(len(cut_value)-1,-1,-1):
        if(cut_value[ti] < max(cut_value)):
            return x[ti+1]
# 返回最小Ising能    (discrete 模型)  
@singledispatch   
def getMinEnergy(sol_info: np.ndarray,setup):

    sign_value = np.sign(sol_info[:,:setup.round_number - 1])
    ising_energy = Ising(setup.couple_matrix , sign_value)
    mim_IsingEnergy = min(ising_energy)
    return mim_IsingEnergy
# 返回最小Ising能   (c-number 模型)  
@getMinEnergy.register 
def _(sol_info: scipy.integrate._ivp.ivp.OdeResult,setup):
    c = sol_info.y
    sign_value = np.sign(c[:,:setup.round_number - 1])
    ising_energy = Ising(setup.couple_matrix , sign_value)
    mim_IsingEnergy = min(ising_energy)
    return mim_IsingEnergy
# 首次找到最小Ising能的时间 (discrete 模型)
@singledispatch 
def getMinEnergyTime(sol_info: np.ndarray,setup):
    
    sign_value = np.sign(sol_info[:,:setup.round_number - 1])
    ising_energy = Ising(setup.couple_matrix , sign_value)
    mim_IsingEnergy_time = np.argmin(ising_energy)
    return mim_IsingEnergy_time
# 首次找到最小Ising能的时间  (c-number 模型) 
@getMinEnergyTime.register 
def _(sol_info: scipy.integrate._ivp.ivp.OdeResult,setup):
    c = sol_info.y
    x = sol_info.t
    sign_value = np.sign(c[:,:setup.round_number - 1])
    ising_energy = Ising(setup.couple_matrix , sign_value)
    mim_IsingEnergy_time = np.argmin(ising_energy)
    return x[mim_IsingEnergy_time]
# 寻找饱和时间点 等于逐渐泵浦的 增益下降时间点和分叉时间点    (discrete 模型)  ### 注意：此方法在逐渐泵浦设置下才可用，其他方案可能得到错误的值  
@singledispatch   
def findSaturationTime(Gain: np.ndarray,setup):
    Gain = Gain[0]
    x = np.linspace(0,setup.round_number - 1,setup.round_number)
    for ti in range(1,len(x)-1):
        if(Gain[ti] - Gain[ti-1] < 0 ):
            return int(x[ti])
# 寻找分叉时间点 在此模型下，认为饱和和分叉时间点是一样的    (c-number 模型)   ### 注意：此方法在逐渐泵浦设置下才可用，其他方案可能得到错误的值    
@findSaturationTime.register 
def _(sol_info: scipy.integrate._ivp.ivp.OdeResult,setup):
    sol = sol_info.y
    x = sol_info.t
    for ti in range(0,len(x)):
        if(abs(sol[0][ti]) > abs((0.1*sol[0][-1]))):
            return x[ti]
        
# 饱和时的OPO振幅    (discrete 模型)
def getSaturationAmplitude(Gain,sol_info,setup):

    SaturationTime = findSaturationTime(Gain,setup)
    SaturationAmplitude = abs(sol_info[0][int(SaturationTime)])
    return SaturationAmplitude
# 饱和时的泵浦功率   (discrete 模型)
def getSaturationPower(Gain,setup):

    SaturationTime = findSaturationTime(Gain,setup)
    SaturationPower = setup.pump_schedule[int(SaturationTime)]
    return SaturationPower
# 画OPO同相分量的演化图  (discrete 模型)
@singledispatch 
def inPhase_graph(sol_info: np.ndarray,setup):

    N = len(sol_info[0:])
    round_number = setup.round_number
    t = np.linspace(0,round_number - 1,round_number)
    for i in range(N):
        plt.plot(t,sol_info[i,:],label=f"{i+1}")
    # plt.legend(loc="upper left",ncol=2)
    plt.xlabel('round number')
    plt.ylabel('in-phase amplitude')
    plt.show()
# 画OPO同相分量的演化图  (c-number 模型)
@inPhase_graph.register 
def _(sol_info: scipy.integrate._ivp.ivp.OdeResult,setup):

    sol = sol_info.y
    x = sol_info.t
    a_sat = abs(sol[:,-1])#饱和时的振幅,用作归一化
    N = len(setup.couple_matrix[0])
    for i in range(0,N):
        plt.plot(x, sol[i,:]/a_sat[i],label=f"{i+1}")
    # plt.legend(loc="upper left",ncol=2)
    plt.xlabel('round  number')
    plt.ylabel('in-phase amplitude')
    plt.show()
# 画Ising能的演化图  (discrete 模型)
@singledispatch 
def energy_graph(sol_info: np.ndarray,setup):

    t = np.linspace(0,setup.round_number - 1,setup.round_number)
    x = t[:-1]
    sign_value = np.sign(sol_info[:,:setup.round_number - 1])
    ising_energy = Ising(setup.couple_matrix , sign_value)
    plt.plot(x,ising_energy)
    plt.xlabel('round number')
    plt.ylabel('Ising energy')
    plt.show()

# 画Ising能的演化图  (c-number 模型)
@energy_graph.register
def _(sol_info: scipy.integrate._ivp.ivp.OdeResult,setup):
    
    x = sol_info.t
    c = sol_info.y
    sign_value = np.sign(c)
    ising_energy = Ising(setup.couple_matrix , sign_value)
    plt.plot(x,ising_energy)
    plt.xlabel('round number')
    plt.ylabel('Ising energy')
    plt.show()
    
# 画增益的演化图   (discrete 模型)
def gain_graph(gain,setup):
    sqrt_G_I = gain
    t = np.linspace(0,setup.round_number - 1,setup.round_number)
    plt.plot( t[:-1] , 10*np.log10((sqrt_G_I[0][:-1]**2)) )
    plt.xlabel('round number')
    plt.ylabel('gain(dB)')
    plt.show()
    return

