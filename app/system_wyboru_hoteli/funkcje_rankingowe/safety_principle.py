import numpy as np
import pandas as pd


def ranking_safety_principle(
        kryteria_hoteli: pd.DataFrame,
        punkty_docelowe: np.ndarray,
        punkty_status_quo: np.ndarray
    ) -> pd.DataFrame:
    """Funkcja tworząca ranking metodą Safety Principle
    
    Parameters
    ----------
    kryteria_hoteli : pd.DataFrame
        DataFrame zawierający wyłącznie minimalizowane kryteria
    punkty_docelowe : np.ndarray
        Punkty docelowe dla metody SP
    punkty_status_quo : np.ndarray
        Punkty status-quo dla metody SP
    
    Returns
    -------
    pd.DataFrame
        DataFrame zawierający jedną kolumnę z wartościami rankingowymi, indeksowanymi
        jak w kryteria_hoteli, posortowana względem jakości rankingu (najlepsze jako pierwsze)
    """

    # TODO
    raise NotImplementedError()
