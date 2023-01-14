import numpy as np
import pandas as pd


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

    # TODO
    # Podpowiedzi:
    #  - kryteria_hoteli.values jest macierzą NumPy, zmiany w niej wpływają na DataFrame
    #  - kryteria_hoteli.drop(indeks) usuwa wiersz
    #  - kryteria_hoteli.index[i] zwraca indeks do użycia w metodzie drop()
    # Istotne jest, aby zachować pierwotne indeksowanie z kryteria_hoteli
    raise NotImplementedError()
