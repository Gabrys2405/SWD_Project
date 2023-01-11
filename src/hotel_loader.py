# Autor: Piotr Sikorski

from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Optional, Iterable
    import numpy as np

import pandas as pd


class HotelLoader():

    def __init__(self) -> None:
        # Miejsce przechowywania danych w formie DataFrame
        self._dane: Optional[pd.DataFrame] = None
    

    def _sprawdz_dane(self) -> bool:
        """
        Sprawdza załadowanie danych. 
        Zwraca True, jeśli załadowano pomyślnie.
        Zgłasza wyjątek RuntimeError, jeśli nie załadowano jakiegokolwiek pliku.
        """
        if self._dane is None:
            raise RuntimeError("Nie załadowano pliku z danymi")
        return True


    def zaladuj_excel(self, sciezka_do_pliku: str, *args, **kwargs) -> HotelLoader:
        """
        Ładuje plik formatu Excel i przechowuje go do dalszego przetwarzania.
        Jako dodatkowe argumenty można podawać parametry funkcji pandas.read_excel().
        
        Zwraca siebie, aby można było wykonywać polecenia łańcuchowo.
        """
        self._dane = pd.read_excel(sciezka_do_pliku, *args, **kwargs)
        return self
    

    def zaladuj_csv(self, sciezka_do_pliku: str, *args, **kwargs) -> HotelLoader:
        """
        Ładuje plik formatu CSV i przechowuje go do dalszego przetwarzania.
        Jako dodatkowe argumenty można podawać parametry funkcji pandas.read_csv().
        
        Zwraca siebie, aby można było wykonywać polecenia łańcuchowo.
        """
        if 'sep' not in kwargs.keys():
            # Ustaw domyślny separator na ';'
            kwargs['sep'] = ';'
        
        self._dane = pd.read_csv(sciezka_do_pliku, *args, **kwargs)
        return self
    

    def jako_dataframe(self) -> pd.DataFrame:
        """
        Zwraca załadowane dane jako DataFrame.
        Zgłasza wyjątek, jeśli nie można odczytać danych.
        """
        self._sprawdz_dane()
        return self._dane
    

    def jako_macierz(self, kolumny: Iterable[int | str]) -> np.ndarray:
        """
        Zwraca załadowane dane jako macierz NumPy z kolumn wskazanych w argumentach, nie dodając indeksów.
        'kolumny' można zapisać jako numery indeksów lub ich nazwy.
        Zgłasza wyjątek, jeśli nie można odczytać danych.
        """
        self._sprawdz_dane()
        kols = []
        for k in kolumny:
            if isinstance(k, int):
                kols.append(self._dane.columns[k])
            elif isinstance(k, str):
                kols.append(k)
            else:
                raise RuntimeError("Podano niewłaściwy typ jako kolumnę")
        return self._dane[kols].values