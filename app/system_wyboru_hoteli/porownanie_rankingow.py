#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd

from typing import List

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# from app.system_wyboru_hoteli.funkcje_rankingowe.rsm import ranking_rsm
# from app.system_wyboru_hoteli.funkcje_rankingowe.safety_principle import ranking_safety_principle
# from app.system_wyboru_hoteli.funkcje_rankingowe.topsis import ranking_topsis

# indeksy = [3, 6, 12]

# kryteria_hoteli = pd.DataFrame([
#             (-2, 0),
#             (1, -3),
#             (0, -1)
#         ],
#         index=indeksy,
#         columns=[0, 1]
#     )

# punkty_docelowe = np.array([
#         [-1, 3],
#         [0, 1],
#         [2, 0],
#     ])

# punkty_status_quo = np.array([
#         [-2,0],
#         [-1,-2],
#         [0,-3],
#     ])

# wagi = [0.5,0.5]

# ranking1 = ranking_rsm(kryteria_hoteli, punkty_docelowe,punkty_status_quo)
# ranking2 = ranking_topsis(kryteria_hoteli, wagi)
# ranking3 = ranking_safety_principle(kryteria_hoteli, punkty_docelowe, punkty_status_quo)

# rankings = [ranking1, ranking2, ranking3]

def compare(rank1: pd.DataFrame, rank2: pd.DataFrame):
    # i1 = rank1.index
    # i2 = list(rank2.index)
    d = 0
    for i in range(rank1.shape[0]):
        d += abs(rank1.values[i] - rank2.values[i])
    return d

def drawDistances(methods: List[str], ranks: List[pd.DataFrame]):
    # print(f"{methods = }, {type(methods) = }")
    # print(f"{len(ranks) = }, {type(ranks[0]) = }")
    # print(ranks[0])
    D = np.zeros([len(methods), len(methods)])
    for i in range(D.shape[0]):
        for j in range(D.shape[1]):
            D[i][j] = compare(ranks[i], ranks[j])

    G = nx.Graph()
    for i in range(len(methods)):
        for j in range(D.shape[1]):
            G.add_edge(methods[i], methods[j], weight=D[i][j])

    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 0]
    plt.figure(figsize=(10, 10))
    pos = nx.planar_layout(G)
    # pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=500)
    nx.draw_networkx_edges(G, pos, edgelist=elarge)

    nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    plt.show()
    print(D)


# compare(ranking1, ranking2)
# drawDistances(['RSM', 'Safety Principle', 'Topsis'], [ranking for ranking in rankings])

