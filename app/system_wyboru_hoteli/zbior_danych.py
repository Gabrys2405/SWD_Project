from __future__ import annotations 
from typing import List
import copy
import pandas as pd
import numpy as np


class ZbiorDanych():
    """Klasa zbierająca dane do dalszego przetwarzania."""

    # Indeksy kolumn, które zawierają dane kryterialne
    kolumny_kryteriow: List[int] = [2, 3, 4, 5, 7]


    @staticmethod
    def indeksy_na_kolumny(df: pd.DataFrame, indeksy: List[int]) -> pd.Index:
        return [df.columns[i] for i in indeksy]


    def __init__(self, dane_hoteli: pd.DataFrame) -> None:
        # === Parametry === #

        # Dane wszystkich hoteli
        self.dane_hoteli = dane_hoteli

        nazwy_kolumn = self.indeksy_na_kolumny(self.dane_hoteli, self.kolumny_kryteriow)

        self.wybrane_kryteria = pd.DataFrame([(True, True, True, True, True)], columns=nazwy_kolumn)

        self.minimalne_kryteria = pd.DataFrame([(0.0, 0, 0, 0, 0)], columns=nazwy_kolumn)
        self.maksymalne_kryteria = pd.DataFrame([(10.0, 10, 10000, 10, 10)], columns=nazwy_kolumn)

        self.punkty_docelowe = pd.DataFrame([(10.0, 10, 0, 0, 10)], columns=nazwy_kolumn)
        self.punkty_status_quo = pd.DataFrame([(0.0, 0, 10000, 10, 0)], columns=nazwy_kolumn)

        self.czy_parking_musi_byc_darmowy: bool = False
        
        self.usun_punkty_zdominowane: bool = False

        # === Cache === #

        # DataFrame zawierający wyłacznie kryteria pasujących 
        # i niezdominowanych hoteli 
        # Można utworzyć macierz z samymi kryteriami
        self.kryteria_hoteli = self.dane_hoteli[nazwy_kolumn]

        self.kolumny_maks_na_min = pd.DataFrame([(True, True, False, False, True)], columns=nazwy_kolumn)
    
    
    @property
    def kolumny_maks_na_min__lista(self) -> List[int]:
        return list(np.where(self.kolumny_maks_na_min)[-1])


    def kopia_z_wybranymi_kryteriami(self) -> ZbiorDanych:
        """Zwraca nowy zbiór danych, ale posiadający kolumny danych tylko wybranych przez użytkownika"""
        kolumny = []
        for nazwa, czy_uwzgledniana in zip(self.kryteria_hoteli.columns, self.wybrane_kryteria.values[0, :]):
            if czy_uwzgledniana:
                kolumny.append(nazwa)
        
        kopia = copy.copy(self)  # unikam niepotrzebnego tworzenia całości klasy
        nazwy_parametrow: List[str] = [
            "wybrane_kryteria", "minimalne_kryteria", "maksymalne_kryteria",
            "punkty_docelowe", "punkty_status_quo", "kolumny_maks_na_min",
            "kryteria_hoteli"
        ]
        for nazwa in nazwy_parametrow:
            df: pd.DataFrame = getattr(self, nazwa)
            setattr(kopia, nazwa, df[kolumny])
        
        return kopia

    def __repr__(self) -> str:
        s = f"{self.dane_hoteli.shape = }, {self.kryteria_hoteli.shape = }\n"
        s += f"    Min. kryteria: \n{self.minimalne_kryteria}\n"
        s += f"    Max. kryteria: \n{self.maksymalne_kryteria}\n"
        s += f"    P. docelowe: \n{self.punkty_docelowe}\n"
        s += f"    P. status-quo: \n{self.punkty_status_quo}\n"
        s += f"    Kryteria hoteli: \n{self.kryteria_hoteli}\n"
        return s
