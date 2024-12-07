from matplotlib import pyplot as plt
import numpy as np
from pycim.utils.getIsingEnergy import Ising
from pycim.simulation import setup
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
from functools import singledispatch 
import scipy 
from scipy.integrate import solve_ivp
# 首次找到最优解的时间     (discrete 模型)
@singledispatch 
def getSolutionTime(sol_info: np.ndarray,setup):

    sign_value = np.sign(sol_info[:,:setup.round_number - 1])
    cut_value = -0.5 * Ising(setup.couple_matrix, sign_value) - 0.25 * np.sum(setup.couple_matrix)
    find_max_time = np.argmax(cut_value)
    return find_max_time
# 首次找到最优解的时间     (c-number 模型)
@getSolutionTime.register 
def _(sol_info: scipy.integrate._ivp.ivp.OdeResult,setup):
    c = sol_info.y
    x = sol_info.t
    sign_value = np.sign(c[:,:setup.round_number - 1])
    cut_value = -0.5 * Ising(setup.couple_matrix, sign_value) - 0.25 * np.sum(setup.couple_matrix)
    find_max_time = np.argmax(cut_value)
    return x[find_max_time]
# 最优解的分类配置    (discrete 模型)
@singledispatch  
def getSolution(sol_info: np.ndarray,setup):
    
    sign_value = np.sign(sol_info[:,:setup.round_number - 1])
    cut_value = -0.5 * Ising(setup.couple_matrix, sign_value) - 0.25 * np.sum(setup.couple_matrix)
    find_max_time = np.argmax(cut_value)
    opt_sol = sign_value[:,find_max_time]
    return opt_sol
# 最优解的分类配置     (c-number 模型)  ##注意：c-number模型得到的分类配置包括同相分量和正交分量。
@getSolution.register 
def _(sol_info: scipy.integrate._ivp.ivp.OdeResult,setup):
    c = sol_info.y
    x = sol_info.t
    sign_value = np.sign(c)
    cut_value = -0.5 * Ising(setup.couple_matrix, sign_value) - 0.25 * np.sum(setup.couple_matrix)
    find_max_time = np.argmax(cut_value)
    opt_sol = sign_value[:,find_max_time]
    return opt_sol
# 模拟求解到的max_cut与based_cut的精度      (discrete 模型)
@singledispatch   
def getAccuracy(sol_info: np.ndarray,setup,based_cut):

    sign_value = np.sign(sol_info[:,:setup.round_number - 1])
    cut_value = -0.5 * Ising(setup.couple_matrix, sign_value) - 0.25 * np.sum(setup.couple_matrix)
    max_cut = max(cut_value)
    accuracy = max_cut / based_cut
    return accuracy
# 模拟求解到的max_cut与based_cut的精度     (c-number 模型)
@getAccuracy.register
def _(sol_info: scipy.integrate._ivp.ivp.OdeResult,setup,based_cut):
    c = sol_info.y
    x = sol_info.t
    sign_value = np.sign(c[:,:setup.round_number - 1])
    cut_value = -0.5 * Ising(setup.couple_matrix, sign_value) - 0.25 * np.sum(setup.couple_matrix)
    max_cut = max(cut_value)
    accuracy = max_cut / based_cut
    return accuracy
# 最优解的最大割值      (discrete 模型)
@singledispatch   
def getCutValue(sol_info: np.ndarray,setup):
    
    sign_value = np.sign(sol_info[:,:setup.round_number - 1])
    
    cut_value = -0.5 * Ising(setup.couple_matrix, sign_value) - 0.25 * np.sum(setup.couple_matrix)
    max_cut = max(cut_value)
    return max_cut
# 最优解的最大割值     (c-number 模型)
@getCutValue.register
def _(sol_info: scipy.integrate._ivp.ivp.OdeResult,setup):
    c = sol_info.y
    x = sol_info.t
    sign_value = np.sign(c[:,:setup.round_number - 1])
    cut_value = -0.5 * Ising(setup.couple_matrix, sign_value) - 0.25 * np.sum(setup.couple_matrix)
    max_cut = max(cut_value)
    return max_cut
# 画cut_value值的演化图       (discrete 模型)
@singledispatch  
def cutvalue_graph(sol_info: np.ndarray,setup):

    t = np.linspace(0,setup.round_number - 1,setup.round_number)
    x = t[:-1]
    sign_value = np.sign(sol_info[:,:setup.round_number - 1])
    ising_energy = Ising(setup.couple_matrix , sign_value)
    cut_value = -0.5 * Ising(setup.couple_matrix, sign_value) - 0.25 * np.sum(setup.couple_matrix)
    y1 = cut_value
    y2 = ising_energy
    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust(right=0.9)
    par1 = host.twinx()
    offset = 100
    par1.axis["right"].toggle(all=True)
    host.set_xlabel("round number")
    host.set_ylabel("cut value")
    par1.set_ylabel("ising energ")
    p1 = host.plot(x, y1,color = 'blue')
    p2 = par1.plot(x, y2)
    # 颠倒y轴的方向
    par1.invert_yaxis()
    plt.show()
# 画cut_value值的演化图     (c-number 模型)
@cutvalue_graph.register
def _(sol_info: scipy.integrate._ivp.ivp.OdeResult,setup):
    c = sol_info.y
    x = sol_info.t
    sign_value = np.sign(c)
    ising_energy = Ising(setup.couple_matrix , sign_value)
    cut_value = -0.5 * Ising(setup.couple_matrix, sign_value) - 0.25 * np.sum(setup.couple_matrix)
    y1 = cut_value
    y2 = ising_energy
    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust(right=0.9)
    par1 = host.twinx()
    offset = 100
    par1.axis["right"].toggle(all=True)
    host.set_xlabel("round number")
    host.set_ylabel("cut value")
    par1.set_ylabel("ising energ")
    p1 = host.plot(x, y1,color = 'blue')
    p2 = par1.plot(x, y2)
    # 颠倒y轴的方向
    par1.invert_yaxis()
    plt.show()

# 成功率
def getSuccessRate(cut_list,based_cut):

    p = sum(i >= based_cut for i in cut_list)
    SuccessRate = p / len(cut_list)
    return SuccessRate
# 平均cut
def getAveCutValue(cut_list,step):

    ave_cut = sum(cut_list) / step
    return ave_cut
# # 稳定找到最优解的时间
# def steadSolutionTime(c,setup):

#     sign_value = np.sign(c[:,:setup.round_number - 1])
#     cut_value = -0.5 * Ising(setup.couple_matrix, sign_value) - 0.25 * np.sum(setup.couple_matrix)
#     MaxCutValueTime = GainDownTime + np.argmax(cut_value[GainDownTime:]) # 稳定找到最大割值的时间点
#     return MaxCutValueTime