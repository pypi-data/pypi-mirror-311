##########这里定义一些用到的常量
import numpy as np
# 定义一些常量
global c 
global deff
global eps0
c = 2.99792458e8  # 光速 m/s
deff = 28e-12  # 二次非线性系数 单位m/V
eps0 = 8.854187817e-12  # 真空介电常数 F/m
h_bar = 1.05457266e-34  #约化普朗克常数 J·s

# 可变参数  这些参数如果是变量的话就可以删除掉
global n1
global n2
n1 = 2  # 折射率
n2 = 2  # 折射率

#定义系数矩阵
def matrix_J(N):
    J=np.ones((N,N))
    for i in range(0,N):
        J[i][i]=0   
    return J  