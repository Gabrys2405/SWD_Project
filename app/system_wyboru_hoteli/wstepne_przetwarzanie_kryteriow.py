from typing import List
import numpy as np
import pandas as pd


def filtruj_hotele__wartosci_kryteriow_minimalne_i_maksymalne(
        kryteria_hoteli: pd.DataFrame,
        wartosci_minimalne: np.ndarray,
        wartosci_maksymalne: np.ndarray
    ) -> pd.DataFrame:
    """Filtruje hotele ze względu na wartości min i max kryteriów.
    
    Funkcja przyjmuje DataFrame z wyłącznie kryteriami hoteli (bez darmowego parkingu 
    i danych w stylu nazwy hotelu) i zwraca te hotele, które mieszczą się pomiędzy 
    wartościami granicznymi. Należy zastosować nierówność słabą (mniejszy lub równy,
    większy lub równy).

    Parameters
    ----------
    kryteria_hoteli : pd.DataFrame
        DataFrame zawierający kryteria
    wartosci_minimalne : np.ndarray
        Minimalne wartości kryteriów
    wartosci_maksymalne : np.ndarray
        Maksymalne wartości kryteriów
    
    Returns
    -------
    pd.DataFrame
        DataFrame zawierający kryteria hoteli mieszczące się w wartościach granicznych
    """

    # TODO
    # Podpowiedzi:
    #  - kryteria_hoteli.values jest macierzą NumPy, zmiany w niej wpływają na DataFrame
    #  - kryteria_hoteli.drop(indeks) usuwa wiersz
    #  - kryteria_hoteli.index[i] zwraca indeks do użycia w metodzie drop()
    # Istotne jest, aby zachować pierwotne indeksowanie z kryteria_hoteli
    raise NotImplementedError()


def filtruj_hotele__czy_parking_darmowy(
        wszystkie_dane_hoteli: pd.DataFrame,
        kryteria_hoteli: pd.DataFrame,
        czy_parking_musi_byc_darmowy: bool
    ) -> pd.DataFrame:
    """Filtruje hotele ze względu na obecność darmowego parkingu.
    
    Funkcja przyjmuje DataFrame z kryteriami hoteli bez darmowego parkingu 
    i danych w stylu nazwy hotelu, dlatego dodatkowo podawane są wszystkie dane hoteli.
    Obydwa DataFrame'y posiadają to samo indeksowanie.

    Jeśli ma być obecny darmowy parking, zwracane są tylko te rekordy z kryteria_hoteli,
    które spełniają ten wymóg. W przeciwnym wypadku kryteria_hoteli zwracana jest bez zmian.

    Parameters
    ----------
    wszystkie_dane_hoteli : pd.DataFrame
        DataFrame wszystkich hoteli z ich wszystkimi informacjami
    kryteria_hoteli : pd.DataFrame
        DataFrame zawierający wyłącznie kryteria
    czy_parking_musi_byc_darmowy : bool
        Warunek posiadania darmowego parkingu
    
    Returns
    -------
    pd.DataFrame
        DataFrame zawierający kryteria hoteli spełniające warunki parkingu
    """

    # TODO
    # Podpowiedzi:
    #  - kryteria_hoteli.drop(indeks) usuwa wiersz
    #  - kryteria_hoteli.index[i] zwraca indeks do użycia w metodzie drop()
    # Istotne jest, aby zachować pierwotne indeksowanie z kryteria_hoteli
    raise NotImplementedError()


# Indeksy kolumn kryterialnych, które należy zmienić na minimalizację
kolumny_do_zmiany_na_minimalizacje: List[int] = [0, 1, 4]


def zamien_maksymalizacje_na_minimalizacje(
        kryteria_hoteli: pd.DataFrame,
    ) -> pd.DataFrame:
    """Zmienia wartości kryteriów, aby wszystkie mogły być minimalizowane.
    
    Niektóre kryteria (np. oceny) są maksymalizowane z natury. Dla ułatwienia
    pracy, ta funkcja zamienia wartości kryteriów tak, aby mogły być minimalizowane.

    Ponieważ jedynymi kolumnami maksymalizowanymi są te z oceną, każdą z nich
    można potraktować jednakowo, wzorem: 
        v = 10 - v
    gdzie v jest wartością danego kryterium.

    Parameters
    ----------
    kryteria_hoteli : pd.DataFrame
        DataFrame zawierający wyłącznie kryteria
    
    Returns
    -------
    pd.DataFrame
        DataFrame zawierający kryteria hoteli poprawione na minimalizację
    """

    # TODO
    # Podpowiedzi:
    #  - kryteria_hoteli.values jest macierzą NumPy, zmiany w niej wpływają na DataFrame
    raise NotImplementedError()


def wyznacz_punkty_niezdominowane(
        kryteria_hoteli: pd.DataFrame,
    ) -> pd.DataFrame:
    """Wyznacza punkty niezdominowane ze zbioru wszystkich punktów.
    
    Funkcja wyznacza punkty niezdominowane ze zbioru punktów kryteria_hoteli
    i zwraca je.

    Parameters
    ----------
    kryteria_hoteli : pd.DataFrame
        DataFrame zawierający wyłącznie minimalizowane kryteria
    
    Returns
    -------
    pd.DataFrame
        DataFrame zawierający niezdominowane kryteria hoteli
    """

    # TODO
    # Podpowiedzi:
    #  - kryteria_hoteli.values jest macierzą NumPy, zmiany w niej wpływają na DataFrame
    #  - kryteria_hoteli.drop(indeks) usuwa wiersz
    #  - kryteria_hoteli.index[i] zwraca indeks do użycia w metodzie drop()
    # Istotne jest, aby zachować pierwotne indeksowanie z kryteria_hoteli
    raise NotImplementedError()
