#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2021/12/28 21:58
# @Author  : Hao Wu
# @File    : .py
# from classes.basicData.basicData import BasicData
# data = BasicData.basicData
# print(data['trade_dates'])
#
# from classes.options import Vanilla
#
# option = Vanilla.VanillaCall()
# option.calculate_greeks()

import pandas as pd
import numpy as np
a = pd.DataFrame(data=np.random.random((2,3)))
print(a)
print(a.diff().fillna(0)**2)