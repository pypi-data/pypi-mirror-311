# -*- coding: utf-8 -*-
"""
模块: utils

功能: 一些tools

"""
# 作者: 李沛翔 peixiangli@quanta.org.cn
from .getIsingEnergy import Ising
from .file_J import read_J,tmp_read_J
from . import const

__all__ = ["Ising","read_J","tmp_read_J","const"]