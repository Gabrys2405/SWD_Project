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
    columns = kryteria_hoteli.columns
    for i, column in enumerate(columns):
        kryteria_hoteli = kryteria_hoteli[
            (kryteria_hoteli[column] < wartosci_maksymalne[i]) & 
            (kryteria_hoteli[column] > wartosci_minimalne[i])]
    return kryteria_hoteli

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
    return kryteria_hoteli[wszystkie_dane_hoteli["Bezpłatny parking "] == czy_parking_musi_byc_darmowy]


# Indeksy kolumn kryterialnych, które należy zmienić na minimalizację
kolumny_do_zmiany_na_minimalizacje: List[int] = ["Opinia", "Opinia dla lokalizacji", "Komfort "]

def zamien_maksymalizacje_na_minimalizacje(
        kryteria_hoteli: pd.DataFrame,
        kolumny_do_zmiany_na_minimalizacje: List[int]
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
    kolumny_do_zmiany_na_minimalizacje : List[int]
        Indeksy kolumn kryterialnych, które należy zmienić na minimalizację
    
    Returns
    -------
    pd.DataFrame
        DataFrame zawierający kryteria hoteli poprawione na minimalizację
    """
    for column in kolumny_do_zmiany_na_minimalizacje:
        kryteria_hoteli[column] = [10 - i for i in kryteria_hoteli[column]]
    return kryteria_hoteli


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
    undominated_points = pd.DataFrame()
    for index, row in kryteria_hoteli.iterrows():
        dominated = False
        for index2, row2 in kryteria_hoteli.iterrows():
            if all(row2[column] <= row[column] for column in kryteria_hoteli.columns) and any(row2[column] < row[column] for column in kryteria_hoteli.columns):
                dominated = True
                break
        if not dominated:
            undominated_points = undominated_points.append(row)
    return undominated_points
