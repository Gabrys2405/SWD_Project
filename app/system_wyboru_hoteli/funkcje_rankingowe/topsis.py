import pandas as pd
from copy import deepcopy

def ranking_topsis(
        kryteria_hoteli: pd.DataFrame,
    ) -> pd.DataFrame:
    """Funkcja tworząca ranking metodą TOPSIS
    
    Parameters
    ----------
    kryteria_hoteli : pd.DataFrame
        DataFrame zawierający wyłącznie minimalizowane kryteria
    
    Returns
    -------
    pd.DataFrame
        DataFrame zawierający jedną kolumnę z wartościami rankingowymi, indeksowanymi
        jak w kryteria_hoteli
    """

    # TODO
    # Podpowiedzi:
    #  - kryteria_hoteli.values jest macierzą NumPy, zmiany w niej wpływają na DataFrame
    #  - kryteria_hoteli.drop(indeks) usuwa wiersz
    #  - kryteria_hoteli.index[i] zwraca indeks do użycia w metodzie drop()
    # Istotne jest, aby zachować pierwotne indeksowanie z kryteria_hoteli

    ranking_list = pd.DataFrame(columns = ['Scoring'],data = [None] * len(kryteria_hoteli))
    kategorie = deepcopy(kryteria_hoteli.values[:, 2:-1])

    for idx_x,kategoria in enumerate(kategorie):
        norma = 0

        for idx_y,wartosc in enumerate(kategoria):
            if wartosc == True: kategorie[idx_x,idx_y] = 1
            elif wartosc == False: kategorie[idx_x,idx_y] = 0.5
            norma += wartosc ** 2
        norma = norma ** (1/2)

        for idx_y,wartosc in enumerate(kategoria):
            kategorie[idx_x,idx_y] /= norma
            #kategorie[idx_x,idx_y] *= wagi[idx_y]

        v_star = [max(kategorie[:,0]),max(kategorie[:,1]),min(kategorie[:,2]),
                  min(kategorie[:,3]),max(kategorie[:,4]),max(kategorie[:,5])]
        v_minus = [min(kategorie[:, 0]), min(kategorie[:, 1]), max(kategorie[:, 2]),
                  max(kategorie[:, 3]),min(kategorie[:, 4]), min(kategorie[:, 5])]
        for i in range(len(kategorie)):
            suma_star,suma_minus = 0,0
            for j in range(len(kategorie[i])):
                suma_star += (v_star[j] - kategorie[i][j]) ** 2
                suma_minus += (v_minus[j] - kategorie[i][j]) ** 2
            ranking_list['Scoring'][i] = suma_star**(1/2)/(suma_minus**(1/2)+suma_star**(1/2))

    return ranking_list
        
