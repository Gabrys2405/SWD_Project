import pytest
import pandas as pd
import numpy as np

import pathlib
import sys
p = str(pathlib.Path().absolute().joinpath("app/system_wyboru_hoteli").resolve())
if p not in sys.path:
    sys.path.insert(0, p)

import wstepne_przetwarzanie_kryteriow
# from app.system_wyboru_hoteli.funkcje_rankingowe.rsm import ranking_rsm


def test_filtruj_hotele__wartosci_kryteriow_minimalne_i_maksymalne():
    """Test daje możliwość podstawowej weryfikacji kodu."""

    indeksy = [3, 6, 12]

    kryteria_hoteli = pd.DataFrame([
            (-2, 0),
            (1, -3),
            (0, -1)
        ], 
        index=indeksy,
        columns=[0, 1]
    )

    wartosci_minimalne: np.ndarray = np.array(
        [-1, -5],
    )

    wartosci_maksymalne: np.ndarray = np.array(
        [5,-1],
    )

    ranking = wstepne_przetwarzanie_kryteriow.filtruj_hotele__wartosci_kryteriow_minimalne_i_maksymalne(
        kryteria_hoteli,
        wartosci_minimalne,
        wartosci_maksymalne
    )

    assert isinstance(ranking, pd.DataFrame), "Zwracany ranking nie jest DataFrame'm"

    ranking_indeksy = list(ranking.index).sort()
    assert indeksy == ranking_indeksy, "Nie zachowano indeksowania z 'kryteria_hoteli'"

    # Sprawdzenie wyniku
    assert (ranking.values == np.array([1, -3])).all()


def test_zamien_maksymalizacje_na_minimalizacje():

    indeksy = [3, 6]

    kryteria_hoteli = pd.DataFrame([
            (1, 9.5),
            (0, 10)
        ], 
        index=indeksy,
        columns=[0, 1]
    )

    v = wstepne_przetwarzanie_kryteriow.zamien_maksymalizacje_na_minimalizacje(
        kryteria_hoteli, [1]
    )

    assert isinstance(v, pd.DataFrame), "Zwracany obiekt nie jest DataFrame'm"

    ranking_indeksy = list(v.index).sort()
    assert indeksy == ranking_indeksy, "Nie zachowano indeksowania z 'kryteria_hoteli'"

    # Sprawdzenie wyniku
    assert (v.values == np.array([
        [1, 0.5],
        [0, 0],
    ])).all()


def test_wyznacz_punkty_niezdominowane():

    indeksy = list(range(1, 5)) + list(range(10, 20))

    kryteria_hoteli = pd.DataFrame(np.array([
        [4, 4],
        [5, 4],
        [-2, 0],
        [0, 1],
        [2, 1],
        [1, -3],
        [4, 1],
        [3, 2],
        [3, 3],
        [3, -1],
        [-1, 1],
        [0, -1],
        [4, -2],
        [-1, 3],
    ]), 
        index=indeksy,
        columns=[0, 1]
    )

    v = wstepne_przetwarzanie_kryteriow.zamien_maksymalizacje_na_minimalizacje(
        kryteria_hoteli, [1]
    )

    assert isinstance(v, pd.DataFrame), "Zwracany obiekt nie jest DataFrame'm"

    ranking_indeksy = list(v.index).sort()
    assert indeksy == ranking_indeksy, "Nie zachowano indeksowania z 'kryteria_hoteli'"

    # Sprawdzenie wyniku
    assert (v.values == np.array([
        [-2,  0],
        [ 1, -3],
        [ 0, -1]
    ])).all()
