import random
from scipy.integrate import solve_ivp
import numpy as np
import sys
from .. import device
from .. import setup
from .. import solver
from ...utils import const
from ...utils.file_J import read_J
from ...utils.getIsingEnergy import Ising

def RK45meanField(phyInput , applInput):

    # 物理层输入
    # PPLN长度： m
    L_ppln = phyInput.L_ppln 
    # 泵浦光波长： m
    lambda_in = phyInput.lambda_in

    # 应用层输入
    intensity = applInput.intensity
    round_number = applInput.round_number
    J = applInput.couple_matrix

    N = J.shape[0]
    t_end = round_number

    sol_info = solver.RK45(t_end , phyInput , applInput)

    return sol_info