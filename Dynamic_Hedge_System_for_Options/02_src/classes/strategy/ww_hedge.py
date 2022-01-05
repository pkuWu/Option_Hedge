#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2021/12/29 21:46
# @Author  : Hao Wu
# @File    : ww_hedge.py
from .strategyBase import StrategyBase
from ..options import Vanilla

class WW_Hedge(StrategyBase):
    def __init__(self):
        super(WW_Hedge, self).__init__()

    def H0(self,greek_df):
        pass




