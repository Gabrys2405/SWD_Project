# Autor główny: Piotr Sikorski
from __future__ import annotations 
from typing import Dict, Optional, List
import copy
import numpy as np
import pandas as pd
import wyjatki
import sprawdzenie_danych_wejsciowych
import wstepne_przetwarzanie_kryteriow
import funkcje_rankingowe

# Indeksy kolumn, które zawierają dane kryterialne
kolumny_kryteriow: List[int] = [2, 3, 4, 5, 7]

def indeksy_na_kolumny(df: pd.DataFrame, indeksy: List[int]) -> pd.Index:
    return [df.columns[i] for i in indeksy]


class ZbiorDanych():
    """Klasa zbierająca dane do dalszego przetwarzania."""

    def __init__(self, dane_hoteli: pd.DataFrame) -> None:
        # === Parametry === #

        # Dane wszystkich hoteli
        self.dane_hoteli = dane_hoteli

        nazwy_kolumn = indeksy_na_kolumny(self.dane_hoteli, kolumny_kryteriow)

        self.wybrane_kryteria = pd.DataFrame([(True, True, True, True, True)], columns=nazwy_kolumn)

        self.minimalne_kryteria = pd.DataFrame([(0, 0, 0, 0, 0)], columns=nazwy_kolumn)
        self.maksymalne_kryteria = pd.DataFrame([(10, 10, 10000, 10, 10)], columns=nazwy_kolumn)

        self.punkty_docelowe = pd.DataFrame([(10, 10, 0, 0, 10)], columns=nazwy_kolumn)
        self.punkty_status_quo = pd.DataFrame([(0, 0, 10000, 10, 0)], columns=nazwy_kolumn)

        self.czy_parking_musi_byc_darmowy: bool = False

        # === Cache === #

        # DataFrame zawierający wyłacznie kryteria pasujących 
        # i niezdominowanych hoteli 
        # Można utworzyć macierz z samymi kryteriami
        kolumny = indeksy_na_kolumny(self.dane_hoteli, kolumny_kryteriow)
        self.kryteria_hoteli = self.dane_hoteli[kolumny]
    

    def kopia_z_wybranymi_kryteriami(self) -> ZbiorDanych:
        """Zwraca nowy zbiór danych, ale posiadający kolumny danych tylko wybranych przez użytkownika"""
        kolumny = []
        for nazwa, czy_uwzgledniana in zip(self.kryteria_hoteli.columns, self.wybrane_kryteria):
            if czy_uwzgledniana:
                kolumny.append(nazwa)
        
        kopia = copy.copy(self)  # unikam niepotrzebnego tworzenia całości klasy
        nazwy_parametrow: List[str] = [
            "wybrane_kryteria", "minimalne_kryteria", "maksymalne_kryteria",
            "punkty_docelowe", "punkty_status_quo"
        ]
        for nazwa in nazwy_parametrow:
            df: pd.DataFrame = getattr(self, nazwa)
            setattr(kopia, nazwa, df[kolumny])
        
        return kopia


class SystemWyboruHoteli():
    """Klasa zbierająca funkcjonalność systemu wyboru hoteli.
    
    Klasa zbiera w jednym miejscu całe przetwarzanie danych koniecznych do 
    wyboru odpowiedniego hotelu. Zawiera metody przetwarzające i przechowuje
    wyniki działań.
    """

    def __init__(self) -> None:
        # Oryginalne dane systemu, tworzone podczas ładowania bazy
        self.dane: Optional[ZbiorDanych] = None

        # Modyfikowane dane podczas tworzenia rankingów
        # Zawierają tylko kolumny wybrane przez użytkownika
        self._dane_przetwarzane: Optional[ZbiorDanych] = None

        # === Wyniki === #
        # Słownik mapujący nazwę metody do jej rankingu
        self.rankingi_metod: Optional[Dict[str, pd.DataFrame]] = None
        pass


    def zaladuj_dane(self, dane_hoteli: pd.DataFrame):
        """Tworzy DataFrame'y na podstawie danych hoteli"""
        self.dane = ZbiorDanych(dane_hoteli)
        

    def wykonaj_wszystkie_obliczenia(self) -> None:
        """Funkcja wykonująca wszystkie kalkulacje do rankingów.

        Funkcja przetwarza wcześniej wprowadzone do niej dane, aby zapisać
        w sobie rankingi z nich wynikające. Zgłasza wiele wyjątków, najczęściej 
        dla niepoprawnych danych. 
        """

        self._sprawdz_poprawnosc_danych()
        self._wykonaj_przetwarzanie_kryteriow()
        self._wygeneruj_rankingi()


    def _sprawdz_poprawnosc_danych(self):

        # Czy wprowadzono w ogóle dane?
        nazwy_parametrow: List[str] = [
            "dane_hoteli", "wybrane_kryteria", "minimalne_kryteria", "maksymalne_kryteria",
            "punkty_docelowe", "punkty_status_quo"
        ]
        for nazwa in nazwy_parametrow:
            if getattr(self.dane, nazwa) is None:
                raise wyjatki.BrakInicjalizacjiParametru(nazwa)
        

        # Sprawdzenie poprawności danych

        # Szerokości macierzy
        szerokosc_oczekiwana: int = self.kryteria_hoteli.shape[1]
        nazwy_parametrow: List[str] = [
            "wybrane_kryteria", "minimalne_kryteria", "maksymalne_kryteria",
            "punkty_docelowe", "punkty_status_quo"
        ]
        for nazwa in nazwy_parametrow:
            szerokosc: int = getattr(self.dane, nazwa).shape[1]
            if szerokosc != szerokosc_oczekiwana:
                raise wyjatki.NiepoprawnaSzerokoscMacierzy(nazwa, szerokosc, szerokosc_oczekiwana)
        
        # Wybrano co najmniej jedno kryterium
        if np.sum(self.dane.wybrane_kryteria.values.astype("int")) < 1:
            raise wyjatki.BladDanychUzytkownika("Wybrano za małą ilość kryteriów")


        # W tym miejscu możesz wybrać tylko kolumny wybrane przez użytkownika
        self._dane_przetwarzane = self.dane.kopia_z_wybranymi_kryteriami()
        dane = self._dane_przetwarzane

        # Granice kryteriów
        if not sprawdzenie_danych_wejsciowych.czy_granice_kryteriow_sa_poprawne(
            dane.minimalne_kryteria.values, 
            dane.maksymalne_kryteria.values
        ):
            raise wyjatki.BladDanychUzytkownika("Kryteria minimalne i maksymalne są sprzeczne")
        
        # Niesprzeczności zbiorów
        if not sprawdzenie_danych_wejsciowych.czy_punkty_w_zbiorze_wzajemnie_niesprzeczne(
            dane.punkty_docelowe.values
        ):
            raise wyjatki.BladDanychUzytkownika("Punkty w zbiorze punktów docelowych są wzajemnie sprzeczne")
        if not sprawdzenie_danych_wejsciowych.czy_punkty_w_zbiorze_wzajemnie_niesprzeczne(
            dane.punkty_status_quo.values
        ):
            raise wyjatki.BladDanychUzytkownika("Punkty w zbiorze punktów status-quo są wzajemnie sprzeczne")
        if not sprawdzenie_danych_wejsciowych.czy_zbiory_wzajemnie_niesprzeczne(
            dane.punkty_docelowe.values, 
            dane.punkty_status_quo.values
        ):
            raise wyjatki.BladDanychUzytkownika("Zbiory punktów docelowych i status-quo są wzajemnie sprzeczne") 

        # Wszystko poprawne
        return
    

    def _wykonaj_przetwarzanie_kryteriow(self):
        dane = self._dane_przetwarzane
        kryteria_hoteli = dane.kryteria_hoteli

        kryteria_hoteli = wstepne_przetwarzanie_kryteriow.filtruj_hotele__czy_parking_darmowy(
            dane.dane_hoteli, kryteria_hoteli, dane.czy_parking_musi_byc_darmowy
        )

        kryteria_hoteli = wstepne_przetwarzanie_kryteriow.filtruj_hotele__wartosci_kryteriow_minimalne_i_maksymalne(
            kryteria_hoteli, dane.minimalne_kryteria.values, dane.maksymalne_kryteria.values
        )

        kryteria_hoteli = wstepne_przetwarzanie_kryteriow.zamien_maksymalizacje_na_minimalizacje(
            kryteria_hoteli
        )

        kryteria_hoteli = wstepne_przetwarzanie_kryteriow.wyznacz_punkty_niezdominowane(
            kryteria_hoteli
        )

        self._dane_przetwarzane.kryteria_hoteli = kryteria_hoteli
    

    def _wygeneruj_rankingi(self):
        dane = self._dane_przetwarzane
        self.rankingi_metod = {
            'topsis': funkcje_rankingowe.ranking_topsis(
                dane.kryteria_hoteli
            ),
            'rsm': funkcje_rankingowe.ranking_rsm(
                dane.kryteria_hoteli, 
                dane.punkty_docelowe.values,
                dane.punkty_status_quo.values
            )
        }
    
