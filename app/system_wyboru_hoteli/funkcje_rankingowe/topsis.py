import pandas as pd


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
    raise NotImplementedError()
