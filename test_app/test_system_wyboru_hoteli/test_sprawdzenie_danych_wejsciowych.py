import pytest
import pandas as pd
import numpy as np

import pathlib
import sys
p = str(pathlib.Path().absolute().joinpath("app/system_wyboru_hoteli").resolve())
if p not in sys.path:
    sys.path.insert(0, p)
import sprawdzenie_danych_wejsciowych


params_czy_granice_kryteriow_sa_poprawne = [
    (
        np.array([0, 0, 0]),
        np.array([1, 2, 3]),
        True
    ),
    (
        np.array([0, 4, 0, 1]),
        np.array([1, 2, 3, 2]),
        False
    ),
    (
        np.array([0, 0, 0]),
        np.array([1, 0, 3]),
        True
    ),
]


@pytest.mark.parametrize("wartosci_minimalne,wartosci_maksymalne,wynik", params_czy_granice_kryteriow_sa_poprawne)
def test_czy_granice_kryteriow_sa_poprawne(
        wartosci_minimalne: np.ndarray, 
        wartosci_maksymalne: np.ndarray,
        wynik: bool
    ):
    v = sprawdzenie_danych_wejsciowych.czy_granice_kryteriow_sa_poprawne(
        wartosci_minimalne, wartosci_maksymalne
    )
    assert v == wynik


params_czy_punkty_w_zbiorze_wzajemnie_niesprzeczne = [
    (
        np.array([
            [0, 0, 0],
            [1, -1, 1],
            [0, 1, -2]
        ]),
        True
    ),
    (
        np.array([
            [0, 0, 0],
            [1, 1, 1],
            [0, 1, -2]
        ]),
        False
    ),
]


@pytest.mark.parametrize("zbior,wynik", params_czy_punkty_w_zbiorze_wzajemnie_niesprzeczne)
def test_czy_punkty_w_zbiorze_wzajemnie_niesprzeczne(
        zbior: np.ndarray,
        wynik: bool
    ):
    v = sprawdzenie_danych_wejsciowych.czy_punkty_w_zbiorze_wzajemnie_niesprzeczne(
        zbior
    )
    assert v == wynik


params_czy_zbiory_wzajemnie_niesprzeczne = [
    (
        np.array([
            [0, 0, 0],
            [1, -1, 1],
            [0, 1, -2]
        ]),
        np.array([
            [10, 10, 10],
            [11, 9, 11],
            [10, 11, 8]
        ]),
        True
    ),
    (
        np.array([
            [0, 0, 0],
            [1, 1, 1],
            [0, 1, -2]
        ]),
        np.array([
            [10, 10, 10],
            [11, 9, 11],
            [-2, -1, -3],
            [10, 11, 8]
        ]),
        False
    ),
]


@pytest.mark.parametrize("zbior_lepszy,zbior_gorszy,wynik", params_czy_zbiory_wzajemnie_niesprzeczne)
def test_czy_zbiory_wzajemnie_niesprzeczne(
        zbior_lepszy: np.ndarray, 
        zbior_gorszy: np.ndarray,
        wynik: bool
    ):
    v = sprawdzenie_danych_wejsciowych.czy_zbiory_wzajemnie_niesprzeczne(
        zbior_lepszy, zbior_gorszy
    )
    assert v == wynik
