import numpy as np
import pandas as pd


def square_search(pu, pA0, pA1):
    if pA0.shape == pA1.shape:
        for i in range(pA0.shape[0]):
            if pA0[i] > pA1[i]:
                if pA1[i] > pu[i] or pu[i] > pA0[i]:
                    return False, 0
            elif pA0[i] < pA1[i]:
                if pA0[i] > pu[i] or pu[i] > pA1[i]:
                    return False, 0
            else:
                return False, 0

        return True, np.prod(np.abs(pA0 - pA1))  # multiply

def ranking_rsm(
        kryteria_hoteli: pd.DataFrame,
        punkty_docelowe: np.ndarray,
        punkty_status_quo: np.ndarray
    ) -> pd.DataFrame:
    """Funkcja tworząca ranking metodą RSM
    
    Parameters
    ----------
    kryteria_hoteli : pd.DataFrame
        DataFrame zawierający wyłącznie minimalizowane kryteria
    punkty_docelowe : np.ndarray
        Punkty docelowe dla metody RSM
    punkty_status_quo : np.ndarray
        Punkty status-quo dla metody RSM
    
    Returns
    -------
    pd.DataFrame
        DataFrame zawierający jedną kolumnę z wartościami rankingowymi, indeksowanymi
        jak w kryteria_hoteli
    """
    wartosci_funkcji_kryterialnej = np.zeros((kryteria_hoteli.values.shape[0],))
    # print(wartosci_funkcji_kryterialnej)
    for iu in range(kryteria_hoteli.values.shape[0]):
        u = kryteria_hoteli.values[iu, :]  # punkt u - do określenia wartości

        suma_pol = 0  # suma pól prostokątów
        pary_wektorow_prostokatow = []  # wektory tworzące potrzebne prostokąty
        pola_prostokatow = []  # pola prostokątów powyżej

        # Szukaj par wierzchołków tworzących prostokąty zawierające punkt u
        for iA0 in range(punkty_docelowe.shape[0]):
            vA0 = punkty_docelowe[iA0, :]
            for iA1 in range(punkty_status_quo.shape[0]):
                vA1 = punkty_status_quo[iA1, :]
                w_prostokacie, pole = square_search(u, vA0, vA1)
                if w_prostokacie:
                    suma_pol += pole
                    pary_wektorow_prostokatow.append((vA0, vA1))
                    pola_prostokatow.append(pole)

        # Zliczenie wag prostokątów
        wagi: np.ndarray = np.array(pola_prostokatow) / suma_pol

        # Zliczenie odległości punktów prostokątów
        odleglosci = []
        for vA0, vA1 in pary_wektorow_prostokatow:
            dA0 = np.sqrt(np.sum((vA0 - u) ** 2))
            dA1 = np.sqrt(np.sum((vA1 - u) ** 2))
            odleglosci.append(dA0 / (dA0 + dA1))

        # Złożenie do wartości funkcji kryterialnej
        wartosci_funkcji_kryterialnej[iu] = np.sum(wagi * np.array(odleglosci))

    # #ranking
    pozycja = np.array(range(wartosci_funkcji_kryterialnej.shape[0])) + 1
    ranking = np.array([pozycja, wartosci_funkcji_kryterialnej]).T
    # ranking = ranking[ranking[:, 1].argsort()[::-1]]
    ranking = ranking[:,1:]
    # print(ranking)
    ranking = pd.DataFrame(ranking, index = kryteria_hoteli.index)
    ranking.sort_values(by=[0], inplace=True, ascending=True)
    # print(ranking)
    return ranking


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

# ranking = ranking_rsm(
#         kryteria_hoteli,
#         punkty_docelowe,
#         punkty_status_quo
#     )


# print(ranking)