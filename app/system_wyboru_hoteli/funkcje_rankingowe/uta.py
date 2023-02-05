from typing import List, Tuple
import numpy as np
import pandas as pd 


def get_Min_Max(data: np.ndarray) -> Tuple[float, float]:
    min = np.min(data,axis=0)
    max = np.max(data,axis=0)

    return min,max

def split(min,max,partitions,max_or_min,func_utility = None):
    comp_list = []
    len_data = len(partitions)
    for i in range(len_data):
        row = [(0,0)]*(partitions[i]+1)
        comp_list.append(row)

    func_utility_max = 1/len_data

    for i in range(len_data):
        if max_or_min[i] == 0:  
            comp_list[i][0] = (min[i],func_utility[i][0])
            comp_list[i][-1] = (max[i],func_utility[i][-1])
            diff = max[i] - min[i]  
            compartment = diff/partitions[i] 
            for j in range(1,partitions[i]):
                comp_list[i][j] = (min[i]+ j*compartment,func_utility[i][j])
        

        if max_or_min[i] == 1:
            comp_list[i][0] = (max[i],func_utility[i][0]) 
            comp_list[i][-1] = (min[i],func_utility[i][-1])
            diff = max[i] - min[i]
            compartment = diff/partitions[i]
            for j in range(1,partitions[i]):
                comp_list[i][j] = (max[i] - j*compartment,func_utility[i][j])

    return comp_list

def function_value(comp_elem,max_or_min):
    comp_list = []
    len_comp = len(comp_elem) - 1
    for i in range(1,len(comp_elem)):
        if max_or_min == 1:
            a = (comp_elem[(len_comp-i+1)][1]-comp_elem[(len_comp-i)][1])/(comp_elem[(len_comp-i+1)][0]-comp_elem[(len_comp-i)][0])
            b = comp_elem[(len_comp-i+1)][1]-a*comp_elem[(len_comp-i+1)][0]
            comp_list.append([a,b])
        
        if max_or_min == 0:
            a = (comp_elem[i-1][1]-comp_elem[i][1])/(comp_elem[i-1][0]-comp_elem[i][0])
            b = comp_elem[(i-1)][1]-a*comp_elem[(i-1)][0]
            comp_list.append([a,b])
    
    return comp_list

def rank(c_utility, comp_elem, point):
    score = 0  
    for i in range(len(comp_elem[0])):
        for j in range(len(comp_elem[i])-1):
            a = point[i]
            x = comp_elem[i][j][0]
            y = comp_elem[i][j+1][0]
            if point[i] <= comp_elem[i][j][0] and point[i] >= comp_elem[i][j+1][0]:
                score += c_utility[i][j][0]*point[i]+c_utility[i][j][1]

            elif point[i] >= comp_elem[i][j][0] and point[i] <= comp_elem[i][j+1][0]:
                score += c_utility[i][j][0]*point[i]+c_utility[i][j][1]

    return score


def ranking_uta(data: pd.DataFrame, wybrane_kolumny: np.ndarray) -> pd.DataFrame:
    # wybrane_kolumny - lista True/False pięciu kolumn, które zostały wybrane do rankingu
    # True oznacza, że kolumna została wybrana, False - że nie
    # Ilość wystąpień True jest równa szerokości (ilości kolumn) tabeli data

    data_matrix = data.to_numpy()
    min_val, max_val = get_Min_Max(data_matrix)
    max_min = [1] * len(data_matrix[0])
    utility = [[0.2,0.16,0.12,0.08,0] for _ in range(len(data_matrix[0]))]
    comp = split(min_val,max_val,max_min,max_min,utility)
    df_utility = pd.DataFrame(data=comp)
    df_utility = df_utility.T
    u = []
    for i in max_min:
        u.append(function_value(comp[i],max_min[i]))

    df_f_val = pd.DataFrame(data=u)
    df_f_val = df_f_val.T
    score = []
    for i in data_matrix:
        score.append(rank(u,comp,i))
    df_score = pd.DataFrame(data=score, index=data.index)
    df_score.sort_values(by=[0], inplace=True, ascending=True)
    return df_score

