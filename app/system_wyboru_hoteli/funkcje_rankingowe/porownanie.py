#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from app.system_wyboru_hoteli.funkcje_rankingowe.rsm import ranking_rsm
from app.system_wyboru_hoteli.funkcje_rankingowe.safety_principle import ranking_safety_principle
from app.system_wyboru_hoteli.funkcje_rankingowe.topsis import ranking_topsis

indeksy = [3, 6, 12]

kryteria_hoteli = pd.DataFrame([
            (-2, 0),
            (1, -3),
            (0, -1)
        ],
        index=indeksy,
        columns=[0, 1]
    )

punkty_docelowe = np.array([
        [-1, 3],
        [0, 1],
        [2, 0],
    ])

punkty_status_quo = np.array([
        [-2,0],
        [-1,-2],
        [0,-3],
    ])

wagi = [0.5,0.5]

ranking1 = ranking_rsm(kryteria_hoteli, punkty_docelowe,punkty_status_quo)
ranking2 = ranking_topsis(kryteria_hoteli, wagi)
ranking3 = ranking_safety_principle(kryteria_hoteli, punkty_docelowe, punkty_status_quo)

def compare(rank1, rank2, type):
    if type == 1:
        i1 = list(rank1.index)
        i2 = list(rank2.index)
        d = 0
        for i in i1:
            d += abs(i1.index(i) - i2.index(i))
        return d

def drawDistances(methods, rank, type):
    D = np.zeros([3,3])
    for i in range(D.shape[0]):
        for j in range(D.shape[1]):
            D[i][j] = compare(methods[i], methods[j], 1)
    print(D)


compare(ranking1, ranking2, 0)
drawDistances([ranking1, ranking2, ranking3],2,3)