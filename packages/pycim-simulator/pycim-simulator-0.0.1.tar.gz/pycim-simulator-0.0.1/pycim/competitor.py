import random
import numpy as np
from pycim.utils.getIsingEnergy import Ising
from matplotlib import pyplot as plt
from pycim.simulation import setup
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
from functools import singledispatch 
import scipy 
from scipy.integrate import solve_ivp
import networkx as nx
from scipy.sparse.linalg import eigsh
def e_J(J):
    return np.sqrt(np.sum(J * J))
def esing(J, s):
    col,row = J.shape
    e = 0
    for c in range(col):
        for r in range(row):
            e = e - 0.5*J[c][r]*s[0][c]*s[0][r]
    return e
#p(i) 是 a(t) , 经历step个步数，从0增加到1
def p(s:int):
    return s*0.005
def dsb(J):
    size = J.shape[0]
    det_t = 0.5  # 时间步长
    step = 200 # KPO的演化步数
    det = 1 # a0 正常数 不知道是什么意思
    ksi0 = 0.5 * np.sqrt(size - 1) / e_J(J)  # c0 基于随机矩阵理论定义的正常数
    # a0 c0 都可以是待优化的参数。
    x = np.zeros([1,size],dtype=np.float64)
    y = np.array(np.random.uniform(-0.1,0.1,size=(1,x.size)),dtype=np.float64)
    for i in range(step+1):
        y = y + det_t * (ksi0 * np.dot(np.sign(x),J) -(det - p(i)) * x)
        x = x + det * det_t * y
        y = np.where(np.abs(x) > 1, 0, y)
        x = np.where(np.abs(x) > 1, np.sign(x), x)
    return np.sign(x)

# 模拟退火算法
## 参考 《Massively Simulating Adiabatic Bifurcations with FPGA to Solve Combinatorial Optimization》
def SA(J):

    size = J.shape[0]
    T = 1000 # 初始温度
    r = 0.99 # 步长
    T_min = 0.01 # 最终温度
    s = np.ones([1,size],dtype=np.int32) # 初始状态全1，初始自旋全为1
    i=0
    while(T > T_min):
        select_num = random.randint(0,size-1) # 在 0 ~ size-1 之间随机选一个整数
        dE = 2 * s[0][select_num] * np.sum(J[select_num] * s[0]) # △E 翻转一个自旋导致的能量改变量
        if(np.exp( -(dE/T) ) > random.uniform( 0 , 1 )): # 根据温度加入噪声，来跳出局部最小值  Metropolis规则：以概率接受新状态
            #翻转s
            s[0][select_num] = -s[0][select_num]
        else:
            pass
        T = r * T
        i += 1
    cut_value = -0.5*esing(J, s)-0.25*np.sum(J)

    return cut_value

# 模拟分岔算法
## 参考《High-performance combinatorial optimization based on classical mechanics》
def SB(J,step):

    i=0
    max_cut_value_sb=0
    while(i<step):
        s = dsb(J)
        if( (-0.5*esing(J, s)-0.25*np.sum(J)) > max_cut_value_sb):
            max_cut_value_sb = -0.5*esing(J, s)-0.25*np.sum(J)
        i+=1
    # print("s:",s)#解的自旋构型是这个矩阵
    return max_cut_value_sb

# 多项式时间复杂度的固定贪婪算法
def SG(J):
    J = -J
    def weight_all(i,S):
        weight = 0
        for j in S:
            weight += J[i][j]
        return weight
    cut_value = float('-inf')
    N = len(J[0])
    V_ = np.linspace(0,N-1,N) # V`=V
    # 找到J中权重最大的边的
    max_weight = J[0][1]
    row=0
    col=1
    for r in range(0,N-1):
        for c in range(r+1,N):
            if(J[r][c] > max_weight):
                max_weight = J[r][c]
                row=r
                col=c
    cut_value = max_weight
    V_ = np.delete(V_,np.where(V_ == row))
    V_ = np.delete(V_,np.where(V_ == col))
    S1 = np.array([row])
    S2 = np.array([col])
    score = [float('-inf')]*N

    for j in range(1,N-1):

        for i in V_:
            i = int(i)
            score[i] = max(weight_all(i,S1),weight_all(i,S2))
        i_ = score.index(max(score))

        if(weight_all(i_,S1) > weight_all(i_,S2)):
            S2 = np.append(S2,i_)
        else:
            S1 = np.append(S1,i_)

        V_ = np.delete(V_,np.where(V_ == i_))
        score[i_] = float("-inf")
        cut_value = cut_value + max(weight_all(i_,S1),weight_all(i_,S2))

    return cut_value

# 能保证至少87.8%近似比的启发式算法
def GW_SDP(J, n_iter=10):
    G = nx.from_numpy_matrix(-J)
    # 构建邻接矩阵和对角矩阵
    A = nx.to_numpy_array(G)
    D = np.diag(A.sum(axis=1))
    J = - nx.to_numpy_array(G)
    # 构建拉普拉斯矩阵
    L = D - A

    # 进行n_iter轮迭代
    for i in range(n_iter):
        # 求解拉普拉斯矩阵的特征值和特征向量
        eigenvalues, eigenvectors = eigsh(L, k=2, which='LA')

        # 将特征向量按照元素大小分成两个切割集合
        labels = np.sign(eigenvectors[:, 1])

        # 更新拉普拉斯矩阵
        L = D - A + np.outer(labels, labels)

    # 返回最终的切割集合
    sign_value = labels
    cut_value = -0.5*Ising(J, sign_value)-0.25*np.sum(J)
    return cut_value
